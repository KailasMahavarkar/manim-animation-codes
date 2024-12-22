from functools import wraps
from time import time
import inspect
import copy
from typing import Dict, List, Any
import uuid
from table_print import TreePrinter

MAX_FRAMES = 1000
MAX_TIME = 10


class TooManyFramesError(Exception):
    pass


class TooMuchTimeError(Exception):
    pass


class callgraph(object):
    """Singleton class that stores global graph data"""

    _callers: Dict[int, Any] = {}  # caller_fn_id : node_data
    _counter = 1  # track call order
    _unwindcounter = 1  # track unwind order
    _step = 1  # track overall steps
    _frames: List[int] = []  # keep frame objects reference
    _tree = None

    @staticmethod
    def reset():
        callgraph._callers = {}
        callgraph._counter = 1
        callgraph._frames = []
        callgraph._unwindcounter = 1
        callgraph._step = 1

    @staticmethod
    def get_callers():
        return callgraph._callers

    @staticmethod
    def increment():
        callgraph._counter += 1
        callgraph._step += 1

    @staticmethod
    def increment_unwind():
        callgraph._unwindcounter += 1
        callgraph._step += 1

    @staticmethod
    def get_frames():
        return callgraph._frames

    @staticmethod
    def get_graph_dictionary():
        """Constructs the graph as a nested dictionary representing a tree of nodes."""
        graph_dict = {
            key: {
                "uuid": uuid.uuid4().hex,
                "fn_name": value.fn_name,
                "args": value.args,
                "kwargs": value.kwargs,
                "ret": value.ret,
                "child_methods": value.child_methods
            }
            for key, value in callgraph.get_callers().items()
        }

        def build_node(node_id):
            """Recursively build a node and its children."""
            node = graph_dict[node_id]
            return {
                "uuid": node["uuid"],
                "fn_name": node["fn_name"],
                "args": node["args"],
                "kwargs": node["kwargs"],
                "ret": node["ret"],
                "children": [
                    build_node(child_id)
                    for child_id, _ in node["child_methods"]
                ]
            }

        # Find the root nodes (nodes without parent references)
        root_nodes = [
            key
            for key in graph_dict.keys()
            if not any(key in [child[0] for child in node["child_methods"]] for node in graph_dict.values())
        ]

        # Build the graph starting from root nodes
        tree = [build_node(root) for root in root_nodes]

        global _tree
        _tree = tree
        return tree

    @staticmethod
    def get_graph_representation():
        """Return a text-based representation of the graph for logging or debugging."""
        lines = []
        for frame_id, node in callgraph.get_callers().items():
            args = node.argstr()
            ret = f" -> {node.ret}" if node.ret is not None else ""
            lines.append(f"{node.fn_name}({args}){ret}")
            for child_id, counter in node.child_methods:
                child_node = callgraph.get_callers().get(child_id)
                if child_node:
                    child_args = child_node.argstr()
                    lines.append(f"  Step {counter}: Calls {child_node.fn_name}({child_args})")
        return "\n".join(lines)

    @staticmethod
    def pretty(indent=0, prefix="", colors=None):
        """
        Recursively prints a tree structure of a function call stack with colored levels.

        :param tree: A list containing recursion tree nodes.
        :param indent: Current indentation level.
        :param prefix: Prefix to append before function details.
        :param colors: List of colors to cycle through for different depths.
        """
        # Default color palette (ANSI escape sequences)
        color_palette = [
            "\033[37m",  # White
            "\033[91m",  # Red
            "\033[92m",  # Green
            "\033[93m",  # Yellow
            "\033[94m",  # Blue
            "\033[95m",  # Magenta
            "\033[96m",  # Cyan
        ]
        colors = colors or color_palette

        def inner(tree, indent, depth):
            # Cycle through colors for each depth
            color = colors[depth % len(colors)]
            reset_color = "\033[0m"
            for node in tree:
                # Print the current node with its color
                print(f"{' ' * indent}{color}{prefix}└── {node['fn_name']}({
                      ', '.join(map(str, node['args']))}){reset_color}")
                # Recurse for children
                if 'children' in node and node['children']:
                    inner(node['children'], indent + 4, depth + 1)

        # Start recursion
        inner(_tree, indent, 0)

    @staticmethod
    def pretty_table(ignore_args_list=[]):
        TreePrinter().table(_tree, ignore_args_list=ignore_args_list)


class node_data(object):
    def __init__(self, _args=None, _kwargs=None, _fn_name=""):
        self.args = _args
        self.kwargs = _kwargs
        self.fn_name = _fn_name
        self.ret = None
        self.child_methods = []  # List to store children (recursive calls)

    def argstr(self):
        s_args = ", ".join([str(arg) for arg in self.args])
        s_kwargs = ", ".join([(str(k), str(v))
                             for (k, v) in self.kwargs.items()])
        return f"{s_args}{s_kwargs}".replace("{", "\\{").replace("}", "\\}")


