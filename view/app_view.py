import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext

class AppView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.title("Game Watchdog")
        self.geometry("500x300")  # Tăng chiều rộng một chút cho đẹp hơn
        self.controller = controller

        self.window_var = tk.StringVar()
        self.exe_path = tk.StringVar()

        # --- Hàng chọn cửa sổ game và nút tải lại ---
        window_frame = ttk.Frame(self)
        window_frame.pack(pady=5, fill=tk.X, padx=10)

        ttk.Label(window_frame, text="Chọn cửa sổ game:").pack(side=tk.LEFT)
        self.window_combo = ttk.Combobox(window_frame, textvariable=self.window_var, width=30)
        self.window_combo['values'] = self.controller.get_window_list()
        self.window_combo.pack(side=tk.LEFT, padx=(5, 5))

        ttk.Button(window_frame, text="Tải lại", command=self.reload_windows).pack(side=tk.LEFT)

        # --- Hàng chọn file và nút Browse ---
        file_frame = ttk.Frame(self)
        file_frame.pack(pady=5, fill=tk.X, padx=10)

        ttk.Label(file_frame, text="Chọn file .exe:").pack(side=tk.LEFT)
        ttk.Entry(file_frame, textvariable=self.exe_path, width=30).pack(side=tk.LEFT, padx=(5, 5))
        ttk.Button(file_frame, text="Browse", command=self.browse_file).pack(side=tk.LEFT)

        # --- Nút bắt đầu ---
        ttk.Button(self, text="Bắt đầu theo dõi", command=self.start_monitoring).pack(pady=10)

        # --- Ô log ---
        self.log_box = scrolledtext.ScrolledText(self, width=60, height=8)
        self.log_box.pack(padx=10)

    def reload_windows(self):
        self.window_combo['values'] = self.controller.get_window_list()

    def browse_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.exe_path.set(path)

    def start_monitoring(self):
        title = self.window_var.get()
        exe = self.exe_path.get()
        if title and exe:
            self.controller.start_monitoring(title, exe)

    def ask_file_path(self):
        return filedialog.askopenfilename()

    def log(self, message):
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)
