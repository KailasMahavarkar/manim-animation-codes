from typing import List
from viz import viz, callgraph
import json


@viz
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@viz
def factorial(n: int) -> int:
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)


@viz
def printNumber(n: int = 0) -> None:
    if n > 4:
        return

    print(n)
    printNumber(n + 1)


@viz
def solve(nums: List[int], temp: List[int], idx: int, answer: List[List[int]]) -> None:
    if idx == len(nums):
        answer.append(temp[:])
        return

    # Exclude current element and move to the next
    solve(nums, temp, idx + 1, answer)

    # Include current element and move to the next
    temp.append(nums[idx])
    solve(nums, temp, idx + 1, answer)
    temp.pop()  # Remove the element after recursion


@viz
def gcd(a, b):
    if (b == 0):
        return a
    return gcd(b, a % b)


def subset_1_recursive(nums: List[int]) -> List[List[int]]:
    nums.sort()
    answer = []
    solve(nums, [], 0, answer)


n = 4
tree = [0] * (4 * 4)


@viz
def update_tree(idx, value, node, start, end):
    if start == end:
        tree[node] += value
        return
    mid = start + (end - start) // 2
    if idx <= mid:
        update_tree(idx, value, 2 * node + 1, start, mid)
    else:
        update_tree(idx, value, 2 * node + 2, mid + 1, end)
    tree[node] = tree[2 * node + 1] + tree[2 * node + 2]


@viz
def query_tree(idx, qs, qe, start, end):
    if qs > end or qe < start:
        return 0

    if qs <= start and qe >= end:
        return tree[idx]

    mid = start + (end - start) // 2
    left = query_tree(2 * idx + 1, qs, qe, start, mid)
    right = query_tree(2 * idx + 2, qs, qe, mid + 1, end)
    return left + right


def update(idx, value):
    update_tree(idx, value, 0, 0, n - 1)


def query(qs, qe):
    result = query_tree(0, qs, qe, 0, n - 1)
    return result


def count_smaller(nums):
    max_val = max(nums)
    seg_tree = tree

    result = [0] * len(nums)
    for i in range(len(nums) - 1, -1, -1):
        result[i] = query(0, nums[i] - 1)
        update(nums[i], 1)
    return [result, seg_tree]


if __name__ == "__main__":
    callgraph.reset()
    result, seg_tree = count_smaller([5, 6, 3, 1])
    call_graph_json = callgraph.get_graph_dictionary()
    print("\n ------ visualize callgraph ------ \n")
    callgraph.pretty_table([])
