class Solution {
   public:
    bool search(vector<int>& arr, int target) {
        int s = 0;
        int e = arr.size() - 1;

        while (s <= e) {
            int mid = s + (e - s) / 2;

            if (arr[mid] == target) {
                return true;
            }

            // case of ambiguity
            if (arr[mid] == arr[s] && arr[e] == arr[mid]) {
                s++;
                e--;
                continue;
            }

            if (arr[s] <= arr[mid]) {
                if (target >= arr[s] && target <= arr[mid]) {
                    e = mid - 1;
                } else {
                    s = mid + 1;
                }
            } else {
                if (target >= arr[mid] && target <= arr[e]) {
                    s = mid + 1;
                } else {
                    e = mid - 1;
                }
            }
        }

        return false;
    }
};
