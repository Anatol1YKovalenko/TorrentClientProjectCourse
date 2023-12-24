from installation_manager import Installation_MNG
from multiprocessing import Pipe
import threading,os

#Установочная форма
class InstallationForm:
    def __init__(install_form,head,torrent,id):
        install_form.head = head
        install_form.name,_ = os.path.splitext(torrent.name)
        install_form.size = torrent.size
        install_form.id = id
        #Труба для обмена сообщениями между установочным процессорои и графическим интерфейсом
        install_form.to_head,install_form.from_install = Pipe()
        #Установочный процесс
        install_form.installation_mng = Installation_MNG(torrent,install_form.to_head)
        #Поток для изменения информации на экране
        install_form.updater_thread = threading.Thread(target=install_form.updater,daemon=True)

    #Размещение установочной формы на экран
    def pack_to_viewer(install_form):
        install_form.head.viewer.insert(parent="",index = "end",iid = install_form.id,
                           values = (install_form.name,install_form.size,"0.0%","Initializing...","0(0)","∞"),tags = ('tor')) 
        
    #Обновление установочной формы
    def updater(install_form):
        while True:
            #Получение информации от установки
            progress,status,peers,speed = install_form.from_install.recv()
            #Изменение информации об установки
            install_form.head.viewer.item(install_form.id,values=(install_form.name,install_form.size,progress,status,peers,speed))

    def begin(install_form):
        #Запустить поток обновляющий информацию на GUI
        install_form.updater_thread.start()
        #Запустить процесс начала установки
        install_form.installation_mng.start()
        