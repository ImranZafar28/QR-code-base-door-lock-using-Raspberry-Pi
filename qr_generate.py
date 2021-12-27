# Muhammad Imran Zafar
# Ammarah Kanwal
# Fareha Akram
# Aamash Khan
# Anwar Siddiqui

import qrcode
from tkinter import *
import pymysql

root=Tk()
root.geometry("500x300")
root.title("QR Code")

db = pymysql.connect(
    host="localhost",
    user="imran",
    passwd="12345",
    database="mydatabase"
)

data_var=StringVar()


def submit():
    data=data_var.get()
    filename = data+"_qr.png"
    img = qrcode.make(data)
    img.save(filename)
    
    mycursor = db.cursor()
    insertQuery = "INSERT INTO students (id) VALUES ('"+data+"');"
    mycursor.execute(insertQuery)
    db.commit()
    db.close()
    
    data=''
    data_var.set('')

l = Label(root, text="QR Code generate", font="normal 20 bold", fg="#4d594e").pack(pady=20)
e = Entry(root, textvariable=data_var, font="normal 16", bd=5).pack(pady=20)
b = Button(root, text="GENERATE", font="normal 16 bold", fg="#3cb833", bg="black", command=submit).pack(pady=20)

root.mainloop()
