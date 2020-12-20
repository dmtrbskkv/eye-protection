from threading import Thread
from tkinter import *
from notifypy import Notify
from time import sleep
import json

settingsDefault = {'timeIntervalValue': 10}
appStatus = True

try:
    f = open('./settings.json', 'r')
    settings = f.read()
    settings = json.loads(settings)
    f.close()
except FileNotFoundError:
    settings = settingsDefault

timeIntervalValue = int(settings["timeIntervalValue"])


def showAlert():
    global timeIntervalValue
    notification = Notify()
    notification.title = "ВНИМАНИЕ! Глазам нужно отдохнуть"
    notification.message = "Посмотрите в окно, поморгайте и просто дайте глазам отдохнуть"
    notification.icon = "./favicon.png"
    while appStatus:
        sleep(int(timeIntervalValue) * 60)
        if appStatus:
            notification.send()


def saveSettings():
    global settings
    file = open('settings.json', 'w')
    file.write(json.dumps(settings))
    file.close()


def startApplication():
    global timeIntervalValue

    def onClosingApp():
        global th2, th1, appStatus
        appStatus = False
        root.destroy()

    def saveAction(event):
        global timeIntervalValue
        timeInterval = intervalInput.get()
        if timeInterval.isdigit() != TRUE:
            intervalMessageError.configure(text='- Пожалуйста, введите целое число')
            return
        timeIntervalValue = timeInterval
        root.iconify()

        settings["timeIntervalValue"] = timeIntervalValue
        saveSettings()

    def setDefaultAction(event):
        global settings, settingsDefault, timeIntervalValue
        settings = settingsDefault
        saveSettings()
        timeIntervalValue = settingsDefault["timeIntervalValue"]
        intervalInput.configure(textvariable=StringVar(root, value=timeIntervalValue))

    root = Tk()
    root['bg'] = '#fafafa'
    root.title('EyesAlerter')
    root.geometry('480x120')
    root.resizable(width=False, height=False)

    homeFrame = Frame(root, bg='#fafafa')
    homeFrame.pack(fill=X)

    homeFrameInfo = Frame(root, bg='#fafafa', pady=8, padx=10)
    homeFrameInfo.pack(fill=X)

    homeFrameButtons = Frame(root, bg='#fafafa', pady=8, padx=10)
    homeFrameButtons.pack(fill=X, side=BOTTOM)

    intervalText1 = Label(homeFrameInfo, text='Показывать уведомление каждые: ', bg='#fafafa')
    intervalText1.grid(row=0)
    intervalInputPlaceholder = StringVar(root, value=timeIntervalValue)
    intervalInput = Entry(homeFrameInfo, width=4, textvariable=intervalInputPlaceholder)
    intervalInput.grid(row=0, column=1)
    intervalText2 = Label(homeFrameInfo, text=' мин', bg='#fafafa')
    intervalText2.grid(row=0, column=3)

    intervalMessageError = Label(homeFrameInfo, bg='#fafafa')
    intervalMessageError.grid(row=1, columnspan=3, sticky=W)

    saveButton = Button(homeFrameButtons, text='Сохранить', bg='#333', fg='#fafafa', bd=0, width=14, pady=8)
    saveButton.bind("<Button-1>", saveAction)
    saveButton.grid(row=0)
    setDefaultButton = Button(homeFrameButtons, text='Сбросить', bg='#333', fg='#fafafa', bd=0, width=14, pady=8)
    setDefaultButton.bind("<Button-1>", setDefaultAction)
    setDefaultButton.grid(row=0, column=1, padx=8)

    img = Image("photo", file="favicon.png")
    root.tk.call('wm', 'iconphoto', root._w, img)
    root.protocol("WM_DELETE_WINDOW", onClosingApp)
    root.mainloop()


th1 = Thread(target=showAlert, daemon=False)
th2 = Thread(target=startApplication, daemon=False)

th1.start()
th2.start()
