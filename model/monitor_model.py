import pyautogui
import pygetwindow as gw
import psutil
import ctypes
from PIL import ImageChops
import time, threading, os
from PIL import ImageGrab

class MonitorModel:
    def __init__(self):
        self.last_screenshot = None
        self.monitoring = False

    def get_window_titles(self):
        return [w.title for w in gw.getWindowsWithTitle('') if w.title]

    def start_monitor(self, window_title, exe_path, log_callback):
        self.monitoring = True

        def monitor():
            log_callback("Bắt đầu theo dõi...")
            count = 0
            while self.monitoring:
                win = next((w for w in gw.getWindowsWithTitle(window_title) if w.title == window_title), None)
                if win:
                    bbox = (win.left, win.top, win.right, win.bottom)
                    screenshot = ImageGrab.grab(bbox)
                    if self.last_screenshot and self.compare_images(screenshot, self.last_screenshot):
                        if count <= 5 :
                            log_callback("Phát hiện treo! Đang khởi động lại...")
                            self.restart_process(window_title, exe_path,log_callback)
                            count +=1
                            time.sleep(5)
                        else:
                            log_callback("khởi động lại quá 5 lần...")
                            self.monitoring = False
                    self.last_screenshot = screenshot
                else:
                    log_callback("Không tìm thấy cửa sổ.")
                time.sleep(25)

        threading.Thread(target=monitor, daemon=True).start()

    def compare_images(self, img1, img2):
        diff = ImageChops.difference(img1, img2)
        return not diff.getbbox()
    
    def restart_process(self, window_title, exe_path,log_callback):
        win = next((w for w in gw.getWindowsWithTitle(window_title) if w.title == window_title), None)
        if win:
            try:
                hwnd = win._hWnd
                pid = ctypes.c_ulong()
                ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                proc = psutil.Process(pid.value)
                proc.kill()
                log_callback(f"Đã kill tiến trình PID={pid.value}")
            except Exception as e:
                log_callback(f"Lỗi khi kill tiến trình theo cửa sổ: {e}")
        else:
            print("Không tìm thấy cửa sổ để kill")

        time.sleep(5)
        os.startfile(exe_path)

