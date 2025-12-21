from sqlite3 import connect
from tkinter import Label, Button, Tk, PhotoImage, Frame, Entry, Toplevel, StringVar
import tkinter.ttk as ttk
from tkinter import messagebox
import os
from datetime import datetime, timedelta
from tkcalendar import DateEntry
from tksheet import Sheet
from texttable import Texttable
from subprocess import Popen
from hashlib import sha256
import threading
from PIL import Image, ImageTk
import math


# Setting up main window
root = Tk()
root.title("Casheir System")
root.state('zoomed')
root.resizable(False, False)
root.iconbitmap('meat.ico')
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

root.update()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

db = connect("main.db", check_same_thread=False)
cr = db.cursor()

sell = 'بيع'
returned = 'مرتجع'

# Creating styles #
# Notebook Style
main_ntbk_style = ttk.Style()
ntbk_font = ("Arial", 12, "bold")
main_ntbk_style.configure('TNotebook', font=ntbk_font)

# Treeview Style
tree_style = ttk.Style()
tree_style.theme_use('clam')
tree_style.configure('Treeview', 
            background='#3286c4',
            foreground='black',
            fieldbackground='white',)

tree_style.configure('Treeview.Heading',
            background='#3286c4',
            foreground='black',
            fieldbackground='white',)

tree_style.map('Treeview.Heading', background=[('!selected', '#3286c4')])

s = ttk.Style()
s.configure('TNotebook', background='#3286c4')
s.configure('TNotebook.Tab', font=('Segoe UI', 10), foreground='black', background='grey')
s.map('TNotebook', background=[('selected', '#d9d9d9'), ('!selected', '#d9d9d9')])
s.map('TNotebook.Tab', background=[('selected', '#d9d9d9'), ('!selected', '#d9d9d9')])

s2 = ttk.Style()
s2.configure('TMenubutton', font=('Segoe UI', 16), width=14, position='e')
s2.configure('TMenubutton.Menu', font=('Segoe UI', 16), position='e')

# Loading images
cashier_img = PhotoImage(file="imgs/cashier.png")
admin_img = PhotoImage(file="imgs/admin.png")
plus_img = PhotoImage(file="imgs/plus.png")
cancel_img = PhotoImage(file="imgs/cancel.png")
zero = PhotoImage(file="imgs/nums/0.png")
one = PhotoImage(file="imgs/nums/1.png")
two = PhotoImage(file="imgs/nums/2.png")
three = PhotoImage(file="imgs/nums/3.png")
four = PhotoImage(file="imgs/nums/4.png")
five = PhotoImage(file="imgs/nums/5.png")
six = PhotoImage(file="imgs/nums/6.png")
seven = PhotoImage(file="imgs/nums/7.png")
eight = PhotoImage(file="imgs/nums/8.png")
nine = PhotoImage(file="imgs/nums/9.png")
price_img = PhotoImage(file="imgs/price.png")
gear_img = PhotoImage(file="imgs/one_gear.png")
gears_img = PhotoImage(file="imgs/gears.png")
cheque_img = PhotoImage(file="imgs/cheque.png")
add_img = PhotoImage(file="imgs/add.png")
return_img = PhotoImage(file="imgs/return.png")
login_img = PhotoImage(file="imgs/login.png")
logout_img = PhotoImage(file="imgs/logout.png")
passwd_img = PhotoImage(file="imgs/password.png")
return_one_img = PhotoImage(file="imgs/return_one.png")
view_img = PhotoImage(file="imgs/view.png")
receipt_img = PhotoImage(file="imgs/receipt.png")
daily_inventory_img = PhotoImage(file="imgs/daily-inventory.png")
monthly_inventory_img = PhotoImage(file="imgs/monthly-inventory.png")

nums = [zero, one, two, three, four, five, six, seven, eight, nine]

# Creating auto threading function
def run_in_thread(fn):
    def run(*k, **kw):
        t = threading.Thread(target=fn, args=k, kwargs=kw)
        t.start()
        return t
    return run

# creating hoover effect function
def on_enter(e, event=None):
    e.widget['background'] = '#1E4F9F'
def on_leave(e, event=None):
    e.widget['background'] = '#2C61BD'

# Create main tabs

main_tabs_ntbk = ttk.Notebook(root)
main_tabs_ntbk.pack(expand=1, fill="both")

cashier_tab = Frame(main_tabs_ntbk, bg="#2C61BD")
admin_tab = Frame(main_tabs_ntbk, bg="#2C61BD")
cashier_tab.columnconfigure(1, weight=1)  # Give weight to column 1 (basket)

main_tabs_ntbk.add(cashier_tab, text="كاشير", image=cashier_img, compound='left')
main_tabs_ntbk.add(admin_tab, text="الادارة", image=admin_img, compound='left')

admin_login_frm = Frame(admin_tab, bg="#2C61BD")
admin_login_frm.pack(fill='both', expand=1)

admin_login_btns_frm = Frame(admin_login_frm, bg="#2C61BD")
admin_login_btns_frm.pack(pady=20)

admin_passwd_lbl = Label(admin_login_btns_frm, text=":كلمة المرور", font=("Arial", 18, "bold"), bg="#2C61BD")
admin_passwd_lbl.grid(row=0, column=1, padx=10, pady=10)

admin_passwd_ent = Entry(admin_login_btns_frm, font=("Arial", 18), show="*")
admin_passwd_ent.grid(row=0, column=0, padx=10, pady=10)

admin_login_btn = Button(admin_login_frm, text="تسجيل الدخول", font=("Arial", 18, "bold"), bg="#2C61BD",
                        image=login_img, compound='right', relief='sunken')
admin_login_btn.pack(pady=10)

admin_mngmnt_frm = Frame(admin_tab, bg="#2C61BD")
# admin_mngmnt_frm.pack(fill='both', expand=1)

admin_mngmnt_ntbk = ttk.Notebook(admin_mngmnt_frm)
admin_mngmnt_ntbk.pack(fill='both', expand=1)

inventories_tab = Frame(admin_mngmnt_ntbk, bg="#2C61BD")
expenses_tab = Frame(admin_mngmnt_ntbk, bg="#2C61BD")
logout_tab = Frame(admin_mngmnt_ntbk, bg="#2C61BD")

admin_mngmnt_ntbk.add(inventories_tab, text="الجرد")
admin_mngmnt_ntbk.add(expenses_tab, text="المصروفات")
admin_mngmnt_ntbk.add(logout_tab, text="تسجيل الخروج", image=logout_img, compound='left')

