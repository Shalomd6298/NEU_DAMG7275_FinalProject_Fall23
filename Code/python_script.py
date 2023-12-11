# from gremlin_python.driver import client, serializer
import json

# Define your Azure Cosmos DB Gremlin API endpoint and credentials
# cosmosdb_endpoint = "your_cosmosdb_endpoint"
# cosmosdb_primary_key = "your_cosmosdb_primary_key"
# cosmosdb_database = "your_database_name"
# cosmosdb_graph = "your_graph_name"

# Connect to Azure Cosmos DB
# client = client.Client(
#     cosmosdb_endpoint,
#     "g",
#     username="/dbs/" + cosmosdb_database + "/colls/" + cosmosdb_graph,
#     password=cosmosdb_primary_key,
#     message_serializer=serializer.GraphSONMessageSerializer()
# )

def create_vertex(label, properties):
    query = f"g.addV('{label}')"
    print(query)
    for key, value in properties.items():
        query += f".property('{key}', '{value}')"
    return query

def create_edge(label, from_vertex_id, to_vertex_id):
    print(f"g.V('{from_vertex_id}').addE('{label}').to(g.V('{to_vertex_id}'))")
    return f"g.V('{from_vertex_id}').addE('{label}').to(g.V('{to_vertex_id}'))"

# Sample data for testing
locations = [
    {"locationID": "loc1", "lat": 40.7128, "long": -74.0060, "city": "New York", "country": "USA"},
    # Add more locations as needed
]

handlers = [
    {"handlerID": "handler1", "name": "Handler 1", "contact": "handler1@example.com", "locationID": "loc1"},
    # Add more handlers as needed
]

sensors = [
    {"sensorID": "sensor1", "type": "Temperature", "manufacturer": "ABC Corp", "sensor_status": "Active", "locationID": "loc1"},
    # Add more sensors as needed
]

# Transform and load data into Azure Cosmos DB
for location in locations:
    query = create_vertex("Location", location)
    # client.submit(query).all().result()

for handler in handlers:
    query = create_vertex("Handler", handler)
    # client.submit(query).all().result()

for sensor in sensors:
    query = create_vertex("Sensor", sensor)
    # client.submit(query).all().result()

# Create edges to represent relationships
for handler in handlers:
    query = create_edge("Manages", handler["handlerID"], handler["locationID"])
    # client.submit(query).all().result()

for sensor in sensors:
    query = create_edge("InstalledAt", sensor["sensorID"], sensor["locationID"])
    # client.submit(query).all().result()

# Close the connection
# client.close()
