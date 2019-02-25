import requests
import os
from PIL import Image as img
import numpy as np
import time
import time
import chaojiying
import shutil
def downloadNewCaptcha():
    if not os.path.exists('./dataset1/'):
        os.mkdir('./dataset1/')
    if not os.path.exists('./dataset1/raw'):
        os.mkdir('./dataset1/raw')
    s = requests.Session()
    for i in range(5000):
        content = s.get('http://navi.cnki.net/knavi/Home/GetImg').content
        with open('./dataset1/raw/'+str(i)+'.jpg', 'wb') as f :
            f.write(content)
    # with Image.open('./dataset1/train/'+str(i)+'.jpg') as img:
    #     img = img.convert('1')
    #     img.save('./dataset1/train/'+str(i)+'.jpg')
def processCaptcha():
    for k in range(5000):
        pic = img.open('./dataset1/train/'+str(k)+'.jpg')
        pic = pic.convert('L')
        pic = np.array(pic)
        pic = pic.reshape(1, 3740)[0]
        pic_array = []
        for i in pic:
            if i >180:
                pic_array.append(256)
            else:
                pic_array.append(0)
        pic_array = np.array(pic_array).reshape(34,110)
        pic1=[]
        count =0
        for i in pic_array:
            pic1.append(i[85:107])
        pic_temp = img.fromarray(np.array(pic1)).convert('1')
        pic_temp.save('./processed/'+str(k)+'_'+str(count)+'.png')
        count += 1
        pic1=[]
        for i in pic_array:
            pic1.append(i[61:83])
        pic_temp = img.fromarray(np.array(pic1)).convert('1')
        pic_temp.save('./processed/'+str(k)+'_'+str(count)+'.png')
        count += 1
        pic1=[]
        for i in pic_array:
            pic1.append(i[8:30])
        pic_temp = img.fromarray(np.array(pic1)).convert('1')
        pic_temp.save('./processed/'+str(k)+'_'+str(count)+'.png')
        count += 1
        pic1=[]
        for i in pic_array:
            pic1.append(i[34:56])
        pic_temp = img.fromarray(np.array(pic1)).convert('1')
        pic_temp.save('./processed/'+str(k)+'_'+str(count)+'.png')
        count += 1


def labelCaptcha():
    if not os.path.exists('./labelled/'):
        os.mkdir('./labelled/')
    chaojiying1 = chaojiying.Chaojiying_Client('517262600', 'blueking007', '898694')
    for i in range(5000):
        filename = str(i)+'.jpg'
        im = open('./dataset1/raw/'+filename, 'rb').read()
        name = chaojiying1.PostPic(im, 1902)['pic_str'].upper()
        now = str(int(time.time()))
        shutil.copyfile('./dataset1/raw/'+filename, './dataset1/train/'+name+'_'+now+'.png')
        print('处理完成', i)
# 1,7   ,i,O,Q,U,V,Z
if __name__ == '__main__':
    labelCaptcha()
