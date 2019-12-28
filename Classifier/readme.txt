接口函数在CapDectect.py中

usage:
model = CapDectect()
predicted_label = model.predict(img)
//img是100*100的3通道RGB图像，uint8
//0,1,2分别对应正，反，侧