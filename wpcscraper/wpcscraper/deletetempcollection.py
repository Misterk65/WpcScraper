import pymongo
import csv

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
collection = db["tbl_data"]

"""
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
"""


prod_list = []

for ven in db["tbl_data"].distinct("Vendor"):
    x = str(db["tbl_data"].find({"Vendor":ven}).count())
    #print(ven + " : " + str(db["tbl_data"].find({"Vendor":ven}).count()))
    prod_list.append({"Vendor": ven, "Count": x})

# sorted(prod_list)

# print(prod_list)

csv_file = "Vendorlist.csv"
csv_columns = ['Vendor', 'Count']
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in prod_list:
            writer.writerow(data)
except IOError:
    print("I/O error")


try:
    conn.close()
    print("Database disconnected successfully !!!")
except:
    print("Database close operation failed !!!")