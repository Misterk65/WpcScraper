import pymongo

# Connect to Database
try:
    conn = pymongo.MongoClient(

        'mongodb+srv://DevUser:$B116168kp$@cluster0-4am5x.mongodb.net/test?retryWrites=true'
    )
    db = conn["scraper"]
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

# Read collections in database
collectionexists = db.list_collection_names()

# Check wether collection is in database
if "tbl_data_temp" in collectionexists:
    # Delete the collection
    try:
        collection = db["tbl_data_temp"]
        db.drop_collection(collection)
        print("Collection successfully deleted !")
        print("Collections in Database: " + str(db.list_collection_names()))
    except:
        print("Error in deleting collection !")

else:
    print("Collection not found")
    print("Collections in Database: " + str(db.list_collection_names()))

try:
    conn.close()
    print("Database disconnected successfully !!!")
except:
    print("Database close operation failed !!!")