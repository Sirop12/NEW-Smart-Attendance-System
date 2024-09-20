

import multiprocessing
import face_recognition
import settings
import threading
from db import get_users
import time
import cv2

MyPrint = []
def preprocess_image(image, target_size=(1000, 1000)):
    return cv2.resize(image, target_size)

Verived_global = {"ID": -1,
                  "Name": "F",
                  "Path": "F",
                  "Verifed": True}
Users = []

TotalTreads = 0

frame_encodings = []

def PrintMy():
    global MyPrint
    while True:
        if len(MyPrint) > 0:
            print(MyPrint[0])
            MyPrint.pop(0)

def Create_Tread():
    global TotalTreads
    Number = settings.THREAD_COUNT
    TotalTreads = Number
    print("Go printer")
    threading.Thread(target=PrintMy, name=f"Printer", daemon=True).start()
    #threading.Thread(target=PrintMy,daemon=True,name=f"Printer").start()
    print(f"strat {Number} Thread")
    for i in range(Number):
        threading.Thread(target=Tread_new, args=[i], name=f"Photo verifed {i}", daemon=True).start()
        #threading.Thread(target=Tread_new,args=[i],daemon=True,name=f"Photo verifed {i}").start()
    print(f"strat {Number} Thread -> OK")
    
lock = threading.Lock()

def Qest(Frame):
    global Verived_global, frame_encodings, Users, MyPrint
    MyPrint.append(f"Запрос получен")
    start_time = time.time()

    with lock:
        frame_encodings = face_recognition.face_encodings(Frame)
    
    if len(frame_encodings) > 0:
        MyPrint.append("Лица закодированы, передача в потоки...")
        Users = get_users()
        Verived_global = {"ID": -1, "Name": "F", "Verifed": False}
        while not Verived_global["Verifed"]:
            pass
        MyPrint.append("Пользователь верифицирован:" + str(Verived_global["ID"]) + " " + str(Verived_global["Name"]))
        total_time = time.time() - start_time
        MyPrint.append(f"Обработка изображений завершена за {total_time:.2f} секунд.")
        time.sleep(0.2)
        if Verived_global["ID"] == -1:
            return None
        return Verived_global["ID"]
    else:
        MyPrint.append(f"Лица необнаружены, возврат None")
        return None
    

def Tread_new(Number):
    global TotalTreads, frame_encodings, Verived_global, MyPrint, Users
    MyPrint.append(f"Поток {Number}, запущен")
    while True:
        if not Verived_global["Verifed"]:
            #MyPrint.append(f"Поток {Number}, получил коды, начинаю проверку")
            
            for i in range(len(Users))[Number::TotalTreads]:
                User = Users[i]
                MyPrint.append(f"Поток {Number}, сравнение с " + str(User["PhotoPath"]))

                with lock:
                    #MyPrint.append(f"Поток {Number}, загрузка изображеия")
                    known_image = face_recognition.load_image_file(User["PhotoPath"])
                    known_image = preprocess_image(known_image)
                    #MyPrint.append(f"Поток {Number}, изображение загружено")
                    #MyPrint.append(f"Поток {Number}, выделение геометрии")
                    known_encodings = face_recognition.face_encodings(known_image)
                    
                #MyPrint.append(f"Поток {Number}, геометрия выделена")
                if len(known_encodings) == 0:
                    MyPrint.append(f"Поток {Number}: Не удалось извлечь лицо из " + str(User["PhotoPath"]) + ". Пропуск...")
                    continue
                
                #MyPrint.append(f"Поток {Number}, сравнение геометрий")
                result = face_recognition.compare_faces([known_encodings[0]], frame_encodings[0])

                #MyPrint.append(f"Поток {Number}, сравнение с " + str(User["PhotoPath"]) + " завершено")

                if result[0]:
                    MyPrint.append(f"Поток {Number}, ОК")
                    Verived_global["ID"] = User["ID"]
                    Verived_global["Name"] = User["Name"]
                    Verived_global["Verifed"] = True
                    break
                else:
                    if i == len(Users) - 1:
                        MyPrint.append(f"Поток {Number}, пользователь не зарегистрирован в системе")
                        Verived_global["ID"] = -1
                        Verived_global["Name"] = "F"
                        Verived_global["Verifed"] = True
                        break

                    #MyPrint.append(f"Поток {Number}, Пользователь не верифицирован, дальше")

























