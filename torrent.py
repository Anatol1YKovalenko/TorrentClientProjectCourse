import bencode as ben   #Библиотека для бенкодирования(используется в метафайлах торрента)

class Torrent:
    #Типы файла
    class _Kinds_of_file:
        MULTIPLE_FILE,SINGLE_FILE = (0,1)
    

    def __init__(tr,file_path,name):
        tr.torrent_path = file_path
        tr.name = name
        
    def read_Metafile(tr):
        with open(tr.torrent_path,"rb") as torrent_file:
            tr.metainfo = ben.bdecode(torrent_file.read())
            tr.meta_keys = tr.metainfo.keys()

            tr.announce = tr.metainfo['announce']
            tr.info = tr.metainfo['info']
            tr.piece_length = tr.info['piece length']
            tr.pieces = tr.info['pieces']
            tr.name = tr.info['name']
            if 'files' in tr.metainfo['info']:
                tr.files = tr.info['files']
                tr.kind_file = Torrent._Kinds_of_file.MULTIPLE_FILE
                tr.length = 0
                for file in tr.files:
                    tr.length += file['length']
            else:
                tr.length = tr.info['length']
                tr.pieces = tr.info['pieces'] #!!!
                tr.kind_file = Torrent._Kinds_of_file.SINGLE_FILE
           
  
    
                    
           