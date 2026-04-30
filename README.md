# Solo-Final-Project-DS3850---Braden-Clark
Final Project for Business Apps Develop
The project is split into multiple Python files so each part of the app has a clear responsibility. Here’s what each file does:

main.py 
This is the entry point of the application. It initializes the database, builds the UI, and starts the Tkinter event loop. If you want to run the app, this is the file you execute.

db.py
Handles all database setup. It creates the clients and sessions tables if they don’t already exist. No UI code lives here — it’s strictly database initialization.

clients.py
Everything related to client management: The “Add Client” form, The client list Treeview, Validation for new clients, Refreshing the client dropdowns used in other tabs

sessions.py
Handles logging and managing work sessions: The session entry form, Date and hour validation, Filtering sessions by client, Deleting sessions, The session list Treeview
