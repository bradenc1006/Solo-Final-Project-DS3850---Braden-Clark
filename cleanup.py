def close_app(root):
    try:
        root.conn.close()
    except:
        pass
    root.destroy()
