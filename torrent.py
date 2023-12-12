import bencode as ben,math,os   #Библиотека для бенкодирования(используется в метафайлах торрента)
from hurry.filesize import size,alternative
from enum import Enum


class Torrent: 
    #Типы файла
    class _Kinds_of_file(Enum):
       SINGLE_FILE,MULTIPLE_FILE = (0,1)
     
    
    def __init__(tr,file_path,name):
        #Путь до торрента
        tr.torrent_path = file_path
        #Имя торрента
        tr.name = name
        tr.file_names = []

    #Чтение метаданных с метафайла
    def read_Metafile(tr):
        #Открытие торрент-файла
        with open(tr.torrent_path,"rb") as torrent_file:
            #Чтение файла и декодирование бенкодинга
            tr.metainfo = ben.bdecode(torrent_file.read())
            #url-адресс трекера
            tr.announce = tr.metainfo['announce']
            #info - информация о файлах торрента, частях и их размеров
            tr.info = tr.metainfo['info']
            #piece length - размер одной части
            tr.piece_length = tr.info['piece length']
            #pieces - части файлов / файла
            tr.pieces = tr.info['pieces']
            if 'files' in tr.metainfo['info']:
                #Имя главной папки
                tr.file_name = tr.info['name']
                tr.files = tr.info['files']
                #Тип файловой системы
                tr.kind_file = Torrent._Kinds_of_file.MULTIPLE_FILE
                #Общий размер
                print(tr.files)
                tr.length = 0
                for file in tr.files:
                    tr.length += file['length']
            else:
                #Имя единственного файла
                tr.file_name = tr.info['name']
                #Тип файловой системы
                tr.kind_file = Torrent._Kinds_of_file.SINGLE_FILE
                #Размер файла
                tr.length = tr.info['length']
            tr.number_of_pieces = math.ceil(tr.length/tr.piece_length)
            #Представление размера файлов в красивом виде    
            tr.size =  size(tr.length,system=alternative)
    '''
    def init_files(tr):
        root = tr.metainfo['info']['name']

        if tr.kind_file == Torrent._Kinds_of_file.MULTIPLE_FILE:
            if not os.path.exists(root):
                os.mkdir(root, 0o0766 )

            for file in tr.files:
                path_file = os.path.join(root, *file["path"])

                if not os.path.exists(os.path.dirname(path_file)):
                    os.makedirs(os.path.dirname(path_file))

                tr.file_names.append({"path": path_file , "length": file["length"]})
                tr.total_length += file["length"]

        else: #SINGLE_FILE
            tr.file_names.append({"path": root , "length": tr.torrent_file['info']['length']})
            tr.total_length = tr.torrent_file['info']['length']
    '''            
           