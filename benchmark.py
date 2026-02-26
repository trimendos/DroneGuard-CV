# benchmark.py
import time
import cv2
from src.video_stream import VideoStream
from src.mock_camera import MockVideoCapture  # Імпортуємо наш мок

# Імітація важкої роботи нейромережі (YOLO inference simulation)
INFERENCE_TIME = 0.03  # 30ms обробка

def heavy_processing():
    time.sleep(INFERENCE_TIME)

def run_sync_test(iterations=100):
    print(f"\n--- Запуск СИНХРОННОГО тесту ({iterations} кадрів) ---")
    # Використовуємо Mock замість реальної камери
    cap = MockVideoCapture(fps=30) 
    
    start_time = time.time()
    for _ in range(iterations):
        # 1. Читання (тут є штучна затримка 33мс всередині Mock)
        ret, frame = cap.read()
        if not ret: break
        
        # 2. Обробка (ще 30мс затримки)
        heavy_processing()
        
    end_time = time.time()
    cap.release()
    
    total_time = end_time - start_time
    fps = iterations / total_time
    print(f"Sync FPS: {fps:.2f}")
    return fps

def run_async_test(iterations=100):
    print(f"\n--- Запуск АСИНХРОННОГО тесту ({iterations} кадрів) ---")
    
    # Створюємо Mock і передаємо його в VideoStream
    mock_cam = MockVideoCapture(fps=30)
    stream = VideoStream(mock_cam).start()
    
    # Даємо потоку розігнатися
    time.sleep(1.0) 
    
    start_time = time.time()
    for _ in range(iterations):
        # 1. Читання (миттєво з пам'яті, бо потік вже прочитав кадр)
        frame = stream.read()
        
        # 2. Обробка (30мс)
        heavy_processing()
        
    end_time = time.time()
    stream.stop()
    
    total_time = end_time - start_time
    fps = iterations / total_time
    print(f"Async FPS: {fps:.2f}")
    return fps

if __name__ == "__main__":
    print("Починаємо бенчмарк на MOCK-камері...")
    try:
        sync_fps = run_sync_test()
        async_fps = run_async_test()
        
        improvement = ((async_fps - sync_fps) / sync_fps) * 100
        print(f"\nRESULT: Асинхронний підхід швидший на {improvement:.1f}%")
    except Exception as e:
        print(f"Помилка: {e}")