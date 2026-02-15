
## ADB激活助手


打包：

Mac:
   pyinstaller --windowed --name AdbActiveTool --icon icon.icns --add-data "platform_tools:platform_tools" main.py
   
   
   
   
   
win:

pyinstaller --onefile --name AdbActiveTool \
            --add-data "platform_tools;platform_tools" \
            --icon icon.ico \
            main.py   