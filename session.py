import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

def build_sessions_tab(root):
    form = ttk.LabelFrame(root.sessions_tab, text="Log Session")
    form.pack(fill="x", padx=10, pady=10)

    root.session_client_var = tk.StringVar()
    root.session_date_var = tk.StringVar()
    root.session_hours_var = tk.StringVar()
    root.session_desc_var = tk.StringVar()

    ttk.Label(form, text="Client:").grid(row=0, column=0, sticky="e")
    root.session_client_combo = ttk.Combobox(form, textvariable=root.session_client_var, state="readonly")
    root.session_client_combo.grid(row=0, column=1)

    ttk.Label(form, text="Date:").grid(row=1, column=0, sticky="e")
    ttk.Entry(form, textvariable=root.session_date_var).grid(row=1, column=1)

    ttk.Label(form, text="Hours:").grid(row=2, column=0, sticky="e")
    ttk.Entry(form, textvariable=root.session_hours_var).grid(row=2, column=1)

    ttk.Label(form, text="Description:").grid(row=3, column=0, sticky="e")
    ttk.Entry(form, textvariable=root.session_desc_var).grid(row=3, column=1)

    ttk.Button(form, text="Add Session",
               command=lambda: add_session(root)).grid(row=4, column=0, columnspan=2, pady=5)

    ff = ttk.Frame(root.sessions_tab)
    ff.pack(fill="x", padx=10, pady=5)

    root.filter_client_var = tk.StringVar()
    root.filter_client_combo = ttk.Combobox(ff, textvariable=root.filter_client_var, state="readonly")
    root.filter_client_combo.pack(side="left")
    root.filter_client_combo.bind("<<ComboboxSelected>>", lambda e: refresh_sessions(root))

    ttk.Button(ff, text="Show All", command=lambda: clear_session_filter(root)).pack(side="left")
    ttk.Button(ff, text="Delete", command=lambda: delete_session(root)).pack(side="right")

    cols = ("id","date","client","hours","earnings","description")
    lf = ttk.LabelFrame(root.sessions_tab, text="Sessions")
    lf.pack(fill="both", expand=True, padx=10, pady=10)

    root.sessions_tree = ttk.Treeview(lf, columns=cols, show="headings")
    for c in cols: root.sessions_tree.heading(c, text=c.capitalize())
    root.sessions_tree.pack(side="left", fill="both", expand=True)
    ttk.Scrollbar(lf, command=root.sessions_tree.yview).pack(side="right", fill="y")

def get_client_id(root, name):
    for cid, cname in root.client_choices:
        if cname == name:
            return cid

def add_session(root):
    name = root.session_client_var.get()
    date_str = root.session_date_var.get()
    hours_str = root.session_hours_var.get()
    desc = root.session_desc_var.get()

    if not name:
        return messagebox.showerror("Error", "Client required.")

    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return messagebox.showerror("Error", "Invalid date format.")

    try:
        hours = float(hours_str)
        assert hours > 0
    except:
        return messagebox.showerror("Error", "Hours must be positive.")

    cid = get_client_id(root, name)
    root.conn.execute(
        "INSERT INTO sessions(client_id,date,hours,description) VALUES(?,?,?,?)",
        (cid, date_str, hours, desc or None)
    )
    root.conn.commit()

    root.session_hours_var.set("")
    root.session_desc_var.set("")
    refresh_sessions(root)

def clear_session_filter(root):
    root.filter_client_combo.current(0)
    refresh_sessions(root)

def refresh_sessions(root):
    root.sessions_tree.delete(*root.sessions_tree.get_children())

    q = """SELECT s.id,s.date,c.name AS client,s.hours,
           s.hours*c.hourly_rate AS earnings,s.description
           FROM sessions s JOIN clients c ON s.client_id=c.id"""
    params = []

    if root.filter_client_var.get() != "All clients":
        q += " WHERE c.name=?"
        params.append(root.filter_client_var.get())

    q += " ORDER BY s.date DESC"

    for r in root.conn.execute(q, params):
        root.sessions_tree.insert("", "end",
            values=(r["id"], r["date"], r["client"], r["hours"],
                    round(r["earnings"], 2), r["description"] or ""))

def delete_session(root):
    sel = root.sessions_tree.selection()
    if not sel:
        return messagebox.showwarning("Warning", "No session selected.")

    if not messagebox.askyesno("Confirm", "Delete this session"):
        return

    sid = root.sessions_tree.item(sel[0])["values"][0]
    root.conn.execute("DELETE FROM sessions WHERE id=?", (sid,))
    root.conn.commit()
    refresh_sessions(root)