"""import multiprocessing
import face_recognition
import settings
import threading
from db import get_users
import time
from concurrent.futures import ThreadPoolExecutor
import asyncio

MyPrint = []

Verived_global = {"ID": -1,
                  "Name": "F",
                  "Path": "F",
                  "Verifed": True}
Users = []

TotalTreads = 0

frame_encodings = []
lock = threading.Lock()

def PrintMy():
    global MyPrint
    while True:
        if len(MyPrint) > 0:
            print(MyPrint[0])
            MyPrint.pop(0)

def Create_Tasks():
    global TotalTreads
    Number = settings.THREAD_COUNT
    TotalTreads = Number
    print("Go printer")
    threading.Thread(target=PrintMy, name=f"Printer", daemon=True).start()
    print(f"strat {Number} Thread")
    for i in range(Number):
        threading.Thread(target=Tread_new, args=[i], name=f"Photo verifed {i}", daemon=True).start()
    print(f"strat {Number} Thread -> OK")

async def Qest(Frame):
    global Verived_global
    global frame_encodings
    global Users
    global MyPrint
    MyPrint.append(f"Запрос получен")
    start_time = time.time()
    frame_encodings = face_recognition.face_encodings(Frame)
    if len(frame_encodings) > 0:
        MyPrint.append("Лица закодированы, передача в потоки...")
        Users = get_users()
        Verived_global = {"ID": -1,
                          "Name": "F",
                          "Verifed": False}
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor(max_workers=TotalTreads) as executor:
            futures = [loop.run_in_executor(executor, Tread_new, i) for i in range(TotalTreads)]
            await asyncio.gather(*futures)
        MyPrint.append("Пользователь верифицирован:" + str(Verived_global["ID"]) + " " + str(Verived_global["Name"]))
        total_time = time.time() - start_time
        MyPrint.append(f"Обработка изображений завершена за {total_time:.2f} секунд.")
        await asyncio.sleep(0.2)
        if Verived_global["ID"] == -1:
            return None
        return Verived_global["ID"]
    else:
        MyPrint.append(f"Лица необнаружены, возврат None")
        return None

def Tread_new(Number):
    global TotalTreads
    global frame_encodings
    global Verived_global
    global MyPrint
    global Users
    MyPrint.append(f"Поток {Number}, запущен")
    while True:
        if not Verived_global["Verifed"]:
            MyPrint.append(f"Поток {Number}, получил коды, начинаю проверку")

            for i in range(Number, len(Users), TotalTreads):
                User = Users[i]
                MyPrint.append(f"Поток {Number}, сравнение с " + str(User["PhotoPath"]))

                known_image = face_recognition.load_image_file(User["PhotoPath"])

                known_encodings = face_recognition.face_encodings(known_image)
                if len(known_encodings) == 0:
                    MyPrint.append(f"Поток {Number}: Не удалось извлечь лицо из " + str(User["PhotoPath"]) + ". Пропуск...")
                    continue
                result = face_recognition.compare_faces([known_encodings[0]], frame_encodings[0])

                MyPrint.append(f"Поток {Number}, сравнение с " + str(User["PhotoPath"]) + " завершено")

                if result[0]:
                    MyPrint.append(f"Поток {Number}, ОК")
                    with lock:
                        Verived_global["ID"] = User["ID"]
                        Verived_global["Name"] = User["Name"]
                        Verived_global["Verifed"] = True
                    break
                else:
                    if i == len(Users) - 1:
                        MyPrint.append(f"Поток {Number}, пользователь не зарегестрирован в системе")
                        with lock:
                            Verived_global["ID"] = -1
                            Verived_global["Name"] = "F"
                            Verived_global["Verifed"] = True
                        break

                    MyPrint.append(f"Поток {Number}, Пользователь не верифицирован, дальше")
"""
