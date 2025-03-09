from heap import MaxHeap


class Solution:
    def minRefuelStops(self, target: int, startFuel: int, stations: list[list[int]]) -> int:
        pq = MaxHeap()  # Initialize the max heap
        currentFuel = startFuel
        steps = 0
        i = 0
        n = len(stations)

        print(f"Initial Fuel: {currentFuel}")  # Initial fuel value
        print(f"Target: {target}")  # Target distance

        # Push all reachable stations' fuel into the priority queue
        while i < n and stations[i][0] <= currentFuel:
            
            pq.push(stations[i][1])
            print(
                f"Added fuel from station at {stations[i][0]} km with { stations[i][1]} liters of fuel."
            )
            i += 1

        # Use the fuel from the priority queue until we can reach the target
        while currentFuel < target:
            print("\n\n")
            if pq.size == 0:
                print("Cannot reach the target, no more stations to refuel.")
                return -1

            print("currentFuel before refueling: ", currentFuel)
            print("pq ", pq.items)
            currentFuel += pq.pop()  # Refuel from the station with the most fuel
            print("currentFuel after refueling: ", currentFuel)
            steps += 1

            print(f"Refueled! Current Fuel: {
                  currentFuel} liters. Stops so far: {steps}")

            # Push all new reachable stations' fuel into the priority queue
            while i < n and stations[i][0] <= currentFuel:
                pq.push(stations[i][1])
                print(f"Added fuel from station at {stations[i][0]} km with {
                      stations[i][1]} liters of fuel.")
                i += 1

        print(f"Reached target with {currentFuel} liters of fuel.")
        return steps


target = 1000
startFuel = 70
stations = [[50, 200], [100, 400], [400, 200], [
    600, 300], [800, 200], [900, 300], [950, 200]]
x = Solution().minRefuelStops(target, startFuel, stations)
print(x)

