from tkinter import *
from server import CatClinicServer

password = ''
db_params = None


def launch_password_window():
    pass_window = Tk()
    pass_window.geometry('400x150')

    pass_label = Label(pass_window, text='Please enter SSL passphrase:', font='Arial 18')
    pass_label.grid(sticky=W, padx=10, pady=10)
    pass_entry = Entry(pass_window, width=40, show='*', font='Arial 12')
    pass_entry.grid(sticky=W, padx=10, pady=10)

    def get_password():
        global password

        password = pass_entry.get()
        global server
        try:
            server = CatClinicServer()
            launch_db_window()
        except:
            #top = Toplevel(pass_window)
            #Label(top, text="Wrong password")

            top = Toplevel(pass_window)
            top.geometry("750x250")
            top.title("Child Window")
            label = Label(top, text="Wrong password", font=('Arial 18')).place(x=150, y=80)
            okbutton = Button(top, text="Ok", command=launch_password_window)
            okbutton.grid(padx=10, sticky=E)

    button = Button(pass_window, text="Ok", command=get_password)
    button.grid(padx=10, sticky=E)
    mainloop()


def launch_db_window():
    db_window = Tk()
    db_window.geometry('400x280')
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
        global db_params
        db_params = (db_name_entry.get(),
                     db_user_entry.get(),
                     db_pass_entry.get())

    def cancel():
        print('Using in-memory storage')
        # TODO

    db_connect_button = Button(db_window, text='Connect', command=connect)
    db_connect_button.grid(row=5, column=1, padx=10, sticky=E)

    db_cancel_button = Button(db_window, text='Cancel', command=cancel)
    db_cancel_button.grid(row=5, column=0, padx=10, sticky=W)

launch_password_window()