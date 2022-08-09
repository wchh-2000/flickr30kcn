from PIL import Image
from io import BytesIO
import base64
import csv,jsonlines
dir = '/mnt/datasets/multimodal/flickr30k-images/'
img_ids=set()
with open("test/flickr30k_cn_test.txt","r") as f:
    lines=f.readlines()
    #print(len(f.readlines()))#5000
with open('../test_imgs.tsv', 'wt') as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t')
    with jsonlines.open("../test_texts.jsonl",'w') as json:
        for id,line in enumerate(lines):
            if id %500 ==0:
                print(i)
            img_id, txt = line.split()            
            img_id =  img_id[:-6]
            Dict={"text_id":id,"text":txt,"image_ids":[img_id]}
            json.write(Dict)

            if img_id in img_ids:#已经存储过
                continue
            else:
                img_ids.add(img_id)
                img_pth = dir+img_id+'.jpg'
                img = Image.open(img_pth) # 访问图片路径
                #图片以base64格式存储到tsv文件中：
                img_buffer = BytesIO()
                img.save(img_buffer, format=img.format)
                byte_data = img_buffer.getvalue()
                base64_str = base64.b64encode(byte_data) 
                tsv_writer.writerow([img_id,base64_str])
            
# with open("train/flickr30k_cna_train.txt","r") as f:
#     print(len(f.readlines()))#148909
# with open("val/flickr30k_cna_val.txt","r") as f:
#     print(len(f.readlines()))#5000
