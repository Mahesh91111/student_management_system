import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pymysql


class StudentManagementSystem:

    def __init__(self, root):

        self.root = root
        self.root.title("Student Record Management System")

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()

        self.root.geometry(f"{self.width}x{self.height}+0+0")
        self.root.config(bg="white")

        # TITLE
        title = tk.Label(
            self.root,
            text="Student Record Management System",
            bd=5,
            relief="raised",
            bg="lightgreen",
            fg="black",
            font=("Elephant", 28, "bold")
        )

        title.pack(side="top", fill="x")

        # LEFT FRAME
        self.optFrame = tk.Frame(
            self.root,
            bd=5,
            relief="ridge",
            bg=self.clr(230, 150, 200)
        )

        self.optFrame.place(
            width=self.width / 3,
            height=self.height - 150,
            x=30,
            y=90
        )

        # RIGHT FRAME
        self.detFrame = tk.Frame(
            self.root,
            bd=5,
            relief="ridge",
            bg=self.clr(150, 230, 120)
        )

        self.detFrame.place(
            width=self.width / 2 + 80,
            height=self.height - 150,
            x=self.width / 3 + 70,
            y=90
        )

        # BUTTONS
        btnFont = ("Arial", 20, "bold")

        tk.Button(
            self.optFrame,
            text="Add_Student",
            command=self.addFrameFun,
            width=20,
            font=btnFont,
            bg="lightgray"
        ).grid(row=0, column=0, padx=30, pady=25)

        tk.Button(
            self.optFrame,
            text="Search_Student",
            command=self.searchStudent,
            width=20,
            font=btnFont,
            bg="lightgray"
        ).grid(row=1, column=0, padx=30, pady=25)

        tk.Button(
            self.optFrame,
            text="Update_Record",
            command=self.updateStudent,
            width=20,
            font=btnFont,
            bg="lightgray"
        ).grid(row=2, column=0, padx=30, pady=25)

        tk.Button(
            self.optFrame,
            text="Show_All",
            command=self.showAllData,
            width=20,
            font=btnFont,
            bg="lightgray"
        ).grid(row=3, column=0, padx=30, pady=25)

        tk.Button(
            self.optFrame,
            text="Remove_Student",
            command=self.deleteStudent,
            width=20,
            font=btnFont,
            bg="lightgray"
        ).grid(row=4, column=0, padx=30, pady=25)

        # TABLE TITLE
        lbl = tk.Label(
            self.detFrame,
            text="Record Details",
            font=("Arial", 28, "bold"),
            bg=self.clr(150, 230, 120)
        )

        lbl.pack(side="top", fill="x")

        self.tabFun()

        # LOAD DATA
        self.showAllData()

    # COLOR FUNCTION
    def clr(self, r, g, b):
        return f"#{r:02x}{g:02x}{b:02x}"

    # DATABASE CONNECTION
    def dbFun(self):

        self.con = pymysql.connect(
            host="localhost",
            user="root",
            password="Mahesh@1234",
            database="student"
        )

        self.cur = self.con.cursor()

    # TABLE
    def tabFun(self):

        tabFrame = tk.Frame(
            self.detFrame,
            bd=4,
            relief="sunken",
            bg="white"
        )

        tabFrame.place(
            width=self.width / 2,
            height=self.height - 260,
            x=20,
            y=70
        )

        x_scroll = tk.Scrollbar(tabFrame, orient="horizontal")
        y_scroll = tk.Scrollbar(tabFrame, orient="vertical")

        self.table = ttk.Treeview(
            tabFrame,
            columns=("roll", "name", "fname", "sub", "grade"),
            xscrollcommand=x_scroll.set,
            yscrollcommand=y_scroll.set
        )

        x_scroll.pack(side="bottom", fill="x")
        y_scroll.pack(side="right", fill="y")

        x_scroll.config(command=self.table.xview)
        y_scroll.config(command=self.table.yview)

        self.table.heading("roll", text="Roll_No")
        self.table.heading("name", text="Name")
        self.table.heading("fname", text="Father_Name")
        self.table.heading("sub", text="Subject")
        self.table.heading("grade", text="Grade")

        self.table["show"] = "headings"

        self.table.column("roll", width=100)
        self.table.column("name", width=150)
        self.table.column("fname", width=150)
        self.table.column("sub", width=150)
        self.table.column("grade", width=100)

        self.table.pack(fill="both", expand=1)

    # CLEAR FRAME
    def clearFrame(self):

        try:
            self.addFrame.destroy()
        except:
            pass

    # ADD STUDENT FRAME
    def addFrameFun(self):

        self.clearFrame()

        self.addFrame = tk.Frame(
            self.root,
            bd=5,
            relief="ridge",
            bg=self.clr(150, 180, 250)
        )

        self.addFrame.place(
            width=500,
            height=600,
            x=500,
            y=100
        )

        heading = tk.Label(
            self.addFrame,
            text="Add Student",
            font=("Arial", 22, "bold"),
            bg=self.clr(150, 180, 250)
        )

        heading.grid(row=0, column=0, columnspan=2, pady=20)

        # Roll No
        tk.Label(
            self.addFrame,
            text="Roll_No",
            font=("Arial", 15, "bold"),
            bg=self.clr(150, 180, 250)
        ).grid(row=1, column=0, padx=20, pady=20)

        self.rollNo = tk.Entry(
            self.addFrame,
            width=20,
            font=("Arial", 15)
        )

        self.rollNo.grid(row=1, column=1)

        # Name
        tk.Label(
            self.addFrame,
            text="Name",
            font=("Arial", 15, "bold"),
            bg=self.clr(150, 180, 250)
        ).grid(row=2, column=0, padx=20, pady=20)

        self.name = tk.Entry(
            self.addFrame,
            width=20,
            font=("Arial", 15)
        )

        self.name.grid(row=2, column=1)

        # Father Name
        tk.Label(
            self.addFrame,
            text="Father_Name",
            font=("Arial", 15, "bold"),
            bg=self.clr(150, 180, 250)
        ).grid(row=3, column=0, padx=20, pady=20)

        self.fname = tk.Entry(
            self.addFrame,
            width=20,
            font=("Arial", 15)
        )

        self.fname.grid(row=3, column=1)

        # Subject
        tk.Label(
            self.addFrame,
            text="Subject",
            font=("Arial", 15, "bold"),
            bg=self.clr(150, 180, 250)
        ).grid(row=4, column=0, padx=20, pady=20)

        self.sub = tk.Entry(
            self.addFrame,
            width=20,
            font=("Arial", 15)
        )

        self.sub.grid(row=4, column=1)

        # Grade
        tk.Label(
            self.addFrame,
            text="Grade",
            font=("Arial", 15, "bold"),
            bg=self.clr(150, 180, 250)
        ).grid(row=5, column=0, padx=20, pady=20)

        self.grade = tk.Entry(
            self.addFrame,
            width=20,
            font=("Arial", 15)
        )

        self.grade.grid(row=5, column=1)

        # SAVE BUTTON
        tk.Button(
            self.addFrame,
            text="SAVE",
            command=self.addStudent,
            bg="green",
            fg="white",
            font=("Arial", 18, "bold"),
            width=15
        ).grid(row=6, column=0, columnspan=2, pady=40)

    # ADD STUDENT
    def addStudent(self):

        rn = self.rollNo.get()
        name = self.name.get()
        fname = self.fname.get()
        sub = self.sub.get()
        grade = self.grade.get()

        if rn and name and fname and sub and grade:

            try:

                self.dbFun()

                sql = """
                INSERT INTO student
                (rollNo,name,fname,sub,grade)
                VALUES(%s,%s,%s,%s,%s)
                """

                values = (rn, name, fname, sub, grade)

                self.cur.execute(sql, values)

                self.con.commit()

                messagebox.showinfo(
                    "Success",
                    "Student Added Successfully"
                )

                self.showAllData()

                self.con.close()

                # CLOSE POPUP WINDOW
                self.addFrame.destroy()

            except Exception as e:

                messagebox.showerror(
                    "Error",
                    f"{e}"
                )

        else:

            messagebox.showerror(
                "Error",
                "Please Fill All Fields"
            )

    # SHOW ALL DATA
    def showAllData(self):

        try:

            self.dbFun()

            self.cur.execute("SELECT * FROM student")

            rows = self.cur.fetchall()

            self.table.delete(*self.table.get_children())

            for row in rows:
                self.table.insert('', tk.END, values=row)

            self.con.close()

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"{e}"
            )

    # SEARCH STUDENT
    def searchStudent(self):

        rn = simpledialog.askstring(
            "Search Student",
            "Enter Roll Number"
        )

        if rn:

            try:

                self.dbFun()

                self.cur.execute(
                    "SELECT * FROM student WHERE rollNo=%s",
                    (rn,)
                )

                row = self.cur.fetchone()

                self.table.delete(*self.table.get_children())

                if row:

                    self.table.insert('', tk.END, values=row)

                else:

                    messagebox.showinfo(
                        "Not Found",
                        "Student Record Not Found"
                    )

                self.con.close()

            except Exception as e:

                messagebox.showerror(
                    "Error",
                    f"{e}"
                )

    # UPDATE STUDENT
    def updateStudent(self):

        rn = simpledialog.askstring(
            "Update Student",
            "Enter Roll Number"
        )

        if rn:

            try:

                self.dbFun()

                self.cur.execute(
                    "SELECT * FROM student WHERE rollNo=%s",
                    (rn,)
                )

                row = self.cur.fetchone()

                if row:

                    name = simpledialog.askstring(
                        "Update",
                        "Enter New Name"
                    )

                    fname = simpledialog.askstring(
                        "Update",
                        "Enter New Father Name"
                    )

                    sub = simpledialog.askstring(
                        "Update",
                        "Enter New Subject"
                    )

                    grade = simpledialog.askstring(
                        "Update",
                        "Enter New Grade"
                    )

                    self.cur.execute(
                        """
                        UPDATE student
                        SET name=%s,
                            fname=%s,
                            sub=%s,
                            grade=%s
                        WHERE rollNo=%s
                        """,
                        (name, fname, sub, grade, rn)
                    )

                    self.con.commit()

                    messagebox.showinfo(
                        "Success",
                        "Record Updated Successfully"
                    )

                    self.showAllData()

                else:

                    messagebox.showerror(
                        "Error",
                        "Student Record Not Found"
                    )

                self.con.close()

            except Exception as e:

                messagebox.showerror(
                    "Error",
                    f"{e}"
                )

    # DELETE STUDENT
    def deleteStudent(self):

        rn = simpledialog.askstring(
            "Delete Student",
            "Enter Roll Number"
        )

        if rn:

            try:

                self.dbFun()

                self.cur.execute(
                    "DELETE FROM student WHERE rollNo=%s",
                    (rn,)
                )

                self.con.commit()

                messagebox.showinfo(
                    "Deleted",
                    "Record Deleted Successfully"
                )

                self.showAllData()

                self.con.close()

            except Exception as e:

                messagebox.showerror(
                    "Error",
                    f"{e}"
                )


# MAIN
root = tk.Tk()

obj = StudentManagementSystem(root)

root.mainloop()## Taks complete