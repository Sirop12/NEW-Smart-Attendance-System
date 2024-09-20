import tkinter as tk
from tkinter import simpledialog, messagebox
from ttkthemes import ThemedTk
import ttkbootstrap as ttk
import hashlib
import pygame
import cv2
from db import get_users, get_user_by_id, update_user_data, delete_user, add_user, commit_changes
from settings import DB_PATH, PHOTO_PATH, SOUND_PATH, connect, cursor
import time



def show_message(title, message):
    messagebox.showinfo(title, message)

def prompt_password(title, prompt):
    return simpledialog.askstring(title, prompt, show='*')

def prompt_input(title, prompt):
    return simpledialog.askstring(title, prompt)

def confirm_action(title, prompt):
    return messagebox.askyesno(title, prompt)

def update_user_list(tree):
    for i in tree.get_children():
        tree.delete(i)
    cursor.execute("SELECT * FROM Users")
    result = cursor.fetchall()
    for row in result:
        tree.insert("", "end", values=row)

def update_data_list(tree):
    for i in tree.get_children():
        tree.delete(i)
    cursor.execute("SELECT * FROM Data")
    result = cursor.fetchall()
    for row in result:
        tree.insert("", "end", values=row)

def search_user(search_var, tree):
    search_term = search_var.get()
    for i in tree.get_children():
        tree.delete(i)
    cursor.execute("SELECT * FROM Users WHERE Name LIKE ?", ('%' + search_term + '%', ))
    result = cursor.fetchall()
    for row in result:
        tree.insert("", "end", values=row)

def clear_search(search_var, tree):
    search_var.set("")
    update_user_list(tree)

