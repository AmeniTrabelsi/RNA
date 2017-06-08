
from Tkinter import *

#creat the window
#root = Tk()

#create label
# theLabel = Label(root, text="This is too easy")
# theLabel.pack()

##create frame
# topFrame = Frame(root)
# topFrame.pack()
# bottomFrame = Frame(root)
# bottomFrame.pack(side=BOTTOM)

#create button
# button1 = Button(topFrame, text="Button 1", fg="red")
# button2 = Button(topFrame, text="Button 2", fg="blue")
# button3 = Button(topFrame, text="Button 3", fg="green")
# button4 = Button(bottomFrame, text="Button 4", fg="purple")
# button1.pack(side=LEFT)
# button2.pack(side=LEFT)
# button3.pack(side=LEFT)
# button4.pack(side=BOTTOM)

#fill the label
# one = Label(root, text="One", bg="red", fg="white")
# one.pack()
# two = Label(root, text="Two", bg="green", fg="black")
# two.pack(fill=X)
# three = Label(root, text="Three", bg="blue", fg="white")
# three.pack(side=LEFT, fill=Y)

#grid
# label_1 = Label(root, text="Name")
# label_2 = Label(root, text="Password")
# entry_1 = Entry(root)
# entry_2 = Entry(root)
# label_1.grid(row=0, sticky=E)
# label_2.grid(row=1, sticky=E)
# entry_1.grid(row=0, column=1)
# entry_2.grid(row=1, column=1)

#checkbox
# c = Checkbutton(root, text="Keep me logged in")
# c.grid(columnspan=2)

###connect function to button 1
# def printName():
#     print("Hello my name is Bucky!")
#
# button_1 = Button(root, text="Print my name", command=printName)
# button_1.pack()

###connect function to button 2
# def printName(event):
#     print("Hello my name is Bucky!")
#
# button_1 = Button(root, text="Print my name")
# button_1.bind("<Button-1>", printName)
# button_1.pack()

####mouse click event
# def leftClick(event):
#     print("Left")
#
# def middleClick(event):
#     print("Middle")
#
# def rightClick(event):
#     print("Right")
#
# frame = Frame(root, width=300, height=250)
# frame.bind("<Button-1>", leftClick)
# frame.bind("<Button-2>", middleClick)
# frame.bind("<Button-3>", rightClick)
# frame.pack()

#using class
# class BuckysButtons:
#
#     def __init__(self, master):
#        frame = Frame(master)
#        frame.pack()
#
#        self.printButton = Button(frame, text="Print Message", command=self.printMessage)
#        self.printButton.pack(side=LEFT)
#
#        self.quitButton = Button(frame, text="Quit", command=frame.quit)
#        self.quitButton.pack(side=LEFT)
#
#     def printMessage(self):
#         print("Wow, this actually worked!")
#
#
# root = Tk()
# b = BuckysButtons(root)
#kick off the event loop


# create drop down menus

def doNothing():
    print("ok ok I won't...")

root = Tk()

menu = Menu(root)
root.config(menu=menu)

subMenu = Menu(menu)
menu.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="New project...", command=doNothing)
subMenu.add_command(label="New...", command=doNothing)
subMenu.add_separator()
subMenu.add_command(label="Exit", command=doNothing)

editMenu = Menu(menu)
menu.add_cascade(label="Edit", menu=editMenu)
editMenu.add_command(label="Redo", command=doNothing)

root.mainloop()