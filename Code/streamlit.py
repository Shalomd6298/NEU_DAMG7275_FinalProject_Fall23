
import streamlit as st
from azure.cosmos import CosmosClient

# Azure Cosmos DB configuration
endpoint = '<endpoint>'
key = '<key>'
database_id = '<db_id>'
container_id = '<container_id>'

# Initialize Cosmos DB client
client = CosmosClient(endpoint, key)
database = client.get_database_client(database_id)
container = database.get_container_client(container_id)

# Streamlit app
def main():
    st.title("Cosmos DB Data Viewer")

    # Query Cosmos DB and display data
    query = 'SELECT * FROM c'
    items = list(container.query_items(query, enable_cross_partition_query=True))

    st.write("## Cosmos DB Data")

    if not items:
        st.warning("No data found.")
    else:
        for item in items:
            st.write(item)

if __name__ == "__main__":
    main()


