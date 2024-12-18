class Solution:
    def insert(self, intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:
        result = []
        i, n = 0, len(intervals)

        # Add all intervals that come before newInterval
        # i = 0
        # ci = [1, 2]
        # ni = [3, 8]
        # ci[1] < ni[0] => 2 < 3 -> everything is fine
        # result = [[1, 2]]

        while i < n and intervals[i][1] < newInterval[0]:
            result.append(intervals[i])
            i += 1

        # i = 1
        # [3, 5] <= [4, 8]
        # ni = min(3, 4) = 3
        # ni = max(5, 8) = 8

        # i = 2
        # [6, 7] <= [3, 8]
        # ni = min(6, 3) = 3
        # ni = max(7, 8) = 8

        # i = 3
        # [8, 10] <= [3, 8]
        # ni = min(8, 3) = 3
        # ni = max(10, 8) = 10

        while i < n and intervals[i][0] <= newInterval[1]:
            newInterval[0] = min(newInterval[0], intervals[i][0])
            newInterval[1] = max(newInterval[1], intervals[i][1])
            i += 1
        result.append(newInterval)

        while i < n:
            result.append(intervals[i])
            i += 1
        return result


intervals = [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]]
newInterval = [4, 8]
print(Solution().insert(intervals, newInterval))
