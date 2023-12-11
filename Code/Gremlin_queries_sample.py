

g.addV('location').property('locationID', 1).property('lat', 123.45).property('long', 67.89).property('city', 'City1').property('country', 'Country1')

g.addV('handler').property('handlerID', 101).property('name', 'Handler1').property('contact', 'Contact1')
g.V().has('locationID', 1).addE('hasHandler').to(g.V().has('handlerID', 101))




g.addV('sensor').property('sensorID', 1001).property('type', 'Type1').property('manufacturer', 'Manufacturer1').property('sensor_status', 'Active')
g.V().has('locationID', 1).addE('hasSensor').to(g.V().has('sensorID', 1001))


g.V().has('handlerID', 101).addE('handles').to(g.V().has('sensorID', 1001))
