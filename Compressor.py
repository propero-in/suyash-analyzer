from PIL import Image
import os

def compress_images():
    cwd = os.getcwd()
    images = os.listdir(cwd+"/output/oversized_images")
    count = 0
    o_li = []
    for i in images:
        img = Image.open(cwd+"/output/oversized_images/"+i)
        if img.mode != "RGB":
            img = img.convert("RGB")
        w = img.width
        h = img.height
        img = img.resize((w, h), Image.ANTIALIAS)
        img.save(cwd+"/output/Compressed_Images/image"+str(count+1)+".jpeg")
        size = os.path.getsize(cwd+"/output/oversized_images/"+i)
        size_kb = int(size/1024)
        o_li.append(size_kb)
        count += 1
    saved_images = os.listdir(cwd+"/output/Compressed_Images")
    c = 0
    c_li = []
    for img in saved_images:
        img_size = os.path.getsize(cwd+"/output/Compressed_Images/"+img)
        img_size_kb = int(img_size/1024)
        c_li.append(img_size_kb)
        c += 1
    difference = sum(o_li) - sum(c_li)
    return difference