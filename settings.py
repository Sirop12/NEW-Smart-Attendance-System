import os
import sqlite3 as sq
import pygame
import cv2

# Настройки
DB_PATH = r'C:\\admin\\data\\db_admin.db'
PHOTO_PATH = r'C:\\admin\\data\\photo\\'
MODEL_NAME = 'Facenet512'
THREAD_COUNT = 1  # Количество потоков
SOUND_PATH = r'C:\\admin\\data\\sound\\'
EXCEL_LOG_PATH = r'C:\\admin\\data\\log.xlsx'

# Настройка камеры
CAMERA_INDEX = 3

# Подключение к базе данных
connect = sq.connect(DB_PATH, check_same_thread=False)
cursor = connect.cursor()

# Инициализация Pygame
pygame.mixer.init()
