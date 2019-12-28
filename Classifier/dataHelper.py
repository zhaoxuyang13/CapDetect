# -*- coding: utf-8 -*-
import numpy as np
from sklearn.model_selection import KFold
from torch.utils.data import Dataset
import torch
import time

def preprocess():
    '''
    划分验证集和训练集
    将标准化后的训练集、验证集保存在本地
    '''
    print('Preprocess Begin!')
    
    Xtrain_dev = np.load('dataset/Xtrain_dev.npy')
    Ytrain_dev = np.load('dataset/Ytrain_dev.npy')

    
    #划分验证集和训练集
    kf = KFold(n_splits=5,shuffle=True,random_state=int(time.time()))
    for train_idx,dev_idx in kf.split(Ytrain_dev):
        tmp1 = train_idx
        tmp2 = dev_idx
    Xtrain = Xtrain_dev[tmp1]
    Ytrain = Ytrain_dev[tmp1]
    Xdev = Xtrain_dev[tmp2]
    Ydev = Ytrain_dev[tmp2]
        
    
    #保存在本地
    np.save('dataset/Xtrain.npy',Xtrain)
    np.save('dataset/Ytrain.npy',Ytrain)
    np.save('dataset/Xdev.npy',Xdev)
    np.save('dataset/Ydev.npy',Ydev)
    
    print('Preprocess Done!')

class DealTrainset(Dataset):

    def __init__(self):
        x_train = np.load('dataset/Xtrain.npy')
        y_train = np.load('dataset/Ytrain.npy')
        #数据增强
        #x_train, y_train = Transform(x_train,y_train,1.8)
        
        self.x_data = torch.from_numpy(x_train)
        self.y_data = torch.from_numpy(y_train)
        self.len = y_train.shape[0]
    
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.len

class DealDevset(Dataset):

    def __init__(self):
        x_dev = np.load('dataset/Xdev.npy')
        y_dev = np.load('dataset/Ydev.npy')

        
        self.x_data = torch.from_numpy(x_dev)
        self.y_data = torch.from_numpy(y_dev)
        self.len = y_dev.shape[0]
    
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.len