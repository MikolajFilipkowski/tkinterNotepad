#from tkinter import *
from tkinter import Tk, Menu, Scrollbar, Frame, BOTH, LEFT, RIGHT, BOTTOM, TOP, HORIZONTAL, VERTICAL, NONE, INSERT, X, Y
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from uuid import uuid4
from codecs import decode


#win.minsize(width=50, height=50)


bfont = {'family':'Lucida Console', 'weight': 'bold', 'size': 20}

def extractFile(file_dict:dict):
    file_name=''
    file_path=''
    if (file_dict['file_path'].find('/')):
        file_name=file_dict['file_path'][::-1].split("/")[0][::-1]
        file_path=file_dict['file_path'].strip(file_dict['file_path'][::-1].split("/")[0][::-1])
    else:
        file_name=file_dict['file_path']
        file_path=None
    return {'file_name':file_name, 'file_path':file_path}

class App:
    def __init__(self):
        self.__win = Tk()
        self.__win.geometry('400x300')
        self.__win.title("Notatnik")
        self.__open_files = []
        self.__notebook = ttk.Notebook(self.__win)
        self.__notebook.pack(fill=BOTH, side=LEFT, expand=True)
    @property
    def win(self) -> Tk:
        return self.__win
    @property
    def open_files(self) -> dict:
        return self.__open_files
    @property
    def notebook(self) -> ttk.Notebook:
        return self.__notebook
    @open_files.setter
    def open_files(self,open_files):
        self.__open_files = open_files
    @staticmethod
    def extractPath(ioin:str):
        ioout = str(ioin)

        getridofme ="<_io.TextIOWrapper name='"
        getridofme2 ="' mode='w' encoding='cp1250'>"
        getridofme3 ="' mode='r' encoding='cp1250'>"

        ioout = ioout.replace(getridofme, "")
        ioout = ioout.replace(getridofme2, "")
        ioout = ioout.replace(getridofme3, "")

        return ioout
    def getOpenFiles(self):
        for k,v in enumerate(self.open_files):
            print(f'Plik {k+1}: {v.getFileInfo()}')
    def findFile(self,file):
        for v in self.open_files:
            if (self.notebook.nametowidget(file)==v.frame):
                return v
        return None
    def createFrame(self,fullFile='untitled',text=''):
        textFrame = TextFrame(self,fullFile,text)
        self.__open_files+=[textFrame.file]
    def createNewFile(self,*args):
        self.createFrame()
    def openFile(self,*args):
        f = filedialog.askopenfile(filetypes=(
            ('Text', '*.txt'),
            ('All files', '*.*')
        ),defaultextension='.txt')
        text=''
        if (f is None): return
        with open(self.extractPath(f),'r',encoding='UTF-8') as my_file:
            for i in my_file.readlines():
                text+=f"{i}\n"
            else: 
                text = text.rstrip('\n')
        self.createFrame(f.name,text)
    def saveFile(self,*args):
        selected = self.notebook.select()
        file = self.findFile(selected)
        if (file == None): return
        file.saveFile()
    def askSave(self,file):
        message = messagebox.askyesnocancel(title='Notatnik',message=f'Czy chcesz zapisac plik {file.file_name}')
        if (message==True):
            file.saveFile()
            file.deleteFile()
        elif (message==False):
            file.deleteFile()
        return message
    def closeCurFile(self,*args):
        selected = self.notebook.select()
        if (selected == None): return
        file = self.findFile(selected)
        if (file == None): return
        self.askSave(file)
    def onTabChange(self,*args):
        selected = self.notebook.select()
        if (selected == None): return
        file = self.findFile(selected)
        if (file == None): return
        self.win.title(f"Notatnik - {file.file_name}")
    def exitApp(self,*args):
        quit(0)
    def buildApp(self):
        menubar=Menu(self.win)
        self.__win.config(menu=menubar)
        file_menu = Menu(menubar,tearoff=0)
        menubar.add_cascade(label='File',menu=file_menu)
        file_menu.add_command(label='New', command=self.createFrame, accelerator="Ctrl+N")
        file_menu.add_command(label='Open', command=self.openFile, accelerator="Ctrl+O")
        file_menu.add_command(label='Save', command=self.saveFile, accelerator="Ctrl+S")
        file_menu.add_command(label='Close', command=self.closeCurFile, accelerator="Ctrl+F4")
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.exitApp, accelerator='Alt+F4')

        edit_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Edit', menu=edit_menu)
        edit_menu.add_checkbutton(label='jd')

        self.win.bind('<Control-n>', self.createNewFile)
        self.win.bind('<Control-o>', self.openFile)
        self.win.bind('<Control-s>', self.saveFile)
        self.win.bind('<Control-F4>', self.closeCurFile)
        self.win.bind('<Alt-F4>', self.exitApp)

        self.notebook.bind("<<NotebookTabChanged>>", self.onTabChange)
        self.win.mainloop()

