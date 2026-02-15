import os
import platform
import subprocess
import time
import socket

class AdbManager:
    def __init__(self, resource_path, port="5111"):
        self.port = str(port)
        self.resource_path = resource_path
        self.adb_path = self.get_adb_path()

    def get_adb_path(self):
        system = platform.system()
        if system == "Windows":
            return self.resource_path("platform_tools/windows/adb.exe")
        elif system == "Darwin":
            return self.resource_path("platform_tools/mac/adb")
        else:
            return self.resource_path("platform_tools/linux/adb")

    def run(self, cmd):
        env = os.environ.copy()
        env["ADB_SERVER_PORT"] = self.port
        return subprocess.run(cmd, capture_output=True, text=True, env=env)

    def is_port_in_use(self, port):
        """检查端口是否被占用"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', port)) == 0

    def kill_adb_on_port(self):
        """杀掉占用 adb 的进程"""
        if platform.system() == "Windows":
            # Windows: 用 netstat 找 adb pid
            cmd = f'netstat -ano | findstr :{self.port}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            for line in result.stdout.strip().splitlines():
                parts = line.strip().split()
                pid = parts[-1]
                if pid.isdigit():
                    subprocess.run(f'taskkill /PID {pid} /F', shell=True)
        else:
            # macOS / Linux
            cmd = f'lsof -i:{self.port}'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            for line in result.stdout.strip().splitlines()[1:]:
                pid = line.split()[1]
                subprocess.run(["kill", "-9", pid])

    def start_server(self):
        # 先杀掉占用端口的 adb
        if self.is_port_in_use(int(self.port)):
            print(f"Port {self.port} in use, killing adb process...")
            self.kill_adb_on_port()
            time.sleep(0.5)

        # 再启动 adb server
        print("Starting adb server...")
        self.run([self.adb_path, "kill-server"])
        self.run([self.adb_path, "start-server"])
        time.sleep(1)

    def get_devices(self):
        result = self.run([self.adb_path, "devices"])
        print(result)
        lines = result.stdout.strip().split("\n")[1:]
        print(lines)
        return [l for l in lines if "device" in l]

    def activate_tcpip(self):
        print("Activating TCP/IP mode on 5555...")
        result = self.run([self.adb_path, "tcpip", "5555"])
        print(result)
        return "5555" in result.stdout