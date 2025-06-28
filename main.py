ver = 2.0

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import *
from tkinter import font
from Pmw import Balloon
import ctypes, os
from os import listdir
import pkg_resources
import subprocess
import threading
import webbrowser
import platform
import requests
import sys

# This function returns a true or false value after determining if the application is run with administrator privileges using the ctypes library.
def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

# If the application was not ran with administrator privileges, display a window notifying the user of the privilege requirement, then exit.
if not isAdmin():
    window = tk.Tk()
    window.geometry('350x100')
    window.resizable(False, False)
    window.title("Program needs admin privileges")
    icon = pkg_resources.resource_filename(__name__, "icon.ico")
    window.iconbitmap(default=icon)
    label = tk.Label(window, text="This program requires administrator privileges to run.\nPlease rerun the program as administrator and try again")
    label.pack(pady=10)
    button = ttk.Button(window, text="Exit", command=window.destroy)
    button.pack()
    window.mainloop()
    sys.exit()

# Main application class
class MainApp:
    def start(self):
        self.window.mainloop()
    def __init__(self):
        # Initialize Application
        self.window = tk.Tk()
        self.window.geometry('420x810')
        self.window.resizable(False, True)
        self.window.title("Thirdprep")
        icon = pkg_resources.resource_filename(__name__, "icon.ico")
        self.window.iconbitmap(default=icon)

        # Check if user has internet
        internetCheck = threading.Thread(target=self.checkHasInternet)
        internetCheck.start()
        self.foundVersion=None        

        # Initialize Application Variables
        self.userlist = listdir("C:\\Users")
        self.userlist.remove("All Users")
        self.userlist.remove("Default User")
        self.userlist.remove("Default")
        self.userlist.remove("desktop.ini")
        self.userlist.remove("Public")
        self.userlist.remove(os.getlogin())

        self.sysprepShown=False

        # Initialize Menubar
        self.menubar = tk.Menu(self.window)
        self.window.config(menu=self.menubar)

        editmenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=editmenu)
        
        editmenu.add_command(label="Edit Sysprep Unattend file", command=self.openNotepad)

        infomenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Info", menu=infomenu)

        infomenu.add_command(label="Check for update", command=self.updateCheck)
        infomenu.add_command(label="About app", command=self.infoBox)

        # Main Application Elements

        # If system is in audit mode, display a message notifying the user that audit mode has been detected. If not, present them with a button which will reboot the system to audit mode.
        if self.checkAuditMode():
            self.infoTxt = tk.Label(self.window, text="Audit mode detected.")
            self.infoTxt.config(fg="green")
            self.infoTxt.pack(pady=(3,0), padx=15, anchor="w")
        else:
            self.infoTxt = tk.Label(self.window, text="Make sure you're in audit mode for reliable results.")
            self.enterAuditBtn = ttk.Button(self.window, text="Enter Audit Mode", command=self.enterAuditMode)
            self.infoTxt.pack(pady=(3, 0), padx=15, anchor="w")
            self.enterAuditBtn.pack()

        # Checkboxes for task options. When checked, each box sets its corresponding variable value to 1 (selected) or 0 (deselected3)
        # Each checkbox also has tooltips bound to it to give more information on what the task will do.
        # This section is purely for the visual display as well as their functionality of changing their corresponding variable values.

        self.checkbox1var = tk.IntVar()
        self.checkbox1 = ttk.Checkbutton(self.window, text="Run Disk Cleanup", variable=self.checkbox1var)
        self.checkbox1.pack(pady=(4, 0), padx=15, anchor="w")
        tooltip = Balloon(self.window)
        tooltip.bind(self.checkbox1, "Automatically run disk cleanup with all boxes selected (except \"Previous Windows installation(s)\") (This may take a while)")

        self.checkbox2var = tk.IntVar()
        self.checkbox2 = ttk.Checkbutton(self.window, text="Clear Temp", variable=self.checkbox2var)
        self.checkbox2.pack(pady=(8, 0), padx=15, anchor="w")
        tooltip = Balloon(self.window)
        tooltip.bind(self.checkbox2, "Clear system temporary files and all user temporary files (This may take a while)")

        self.checkbox3var = tk.IntVar()
        self.checkbox3 = ttk.Checkbutton(self.window, text="Clear Recycle Bin", variable=self.checkbox3var)
        self.checkbox3.pack(pady=(8, 0), padx=15, anchor="w")
        tooltip = Balloon(self.window)
        tooltip.bind(self.checkbox3, "Delete the files in all users' recycle bins")

        self.checkbox4var = tk.IntVar()
        self.checkbox4 = ttk.Checkbutton(self.window, text="Shrink Install", variable=self.checkbox4var)
        self.checkbox4.pack(pady=(8, 0), padx=15, anchor="w")
        tooltip = Balloon(self.window)
        tooltip.bind(self.checkbox4, "Clean up the WinSxS folder (Windows core components) (This will take a while)")

        self.checkbox5var = tk.IntVar()
        self.checkbox5 = ttk.Checkbutton(self.window, text="Clear Prefetch", variable=self.checkbox5var)
        self.checkbox5.pack(pady=(8, 0), padx=15, anchor="w")
        tooltip = Balloon(self.window)
        tooltip.bind(self.checkbox5, "Clear out the prefetch folder")            

        self.checkbox6var = tk.IntVar()
        self.checkbox6= ttk.Checkbutton(self.window, text="Reset resolution", variable=self.checkbox6var)
        self.checkbox6.pack(pady=(8, 0), padx=15, anchor="w")
        tooltip = Balloon(self.window)
        tooltip.bind(self.checkbox6, "Reset the resolution of the main display to 1024x768")

        self.checkbox7var = tk.IntVar()
        self.checkbox7= ttk.Checkbutton(self.window, text="Delete this application after completion", variable=self.checkbox7var)
        self.checkbox7.pack(pady=(8, 0), padx=15, anchor="w")
        tooltip = Balloon(self.window)
        tooltip.bind(self.checkbox7, "Delete the exe file of this application after all tasks have been executed") 

        # This checkbox shows a recreation of sysprep within the application when checked.

        self.checkbox8var = tk.IntVar()
        self.checkbox8 = ttk.Checkbutton(self.window, text="Run sysprep when done", variable=self.checkbox8var, command=self.showSysprep)
        self.checkbox8.pack(pady=(8, 0), padx=15, anchor="w")
        tooltip = Balloon(self.window)
        tooltip.bind(self.checkbox8, "Run sysprep with the specified arguments when done with everything else")

        self.runBtn = ttk.Button(self.window, text="Run", command=self.run)
        self.runBtn.pack(pady=5)

        # Application console which shows information to the user.

        self.console = tk.Text(
            self.window,
            height = '18',
            width = self.window.winfo_reqwidth()
        )

        # Display the application version and a note indicating that this is the console log. 

        self.console.tag_configure("warning", foreground="red")
        self.console.insert("end", f"Thirdprep {str(ver)} - Console log\n\n")
        self.console.config(state="disabled")
        self.console.pack(side="bottom")

        # Check for application updates
        self.updateCheck(onStart=True)

    # Check if Windows is in audit mode by querying a registry key. Slice the needed value to check from the string output then run a check and return the correct value.
    def checkAuditMode(self):
        proc = subprocess.run("reg query HKLM\SYSTEM\Setup\Status /v AuditBoot", shell=True, capture_output=True, text=True)
        if int(proc.stdout.split("\n")[2][-1]) > 1:
            return True
        else:
            return False

    # This function reboots the computer to audit mode. It first displays a confirmation window asking the user if they are sure they want to reboot, then runs the command prompt command to reboot to audit mode.
    def enterAuditMode(self):
        def proc():
            subprocess.run(r"%WINDIR%\System32\Sysprep\sysprep.exe /audit /reboot", shell=True, capture_output=True)
        IW = tk.Toplevel()
        IW.title("Are you sure?")
        IW.geometry('420x150')
        IW.resizable(False, False)
        label = tk.Label(IW, text="Are you sure you want to enter Audit mode?\nDoing so will restart your computer,\nso be sure to save your work.")
        label.pack(pady=15)
        enterAuditBtn=ttk.Button(IW, text="Enter Audit Mode", command=proc)
        enterAuditBtn.pack()
        
    # This function shows a recreation of sysprep within the application upon the corresponding checkbox being ticked.
    def showSysprep(self):
        if self.checkbox8var.get() == 1:
            self.runBtn.pack_forget()

            self.sysprepText = tk.Label(self.window, text="System Preparation Tool (Sysprep) prepares the machine for\nhardware independence and cleanup.", justify="left")
            self.sysprepText.pack(pady=6)

            self.actionFrame = ttk.LabelFrame(self.window, text="System Cleanup Action")
            self.actionFrame.pack(pady=10)

            self.actionOptionsList=["Enter System Out-of-Box Experience (OOBE)", "Enter System Audit Mode"]
            self.selectedAction=tk.StringVar()
            self.selectedAction.set(self.actionOptionsList[0])
            self.actionOptions = ttk.Combobox(self.actionFrame, textvariable=self.selectedAction, values=self.actionOptionsList, width=42, state="readonly")
            self.actionOptions.pack(padx=(8, 20))
            
            self.generalizeVar = tk.IntVar()
            self.generalize = ttk.Checkbutton(self.actionFrame, text="Generalize", variable=self.generalizeVar)
            self.generalize.pack(anchor="w", padx=20)
                            
            self.shutdownFrame = ttk.LabelFrame(self.window, text="Shutdown Options")
            self.shutdownFrame.pack(pady=10)

            self.shutdownOptionsList=["Quit","Reboot","Shutdown"]
            self.selShutdown = tk.StringVar()
            self.selShutdown.set(self.shutdownOptionsList[1])
            self.shutdownOptions = ttk.Combobox(self.shutdownFrame, textvariable=self.selShutdown, values=self.shutdownOptionsList, width=42, state="readonly")
            self.shutdownOptions.pack(padx=(8, 20), pady=(0, 8))

            self.runBtn.pack(pady=5)

            self.sysprepShown=True
        elif self.checkbox8var.get() == 0:
            self.sysprepText.pack_forget()
            self.actionFrame.pack_forget()
            self.actionOptions.pack_forget()
            self.generalize.pack_forget()
            self.shutdownFrame.pack_forget()
            self.shutdownOptions.pack_forget()
            self.sysprepShown=False
    
    # The main function to carry out the selected tasks.
    def run(self):        
        # Here each task is assigned its own function, apart from deleting the application after completion and running sysprep when done, as they must run asynchronously.
        def disk_cleanup():
            self.console.config(state="normal")
            self.console.insert("end", "Running disk cleanup...\n")
            self.console.config(state="disabled")
            subprocess.run(f"reg import {sys._MEIPASS}\\DiskCleanupFlags.reg && cleanmgr /sagerun:1", shell=True, capture_output=True, text=True)
        # Clear Temporary files
        # Remove all files/folders in C:\Windows\Temp, then remove all files/folders in every user (except current)'s temporary directory
        # then remove all files/folders in the current user's temporary directory
        # (except the application's working folder, deleting them will interfere with the application, and they are automatically removed upon the application closing) using a powershell script
        def clear_temp():
            self.console.config(state="normal")
            self.console.insert("end", "Clearing all system and user temp files...\n")
            self.console.config(state="disabled")
            subprocess.run("del /S /Q \"C:\\Windows\\Temp\" && powershell -WindowStyle Hidden -Command \"Get-ChildItem -Path 'C:\\Windows\\Temp' -Directory | Remove-Item -Recurse -Force\"", shell=True, capture_output=True)
            for user in self.userlist:
                subprocess.run(f"del /S /Q \"C:\\Users\\{user}\\AppData\\Local\\Temp\" && powershell -WindowStyle Hidden -Command \"Get-ChildItem -Path 'C:\\Windows\\Temp' -Directory | Remove-Item -Recurse -Force\"", shell=True, capture_output=True)

            temp=fr"C:\Users\{os.getlogin()}\AppData\Local\Temp"
            app_cwd=sys._MEIPASS

            ps_script = fr'''
            # Normalize and resolve long paths
            function Get-LongPath([string]$Path) {{
                $fs = Get-Item -LiteralPath $Path -Force
                return $fs.FullName.TrimEnd('\')
            }}

            $Target = Get-LongPath "{temp}"
            $Exclude = Get-LongPath "{app_cwd}"

            # Delete files
            Get-ChildItem -Path $Target -Recurse -Force |
                Where-Object {{
                    -not $_.PSIsContainer -and
                    ($_.FullName -notlike "$Exclude*")
                }} |
                ForEach-Object {{
                    Remove-Item -LiteralPath $_.FullName -Force -ErrorAction SilentlyContinue
                }}

            # Delete folders (bottom-up)
            Get-ChildItem -Path $Target -Recurse -Force -Directory |
                Sort-Object FullName -Descending |
                Where-Object {{
                    $_.FullName -notlike "$Exclude*"
                }} |
                ForEach-Object {{
                    Remove-Item -LiteralPath $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
                }}
            '''

            result = subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", "-"],
                input=ps_script,
                text=True,
                capture_output=True
            )

        def clear_bin():
            self.console.config(state="normal")
            self.console.insert("end", "Clearing all recycle bins...\n")
            self.console.config(state="disabled")
            subprocess.run("rd /s /q C:\$Recycle.Bin && powershell -WindowStyle Hidden -command \"Clear-RecycleBin -Force -ErrorAction SilentlyContinue\"", shell=True, capture_output=True)
        def shrink_install():
            self.console.config(state="normal")
            self.console.insert("end", "Shrinking installation...\n")
            self.console.config(state="disabled")
            subprocess.run("cmd /c dism /online /cleanup-image /StartComponentCleanup", creationflags=subprocess.CREATE_NEW_CONSOLE)
        def clear_prefetch():
            self.console.config(state="normal")
            self.console.insert("end", "Clearing prefetch...\n")
            self.console.config(state="disabled")
            subprocess.run("del /S /Q \"C:\\Windows\\Prefetch\" && powershell -WindowStyle Hidden -Command \"Get-ChildItem -Path 'C:\\Windows\\Prefetch' -Directory | Remove-Item -Recurse -Force\"", shell=True, capture_output=True)
        def reset_resolution():
            self.console.config(state="normal")
            self.console.insert("end", "Resetting resolution...\n")
            self.console.config(state="disabled")
            subprocess.run(f"{sys._MEIPASS}\\nircmdc.exe setdisplay 1024 768 32")
        
        # Check if each checkbox is ticked, and if it is, add its corresponding function to a master tasks list, and set self.stuffSelected to True.
        # self.stuffSelected must be True in order for the tasks to be carried out, otherwise the console displays a message notifying the user that they need to make a selection.
        tasks_list=[]
        if self.checkbox1var.get() == 1:
            tasks_list.append(disk_cleanup)
            self.stuffSelected=True
        if self.checkbox2var.get() == 1:
            tasks_list.append(clear_temp)
            self.stuffSelected=True
        if self.checkbox3var.get() == 1:
            tasks_list.append(clear_bin)
            self.stuffSelected=True
        if self.checkbox4var.get() == 1:
            tasks_list.append(shrink_install)
            self.stuffSelected=True
        if self.checkbox5var.get() == 1:
            tasks_list.append(clear_prefetch)
            self.stuffSelected=True
        if self.checkbox6var.get() == 1:
            tasks_list.append(reset_resolution)
            self.stuffSelected=True
        if self.checkbox7var.get() == 1 or self.checkbox8var.get() == 1: # Asynchronous tasks
                self.stuffSelected=True

        # The function which executes the tasks in the master tasks list. It is within its own separate function so it can be ran in a separate thread, as to not freeze the application upon task execution.
        def execute_tasks():
            # Disable all checkboxes and the run button while the tasks are being carried out, so they are not interfered with.
            self.checkbox1.config(state="disabled")
            self.checkbox2.config(state="disabled")
            self.checkbox3.config(state="disabled")
            self.checkbox4.config(state="disabled")
            self.checkbox5.config(state="disabled")
            self.checkbox6.config(state="disabled")
            self.checkbox7.config(state="disabled")
            self.checkbox8.config(state="disabled")
            self.runBtn.config(state="disabled")
            if self.sysprepShown:
                self.actionOptions.config(state="disabled")
                self.generalize.config(state="disabled")
                self.shutdownOptions.config(state="disabled")
            for task in tasks_list:
                task()
        

        if not self.stuffSelected:
            self.console.config(state="normal")
            self.console.insert("end", "Must select options!\n\n")
            self.console.config(state="disabled")

        elif self.stuffSelected:
            tasks=threading.Thread(target=execute_tasks)
            tasks.start()

            # This function is ran in another separate thread (to avoid the application freezing) which, upon completion of the synchronous tasks, will re-enable the checkboxes and run button,
            # as well as run the asynchronous tasks (if they have been selected)
            def on_complete():
                while tasks.is_alive():
                    pass
                self.console.config(state="normal")
                self.console.insert("end", "Completed\n\n")
                self.console.config(state="disabled")
                self.checkbox1.config(state="normal")
                self.checkbox2.config(state="normal")
                self.checkbox3.config(state="normal")
                self.checkbox4.config(state="normal")
                self.checkbox5.config(state="normal")
                self.checkbox6.config(state="normal")
                self.checkbox7.config(state="normal")
                self.checkbox8.config(state="normal")
                self.runBtn.config(state="normal")
                if self.sysprepShown:
                    self.actionOptions.config(state="normal")
                    self.generalize.config(state="normal")
                    self.shutdownOptions.config(state="normal")

                # Run sysprep
                if self.checkbox8var.get() == 1:
                    self.console.config(state="normal")
                    self.console.insert("end", "Running sysprep...\n")
                    self.console.config(state="disabled")
                    command = ["sysprep.exe"]
                    if self.selectedAction.get() == self.actionOptionsList[0]:
                        command.append("/oobe")
                    elif self.selectedAction.get() == self.actionOptionsList[1]:
                        command.append("/audit")
                    if self.generalizeVar.get() == 1:
                        command.append("/generalize")
                    if self.selShutdown.get() == self.shutdownOptionsList[0]:
                        command.append("/quit")
                    elif self.selShutdown.get() == self.shutdownOptionsList[1]:
                        command.append("/reboot")
                    elif self.selShutdown.get() == self.shutdownOptionsList[2]:
                        command.append("/shutdown")
                    thread=threading.Thread(target=lambda: subprocess.run(command, shell=True, capture_output=True, cwd=r"C:\Windows\System32\Sysprep"))
                    thread.start()

                # Application deletion. This is delayed so sysprep can be run before the application is deleted (if it is selected)
                if self.checkbox7var.get() == 1:
                    self.console.config(state="normal")
                    self.console.insert("end", "Deleting this application...\n")
                    self.console.config(state="disabled")
                    filename, cwd = self.getProcessAttributes()
                    subprocess.Popen(f"cmd /c timeout /t 2 && del /f /q \"{cwd}\\{filename}\"", creationflags=subprocess.CREATE_NO_WINDOW)
                    self.window.destroy()
                    sys.exit()
                    
            threading.Thread(target=on_complete, daemon=True).start()
        
    def getProcessAttributes(self):
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            return os.path.basename(sys.executable), os.path.dirname(sys.executable)
        else:
            # Running as a .py script
            return os.path.basename(__file__), os.path.dirname(os.path.abspath(__file__))            
    
    def openNotepad(self):
        subprocess.run(["notepad.exe", "C:\\Windows\\Panther\\unattend.xml"])

    # This function obtains which version of Windows the host is using using the platform libary.
    def getWindowsVersion(self):
        if int(platform.version().split(".")[-1]) >= 22000:
            return "11"
        else:
            return platform.release()
    
    # Copy text to the clipboard. This function is used in the "About app" window.
    def copy(self, txt):
        self.window.clipboard_clear()
        self.window.clipboard_append(txt)

    # This is the "About app" window. It displays obtained information about the application and the host, as well as resource links for this software. 
    def infoBox(self):
        winver=self.getWindowsVersion()
        IW = tk.Toplevel()
        IW.title("Application Info")
        IW.geometry('420x200')
        IW.resizable(False, False)
        label = tk.Label(IW, text=f"Thirdprep {str(ver)}\nCreated by IveMalfunctioned\nPython version {platform.python_version()}\n{platform.system()} {winver} {platform.architecture()[0]}\nClick to copy", cursor="hand2")
        label.bind("<Button-1>", lambda e: self.copy(txt=f"Thirdprep version {str(ver)}\nPython version {platform.python_version()}\n{platform.system()} {winver} {platform.architecture()[0]}"))
        label.pack(pady=15)
        glink = tk.Label(IW, text="GitHub", fg="#0368BA", cursor="hand2")
        glink.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/IveMalfunctioned"))
        glink.bind("<Enter>", lambda e: glink.config(font=font.Font(IW, size=9, underline=True, family='Segoe UI')))
        glink.bind("<Leave>", lambda e: glink.config(font=font.Font(IW, size=9, underline=False, family='Segoe UI')))
        glink.pack()
        slink = tk.Label(IW, text="Source code", fg="#0368BA", cursor="hand2")
        slink.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/IveMalfunctioned/Thirdprep"))
        slink.bind("<Enter>", lambda e: slink.config(font=font.Font(IW, size=9, underline=True, family='Segoe UI')))
        slink.bind("<Leave>", lambda e: slink.config(font=font.Font(IW, size=9, underline=False, family='Segoe UI')))
        slink.pack()
        dlink = tk.Label(IW, text="Discord", fg="#0368BA", cursor="hand2")
        dlink.bind("<Button-1>", lambda e: webbrowser.open_new("https://discord.gg/hzScjC9re6"))
        dlink.bind("<Enter>", lambda e: dlink.config(font=font.Font(IW, size=9, underline=True, family='Segoe UI')))
        dlink.bind("<Leave>", lambda e: dlink.config(font=font.Font(IW, size=9, underline=False, family='Segoe UI')))
        dlink.pack()
    
    # Check if the host machine has internet by sending out a simple request.
    def checkHasInternet(self):
        try:
            requests.get("https://1.1.1.1/")
            self.userHasInternet=True
        except:
            self.userHasInternet=False
    
    # Check for application updates. If it finds a new version, it saves it to the variable self.foundVersion to avoid having to send another request.
    # If there is not yet a value in self.foundVersion, it performs the update check functionality within a separate thread as to avoid freezing the application.
    def updateCheck(self, onStart=False):
        def doUpdateCheck(onStart=False):
            try:
                response = requests.get("https://api.github.com/repos/IveMalfunctioned/Thirdprep/releases/latest")
                self.foundVersion = float(response.json()["name"][2:5])
            except:
                if not onStart:
                    self.console.config(state="normal")
                    self.console.insert('end', "Couldn't check for update\n", 'warning')
                    self.console.config(state="disabled")
                return
            if self.foundVersion > ver:
                self.console.config(state="normal")
                self.console.insert('end', f"Application update found!\nLatest:  v{self.foundVersion}\nCurrent: v{str(ver)}\n\n")
                self.console.config(state="disabled")
        
        if self.foundVersion is None:
            self.updateCheckThread = threading.Thread(target=lambda: doUpdateCheck(onStart=onStart))
            self.updateCheckThread.start()
        
        # Display the window to show if there is a new release of the application or not.
        # This function is ran in a separate thread to avoid freezing the application. Upon the update check completing, it displays the box.
        def showUpdateWindow():
            while self.updateCheckThread.is_alive():
                pass
            if self.foundVersion > ver and onStart==False:
                IW = tk.Toplevel()
                IW.geometry('340x150')
                IW.resizable(False, False)
                IW.title("Update found")
                frame = tk.Frame(IW)
                label = tk.Label(frame, text=f"Update found!\nLatest: v{str(self.foundVersion)}\nCurrent: v{str(ver)}")
                dlBtn = ttk.Button(frame, text="Download", command=lambda: webbrowser.open_new("https://github.com/IveMalfunctioned/Thirdprep/releases/latest"), style="NStyle.TButton")
                noBtn = ttk.Button(frame, text="Cancel", command=IW.destroy, style="NStyle.TButton")
                label.pack(pady=20)
                frame.pack(fill="x")
                dlBtn.pack(pady=5, side="left", padx=(90,0))
                noBtn.pack(side="right", padx=(0,90))
                
            elif ver >= self.foundVersion and onStart==False:
                IW = tk.Toplevel()
                IW.geometry('340x150')
                IW.resizable(False, False)
                IW.title("Using latest version")
                frame = tk.Frame(IW)
                label = tk.Label(frame, text="You're using the\nlatest version: " + str(ver))
                noBtn = ttk.Button(frame, text="Close", command=IW.destroy, style="NStyle.TButton")
                label.pack(pady=25)
                noBtn.pack()
                frame.pack(fill="x")
        
        if self.foundVersion is not None:
            showUpdateThread = threading.Thread(target=showUpdateWindow)
            showUpdateThread.start()

# Create an instance of the application and start the main loop
application = MainApp()
application.start()