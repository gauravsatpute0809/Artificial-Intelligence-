import heapq

# Graph and heuristic storage
graph_data = {}
heuristic_values = {}

num_nodes = int(input("Enter number of nodes: "))

node_list = []
for i in range(num_nodes):
    node_name = input(f"Enter node {i+1}: ")
    node_list.append(node_name)
    
    graph_data[node_name] = []

num_edges = int(input("Enter number of edges: "))
print("Enter edges in format: source destination cost")

for i in range(num_edges):
    source, destination, edge_cost = input(f"Edge {i+1}: ").split()
    graph_data[source].append((destination, int(edge_cost)))

print("\nEnter heuristic values:")
for node in node_list:
    heuristic_values[node] = int(input(f"Heuristic of {node}: "))

start_node = input("\nEnter start node: ")
goal_node = input("Enter goal node: ")

def a_star_search(start_node, goal_node):
    priority_queue = []
    heapq.heappush(priority_queue, (0, start_node))

    cost_from_start = {node: float('inf') for node in graph_data}
    cost_from_start[start_node] = 0

    parent_node = {}

    while priority_queue:
        _, current_node = heapq.heappop(priority_queue)

        if current_node == goal_node:
            path = []
            while current_node in parent_node:
                path.append(current_node)
                current_node = parent_node[current_node]

            path.append(start_node)
            return path[::-1], cost_from_start[goal_node]

        for neighbor, travel_cost in graph_data[current_node]:
            new_cost = cost_from_start[current_node] + travel_cost

            if new_cost < cost_from_start[neighbor]:
                cost_from_start[neighbor] = new_cost
                total_cost = new_cost + heuristic_values[neighbor]

                heapq.heappush(priority_queue, (total_cost, neighbor))
                parent_node[neighbor] = current_node

    return None, float('inf')


shortest_path, total_cost = a_star_search(start_node, goal_node)

print("\nShortest Path using A*:", shortest_path)
print("Total Cost:", total_cost)