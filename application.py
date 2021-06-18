from tkinter import *
from pprint import *
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import tkinter.messagebox as tkMessageBox
import sqlite3


class db:

    def sql():
        global conn, cursor
        conn = sqlite3.connect('new_hahaha.db')
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS `member` (username text, password text, phone text, birthday text)")
        conn.commit()

    def get_users():
        db.sql()
        cursor.execute("SELECT * FROM `member` ORDER BY `username` ASC")
        auth = cursor.fetchall()
        return auth

    def getuserid(username, password):
        ans = ':('
        db.sql()
        cursor.execute("SELECT * FROM `member` ORDER BY `username` ASC")
        auth = cursor.fetchall()

        if (len(auth)==0):
            return -1

        for i in range(len(auth)):
            if auth[i][0] == username and auth[i][1] == password:
                ans = 'exists'
        
        if ans == 'exists':
            return auth[i] 
        else:
            messagebox.showwarning('Ошибка', 'Пользователь с такими данными не найден')
            return -1

    def register(username, password, phone, birthday):
        db.sql()
        users = db.get_users()
        new_users = [(users[i][0], users[i][2], users[i][3]) for i in range(len(users))]
        if (username, phone, birthday) not in new_users:
            cursor.execute("INSERT INTO `member` (`username`, `password`, `phone`, `birthday`) VALUES (?, ?, ?, ?)", (username, password, phone, birthday,))
            ans = 'good'
        else:
            ans = 'bad'
            messagebox.showwarning('Ошибка', 'Пользователь с такими данными уже зарегистрирован')
        conn.commit()
        return ans


