import pymongo

try:
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb+srv://wwwsanjayijk07:xaZYk6xBacA4LabQ@cluster0.ek565j8.mongodb.net/")

    # Access a database
    db = client["test"]

    # Access a collection
    collection = db["to_do"]
    print("Database connection successful!")

except pymongo.errors.ConnectionFailure as e:
    # If a connection error occurs, print the error message
    print("Failed to connect to MongoDB:", e)
