import json
from config.database import entity_collection
from datetime import datetime

if __name__ == "__main__":
    file = open("data.json", "r")

    data = json.load(file)
    result = []

    for entity in data:
        resultEntity = entity
        print(resultEntity)

        # del resultEntity["id"]
        resultEntity["created_at"] = datetime.strptime(resultEntity["created_at"],'%Y-%m-%dT%H:%M:%S.%f%z')
        resultEntity["updated_at"] = datetime.strptime(resultEntity["updated_at"],'%Y-%m-%dT%H:%M:%S.%f%z')

        entity_collection.insert_one(resultEntity)
        print(resultEntity)


    print("Done!")