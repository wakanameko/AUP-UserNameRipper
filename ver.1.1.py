# -*- coding: utf-8 -*-
import os
import platform
import shutil
import PIL
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
from tkinter import filedialog
from PIL import ImageTk, Image
import webbrowser
import datetime

APPNAME = "AUP UserNameRipper"
DEVELOP = "wakanameko"
VERSION = "1.1"

print(APPNAME + " ver" + VERSION + " by " + DEVELOP)

ur = platform.uname()
print(ur.system)
print(ur.release)
print(ur.version)

if not ur.system == 'Windows':messagebox.showerror('Attention','Windows以外のPCでの実行は想定されていません。エラーが発生しても自己責任でお願いします。')

##############################
##  Setup environment
##############################
if not os.path.exists((os.path.dirname(__file__) + '\\Extracted')):
    os.makedirs((os.path.dirname(__file__) + '\\Extracted'))

UserNamePath = os.path.dirname(__file__) + '/UserData.txt'
if not (os.path.isfile(UserNamePath)):
    with open(UserNamePath, 'w') as UserData:
        UserData.write("Empty\n")

tempDataPath = os.path.dirname(__file__) + '/tempData.txt'
if not (os.path.isfile(tempDataPath)):
    with open(tempDataPath, 'w') as UserData:
        UserData.write("Empty\n")

##############################
##  Setup Main window
##############################
MainWindow = tk.Tk()
MainWindow.geometry('600x450')
MainWindow.resizable(width = False, height = False)
MainWindow.title(f"{APPNAME} | ver{VERSION} | Developed by {DEVELOP}")

# make menubar
MenuB = tk.Menu(MainWindow)
MainWindow.config(menu=MenuB)

# setup Raddio button
var = tk.IntVar()
var.set(0)

# Load images
if(os.path.isfile(os.path.dirname(__file__) + '\\images\\mainicon.png')):
    MainWindow.iconphoto(False, tk.PhotoImage(file = os.path.dirname(__file__) + '\\images\\mainicon.png'))
    img = ImageTk.PhotoImage(Image.open(os.path.dirname(__file__) + '\\images\\mainicon.png'))
    isMainIcon = True
else:
    messagebox.showerror('Attention','\\images\\mainicon.pngが見つかりません!')
    isMainIcon = False


#get image on the main window
class Application(tk.Frame):
    def drawLabelPngImg(self):
        global iswindowIcon
        if(os.path.isfile(os.path.dirname(__file__) + '\\images\\windowicon.png')):
            global pngImg
            pngImg = tk.PhotoImage(file = os.path.dirname(__file__) + '\\images\\windowicon.png')
            label = tk.Label(dlg_modeless, width=100,height=100,image=pngImg)
            label.pack()
            iswindowIcon = True
        else:
            iswindowIcon = False


#EVENTS
def OpenGitHub():
    webbrowser.open("https://github.com/wakanameko")

def exitAUP():
    exit()

def OpenBaseAUP():
    FileTypeAUP = [("プロジェクトファイル", "*.AUP"),("すべて", "*")]
    iFile = os.path.abspath(os.path.dirname(__file__))
    BaseAPUFilePath = filedialog.askopenfilename(filetype = FileTypeAUP, initialdir = iFile)
    Text_OpenedAUP.delete(0, tk.END)
    Text_OpenedAUP.insert(tk.END, BaseAPUFilePath)

def SaveEnterDatas():
    Text_baseAUP_get = (Text_OpenedAUP.get())
    SIF = open(os.path.dirname(__file__) + '/UserData.txt', 'w', encoding='UTF-8')
    SIF.write(f"baseAUP:{Text_baseAUP_get}\nFINISHPOINT")
    SIF.close()

def OpenEnterDatas():
    if (os.path.isfile(os.path.dirname(__file__) + '/UserData.txt')):
        UserInfo = open(os.path.dirname(__file__) + '/UserData.txt', "r")
    else:
        askRUOpenHistoryFile = messagebox.askyesno('Info','入力履歴が見つかりませんでした。入力履歴のファイルを参照しますか？')
        if askRUOpenHistoryFile == True:
            OpenHistoryFile = [("入力履歴(テキストファイル)", "*.txt"),("すべて", "*")]
            iFile = os.path.abspath(os.path.dirname(__file__))
            OpenedHistoryFileAddress = filedialog.askopenfilename(filetype = OpenHistoryFile, initialdir = iFile)
            UserInfo = open(OpenedHistoryFileAddress, "r")
    UserData = UserInfo.read()

    #Get AUP address
    startI = 'baseAUP:'
    endI = '\nFINISHPOINT'
    sOpenedAUPData = str(UserData)
    OpenedAUPData = sOpenedAUPData[sOpenedAUPData.find(startI)+len(startI):sOpenedAUPData.rfind(endI)]
    Text_OpenedAUP.delete(0, tk.END)
    Text_OpenedAUP.insert(tk.END, OpenedAUPData)    
    
