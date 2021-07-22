import socket
import tkinter as tk
from tkinter import *
import time
import threading
import os
from random import randint
from tkinter import filedialog
import string
import random


class GUI:

    # root = tk()
    def new_rand(self):
        # Clear Our Entry Box
        self.pw_entry.delete(0, END)

        # Get PW Length and convert to integer
        self.pw_length = 5

        # create a variable to hold our password
        self.my_password = ''

        # Loop through password length
        letters = string.ascii_lowercase + string.ascii_uppercase
        self.result_str = ''.join(random.choice(letters) for i in range(5))
        # for x in range(self.pw_length):
        #     self.my_password += chr(randint(65, 90), randint(97, 122))

        # Output password to the screen
        self.pw_entry.insert(0, self.result_str)

    # def clipper():
    #     # Clear the clipboard
    #     tk.clipboard_clear()
    #     # Copy to clipboard
    #     tk.clipboard_append(pw_entry.get())

    def __init__(self, ip_address, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((ip_address, port))

        self.Window = tk.Tk()
        self.Window.withdraw()

        self.login = tk.Toplevel()

        self.login.title("Login")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=500, height=400)

        self.pls = tk.Label(self.login,
                            text="Please Login to a chatroom",
                            justify=tk.CENTER,
                            font="Helvetica 12 bold")

        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)

        self.userLabelName = tk.Label(
            self.login, text="Username: ", font="Helvetica 11")
        self.userLabelName.place(relheight=0.2, relx=0.1, rely=0.25)

        self.userEntryName = tk.Entry(self.login, font="Helvetica 12")
        self.userEntryName.place(
            relwidth=0.4, relheight=0.1, relx=0.35, rely=0.30)
        self.userEntryName.focus()

        # Create our Button
        self.my_button = tk.Button(
            self.login, text="Generate Random String", command=self.new_rand)
        self.my_button.place(relx=0.4, rely=0.6)

        # Create Entry Box For Our Returned Password
        self.pw_entry = tk.Entry(self.login, text="", font=(
            "Helvetica", 24), bd=0, bg="systembuttonface")
        self.pw_entry.place(relx=0.4, rely=0.7)

        self.roomLabelName = tk.Label(
            self.login, text="Room Id: ", font="Helvetica 12")
        self.roomLabelName.place(relheight=0.2, relx=0.1, rely=0.40)

        self.roomEntryName = tk.Entry(
            self.login, font="Helvetica 11", show="*")
        self.roomEntryName.place(
            relwidth=0.4, relheight=0.1, relx=0.35, rely=0.45)

        self.go = tk.Button(self.login,
                            text="CONTINUE",
                            font="Helvetica 12 bold",
                            command=lambda: self.goAhead(self.userEntryName.get(), self.roomEntryName.get()))

        self.go.place(relx=0.4, rely=0.8)

        self.Window.mainloop()

    def goAhead(self, username, room_id=0):
        self.name = username
        self.server.send(str.encode(username))
        time.sleep(0.1)
        self.server.send(str.encode(room_id))

        self.login.destroy()
        self.layout()

        rcv = threading.Thread(target=self.receive)
        rcv.start()

    def layout(self):
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False, height=False)
        self.Window.configure(width=470, height=550,
                              bg="#696969")  # warna ga guna
        self.chatBoxHead = tk.Label(self.Window,
                                    bg="#696969",  # warna header
                                    fg="#EAECEE",
                                    text=self.name,
                                    font="Helvetica 11 bold",
                                    pady=5)

        self.chatBoxHead.place(relwidth=1)

        self.line = tk.Label(self.Window, width=450, bg="#ABB2B9")

        self.line.place(relwidth=1, rely=0.07, relheight=0.012)

        self.textCons = tk.Text(self.Window,
                                width=20,
                                height=2,
                                bg="#DEB887",  # warna background chat gede
                                fg="#3c7859",  # font color
                                font="Helvetica 11",
                                padx=5,
                                pady=5)

        self.textCons.place(relheight=0.745, relwidth=1, rely=0.08)

        self.labelBottom = tk.Label(
            self.Window, bg="#696969", height=80)  # warna outer input text

        self.labelBottom.place(relwidth=1,
                               rely=0.8)

        self.entryMsg = tk.Entry(self.labelBottom,
                                 bg="#CD853F",  # warna input kalimat
                                 fg="#000000",  # warna font input kalimat
                                 font="Helvetica 11")
        self.entryMsg.place(relwidth=0.74,
                            relheight=0.03,
                            rely=0.008,
                            relx=0.011)
        self.entryMsg.focus()

        self.buttonMsg = tk.Button(self.labelBottom,
                                   text="Send",
                                   font="Helvetica 10 bold",
                                   width=20,
                                   bg="#ABB2B9",  # warna button send
                                   command=lambda: self.sendButton(self.entryMsg.get()))
        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.03,
                             relwidth=0.22)

        self.labelFile = tk.Label(self.Window, bg="#696969", height=70)

        self.labelFile.place(relwidth=1,
                             rely=0.9)

        self.fileLocation = tk.Label(self.labelFile,
                                     text="Choose file to send",
                                     bg="#CD853F",  # warna background tulisan location file
                                     fg="#000000",  # warna font tulisan location file
                                     font="Helvetica 11")
        self.fileLocation.place(relwidth=0.65,
                                relheight=0.03,
                                rely=0.008,
                                relx=0.011)

        self.browse = tk.Button(self.labelFile,
                                text="Browse",
                                font="Helvetica 10 bold",
                                width=13,
                                bg="#ABB2B9",  # warna button browse
                                command=self.browseFile)
        self.browse.place(relx=0.67,
                          rely=0.008,
                          relheight=0.03,
                          relwidth=0.15)

        self.sengFileBtn = tk.Button(self.labelFile,
                                     text="Send",
                                     font="Helvetica 10 bold",
                                     width=13,
                                     bg="#ABB2B9",  # warna button send
                                     command=self.sendFile)
        self.sengFileBtn.place(relx=0.84,
                               rely=0.008,
                               relheight=0.03,
                               relwidth=0.15)

        self.textCons.config(cursor="arrow")
        scrollbar = tk.Scrollbar(self.textCons)
        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.textCons.yview)
        self.textCons.config(state=tk.DISABLED)

    def browseFile(self):
        self.filename = filedialog.askopenfilename(initialdir="/",
                                                   title="Select a file",
                                                   filetypes=(("Text files",
                                                               "*.txt*"),
                                                              ("all files",
                                                               "*.*")))
        self.fileLocation.configure(text="File Opened: " + self.filename)

    def sendFile(self):
        self.server.send("FILE".encode())
        time.sleep(0.1)
        self.server.send(
            str("client_" + os.path.basename(self.filename)).encode())
        time.sleep(0.1)
        self.server.send(str(os.path.getsize(self.filename)).encode())
        time.sleep(0.1)

        file = open(self.filename, "rb")
        data = file.read(1024)
        while data:
            self.server.send(data)
            data = file.read(1024)
        self.textCons.config(state=tk.DISABLED)
        self.textCons.config(state=tk.NORMAL)
        self.textCons.insert(tk.END, "<You> "
                                     + str(os.path.basename(self.filename))
                                     + " Sent\n\n")
        self.textCons.config(state=tk.DISABLED)
        self.textCons.see(tk.END)

    def sendButton(self, msg):
        self.textCons.config(state=tk.DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, tk.END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()

    def receive(self):
        while True:
            try:
                message = self.server.recv(1024).decode()

                if str(message) == "FILE":
                    file_name = self.server.recv(1024).decode()
                    lenOfFile = self.server.recv(1024).decode()
                    send_user = self.server.recv(1024).decode()

                    if os.path.exists(file_name):
                        os.remove(file_name)

                    total = 0
                    with open(file_name, 'wb') as file:
                        while str(total) != lenOfFile:
                            data = self.server.recv(1024)
                            total = total + len(data)
                            file.write(data)

                    self.textCons.config(state=tk.DISABLED)
                    self.textCons.config(state=tk.NORMAL)
                    self.textCons.insert(
                        tk.END, "<" + str(send_user) + "> " + file_name + " Received\n\n")
                    self.textCons.config(state=tk.DISABLED)
                    self.textCons.see(tk.END)

                else:
                    self.textCons.config(state=tk.DISABLED)
                    self.textCons.config(state=tk.NORMAL)
                    self.textCons.insert(tk.END,
                                         message+"\n\n")

                    self.textCons.config(state=tk.DISABLED)
                    self.textCons.see(tk.END)

            except:
                print("An error occured!")
                self.server.close()
                break

    def sendMessage(self):
        self.textCons.config(state=tk.DISABLED)
        while True:
            self.server.send(self.msg.encode())
            self.textCons.config(state=tk.NORMAL)
            self.textCons.insert(tk.END,
                                 "<You> " + self.msg + "\n\n")

            self.textCons.config(state=tk.DISABLED)
            self.textCons.see(tk.END)
            break


if __name__ == "__main__":
    ip_address = "127.0.0.1"
    port = 12345
    g = GUI(ip_address, port)
