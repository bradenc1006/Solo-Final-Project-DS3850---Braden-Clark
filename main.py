import tkinter as tk
from db import init_db
from clients import build_clients_tab, refresh_clients, refresh_client_dropdowns
from sessions import build_sessions_tab, refresh_sessions
from summary import build_summary_tab, refresh_summary
from utils import close_app
import sqlite3

DB_PATH = "freelance.db"

def build_app(root):
    root.conn = sqlite3.connect(DB_PATH)
    root.conn.row_factory = sqlite3.Row
    root.summary_df = None
    root.client_choices = []

    import tkinter.ttk as ttk
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    root.clients_tab = ttk.Frame(notebook)
    root.sessions_tab = ttk.Frame(notebook)
    root.summary_tab = ttk.Frame(notebook)

    notebook.add(root.clients_tab, text="Clients")
    notebook.add(root.sessions_tab, text="Sessions")
    notebook.add(root.summary_tab, text="Pay Summary & Invoices")

    build_clients_tab(root)
    build_sessions_tab(root)
    build_summary_tab(root)

    refresh_clients(root)
    refresh_client_dropdowns(root)
    refresh_sessions(root)
    refresh_summary(root)

def main():
    init_db()
    root = tk.Tk()
    root.title("Freelance Time & Pay Tracker")
    build_app(root)
    root.protocol("WM_DELETE_WINDOW", lambda: close_app(root))
    root.mainloop()

if __name__ == "__main__":
    main()
