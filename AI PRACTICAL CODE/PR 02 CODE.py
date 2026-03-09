# Water Jug Problem using DFS

def solve_water_jug_dfs(capacity_jug1, capacity_jug2, target_amount, goal_state):
    all_solutions = []

    def dfs_search(jug1_level, jug2_level, current_path, visited_states):
        if (jug1_level, jug2_level) in visited_states:
            return

        visited_states.add((jug1_level, jug2_level))
        current_path.append((jug1_level, jug2_level))

        # Check if goal reached
        if (jug1_level, jug2_level) == goal_state:
            all_solutions.append(current_path.copy())
            current_path.pop()
            return

        # Possible operations
        possible_moves = [
            (capacity_jug1, jug2_level),  # Fill jug1
            (jug1_level, capacity_jug2),  # Fill jug2
            (0, jug2_level),              # Empty jug1
            (jug1_level, 0),              # Empty jug2
            (max(0, jug1_level - (capacity_jug2 - jug2_level)),
             min(capacity_jug2, jug1_level + jug2_level)),  # Pour jug1 → jug2
            (min(capacity_jug1, jug1_level + jug2_level),
             max(0, jug2_level - (capacity_jug1 - jug1_level)))  # Pour jug2 → jug1
        ]

        for next_state in possible_moves:
            dfs_search(next_state[0], next_state[1], current_path, visited_states.copy())

        current_path.pop()

    dfs_search(0, 0, [], set())
    return all_solutions


# -------- USER INPUT --------

jug1_capacity = int(input("Enter capacity of Jug 1 (m): "))
jug2_capacity = int(input("Enter capacity of Jug 2 (n): "))
desired_amount = int(input("Enter desired amount (d): "))

goal_text = input("Enter goal state in format <x,y>: ")
goal_state = tuple(map(int, goal_text.strip("<>").split(",")))

# -------- VALIDATION --------

if goal_state[0] < 0 or goal_state[1] < 0 or goal_state[0] > jug1_capacity or goal_state[1] > jug2_capacity:
    print("\nInvalid goal state")

elif goal_state[0] != desired_amount and goal_state[1] != desired_amount:
    print("\nInvalid goal state (desired amount not present)")

else:
    solutions_found = solve_water_jug_dfs(jug1_capacity, jug2_capacity, desired_amount, goal_state)

    if not solutions_found:
        print("\nNo solution found")

    else:
        print("\nPOSSIBLE SOLUTIONS:\n")

        for index, solution in enumerate(solutions_found, 1):
            print(f"Solution {index} (Steps = {len(solution) - 1}):")
            print(solution)
            print()

        # Best solution with minimum steps
        shortest_solution = min(solutions_found, key=len)

        print("BEST SOLUTION (Minimum Steps):")
        print(shortest_solution)
        print(f"Total steps: {len(shortest_solution) - 1}")