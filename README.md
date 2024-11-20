# Student Management Application

This is a simple **Student Management Application** built using Python's **Tkinter** library. The application allows users to perform CRUD (Create, Read, Update, Delete) operations to manage student records.

---

## Features

1. **Add Student**  
   Allows users to add new student records, including:
   - Name
   - Age
   - Gender
   - Department, and more.

2. **View Students**  
   Displays all student records in a list. Users can browse and search for specific students.

3. **Update Student**  
   Enables editing and updating of existing student information.

4. **Delete Student**  
   Allows users to delete a student's record.

5. **User-Friendly Interface**  
   An intuitive and easy-to-navigate graphical interface for managing data.

---

## Environmental Variables

- **HOST**: The URL of the database server.

- **USER**: The username for login.

- **PASSWORD**: The password of the user.

- **BACKEND**: The database dialect and driver to use when connecting to the database. [Examples](https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls)

---

## How to Run

1. Install packages:

   ```shell
   pip install -r requirements.txt
   ```

   2. Set environment variables in `.env`

   3. Run application
   
   ```shell
   python main.py
   ```
