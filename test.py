import pycouchdb
server = pycouchdb.Server("http://admin:password@localhost:5984/")
db = server.database("masterdb")

print(db.get("Exclusion Mage"))