class File:
    def __init__(self,file_dict:dict,app:App):
        self.__id = str(uuid4())
        self.__frame = file_dict['file']
        self.__file_name = extractFile(file_dict)['file_name']
        self.__file_path = extractFile(file_dict)['file_path']
        self.__app = app
    @property
    def id(self) -> str:
        return self.__id
    @property
    def file_name(self) -> str:
        return self.__file_name
    @property
    def file_path(self) -> str:
        return self.__file_path
    @property
    def frame(self) -> Frame:
        return self.__frame
    @property
    def app(self) -> App:
        return self.__app
    @file_name.setter
    def file_name(self,value):
        conValue=extractFile({'file_path':value})['file_name']
        self.__file_name=conValue
        text=self.frame.winfo_children()[0].winfo_children()[1].get('1.0','end')

        frame1=Frame(self.app.notebook)
        textbox = ScrolledText(master=frame1, width=1, height=1,wrap=NONE)
        textbox.pack(fill=BOTH, side=TOP,expand=True)
        scrollbar = Scrollbar(master=frame1,orient=HORIZONTAL,takefocus=0,command=textbox.xview)
        scrollbar.pack(fill=X,side=BOTTOM)
        textbox.config(xscrollcommand=scrollbar.set,font=bfont)
        textbox.insert(INSERT,text)
        index=self.app.notebook.index(self.frame)
        maxIndex=self.app.notebook.index('end')-1
        self.app.notebook.forget(self.app.notebook.index(self.frame))
        if (index==0 or index==maxIndex):
            self.app.notebook.add(frame1,text=f'{conValue}')
        else:
            self.app.notebook.insert(index,frame1,text=f'{conValue}')
        self.app.notebook.select(index)
        self.app.win.title(f"Notatnik - {conValue}")
        self.frame=frame1
    @file_path.setter
    def file_path(self,value):
        self.__file_path=value
    @frame.setter
    def frame(self,value):
        self.__frame=value
    def __repr__(self):
        id=self.id
        file_name=self.file_name
        file_path=self.file_path
        frame=self.frame
        return f'{id =}, {file_name =}, {file_path =}, {frame =}'
    def deleteFile(self):
        self.app.notebook.forget(self.app.notebook.index(self.frame))
        new_open_files = []
        for i in self.app.open_files:
            if (not i==self):
                new_open_files +=[i]
        self.app.open_files=new_open_files
    def saveFile(self):
        createdFile = filedialog.asksaveasfile(initialdir=self.file_path,initialfile=self.file_name, filetypes=(
            ('Text','*.txt'),
            ('All files','*.*')
        ), defaultextension='.txt')
        if (createdFile is None): return
        createdFile = App.extractPath(createdFile)
        with open(createdFile,'w',encoding='utf8') as my_file:
            text = self.frame.winfo_children()[0].winfo_children()[1].get('1.0','end')
            my_file.write(text)
        self.file_name=extractFile({'file_path':createdFile})['file_name']
        self.file_path=extractFile({'file_path':createdFile})['file_path']

class TextFrame:
    def __init__(self,appInstance:App,fullFilePath:str,text:str):
        frame1=Frame(appInstance.notebook)
        textbox = ScrolledText(master=frame1, width=1, height=1,wrap=NONE)
        textbox.pack(fill=BOTH, side=TOP,expand=True)
        scrollbar = Scrollbar(master=frame1,orient=HORIZONTAL,takefocus=0,command=textbox.xview)
        scrollbar.pack(fill=X,side=BOTTOM)
        textbox.config(xscrollcommand=scrollbar.set,font=bfont)
        textbox.insert(INSERT,text)
        file_name=extractFile({'file_path':fullFilePath})['file_name']
        appInstance.notebook.add(frame1,text=f'{file_name}')
        appInstance.notebook.select(appInstance.notebook.index(frame1))
        newFile = File({'file':frame1,'file_path':fullFilePath},appInstance)
        appInstance.win.title(f"Notatnik - {file_name}")
        appInstance.open_files+=[newFile]
        self.__appInstance = appInstance
        self.__textbox = textbox
        self.__scrollbar = scrollbar
        self.__file = newFile
    @property
    def file(self) -> File:
        return self.__file
    @property
    def appInstance(self) -> App:
        return self.__appInstance
    @property
    def frame(self) -> Frame:
        return self.file.frame
    @property
    def textbox(self) -> ScrolledText:
        return self.__textbox
    @property
    def text(self) -> str:
        return self.textbox.get('1.0','end')
    @property
    def scrollbar(self) -> Scrollbar:
        return self.__scrollbar
    

App().buildApp()