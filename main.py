import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import *
from Pmw import Balloon
import ctypes, os
from os import listdir
import pkg_resources
import subprocess
import webbrowser
import platform
import requests

ver = "1.0"
hasInternet = 1
getWinver = subprocess.run("reg query \"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\" /v \"CurrentBuild\"", shell=True, capture_output=True)
winver = ""
for i in str(getWinver.stdout):
    if i.isdigit():
        winver = winver + i
if int(winver) >= 22000:
    winver = "11"
else:
    winver = platform.release()

def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

if isAdmin():

    class MainApp:
        def __init__(self, window):
            self.window = window

            self.userlist = listdir("C:\\Users")
            self.userlist.remove("All Users")
            self.userlist.remove("Default User")
            self.userlist.remove("Default")
            self.userlist.remove("desktop.ini")
            self.userlist.remove("Public")

            try:
                r = requests.get("https://1.1.1.1/")
                hasInternet = 1
            except:
                hasInternet = 0
                self.updateCheck(onStart=True)

            self.menubar = tk.Menu(window)
            window.config(menu=self.menubar)

            editmenu = tk.Menu(self.menubar, tearoff=0)
            self.menubar.add_cascade(label="Edit", menu=editmenu)
            
            editmenu.add_command(label="Edit Sysprep Unattend file", command=self.openNotepad)

            infomenu = tk.Menu(self.menubar, tearoff=0)
            self.menubar.add_cascade(label="Info", menu=infomenu)

            infomenu.add_command(label="Check for update", command=lambda: self.updateCheck(onStart=False))
            infomenu.add_command(label="About app", command=self.infoBox)



            self.infoTxt = tk.Label(self.window, text="Make sure you're in audit mode for reliable results.")
            self.infoTxt.pack(pady=(3, 0), padx=15, anchor="w")
            self.infoTxt2 = tk.Label(self.window, text="Window may buffer when carrying out selected options,\nthis does not necessarily mean it has frozen or crashed.", fg="red")
            self.infoTxt2.pack(padx=15, anchor="w")

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
            self.checkbox7 = ttk.Checkbutton(self.window, text="Run sysprep when done", variable=self.checkbox7var, command=self.showSysprep)
            self.checkbox7.pack(pady=(8, 0), padx=15, anchor="w")
            tooltip = Balloon(self.window)
            tooltip.bind(self.checkbox7, "Run sysprep with the specified arguments when done with everything else")

            self.runBtn = ttk.Button(self.window, text="Run", command=self.run)
            self.runBtn.pack(pady=5)

            self.console = tk.Text(
                window,
                height = '20',
                width = window.winfo_reqwidth()
            )
            self.console.tag_configure("warning", foreground="red")
            self.console.insert("end", "Thirdprep 1.0 - Console log\n\n")
            self.console.config(state="disabled")
            self.console.pack(side="bottom")

        def showSysprep(self):
            if self.checkbox7var.get() == 1:
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
            elif self.checkbox7var.get() == 0:
                self.sysprepText.pack_forget()
                self.actionFrame.pack_forget()
                self.actionOptions.pack_forget()
                self.generalize.pack_forget()
                self.shutdownFrame.pack_forget()
                self.shutdownOptions.pack_forget()
        
        def run(self):
            self.stuffSelected=False
            if self.checkbox1var.get() == 1:
                self.console.config(state="normal")
                self.console.insert("end", "Running disk cleanup...\n")
                self.console.config(state="disabled")
                proc = subprocess.run("reg import DiskCleanupFlags.reg && cleanmgr /sagerun:1", shell=True, capture_output=True)
                self.stuffSelected=True
            if self.checkbox2var.get() == 1:
                self.console.config(state="normal")
                self.console.insert("end", "Clearing all system and user temp files...\n")
                self.console.config(state="disabled")
                proc = subprocess.run("del /S /Q \"C:\\Windows\\Temp\"", shell=True, capture_output=True)
                for user in self.userlist:
                    proc = subprocess.run(f"del /S /Q \"C:\\Users\\{user}\\AppData\\Local\\Temp\"", shell=True, capture_output=True)
                self.stuffSelected=True
            if self.checkbox3var.get() == 1:
                self.console.config(state="normal")
                self.console.insert("end", "Clearing all recycle bins...\n")
                self.console.config(state="disabled")
                proc = subprocess.run("rd /s /q C:\$Recycle.Bin && powershell -command \"Clear-RecycleBin -Force -ErrorAction SilentlyContinue\"", shell=True, capture_output=True)
                self.stuffSelected=True            
            if self.checkbox4var.get() == 1:
                self.console.config(state="normal")
                self.console.insert("end", "Shrinking installation...\n")
                self.console.config(state="disabled")
                proc = subprocess.Popen("cmd dism /online /cleanup-image /StartComponentCleanup", creationflags=subprocess.CREATE_NEW_CONSOLE)
                self.stuffSelected=True
            if self.checkbox5var.get() == 1:
                self.console.config(state="normal")
                self.console.insert("end", "Clearing prefetch...\n")
                self.console.config(state="disabled")
                proc = subprocess.run("del /S /Q \"C:\\Windows\\Prefetch\"", shell=True, capture_output=True)     
                self.stuffSelected=True           
            if self.checkbox6var.get() == 1:
                self.console.config(state="normal")
                self.console.insert("end", "Resetting resolution...\n")
                self.console.config(state="disabled")
                subprocess.run(f"nircmdc.exe setdisplay 1024 768 32")
                self.stuffSelected=True
            if self.checkbox7var.get() == 1:
                self.console.config(state="normal")
                self.console.insert("end", "Running sysprep...\n")
                self.console.config(state="disabled")
                command = "sysprep.exe "
                if self.selectedAction.get() == self.actionOptionsList[0]:
                    command += "/oobe "
                elif self.selectedAction.get() == self.actionOptionsList[1]:
                    command += "/audit "
                if self.generalizeVar.get() == 1:
                    command += "/generalize "
                if self.selShutdown.get() == self.shutdownOptionsList[0]:
                    command += "/quit"
                elif self.selShutdown.get() == self.shutdownOptionsList[1]:
                    command += "/reboot"
                elif self.selShutdown.get() == self.shutdownOptionsList[2]:
                    command += "/shutdown"
                proc = subprocess.run(command, shell=True, capture_output=True)
                self.stuffSelected=True
            if not self.stuffSelected:   
                self.console.config(state="normal")
                self.console.insert("end", "Must select options!\n\n")
                self.console.config(state="disabled")
            elif self.stuffSelected:
                self.console.config(state="normal")
                self.console.insert("end", "Completed\n\n")
                self.console.config(state="disabled")
        
        def openNotepad(self):
            subprocess.run(["notepad.exe", "C:\\Windows\\Panther\\unattend.xml"])

        def infoBox(self):
            IW = tk.Toplevel()
            IW.title("Application Info")
            IW.geometry('420x200')
            IW.resizable(False, False)
            label = tk.Label(IW, text=f"Thirdprep {ver}\nCreated by IveMalfunctioned\nPython version {platform.python_version()}\n{platform.system()} {winver} {platform.architecture()[0]}\nClick to copy", cursor="hand2")
            label.bind("<Button-1>", lambda e: self.copy(txt=f"Thirdprep version {ver}\nPython version {platform.python_version()}\n{platform.system()} {winver} {platform.architecture()[0]}"))
            label.pack(pady=15)
            glink = tk.Label(IW, text="GitHub", fg="#0368BA", cursor="hand2")
            glink.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/IveMalfunctioned"))
            glink.pack()
            slink = tk.Label(IW, text="Source code", fg="#0368BA", cursor="hand2")
            slink.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/IveMalfunctioned/Thirdprep"))
            slink.pack()
            dlink = tk.Label(IW, text="Discord", fg="#0368BA", cursor="hand2")
            dlink.bind("<Button-1>", lambda e: webbrowser.open_new("https://discord.gg/hzScjC9re6"))
            dlink.pack()
        
        def updateCheck(self, onStart):
            def throwError(self, onStart):
                if not onStart:
                    self.console.config(state="normal")
                    self.console.insert('end', "Couldn't check for update\n", 'warning')
                    self.console.config(state="disabled")
                else:
                    return
            try:
                response = requests.get("https://api.github.com/repos/IveMalfunctioned/Thirdprep/releases/latest")
            except:
                throwError(self, onStart)
                return
            Fver = ""
            charCount = 0
            for char in str(response.json()["name"]):
                if charCount == 0:
                    charCount += 1
                elif charCount > 0:
                    if charCount >= 4:
                        break
                    elif charCount < 4:
                        Fver = Fver + char
                        charCount += 1
            if float(Fver) > float(ver):
                if not onStart:
                    IW = tk.Toplevel()
                    IW.geometry('200x240')
                    IW.resizable(False, False)
                    IW.title("Update found")
                    frame = tk.Frame(IW)
                    label = tk.Label(frame, text=f"Update found!\nLatest: {response.json()['name']}\nCurrent: " + ver)
                    dlBtn = ttk.Button(frame, text="Download", command=lambda: webbrowser.open_new("https://github.com/IveMalfunctioned/Thirdprep/releases/latest"), style="NStyle.TButton")
                    noBtn = ttk.Button(frame, text="Cancel", command=IW.destroy, style="NStyle.TButton")
                    label.pack(pady=35)
                    frame.pack(fill="x")
                    dlBtn.pack(pady=5)
                    noBtn.pack()

                self.console.config(state="normal")
                self.console.insert('end', f"Application update found!\nLatest:  v{Fver}\nCurrent: v{ver}\n\n")
                self.console.config(state="disabled")
            elif float(ver) >= float(Fver):
                if not onStart:
                    IW = tk.Toplevel()
                    IW.geometry('200x240')
                    IW.resizable(False, False)
                    IW.title("Using latest version")
                    frame = tk.Frame(IW)
                    label = tk.Label(frame, text="You're using the\nlatest version: " + ver)
                    noBtn = ttk.Button(frame, text="Close", command=IW.destroy, style="NStyle.TButton")
                    label.pack(pady=40)
                    noBtn.pack()
                    frame.pack(fill="x")

    icon = pkg_resources.resource_filename(__name__, "icon.ico")

    window = tk.Tk()
    window.geometry('420x820')
    window.resizable(False, False)
    window.title("Thirdprep")
    window.iconbitmap(default=icon)
    main = MainApp(window)
    window.mainloop()

else:
    window = tk.Tk()
    window.geometry('350x100')
    window.resizable(False, False)
    window.title("Program needs admin privileges")
    icon = pkg_resources.resource_filename(__name__, "icon.ico")
    window.iconbitmap(default=icon)
    label = tk.Label(window, text="This program requires administrator privileges to run.\nPlease rerun the program as administrator and try again")
    label.pack()
    button = tk.Button(window, text="Exit", command=window.destroy)
    button.pack()
    window.mainloop()