from pymongo import MongoClient

uri = "mongodb+srv://banerjeeapurv84_db_user:yZBrszN0WkMhUqQG@cluster0.xvwpv6a.mongodb.net/"
client = MongoClient(uri)
try:
    client.admin.command("ping")
    print("Connected successfully")
    client.close()

except Exception as e:
    raise Exception(
        "The following error occurred: ", e)