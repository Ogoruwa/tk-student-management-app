from re import match
from enum import Enum
from hashlib import md5
from sqlalchemy.exc import IntegrityError

from tkinter import StringVar, Canvas
from tkinter.ttk import Frame, Entry, Label, Combobox, Button, Separator, Scrollbar
from tkinter.constants import BOTH, LEFT, RIGHT, TOP, BOTTOM, VERTICAL, DISABLED, NORMAL, ALL, SUNKEN

from models import Student, Employee


GENDERS = ("Male", "Female")
DEPARTMENTS = ("A", "B", "C", "D", "E")
REG_NUMBER_PATTERN = f"({'|'.join(DEPARTMENTS)})" + r"/(\d{2})/(\d{4})"


def validate_student_data(fn: str, mn: str, ln: str, reg: str, gender: str, dep: str, update: bool = False):
    message = ""
    passed = False

    if not (1 <= len(fn) <= 64):
        message = "First name should be 1 to 64 chracters long"
    elif not (1 <= len(mn) <= 64):
        message = "Middle name should be 1 to 64 chracters long"
    elif not (1 <= len(ln) <= 64):
        message = "Middle name should be 1 to 64 chracters long"
    elif not match(REG_NUMBER_PATTERN, reg):
        message = "Registration number should be of the format DEP/24/1234"
    elif gender not in GENDERS:
        message = f"Gender should be one of {','.join(GENDERS)}"
    elif dep not in DEPARTMENTS:
        message = f"{dep} department does not exist"
    elif reg[:reg.find("/")] != dep:
        message = "Registration number and department do not match"
    elif not update and Student.get(reg_number = reg).first():
        message = f"Student with registration number already {reg} exists"
    else:
        passed = True

    return passed, message


class AppFrame:
    def __init__(self, app, master) -> None:
        self._app = app
        self._frame = Frame(master)
        self.init_ui()
    
    def init_ui(self):
        pass

    def layout(self):
        self._frame.pack(expand = True, side = TOP, fill = BOTH)
    
    def destroy(self):
        self._frame.destroy()


class LoginFrame(AppFrame):
    def init_ui(self):
        self._username = StringVar(self._frame, "", "username")
        self._password = StringVar(self._frame, "", "password")
        self._error_message = StringVar(self._frame, "", "error_message")
        
        self._frame_name = Frame(self._frame)
        self._frame_password = Frame(self._frame)

        self._entry_name = Entry(self._frame_name, textvariable = self._username, validate = "all")
        self._entry_password = Entry(self._frame_password, textvariable = self._password)

        self._label_name = Label(self._frame_name, text = "Name: ")
        self._label_password = Label(self._frame_password, text = "Password: ")
        self._label_message = Label(self._frame, textvariable = self._error_message)

        self._button_submit = Button(self._frame, command = self.login, text = "Login")
    

    def layout(self):
        super().layout()
        self._label_message.pack(expand = True, side = TOP, pady = (0, 10))
        
        self._frame_name.pack(expand = True, side = TOP)
        self._label_name.pack(expand = True, side = LEFT)
        self._entry_name.pack(expand = True, side = LEFT)
        
        self._frame_password.pack(expand = True, side = TOP)
        self._label_password.pack(expand = True, side = LEFT)
        self._entry_password.pack(expand = True, side = LEFT)

        self._button_submit.pack(expand = True, side = TOP, pady = (20,0))
        self._frame.after(1000, self._entry_name.focus_set)


    def login(self):
        self._error_message.set("")
        username = self._entry_name.get()

        employee: Employee = Employee.get(username = username).first()
        # Have to check if the username matches, because the get_object method is case insensitive
        if not employee or employee.username != username:
            self._error_message.set("User not found")
            return

        # TODO: Add logic to get password from database 
        password = employee.password
        hashed = md5(self._password.get().encode()).hexdigest()
        
        if hashed != password:
            self._error_message.set("Password is incorrect")
            return
        
        self._app.load_frame(FRAMES.MENU.value)
    

