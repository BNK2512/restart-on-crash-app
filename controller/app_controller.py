from view.app_view import AppView
from model.monitor_model import MonitorModel

class AppController:
    def __init__(self):
        self.model = MonitorModel()
        self.view = AppView(self)

    def run(self):
        self.view.mainloop()

    def get_window_list(self):
        return self.model.get_window_titles()

    def start_monitoring(self, window_title, exe_path):
        self.model.start_monitor(window_title, exe_path, self.view.log)

    def browse_exe_path(self):
        return self.view.ask_file_path()
