import heapq
import heapq


class Solution:
    def kSmallestPairs(self, nums1, nums2, k):
        result = []
        print(f"Initial result: {result}")

        if not nums1 or not nums2:
            print("One of the input arrays is empty, returning empty result.")
            return result

        pq = []
        print(f"Initial priority queue (pq): {pq}")

        # Push first element from nums1 and the first element from nums2 into the priority queue
        for i in range(min(len(nums1), k)):
            heapq.heappush(pq, (nums1[i] + nums2[0], i, 0))
            print(f"Heap after pushing ({nums1[i] + nums2[0]}, {i}, 0): {pq}")

        print("\n")

        while k > 0 and pq:
            sum_value, i, j = heapq.heappop(pq)
            print(f"Popped from heap: sum_value={sum_value}, i={i}, j={j}")
            result.append([nums1[i], nums2[j]])
            print(f"Updated result: {result}")

            if j + 1 < len(nums2):
                heapq.heappush(pq, (nums1[i] + nums2[j + 1], i, j + 1))
                print(f"Heap after pushing ({
                      nums1[i] + nums2[j + 1]}, {i}, {j + 1}): {pq}")

            k -= 1
            print(f"Remaining k: {k}")
            print("\n")

        return result


nums1 = [1, 2, 3]
nums2 = [4, 5]
k = 5
x = Solution().kSmallestPairs(nums1, nums2, k)
print(x)
