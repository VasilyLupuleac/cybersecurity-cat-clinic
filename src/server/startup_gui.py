from tkinter import *


def launch_password_window():
    pass_window = Tk()
    pass_window.geometry('400x150')
    password = ''

    pass_label = Label(pass_window, text='Please enter SSL passphrase:', font='Arial 18')
    pass_label.grid(sticky=W, padx=10, pady=10)
    pass_entry = Entry(pass_window, width=40, show='*', font='Arial 12')
    pass_entry.grid(sticky=W, padx=10, pady=10)

    def get_password():
        nonlocal password
        password = pass_entry.get()
        pass_window.destroy()

    button = Button(pass_window, text='Ok', command=get_password)
    button.grid(padx=10, sticky=E)
    mainloop()
    return password


def relaunch_password():
    popup = Tk()
    popup.geometry('300x100')
    popup.title('Error')
    plabel = Label(popup, text='Wrong passphrase, please try again', font='Arial 12')
    plabel.grid(sticky=W, padx=10, pady=10)

    okbutton = Button(popup, text='Ok', command=lambda: popup.destroy())
    okbutton.grid(padx=10, pady=10, sticky=E)
    mainloop()
    return launch_password_window()


def password_ok(port):
    popup = Tk()
    popup.geometry('330x100')
    popup.title('Password OK')
    plabel = Label(popup, text=f'HTTPS server will be running on port {port}', font='Arial 12')
    plabel.grid(sticky=W, padx=10, pady=10)
    okbutton = Button(popup, text='Ok', command=lambda: popup.destroy())
    okbutton.grid(padx=10, pady=10, sticky=E)
    mainloop()


def launch_db_window():
    db_params = None
    db_window = Tk()
    db_window.geometry('400x200')
    db_label = Label(db_window, text='Connect to the database:', font='Arial 18')
    db_label.grid(padx=2, pady=2, row=0, column=1, sticky=E)

    db_name_label = Label(db_window, text='DB Name:', font='Arial 12')
    db_name_label.grid(padx=2, pady=2, row=1, column=0)
    db_name_entry = Entry(db_window, width=29, font='Arial 12')
    db_name_entry.grid(column=1, row=1, padx=10, pady=10)

    db_user_label = Label(db_window, text='Username:', font='Arial 12')
    db_user_label.grid(padx=2, pady=2, row=2, column=0, sticky=E)
    db_user_entry = Entry(db_window, width=29, font='Arial 12')
    db_user_entry.grid(column=1, row=2, padx=2, pady=2)

    db_pass_label = Label(db_window, text='Password:', font='Arial 12')
    db_pass_label.grid(padx=2, pady=2, row=3, column=0, sticky=E)
    db_pass_entry = Entry(db_window, width=29, show='*', font='Arial 12')
    db_pass_entry.grid(column=1, row=3, padx=10, pady=10)

    def connect():
        nonlocal db_params
        db_params = (db_name_entry.get(),
                     db_user_entry.get(),
                     db_pass_entry.get())
        db_window.destroy()

    def cancel():
        db_window.destroy()

    db_connect_button = Button(db_window, text='Connect', command=connect)
    db_connect_button.grid(row=5, column=1, padx=10, sticky=E)

    db_cancel_button = Button(db_window, text='Cancel', command=cancel)
    db_cancel_button.grid(row=5, column=0, padx=10, sticky=W)
    mainloop()
    return db_params


def db_ok():
    popup = Tk()
    popup.geometry('300x100')
    popup.title('Database connected')
    plabel = Label(popup, text=f'Successfully connected to the database', font='Arial 12')
    plabel.grid(sticky=W, padx=10, pady=10)
    okbutton = Button(popup, text='Ok', command=lambda: popup.destroy())
    okbutton.grid(padx=10, pady=10, sticky=E)
    mainloop()


def db_error():
    popup = Tk()
    popup.geometry('280x140')
    popup.title('Database error')
    label1 = Label(popup, text=f'Could not connect to the database.', font='Arial 12')
    label1.grid(row=0, column=0, sticky=W, padx=10, pady=10)
    label2 = Label(popup, text=f'Using in-memory storage', font='Arial 12')
    label2.grid(row=1, column=0, sticky=W, padx=10, pady=10)
    okbutton = Button(popup, text='Ok', command=lambda: popup.destroy())
    okbutton.grid(padx=10, pady=10, sticky=E)
    mainloop()

