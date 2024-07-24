from Lib import *
from HanziReplacer import *
import os

trans_file_path = "trans_text_json\\"
trans_files = os.listdir(trans_file_path)

ori_file_path ="ori_text_json\\"

trans_out_path = "release\\trans.dat"
trans_out_file = open(trans_out_path,'w',encoding='sjis')
font_path = "MAINFONT.FNT"
font_out_path = "release\\MAINFONT.FNT"

trans_dict={}
nameset = []

print("正在读取译文……")
for _ in trans_files:
    trans_path = trans_file_path + _
    ori_path = ori_file_path + _

    trans_f = open_json(trans_path)
    ori_f = open_json(ori_path)

    for i in range(len(trans_f)):
        name = trans_f[i]['name']
        trans = trans_f[i]["post_zh_preview"]
        ID = trans_f[i]["index"]

        #对trans进行处理
        trans = replace_halfwidth_and_fullwidth(trans)
        trans = replace_halfwidth_with_fullwidth(trans)
        trans = trans.replace("“","＂").replace("”","＂")

        ori = ori_f[ID-1]['message']
        ori_ = re.sub(r'\|.+?>',"",ori).replace("<R","")
        while ori_ != trans_f[i]["pre_jp"]:
            ID += 1
            ori = ori_f[ID-1]['message']
            ori_ = re.sub(r'\|.+?>',"",ori).replace("<R","")
            

        if name!="":
            if name not in nameset:
                nameset.append(name)
            trans = f'<N{name}>{trans}'
            ori = f'<N{name}>{ori}'
        
        trans_dict[ori] = trans

print("正在生成字体……")
hanzireplacer = HanziReplacer()
hanzireplacer.ReadTransAndGetHanzidict([trans_dict,nameset])
hanzireplacer.ChangeFNTFont(font_path,font_out_path)

print("正在生成译文字典……")
for i in trans_dict:
    trans_ = hanzireplacer.hanzitihuan(trans_dict[i])
    trans_out_file.write(f"{i}={trans_}\n")
