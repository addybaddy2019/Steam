from tkinter import *
from functools import partial

#def onclick(message):
# logica
# mag ook in paats van IF statment (match) gebuiken.
root = Tk()

label = Label(master=root, text="Results: ", height=2)
label.pack()


integer1 = Label(master=root, text="Integer 1: ", height=2)
integer1.pack()
entry1 = Entry(master=root)
entry1.pack(padx=10, pady=10)


integer2 = Label(master=root, text="results: ", height=2)
integer2.pack()

entry2 = Entry(master=root)
entry2.pack(padx=10, pady=10)

addButton = Button(master=root, text="+"
                   command=partial(onclick, ))
addButton.pack(padx=10)

substractButton = Button(master=root, text="-")
substractButton.pack(padx=10)


root.mainloop()

