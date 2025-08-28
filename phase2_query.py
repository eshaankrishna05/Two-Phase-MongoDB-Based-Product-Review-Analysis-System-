import pymongo
import sys

def connect_to_db(port):
    try:
        client = pymongo.MongoClient(f"mongodb://localhost:{port}/")
        db = client["291db"]
        return db
    except Exception as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)

def get_average_rating(db, asin):
    reviews = db.reviews.find({"asin": asin})
    ratings = [review["overall"] for review in reviews]
    if ratings:
        avg_rating = sum(ratings) / len(ratings)
        print(f"Average rating for ASIN {asin}: {avg_rating:.2f}")
    else:
        print("Invalid ASIN or/No reviews found for this product ASIN.")

def get_top_n_products(db, n):
    pipeline = [
        {"$group": {"_id": "$asin", "avg_rating": {"$avg": "$overall"}}},
        {"$sort": {"avg_rating": -1}},
        {"$limit": n}
    ]
    top_products = db.reviews.aggregate(pipeline)
    for product in top_products:
        print(f"ASIN: {product['_id']}, Average Rating: {product['avg_rating']:.2f}")

def get_most_active_reviewers(db):
    pipeline = [
        {"$group": {"_id": "$reviewerID", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    reviewers = db.reviews.aggregate(pipeline)
    for reviewer in reviewers:
        print(f"ReviewerID: {reviewer['_id']}, Number of Reviews: {reviewer['count']}")

def reviews_over_time(db, asin, years):
    # Ensure years are strings for consistency
    years = [str(year) for year in years]

    # Create an aggregation pipeline to match ASIN and extract years from reviewTime
    pipeline = [
        {"$match": {"asin": asin}},
        {
            "$project": {
                "year": {
                    "$substrCP": ["$reviewTime", {"$subtract": [{"$strLenCP": "$reviewTime"}, 4]}, 4]
                }
            }
        },
        {"$match": {"year": {"$in": years}}},  # Filter for selected years
        {"$group": {"_id": "$year", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]

    review_counts = list(db.reviews.aggregate(pipeline))

    # Initialize a dictionary with all years set to 0
    review_dict = {year: 0 for year in years}
    for review in review_counts:
        review_dict[review["_id"]] = review["count"]

    # Output the review count per year
    for year in years:
        print(f"{year}: {review_dict[year]} reviews")

    # If no reviews found, print a message indicating that
    if all(count == 0 for count in review_dict.values()):
        print(f"No reviews found for ASIN {asin} in the specified years {years}.")
        
def flag_suspicious_reviews(db):
    try:
        user_input = input("Enter the number of suspicious reviews to display (press Enter to show top 10 by default): ")
        limit = int(user_input) if user_input.strip().isdigit() else 10
    except Exception:
        limit = 10

    pipeline = [
        {
            "$match": {
                "$expr": {
                    "$and": [
                        {"$gte": ["$overall", 4.5]},
                        {"$gt": [{"$size": "$helpful"}, 1]},
                        {
                            "$let": {
                                "vars": {
                                    "unhelpful": {"$arrayElemAt": ["$helpful", 0]},
                                    "helpful": {"$arrayElemAt": ["$helpful", 1]}
                                },
                                "in": {
                                    "$lt": [
                                        {"$divide": [
                                            "$$helpful",
                                            {"$max": [{"$add": ["$$helpful", "$$unhelpful"]}, 1]}
                                        ]},
                                        0.1  # Less than 10% helpfulness = suspicious
                                    ]
                                }
                            }
                        }
                    ]
                }
            }
        },
        {
            "$addFields": {
                "helpfulness_ratio": {
                    "$let": {
                        "vars": {
                            "unhelpful": {"$arrayElemAt": ["$helpful", 0]},
                            "helpful": {"$arrayElemAt": ["$helpful", 1]}
                        },
                        "in": {
                            "$divide": [
                                "$$helpful",
                                {"$max": [{"$add": ["$$helpful", "$$unhelpful"]}, 1]}
                            ]
                        }
                    }
                }
            }
        },
        {"$sort": {"helpfulness_ratio": 1}},  # Most suspicious first (lowest ratio)
        {"$limit": limit}
    ]

    suspicious_reviews = list(db.reviews.aggregate(pipeline))

    if suspicious_reviews:
        print(f"\nTop {limit} Suspicious Reviews:")
        for review in suspicious_reviews:
            reviewer_id = review.get('reviewerID', 'N/A')
            helpful = review.get('helpful', [])
            overall = review.get('overall', 'N/A')
            ratio = review.get('helpfulness_ratio', 0)
            print(f"Review ID: {reviewer_id}, Helpful: {helpful}, Overall: {overall}, Helpfulness Ratio: {ratio:.2%}")
    else:
        print("No suspicious reviews found based on the defined criteria.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python phase2_query.py <port>")
        sys.exit(1)
    
    port = sys.argv[1]
    db = connect_to_db(port)
    
    print("Connected to the database...")  # Debugging statement
    
    while True:
        print("\nMenu:")
        print("1. Get average rating of a product")
        print("2. Find top N highest-rated products")
        print("3. List most active reviewers")
        print("4. Reviews over time")
        print("5. Flag suspicious reviews")
        print("6. Exit")
        
        choice = input("Enter choice: ")
        print(f"User chose option: {choice}")  # Debugging statement
        
        if choice == "1":
            asin = input("Enter ASIN: ")
            get_average_rating(db, asin)
        elif choice == "2":
            while True:
                n = input("Enter number of top products to display: ")
                if n.isdigit():  # Check if the input is numeric
                    n = int(n)  # Convert the input to an integer
                    break  # Exit the loop if the input is valid
                else:
                    print("Error: Please enter a numeric value.")  # Error message
            get_top_n_products(db, n)
        elif choice == "3":
            get_most_active_reviewers(db)
        elif choice == "4":
            asin = input("Enter ASIN: ")
            years = input("Enter years (comma-separated, up to 5): ").split(',')
            years = [int(year.strip()) for year in years if year.strip().isdigit()][:5]
            reviews_over_time(db, asin, years)
        elif choice == "5":
            flag_suspicious_reviews(db)
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