class MainMenuFrame(AppFrame):
    def init_ui(self):
        self._button_create = Button(self._frame, text = "Add student", command = self.create)
        self._button_view = Button(self._frame, text = "View students", command = self.view)
    
    def layout(self):
        super().layout()
        self._button_create.pack(expand = True, side = TOP)
        self._button_view.pack(expand = True, side = TOP)                           
        self._button_create.focus_set()
    

    def logout(self):
        self._app.back()
    
    def create(self):
        self._app.load_frame(FRAMES.CREATE.value)
    
    def view(self):
        self._app.load_frame(FRAMES.VIEW.value)



class StudentCreateFrame(AppFrame):
    def __init__(self, app, master) -> None:
        super().__init__(app, master)

    def init_ui(self):
        self.var_message = StringVar(self._frame, "", "message")
        self.var_first_name = StringVar(self._frame, "", "first_name")
        self.var_middle_name = StringVar(self._frame, "", "middle_name")
        self.var_last_name = StringVar(self._frame, "", "last_name")
        self.var_gender = StringVar(self._frame, "", "gender")
        self.var_reg_number = StringVar(self._frame, "", "reg_number")
        self.var_department = StringVar(self._frame, "", "department")
        
        self.label_first_name = Label(self._frame, text = "First name")
        self.label_middle_name = Label(self._frame, text = "Middle name")
        self.label_last_name = Label(self._frame, text = "Last name")
        self.label_gender = Label(self._frame, text = "Gender")
        self.label_reg_number = Label(self._frame, text = "Registration number")
        self.label_department = Label(self._frame, text = "Department")
        self.label_message = Label(self._frame, textvariable = self.var_message)

        self.entry_first_name = Entry(self._frame, textvariable = self.var_first_name)
        self.entry_middle_name = Entry(self._frame, textvariable = self.var_middle_name)
        self.entry_last_name = Entry(self._frame, textvariable = self.var_last_name)
        self.entry_reg_number = Entry(self._frame, textvariable = self.var_reg_number)
        self.combo_gender = Combobox(self._frame, textvariable = self.var_gender, values = GENDERS, state = "readonly")
        self.entry_department = Combobox(self._frame, textvariable = self.var_department, state = "readonly", values = DEPARTMENTS)
        self.button_create = Button(self._frame, text = "Add", command = self.create)


    def layout(self):
        super().layout()

        self.label_message.pack(side = TOP, expand = True)
        self.label_first_name.pack(side = TOP, expand = True)
        self.entry_first_name.pack(side = TOP, expand = True)
        self.label_middle_name.pack(side = TOP, expand = True)
        self.entry_middle_name.pack(side = TOP, expand = True)
        self.label_last_name.pack(side = TOP, expand = True)
        self.entry_last_name.pack(side = TOP, expand = True)
        
        self.label_reg_number.pack(side = TOP, expand = True)
        self.entry_reg_number.pack(side = TOP, expand = True)
        self.label_gender.pack(side = TOP, expand = True)
        self.combo_gender.pack(side = TOP, expand = True)
        self.label_department.pack(side = TOP, expand = True)
        self.entry_department.pack(side = TOP, expand = True)
        self.button_create.pack(side = BOTTOM, expand = True)

        self.entry_first_name.focus_set()


    def create(self) -> None:
        self.var_message.set("")

        fn = self.var_first_name.get()
        mn = self.var_middle_name.get()
        ln = self.var_last_name.get()
        reg = self.var_reg_number.get()
        gender = self.var_gender.get()
        dep = self.var_department.get()

        passed, message = validate_student_data(fn, mn, ln, reg, gender, dep)
        if not passed:   
            self.var_message.set(message)
            self._frame.after(1200, self.var_message.set, "")
            return
        
        try:
            student = Student(first_name = fn, middle_name = mn, last_name = ln, reg_number = reg, gender = gender, department = dep)
            student.save()
        except IntegrityError as exception:
            self.var_message.set(f"Student could not be created: {exception}")
            return

        def cmd():
            self.clear()
            self.var_message.set("")
            self.button_create.configure(state = NORMAL)
        
        self.button_create.configure()
        self.var_message.set("Student added successfully")
        self._frame.after(1200, cmd)
    

    def clear(self):
        self.var_first_name.set("")
        self.var_middle_name.set("")
        self.var_last_name.set("")
        self.var_gender.set("")
        self.var_reg_number.set("")
        self.var_department.set("")



