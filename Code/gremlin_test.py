import streamlit as st
from gremlin_python.driver import client, serializer
import networkx as nx
import matplotlib.pyplot as plt

def main():
    st.title("Graph Visualization with Streamlit")

    # Set up the Cosmos DB connection configuration
    cosmos_db_password = "FKJtn6TJL6firROtZoYX3AsaVJA9XzbFBAuUlsFksKZKkNeTTLFzhlhaZjTojLIPBAbuAToxkMCOACDb72oXtA=="

    # Create a Gremlin client
    gremlin_client = client.Client(
        f"wss://graphdatamodel-acc-adbms.gremlin.cosmos.azure.com:443/",
        "g",
        username=f"/dbs/adbms-graph2/colls/graph1",
        password=cosmos_db_password,
        message_serializer=serializer.GraphSONSerializersV2d0(),
    )

    # Define a simple Gremlin query
    gremlin_query = "g.V().limit(5)"

    # Execute the query
    result_set = gremlin_client.submit(gremlin_query)

    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes and edges to the graph
    for result in result_set:
        for vertex in result:
            node_id = vertex['label']  # Use the label as the node ID
            node_label = vertex['label']
            G.add_node(node_id, label=node_label)
            for prop_name, prop_values in vertex['properties'].items():
                for prop_value in prop_values:
                    if prop_name != 'graph':  # Skip the 'graph' property
                        target_node_id = prop_value['value']
                        G.add_edge(node_id, target_node_id, label=prop_name)

    # Calculate node positions using spring layout
    pos = nx.spring_layout(G)

    # Draw the graph
    fig, ax = plt.subplots(figsize=(10, 8))
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=2000, node_color='skyblue', font_color='black', font_size=8, edge_color='gray', arrowsize=20)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=8)

    # Display the graph in Streamlit
    st.pyplot(fig)

    # Close the Gremlin client
    gremlin_client.close()

if __name__ == "__main__":
    main()
