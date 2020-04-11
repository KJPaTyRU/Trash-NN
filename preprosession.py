import os
import pandas as pd
import numpy as np
import pickle
from PIL import Image
from options import *


def read_raw():
    images = os.listdir(RAW_DIR)
    data = []
    for img in images:
        path = os.path.join(RAW_DIR, img)
        image = np.asarray(Image.open(path))
        data.append(image)
    return np.array(data)

def center_select(m):
    b = []
    for k in range(0, FRAME_SIZE):
        if k < BORDER or FRAME_SIZE - (k+1) < BORDER:
            b += list(m[k])
        else:
            b+= list(m[k,0:BORDER]) + list(m[k,BORDER+BLACK_SIZE:FRAME_SIZE])
    return b

def slice_image_to_box(image):
    if image.shape[0] < FRAME_SIZE or image.shape[1] < FRAME_SIZE:
        return []
    fin = []
    i,j = 0, 0
    for j in range(0,image.shape[1]-FRAME_SIZE+1,SHIFT_Y):
        for i in range(0,image.shape[0]-FRAME_SIZE+1,SHIFT_X):
            m = image[i:i+FRAME_SIZE, j:j+FRAME_SIZE]
            fin.append(m)
    return fin

def slice_images_to_box(data):
    img_frames = []
    for d in data:
        img_frames.append(slice_image_to_box(d))
    return img_frames

def save_image_to_train(data):
    try:
        prev = int(os.listdir(TRAIN_DIR)[-1].split('.')[0])
    except:
        prev = 0

    for pic in data:
        for img in range(100,len(pic)):
            # change range beg if u want
            if prev == 50:
                break
            prev += 1
            image_to_save = Image.fromarray(pic[img])
            image_to_save.save(os.path.join(TRAIN_DIR,f"{prev}.jpg"))

def save_to_pickle(data, to_, file_name):
    with open(os.path.join(to_,file_name+".nnt"), 'wb') as out:
        pickle.dump(data, out)

def load_from_pickle(from_, file_name):
    with open(os.path.join(from_,file_name+".nnt"), 'rb') as inp:
        data = pickle.load(inp)
    return data

if __name__ == '__main__':
    d = read_raw()[0]
    n = slice_images_to_box(d)
    save_image_to_train(n)
    # save_to_pickle(n, TRAIN_DIR, "d_in2")
    # print(load_from_pickle(TRAIN_DIR, "d_in2"))












#
