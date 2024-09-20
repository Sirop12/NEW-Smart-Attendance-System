import sqlite3 as sq
from settings import DB_PATH, connect, cursor

def get_users():
    try:
        cursor.execute("SELECT ID, Name, PhotoPath FROM Users")
        users = cursor.fetchall()
        user_list = [{"ID": user[0], "Name": user[1], "PhotoPath": user[2]} for user in users]
        print(f"Загружены пользователи: {user_list}")
        return user_list
    except sq.Error as e:
        print(f"Ошибка при получении пользователей: {e}")
        return []

def get_user_by_id(user_id):
    try:
        cursor.execute("SELECT ID, Name, PhotoPath FROM Users WHERE ID = ?", (user_id,))
        user = cursor.fetchone()
        if user:
            user_data = {"ID": user[0], "Name": user[1], "PhotoPath": user[2]}
            print(f"Данные пользователя: {user_data}")
            return user_data
        else:
            print(f"Пользователь с ID {user_id} не найден")
            return None
    except sq.Error as e:
        print(f"Ошибка при получении пользователя с ID {user_id}: {e}")
        return None

def update_user_data(user_id, new_value):
    try:
        cursor.execute("UPDATE Users SET Name = ? WHERE ID = ?", (new_value, user_id))
        connect.commit()
        print(f"Пользователь с ID {user_id} обновлен до {new_value}")
    except sq.Error as e:
        print(f"Ошибка при обновлении пользователя с ID {user_id}: {e}")

def delete_user(user_id):
    try:
        cursor.execute("DELETE FROM Users WHERE ID = ?", (user_id,))
        connect.commit()
        print(f"Пользователь с ID {user_id} удален")
    except sq.Error as e:
        print(f"Ошибка при удалении пользователя с ID {user_id}: {e}")

def add_user(name, photo_path):
    try:
        cursor.execute("INSERT INTO Users (Name, PhotoPath) VALUES (?, ?)", (name, photo_path))
        connect.commit()
        print(f"Добавлен пользователь {name}")
    except sq.Error as e:
        print(f"Ошибка при добавлении пользователя: {e}")

def commit_changes():
    try:
        connect.commit()
        print("Изменения сохранены")
    except sq.Error as e:
        print(f"Ошибка при сохранении изменений: {e}")
