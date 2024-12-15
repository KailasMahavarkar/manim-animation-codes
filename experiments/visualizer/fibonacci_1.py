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


if __name__ == "__main__":
    callgraph.reset()
    gcd(180, 24)
    call_graph_json = callgraph.get_graph_dictionary()
    print("\n ------ visualize callgraph ------ \n")
    callgraph.pretty_table()















