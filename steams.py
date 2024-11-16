# import alles van module tkinter
from tkinter import *

root = Tk()
# deze loop hierin worden de widgets getekent.
# label toevogen
# een label kan wat tekst tonen in een window.


label = Label(master=root,
              text="IKEA",
              background="Yellow",
              foreground="Blue",
              font=("Arial", 16, "bold"),
              width=15,
              height=8)
# label positionaren in masters
label.pack()
# img = PhotoImage(file ="fietsen_font.png")
# smaller_img = img.subsample(10, 10)
root.mainloop()
