from tkinter import *


pass_window = Tk()
pass_window.geometry('400x150')

pass_label = Label(pass_window, text='Please enter SSL passphrase:', font='Arial 18')
pass_label.grid(sticky=W, padx=10, pady=10)
pass_entry = Entry(pass_window, width=40, show='*', font='Arial 12')
pass_entry.grid(sticky=W, padx=10, pady=10)


def get_password():
    password = pass_entry.get()
    print(password)
    pass_window.destroy()
    launch_db_window()
    return password


def launch_db_window():
    db_window = Tk()
    db_window.geometry('400x280')
    db_label = Label(db_window, text='Connect to the database:', font='Arial 18')
    db_label.grid(padx=2, pady=2, row=0, column=1, sticky=E)

    db_user_label = Label(db_window, text='Username:', font='Arial 12')
    db_user_label.grid(padx=2, pady=2, row=1, column=0)
    db_user_entry = Entry(db_window, width=29, font='Arial 12')
    db_user_entry.grid(column=1, row=1, padx=10, pady=10)

    db_pass_label = Label(db_window, text='Password:', font='Arial 12')
    db_pass_label.grid(padx=2, pady=2, row=2, column=0, sticky=E)
    db_pass_entry = Entry(db_window, width=29, show='*', font='Arial 12')
    db_pass_entry.grid(column=1, row=2, padx=2, pady=2)

    db_host_label = Label(db_window, text='Host:', font='Arial 12')
    db_host_label.grid(padx=2, pady=2, row=3, column=0, sticky=E)
    db_host_entry = Entry(db_window, width=29, font='Arial 12')
    db_host_entry.grid(column=1, row=3, padx=10, pady=10)

    db_host_label = Label(db_window, text='Port:', font='Arial 12')
    db_host_label.grid(padx=2, pady=2, row=4, column=0, sticky=E)
    db_host_entry = Entry(db_window, width=29, font='Arial 12')
    db_host_entry.grid(column=1, row=4, padx=10, pady=10)

    def connect():
        print(db_pass_entry.get())
        # TODO

    def cancel():
        print('Using in-memory storage')
        # TODO

    db_connect_button = Button(db_window, text='Connect', command=connect)
    db_connect_button.grid(row=5, column=1, padx=10, sticky=E)

    db_cancel_button = Button(db_window, text='Cancel', command=cancel)
    db_cancel_button.grid(row=5, column=0, padx=10, sticky=W)


button = Button(pass_window, text="Ok", command=get_password)
button.grid(padx=10, sticky=E)
mainloop()
