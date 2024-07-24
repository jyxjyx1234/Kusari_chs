#没搞清楚压缩算法，放弃
from Lib import *
import os

class PAK_file():
    def __init__(self) -> None:
        pass

    def load(self,data:bytes):
        self._p = 0
        self._head = data[0:4]
        self._file_num = data[4:8]
        self.file_num = from_bytes(self._file_num)
        self._data = data
        self._names = data[8:8+0x28*self.file_num]#存储文件信息的区域
        self.bodyoffset = 8+0x28*self.file_num
        self._body = data[self.bodyoffset:]

    def unpack(self,path:str) -> None:
        self._read_namebuffers()
        for file in self.namebuffers:
            filename = file.get_filename()
            offset = file.offset
            size = file.size
            file_ori_size = from_bytes(self._data[offset:offset+4])
            file_data = self._data[offset+4:offset+size]
            save_file_b(path+filename,file_data)

    def pack(self,ori_path:str,out_path:str,pack = 1) ->None:
        #pack为0时，不进行压缩，直接导入
        out_data = b'\x4c\x1c\x43\x00'
        files = os.listdir(ori_path)
        num = len(files)
        out_data += to_bytes(num,4)

        offset = 8+0x28*num
        
        filedatas = []
        for filename in files:
            filepath = ori_path +filename
            f_data = open_file_b(filepath)[4:]#去除文件标识
            ori_size:int = len(f_data) + 4
            if pack:
                f_data = self.yasuo(f_data)
            size:int = len(f_data) + 8 #namebuffer中的size包括了压缩后文件的大小，还包含了4字节的原大小标识+4字节文件标识
            namebuffer = NameBuffer()
            offset = namebuffer.gen_namebuffer(filename,pack,size,offset)#生成namebuffer并更新offset
            out_data += namebuffer.to_bytes()
            filedatas.append(to_bytes(ori_size,4) + b'\xFF\x4c\x00\x46' + f_data)
        out_data += b''.join(filedatas)
        save_file_b(out_path,out_data)


    def yasuo(data:bytes) -> bytes:
        return data

    def _read(self,length:int) -> bytes:
        out = self._data[self._p:self._p+length]
        self._p += length
        return out
    
    def _read_namebuffers(self):
        self.namebuffers:list[NameBuffer] = []
        self._p = 8
        for i in range(self.file_num):
            namebuffer = NameBuffer()
            namebuffer.load(self._read(0x28))
            self.namebuffers.append(namebuffer)
        self._p = 0


class NameBuffer():
    def __init__(self) -> None:
        pass

    def load(self,data:bytes)-> None:#从bytes导入
        self._name = data[:0x19]
        self._ispacked = data[0x19:0x20]
        self._size = data[0x20:0x24]
        self._offset = data[0x24:0x28]

        self.size = from_bytes(self._size)
        self.offset = from_bytes(self._offset)

    def get_filename(self) -> str:
        for i in range(0x19):
            if self._name[i]:
                name = self._name[:i+1]
        name = list(name)
        name = [i^0xff for i in name]
        name = bytes(name).decode(encoding='sjis')
        return name
    
    def gen_namebuffer(self,name:str,pack:int,size:int,offset:int) ->int:
        self.name = name
        name_ = list(name.encode(encoding='sjis'))
        name_ = bytes([i^0xff for i in name_])
        self._name = name_
        while len(self._name) < 0x1F:
            self._name += b'\x00'
        self._ispacked = to_bytes(pack,1)
        self._size = to_bytes(size,4)
        self._offset = to_bytes(offset,4)
        return offset+size

    def to_bytes(self) ->bytes:
        out = b''
        out += self._name
        out += self._ispacked
        out += self._size
        out += self._offset
        return out


#测试
if __name__ == '__main__':
    a = PAK_file()
    a.load(open_file_b('SCRIPT.PAK'))
    a.unpack('scn_\\')
    