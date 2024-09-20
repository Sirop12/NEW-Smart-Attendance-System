import cv2
import threading
import time
import worker2
from settings import CAMERA_INDEX
from audio import record_and_recognize_audio  # Импортируем функцию для распознавания речи
from admin import admin_mode  # Импортируем функцию для режима администратора

camReady = False
frame = None

# Функция для захвата изображения с камеры
def camera_loader():
    global frame, camReady
    camera = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)
    while True:
        ret, frame = camera.read()
        if ret:
            cv2.imshow('Камера', frame)
            cv2.waitKey(1)
        if not camReady:
            time.sleep(0.5)
            camReady = True
            print("Камера готова к работе")

def main():
    global camReady, frame
    print("Запуск камеры...")
    threading.Thread(target=camera_loader, daemon=True).start()

    while not camReady:
        print("Ожидание камеры...")
        time.sleep(0.2)

    while True:
        # Процесс распознавания лиц с использованием текущего кадра
        ID = worker2.Qest(frame)
        print("Полученный ID:", ID)

        # Можно добавить функцию для распознавания голоса
        if ID:
            print("Голосовой ввод")
            voice_input = record_and_recognize_audio()
            if voice_input:
                print(f"Распознана голосовая команда: {voice_input}")
                if voice_input.lower() == "админ":
                    admin_mode()
        else:
            print("Чела нет на фото")

if __name__ == '__main__':
    worker2.Create_Tread()
    main()




"""import cv2
import asyncio
from worker import process_images  # Импортируем функцию для проверки лиц
import time
import worker2
from settings import CAMERA_INDEX
from audio import record_and_recognize_audio  # Импортируем функцию для распознавания речи

camReady = False
frame = None

# Функция для захвата изображения с камеры
async def camera_loader():
    global frame, camReady
    print("Запуск камеры...")
    camera = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)
    print("Камера готова к работе")
    while True:
        ret, frame = camera.read()
        if ret:
            cv2.imshow('Камера', frame)
            cv2.waitKey(1)
        if not camReady:
            print("CamReady = True")
            camReady = True

async def main():
    global camReady, frame
    print("Запуск камеры...")
    asyncio.create_task(camera_loader())
    await worker2.Create_Tasks()
    while not camReady:
        print("Ожидание камеры...")
        await asyncio.sleep(0.2)

    while True:
        # Процесс распознавания лиц с использованием текущего кадра
        ID = await worker2.Qest(frame)
        # process_images(frame)
        print("Полученный ID:", ID)
        # Можно добавить функцию для распознавания голоса
        if ID:
            print("Голосовой ввод")
            voice_input = record_and_recognize_audio()
            if voice_input:
                print(f"Распознана голосовая команда: {voice_input}")
        else:
            print("Чела нет на фото")
        await asyncio.sleep(1)  # Добавляем задержку, чтобы не перегружать процессор

if __name__ == '__main__':
    asyncio.run(main())
"""
