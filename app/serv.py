from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
from rest_framework.fields import empty

Username = "5e76bd4d-d763-4fce-aff0-887cdde87a86-bluemix"
api = "3fFtXuIMXq4xEPtfCws-bggNAu9KCLxsmLALbWayfdMz"

client = Cloudant.iam(Username, api, connect=True)
client.connect()
session=client.session()

database=client['hack1']
db = Result(database.all_docs,include_docs=True)
print(db[0][0]["doc"]["log"])
print()
for doc in database:
    doc["log"]=0
    doc.save()
    print(doc["log"])

jsonDocument = {
    "name": "Rohit Ram",
    "email": "tridot64@gmail.com",
    "password": "rohitibm",
    "district": "chennai",
    "state": "Tamil Nadu"
}
if jsonDocument["email"]!=db[0][0]["doc"]["email"]:
    newDocument = database.create_document(jsonDocument)
else:
    print("no")

client.disconnect()