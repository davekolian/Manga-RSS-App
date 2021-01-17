import pymongo

client = pymongo.MongoClient(
    "mongodb+srv://dbMain:2G9eS0uUgSaFhzX7@maincluster.idq3f.mongodb.net/manga_app?retryWrites=true&w=majority")

db = client.get_database('manga_app')

table = db.get_collection("manga_app_records")
# collection -> table
# document -> rows

table.delete_many({})

print(table.count_documents({}))

# insert a document i.e row insert_one() or insert_many()

new_row = {
    'record_id': 3,
    'manga_name': 'dummy name',
    'manga_chapters': ['c1', 'c2'],
    'img_link_bg': 'dummy_link',
    'chapter_links': ['link1', 'link2']
}

# table.insert_one(new_row)


# find a document, find() -> returns an iterator, find_one({'keyword': search})
# print(list(table.find({})))

# update, update_one(filter_dict, {'$set': new_dict}) or update_many

# delete, delete_one(filter_dict) or delete_many(filter_dict)
# print(list(table.find({'manga_name': 'dummy name'})))
# table.delete_many({'manga_name': 'dummy name'})

