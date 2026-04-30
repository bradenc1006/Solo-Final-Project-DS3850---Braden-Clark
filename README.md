# Solo-Final-Project-DS3850---Braden-Clark
Final Project for Business Apps Develop made with Python

The project is split into multiple Python files so each part of the app has a clear responsibility. Here’s what each file does:

(main.py) 
This is the entry point of the application. It initializes the database, builds the UI, and starts the Tkinter event loop. If you want to run the app, this is the file you execute.

(db.py)
Handles all database setup. It creates the clients and sessions tables if they don’t already exist. No UI code lives here, it’s strictly database initialization.

(clients.py)
Everything related to client management: The “Add Client” form, The client list Treeview, Validation for new clients, Refreshing the client dropdowns used in other tabs

(sessions.py)
Handles logging and managing work sessions: The session entry form, Date and hour validation, Filtering sessions by client, Deleting sessions, The session list Treeview

(summary.py)
This is where the Pandas and NumPy work happens: Loading joined data from SQLite, Computing earnings, Grouping by client, Displaying the summary, Exporting CSV files, Generating invoices

(cleanup.py)
A small cleanup file. Right now it just contains the cleanup function that closes the database connection when the window is closed.

The database file (freelance.db) is created in the same directory as the code. Earnings are not stored in the database, they’re always calculated live, which keeps everything accurate even if a client’s rate changes later. CSV exports and invoices are saved wherever you choose using the file dialog. If you cancel a save dialog, the app safely does nothing.

Required packages to run the files are pandas, numpys, sqlite3, and tkinter. Make sure you have the latest version of python installed too.

How to run the app

1. Make sure you have Python installed
   
This project requires Python 3.8 or newer.
If you’re not sure what version you have, open a terminal (Command Prompt, PowerShell, or macOS Terminal) and type:

python --version

If Python isn’t installed, download it from:
https://www.python.org/downloads/

Make sure to check “Add Python to PATH” during installation.

2. Install the required Python packages
   
The app uses Pandas and NumPy for the summary calculations. Install them by running:

pip install pandas numpy

Tkinter and SQLite come bundled with most Python installations, so you shouldn’t need to install anything extra for those.

3. Download or clone the project folder
   
Your project should look like this:

freelance_tracker/

 main.py
 db.py
 clients.py
 sessions.py
 summary.py
 utils.py

Make sure all files stay in the same folder. They depend on each other.

4. Open a terminal inside the project folder
   
Navigate to the folder where main.py lives.

5. Run the application
   
Start the program by running:

python main.py

After a moment, a window titled “Freelance Time & Pay Tracker” will appear.

If this is your first time running it, the app will automatically create a SQLite database file called:

freelance.db

You don’t need to set anything up manually. The tables are created for you.

6. Start using the app
Once the window opens, you’ll see three tabs:

Clients - Add new clients, View all clients, Their hourly rates and contact info

Sessions - Log work sessions, Filter sessions by client, Delete sessions, View calculated earnings per session

Pay Summary & Invoices - Generate a Pandas/NumPy summary, Export the summary to CSV, Create a plain‑text invoice for any client

Everything you enter is saved instantly to the database.

7. Closing the app
   
Just close the window normally.
The app safely closes the database connection behind the scenes.

8. Re‑opening the app later
    
Just run:

python main.py
again.

Your clients, sessions, and summaries will still be there. The database persists between runs.
