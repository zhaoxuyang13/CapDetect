import torch
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim
import numpy as np
from Classifier.dataHelper import DealTrainset,DealDevset,preprocess
from .Classifier.model import CapCNN
from sklearn import metrics

# 定义是否使用GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# 超参数设置
BATCH_SIZE = 32
NUM_EPOCHS = 64
LR = 0.001

#数据预处理
#preprocess()
#定义训练批处理数据
dealTrainset = DealTrainset()
train_loader = DataLoader(dataset=dealTrainset,
                          batch_size=BATCH_SIZE,
                          shuffle=True
                          )

# 定义测试批处理数据
dealTestset = DealDevset()
test_loader = DataLoader(dataset=dealTestset,
                          batch_size=BATCH_SIZE,
                          shuffle=True
                          )
#定义损失函数和优化方式
net = CapCNN().to(device)
criterion = nn.CrossEntropyLoss()
#criterion = nn.BCELoss()
#criterion = nn.MSELoss()
optimizer = optim.Adam(net.parameters(), lr=LR)

dev_accu = []
optim_correct = 0
for epoch in range(NUM_EPOCHS):
    sum_loss = 0.0
    #数据读取
    for i,data in enumerate(train_loader):
        Xtrain,Ytrain = data
        Xtrain = Xtrain.type(torch.FloatTensor)
        Ytrain = Ytrain.type(torch.LongTensor)
        Xtrain,Ytrain = Xtrain.to(device), Ytrain.to(device)
        
        #梯度清零
        optimizer.zero_grad()
        
        #前后传播+后向传播
        outputs = net(Xtrain)        
        loss = criterion(outputs,Ytrain)
        loss.backward()
        optimizer.step()
        
        # 每训练3个batch打印一次平均loss
        sum_loss += loss.item()
        if i % 3 == 2:
            print('[%d, %d] loss: %.08f'
                  %((epoch+1),i+1,sum_loss/3))
            sum_loss = 0.0
            
    # 每跑完一次epoch测试一下准确率(测试集)
    with torch.no_grad():
        correct = 0
        total = 0

        for data in test_loader:
            Xdev, Ydev = data
            Xdev = Xdev.type(torch.FloatTensor)
            Ydev = Ydev.type(torch.LongTensor)
            Xdev, Ydev = Xdev.to(device), Ydev.to(device)
            outputs = net(Xdev)
                
            #计算准确率
            _, predicted = torch.max(outputs.data, 1)
            total += Ydev.size(0)
            correct += (predicted==Ydev).sum()
                    

        print('第%d个epoch的识别准确率为(测试集)：%.2f%%' % (epoch + 1, (100.0 * correct / total)))
        correct = np.array(correct.cpu())
        dev_accu.append(correct)
        
        #保存模型
        if optim_correct < correct:
            optim_correct = correct
            torch.save(net.state_dict(), 'cap_para.pkl')
        
    
       # 每跑完一次epoch测试一下准确率(训练集)    
    with torch.no_grad():
        correct = 0
        total = 0
        for data in train_loader:
            Xtrain, Ytrain = data
            Xtrain = Xtrain.type(torch.FloatTensor)
            Ytrain = Ytrain.type(torch.LongTensor)
            Xtrain, Ytrain = Xtrain.to(device), Ytrain.to(device)
            outputs = net(Xtrain)
            
            #计算准确率
            _, predicted = torch.max(outputs.data, 1)
            total += Ytrain.size(0)
            correct += (predicted==Ytrain).sum()
        print('第%d个epoch的识别准确率为(训练集)：%.2f%%' % (epoch + 1, (100.0 * correct / total)))


        
