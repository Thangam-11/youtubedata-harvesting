from app.mongodb_handler import MongoDBHandler
from app.youtube_extract import YouTubeExtract
if __name__ == "__main__":
    db = MongoDBHandler()

    # Insert
    doc_id = db.insert_document("test_collection", {"name": "Codebasics", "topic": "YouTube API"})
    print("Inserted:", doc_id)

    # Find
    docs = db.find_documents("test_collection")
    for doc in docs:
        print(doc)