class viz(object):
    """decorator to construct the call graph with args and return values as labels"""

    def __init__(self, wrapped):
        self.wrapped = wrapped
        self.max_frames = MAX_FRAMES
        self.max_time = MAX_TIME  # in seconds
        self.start_time = time()

    def __call__(self, *args, **kwargs):
        g_callers = callgraph.get_callers()
        g_frames = callgraph.get_frames()

        # find the caller frame, and add self as a child node
        caller_frame_id = None

        fullstack = inspect.stack()

        this_frame_id = id(fullstack[0][0])
        if len(fullstack) > 2 and fullstack[2].function == "__call__":
            caller_frame_id = id(fullstack[2][0])

        if this_frame_id not in g_frames:
            g_frames.append(fullstack[0][0])

        if this_frame_id not in g_callers.keys():
            g_callers[this_frame_id] = node_data(
                copy.deepcopy(args), copy.deepcopy(
                    kwargs), self.wrapped.__name__
            )

        edgeinfo = None
        if caller_frame_id:
            edgeinfo = [this_frame_id, callgraph._step]
            g_callers[caller_frame_id].child_methods.append(edgeinfo)
            callgraph.increment()

        if len(g_frames) > self.max_frames:
            raise TooManyFramesError(
                f"Encountered more than ${
                    self.max_frames} while executing function"
            )
        if (time() - self.start_time) > self.max_time:
            raise TooMuchTimeError(
                f"Took more than ${self.max_time} seconds to run function")

        # Invoke the wrapped
        ret = self.wrapped(*args, **kwargs)

        g_callers[this_frame_id].ret_step = callgraph._step

        if edgeinfo:
            callgraph.increment_unwind()

        g_callers[this_frame_id].ret = copy.deepcopy(ret)

        return ret


def decorate_funcs(func_source: str):
    outlines = []
    for line in func_source.split("\n"):
        if line.startswith("def "):
            outlines.append("@viz")
        outlines.append(line)

    return "\n".join(outlines)


def visualize(function_definition, function_call, as_dict=False):
    """Either returns generated text representation or raises an error."""
    callgraph.reset()
    function_definition = decorate_funcs(function_definition)
    exec(function_definition, globals())
    eval(function_call)

    if as_dict:
        return callgraph.get_graph_dictionary()
    return callgraph.get_graph_representation()


def base_recursion_tree(func):
    """
    A single decorator to visualize recursive or nested function calls
    as a tree structure.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        global current_depth
        is_root_call = current_depth == 0

        if is_root_call:
            print(f"Visualizing execution tree for {func.__name__}:\n")

        prefix = "    " * current_depth + "└── "
        print(f"{prefix}{func.__name__}({', '.join(map(str, args))})")

        current_depth += 1
        result = func(*args, **kwargs)
        current_depth -= 1

        if is_root_call:
            print(f"\nExecution tree complete. Final result: {result}")

        return result
    return wrapper


# def external_call():
#     # This works as before
#     factorial_function = """
# def factorial(n):
#     if n == 0:
#         return 1
#     return n * factorial(n - 1)
#     """

#     # Call the factorial function
#     function_call = "factorial(3)"
#     call_graph = visualize(factorial_function, function_call)
#     return call_graph


def internal_call():
    callgraph.reset()

    @viz
    def factorial(n):
        if n <= 1:
            return n

        return factorial(n - 1) + factorial(n - 2)
    factorial(3)

    return callgraph.get_graph_dictionary()


def convert_to_adj_list(graph):
    adj_list = {}
    node_counter = 0  # To generate unique IDs for each node

    def add_node(node, parent=None):
        nonlocal node_counter

        # Generate a unique ID for the node (you can use the function name + arguments as ID)
        node_id = f"{node['fn_name']}({', '.join(map(str, node['args']))})"

        if node_id not in adj_list:
            adj_list[node_id] = []

        # Add the parent-child relationship in the adjacency list
        if parent:
            adj_list[parent].append([
                node_id,
                {
                    "ret": node['ret'],
                    "args": node['args'],
                    "kwargs": node['kwargs'],
                    "fn_name": node['fn_name']
                }]
            )

        # Recursively process children nodes
        for child in node['children']:
            add_node(child, node_id)

    # Iterate through all root nodes in the graph
    for node in graph:
        add_node(node)

    return adj_list


if __name__ == "__main__":
    call_graph_json = internal_call()
    print(call_graph_json)
