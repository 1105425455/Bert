import os
import pandas as pd


'''
通过 NLPCC2016KBQA 中的原始数据，构建用来训练NER的样本集合
构造NER训练集，实体序列标注，训练BERT+CRF
'''

data_dir = 'NLPCC2016KBQA'
file_name_list = ['train.txt','dev.txt','test.txt']

new_dir = '../data_/ner_data'
question = 'question'
triple = 'triple'
for file_name in file_name_list:
    ner_list = []
    ner_tag_list = []
    file_path_name = os.path.join(data_dir,file_name)
    assert os.path.exists(file_path_name)
    with open(file_path_name,'r',encoding='utf-8') as f:
        for line in f:
            if question in line:
                q_str = line.strip()
            if triple in line:
                t_str = line.strip()
            if "====" in line: #分隔符
                q_str = q_str.split(">")[1].replace(" ", "").strip()
                entities = t_str.split("|||")[0].split(">")[1].strip()
                if entities in q_str:
                    q_list = list(q_str)
                    ner_list.extend(q_list)
                    ner_list.extend([" "])
                    tag_list = ["O" for i in range(len(q_list))]
                    tag_start_index = q_str.find(entities)
                    for i in range(tag_start_index, tag_start_index + len(entities)):
                        if tag_start_index == i:
                            tag_list[i] = "B-LOC"
                        else:
                            tag_list[i] = "I-LOC"
                    ner_tag_list.extend(tag_list)
                    ner_tag_list.extend([" "])
                else:
                    pass
    ner_result = [str(q) + " " + tag for q, tag in zip(ner_list, ner_tag_list)]
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)

    with open(os.path.join(new_dir,file_name), "w", encoding='utf-8') as f:
        f.write("\n".join(ner_result))
    f.close()
print("Done!")