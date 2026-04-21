from google.cloud import bigquery


client = bigquery.Client(project="juan-gomez-fiu")

query = "SELECT * FROM `juan-gomez-fiu.SWEpers.Posts`"
results = client.query(query).result()

for row in results:
    print(dict(row))