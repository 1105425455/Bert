# -*- coding: utf-8 -*-
import os
import pandas as pd
'''
将nlqcc的数据更新到数据库中
'''
new_dir = './DB_Data'
file_name = 'clean_triple.csv'
triple_list = []
for data_type in ["training", "testing"]:
    file = "./NLPCC2016KBQA/nlpcc-iccpol-2016.kbqa." + data_type + "-data"
    with open(file, 'r',encoding='utf-8') as f:
        q_str = ""
        t_str = ""
        a_str = ""
        for line in f:
            if 'question' in line:
                q_str = line.strip()
            if 'triple' in line:
                t_str = line.strip()
            if '=============' in line:  #new question answer triple
                entities = t_str.split("|||")[0].split(">")[1].strip()
                q_str = q_str.split(">")[1].replace(" ","").strip()
                if ''.join(entities.split(' ')) in q_str:
                    clean_triple = t_str.split(">")[1].replace('\t','').replace(" ","").strip().split("|||")
                    triple_list.append(clean_triple)
df = pd.DataFrame(triple_list, columns=["entity", "attribute", "answer"])
print(df)
print(df.info())
if not os.path.exists(new_dir):
    os.mkdir(new_dir)
new_file = os.path.join(new_dir,file_name)
df.to_csv(new_file, encoding='utf-8', index=False)