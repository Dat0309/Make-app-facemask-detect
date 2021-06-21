import cv2 as cv
import os
import numpy as np
from keras.utils import np_utils

#Tên thư mục dataset chứa dữ liệu để train cho máy tính
data_path = 'dataset'
#Trả về một danh sách chưa tên của các mục trong thư mục được đưa ra bởi đường dẫn
categories = os.listdir(data_path)
labels = [i for i in range(len(categories))]

#empty dictionary
label_dict = dict(zip(categories,labels))

print(label_dict)
print(categories)
print(labels)

img_size = 100
data = []
target = []

print('Training.......................')

for category in categories:
    #tên file dataset với tên của các thư mục bên trong để tạo thành đường dẫn.
    folder_path = os.path.join(data_path,category)
    img_names = os.listdir(folder_path)

    for name in img_names:
        #Tiếp tục ghép tạo đường dẫn tới ảnh trong thư mục dataset
        img_path = os.path.join(folder_path,name)
        img = cv.imread(img_path)

        try:
            #Phủ màu nâu cho từng ảnh.
            gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
            resized = cv.resize(gray,(img_size,img_size))
            #Thêm ảnh đã được đổi màu và đổi kích cỡ vào list
            data.append(resized)
            target.append(label_dict[category])

        except Exception as e:
            pass

# data.clear()
# target.clear()
# print(len(data))
# print(len(target))
# cv.imshow('Img1',data[1])
# cv.waitKey()
# print(target)

data = np.array(data)/255.0
#Thay dổi hình dạng cho mảng data mà không làm thay đổi dữ liệu 
data = np.reshape(data, (data.shape[0],img_size,img_size,1))
target = np.array(target)

#Ghi file data
new_target = np_utils.to_categorical(target)
np.save('data',data)
np.save('target',new_target)

