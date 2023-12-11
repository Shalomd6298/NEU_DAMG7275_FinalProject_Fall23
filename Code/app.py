import streamlit as st
from azure.cosmos import CosmosClient
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from gremlin_python.driver import client, serializer
import networkx as nx



# Function to fetch data from Azure SQL DB
def fetch_data_from_sql():
    server = '<>'
    database = '<>'
    username = '<>'
    password = '<>'

    driver = '{ODBC Driver 18 for SQL Server};'
    conn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' +
                          server + ';PORT=1433;DATABASE=' + database +
                          ';UID=' + username + ';PWD=' + password)
    cursor = conn.cursor()

    sql_query = 'SELECT * FROM dbo.soil_reading'
    cursor.execute(sql_query)

    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    data = [tuple(row) for row in rows]

    df = pd.DataFrame(data, columns=columns)

    cursor.close()
    conn.close()

    return df

# Function to fetch data from Cosmos DB
def fetch_data_from_cosmos():
    endpoint = '<>'
    key = '<>'

    client = CosmosClient(endpoint, key)
    database_name = '<>'
    container_name = '<>'

    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)

    query = 'SELECT * FROM c'
    result = container.query_items(query, enable_cross_partition_query=True)

    return result

# Streamlit app
def main():
    st.title("Data Fetching App")

    # Page for Azure SQL DB
    st.header("Azure SQL DB Data")
    sql_data = fetch_data_from_sql()
    st.dataframe(sql_data)

    # Page for Cosmos DB
    st.header("Cosmos DB Data")
    cosmos_data = fetch_data_from_cosmos()
    for item in cosmos_data:
        st.write(item)

def visualize_cosmos_db_graph():
    st.header("Cosmos DB Graph Visualization")

    # Set up the Cosmos DB connection configuration
    cosmos_db_password = "<>"

    # Create a Gremlin client
    gremlin_client = client.Client(
        f"<>",
        "g",
        username=f"<>",
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

# Streamlit app
def main():
    st.title("Data Fetching and Parsing App")

    # Sidebar for navigation
    page = st.sidebar.radio("Select a Page", ["Azure SQL DB", "Cosmos DB", "Cosmos DB Graph Visualization"])

    if page == "Azure SQL DB":
        st.header("Azure SQL DB Data")
        sql_data = fetch_data_from_sql()
        st.dataframe(sql_data)

    elif page == "Cosmos DB":
        st.header("Cosmos DB Data")
        cosmos_data = fetch_data_from_cosmos()
        for item in cosmos_data:
            st.write(item)

    elif page == "Cosmos DB Graph Visualization":
        visualize_cosmos_db_graph()


if __name__ == "__main__":
    main()
