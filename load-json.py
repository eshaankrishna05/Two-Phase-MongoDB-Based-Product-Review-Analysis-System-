import argparse
import json
import pymongo

def load_data_to_mongo(json_file, port, verbose):
    """Load reviews from a JSON file into a MongoDB collection."""
    try:
        # Connect to MongoDB
        #client = pymongo.MongoClient(f"mongodb://localhost:{port}/", serverSelectionTimeoutMS=5000)
        client = pymongo.MongoClient(f"mongodb://localhost:{port}/")

        db = client["291db"]
        collection = db["reviews"]

        # Drop the existing collection if it exists
        collection.drop()

        if verbose:
            print(f"Connected to MongoDB on port {port}. Collection 'reviews' will be created.")

        batch_size = 100
        batch = []

        # Open the JSON file and read line by line
        with open(json_file, "r", encoding="utf-8") as file:
            for line in file:
                try:
                    review = json.loads(line.strip())  # Convert JSON string to dictionary
                    batch.append(review)

                    # Insert when batch reaches the specified size
                    if len(batch) >= batch_size:
                        collection.insert_many(batch)
                        if verbose:
                            print(f"Inserted {len(batch)} reviews into MongoDB.")
                        batch.clear()
                except json.JSONDecodeError as e:
                    print(f"Skipping invalid JSON entry: {e}")

        # Insert any remaining reviews in the last batch
        if batch:
            collection.insert_many(batch)
            if verbose:
                print(f"Inserted the final {len(batch)} reviews into MongoDB.")

        # Confirm data insertion
        total_inserted = collection.count_documents({})
        print(f"✅ Data loading complete. Total documents inserted: {total_inserted}")

    except pymongo.errors.ServerSelectionTimeoutError:
        print("❌ Error: Unable to connect to MongoDB. Ensure the server is running on the specified port.")
    except FileNotFoundError:
        print(f"❌ Error: The file '{json_file}' was not found.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load Amazon reviews from a JSON file into MongoDB.")
    parser.add_argument("json_file", help="Path to the JSON file")
    parser.add_argument("port", type=int, help="MongoDB server port")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()
    load_data_to_mongo(args.json_file, args.port, args.verbose)
