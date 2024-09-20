import speech_recognition as sr
import time
import pygame
from settings import SOUND_PATH

# Инициализация Pygame для звуков
pygame.mixer.init()

# Функция для записи и распознавания речи
def record_and_recognize_audio():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone:
        print("Настройка шумоподавления...")
        recognizer.adjust_for_ambient_noise(microphone, duration=2)

        try:
            print("Слушаю...")
            audio = recognizer.listen(microphone, timeout=5)
        except sr.WaitTimeoutError:
            print("Проверьте микрофон!")
            pygame.mixer.music.load(SOUND_PATH + 'check_micro.mp3')
            pygame.mixer.music.play()
            time.sleep(2)
            return None

        try:
            print("Распознаю речь...")
            text = recognizer.recognize_google(audio, language="ru-RU")
            print(f"Распознано: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("Речь не распознана")
        except sr.RequestError:
            print("Ошибка соединения с интернетом")
