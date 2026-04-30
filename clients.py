import tkinter as tk
from tkinter import ttk, messagebox

def build_clients_tab(root):
    form = ttk.LabelFrame(root.clients_tab, text="Add Client")
    form.pack(fill="x", padx=10, pady=10)

    root.client_name_var = tk.StringVar()
    root.client_rate_var = tk.StringVar()
    root.client_contact_var = tk.StringVar()

    ttk.Label(form, text="Name:").grid(row=0, column=0, sticky="e")
    ttk.Entry(form, textvariable=root.client_name_var).grid(row=0, column=1)

    ttk.Label(form, text="Hourly Rate:").grid(row=1, column=0, sticky="e")
    ttk.Entry(form, textvariable=root.client_rate_var).grid(row=1, column=1)

    ttk.Label(form, text="Contact:").grid(row=2, column=0, sticky="e")
    ttk.Entry(form, textvariable=root.client_contact_var).grid(row=2, column=1)

    ttk.Button(form, text="Add Client",
               command=lambda: add_client(root)).grid(row=3, column=0, columnspan=2, pady=5)

    cols = ("id","name","hourly_rate","contact","active")
    lf = ttk.LabelFrame(root.clients_tab, text="Clients")
    lf.pack(fill="both", expand=True, padx=10, pady=10)

    root.clients_tree = ttk.Treeview(lf, columns=cols, show="headings")
    for c in cols: root.clients_tree.heading(c, text=c.capitalize())
    root.clients_tree.pack(side="left", fill="both", expand=True)
    ttk.Scrollbar(lf, command=root.clients_tree.yview).pack(side="right", fill="y")

def add_client(root):
    name = root.client_name_var.get().strip()
    rate_str = root.client_rate_var.get().strip()
    contact = root.client_contact_var.get().strip()

    if not name:
        return messagebox.showerror("Error", "Client name required.")

    try:
        rate = float(rate_str)
        assert rate > 0
    except:
        return messagebox.showerror("Error", "Hourly rate must be positive.")

    try:
        root.conn.execute(
            "INSERT INTO clients(name,hourly_rate,contact,active) VALUES(?,?,?,1)",
            (name, rate, contact or None)
        )
        root.conn.commit()
    except:
        return messagebox.showerror("Error", "Client name must be unique.")

    root.client_name_var.set("")
    root.client_rate_var.set("")
    root.client_contact_var.set("")

    refresh_clients(root)
    refresh_client_dropdowns(root)

def refresh_clients(root):
    root.clients_tree.delete(*root.clients_tree.get_children())
    for r in root.conn.execute("SELECT * FROM clients ORDER BY name"):
        root.clients_tree.insert("", "end",
            values=(r["id"], r["name"], r["hourly_rate"], r["contact"] or "", r["active"]))

def refresh_client_dropdowns(root):
    rows = list(root.conn.execute("SELECT id,name FROM clients WHERE active=1 ORDER BY name"))
    root.client_choices = [(r["id"], r["name"]) for r in rows]
    names = [n for _, n in root.client_choices]

    root.session_client_combo["values"] = names
    if names: root.session_client_combo.current(0)

    root.filter_client_combo["values"] = ["All clients"] + names
    root.filter_client_combo.current(0)