class RegisterFrame(Frame):
    def refresh(self):
        self.pass1.set('')
        self.pass2.set('')
        self.phone.set('')
        self.usEntry_reg.set('')
        self.birth.set('')

    def create_account(self):
        if self.usEntry_reg.get() == "" or self.pass1.get() == "" or self.pass2.get() == "" or self.birth.get() == "" or self.phone.get() == '':
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля")

        if self.pass1.get() != self.pass2.get():
            self.pass1.set('')
            self.pass2.set('')
            messagebox.showwarning("Пароль не совпадает","Пожалуйста, подтвердите свой пароль еще раз")

        elif(self.pass1.get() == ''):
            messagebox.showwarning("Пустые поля","Пожалуйста, не оставляйте поля пустыми")

        else:
            try:
                ans = db.register(self.usEntry_reg.get(), self.pass1.get(), self.phone.get(), self.birth.get())
                if ans == 'good':
                    messagebox.showwarning('Пользователь зарегистрирован', 'Ваши данные в телефонной книжке')
                    Button(self, text='Телефонная книжка', width=15, command=Table).grid(row=7, column=1)
                else:
                    self.controller.show_frame("LoginFrame")
            except:
                messagebox.showwarning('Ошибка', 'Попробуйте другое имя пользователя или пароль')

    def __init__(self,parent,controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.usEntry_reg = StringVar(parent)
        Label(self, text="Имя пользователя").grid(row=0,column=0) 
        Entry(self, textvariable = self.usEntry_reg).grid(row=0,column=1) 

        self.pass1 = StringVar(parent)
        self.pass1.set('')
        self.pass2 = StringVar(parent)
        self.pass2.set('')
        self.phone = StringVar(parent)
        self.phone.set('')
        self.birth = StringVar(parent)
        self.birth.set('')
        
        Label(self, text="Пароль").grid(row=1,column=0)
        Entry(self, show="*", textvariable=self.pass1).grid(row=1,column=1)

        Label(self, text="Повторите пароль").grid(row=2,column=0)
        Entry(self, show="*", textvariable=self.pass2).grid(row=2,column=1)

        Label(self, text="Номер телефона").grid(row=3,column=0)
        Entry(self, textvariable=self.phone).grid(row=3,column=1)
        
        Label(self, text="Дата рождения").grid(row=4,column=0)
        Entry(self, textvariable=self.birth).grid(row=4,column=1)

        Label(self, text='пример: \n 2021-09-17').grid(row=5, column=0)
        
        Button(self, borderwidth=4, text="Регистрация", width=10, pady=4, command=self.create_account, bg='grey').grid(row=5,column=1)
        Button(self, borderwidth=4, text="Отмена", width=10, pady=4, command=lambda: self.controller.show_frame("LoginFrame"), bg='red').grid(row=5,column=2)


class PasswordFrame(Frame):
    def refresh(self):
        self.email.set('')

    def __init__(self,parent,controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.email = StringVar(parent)
        Label(self, text="Адреc электронной почты").grid(row=0,column=0) 
        Entry(self, textvariable = self.email).grid(row=0,column=1) 

        Button(self, borderwidth=4, text="Сменить пароль", width=15, pady=4, command=lambda: self.controller.show_frame("LoginFrame"), bg='gray').grid(row=1,column=1)
        Button(self, borderwidth=4, text="Отмена", width=10, pady=4, command=lambda: self.controller.show_frame("LoginFrame"), bg='red').grid(row=2,column=1)


class LoginFrame(Frame):
    def refresh(self):
        self.pwEntry.set('')
        self.usEntry.set('')
        self.pwEntry.set('')

    def check_password(self):
        self.row = db.getuserid(self.usEntry.get(), self.pwEntry.get())
        self.pwEntry.set('')

        if (self.row == -1):
            self.login_failure()

        else:
            self.usEntry.set('')
            self.login_success()

    def login_success(self):
        Button(self, text='Телефонная книжка', width=15, command=Table).grid(row=5, column=1)
        Button(self, text='Именинники', width=15, command=Birthday_people).grid(row=5, column=2)
        
    def login_failure(self):
        self.wrongpass +=1
        if(self.wrongpass >= 3):
            self.btn_login.configure(state = DISABLED)
        
    def __init__(self,parent,controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.wrongpass = 0
        self.grid(row=0,column=0) 
        self.usEntry = StringVar()
        self.pwEntry = StringVar()
        Label(self, text="Имя пользователя").grid(row=0,column=0) 
        Entry(self,textvariable = self.usEntry).grid(row=0,column=1)

        Label(self, text="Пароль").grid(row=1,column=0) 
        passwd_entry = Entry(self, show="*",textvariable = self.pwEntry)
        passwd_entry.grid(row=1,column=1)

        row = 4
        Button(self, borderwidth=4, text="Войти", width=10, pady=4,
               command=self.check_password, bg='green').grid(row=row,column=0,columnspan=1)
        Button(self, borderwidth=4, text="Регистрация", width=10, pady=4,
               command=lambda: self.controller.show_frame("RegisterFrame"), bg='grey').grid(row=row,column=1,columnspan=1)
        Button(self, borderwidth=4, text="Отмена", width=10, pady=4, command=Exit, bg='red').grid(row=row,column=2)

        Radiobutton(self, text="Запомнить меня", variable=self.usEntry, command=self.login_success).grid(row=6, column=1)

        def toggle_password():
            if passwd_entry.cget('show') == '':
                passwd_entry.config(show='*')
                toggle_btn.config(text='Показать пароль')
            else:
                passwd_entry.config(show='')
                toggle_btn.config(text='Скрыть пароль')

        toggle_btn = tk.Radiobutton(self, text='Показать пароль', width=15, command=toggle_password)
        toggle_btn.grid(row=7, column=1)
        
        Button(self, borderwidth=4, text="Забыли пароль?", width=15, pady=4,
               command=lambda: self.controller.show_frame("PasswordFrame")).grid(row=8,column=1)


class client:
    def __init__(self,user_id):
        if user_id == -1:
            self.username = None
            self.is_admin = None
            self.user_id = None


def Table():
    def delete_records():
        db.sql()
        for selection_item in tree.selection():
            phone = tree.set(selection_item)['Телефон']
            cursor.execute("DELETE FROM `member` WHERE phone=?", (phone,)) #идентификатор личности (один номер - одно имя пользователя)
            tree.delete(selection_item)
        conn.commit()

    scores = tk.Tk() 
    Label(scores, text="Телефонная книжка", font=("Arial", 20)).grid(row=1, columnspan=3)
    cols = ("Имя", "Телефон", "Дата рождения")
    tree = ttk.Treeview(scores, columns=cols, show='headings')

    for col in cols:
        tree.heading(col, text=col, anchor='center')    
        tree.column(col, anchor='center')

    tree.grid(row=1, column=0, columnspan=2)
    users = db.get_users()
    users.sort(key=lambda e: e[0], reverse=False)

    for (name, _, phone, day) in users:
        tree.insert("", "end", values=(name, phone, day))

    Button(scores, text='Удалить', width=15, command=delete_records).grid(row=6, column=1)
    scores.mainloop()


def Birthday_people():
    one_day = timedelta(days=1)

    def get_week(date):
        day_idx = (date.weekday() + 1) % 7 
        sunday = date - timedelta(days=day_idx)
        date = sunday
        for _ in range(7):
            yield date
            date += one_day

    scores = tk.Tk() 
    Label(scores, text="Именинники", font=("Arial", 20)).grid(row=1, columnspan=3)
    cols = ("Имя", "Телефон", "Дата рождения")
    tree = ttk.Treeview(scores, columns=cols, show='headings')

    for col in cols:
        tree.heading(col, text=col, anchor='center')    
        tree.column(col, anchor='center')

    tree.grid(row=1, column=0, columnspan=2)
    users = db.get_users()
    users.sort(key=lambda e: e[3], reverse=False)
    week = [d.isoformat() for d in get_week(datetime.now().date())]
    today = datetime.today().strftime('%Y-%m-%d')

    for (name, _, phone, day) in users:
        new_week = [day[:4] + week[i][4:] for i in range(len(week))]
        if day in new_week and (week[0][:4] + day[4:]) >= today:
            tree.insert("", "end", values=(name, phone, day))

    scores.mainloop()


def Exit():
    result = tkMessageBox.askquestion('Выход', 'Вы уверены, что хотите выйти?', icon="warning")
    if result == 'yes':
        exit()


class SampleApp(Tk):
    def onFrameConfigure(self,canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def FrameWidth(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width = canvas_width)

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.canvas = Canvas(self, borderwidth=0, background="#ffffff")
        self.user = client(-1)
        container = Frame(self.canvas)
        vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_frame = self.canvas.create_window((4,4), window=container, anchor="nw")

        container.bind("<Configure>", lambda event, canvas=self.canvas: self.onFrameConfigure(canvas))
        self.canvas.bind('<Configure>', self.FrameWidth)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginFrame, RegisterFrame, PasswordFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginFrame")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class Login(Tk):
    def register(self):
        pass


def main():
    app = SampleApp()
    app.mainloop()


if __name__ == '__main__':
    main()