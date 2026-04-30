# Solo-Final-Project-DS3850---Braden-Clark
Final Project for Business Apps Develop
The project is split into multiple Python files so each part of the app has a clear responsibility. Here’s what each file does:

main.py 
This is the entry point of the application. It initializes the database, builds the UI, and starts the Tkinter event loop. If you want to run the app, this is the file you execute.

db.py
Handles all database setup. It creates the clients and sessions tables if they don’t already exist. No UI code lives here, it’s strictly database initialization.

clients.py
Everything related to client management: The “Add Client” form, The client list Treeview, Validation for new clients, Refreshing the client dropdowns used in other tabs

sessions.py
Handles logging and managing work sessions: The session entry form, Date and hour validation, Filtering sessions by client, Deleting sessions, The session list Treeview

summary.py
This is where the Pandas and NumPy work happens: Loading joined data from SQLite, Computing earnings, Grouping by client, Displaying the summary, Exporting CSV files, Generating invoices

cleanup.py
A small cleanup file. Right now it just contains the cleanup function that closes the database connection when the window is closed.

The database file (freelance.db) is created in the same directory as the code. Earnings are not stored in the database, they’re always calculated live, which keeps everything accurate even if a client’s rate changes later. CSV exports and invoices are saved wherever you choose using the file dialog. If you cancel a save dialog, the app safely does nothing.

Required packages to run the files are pandas, numpys, sqlite3, and tkinter. Make sure you have the latest version of python installed too.

How to Run the App
Make sure you have newest Python installed.

Install the required packages:

Code
pip install pandas numpy

Open a terminal in the project folder.

Run:

Code
python main.py

The app window will open, and the database will be created automatically if it doesn’t exist.
