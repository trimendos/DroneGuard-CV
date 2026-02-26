# src/video_stream.py
import threading
import time
from typing import Optional, Any

import cv2
import numpy as np


class VideoStream:
    """
    Клас для асинхронного захоплення відеопотоку з камери.
    Використовує окремий потік (Thread) для читання кадрів,
    щоб не блокувати основний цикл програми (AI Inference).
    """

    def __init__(self, src: int | str | Any = 0):
        # Перевіряємо, чи передали нам вже готовий об'єкт камери (Mock)
        # Ми перевіряємо наявність методу 'read', який є і у cv2.VideoCapture, і у нашого Mock
        if hasattr(src, "read") and hasattr(src, "release"):
            self.stream = src
            self.is_mock = True
        else:
            # Якщо це число або рядок — ініціалізуємо OpenCV
            self.stream = cv2.VideoCapture(src)
            self.is_mock = False
            if not self.stream.isOpened():
                raise ValueError(f"Не вдалося відкрити відеопотік: {src}")

        # Читаємо перший кадр
        self.grabbed, self.frame = self.stream.read()

        # Флаг для зупинки потоку
        self.stopped = False
        
        # Lock для безпечного доступу до кадру з різних потоків
        self.read_lock = threading.Lock()

    def start(self) -> "VideoStream":
        """Запускає потік для постійного читання кадрів."""
        threading.Thread(target=self._update, args=(), daemon=True).start()
        return self

    def _update(self) -> None:
        """Внутрішній метод потоку. Постійно читає нові кадри."""
        while not self.stopped:
            grabbed, frame = self.stream.read()
            
            # Блокуємо доступ до змінної, поки оновлюємо її
            with self.read_lock:
                self.grabbed = grabbed
                self.frame = frame

            # Якщо це Mock, йому не треба спати, він сам емулює затримку.
            # А от якщо це реальна камера і вона відвалилась — треба вийти.
            if not grabbed and not self.is_mock:
                self.stop()                

    def read(self) -> Optional[np.ndarray]:
        """Повертає останній зчитаний кадр."""
        with self.read_lock:
            if not self.grabbed:
                return None
            # Повертаємо копію кадру, щоб уникнути мутацій в основному потоці
            return self.frame.copy()

    def stop(self) -> None:
        """Зупиняє потік і звільняє ресурси камери."""
        self.stopped = True
        # Даємо потоку час на завершення
        time.sleep(0.1)
        self.stream.release()