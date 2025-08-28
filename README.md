Introduction 
The goal of this project is to teach the concept of working with data stored in files and NoSQL databases. This is done by building and operating on a document store, using MongoDB. Your job in this project is to write programs that store data in MongoDB and provide basic functions for searches and update.


Task 
You are given a JSON file, which you will be loading into MongoDB. You should be able to find sample input files attached to this assignment description. The data is obtained from Kaggle and includes a set of Amazon reviews. 


Each review is given in a line and includes: 

The unique ID of the reviewer

The unique ID of the Amazon product  (ASIN: Amazon Standard Identification Number)

The name of the reviewer

Tuple values with votes of helpfulness. For example, [2,4] represents 2 who found it unhelpful, while 4 found it helpful. 

The content of their review message

Overall rating of the product (Max of 5.0) 

Summary of their review message content 

Review time in UNIX and in string value. 


Phase 1: Building a document store 
For this part, you will write a program named load-json with a proper extension (e.g. load-json.py if using Python) which will take in a json file in the current directory and construct a MongoDB collection. Your program will take as input in the command line a json file name and a port number under which the MongoDB server is running, will connect to the server and will create a database named 291db (if it does not exist). Your program will then create a collection named reviews. If the collection exists, your program should drop it and create a new collection. Your program for this phase ends after building the collection.


Data should be inserted in small batches (say 1k-10k reviews per batch) using the insertMany command in MongoDB. The input file is expected to be too large to fit in memory. You may also use Mongoimport ( if available on lab machines).

Phase 2: Operating on the document store
For Phase 2, you will write a program named phase2_query with a proper extension (i.e. phase2_query.py) that supports the following operations on the MongoDB database created in Phase 1. 

Your program will take as input a port number under which the MongoDB server is running, and will connect to a database named 291db on the server. 


Next, users should be able to perform the following tasks: 


Return the average ratings of a product using the ASIN

The user should be able to provide the ASIN, and the system should retrieve all the reviews that match this ASIN, and return the average overall rating for the product. 


Find the Top N products

The user should be able to find the top N highest-rated products across the database by providing the number of products desired to be seen (N). The system should output products that are sorted by average rating, with their ASIN and average score. 


List the most active reviewers

The system should return reviewers sorted by the number of reviews they have written, in descending order. You should limit the output to 10 most active reviewers.


Reviews Over Time 

Show how the number of reviews for a specific product has changed over time. The user should be able to input years of choice (up to 5) for comparison. The system should output a number of reviews per year (e.g. 2013: 13 reviews, 2014: 0 reviews).

                                                 

Flagging Suspicious Reviews 

Identify reviews that might be spam. A user should be able to access reviews with very low helpfulness (fewer than 10% of voters found the review helpful), but high ratings (ratings >= 4.5). The system should output a list of the top 10 potentially suspicious reviews. 


After each action, the user should be able to return to the main menu for further operations. There should also be an option to end the program. Failure to do so will cost you up to 10 marks.

Testing 
You will test your programs using your own datasets while adhering to the project specification. 
