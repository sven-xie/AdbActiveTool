from PySide6.QtCore import QThread, Signal

from adb_manager import AdbManager


class ActivateWorker(QThread):
    finished = Signal(bool, str)

    def __init__(self, resource_path):
        super().__init__()
        self.resource_path = resource_path

    def run(self):
        try:
            self.adb = AdbManager(self.resource_path)

            self.adb.start_server()
            devices = self.adb.get_devices()

            success = True
            message = "激活成功"

            if len(devices) == 0:
                success = False
                message = "未检测到设备"
                self.finished.emit(success, message)
                return

            if len(devices) > 1:
                success = False
                message = "检测到多台设备"
                self.finished.emit(success, message)
                return

            success = self.adb.activate_tcpip()

            if success:
                self.finished.emit(True, "ADB激活成功！")
            else:
                self.finished.emit(False, "ADB激活失败，请重试")


        except Exception as e:
            print(e)
            self.finished.emit(False, str(e))
