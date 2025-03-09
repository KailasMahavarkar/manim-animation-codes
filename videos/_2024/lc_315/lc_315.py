class SegmentTree:
    def __init__(self, size):
        self.n = size
        self.tree = [0] * (4 * size)

    def update_tree(self, idx, value, node, start, end):
        if start == end:
            self.tree[node] += value
            return
        mid = start + (end - start) // 2
        if idx <= mid:
            self.update_tree(idx, value, 2 * node + 1, start, mid)
        else:
            self.update_tree(idx, value, 2 * node + 2, mid + 1, end)
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]

    def query_tree(self, qs, qe, node, start, end):
        print("qs > end or qe < start")
        print(
            f"qs > qe or qe < start -> {qs} > {qe} or {qe} < {start} -> {qs > qe or qe < start}")
        if qs > end or qe < start:
            print("\t--> return 0")
            return 0

        print("qs <= start and qe >= end")
        print(f"qs <= start and qe >= end -> {qs} <= {start} and {
              qe} >= {end} -> {qs <= start and qe >= end}")
        if qs <= start and qe >= end:
            print(f"\t--> return tree node, {self.tree[node]}")
            return self.tree[node]

        mid = start + (end - start) // 2
        left = self.query_tree(qs, qe, 2 * node + 1, start, mid)
        right = self.query_tree(qs, qe, 2 * node + 2, mid + 1, end)
        print("\n\n\n")
        return left + right

    def update(self, idx, value):
        self.update_tree(idx, value, 0, 0, self.n - 1)

    def query(self, qs, qe):
        result = self.query_tree(qs, qe, 0, 0, self.n - 1)
        return result


def count_smaller(nums):
    max_val = max(nums)
    seg_tree = SegmentTree(max_val + 1)
    result = [0] * len(nums)
    for i in range(len(nums) - 1, -1, -1):
        result[i] = seg_tree.query(0, nums[i] - 1)
        seg_tree.update(nums[i], 1)
    return [result, seg_tree]


result, seg_tree = count_smaller([5, 6, 3, 1])
