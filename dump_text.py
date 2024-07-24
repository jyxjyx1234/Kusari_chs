import re
import json
import os
from SDT_file import *

ori_folder = "scn\\"
out_folder = "ori_text_json\\"

filelist = os.listdir(ori_folder)

for file in filelist:
    print(file)
    # 解析：文本格式为 \xb8\x00(1字节，标识长度)\x00（文本）
    # 其中，人名格式为\x3c\x4e(人名)\x3e,在文本开头
    f_data = open(ori_folder + file, "rb").read()
    f = SDTFile(f_data)
    out_json = f.find_text()

    '''
    for i in range(len(out_json)):
        try:
            m = out_json[i]['message']
        except:
            print(out_json[i])
            print(i)
            exit()
        m = m.replace('<R',"")
        out_json[i]['message'] = re.sub(r'\|.+?>',"",m)
    '''
    save_json(out_folder + file.replace(".SDT", ".json"), out_json)