def admin_mode():
    pygame.mixer.music.load(SOUND_PATH + 'check_admin.mp3')
    pygame.mixer.music.play()

    password = prompt_password("Администратор", "Введите пароль")
    if not password:
        return

    if hashlib.sha256(password.encode()).hexdigest() == "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4":
        pygame.mixer.music.load(SOUND_PATH + 'set.mp3')
        pygame.mixer.music.play()

        root = ThemedTk(theme="Black")  # Используем темную тему
        root.title("Admin Mode")
        root.geometry("800x600")

        tab_control = ttk.Notebook(root)

        users_tab = ttk.Frame(tab_control)
        data_tab = ttk.Frame(tab_control)

        tab_control.add(users_tab, text='Users')
        tab_control.add(data_tab, text='Data')

        tab_control.pack(expand=1, fill='both')

        # Users tab
        users_frame = ttk.Frame(users_tab)
        users_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        search_frame = ttk.Frame(users_tab)
        search_frame.pack(side=tk.TOP, fill=tk.X)

        search_label = ttk.Label(search_frame, text="Search:")
        search_label.pack(side=tk.LEFT, padx=5, pady=5)

        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

        search_button = ttk.Button(search_frame, text="Search", command=lambda: search_user(search_var, user_tree))
        search_button.pack(side=tk.LEFT, padx=5, pady=5)

        clear_search_button = ttk.Button(search_frame, text="Clear Search", command=lambda: clear_search(search_var, user_tree))
        clear_search_button.pack(side=tk.LEFT, padx=5, pady=5)

        def on_data_double_click(event):
            item = data_tree.selection()[0]
            col = data_tree.identify_column(event.x)
            col_index = int(col.replace("#", "")) - 1
            old_value = data_tree.item(item, "values")[col_index]
            new_value = simpledialog.askstring("Edit Value", "Enter new value:", initialvalue=old_value)

            if new_value:
                col_name = data_tree.heading(col)["text"]
                row_id = data_tree.item(item)["values"][0]  # Assuming the first column is a unique ID
                cursor.execute(f"UPDATE Data SET \"{col_name}\" = ? WHERE ID = ?", (new_value, row_id))
                connect.commit()
                update_data_list(data_tree)

        def on_user_double_click(event):
            item = user_tree.selection()[0]
            col = user_tree.identify_column(event.x)
            col_index = int(col.replace("#", "")) - 1
            old_value = user_tree.item(item, "values")[col_index]
            new_value = simpledialog.askstring("Edit Value", "Enter new value:", initialvalue=old_value)

            if new_value:
                col_name = user_tree.heading(col)["text"]
                user_id = user_tree.item(item)["values"][0]  # Assuming the first column is a unique ID
                cursor.execute(f"UPDATE Users SET \"{col_name}\" = ? WHERE ID = ?", (new_value, user_id))
                connect.commit()
                update_user_list(user_tree)

        user_tree = ttk.Treeview(users_frame, columns=('ID', 'Name', 'PhotoPath'), show='headings')
        user_tree.heading('ID', text='ID')
        user_tree.heading('Name', text='Name')
        user_tree.heading('PhotoPath', text='PhotoPath')

        user_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        user_scrollbar = ttk.Scrollbar(users_frame, orient="vertical", command=user_tree.yview)
        user_scrollbar.pack(side=tk.RIGHT, fill='y')

        user_tree.configure(yscroll=user_scrollbar.set)

        update_user_list(user_tree)
        user_tree.bind("<Double-1>", on_user_double_click)

        def add_user():
            Name = prompt_input("Add User", "Enter name:")

            if Name:
                cursor.execute(f'INSERT INTO `Users` (`Name`) VALUES ("NewUser")')
                connect.commit()
                result = cursor.execute('''SELECT `ID` FROM `Users` WHERE `Name` == "NewUser"''')
                UID = result[0]
                update_user_data(UID, Name)
                photo_path = PHOTO_PATH + f"{UID}.jpg"
                update_user_data(UID, photo_path)
                show_message("Администратор", "Убедитесь, что камера видит человека.")
                cv2.imwrite(photo_path, frame)
                update_user_list(user_tree)

        def delete_user():
            selected_item = user_tree.selection()[0]
            user_id = user_tree.item(selected_item)['values'][0]
            delete_user(user_id)
            update_user_list(user_tree)

        def update_user():
            selected_item = user_tree.selection()[0]
            user_id = user_tree.item(selected_item)['values'][0]
            column = prompt_input("Update User", "Enter column to update:")
            value = prompt_input("Update User", "Enter new value:")
            if column and value:
                update_user_data(user_id, value)
                update_user_list(user_tree)

        def commit_changes():
            commit_changes()
            show_message("Admin", "Changes committed!")

        btn_frame = ttk.Frame(users_tab)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X)

        add_btn = ttk.Button(btn_frame, text="Add User", command=add_user)
        add_btn.pack(side=tk.LEFT)

        update_btn = ttk.Button(btn_frame, text="Update User", command=update_user)
        update_btn.pack(side=tk.LEFT)

        delete_btn = ttk.Button(btn_frame, text="Delete User", command=delete_user)
        delete_btn.pack(side=tk.LEFT)

        commit_btn = ttk.Button(btn_frame, text="Commit Changes", command=commit_changes)
        commit_btn.pack(side=tk.LEFT)

        # Data tab
        data_frame = ttk.Frame(data_tab)
        data_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        data_tree = ttk.Treeview(data_frame, columns=('ID', 'Value'), show='headings')
        data_tree.heading('ID', text='ID')
        data_tree.heading('Value', text='Value')

        data_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        data_scrollbar = ttk.Scrollbar(data_frame, orient="vertical", command=data_tree.yview)
        data_scrollbar.pack(side=tk.RIGHT, fill='y')

        data_tree.configure(yscroll=data_scrollbar.set)

        update_data_list(data_tree)

        data_tree.bind("<Double-1>", on_data_double_click)

        def add_data():
            key = prompt_input("Add Data", "Enter key:")
            value = prompt_input("Add Data", "Enter value:")
            if key and value:
                cursor.execute(f'INSERT INTO Data (`ID`, `Value`) VALUES (?, ?)', (key, value))
                connect.commit()
                update_data_list(data_tree)

        def update_data():
            selected_item = data_tree.selection()[0]
            name = data_tree.item(selected_item)['values'][0]
            value = prompt_input("Update Data", "Enter new value:")
            if value:
                cursor.execute(f"UPDATE Data SET `Value` = ? WHERE `ID` = ?", (value, name))
                connect.commit()
                update_data_list(data_tree)

        def delete_data():
            selected_item = data_tree.selection()[0]
            name = data_tree.item(selected_item)['values'][0]
            cursor.execute(f"DELETE FROM Data WHERE `ID` = ?", (name,))
            connect.commit()
            update_data_list(data_tree)

        data_btn_frame = ttk.Frame(data_tab)
        data_btn_frame.pack(side=tk.BOTTOM, fill=tk.X)

        add_data_btn = ttk.Button(data_btn_frame, text="Add Data", command=add_data)
        add_data_btn.pack(side=tk.LEFT)

        update_data_btn = ttk.Button(data_btn_frame, text="Update Data", command=update_data)
        update_data_btn.pack(side=tk.LEFT)

        delete_data_btn = ttk.Button(data_btn_frame, text="Delete Data", command=delete_data)
        delete_data_btn.pack(side=tk.LEFT)

        root.mainloop()

    else:
        pygame.mixer.music.load(SOUND_PATH + 'uncorrect.mp3')
        pygame.mixer.music.play()
        time.sleep(2)
