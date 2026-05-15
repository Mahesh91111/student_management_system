import tkinter as tk
from tkinter import ttk, messagebox
import pymysql


class CarRental:

    def __init__(self, root):
        self.root = root
        self.root.title("Car Rental Management System")
        self.root.geometry("1400x800")
        self.root.config(bg="#0f172a")

        title = tk.Label(
            self.root,
            text="CAR RENTAL MANAGEMENT SYSTEM",
            bg="#1e293b",
            fg="white",
            font=("Segoe UI", 28, "bold"),
            pady=15
        )
        title.pack(fill="x")



        dashboard = tk.Frame(self.root, bg="#0f172a")
        dashboard.pack(fill="x", pady=10)

        self.totalCarsCard = self.create_card(dashboard, "Total Cars", 0)
        self.availableCard = self.create_card(dashboard, "Available", 1)
        self.reservedCard = self.create_card(dashboard, "Reserved", 2)


        mainFrame = tk.Frame(self.root, bg="#0f172a")
        mainFrame.pack(fill="both", expand=True, padx=20, pady=10)



        leftFrame = tk.Frame(mainFrame, bg="#1e293b", bd=2, relief="ridge")
        leftFrame.pack(side="left", fill="y", padx=10)

        heading = tk.Label(
            leftFrame,
            text="Operations",
            bg="#1e293b",
            fg="white",
            font=("Segoe UI", 18, "bold")
        )
        heading.pack(pady=20)

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TButton",
            font=("Segoe UI", 12, "bold"),
            padding=10
        )

        reserveBtn = ttk.Button(
            leftFrame,
            text="Reserve Car",
            command=self.reserve_window
        )
        reserveBtn.pack(pady=20, padx=20, fill="x")

        returnBtn = ttk.Button(
            leftFrame,
            text="Return Car",
            command=self.return_window
        )
        returnBtn.pack(pady=20, padx=20, fill="x")

        refreshBtn = ttk.Button(
            leftFrame,
            text="Refresh",
            command=self.load_data
        )
        refreshBtn.pack(pady=20, padx=20, fill="x")

        closeBtn = ttk.Button(
            leftFrame,
            text="Exit",
            command=self.root.destroy
        )
        closeBtn.pack(pady=20, padx=20, fill="x")



        rightFrame = tk.Frame(mainFrame, bg="#1e293b", bd=2, relief="ridge")
        rightFrame.pack(side="right", fill="both", expand=True)

        topBar = tk.Frame(rightFrame, bg="#1e293b")
        topBar.pack(fill="x", pady=10)

        searchLabel = tk.Label(
            topBar,
            text="Search Car:",
            bg="#1e293b",
            fg="white",
            font=("Segoe UI", 12, "bold")
        )
        searchLabel.pack(side="left", padx=10)

        self.searchEntry = ttk.Entry(topBar, width=30)
        self.searchEntry.pack(side="left", padx=10)

        searchBtn = ttk.Button(
            topBar,
            text="Search",
            command=self.search_car
        )
        searchBtn.pack(side="left")



        columns = ("reg", "car", "rent", "status")

        self.tree = ttk.Treeview(
            rightFrame,
            columns=columns,
            show="headings",
            height=25
        )

        self.tree.heading("reg", text="Registration No")
        self.tree.heading("car", text="Car Name")
        self.tree.heading("rent", text="Rent Per Day")
        self.tree.heading("status", text="Status")

        self.tree.column("reg", width=150)
        self.tree.column("car", width=250)
        self.tree.column("rent", width=150)
        self.tree.column("status", width=150)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_data()

    # ================= DATABASE =================

    def db_connect(self):
        self.con = pymysql.connect(
            host="localhost",
            user="root",
            password="Mahesh@1234",
            database="car"
        )

        self.cur = self.con.cursor()


    def create_card(self, parent, title, column):

        card = tk.Frame(parent, bg="#2563eb", width=250, height=100)
        card.grid(row=0, column=column, padx=20)

        label = tk.Label(
            card,
            text=title,
            bg="#2563eb",
            fg="white",
            font=("Segoe UI", 16, "bold")
        )
        label.pack(pady=10)

        value = tk.Label(
            card,
            text="0",
            bg="#2563eb",
            fg="white",
            font=("Segoe UI", 20, "bold")
        )
        value.pack()

        return value



    def load_data(self):

        self.db_connect()

        self.tree.delete(*self.tree.get_children())

        self.cur.execute("SELECT * FROM car")
        rows = self.cur.fetchall()

        total = len(rows)
        available = 0
        reserved = 0

        for row in rows:
            self.tree.insert("", tk.END, values=row)

            if row[3] == "Avail":
                available += 1
            else:
                reserved += 1

        self.totalCarsCard.config(text=str(total))
        self.availableCard.config(text=str(available))
        self.reservedCard.config(text=str(reserved))

        self.cur.close()
        self.con.close()



    def search_car(self):

        keyword = self.searchEntry.get()

        self.db_connect()

        query = f"SELECT * FROM car WHERE car LIKE '%{keyword}%' OR regNo LIKE '%{keyword}%'"

        self.cur.execute(query)
        rows = self.cur.fetchall()

        self.tree.delete(*self.tree.get_children())

        for row in rows:
            self.tree.insert("", tk.END, values=row)

        self.cur.close()
        self.con.close()



    def reserve_window(self):

        win = tk.Toplevel(self.root)
        win.title("Reserve Car")
        win.geometry("400x300")
        win.config(bg="#1e293b")

        tk.Label(
            win,
            text="Car Number",
            bg="#1e293b",
            fg="white",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=10)

        regEntry = ttk.Entry(win)
        regEntry.pack(pady=10)

        tk.Label(
            win,
            text="Days",
            bg="#1e293b",
            fg="white",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=10)

        dayEntry = ttk.Entry(win)
        dayEntry.pack(pady=10)

        def reserve_now():

            try:
                reg = int(regEntry.get())
                days = int(dayEntry.get())
            except:
                messagebox.showerror("Error", "Enter valid numbers")
                return

            self.db_connect()

            self.cur.execute(f"SELECT rent,status FROM car WHERE regNo={reg}")
            row = self.cur.fetchone()

            if row:

                if row[1] == "Avail":

                    amount = row[0] * days

                    self.cur.execute(
                        f"UPDATE car SET status='Reserved' WHERE regNo={reg}"
                    )

                    self.con.commit()

                    messagebox.showinfo(
                        "Success",
                        f"Car Reserved Successfully\n\nTotal Amount = {amount}"
                    )

                    self.load_data()
                    win.destroy()

                else:
                    messagebox.showerror("Error", "Car Already Reserved")

            else:
                messagebox.showerror("Error", "Car Not Found")

            self.cur.close()
            self.con.close()

        ttk.Button(
            win,
            text="Reserve",
            command=reserve_now
        ).pack(pady=20)



    def return_window(self):

        win = tk.Toplevel(self.root)
        win.title("Return Car")
        win.geometry("400x250")
        win.config(bg="#1e293b")

        tk.Label(
            win,
            text="Car Number",
            bg="#1e293b",
            fg="white",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=20)

        regEntry = ttk.Entry(win)
        regEntry.pack(pady=10)

        def return_now():

            try:
                reg = int(regEntry.get())
            except:
                messagebox.showerror("Error", "Enter valid car number")
                return

            self.db_connect()

            self.cur.execute(
                f"UPDATE car SET status='Avail' WHERE regNo={reg}"
            )

            self.con.commit()

            messagebox.showinfo(
                "Success",
                "Car Returned Successfully"
            )

            self.load_data()
            win.destroy()

            self.cur.close()
            self.con.close()

        ttk.Button(
            win,
            text="Return",
            command=return_now
        ).pack(pady=20)




root = tk.Tk()
obj = CarRental(root)
root.mainloop()
