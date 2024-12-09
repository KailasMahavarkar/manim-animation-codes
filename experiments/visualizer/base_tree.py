from functools import wraps
import sys
sys.stdout.reconfigure(encoding='utf-8')

current_depth = 0
recursion_tree_data = {}


class Node:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def remove_child(self, child):
        self.children.remove(child)

    def to_dict(self):
        return {
            "name": self.name,
            "args": self.args,
            "children": [child.to_dict() for child in self.children]
        }




# # Example usage (assuming call_graph is already built with required details)
# call_graph = {
#     'main': {
#         'args': ['arg1', 'arg2'],
#         'parent': None,
#         'children': {
#             'function1': {
#                 'args': ['arg1'],
#                 'parent': 'main',
#                 'children': {
#                     'function2': {
#                         'args': [],
#                         'parent': 'function1',
#                         'children': {}
#                     }
#                 }
#             }
#         }
#     }
# }

# # Call the function to print the recursion tree
# print_recursion_tree(call_graph)
