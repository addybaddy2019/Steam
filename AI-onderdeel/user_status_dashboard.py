# Team FaaaM,
# Opdracht: Steam_AI_deel
from tkinter.ttk import Notebook
from tkinter import *
import matplotlib.pyplot as plt

# Nieuwe lijsten van gebruikersgegevens
naam_lijst = [
    "Anas", "Adnan Omar", "Fu-An", "Morrid", "Ahmed", "Serik", "Oscar", "Adam",
    "Abdulilah", "Ahmetcan", "Kaan", "Rachid", "Melih", "Safoun", "Jesmar",
    "Rick", "Lesley", "Deniz", "Dennis", "Idir", "Nabil", "Sem", "Test Project"
]

status_lijst = [
    "online", "online", "offline", "away", "away", "online", "busy", "online",
    "online", "online", "busy", "away", "online", "busy", "online", "busy",
    "away", "online", "away", "away", "busy", "online", "offline"
]

game_lijst = [
    "Minecraft", "League of Legends (Arcane)", "", "Kruner IO", "Roblox",
    "Counter-Strike: Global Offensive", "Dota 2", "Valorant", "chess", "CSGO",
    "Apex Legends", "World of Warcraft", "Call of Duty: Warzone", "Genshin Impact",
    "overwatch 2", "PUBG", "Fortnite", "Fifa 24", "Red Dead Redemption 2",
    "Elden Ring", "The Witcher 3", "Rocket League", ""
]

# Tellen van gebruikers per status
status_types = ["online", "away", "busy", "offline"]
status_counts = {status: status_lijst.count(status) for status in status_types}

# Scatter plot gegevens
status_labels = list(status_counts.keys())
status_values = list(status_counts.values())

# Scatter plot maken
plt.scatter(status_labels, status_values)
plt.title("Aantal gebruikers per status")
plt.xlabel("Status")
plt.ylabel("Aantal Gebruikers")
plt.savefig("user_status_plot.png")

# Tkinter venster instellen
root = Tk()
root.title("Gebruikers Status Visualisatie")

# Functie om de scatter plot in een nieuw venster te openen
def open_scatter_plot_in_new_window():
    top = Toplevel()
    top.title("Scatter plot in nieuw venster")
    top_label = Label(top, text="Aantal Gebruikers per Status:")
    top_label.pack(pady=20)
    scatter_plot_image = PhotoImage(file="user_status_plot.png")
    top_image_label = Label(top, image=scatter_plot_image)
    top_image_label.pack()
    top_image_label.image = scatter_plot_image

# Tabblad interface maken
tabControl = Notebook(root)

# Twee tabbladen maken
tab1 = Frame(tabControl)
tab2 = Frame(tabControl)

# Voeg de tabbladen toe aan het tabbladbeheersysteem
tabControl.add(tab1, text="Welkom")
tabControl.add(tab2, text="Achtergrondinformatie")
tabControl.pack()

# Voeg informatie toe aan het eerste tabblad
Label(tab1, text="Welkom bij mijn Steam uitbreiding").pack(padx=30, pady=30)
Button(tab1, text="Open scatter plot", command=open_scatter_plot_in_new_window).pack(pady=20)

# Voeg achtergrondinformatie toe aan het tweede tabblad
Label(tab2, text="Aantal Gebruikers per Status:").pack(padx=30, pady=30)
scatter_plot = PhotoImage(file="user_status_plot.png")
Label(tab2, image=scatter_plot).pack()

# Start de Tkinter hoofdloop
root.mainloop()
