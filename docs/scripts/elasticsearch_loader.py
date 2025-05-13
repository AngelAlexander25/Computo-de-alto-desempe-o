import json
import requests

ELASTIC_URL = "http://localhost:9200"
INDEX_NAME = "messi_barcelona"

with open("docs/data/messi_barcelona_clean.json", "r") as file:
    lines = file.readlines()

bulk_data = ""
for line in lines:
    bulk_data += json.dumps({"index": {"_index": INDEX_NAME}}) + "\n" + line

res = requests.post(f"{ELASTIC_URL}/_bulk", headers={"Content-Type": "application/json"}, data=bulk_data)
print(res.json())
