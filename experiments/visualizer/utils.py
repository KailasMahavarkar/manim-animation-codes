from functools import wraps
import copy
import json
from time import time
import inspect
from typing import Dict, List, Any


MAX_FRAMES = 1000
MAX_TIME = 10


class TooManyFramesError(Exception):
    pass


class TooMuchTimeError(Exception):
    pass


class RecursionTracker:
    def __init__(self):
        self.root = None
        self.current_node = None
        self.depth = 0
        self.calls = []
        self.frames = []
        self.start_time = time()
        self.max_frames = MAX_FRAMES
        self.max_time = MAX_TIME

    def start_call(self, func_name, args, kwargs):
        # Ensure we don't exceed the max frames/time
        if len(self.frames) > self.max_frames:
            raise TooManyFramesError(
                f"Encountered more than {self.max_frames} frames."
            )
        if (time() - self.start_time) > self.max_time:
            raise TooMuchTimeError(f"Took more than {self.max_time} seconds.")

        # Create a new call entry
        call_entry = {
            'name': func_name,
            'args': [str(arg) for arg in args],
            'kwargs': {k: str(v) for k, v in kwargs.items()},
            'result': None,
            'children': [],
            'ret': None,
            'ret_step': None
        }

        # If this is the first call, set as root
        if self.root is None:
            self.root = call_entry
            self.current_node = call_entry
        else:
            # Add to children of current node
            self.current_node['children'].append(call_entry)
            self.current_node = call_entry

        self.depth += 1
        self.calls.append(call_entry)
        self.frames.append(id(call_entry))

        return call_entry

    def end_call(self, result):
        # Set result for the current node
        self.current_node['result'] = str(result)

        # Track return step
        self.current_node['ret'] = result
        self.current_node['ret_step'] = len(self.calls)

        # Decrement depth
        self.depth -= 1

        # Move back up the tree
        if self.depth > 0:
            parent = self.root
            for _ in range(self.depth - 1):
                parent = parent['children'][-1]
            self.current_node = parent

    def get_call_graph(self):
        return self.root

    def reset(self):
        self.root = None
        self.current_node = None
        self.depth = 0
        self.calls = []
        self.frames = []
        self.start_time = time()


MAX_FRAMES = 1000
MAX_TIME = 10


class TooManyFramesError(Exception):
    pass


class TooMuchTimeError(Exception):
    pass


class RecursionTracker:
    def __init__(self):
        self.root = None
        self.current_node = None
        self.depth = 0
        self.calls = []
        self.frames = []
        self.start_time = time()
        self.max_frames = MAX_FRAMES
        self.max_time = MAX_TIME

    def start_call(self, func_name, args, kwargs):
        # Ensure we don't exceed the max frames/time
        if len(self.frames) > self.max_frames:
            raise TooManyFramesError(
                f"Encountered more than {self.max_frames} frames."
            )
        if (time() - self.start_time) > self.max_time:
            raise TooMuchTimeError(f"Took more than {self.max_time} seconds.")

        # Create a new call entry
        call_entry = {
            'name': func_name,
            'args': [str(arg) for arg in args],
            'kwargs': {k: str(v) for k, v in kwargs.items()},
            'result': None,
            'children': [],
            'ret': None,
            'ret_step': None
        }

        # If this is the first call, set as root
        if self.root is None:
            self.root = call_entry
            self.current_node = call_entry
        else:
            # Add to children of current node
            self.current_node['children'].append(call_entry)
            self.current_node = call_entry

        self.depth += 1
        self.calls.append(call_entry)
        self.frames.append(id(call_entry))

        return call_entry

    def end_call(self, result):
        # Set result for the current node
        self.current_node['result'] = str(result)

        # Track return step
        self.current_node['ret'] = result
        self.current_node['ret_step'] = len(self.calls)

        # Decrement depth
        self.depth -= 1

        # Move back up the tree
        if self.depth > 0:
            parent = self.root
            for _ in range(self.depth - 1):
                parent = parent['children'][-1]
            self.current_node = parent

    def get_call_graph(self):
        return self.root

    def reset(self):
        self.root = None
        self.current_node = None
        self.depth = 0
        self.calls = []
        self.frames = []
        self.start_time = time()


def recursion_tree(func):
    """
    A decorator to create a detailed recursion tree visualization in JSON format.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Create a tracker instance
        tracker = kwargs.get('tracker') or RecursionTracker()

        # Capture the current call
        tracker.start_call(func.__name__, args, kwargs)

        if kwargs == {'tracker': None}:
            kwargs.pop('tracker')

        # Perform the actual function call
        # pass the tracker instance to the function but its also passed via decorator so we need to remove it
        result = func(*args, **kwargs)

        # End the current call and set its result
        tracker.end_call(result)

        # If this is the root call, return the full call graph in JSON format
        if tracker.depth == 0:
            return json.dumps(tracker.get_call_graph(), indent=4)

        return result

    return wrapper


def decorate_funcs(func_source: str):
    outlines = []
    for line in func_source.split("\n"):
        if line.startswith("def "):
            outlines.append("@recursion_tree")
        outlines.append(line)
    return "\n".join(outlines)


def visualize(function_definition, function_call):
    """Either returns generated JSON for the call graph."""
    RecursionTracker().reset()
    function_definition = decorate_funcs(function_definition)
    exec(function_definition, globals())
    result_json = eval(function_call)
    return result_json


def print_recursion_tree(call_graph, current_depth=0, parent=None):
    """
    Prints the recursion tree based on the call graph structure.

    :param call_graph: The call graph containing function call details.
    :param current_depth: Current depth in the recursion tree (used for formatting).
    :param parent: The parent function node from which the current node is called.
    """
    # If the call graph is empty or there's no parent, return
    if not call_graph:
        return

    # Ensure that the call graph is a dictionary
    if isinstance(call_graph, str):
        call_graph = json.loads(call_graph)

    # Format the function call
    func_name = call_graph['name']
    args = ", ".join(call_graph['args'])

    # Print the current function call at this level
    prefix = "    " * current_depth + "└── "
    print(f"{prefix}{func_name}({args})")

    # Recursively print child calls if they exist
    for child in call_graph['children']:
        print_recursion_tree(child, current_depth + 1, func_name)


@recursion_tree
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


if __name__ == "__main__":
    cg = fibonacci(3)
    print_recursion_tree(cg)
