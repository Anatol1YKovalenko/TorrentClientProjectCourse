import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from showinfo import winfoWindow
from installation_manager import Installation_MNG
from multiprocessing import Pipe
import threading

class InstallationForm:
    def __init__(install_form,head,torrent,id):
        install_form.head = head
        install_form.name = torrent.name
        install_form.size = torrent.size
        install_form.id = id
        install_form.to_head,install_form.from_install = Pipe()
        install_form.installation_mng = Installation_MNG(torrent,install_form.to_head)
        install_form.updater_thread = threading.Thread(target=install_form.updater)
        
    def updater(install_form):
        while True:
            progress,status,peers= install_form.from_install.recv()
            install_form.head.viewer.item(install_form.id,text = "",values=(install_form.name,install_form.size,progress,status,peers))

    def begin(install_form):
        install_form.updater_thread.start()
        install_form.installation_mng.start()
        

class HeadWindow(tk.Tk): #главное окно
    def __init__(head):
        super().__init__()    
        head.title('PirTorrent')
        head.sc_width = head.winfo_screenwidth()
        head.sc_height = head.winfo_screenheight()
        head.head_width = head.sc_width//2 + head.sc_width//4 #ширина главного окна
        head.head_height = head.sc_height//2 + head.sc_height//4 #высота главного окна
        head.geometry(f"{head.head_width}x{head.head_height}+{(head.sc_width - head.head_width)//2}+{(head.sc_height - head.head_height -100)//2}")
        head.iconbitmap("images/icon.ico")
        #Инициализация списка труб для передачи информации между процессами
        head.amount_of_installation = 0
        head.installation_form_list = {}
        head.torrent_list = []
        #Обзорщик установок
        head.number_of_torrent = 0
        head.frame_viewer = tk.Frame(head)
        head.viewer = ttk.Treeview(head.frame_viewer,show="headings")
        head.viewer.pack(fill=tk.BOTH,expand=True)
        head.fill_viewer_collums()
        head.frame_viewer.pack(fill=tk.BOTH,expand=True)
        #Установка панели инструментов
        head.set_tool_bar() 
        
    #Функция создания панели инструментов(Open|Edit|View)
    def set_tool_bar(head):
        #Функция открытия файловой системы и выбора файла
        def open_file_system(): 
            #Пользователь выбирает торрент файл
            head.target_torrent = fd.askopenfile(initialdir="C:\\",filetypes =[('Torrent Files', '*.torrent')]) 
            head.show_info_ab_file()

        #Инициализация панели инструментов (Open|Edit|View)
        main_menu = tk.Menu(head) 
        #Всплывающее окно для File
        file_menu = tk.Menu(tearoff=0)
        file_menu.add_command(label="Open...",command=open_file_system) #Open... открывает обзор файловой системы
        file_menu.add_command(label="Open url...")
        file_menu.add_separator()
        file_menu.add_command(label="Exit")
        #Инициализация(File|Edit|View) 
        main_menu.add_cascade(label="File",menu = file_menu)
        main_menu.add_cascade(label="Edit")
        main_menu.add_cascade(label="View")
        #Бинд на главное окно
        head.config(menu=main_menu)

    #Функция для вызова окна обзорщика файла
    #@param file_name - путь до файла выбранного пользователем
    def show_info_ab_file(head):
        #Jткрытия окна обзорщика файловой системы торрент файла
        # TODO: Реализовать проверку на дурака(пользователь добавляет один и тот же торрент несколько раз)(проверять части)
        if  head.target_torrent != None:
            head.torrent_show = winfoWindow(head) 
            head.check_user_action()
            

    #Проверка ответа пользователя     
    def check_user_action(head):  
        #Ожидание ответа пользователя
        head.wait_window(head.torrent_show)
        if head.torrent_show.state_of_answer == winfoWindow.__States_of_answer__.T_OPENED:
                #Добавление выбранного торрента в список торрентов 
                head.torrent_list.append(head.torrent_show.torrent) 
                #Инициализация и начала установки
                head.initalize_installation()
    
    #Инициализация и начала установки           
    def initalize_installation(head):
        torrent = head.torrent_list[-1]
        #Размещение строки в обзорщик установки
        id = len(head.torrent_list)
        head.viewer.insert(parent="",index = "end",iid = id,
                           values = (torrent.name,torrent.size,"0%","Downloading...","0(0)"))
        head.installation_form_list[id] = InstallationForm(head,torrent,id)
        head.installation_form_list[id].begin()

    #Обзорщик установо5к
    def fill_viewer_collums(head):
        columns =  ["Name","Size","Progress","Status","Peers"]
        head.viewer['columns'] = tuple(columns)
        head.viewer.column("#0")
        head.viewer.heading("#0")
        for inf in columns:
            #Инициализация столбцов
            head.viewer.column(inf,anchor = "w")
            #Инициализация строк
            head.viewer.heading(inf,text = inf,anchor = "w")
 

if __name__ == "__main__":
    window = HeadWindow()
    window.mainloop()