sold_items_btn = Button(inventories_tab, text="الأصناف المباعة", font=("Arial", 18, "bold"), bg="#2C61BD", relief='sunken',
                        width=((screen_width//5)-30) , image=gears_img, compound='right', padx=5)
sold_items_btn.grid(row=0, column=0, padx=5, pady=10)

daily_net_btn = Button(inventories_tab, text="صافي اليوم", font=("Arial", 18, "bold"), bg="#2C61BD", relief='sunken',
                        width=((screen_width//5)-30) , image=cheque_img, compound='right', padx=5)
daily_net_btn.grid(row=0, column=1, padx=5, pady=10)

daily_bills_btn = Button(inventories_tab, text="الفوتير اليومية", font=("Arial", 18, "bold"), bg="#2C61BD", relief='sunken',
                        width=((screen_width//5)-30) , image=daily_inventory_img, compound='right', padx=5)
daily_bills_btn.grid(row=0, column=2, padx=5, pady=10)

monthly_inventory_btn = Button(inventories_tab, text="الجرد الشهري", font=("Arial", 18, "bold"), bg="#2C61BD", relief='sunken',
                        width=((screen_width//5)-30) , image=gear_img, compound='right', padx=5)
monthly_inventory_btn.grid(row=0, column=3, padx=5, pady=10)

print_inventory_btn = Button(inventories_tab, text="طباعة الجرد", font=("Arial", 18, "bold"), bg="#2C61BD", relief='sunken',
                        width=((screen_width//5)-30) , image=receipt_img, compound='right', padx=5)
print_inventory_btn.grid(row=0, column=4, padx=5, pady=10)

inventory_sheet_frame = Frame(inventories_tab, bg="#2C61BD")
inventory_sheet_frame.grid(row=1, column=0, columnspan=5, sticky='nsew')

inventories_sheet = Sheet(inventory_sheet_frame,
                        headers=[],
                        height=screen_height-100,
                        width=screen_width-100,
                        show_x_scrollbar=True,
                        show_y_scrollbar=True,
                        bg="#2C61BD",
                        header_bg="#3286c4",
                        header_fg="black",
                        even_bg="#d9d9d9",
                        odd_bg="white",
                        )
inventories_sheet.enable_bindings(("single_select", "row_select", "column_select", "column_width_resize", "arrowkeys",
                                    "right_click_popup_menu", "rc_select", "copy"))
inventories_sheet.pack(expand=1, fill="both")



def logout_admin():
    admin_mngmnt_frm.pack_forget()
    admin_login_frm.pack(fill='both', expand=1)
    admin_mngmnt_ntbk.select(0)  # switching back to first tab

# admin_mngmnt_ntbk.bind('<<NotebookTabChanged>>', logout_admin)

def admin_login():
    passwd = sha256(admin_passwd_ent.get().encode()).hexdigest()
    stored_passwd = cr.execute("SELECT passwd FROM info").fetchone()[0]
    if passwd == stored_passwd:
        admin_login_frm.pack_forget()
        admin_mngmnt_frm.pack(fill='both', expand=1)
        admin_passwd_ent.delete(0, 'end')
    else:
        messagebox.showerror("خطأ", "كلمة المرور غير صحيحة")
        admin_passwd_ent.delete(0, 'end')
    
admin_passwd_ent.bind('<Return>', lambda event: admin_login())
admin_login_btn['command'] = admin_login

def daily_bills():
    # Clearing previous data
    for i in range(inventories_sheet.get_total_rows()):
        inventories_sheet.delete_row(0, redraw=False)
    # removing extra columns if exists
    if inventories_sheet.get_total_columns() > len(['رقم الفاتورة', 'العملية', 'الصنف', 'الكمية', 'سعر الوحدة', 'الاجمالي', 'الوقت']):
        for i in range(inventories_sheet.get_total_columns() - len(['رقم الفاتورة', 'العملية', 'الصنف', 'الكمية', 'سعر الوحدة', 'الاجمالي', 'الوقت'])):
            inventories_sheet.delete_column(inventories_sheet.get_total_columns()-1, redraw=False)


    inventories_sheet.set_header_data(['رقم الفاتورة', 'العملية', 'الصنف', 'الكمية', 'سعر الوحدة', 'الاجمالي', 'الوقت'])

    # inventories_sheet.headers(['رقم الفاتورة', 'العملية', 'الصنف', 'الكمية', 'سعر الوحدة', 'الاجمالي', 'الوقت'])
    bills = cr.execute("SELECT * FROM daily_log").fetchall()
    for bill in bills:
        inventories_sheet.insert_row([bill[0], bill[1], bill[2], bill[3], bill[4], bill[5], bill[6]])
    # disabling daily bills button to prevent multiple clicks
    for widget in inventories_tab.winfo_children():
        if isinstance(widget, Button):
            if widget['text'] == "الفوتير اليومية":
                widget['state'] = 'disabled'
            else:
                widget['state'] = 'normal'

daily_bills_btn['command'] = daily_bills

def monthly_inventory_lvl():
    pass  # Here you

monthly_inventory_btn['command'] = monthly_inventory_lvl

def print_inventory():
    pass  # Here you
print_inventory_btn['command'] = print_inventory

def sold_items():
    for i in range(inventories_sheet.get_total_rows()):
        inventories_sheet.delete_row(0, redraw=False)
    if inventories_sheet.get_total_columns() > len(['الصنف', 'الكمية المباعة', 'الإجمالي']):
        for i in range(inventories_sheet.get_total_columns()):
            # deleting extra columns from the end
            inventories_sheet.delete_column(0, redraw=False)
    # removing previous headers and setting new ones
    inventories_sheet.set_header_data(['الصنف', 'الكمية المباعة', 'الإجمالي'])
    sold_items = cr.execute("""SELECT DISTINCT item_name FROM daily_log""").fetchall()

    for item in sold_items:
        item_name = item[0]
        total_qty = cr.execute(f"""SELECT SUM(quantity) FROM daily_log WHERE item_name = '{item_name}' AND transaction_type = '{sell}'""").fetchone()[0]
        total_price = cr.execute(f"""SELECT SUM(total) FROM daily_log WHERE item_name = '{item_name}' AND transaction_type = '{sell}'""").fetchone()[0]
        inventories_sheet.insert_row([item_name, total_qty, total_price])
    sub_total = cr.execute(f"""SELECT SUM(total) FROM daily_log WHERE transaction_type = '{sell}'""").fetchone()[0]
    inventories_sheet.insert_row(['الإجمالي', '', sub_total])

    for widget in inventories_tab.winfo_children():
        if isinstance(widget, Button):
            if widget['text'] == "الأصناف المباعة":
                widget['state'] = 'disabled'
            else:
                widget['state'] = 'normal'

sold_items_btn['command'] = sold_items

def daily_net():
    # Perform DB queries in background thread, prepare data, then update UI on main thread.
    sold_items = cr.execute(f"SELECT DISTINCT item_name FROM daily_log WHERE transaction_type = '{sell}'").fetchall()
    expense_names = cr.execute(f"SELECT DISTINCT item FROM daily_expenses").fetchall()

    total_sales_row = cr.execute(f"""SELECT SUM(total) FROM daily_log WHERE transaction_type = '{sell}'""").fetchone()
    total_expenses_row = cr.execute(f"""SELECT SUM(total) FROM daily_expenses""").fetchone()

    total_sales = total_sales_row[0] if total_sales_row and total_sales_row[0] is not None else 0
    total_expenses = total_expenses_row[0] if total_expenses_row and total_expenses_row[0] is not None else 0
    net = total_sales - total_expenses

    sold_rows = []
    for item in sold_items:
        item_name = item[0]
        total_price_row = cr.execute(f"""SELECT SUM(total) FROM daily_log WHERE item_name = '{item_name}' AND transaction_type = '{sell}'""").fetchone()
        total_price = total_price_row[0] if total_price_row and total_price_row[0] is not None else 0
        sold_rows.append([item_name, total_price])

    expense_rows = []
    for expense in expense_names:
        expense_name = expense[0]
        total_expense_row = cr.execute(f"""SELECT SUM(total) FROM daily_expenses WHERE item = '{expense_name}'""").fetchone()
        total_expense = total_expense_row[0] if total_expense_row and total_expense_row[0] is not None else 0
        expense_rows.append([expense_name, -total_expense])

    def update_ui():
        # clear all rows and columns using while loops to avoid index-shift/crash and reduce redraw calls
        while inventories_sheet.get_total_rows() > 0:
            inventories_sheet.delete_row(0, redraw=False)
        while inventories_sheet.get_total_columns() > 0:
            inventories_sheet.delete_column(0, redraw=False)
        # redraw once after bulk changes if available
        try:
            inventories_sheet.redraw()
        except Exception:
            pass

        inventories_sheet.set_header_data(['الصنف', 'الإجمالي'])

        for row in sold_rows:
            inventories_sheet.insert_row(row)

        inventories_sheet.insert_row(['------------------', '------------------'])

        for row in expense_rows:
            inventories_sheet.insert_row(row)

        inventories_sheet.insert_row(['------------------', '------------------'])
        inventories_sheet.insert_row(['صافي اليوم', net])

        for widget in inventories_tab.winfo_children():
            if isinstance(widget, Button):
                if widget['text'] == "صافي اليوم":
                    widget['state'] = 'disabled'
                else:
                    widget['state'] = 'normal'

    # schedule UI update on main thread
    root.after(0, update_ui)

daily_net_btn['command'] = lambda: run_in_thread(daily_net)()

# Expenses Tab in Admin Tab
expenses_mngmnt_frm = Frame(expenses_tab, bg="#2C61BD")
expenses_mngmnt_frm.grid(row=0, column=0, pady=10)

add_expense_btn = Button(expenses_mngmnt_frm, text="إضافة مصروف", font=("Arial", 14, "bold"), bg="#2C61BD", relief='sunken',
                        width=((screen_width//5)-30) , image=plus_img, compound='right', padx=5)
add_expense_btn.pack(padx=5)

delete_expense_btn = Button(expenses_mngmnt_frm, text="حذف مصروف", font=("Arial", 14, "bold"), bg="#2C61BD", relief='sunken',
                        width=((screen_width//5)-30) , image=cancel_img, compound='right', padx=5)
delete_expense_btn.pack(padx=5)

print_expenses_btn = Button(expenses_mngmnt_frm, text="طباعة المصروفات", font=("Arial", 14, "bold"), bg="#2C61BD", relief='sunken',
                        width=((screen_width//5)-30) , image=receipt_img, compound='right', padx=5)
print_expenses_btn.pack(padx=5)

adding_expense_frm = Frame(expenses_tab, bg="#2C61BD")
adding_expense_frm.grid(row=0, column=1, pady=5)

expense_name_lbl = Label(adding_expense_frm, text=":اسم المصروف", font=("Arial", 14, "bold"), bg="#2C61BD")
expense_name_lbl.grid(row=0, column=1, padx=5)

expense_name_ent = Entry(adding_expense_frm, font=("Arial", 14))
expense_name_ent.grid(row=0, column=0, padx=5)

expense_qty_lbl = Label(adding_expense_frm, text=": العدد", font=("Arial", 14, "bold"), bg="#2C61BD")
expense_qty_lbl.grid(row=0, column=3, padx=5)

expense_qty_ent = Entry(adding_expense_frm, font=("Arial", 14))
expense_qty_ent.grid(row=0, column=2, padx=5)

expense_price_lbl = Label(adding_expense_frm, text=": السعر", font=("Arial", 14, "bold"), bg="#2C61BD")
expense_price_lbl.grid(row=1, column=1, padx=5)

expense_price_ent = Entry(adding_expense_frm, font=("Arial", 14))
expense_price_ent.grid(row=1, column=0, padx=5)

importer_lbl = Label(adding_expense_frm, text=":المورد", font=("Arial", 14, "bold"), bg="#2C61BD")
importer_lbl.grid(row=1, column=3, padx=5)

importer_ent = Entry(adding_expense_frm, font=("Arial", 14))
importer_ent.grid(row=1, column=2, padx=5)

expenses_type_frm = Frame(adding_expense_frm, bg="#2C61BD")
expenses_type_frm.grid(row=0, column=4, rowspan=2, padx=20)

daily_expense_rbtn = Button(expenses_type_frm, text="مصروفات يومية", font=("Arial", 14, "bold"), bg="#2C61BD",
                            image=daily_inventory_img,compound='right', relief='sunken')
daily_expense_rbtn.grid(row=0, column=0, pady=5)

monthly_expense_rbtn = Button(expenses_type_frm, text="مصروفات شهرية", font=("Arial", 14, "bold"), bg="#2C61BD",
                            image=monthly_inventory_img,compound='right', relief='sunken')
monthly_expense_rbtn.grid(row=1, column=0, pady=5)

expense_sheet_frame = Frame(expenses_tab, bg="#2C61BD")
expense_sheet_frame.grid(row=1, column=0, columnspan=3, sticky='nsew')
expense_sheet = Sheet(expense_sheet_frame,
                        height=screen_height-10,
                        width=screen_width-10,
                        show_x_scrollbar=True,
                        show_y_scrollbar=True,
                        bg="#2C61BD",
                        header_bg="#3286c4",
                        header_fg="black",
                        even_bg="#d9d9d9",
                        odd_bg="white",
                        )
expense_sheet.enable_bindings(("single_select", "row_select", "column_select", "column_width_resize", "arrowkeys",
                                    "right_click_popup_menu", "rc_select", "copy"))
expense_sheet.pack(expand=1, fill="both") 


def daily_expenses():
    expenses = cr.execute("SELECT * FROM daily_expenses").fetchall()
    # Clearing previous data
    for i in range(expense_sheet.get_total_rows()):
        expense_sheet.delete_row(0, redraw=False)
    # removing old columns and setting new ones
    for i in range(expense_sheet.get_total_columns()):
        expense_sheet.delete_column(0, redraw=False)
    expense_sheet.set_header_data(['المورد', 'المصروف', 'السعر', 'الكمية', 'الاجمالي', 'الوقت'])
    for expense in expenses:
        expense_sheet.insert_row([expense[0], expense[1], expense[2], expense[3], expense[4], expense[5]])

# daily_expense_rbtn = lambda: run_in_thread(daily_expenses)()

def auto_expense_show():
    if admin_mngmnt_ntbk.tab(admin_mngmnt_ntbk.select(), "text") == "المصروفات":
        daily_expenses()

# admin_mngmnt_ntbk.bind('<<NotebookTabChanged>>', lambda event: run_in_thread(auto_expense_show)())

def ntbk_tab_change(event):
    if admin_mngmnt_ntbk.tab(admin_mngmnt_ntbk.select(), "text") == "تسجيل الخروج":
        logout_admin()
    elif admin_mngmnt_ntbk.tab(admin_mngmnt_ntbk.select(), "text") == "المصروفات":
        daily_expenses()
    elif admin_mngmnt_ntbk.tab(admin_mngmnt_ntbk.select(), "text") == "الجرد":
        daily_bills()

admin_mngmnt_ntbk.bind('<<NotebookTabChanged>>', ntbk_tab_change)

def monthly_expenses_lvl():
    top = Toplevel()
    top.title("مصروفات شهرية")
    top['bg'] = '#2C61BD'
    top.iconbitmap('meat.ico')
    # making root doesn't accept input until this window is closed
    top.grab_set()
    from_date_lbl = Label(top, text=":من تاريخ", font=("Arial", 12, 'bold'), bg='#2C61BD')
    from_date_lbl.grid(row=0, column=1, padx=10, pady=10)

    from_date_ent = DateEntry(top, font=("Arial", 12), date_pattern='dd-mm-yyyy')
    from_date_ent.grid(row=0, column=0, padx=10, pady=10)

    to_date_lbl = Label(top, text=":إلى تاريخ", font=("Arial", 12, 'bold'), bg='#2C61BD')
    to_date_lbl.grid(row=1, column=1, padx=10, pady=10)

    to_date_ent = DateEntry(top, font=("Arial", 12), date_pattern='dd-mm-yyyy')
    to_date_ent.grid(row=1, column=0, padx=10, pady=10)

    def dates_between_two_dates(start_date, end_date):
        delta = timedelta(days=1)
        dates = []
        while start_date <= end_date:
            dates.append(start_date.isoformat())
            start_date += delta
        
        return dates
    def show_monthly_expenses():
        from_date = from_date_ent.get()
        to_date = to_date_ent.get()
        if from_date > to_date:
            messagebox.showerror("خطأ", "تأكد من صحة التواريخ المدخلة")
            return
        if from_date == to_date or from_date_ent.get() == "" or to_date_ent.get() == "":
            messagebox.showerror("خطأ", "تأكد من إدخال التواريخ بشكل صحيح")
            return
        
        from_date = datetime.strptime(from_date, r"%d-%m-%Y").date()
        to_date =  datetime.strptime(to_date, r"%d-%m-%Y").date()

        dates_list = dates_between_two_dates(from_date, to_date)
        print(dates_list)

        # Clearing previous data
        for i in range(expense_sheet.get_total_rows()):
            expense_sheet.delete_row(0, redraw=False)
        # removing old columns and setting new ones
        for i in range(expense_sheet.get_total_columns()):
            expense_sheet.delete_column(0, redraw=False)
        expense_sheet.set_header_data(['المورد', 'المصروف', 'السعر', 'الكمية', 'الاجمالي', 'التاريخ', 'الوقت'])
        for date in dates_list:
            # reversing date str to match db format
            date = datetime.strptime(date, r"%Y-%m-%d").strftime(r"%d-%m-%Y")
            expenses = cr.execute(f"""SELECT * FROM expenses WHERE date = '{date}'""").fetchall()
            print(date)
            for expense in expenses:
                expense_sheet.insert_row([expense[0], expense[1], expense[2], expense[3], expense[4], expense[5], expense[6]])
        top.destroy()
    
    show_expenses_btn = Button(top, text="عرض المصروفات", font=("Arial", 12, "bold"), bg='#2C61BD', relief='sunken',
                              command=show_monthly_expenses)
    show_expenses_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

monthly_expense_rbtn['command'] = monthly_expenses_lvl

# monthly_inventory_expense_rbtn['command'] = monthly_expenses_lvl

def add_expense():
    expense = expense_name_ent.get()
    qty = expense_qty_ent.get()
    price = expense_price_ent.get()
    importer = importer_ent.get()
    # Validate inputs on the main thread
    if not (qty.isdigit() and price.isdigit() and expense != "" and importer != ""):
        messagebox.showerror("خطأ", "تأكد من إدخال جميع البيانات بشكل صحيح")
        return

    qty_int = int(qty)
    price_int = int(price)
    total = price_int * qty_int
    time_str = datetime.now().strftime(r"%I:%M %p")
    date_str = datetime.now().strftime(r"%d-%m-%Y")

    def db_task():
        try:
            # use parameterized queries to avoid injection and type issues
            cr.execute("""INSERT INTO daily_expenses (importer, item, price, amount, total, time) VALUES 
                       (?, ?, ?, ?, ?, ?)""", (importer, expense, price_int, qty_int, total, time_str))
            cr.execute("""INSERT INTO expenses (importer, item, price, amount, total, date, time) VALUES 
                        (?, ?, ?, ?, ?, ?, ?)""", (importer, expense, price_int, qty_int, total, date_str, time_str))
            db.commit()

            # schedule UI updates back on the main thread
            def on_success():
                expense_name_ent.delete(0, 'end')
                expense_qty_ent.delete(0, 'end')
                expense_price_ent.delete(0, 'end')
                importer_ent.delete(0, 'end')
                daily_expenses()
                messagebox.showinfo("نجاح", "تم اضافة المصروف بنجاح")
            root.after(0, on_success)
        except Exception as e:
            def on_error():
                messagebox.showerror("خطأ", f"حدث خطأ أثناء إضافة المصروف: {e}")
            root.after(0, on_error)

    # run only the DB work in a background thread
    run_in_thread(db_task)()

add_expense_btn['command'] = add_expense

def delete_expense():
    if messagebox.askyesno("تأكيد الحذف", "هل أنت متأكد من حذف المصروف"):
        cr.execute(f"""DELETE FROM daily_expenses""")
        db.commit()
        daily_expenses()

delete_expense_btn['command'] = lambda : run_in_thread(delete_expense)()

def print_expenses():
    pass  # Here you

print_expenses_btn['command'] = print_expenses


# Setting up db connection



# dividing cashier tab into sections


items_frame = Frame(cashier_tab, bg="#2C61BD", width=screen_width/2, height=screen_height/2)
items_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

items_ntbk = ttk.Notebook(items_frame, width=screen_width/2, height=screen_height/2)
items_ntbk.grid(row=0, column=0, sticky="nw")

items_btns_frame = Frame(items_frame, bg="#2C61BD")
items_btns_frame.grid(row=1, column=0)


return_btn = Button(items_btns_frame, text="إرجاع فتورة", font=("Arial", 18, "bold"), bg="#2C61BD", relief='sunken',
                    width=screen_width//4, image=return_img, compound='right', padx=5)
return_btn.grid(row=1, column=0, sticky="sw")

add_new_item_btn = Button(items_btns_frame, text="إضافة صنف جديد", font=("Arial", 18, "bold"), bg="#2C61BD", relief='sunken',
                        width=screen_width//4, image=add_img, compound='right', padx=5)
add_new_item_btn.grid(row=1, column=1, sticky="se")

print_bill_btn = Button(items_btns_frame, text="طباعة الفاتورة", font=("Arial", 18, "bold"), bg="#2C61BD", relief='sunken',
                        width=screen_width//4, image=receipt_img, compound='right', padx=5)
print_bill_btn.grid(row=2, column=1, sticky="se", pady=(0, 10))

del_order_btn = Button(items_btns_frame, text="حذف الفاتورة", font=("Arial", 18, "bold"), bg="#2C61BD", relief='sunken',
                        width=screen_width//4, image=cancel_img, compound='right', padx=5)
del_order_btn.grid(row=2, column=0, sticky="sw", pady=(0, 10))

total_lbl = Label(items_btns_frame, text=":الاجمالي", font=("Arial", 18, "bold"), bg="#2C61BD")
total_lbl.grid(row=3, column=1, padx=10, pady=10)

total_ent = Entry(items_btns_frame, font=("Arial", 18), state='disabled', width=20, justify='center')
total_ent.grid(row=3, column=0, padx=10, pady=10)

comments_lbl = Label(items_btns_frame, text=":ملاحظات", font=("Arial", 18, "bold"), bg="#2C61BD")
comments_lbl.grid(row=4, column=1, padx=10, pady=10)

comments_ent = Entry(items_btns_frame, font=("Arial", 18), width=20, justify='center')
comments_ent.grid(row=4, column=0, padx=10, pady=10)


# order editing buttons funcs

def return_bill_lvl():
    top = Toplevel()
    top.title("إرجاع فاتورة")
    top['bg'] = '#2C61BD'
    top.iconbitmap('meat.ico')

    # making root doesn't accept input until this window is closed
    top.grab_set()

    bill_num_lbl = Label(top, text=":رقم الفاتورة", font=("Arial", 12, 'bold'), bg='#2C61BD')
    bill_num_lbl.grid(row=0, column=1, padx=10, pady=10)

    bill_num_ent = Entry(top, font=("Arial", 12))
    bill_num_ent.grid(row=0, column=0, padx=10, pady=10)

    bill_state_lbl = Label(top, text=":حالة الفاتورة", font=("Arial", 12, 'bold'), bg='#2C61BD')
    bill_state_lbl.grid(row=1, column=1, padx=10, pady=10)

    bill_state_ent = Entry(top, font=("Arial", 12), state='disabled')
    bill_state_ent.grid(row=1, column=0, padx=10, pady=10)

    peek_bill_btn = Button(top, text="استعراض الفاتورة", font=("Arial", 12, "bold"), bg='#2C61BD', relief='sunken',
                          image=view_img, anchor='w', compound='right')
    peek_bill_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    bill_peek_tree = ttk.Treeview(top, show="headings", height=10)
    bill_peek_tree['columns'] = ("الاجمالي", "الكمية", "سعر الوحدة", "الصنف")

    bill_peek_tree.column("الاجمالي", anchor='center')
    bill_peek_tree.column("الكمية", anchor='center')
    bill_peek_tree.column("سعر الوحدة", anchor='center')
    bill_peek_tree.column("الصنف", anchor='center')

    bill_peek_tree.heading("الاجمالي", text="الاجمالي", anchor='center')
    bill_peek_tree.heading("الكمية", text="الكمية", anchor='center')
    bill_peek_tree.heading("سعر الوحدة", text="سعر الوحدة", anchor='center')
    bill_peek_tree.heading("الصنف", text="الصنف", anchor='center')

    bill_peek_tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    total_lbl = Label(top, text=":الاجمالي", font=("Arial", 12, 'bold'), bg='#2C61BD')
    total_lbl.grid(row=4, column=1, padx=10, pady=10)
    total_ent = Entry(top, font=("Arial", 12), state='disabled')
    total_ent.grid(row=4, column=0, padx=10, pady=10)

    return_bill_btn = Button(top, text="إرجاع الفاتورة", font=("Arial", 12, "bold"), bg='#2C61BD', relief='sunken',
                          image=return_one_img, anchor='w', compound='right')
    return_bill_btn.grid(row=5, column=0, padx=10, pady=10)

    reprint_bill_btn = Button(top, text="إعادة طباعة الفاتورة", font=("Arial", 12, "bold"), bg='#2C61BD', relief='sunken',
                          image=receipt_img, anchor='w', compound='right')
    reprint_bill_btn.grid(row=5, column=1, padx=10, pady=10)


    def peek_bill():
        bill_num = bill_num_ent.get()
        # Clearing previous bill peek data if exists
        for row in bill_peek_tree.get_children():
            bill_peek_tree.delete(row)
        # Checking if bill exists
        if bill_num.isdigit():
            bill_num = int(bill_num)
            bills_range = cr.execute("SELECT MAX(bill_num) FROM daily_log").fetchone()[0]
            if bill_num <= bills_range:
                bill_state = cr.execute(f"SELECT transaction_type FROM daily_log WHERE bill_num = {bill_num}").fetchone()[0]
                items = cr.execute(f"SELECT item_name, price, quantity, total FROM daily_log WHERE bill_num = {bill_num}").fetchall()
                # appending items to treeview
                for item in items:
                    bill_peek_tree.insert("", "end", values=(item[3], item[2], item[1], item[0]), )
                total_price = cr.execute(f"SELECT SUM(total) FROM daily_log WHERE bill_num = {bill_num}").fetchone()[0]

                total_ent.config(state='normal')
                total_ent.delete(0, 'end')
                total_ent.insert(0, str(total_price))
                total_ent.config(state='disabled')

                bill_state_ent.config(state='normal')
                bill_state_ent.delete(0, 'end')
                bill_state_ent.insert(0, bill_state)
                bill_state_ent.config(state='disabled')
    
    def reprint_bill():
        pass  # Here you can add the logic to reprint the bill

    def return_bill():
        if bill_state_ent.get() == sell:
            bill_num = bill_num_ent.get()
            cr.execute(f"""UPDATE daily_log SET transaction_type = '{returned}' WHERE bill_num = {bill_num}""")
            db.commit()
            messagebox.showinfo("نجاح", "تم ارجاع الفاتورة بنجاح")
            top.destroy()
        else:
            messagebox.showerror("خطأ", "تم ارجاع هذه الفاتورة من قبل")

    peek_bill_btn['command'] = peek_bill
    reprint_bill_btn['command'] = reprint_bill
    return_bill_btn['command'] = return_bill

return_btn['command'] = return_bill_lvl

def add_new_item_lvl():
    top = Toplevel()
    top.title("إضافة صنف جديد")
    top['bg'] = '#2C61BD'
    top.grab_set()
    category_name_lbl = Label(top, text=":اسم القسم", font=("Arial", 12, 'bold'), bg='#2C61BD')
    category_name_lbl.grid(row=0, column=1, padx=10, pady=10)

    category_names = []

    for cat in cr.execute("SELECT name FROM sqlite_master WHERE type='table'"):
        if cat[0] not in ["info", "log", "daily_log", "expenses", "basket"]:
            category_names.append(cat[0])
    

    category_name_ttk_menu_var = StringVar()
    category_name_ttk_menu = ttk.OptionMenu(top, category_name_ttk_menu_var, 'اختر القسم', *category_names, style='TMenubutton')
    category_name_ttk_menu.grid(row=0, column=0, padx=10, pady=10)


    item_name_lbl = Label(top, text=":اسم الصنف", font=("Arial", 12, 'bold'), bg='#2C61BD')
    item_name_lbl.grid(row=1, column=1, padx=10, pady=10)

    item_ent = Entry(top, font=("Arial", 12))
    item_ent.grid(row=1, column=0, padx=10, pady=10)

    price_lbl = Label(top, text=":السعر", font=("Arial", 12, 'bold'), bg='#2C61BD')
    price_lbl.grid(row=2, column=1, padx=10, pady=10)

    price_ent = Entry(top, font=("Arial", 12))
    price_ent.grid(row=2, column=0, padx=10, pady=10)

    add_item_btn = Button(top, text="إضافة الصنف", font=("Arial", 12, "bold"), bg='#2C61BD', image=plus_img, anchor='w',
                            compound='right', relief='sunken')
    add_item_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def add_item_to_db():
        cat_name = category_name_ttk_menu_var.get()
        item_name = item_ent.get()
        item_price = price_ent.get()
        if item_price.isdigit() and cat_name in category_names and item_name != "":
            item_price = int(item_price)
            cr.execute(f"""INSERT INTO '{cat_name}' (item, price, row, column) VALUES ('{item_name}', {item_price}, 0, 0)""")
            db.commit()
            update_item_buttons_layout_db()
            for widget in categories_tabs[cat_name].frame.winfo_children():
                widget.destroy()
            items = cr.execute(f"SELECT * FROM '{cat_name}'").fetchall()
            for item in items:
                ItemButton(item[0], item[1], item[2], item[3], categories_tabs[cat_name].frame, cat_name)
            messagebox.showinfo("نجاح", f"تم اضافة الصنف {item_name} بنجاح")
            top.destroy()
        else:
            messagebox.showerror("خطأ", "برجاء ادخال بيانات صحيحة")
    

    add_item_btn['command'] = lambda: run_in_thread(add_item_to_db)()

add_new_item_btn['command'] = add_new_item_lvl

def print_bill():
    cr.execute("SELECT * FROM basket WHERE temp = 0")
    items = cr.fetchall()
    if items:

        last_bill_num = cr.execute("SELECT MAX(bill_num) FROM daily_log").fetchone()[0]
        if last_bill_num is None:
            bill_num = 1
        else:
            bill_num = last_bill_num + 1

        now = datetime.now()
        time_str = now.strftime("%I:%M %p")
        date_str = now.strftime("%d-%m-%Y")
        for item in items:
            cr.execute(f"""INSERT INTO daily_log (bill_Num, transaction_type, item_name, quantity, price, total, time) VALUES
                            ({bill_num}, '{sell}', '{item[0]}', {item[2]}, {item[1]}, {item[5]}, '{time_str}')""")
            cr.execute(f"""INSERT INTO log (bill_Num, transaction_type, item_name, quantity, price, total, time, date) VALUES
                            ({bill_num}, '{sell}', '{item[0]}', {item[2]}, {item[1]}, {item[5]}, '{time_str}', '{date_str}')""")

        cr.execute("DELETE FROM basket")
        db.commit()
        run_in_thread(refresh_treeview)()
        total_ent['state'] = 'normal'
        total_ent.delete(0, 'end')
        total_ent['state'] = 'disabled'
        comments_ent.delete(0, 'end')
    # Here you can add the logic to print the bill

print_bill_btn['command'] = print_bill

def del_order():
    if messagebox.askyesno("تأكيد", "هل أنت متأكد من حذف الفاتورة الحالية؟") and basket_tree.get_children():
        cr.execute("DELETE FROM basket")
        db.commit()
        run_in_thread(refresh_treeview)()
    else:
        messagebox.showinfo("تنبيه", "لا توجد فاتورة لحذفها")

del_order_btn['command'] = del_order

# Creating Tabs Obejcts for each category
cr.execute("SELECT name FROM sqlite_master WHERE type='table'")
categories = cr.fetchall()
category_names = [cat[0] for cat in categories if cat[0] not in ["info", "log", "daily_log", "expenses", "basket", "daily_expenses"]]


class CategoriesTabs:
    def __init__(self, tab_name, frame=None):
        self.tab_name = tab_name
        self.frame = frame
        self.frame = Frame(items_ntbk, bg="#2C61BD")
        items_ntbk.add(self.frame, text=tab_name)


categories_tabs = {}
for cat_name in category_names:
    categories_tabs[cat_name] = CategoriesTabs(cat_name)


# Creating Treeview for basket items
basket_frame = Frame(cashier_tab, bg="#2C61BD", height=(screen_height/2), width=(screen_width/2))
# cashier_tab.columnconfigure(1, weight=1)
basket_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

basket_tree = ttk.Treeview(basket_frame, show="headings", height=15, yscrollcommand=True,)
basket_tree['columns'] = ("الاجمالي", "الكمية", "سعر الوحدة", "الصنف")

basket_tree.column("الاجمالي", width=(screen_width//8), anchor='center')
basket_tree.column("الكمية", width=(screen_width//8), anchor='center')
basket_tree.column("سعر الوحدة", width=(screen_width//8), anchor='center')
basket_tree.column("الصنف", width=(screen_width//8), anchor='center')

basket_tree.heading("الاجمالي", text="الاجمالي", anchor='center')
basket_tree.heading("الكمية", text="الكمية", anchor='center')
basket_tree.heading("سعر الوحدة", text="سعر الوحدة", anchor='center')
basket_tree.heading("الصنف", text="الصنف", anchor='center')
basket_tree.grid(row=0, column=1, sticky='nw', padx=10, pady=10)

edit_basket_frm = Frame(basket_frame, bg="#2C61BD")
edit_basket_frm.grid(row=1, column=1,pady=10)

add_temp_item_btn = Button(edit_basket_frm, text="اضافة صنف مؤقت", font=("Arial", 12, "bold"), 
                            relief='sunken', bg='#2C61BD', image=plus_img, anchor='w', compound='right')
add_temp_item_btn.grid(row=0, column=0, padx=5, pady=5)

del_item_btn = Button(edit_basket_frm, text="حذف صنف", font=("Arial", 12, "bold"),  relief='sunken',
                       bg='#2C61BD', image=cancel_img, anchor='w', compound='right')
del_item_btn.grid(row=0, column=1, padx=5, pady=5)

## Editing Basket Items funcs##
# Editing item on double click

def edit_item_top(event):
    if basket_tree.selection() != ():
        top = Toplevel()
        top.iconbitmap('meat.ico')
        top.grab_set()
        top.title(f"تعديل الصنف  {basket_tree.item(basket_tree.selection())['values'][3]}")
        top.geometry("600x600")
        top['bg'] = '#2C61BD'

        ent = Entry(top, font=("Arial", 14), justify='center', state='disabled')
        ent.pack(pady=20, anchor='center')

        nums_frame = Frame(top, bg='#2C61BD')
        nums_frame.pack(pady=10)

        edit_frm = Frame(top, bg='#2C61BD')
        edit_frm.pack(pady=10)


        def insert_num(e, num):
            ent.config(state='normal')
            ent.insert('end', str(num))
            ent.config(state='disabled')
        
        def clear_ent(e):
            ent.config(state='normal')
            ent.delete(0, 'end')
            ent.config(state='disabled')
        
        def backspace_ent(e):
            current_text = ent.get()
            ent.config(state='normal')
            ent.delete(len(current_text)-1, 'end')
            ent.config(state='disabled')
        
        # Creating number buttons and loading images with PIL for better performance
        row = 0
        col = 0

        for i in range(1, 10):
            btn = Button(nums_frame, image=nums[i], bg='#2C61BD', relief='sunken', font=("Arial", 18, "bold"),
                        command=lambda n=i: insert_num(None, n), compound='center')
            btn.grid(row=row, column=col, padx=5, pady=5)
            
            col += 1
            if col == 3:  # Reset after 3 columns for a 3x3 grid
                row += 1
                col = 0
        zero_btn = Button(nums_frame, image=nums[0], bg='#2C61BD', relief='sunken', font=("Arial", 18, "bold"),
                         command=lambda n=i: insert_num(None, 0), pady=5)
        zero_btn.grid(row=3, column=1, padx=5, pady=5)


        clear_btn = Button(nums_frame, text='C', font=("Arial", 22, "bold"), bg='#2C61BD', relief='sunken',
                           command=lambda: clear_ent(None), pady=5)
        clear_btn.grid(row=3, column=0, padx=5, pady=5)

        backspace_btn = Button(nums_frame,  font=("Arial", 20, "bold"), bg='#2C61BD', relief='sunken',
                                command=lambda: backspace_ent(None), text='⌫')
        backspace_btn.grid(row=3, column=2, padx=5, pady=5)

        def edit_qty():
            new_qty = ent.get()
            if new_qty.isdigit():
                new_qty = int(new_qty)/1000  # converting to proper qty
                selected_item = basket_tree.item(basket_tree.selection())['values'][3]
                cr.execute(f"""UPDATE basket SET qty = {new_qty}, total = (unit_price * {new_qty}) WHERE item = '{selected_item}'""")
                db.commit()
                run_in_thread(refresh_treeview)()
                top.destroy()
            else:
                messagebox.showerror("خطأ", "برجاء ادخال كمية صحيحة")

        def edit_price():
            price = ent.get()
            if price.isdigit():
                new_price = int(price)
                selected_item = basket_tree.item(basket_tree.selection())['values'][3]
                unit_price = cr.execute(f"SELECT unit_price FROM basket WHERE item = '{selected_item}'").fetchone()[0]
                new_qty = round((new_price / unit_price), 3)
                cr.execute(f"""UPDATE basket SET total = {new_price}, qty = {new_qty} WHERE item = '{selected_item}'""")
                db.commit()
                run_in_thread(refresh_treeview)()
                top.destroy()
            else:
                messagebox.showerror("خطأ", "برجاء ادخال سعر صحيح")


        edit_qty_btn = Button(edit_frm, text="تعديل الكمية", font=("Arial", 12, "bold"), bg='#2C61BD', relief='sunken',
                               image=gear_img, compound='left',  command=edit_qty)
        edit_qty_btn.grid(row=0, column=0, pady=10, padx=10)

        edit_price_btn = Button(edit_frm, text="تعديل السعر", font=("Arial", 12, "bold"), bg='#2C61BD', relief='sunken',
                                image=price_img, compound='left', command=edit_price)  
        edit_price_btn.grid(row=0, column=1, pady=10, padx=10)


def del_item():
    if basket_tree.selection():
        selected_item = basket_tree.item(basket_tree.selection())['values'][3]
        cr.execute(f"DELETE FROM basket WHERE item = '{selected_item}'")
        db.commit()
        run_in_thread(refresh_treeview)()
    else:
        # selecting last item to delete
        selected_item = basket_tree.get_children()[-1]
        selected_item_name = basket_tree.item(selected_item)['values'][3]
        cr.execute(f"DELETE FROM basket WHERE item = '{selected_item_name}'")
        db.commit()
        run_in_thread(refresh_treeview)()

del_item_btn['command'] = del_item

def add_temp_item_lvl():
    top = Toplevel()
    top.iconbitmap('meat.ico')
    top.title("اضافة صنف مؤقت")
    top.geometry("400x300")
    top['bg'] = '#2C61BD'
    top.grab_set()

    name_lbl = Label(top, text=":اسم الصنف", font=("Arial", 12, 'bold'), bg='#2C61BD')
    name_lbl.grid(row=0, column=1, padx=10, pady=10)
    name_ent = Entry(top, font=("Arial", 12))
    name_ent.grid(row=0, column=0, padx=10, pady=10)

    price_lbl = Label(top, text=":سعر الوحدة", font=("Arial", 12, 'bold'), bg='#2C61BD')
    price_lbl.grid(row=1, column=1, padx=10, pady=10)
    price_ent = Entry(top, font=("Arial", 12))
    price_ent.grid(row=1, column=0, padx=10, pady=10)

    qty_lbl = Label(top, text=":الكمية", font=("Arial", 12, 'bold'), bg='#2C61BD')
    qty_lbl.grid(row=2, column=1, padx=10, pady=10)
    qty_ent = Entry(top, font=("Arial", 12))
    qty_ent.grid(row=2, column=0, padx=10, pady=10)

    add_item_btn = Button(top, text="اضافة الصنف", font=("Arial", 12, "bold"), bg='#2C61BD', image=plus_img, anchor='w', compound='right', relief='sunken')
    add_item_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def add_temp_item_to_basket():
        item_name = name_ent.get()
        item_price = float(price_ent.get())
        item_qty = int(qty_ent.get())
        total_price = item_price * item_qty

        cr.execute(f"""INSERT INTO basket (item, unit_price, qty, category, temp, total) VALUES ('{item_name}',
                        {item_price}, {item_qty}, 'مؤقت', 1, {total_price})""")
        db.commit()
        run_in_thread(refresh_treeview)()
        top.destroy()

    add_item_btn['command'] = add_temp_item_to_basket


add_temp_item_btn['command'] = add_temp_item_lvl


basket_tree.bind('<Double-1>', edit_item_top)

def refresh_treeview():
    for row in basket_tree.get_children():
        basket_tree.delete(row)
    cr.execute("SELECT item, unit_price, qty, total FROM basket")
    rows = cr.fetchall()
    for row in rows:
        basket_tree.insert("", "end", values=(row[3], row[2], row[1], row[0]), )
    # updating total entry
    total = cr.execute("SELECT SUM(total) FROM basket").fetchone()[0]
    if total is None:
        total = 0
    total_ent['state'] = 'normal'
    total_ent.delete(0, 'end')
    total_ent.insert(0, str(total))
    total_ent['state'] = 'disabled'


# determining number of columns for item buttons
def get_num_of_columns():
    btn_width = screen_width//160 + 10  # button width + padding
    num_of_columns = screen_width/10 // btn_width
    return num_of_columns - 1  # subtracting 1 for better fit


def update_item_buttons_layout_db():
    num_of_columns = get_num_of_columns()
    for category in category_names:
        row = 0
        col = 0
        items = cr.execute(f"SELECT DISTINCT item FROM '{category}'").fetchall()
        for item in items:
            cr.execute(f"""UPDATE '{category}' SET row = {row}, column = {col} WHERE item = '{item[0]}'""")
            col += 1
            if col >= num_of_columns:
                col = 0
                row += 1
    db.commit()

update_item_buttons_layout_db()


cashier_mngmnt_frm_login = Frame(basket_frame, bg="#2C61BD", height=screen_height/2-20)
cashier_mngmnt_frm_login.grid(row=2, column=1, pady=10)

cashier_mngmnt_ent = Entry(cashier_mngmnt_frm_login, font=("Arial", 12), show='*', width=20)
cashier_mngmnt_ent.grid(row=0, column=0, padx=5, pady=5,sticky='s')

cashier_mngmnt_login_btn = Button(cashier_mngmnt_frm_login, text="تسجيل الدخول", font=("Arial", 12, "bold"),
                            bg='#2C61BD', relief='sunken', image=login_img, anchor='w', compound='right')
cashier_mngmnt_login_btn.grid(row=1, column=0, padx=5, pady=5,sticky='s')

cashier_mngmnt_frm = Frame(basket_frame, bg="#2C61BD")

edit_internal_price_btn = Button(cashier_mngmnt_frm, text="تعديل الاسعار", font=("Arial", 12, "bold"),
                            bg='#2C61BD', relief='sunken', image=gears_img, anchor='w', compound='right')
edit_internal_price_btn.grid(row=0, column=0, padx=5, pady=5,sticky='s')

remove_item_btn = Button(cashier_mngmnt_frm, text="حذف صنف", font=("Arial", 12, "bold"),
                            bg='#2C61BD', relief='sunken', image=cancel_img, anchor='w', compound='right')
remove_item_btn.grid(row=0, column=1, padx=5, pady=5,sticky='s')

change_passwd_btn = Button(cashier_mngmnt_frm, text="تغيير كلمة المرور", font=("Arial", 12, "bold"), bg='#2C61BD', relief='sunken',
                           image=passwd_img, anchor='w', compound='right')
change_passwd_btn.grid(row=1, column=0, padx=5, pady=5,sticky='s')

add_new_category_btn = Button(cashier_mngmnt_frm, text="اضافة قسم جديد", font=("Arial", 12, "bold"), bg='#2C61BD', relief='sunken',
                           image=add_img, anchor='w', compound='right')
add_new_category_btn.grid(row=1, column=1, padx=5, pady=5,sticky='s')

delete_category_btn = Button(cashier_mngmnt_frm, text="حذف قسم", font=("Arial", 12, "bold"), bg='#2C61BD', relief='sunken',
                           image=cancel_img, anchor='w', compound='right')
delete_category_btn.grid(row=2, column=1, padx=5, pady=5,sticky='s')

cashier_logout_btn = Button(cashier_mngmnt_frm, text="تسجيل خروج", font=("Arial", 12, "bold"), bg='#2C61BD', relief='sunken',
                           image=logout_img, anchor='w', compound='right')
cashier_logout_btn.grid(row=2, column=0, padx=5, pady=5,sticky='s')



def cashier_mngmnt_login(_=None):
    password = sha256(cashier_mngmnt_ent.get().encode()).hexdigest()
    cr.execute("SELECT passwd FROM info")
    correct_passwd = cr.fetchone()[0]
    if password == correct_passwd:
        cashier_mngmnt_frm_login.grid_forget()
        cashier_mngmnt_frm.grid(row=2, column=1, pady=10)

    else:
        messagebox.showerror("خطأ", "كلمة المرور غير صحيحة")

cashier_mngmnt_login_btn['command'] = cashier_mngmnt_login
cashier_mngmnt_ent.bind('<Return>', cashier_mngmnt_login)

def add_new_category_lvl():
    top = Toplevel()
    top.iconbitmap('meat.ico')
    top.title("اضافة قسم جديد")
    top['bg'] = '#2C61BD'
    top.grab_set()

    frm = Frame(top, bg='#2C61BD')
    frm.pack(fill='both', expand=1)


    name_lbl = Label(frm, text=":اسم القسم", font=("Arial", 12, 'bold'), bg='#2C61BD')
    name_lbl.grid(row=0, column=1, padx=10, pady=10)
    name_ent = Entry(frm, font=("Arial", 12))
    name_ent.grid(row=0, column=0, padx=10, pady=10)
    add_cat_btn = Button(frm, text="اضافة القسم", font=("Arial", 12, "bold"), bg='#2C61BD', image=plus_img,
                        anchor='w', compound='right', relief='sunken')
    add_cat_btn.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    def add_category():
        cat_name = name_ent.get()
        if cat_name != "":
            cr.execute(f"""CREATE TABLE IF NOT EXISTS '{cat_name}' (
                            item TEXT,
                            price REAL,
                            row INTEGER,
                            column INTEGER
                        )""")
            db.commit()
            categories_tabs[cat_name] = CategoriesTabs(cat_name)
            update_item_buttons_layout_db()
            messagebox.showinfo("نجاح", f"تم اضافة القسم {cat_name} بنجاح")
            top.destroy()
        else:
            messagebox.showerror("خطأ", "برجاء ادخال اسم القسم")
    add_cat_btn['command'] = add_category

add_new_category_btn['command'] = add_new_category_lvl

def edit_internal_prices_lvl():
    top = Toplevel()
    top.iconbitmap('meat.ico')
    top.title("تعديل الاسعار")
    top['bg'] = '#2C61BD'
    top.grab_set()

    category_name_lbl = Label(top, text=":اسم القسم", font=("Arial", 12, 'bold'), bg='#2C61BD')
    category_name_lbl.grid(row=0, column=1, padx=10, pady=10)

    def load_items_in_category(_event=None):
        category = category_name_ttk_menu_var.get()
        items = cr.execute(f"SELECT DISTINCT item FROM '{category}'").fetchall()
        item_names = [item[0] for item in items]
        item_name_ttk_menu.set_menu('اختر الصنف', *item_names)


    category_names = []

    for cat in cr.execute("SELECT name FROM sqlite_master WHERE type='table'"):
        if cat[0] not in ["info", "log", "daily_log", "expenses", "basket", "daily_expenses"]:
            category_names.append(cat[0])
    
    category_name_ttk_menu_var = StringVar()
    category_name_ttk_menu = ttk.OptionMenu(top, category_name_ttk_menu_var, 'اختر القسم', *category_names, style='TMenubutton', command=load_items_in_category)
    category_name_ttk_menu.grid(row=0, column=0, padx=10, pady=10)


    item_name_lbl = Label(top, text=":اسم الصنف", font=("Arial", 12, 'bold'), bg='#2C61BD')
    item_name_lbl.grid(row=1, column=1, padx=10, pady=10)

    item_name_ttk_menu_var = StringVar()
    item_name_ttk_menu = ttk.OptionMenu(top, item_name_ttk_menu_var, '')
    item_name_ttk_menu.grid(row=1, column=0, padx=10, pady=10)


    new_price_lbl = Label(top, text=":السعر الجديد", font=("Arial", 12, 'bold'), bg='#2C61BD')
    new_price_lbl.grid(row=2, column=1, padx=10, pady=10)

    new_price_ent = Entry(top, font=("Arial", 12))
    new_price_ent.grid(row=2, column=0, padx=10, pady=10)

    edit_price_btn = Button(top, text="تعديل السعر", font=("Arial", 12, "bold"), bg='#2C61BD', image=gear_img,
                            anchor='w', compound='right', relief='sunken')
    edit_price_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def edit_price():
        selected_cat = category_name_ttk_menu_var.get()
        selected_item = item_name_ttk_menu_var.get()
        new_price = new_price_ent.get()
        if new_price.isdigit() and selected_cat != 'اختر القسم' and selected_item != 'اختر الصنف':
            new_price = float(new_price)
            cr.execute(f"""UPDATE '{selected_cat}' SET price = {new_price} WHERE item = '{selected_item}'""")
            db.commit()
            messagebox.showinfo("نجاح", f"تم تعديل سعر الصنف {selected_item} بنجاح")
            # Updating item buttons
            for widget in categories_tabs[selected_cat].frame.winfo_children():
                widget.destroy()
            items = cr.execute(f"SELECT * FROM '{selected_cat}'").fetchall()
            for item in items:
                ItemButton(item[0], item[1], item[2], item[3], categories_tabs[selected_cat].frame, selected_cat)

        else:
            messagebox.showerror("خطأ", "برجاء ادخال سعر صحيح")
    edit_price_btn['command'] = lambda:run_in_thread(edit_price)()

edit_internal_price_btn['command'] = edit_internal_prices_lvl

def remove_item_lvl():
    top = Toplevel()
    top.iconbitmap('meat.ico')
    top.title()
    top['bg'] = '#2C61BD'
    top.grab_set()

    category_name_lbl = Label(top, text=":اسم القسم", font=("Arial", 12, 'bold'), bg='#2C61BD')
    category_name_lbl.grid(row=0, column=1, padx=10, pady=10)

    def load_items_in_category(_event=None):
        category = category_name_ttk_menu_var.get()
        items = cr.execute(f"SELECT DISTINCT item FROM '{category}'").fetchall()
        item_names = [item[0] for item in items]
        item_name_ttk_menu.set_menu('اختر الصنف', *item_names)

    category_names = []

    for cat in cr.execute("SELECT name FROM sqlite_master WHERE type='table'"):
        if cat[0] not in ["info", "log", "daily_log", "expenses", "basket"]:
            category_names.append(cat[0])
    

    category_name_ttk_menu_var = StringVar()
    category_name_ttk_menu = ttk.OptionMenu(top, category_name_ttk_menu_var, 'اختر القسم', *category_names, style='TMenubutton', command=load_items_in_category)
    category_name_ttk_menu.grid(row=0, column=0, padx=10, pady=10)


    item_name_lbl = Label(top, text=":اسم الصنف", font=("Arial", 12, 'bold'), bg='#2C61BD')
    item_name_lbl.grid(row=1, column=1, padx=10, pady=10)

    item_name_ttk_menu_var = StringVar()
    item_name_ttk_menu = ttk.OptionMenu(top, item_name_ttk_menu_var, '')
    item_name_ttk_menu.grid(row=1, column=0, padx=10, pady=10)

    remove_item_btn = Button(top, text="حذف الصنف", font=("Arial", 12, "bold"), bg='#2C61BD', image=cancel_img,
                            anchor='w', compound='right', relief='sunken')
    remove_item_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def remove_item():
        selected_cat = category_name_ttk_menu_var.get()
        selected_item = item_name_ttk_menu_var.get()
        if selected_cat != 'اختر القسم' and selected_item != 'اختر الصنف':
            cr.execute(f"""DELETE FROM '{selected_cat}' WHERE item = '{selected_item}'""")
            db.commit()
            messagebox.showinfo("نجاح", f"تم حذف الصنف {selected_item} بنجاح")
            # Updating category items positions in db
            update_item_buttons_layout_db()
            # Updating item buttons
            for widget in categories_tabs[selected_cat].frame.winfo_children():
                widget.destroy()
            items = cr.execute(f"SELECT * FROM '{selected_cat}'").fetchall()
            for item in items:
                ItemButton(item[0], item[1], item[2], item[3], categories_tabs[selected_cat].frame, selected_cat)
            messagebox.showinfo("نجاح", f"تم حذف الصنف {selected_item} بنجاح")
            top.destroy()
        else:
            messagebox.showerror("خطأ", "برجاء اختيار القسم والصنف")

    remove_item_btn['command'] = lambda:run_in_thread(remove_item)()

remove_item_btn['command'] = remove_item_lvl

def delete_category_lvl():
    top = Toplevel()
    top.iconbitmap('meat.ico')
    top.title("حذف قسم")
    top['bg'] = '#2C61BD'
    top.grab_set()

    category_name_lbl = Label(top, text=":اسم القسم", font=("Arial", 12, 'bold'), bg='#2C61BD')
    category_name_lbl.grid(row=0, column=1, padx=10, pady=10)

    category_names = []

    for cat in cr.execute("SELECT name FROM sqlite_master WHERE type='table'"):
        if cat[0] not in ["info", "log", "daily_log", "expenses", "basket"]:
            category_names.append(cat[0])
    

    category_name_ttk_menu_var = StringVar()
    category_name_ttk_menu = ttk.OptionMenu(top, category_name_ttk_menu_var, 'اختر القسم', *category_names, style='TMenubutton')
    category_name_ttk_menu.grid(row=0, column=0, padx=10, pady=10)

    delete_cat_btn = Button(top, text="حذف القسم", font=("Arial", 12, "bold"), bg='#2C61BD', image=cancel_img,
                            anchor='w', compound='right', relief='sunken')
    delete_cat_btn.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def delete_category():
        cat_name = category_name_ttk_menu_var.get()
        if cat_name != 'اختر القسم':
            cr.execute(f"""DROP TABLE IF EXISTS '{cat_name}'""")
            db.commit()
            # Removing tab from notebook
            tab_id = items_ntbk.index(categories_tabs[cat_name].frame)
            items_ntbk.forget(tab_id)
            messagebox.showinfo("نجاح", f"تم حذف القسم {cat_name} بنجاح")
            top.destroy()
        else:
            messagebox.showerror("خطأ", "برجاء اختيار القسم")
    delete_cat_btn['command'] = lambda:run_in_thread(delete_category)()

delete_category_btn['command'] = delete_category_lvl

def change_passwd_lvl():
    top = Toplevel()
    top.iconbitmap('meat.ico')
    top.title("تغيير كلمة المرور")
    top['bg'] = '#2C61BD'
    top.grab_set()

    old_passwd_lbl = Label(top, text=":كلمة المرور القديمة", font=("Arial", 12, 'bold'), bg='#2C61BD')
    old_passwd_lbl.grid(row=0, column=1, padx=10, pady=10)

    old_passwd_ent = Entry(top, font=("Arial", 12), show='*')
    old_passwd_ent.grid(row=0, column=0, padx=10, pady=10)

    new_passwd_lbl = Label(top, text=":كلمة المرور الجديدة", font=("Arial", 12, 'bold'), bg='#2C61BD')
    new_passwd_lbl.grid(row=1, column=1, padx=10, pady=10)

    new_passwd_ent = Entry(top, font=("Arial", 12), show='*')
    new_passwd_ent.grid(row=1, column=0, padx=10, pady=10)

    change_passwd_btn = Button(top, text="تغيير كلمة المرور", font=("Arial", 12, "bold"), bg='#2C61BD', image=passwd_img,
                            anchor='w', compound='right', relief='sunken')
    change_passwd_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def change_passwd():
        old_passwd = sha256(old_passwd_ent.get().encode()).hexdigest()
        new_passwd = new_passwd_ent.get()
        cr.execute("SELECT passwd FROM info")
        correct_passwd = cr.fetchone()[0]
        if old_passwd == correct_passwd and new_passwd != "":
            new_passwd_hashed = sha256(new_passwd.encode()).hexdigest()
            cr.execute(f"""UPDATE info SET passwd = '{new_passwd_hashed}'""")
            db.commit()
            messagebox.showinfo("نجاح", "تم تغيير كلمة المرور بنجاح")
            top.destroy()
        else:
            messagebox.showerror("خطأ", "كلمة المرور القديمة غير صحيحة أو كلمة المرور الجديدة فارغة")
    change_passwd_btn['command'] = lambda:run_in_thread(change_passwd)()

change_passwd_btn['command'] = change_passwd_lvl

def cashier_mngmnt_logout():
    cashier_mngmnt_frm.grid_forget()
    cashier_mngmnt_frm_login.grid(row=2, column=1, pady=10)
    cashier_mngmnt_ent.delete(0, 'end')

cashier_logout_btn['command'] = cashier_mngmnt_logout

# Creating Item Buttons

class ItemButton:
    def __init__(self, item_name, item_price, row, column, master, category):
        self.item_name = item_name
        self.item_price = item_price
        self.row = row
        self.column = column
        self.master = master
        self.category = category

        self.btn = Button(master, text=f"{self.item_name}\n{self.item_price} ج.م", font=("Arial", 12), width=screen_width//140,)
        self.btn.grid(row=self.row, column=self.column, padx=5, pady=5)
        self.btn['command'] = self.add_to_basket

    def add_to_basket(self):
        print(f"Adding {self.item_name} to basket")
        # Here you can add the logic to add the item to the basket
        distinct_items = cr.execute("SELECT DISTINCT item FROM basket").fetchall()
        distinct_items = [item[0] for item in distinct_items]
        if self.item_name in distinct_items:
            old_qty = cr.execute(f"SELECT qty FROM basket WHERE item = '{self.item_name}'").fetchone()[0]
            cr.execute(f"""UPDATE basket SET qty = (qty + 1), total = (unit_price * {old_qty+1}) WHERE item = '{self.item_name}'""")
        else:
            cr.execute(f"""INSERT INTO basket (item, unit_price, qty, category, temp, total) VALUES ('{self.item_name}',
                            {self.item_price}, 1, '{self.category}', 0, {self.item_price})""")
        db.commit()
        run_in_thread(refresh_treeview)()

# Populating Item Buttons in their respective category tabs
for cat_name, cat_tab in categories_tabs.items():
    cr.execute(f"SELECT * FROM '{cat_name}'")
    items = cr.fetchall()
    for item in items:
        ItemButton(item[0], item[1], item[2], item[3], cat_tab.frame, cat_name)

def is_day_over():
    today_date = datetime.now().strftime("%d-%m-%Y")
    dates = cr.execute("SELECT DISTINCT date FROM log").fetchall()
    dates = [date[0] for date in dates]
    if today_date not in dates :
        return True
    else:
        return False

# running app startup essentials functions
def startup_funcs():
    if is_day_over():
        cr.execute("DELETE FROM daily_log")
        db.commit()
    cr.execute("DELETE FROM basket")
    db.commit()
    refresh_treeview()


run_in_thread(startup_funcs)()


# Checking Copyright
device_id = os.popen('wmic csproduct get uuid').read().replace("UUID", "").strip()
cr.execute("SELECT device_id FROM info")
permited_id = cr.fetchone()[0]

if sha256(device_id.encode()).hexdigest() != permited_id:
    messagebox.showerror("Error", "This device is not authorized to run this application.")
    exit()
else:
    root.mainloop()
