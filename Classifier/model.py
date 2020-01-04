import torch
import torch.nn as nn
import torch.nn.functional as F

class CapCNN(nn.Module):
    def __init__(self):
        super(CapCNN,self).__init__()
        self.features = nn.Sequential( #input_size=(1*100*100))
                nn.Conv2d(1,32,kernel_size=3,stride=2,padding=1),
                nn.ReLU(inplace=True),
                nn.MaxPool2d(kernel_size=2,stride=2),
                
                nn.Conv2d(32,64,kernel_size=5,padding=2),
                nn.ReLU(inplace=True),
                nn.MaxPool2d(kernel_size=2,stride=2),
                
                nn.Conv2d(64,32,kernel_size=3,padding=1),
                nn.ReLU(inplace=True),
                nn.MaxPool2d(kernel_size=2,stride=2)
                
#                nn.Conv2d(32,16,kernel_size=3,padding=1),
#                nn.ReLU(inplace=True),
#                nn.MaxPool2d(kernel_size=2,stride=2),
                )
        
        self.classifier = nn.Sequential(
#                nn.Dropout(p=0.5),
                nn.Linear(32*6*6,32),
                nn.ReLU(inplace=True),
                nn.Linear(32,4)
                )
        
    def forward(self,x):
        x = self.features(x)
        x = x.view(x.size(0),-1)
        x = self.classifier(x)
        x = F.softmax(x,dim=1)
        return x