class StudentViewFrame(AppFrame):
    def __init__(self, app, master) -> None:
        super().__init__(app, master)    
        self._updated = False
        self._prev_search = None

    def init_ui(self):
        self._students: list = []
        self._student: Student = None
        self.frame_search = Frame(self._frame)
        self.canvas_list = Canvas(self._frame)
        self.frame_detail = Frame(self._frame)
        self.frame_list = Frame(self.canvas_list, relief = SUNKEN)
        self.scroll_list = Scrollbar(self._frame, orient = VERTICAL, command = self.canvas_list.yview)

        self.var_search = StringVar(self.frame_list, "", "search")
        self.var_message = StringVar(self.frame_detail, "", "message")
        self.var_first_name = StringVar(self.frame_detail, "", "first_name")
        self.var_middle_name = StringVar(self.frame_detail, "", "middle_name")
        self.var_last_name = StringVar(self.frame_detail, "", "last_name")
        self.var_gender = StringVar(self.frame_detail, "", "gender")
        self.var_reg_number = StringVar(self.frame_detail, "", "reg_number")
        self.var_department = StringVar(self.frame_detail, "", "department")
        
        self.label_list = Label(self.frame_list, text = "List of students")
        self.label_first_name = Label(self.frame_detail, text = "First name")
        self.label_middle_name = Label(self.frame_detail, text = "Middle name")
        self.label_last_name = Label(self.frame_detail, text = "Last name")
        self.label_reg_number = Label(self.frame_detail, text = "Registration number")
        self.label_gender = Label(self.frame_detail, text = "Gender")
        self.label_department = Label(self.frame_detail, text = "Department")
        self.label_message = Label(self._frame, textvariable = self.var_message)

        self.entry_first_name = Entry(self.frame_detail, textvariable = self.var_first_name)
        self.entry_middle_name = Entry(self.frame_detail, textvariable = self.var_middle_name)
        self.entry_last_name = Entry(self.frame_detail, textvariable = self.var_last_name)
        self.entry_reg_number = Entry(self.frame_detail, textvariable = self.var_reg_number)
        self.combo_gender = Combobox(self.frame_detail, textvariable = self.var_gender, values = GENDERS, state = "readonly")
        self.entry_department = Combobox(self.frame_detail, textvariable = self.var_department, state = "readonly", values = DEPARTMENTS)
        self.button_update = Button(self.frame_detail, text = "Update", command = self.update)
        self.button_delete = Button(self.frame_detail, text = "Delete", command = self.delete)
        
        self.label_search = Label(self.frame_search, text = "Registration Number")
        self.entry_search = Entry(self.frame_search, textvariable = self.var_search)
        
        def cmd():
            self._prev_search = self.entry_search.get()
            self.load_list()
        self.button_search = Button(self.frame_search, text = "Search", command = cmd)
    

    def layout(self):
        super().layout()
        self.frame_search.pack(side = TOP, expand = True)
        self.label_message.pack(side = TOP, expand = True)
        self.canvas_list.pack(side = LEFT, expand = True)
        self.scroll_list.pack(side = LEFT, fill = BOTH, expand = True)
        self.frame_detail.pack(side = LEFT, expand = True)
        
        self.canvas_list.create_window( 10, 10,  window = self.frame_list )
        self.canvas_list.configure( yscrollcommand = self.scroll_list.set )

        self.label_search.pack(side = LEFT, expand = True)
        self.entry_search.pack(side = LEFT, expand = True)
        self.button_search.pack(side = LEFT, expand = True)

        self.label_list.pack(side = TOP)
        self.label_first_name.pack(side = TOP, expand = True)
        self.entry_first_name.pack(side = TOP, expand = True)
        self.label_middle_name.pack(side = TOP, expand = True)
        self.entry_middle_name.pack(side = TOP, expand = True)
        self.label_last_name.pack(side = TOP, expand = True)
        self.entry_last_name.pack(side = TOP, expand = True)
        
        self.label_reg_number.pack(side = TOP, expand = True)
        self.entry_reg_number.pack(side = TOP, expand = True)
        self.label_gender.pack(side = TOP, expand = True)
        self.combo_gender.pack(side = TOP, expand = True)
        self.label_department.pack(side = TOP, expand = True)
        self.entry_department.pack(side = TOP, expand = True)
        self.button_delete.pack(side = BOTTOM, expand = True, pady = (10,0))
        self.button_update.pack(side = BOTTOM, expand = True, pady = (10,0))
        self.frame_list.bind ( "<Configure>" , self.resize_scroll )
        self.entry_search.focus_set()
    

    def resize_scroll(self , *args):
        self.canvas_list.configure( scrollregion = self.canvas_list.bbox(ALL) )


    def load_list(self):
        reg_number = self._prev_search if self._updated else self.var_search.get()
        for child in self._students:
            child.destroy()
        
        # Get only first name, middle name, last name and registration number
        students = Student.get().with_entities(Student.first_name, Student.middle_name, Student.last_name, Student.reg_number).filter(Student.reg_number.ilike(f"%{reg_number}%"))
        if not students:
            self.var_message.set("No student found with similar registrstion number")
            return
        
        # Creat a label and button for each student
        for student in students: 
            first_name, middle_name, last_name, reg_number = student
            full_name = f"{first_name} {middle_name} {last_name}"
            text = f"Name: {full_name}\nRegistration number: {reg_number}"
            
            def cmd(reg: str):
                return lambda: self.load_details(reg)
            
            frame = Frame(self.frame_list)
            label = Label(frame, text = text)
            button = Button(frame, text = "View", command = cmd(reg_number))
            self._students.append(frame)

            frame.pack(side = TOP, expand = True, pady = (5,5))
            label.pack(side = LEFT, expand = True, padx = (10, 10))
            button.pack(side = RIGHT)
    

    def load_details(self, reg_number: str):
        self.var_message.set("")
        student = Student.get(reg_number = reg_number).first()
        
        if not student:
            self.var_message.set(f"Student with registration number {reg_number} not found")
            return
        
        self._student = student
        self.var_first_name.set(student.first_name)
        self.var_middle_name.set(student.middle_name)
        self.var_last_name.set(student.last_name)
        self.var_reg_number.set(student.reg_number)
        self.var_gender.set(student.gender)
        self.var_department.set(student.department)
    

    def toggle(self, on: bool):
        self.load_list()
        state = NORMAL if on else DISABLED
        self.button_update.configure(state = state)
        self.button_delete.configure(state = state)
        

    def clear(self):
        self.var_first_name.set("")
        self.var_middle_name.set("")
        self.var_last_name.set("")
        self.var_gender.set("")
        self.var_reg_number.set("")
        self.var_department.set("")
        self._student = None


    def delete(self):
        if not self._student:
            self.var_message.set("Select a student")
            return
        
        # reg_number = self.entry_reg_number.get()
        # obj = Student.get(reg_number = reg_number).first()
        # if not obj:
        #     self.var_message.set("Student ")
        #     return

        def cmd():
            self.toggle(True)
            self.var_message.set("")
        
        try:
            self.var_message.set("")
            self._student.delete()
            
            self.clear()
            self.toggle(False)
            self.var_message.set("Student deleted successfully")
            self._frame.after(1200, cmd)
        except IntegrityError as exception:
            self.var_message.set(f"{exception}")
    

    def get_input_data(self):
        fn = self.var_first_name.get()
        mn = self.var_middle_name.get()
        ln = self.var_last_name.get()
        reg = self.var_reg_number.get()
        gender = self.var_gender.get()
        dep = self.var_department.get()
        return fn, mn, ln, reg, gender, dep


    def update(self):
        if not self._student:
            self.var_message.set("Select a student")
            return
        elif self._updated:
            return

        self.var_message.set("")
        fn, mn, ln, reg, gender, dep = self.get_input_data()
        passed, message = validate_student_data(fn, mn, ln, reg, gender, dep, update = True)
        if not passed:
            self.var_message.set(message)
            return

        self._student.first_name = fn
        self._student.middle_name = mn
        self._student.last_name = ln
        self._student.gender = gender
        self._student.reg_number = reg
        self._student.department =  dep
        
        try:
            self._student.save(update = True)
        except IntegrityError as exception:
            self.var_message.set(f"{exception}")
            return
        
        def cmd():
            self.var_message.set("")
            self.toggle(True)
        
        self.toggle(False)
        self.var_message.set("Student updated successfully")
        self.frame_detail.after(1200, cmd)



class FRAMES(Enum):
    """Enum containing available frames"""
    MENU = MainMenuFrame
    LOGIN = LoginFrame
    VIEW = StudentViewFrame
    CREATE = StudentCreateFrame
