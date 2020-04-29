import numpy as np
import os
import re
import csv
import glob
import os.path as path
import scipy.misc as misc
import pandas as pd
import keras.backend as K
from keras.preprocessing.image import *
from PIL import Image,ImageOps
from scipy import linalg
from sklearn.model_selection import train_test_split
from utils import *

class Dataset(object):
    def __init__(this,basepath=""):
        this.basepath = basepath
        this.Images = []

    def __add__(this, other):
        this.Images += other.Images
        return this

    def __len__(this):
        return len(this.Images)

    def __getitem__(this, key):
        return this.Images[key]

    def load(this,**kwargs):
        raise NotImplementedError

    def load_data(this,**kwargs):
        raise NotImplementedError

    def _pad_images(this,list):
        N = len(list)

        max_shape = max([list[x].shape for x in range(N)])

        for i in range(N):
            shape = list[i].shape

            diff = [ max_shape[k] - shape[k] for k in range(len(max_shape)) ]

            if (np.sum(diff)>0):
                T = np.zeros(shape=max_shape)
                diff = np.floor(np.asarray(diff)/2.).astype('int')
                slices = [slice(diff[k],diff[k]+shape[k]) for k in range(len(shape))]
                T[slices] = list[i]
                list[i] = T

        return list


class CVPPPDataset(Dataset):
    def __init__(this,basepath,folders=range(1,5)):
        super(CVPPPDataset, this).__init__(basepath)
        this.folders=folders

    def load(this,**kwargs):
        new_size = kwargs.get('new_size',(250,250))

        for k in this.folders:
            folder = 'A'+str(k)
            path = os.path.join(this.basepath,folder)

            csv_handle = open(os.path.join(path,folder+'.csv'),'r')
            csv_reader = csv.reader(csv_handle,delimiter=',')

            for row in csv_reader:
                I = Image.open(os.path.join(path,row[0]))
                I = I.resize(new_size)
                im = np.asarray(I)[:,:,0:3]
                count = int(row[1])

                this.Images.append({'rgb':im,'count':count})

            csv_handle.close()

        N = len(this.Images)
        l = [this.Images[i]['rgb'] for i in range(N)]
        l = this._pad_images(l)

        for i in range(N):
            this.Images[i]['rgb'] = l[i]

    def load_data(this, **kwargs):
        this.load(**kwargs)
        counts = np.asarray([this.Images[i]['count'] for i in range(len(this))])
        images = np.asarray([this.Images[i]['rgb'] for i in range(len(this))])
        return (images, counts)

def train_val_test_split(X, Y):
    x_train_val, x_test, y_train_val, y_test = train_test_split(X, Y, test_size=0.2, train_size=0.8)
    x_train, x_val, y_train, y_val = train_test_split(x_train_val, y_train_val, test_size=0.25, train_size=0.75)
    return (x_train, x_val, x_test, y_train, y_val, y_test)

if __name__ == "__main__":
    D = CVPPPDataset("E:/Dataset",folders=[1,2,3,5])
    (x, y) = D.load_data(new_size=(240,240))

    (x_train, x_val, x_test, y_train, y_val, y_test) = train_val_test_split(x, y)
    # x_train, x_test, y_train, y_test  = train_test_split(x, y, test_size=0.2, train_size=0.8)

    np.savez('data/dataset.npz', data=(x_train, x_val, x_test, y_train, y_val, y_test))

