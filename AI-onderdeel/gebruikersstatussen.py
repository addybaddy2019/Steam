from tkinter import *
from tkinter.ttk import Notebook
from PIL import Image, ImageTk
import json
import matplotlib.pyplot as plt

# Functie om JSON-data te lezen van een bestand
def load_json_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Laad de data uit het JSON-bestand
data = load_json_data('friends_data.json')

# Data parsing
statuses = ["online", "away", "busy", "offline"]
status_count = {status: 0 for status in statuses}

# Count number of users for each status
for user in data:
    if user["status"] in status_count:
        status_count[user["status"]] += 1

# Scatter plot data
status_labels = list(status_count.keys())
status_values = list(status_count.values())

# Scatter plot creation
plt.scatter(status_labels, status_values)
plt.title("User Status Distribution")
plt.xlabel("Status")
plt.ylabel("Number of Users")
plt.savefig("user_status_plot.png")

# Tkinter GUI opzetten
root = Tk()
root.title("Steam Analyse Applicatie")
root.geometry("800x600")  # Stel venstergrootte in

# Voeg een notebook toe voor tabbladen
tabControl = Notebook(root)

# Maak tabbladen aan
tab1 = Frame(tabControl)
tab2 = Frame(tabControl)

# Voeg tabbladen toe aan de notebook
tabControl.add(tab1, text="🌟 Welcome 🌟")
tabControl.add(tab2, text="ℹ️ Background Information ℹ️")
tabControl.pack(expand=1, fill="both")

# Voeg inhoud toe aan het 'Welcome'-tabblad
Label(tab1, text="Welkom bij mijn Steam-extensie!", font=("Helvetica", 16, "bold"), fg="#2e7d32").pack(padx=30, pady=20)
Label(tab1, text="Ontdek de verborgen inzichten van Steam-data met een klik!", font=("Helvetica", 12)).pack(padx=30, pady=10)
Button(tab1, text="📊 Open Scatter Plot", bg="#64b5f6", fg="white", font=("Helvetica", 12, "bold")).pack(pady=20)

# Voeg inhoud toe aan het 'Background Information'-tabblad
Label(tab2, text="📈 Gebruikersstatus Distributie", font=("Helvetica", 16, "bold"), fg="#d84315").pack(padx=30, pady=20)
Label(tab2, text="Bekijk hoe gebruikers actief bijdragen en reageren op Steam.", font=("Helvetica", 12)).pack(padx=30, pady=10)

# Gebruik Pillow om een PNG-afbeelding te laden
try:
    scatter_plot_img = Image.open("user_status_plot.png")
    scatter_plot = ImageTk.PhotoImage(scatter_plot_img)
    Label(tab2, image=scatter_plot).pack(padx=10, pady=10)
except Exception as e:
    Label(tab2, text=f"Kan de afbeelding niet laden: {e}", fg="red").pack(padx=30, pady=30)

# Start de GUI
root.mainloop()
