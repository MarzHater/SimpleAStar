import osmnx as osm
import networkx as nx
import csv
from haversine import haversine
import heapq

G = osm.graph_from_place("Barcelona, Spain", network_type="walk")

start_point = osm.geocode("Plaça de Catalunya, Barcelona") #Start point
end_point = osm.geocode("Sagrada Familia, Barcelona")      #End point
start_node = osm.distance.nearest_nodes(G, X=start_point[1], Y=start_point[0])
end_node = osm.distance.nearest_nodes(G, X=end_point[1], Y=end_point[0])

open_set = [(0, start_node)]
prev = {}
score = {start_node: 0}

visited = []
step_count = 0

while open_set:
    _, current = heapq.heappop(open_set)
    step_count += 1

    if current == end_node:
        break

    for neighbor in G.neighbors(current):
        total_cost_g = score[current] + G[current][neighbor][0]['length']
        if neighbor not in score or total_cost_g < score[neighbor]:
            prev[neighbor] = current
            score[neighbor] = total_cost_g
            x1, y1 = G.nodes[neighbor]['x'], G.nodes[neighbor]['y']
            x2, y2 = G.nodes[end_node]['x'], G.nodes[end_node]['y']
            f_score = total_cost_g + haversine((y1, x1), (y2, x2)) * 1000
            heapq.heappush(open_set, (f_score, neighbor))
            visited.append((step_count, current, neighbor))

final_path = []
node = end_node
while node in prev:
    final_path.append((node, prev[node]))
    node = prev[node]
final_path.reverse()

with open("osm_exploration.csv", "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["step", "x1", "y1", "x2", "y2", "type"])
    for step, u, v in visited:
        x1, y1 = G.nodes[u]['x'], G.nodes[u]['y']
        x2, y2 = G.nodes[v]['x'], G.nodes[v]['y']
        writer.writerow([step, x1, y1, x2, y2, "explored"])

    for step, (u, v) in enumerate(final_path, start=step_count + 1):
        x1, y1 = G.nodes[u]['x'], G.nodes[u]['y']
        x2, y2 = G.nodes[v]['x'], G.nodes[v]['y']
        writer.writerow([step, x1, y1, x2, y2, "path"])

print("Exported osm_exploration.csv")