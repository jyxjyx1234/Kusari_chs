from Lib import *
from PIL import Image
def getoffset(cha):
    t = cha.encode(encoding='sjis')
    str1 = t[0]
    if len(t) == 2:
        str2 = t[1]
    orgSize = 24
    if str1<0x80:
        offset = ((str1-0x20)+189*43)*orgSize*orgSize
    elif str1>=0xA0 and str1<=0xDF:
        offset = ((str1-0x40)+189*43)*orgSize*orgSize
    else:
        if str1>=0xf0:
            str1 -= 0x45
        elif str1>=0xe0:
            str1 -= 0x40;
        offset = ((str1-0x81)*189 +(str2-0x40))*orgSize*orgSize;
    return offset

def getla(val):
    if val == 0:
        return 0,0
    elif val<=64:	
        bAlpha = 0xff
        l = int((val-1)*0xff/63)
        return l,bAlpha
    else:	
        bAlpha = int((val-65)*0xdb/63 +0x24)
        return 0,bAlpha

font = open_file_b('MAINFONT.FNT')

o = getoffset('友')
print(hex(o))
f_b = font[o:o+24*24]

# 创建一个新的灰度图像
img = Image.new('LA', (24, 24))

img_bytes=[]
for i in f_b:
    _ = getla(i)
    img_bytes.append(_[0])
    img_bytes.append(_[1])
img_bytes=bytes(img_bytes)
# 将字节数据直接应用到图像
img.frombytes(img_bytes)

# 放大图像以便更容易查看
img_resized = img.resize((240, 240), Image.NEAREST)

# 保存图像
img_resized.save('gray_output.png')

# 显示图像
img_resized.show()
