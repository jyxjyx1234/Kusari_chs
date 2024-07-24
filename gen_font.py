from PIL import Image, ImageDraw, ImageFont
import numpy as np

from PIL import Image, ImageDraw, ImageFont
import numpy as np

def draw_character(char, font_path='WenQuanYi.ttf', size=24):
    # 创建一个透明的图像
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 加载字体
    font = ImageFont.truetype(font_path, size-3)

    # 获取字符的尺寸
    bbox = draw.textbbox((0, 0), char, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # 计算居中位置
    x = (size - w) / 2
    y = 0

    # 绘制黑色描边
    for i in range(3):
        _ = 20
        draw.text((x-i, y-i), char, font=font, fill=(_ * i, _ * i, _ * i, 255))
        draw.text((x+i, y-i), char, font=font, fill=(_ * i, _ * i, _ * i, 255))
        draw.text((x-i, y+i), char, font=font, fill=(_ * i, _ * i, _ * i, 255))
        draw.text((x+i, y+i), char, font=font, fill=(_ * i, _ * i, _ * i, 255))

    # 绘制白色字符
    draw.text((x, y), char, font=font, fill=(255, 255, 255, 255))

    # 转换为numpy数组
    img_array = np.array(img)
    
    if __name__ =="__main__":
        img.show()

    # 创建结果列表
    result = []
    for row in img_array:
        for pixel in row:
            # 计算灰度值
            gray = int(0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2])
            alpha = pixel[3]
            result.append((gray, alpha))

    return result

def process_result(ori_bitmap):
    outbitmap = []
    for i in ori_bitmap:
        if i[1] == 255:
            outbitmap.append(int(i[0]/4))
        elif i[0] == 0 and i [1] == 0:
            outbitmap.append(0)
        else:
            outbitmap.append(80)
    return bytes(outbitmap)

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

if __name__ =="__main__":
    char = '折'
    font_path = 'wenquanyi.ttf'
    bitmap = draw_character(char, font_path)