def RunningExtract():
    # get the address of opened AUP file
    Text_OpenedAUP_get = (Text_OpenedAUP.get())         #Read All entries
    OpenedAUP = open(Text_OpenedAUP_get, "rb")          #open base AUP file
    shutil.copyfile(Text_OpenedAUP_get, (os.path.dirname(__file__) + '/tempData.txt'))
    OpenedAUP.close()                                   #close BaseAUP

    ##################
    # Extract!!
    ##################
    OpenedCopiedAUP = open((os.path.dirname(__file__) + '/tempData.txt'), "rb")
    ReadOpenedCopiedAUP = OpenedCopiedAUP.read()

    # get user name from .aup file path
    startI = "Users\\\\"
    endI = "\\\\"
    sOpenedAUPData = str(ReadOpenedCopiedAUP)
    # ExtractedName = sOpenedAUPData[sOpenedAUPData.find(startI)+len(startI):sOpenedAUPData.rfind(endI)]
    print(sOpenedAUPData[sOpenedAUPData.find(startI)+len(startI)])
    ExtractedName = sOpenedAUPData[sOpenedAUPData.find(startI)+len(startI):sOpenedAUPData.find(startI)+len(startI)+sOpenedAUPData.rfind(endI)]
    
    # get now time
    gettime = str(datetime.datetime.now())
    gettimeShitSpace = gettime.replace(' ', '_')
    gettimeShitCoron = gettimeShitSpace.replace(':', '-')
    print(gettimeShitCoron)

    # save extracted name
    fileName = (f"{(os.path.dirname(__file__))}/Extracted/{gettimeShitCoron}.txt")
    with open(fileName, mode='x', encoding='UTF-8') as SaveExtractedName:
        SaveExtractedName.write(ExtractedName)

    OpenedCopiedAUP.close()                                                                    #close Copied AUP
    
    # insert Extracted name into the textbox
    Text_ExtractedList.delete(0, tk.END)
    Text_ExtractedList.insert(tk.END, ExtractedName)
    

########################################


#MENUBER
menu_file = tk.Menu(MainWindow)
MenuB.add_cascade(label = f"{APPNAME}", menu = menu_file)
menu_file.add_command(label = 'AUPファイルを選択', command = OpenBaseAUP)
menu_file.add_separator()
menu_file.add_command(label = '実行', command = RunningExtract)
menu_file.add_separator()
menu_file.add_command(label = '入力履歴を開く', command = OpenEnterDatas)
menu_file.add_command(label = '入力履歴を保存', command = SaveEnterDatas)
menu_file.add_separator()
menu_file.add_command(label = '閉じる', command = exitAUP)

menu_Help = tk.Menu(MainWindow)
MenuB.add_cascade(label = "Help", menu = menu_Help)
menu_Help.add_command(label = "ver" + VERSION)
menu_Help.add_command(label = "Developed by " + DEVELOP)
menu_Help.add_separator()
menu_Help.add_command(label = 'GitHubを開く', command = OpenGitHub)

#WIDGETS
if isMainIcon == True:
    Label_icon = tk.Label(MainWindow, image = img)
Label_AppnameLavel = tk.Label(MainWindow, text = f"{APPNAME}", font = ("normal", 12, "bold"))

border=ttk.Separator(MainWindow,orient="horizontal")

Label_BaseAUP = tk.Label(MainWindow, text = "AUPファイルを選択:")
Text_OpenedAUP = tk.Entry(width=80)
Sepa1 = tk.Label(MainWindow, text = " ", font = ("normal", 3, "normal"))
Button_BaseAUP = tk.Button(MainWindow, text = "参照", command = OpenBaseAUP, width = 12)

Sepa2 = tk.Label(MainWindow, text = " ", font = ("normal", 3, "normal"))
Button_RUN = tk.Button(MainWindow, text = "実行", command = RunningExtract, width = 20)
Sepa3 = tk.Label(MainWindow, text = " ", font = ("normal", 3, "normal"))

border2=ttk.Separator(MainWindow,orient="horizontal")

Sepa4 = tk.Label(MainWindow, text = " ", font = ("normal", 3, "normal"))
Label_LatestLog = tk.Label(MainWindow, text = "実行結果:")
Text_ExtractedList = tk.Entry(width = 95)

########################################


#LAYOUTS
if isMainIcon == True:
    Label_icon.pack()
Label_AppnameLavel.pack()

border.pack(fill="both", padx=10, pady=5)

Label_BaseAUP.pack(anchor = tk.W, padx = 15, pady = 0)
Text_OpenedAUP.pack(anchor = tk.W, padx = 15, pady = 0)
Sepa1.pack(anchor = tk.W, padx = 1, pady = 0)
Button_BaseAUP.pack(anchor = tk.E, padx = 15, pady = 0)
Sepa2.pack(anchor = tk.W, padx = 1, pady = 0)
Button_RUN.pack(anchor = tk.N, padx = 1, pady = 0)
Sepa3.pack(anchor = tk.W, padx = 1, pady = 0)

border2.pack(fill="both", padx=10, pady=5)

Sepa4.pack(anchor = tk.W, padx = 1, pady = 0)
Label_LatestLog.pack(anchor = tk.W, padx = 15, pady = 0)
Text_ExtractedList.pack(anchor = tk.N, padx = 1, pady = 0)

########################################

MainWindow.mainloop()