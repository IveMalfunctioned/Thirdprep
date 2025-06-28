# Thirdprep
Thirdprep is a GUI based tool for Windows made in Python using the Tkinter library. Its purpose is to serve as an easy to use application to prepare a Windows 10 or 11 installation for image capture.

# Screenshot
![image](https://github.com/user-attachments/assets/85d1e511-cb18-4718-a41d-13fc8e0f83ed)

# Usage / download

In order to use this program, download one of the precompiled binaries from the [releases tab](https://github.com/IveMalfunctioned/Thirdprep/releases/latest) or compile it using [PyInstaller](https://pyinstaller.org/en/stable/). This application requires the installation of the [Pmw](https://pypi.org/project/Pmw/) library.

To compile, type this command and replace your username (or change the path to the Pmw library)

```pyinstaller --onefile --icon=icon.ico --name=Thirdprep --add-data "DiskCleanupFlags.reg:." --add-data "icon.ico:." --add-data "nircmdc.exe:." --add-data "C:\Users\(your username)\AppData\Local\Programs\Python\Python311\Lib\site-packages\Pmw;Pmw" --hidden-import=Pmw --uac-admin --clean --noconfirm --noconsole main.py```

The program requires administrative privileges to run, so make sure you right click the exe and click "Run as administrator".

Check the boxes with the options you want the program to execute upon running the script, and the application will carry them out.
There is also an option under the "Edit" tab to open the unattend.xml file in Notepad.

For more direct information or updates on the project, join the [Windows Modding Discord](https://discord.gg/hzScjC9re6)
