from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import dotenv_values
import argparse
from bson.objectid import ObjectId

# завантаження credentials з .env
config = dotenv_values(".env")

# підключення до MongoDB
uri = f"mongodb+srv://{config["USER_MDB"]}:{config["PASSWORD_MDB"]}@msds2.ulj7i4g.mongodb.net/?retryWrites=true&w=majority&appName=Msds2"
client = MongoClient(uri, server_api=ServerApi('1'))

# вибір бази
db = client.mds02

# налаштування аргументів командного рядка
parser = argparse.ArgumentParser(description="Add a new cat")
parser.add_argument("--action", help="[create, read_all, read_one, update_age, add_features, delete_one, delete_all]")
parser.add_argument("--id", help="ID of the cat")
parser.add_argument("--name", help="Name of the cat")
parser.add_argument("--age", type=int,  help="Age of the cat")
parser.add_argument("--features", help="Features of the cat", nargs="+")

# парсинг аргументів
args = vars(parser.parse_args())
action = args["action"]
pk = args["id"]
name = args["name"]
age = args["age"]
features = args["features"]

# функція додавання
def create(name, age, features):
    return db.cats.insert_one({
        "name": name,
        "age": age,
        "features": features
    })

# функція виведення всих котів
def read_all():
    cats = db.cats.find()
    return cats

# функція виведення одного кота
def read_one(name):
    cat = db.cats.find_one({"name": name})
    return cat

# функція оновлення віку
def update_age(name, age):
    return db.cats.update_one({"name": name}, {"$set": {"age": age}})

# функція додавання features
def add_features(name, features):
    return db.cats.update_one({"name": name}, {"$push": {"features": features}})
   
# функція видалення 1 кота
def delete_one(name):
    return db.cats.delete_one({"name": name})

# функція видалення всіх котів
def delete_all():
    return db.cats.delete_many({})


if __name__ == "__main__":
    match action:
        case "create":
            r = create(name, age, features)
            print(r.inserted_id)
        case "read_all":
            [print(cat) for cat in read_all()]
        case "read_one":
            print(read_one(name))
        case "update_age":
            r = update_age(name, age)
            print(r.modified_count)
        case "add_features":
            r = add_features(name, features[0])
            print(r.modified_count)
        case "delete_one":
            r = delete_one(name)
            print(r.deleted_count)
        case "delete_all":
            r = delete_all()
            print(r.deleted_count)
        case _:
            print("Wrong action")
