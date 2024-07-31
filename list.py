from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

def add_task():
    task_string = task_field.get()
    if len(task_string) == 0:
        messagebox.showinfo('Error', 'Field is Empty.')
    else:
        tasks.append(task_string)
        the_cursor.execute('INSERT INTO tasks VALUES (?)', (task_string,))
        list_update()
        task_field.delete(0, 'end')

def list_update():
    clear_list()
    for task in tasks:
        task_listbox.insert('end', task)

def delete_task():
    try:
        the_value = task_listbox.get(task_listbox.curselection())
        if the_value in tasks:
            tasks.remove(the_value)
            list_update()
            the_cursor.execute('DELETE FROM tasks WHERE title = ?', (the_value,))
    except:
        messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')

def delete_all_tasks():
    message_box = messagebox.askyesno('Delete All', 'Are you sure?')
    if message_box:
        while(len(tasks) != 0):
            tasks.pop()
        the_cursor.execute('DELETE FROM tasks')
        list_update()

def clear_list():
    task_listbox.delete(0, 'end')

def close():
    print(tasks)
    guiWindow.destroy()

def retrieve_database():
    while(len(tasks) != 0):
        tasks.pop()
    for row in the_cursor.execute('SELECT title FROM tasks'):
        tasks.append(row[0])

if __name__ == "__main__":
    guiWindow = Tk()
    guiWindow.title("To-Do List")
    guiWindow.geometry("360x640")  # Set to mobile resolution
    guiWindow.resizable(0, 0)
    guiWindow.configure(bg = "#B5E5CF")

    the_connection = sql.connect('listOfTasks.db')
    the_cursor = the_connection.cursor()
    the_cursor.execute('CREATE TABLE IF NOT EXISTS tasks (title TEXT)')

    tasks = []

    functions_frame = Frame(guiWindow, bg = "#8EE5EE")
    functions_frame.pack(side = "top", expand = True, fill = "both")

    task_label = Label(functions_frame, text="TO-DO-LIST \nEnter the Task Title:",
                       font=("arial", "10", "bold"),  # Smaller font size for mobile
                       background="#8EE5EE",
                       foreground="#FF6103")
    task_label.place(x = 20, y = 30)

    task_field = Entry(functions_frame,
                       font=("Arial", "10"),  # Smaller font size for mobile
                       width=30,  # Adjust width for mobile
                       foreground="black",
                       background="white")
    task_field.place(x = 20, y = 70)

    add_button = Button(functions_frame,
                        text="Add",
                        width=10,  # Adjust width for mobile
                        bg='#D4AC0D', font=("arial", "10", "bold"),  # Smaller font size for mobile
                        command=add_task)
    add_button.place(x=20, y=110)

    del_button = Button(functions_frame,
                        text="Remove",
                        width=10,  # Adjust width for mobile
                        bg='#D4AC0D', font=("arial", "10", "bold"),  # Smaller font size for mobile
                        command=delete_task)
    del_button.place(x=140, y=110)

    del_all_button = Button(functions_frame,
                            text="Delete All",
                            width=10,  # Adjust width for mobile
                            font=("arial", "10", "bold"),  # Smaller font size for mobile
                            bg='#D4AC0D',
                            command=delete_all_tasks)
    del_all_button.place(x=260, y=110)

    exit_button = Button(functions_frame,
                         text="Exit / Close",
                         width=30,  # Adjust width for mobile
                         bg='#D4AC0D', font=("arial", "10", "bold"),  # Smaller font size for mobile
                         command=close)
    exit_button.place(x=20, y=570)

    task_listbox = Listbox(functions_frame,
                           width=45,  # Adjust width for mobile
                           height=20,  # Adjust height for mobile
                           font=("Arial", "10", "bold"),  # Smaller font size for mobile
                           selectmode='SINGLE',
                           background="WHITE",
                           foreground="BLACK",
                           selectbackground="#FF8C00",
                           selectforeground="BLACK")
    task_listbox.place(x=20, y=150)

    retrieve_database()
    list_update()
    guiWindow.mainloop()
    the_connection.commit()
    the_cursor.close()
