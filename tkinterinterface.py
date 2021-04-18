from tkinter import *
import os

def got_clicked():
    os.system('python im3.py')
top = Tk()
top.title("SRM Attendance System")
top.geometry("500x500")
label=Label(top,text="Attendance System using Face Recognition",relief=RAISED)
img=PhotoImage(file='srmlogo.png')
Label(top,image=img).pack()
label.pack()
my_button = Button(text="Start Face Recognition", command=got_clicked)
my_button.pack()
top.mainloop()