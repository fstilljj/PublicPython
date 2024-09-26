import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_nodes_from(['Router1', 'Router2', 'Switch1', 'Switch2', 'PC1', 'PC2'])
G.add_edges_from([('Router1', 'Switch1'), ('Router1', 'Switch2')])

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=8)
plt.show()
