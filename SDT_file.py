from Lib import *
import re

class SDTFile():
    def __init__(self,data:bytes) -> None:
        self.head = data[0:4]
        self.size = data[4:8]
        self.body = data[8:]
        self._p = 0

    #压缩/解压缩相关方法

    #文本提取相关方法
    def _find_b8(self) -> int:
        #增加_p，直到self.body[_p] == \xb8,返回p或者-1（文件结尾）
        while self._p < len(self.body):
            if self.body[self._p] == 0xb8:
                if not re.match(rb'[\x81-\x9F\xE0-\xEF]',self.body[self._p-1:self._p]):
                    if self.body[self._p+1] == 0x00:
                        return self._p
            self._p += 1
        return -1
    
    def _find_c0(self) -> int:
        #增加_p，直到self.body[_p] == \xc0,返回p或者-1（文件结尾）
        while self._p < len(self.body):
            if self.body[self._p] == 0xc0:
                if not re.match(rb'[\x81-\x9F\xE0-\xEF]',self.body[self._p-1:self._p]):
                    return self._p
            self._p += 1
        return -1
    
    def _read(self,length:int) -> bytes:
        out = self.body[self._p:self._p+length]
        self._p += length
        return out
    
    def _process_text(self,text:bytes) ->dict:
        dic = {}
        m = re.match(rb'\x3C\x4E([\x00-\xff]*?)\x3E([\x00-\xff]*)',text)
        try:
            if m:
                dic['name'] = m[1].decode(encoding='sjis')
                dic['message'] = m[2].decode(encoding='sjis')
            else:
                dic['message'] = text.decode(encoding='sjis')
        except:
            print(text)
            return None
        return dic
    
    def find_text(self) -> list[dict]:
        out = []
        while self._find_b8()!=-1:
            self._read(2)
            l = int.from_bytes(self._read(1),'little')
            if l == 184:
                self._read(1)
                l = int.from_bytes(self._read(1),'little')
            self._read(1)
            text = self._read(l)

            d = self._process_text(text)
            if d != None:
                out.append(d)

            self._read(2)
        self._p = 0

        while self._find_c0()!=-1:
            self._read(2)
            l = int.from_bytes(self._read(1),'little')
            if l == 184:
                self._read(1)
                l = int.from_bytes(self._read(1),'little')
                text = self._read(l)
                self._read(2)
                continue
            text = self._read(l)

            d = self._process_text(text)
            if d != None:
                out.append(d)
            self._read(2)
        return out
        