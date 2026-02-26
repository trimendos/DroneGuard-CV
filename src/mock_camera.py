# src/mock_camera.py
import time

import cv2
import numpy as np


class MockVideoCapture:
    """
    Імітація камери для розробки без фізичного пристрою.
    Генерує відеопотік з рухомим об'єктом.
    """

    def __init__(self, width=640, height=480, fps=30):
        self.width = width
        self.height = height
        # Емулюємо затримку реальної камери (наприклад, 33мс)
        self.delay = 1.0 / fps

        # Початкові координати "цілі"
        self.x, self.y = width // 2, height // 2
        self.dx, self.dy = 5, 5  # Швидкість руху

    def isOpened(self):
        return True

    def read(self):
        """Генерує один кадр."""
        # Емулюємо час, який камера витрачає на зйомку (Hardware Latency)
        time.sleep(self.delay)

        # Створюємо чорний фон
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        # Оновлюємо координати кола (щоб воно літало і відбивалось від стінок)
        self.x += self.dx
        self.y += self.dy

        # Відбивання від стінок
        if self.x <= 20 or self.x >= self.width - 20:
            self.dx *= -1
        if self.y <= 20 or self.y >= self.height - 20:
            self.dy *= -1

        # Малюємо зелене коло (наша "ціль")
        cv2.circle(frame, (self.x, self.y), 20, (0, 255, 0), -1)

        # Додаємо таймстемп, щоб бачити, що відео живе
        cv2.putText(frame, f"MOCK CAM: {time.time():.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        return True, frame

    def release(self):
        pass
