Steps required to run the code

-	Ensure that Python 3.0 or above version and MongoDB is installed in the system.
-	Install pymongo (if not already installed):

    Run the following command in your terminal:

 	  Pip3 install pymongo

- Create the database directory:

    Use the command mkdir to create a directory for MongoDB to store its data:

    Mkdir db_folder

- Start the MongoDB server:

    Run the following command to start the MongoDB server with the specified port and database path: 

    Mongod – port 27017 –dbpath db_folder

    Leave this terminal tab/window open to keep the server running.

- Run your Python script for phase-1 with the input file and port number as input:

    Open a new terminal tab/window and run your python script with the port number

    Python3 load-json.py 10000.json 27017

    Enter the Batch No: <Enter a number>

    Ensure your Python script correctly handles the port number as a command-line argument using sys.srgv.

- Verify the results for phase-1:

    Output would be: Data loading complete. Total documents inserted: xx

    Observe the output of your script. Perform the required operations and verify that MongoDB is being accessed correctly.

- Run your Python script for phase-2 with port number as input:

    Python3 phase2_query.py 27017

    Ensure your Python script correctly handles the port number as a command-line argument using sys.srgv.

- Verify the results for phase-2:

- Output would be the menu:

    Connected to the database...

    Menu:
	
    Get average rating of a product

    Find top N highest-rated products

    List most active reviewers
	
    Reviews over time

    Flag suspicious reviews

    Exit

    Enter choice: 1/2/3/4/5/6

    Observe the output of your script. Perform the required operations by traversing the friendly user-friendly menu and verify that MongoDB is being accessed correctly.

- Terminate the MongoDB server:

    Once you're done, stop the MongoDB server by pressing Ctrl +C in the terminal window where it is running.


# SOURCES OF INFORMATION:
This is the place to acknowledge the use of any source of information beside the course textbook and/or class notes

1. Python reference manual was used called geeksforgeeks.org and W3Schools

# AI AGENT USE: 
If you have utilized any AI tools, such as ChatGPT, Deepseek, Claude, Gemini, or other similar AI platforms, you are required to provide more details in the AI Agent section. This should include the prompts you used and the responses you received from the model.
If no AI tools were used, please include a statement confirming this.

- No AI tools, such as ChatGPT, Deepseek, Claude, Gemini, or other similar AI platforms were used.
