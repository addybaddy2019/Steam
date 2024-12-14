import pandas as pd
from sqlalchemy import create_engine
from tkinter.ttk import Notebook
from tkinter import *
import matplotlib.pyplot as plt
from collections import Counter

# Database connection parameters
DB_CONFIG = {
    "host": "40.114.250.29",
    "port": "5432",
    "database": "steamdb",
    "user": "teammember1",
    "password": "ASDFG"
}

# SQLAlchemy connection string
DATABASE_URI = f'postgresql://{DB_CONFIG["user"]}:{DB_CONFIG["password"]}@{DB_CONFIG["host"]}:{DB_CONFIG["port"]}/{DB_CONFIG["database"]}'

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URI)

# Functie om data uit de database in een Pandas DataFrame te laden
def db_to_pandas(query):
    """
    Laadt data uit de PostgreSQL database en zet het om naar een Pandas DataFrame.
    """
    with engine.connect() as connection:
        return pd.read_sql_query(query, connection)

# Haal de gegevens van gebruikersstatus en games op uit de database
query = """
SELECT users.naam, status.status, games.game 
FROM users
JOIN status ON users.id = status.user_id
JOIN games ON users.id = games.user_id
"""
df = db_to_pandas(query)

# Data parsing: Tel de gebruikers per status
statuses = ["online", "away", "busy", "offline"]
status_count = {status: 0 for status in statuses}

# Tel het aantal gebruikers per status
for _, row in df.iterrows():
    if row["status"] in status_count:
        status_count[row["status"]] += 1

# Scatter plot data
status_labels = list(status_count.keys())
status_values = list(status_count.values())

# Scatter plot maken
plt.scatter(status_labels, status_values)
plt.title("User Status Distribution")
plt.xlabel("Status")
plt.ylabel("Number of Users")
plt.savefig("user_status_plot.png")

# Tkinter venster setup
root = Tk()
root.title("Steam User Data")

# Functie om de scatter plot in een nieuw venster te openen
def open_scatter_plot_in_new_window():
    top = Toplevel()
    top.title("Scatter Plot in New Window")
    top_label = Label(top, text="User Status Distribution:")
    top_label.pack(pady=20)
    scatter_plot_image = PhotoImage(file="user_status_plot.png")
    top_image_label = Label(top, image=scatter_plot_image)
    top_image_label.pack()
    top_image_label.image = scatter_plot_image

# Maak notebook voor tab-interface
tabControl = Notebook(root)

# Maak twee tabbladen
tab1 = Frame(tabControl)
tab2 = Frame(tabControl)

# Voeg tabbladen toe aan notebook
tabControl.add(tab1, text="Welcome")
tabControl.add(tab2, text="Background Information")
tabControl.pack()

# Voeg inhoud toe aan welkom-tabblad
Label(tab1, text="Welcome to my Steam extension").pack(padx=30, pady=30)
Button(tab1, text="Open scatter plot", command=open_scatter_plot_in_new_window).pack(pady=20)

# Voeg achtergrondinformatie toe aan het tweede tabblad
Label(tab2, text="User Status Distribution:").pack(padx=30, pady=30)
scatter_plot = PhotoImage(file="user_status_plot.png")
Label(tab2, image=scatter_plot).pack()

# Start de Tkinter hoofdloop
root.mainloop()
