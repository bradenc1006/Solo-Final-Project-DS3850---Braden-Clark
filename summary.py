import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd, numpy as np
from datetime import datetime

def build_summary_tab(root):
    top = ttk.Frame(root.summary_tab); top.pack(fill="x", padx=10, pady=10)

    ttk.Button(top, text="Refresh", command=lambda: refresh_summary(root)).pack(side="left")
    ttk.Button(top, text="Export CSV", command=lambda: export_summary_csv(root)).pack(side="left")
    ttk.Button(top, text="Invoice", command=lambda: generate_invoice(root)).pack(side="left")

    root.summary_stats_label = ttk.Label(top, text="")
    root.summary_stats_label.pack(side="right")

    cols = ("client","sessions","total_hours","total_earned")
    lf = ttk.LabelFrame(root.summary_tab, text="Summary")
    lf.pack(fill="both", expand=True, padx=10, pady=10)

    root.summary_tree = ttk.Treeview(lf, columns=cols, show="headings")
    for c in cols: root.summary_tree.heading(c, text=c.replace("_"," ").title())
    root.summary_tree.pack(side="left", fill="both", expand=True)
    ttk.Scrollbar(lf, command=root.summary_tree.yview).pack(side="right", fill="y")

def refresh_summary(root):
    root.summary_tree.delete(*root.summary_tree.get_children())

    df = pd.read_sql("""SELECT s.id,c.name AS client,c.hourly_rate,
                        s.date,s.hours,s.description
                        FROM sessions s JOIN clients c ON s.client_id=c.id""",
                     root.conn)

    if df.empty:
        root.summary_df = None
        root.summary_stats_label.config(text="No sessions yet.")
        return

    df["earnings"] = df["hours"] * df["hourly_rate"]

    summary = df.groupby("client").agg(
        sessions=("id","count"),
        total_hours=("hours","sum"),
        total_earned=("earnings","sum")
    ).reset_index()

    summary["total_hours"] = np.round(summary["total_hours"], 2)
    summary["total_earned"] = np.round(summary["total_earned"], 2)

    root.summary_df = summary

    for _, r in summary.iterrows():
        root.summary_tree.insert("", "end",
            values=(r["client"], int(r["sessions"]), r["total_hours"], r["total_earned"]))

    total_hours = np.round(np.sum(df["hours"].to_numpy()), 2)
    avg_earn = np.round(np.mean(df["earnings"].to_numpy()), 2)

    root.summary_stats_label.config(
        text=f"Total hours: {total_hours} | Avg earnings: ${avg_earn}"
    )

def export_summary_csv(root):
    if root.summary_df is None:
        return messagebox.showwarning("Warning", "No data.")
    path = filedialog.asksaveasfilename(defaultextension=".csv",
                                        filetypes=[("CSV","*.csv")])
    if path:
        root.summary_df.to_csv(path, index=False)
        messagebox.showinfo("Saved", f"Exported to {path}")

def generate_invoice(root):
    sel = root.summary_tree.selection()
    if not sel:
        return messagebox.showwarning("Warning", "Select a client.")

    client = root.summary_tree.item(sel[0])["values"][0]

    cur = root.conn.cursor()
    cur.execute("SELECT id,hourly_rate,contact FROM clients WHERE name=?", (client,))
    c = cur.fetchone()

    cur.execute("SELECT date,hours,description FROM sessions WHERE client_id=? ORDER BY date",
                (c["id"],))
    rows = cur.fetchall()

    if not rows:
        return messagebox.showwarning("Warning", "No sessions.")

    total_hours = sum(r["hours"] for r in rows)
    total_earned = round(total_hours * c["hourly_rate"], 2)
    today = datetime.today().strftime("%Y-%m-%d")

    lines = [
        "INVOICE", "",
        f"Client: {client}",
        f"Contact: {c['contact'] or ''}",
        f"Date: {today}",
        f"Rate: ${c['hourly_rate']:.2f}", "",
        "Date        Hours   Earnings   Description",
        "-" * 60
    ]

    for r in rows:
        earn = round(r["hours"] * c["hourly_rate"], 2)
        lines.append(f"{r['date']:10}  {r['hours']:5.2f}  ${earn:7.2f}   {r['description'] or ''}")

    lines += ["", f"Total Hours: {total_hours:.2f}", f"Total Due: ${total_earned:.2f}"]

    path = filedialog.asksaveasfilename(defaultextension=".txt",
                                        filetypes=[("Text","*.txt")])
    if path:
        open(path, "w").write("\n".join(lines))
        messagebox.showinfo("Saved", f"Invoice saved to {path}")
