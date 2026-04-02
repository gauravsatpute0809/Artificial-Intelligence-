import matplotlib.pyplot as plt
import networkx as nx # type: ignore

class SemanticNetwork:
    def __init__(self):
        self.entities = set()
        self.relationships = []

    def add_relation(self, subject_entity, relation_type, object_entity):
        self.entities.add(subject_entity)
        self.entities.add(object_entity)
        self.relationships.append((subject_entity, relation_type, object_entity))

    def display_network(self):
        print("\nSemantic Network (Relationships):")
        for subject_entity, relation_type, object_entity in self.relationships:
            print(f"{subject_entity} --{relation_type}--> {object_entity}")

    def display_predicate_logic(self):
        print("\nPredicate Logic Representation:")
        for subject_entity, relation_type, object_entity in self.relationships:
            print(f"{relation_type}({subject_entity}, {object_entity})")

    def draw_graph(self):
        graph = nx.DiGraph()  # Directed graph
        
        for subject_entity, relation_type, object_entity in self.relationships:
            graph.add_edge(subject_entity, object_entity, label=relation_type)

        position = nx.spring_layout(graph, seed=42)

        plt.figure(figsize=(8,6))
        nx.draw(
            graph, position,
            with_labels=True,
            node_color='lightblue',
            node_size=2000,
            font_size=12,
            arrowsize=20
        )

        # Draw edge labels
        edge_labels = nx.get_edge_attributes(graph, 'label')
        nx.draw_networkx_edge_labels(
            graph, position,
            edge_labels=edge_labels,
            font_color='red',
            font_size=10
        )

        plt.title("Semantic Network Graph")
        plt.show()


# Create network object
semantic_network = SemanticNetwork()

# Input number of relationships
total_relations = int(input("Enter number of relations: "))

# Take user input
for relation_index in range(total_relations):
    print(f"\nEnter details for relation {relation_index + 1}:")
    subject_entity = input("  Subject: ")
    relation_type = input("  Relation (predicate): ")
    object_entity = input("  Object: ")
    
    semantic_network.add_relation(subject_entity, relation_type, object_entity)

# Display outputs
semantic_network.display_network()
semantic_network.display_predicate_logic()

# Draw graph
semantic_network.draw_graph()