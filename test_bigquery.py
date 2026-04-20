from google.cloud import bigquery


client = bigquery.client(projects="juan-gomez-fiu")

query = "SELECT * FROM `juan-gomez-fiu.SWEpers.posts"
results = client.query(query).result()

for row in results:
    print(dict(row))