from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
from pathlib import Path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime
import csv
import pandas as pd
from utils_my import Read_Img_2_Tensor, Load_DeepFashion2_Yolov3, Draw_Bounding_Box
import tensorflow as tf
import cv2
from PIL import Image
from tensorflow.python.ops.gen_image_ops import image_projective_transform_v3_eager_fallback
from cloth_detection import Detect_Clothes_and_Crop
from utils_my import Read_Img_2_Tensor, Save_Image, Load_DeepFashion2_Yolov3

model = Load_DeepFashion2_Yolov3()

###


class FeatureExtractor:
    def __init__(self):
        base_model = VGG16(weights='imagenet')
        self.model = Model(inputs=base_model.input,
                           outputs=base_model.get_layer('fc1').output)
        self.features = np.array(
            np.load(os.getcwd() + "./Total(Crop).npy"))  # 이미지의 특징이 저장된 npy파일 load 할떄 미리 load를 한 상태면 좋을듯
        # self.Img_features = np.array(  # 없어도 됨.
        #    np.load(os.getcwd() + "/Feature/Image_3_2(Big).npy"))  # 이미지 경로가 저장된 npy 파일/ 수정가능.수정필요. (그리고 굳이 안해도 되는것같음)

    def extract(self, img):
        img = img.resize((224, 224))
        img = img.convert('RGB')

        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        feature = self.model.predict(x)[0]
        return feature / np.linalg.norm(feature)


def MainFunction():  # 인자로 사용자가 넣을 이미지 이름 / 링크 넣어주면 ㅇㅋ
    fe = FeatureExtractor()
    FEATURES = fe.features  # FEATRUES는 특징들이 들어가있는 Total.npy

    img_path = '38165.jpg'  # 자를 사진 ( 사용자가 넣을 이미지 )
    # Read image

    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_tensor = Read_Img_2_Tensor(img_path)

    img_crop = Detect_Clothes_and_Crop(img_tensor, model)
    Save_Image(img_crop, '38165_crop2.jpg')

    img = Image.open('38165_crop2.jpg')  # 궁금한 이미지
    query = fe.extract(img)  # 이 작업까지 서버 실행 시 미리 해놓으면 그나마 빠를것같..
    #img_paths = fe.Img_features
    dists = np.linalg.norm(FEATURES - query, axis=1)
    ids = np.argsort(dists)[:50]

    # print(ids)
    ids_list = ids.tolist()
    df = pd.read_csv("./train_top50000.csv", index_col=0)
    # print(df)
    result_img_arr = []
    
    for i in range(0, len(ids_list)):
        result_img_arr.append(df.iloc[ids_list[i]]['img_url'])  # return 해줄 것

    #   result_img_arr 받으면 됨

    #for i in range(len(result_img_arr)):
    #    print(result_img_arr[i])
    os.remove(r"38165_crop2.jpg")
    
    return result_img_arr


"""
scores = [(dists[id-1], img_paths[id-1], id-1)
          for id in ids]  # id값은 아마 제대로

axes = []
fig = plt.figure(figsize=(8, 8))
for a in range(5*6):
    score = scores[a]
    axes.append(fig.add_subplot(5, 6, a+1))
    subplot_title = str(round(score[0], 2)) + \
        "/m" + str(score[2]+1)  # dists + id
    axes[-1].set_title(subplot_title)
    plt.axis('off')
    plt.imshow(Image.open(score[1]))  # 이미지 창 열음
fig.tight_layout()
plt.show()
"""

# 메인


def Detect_Clothes(img, model_yolov3, eager_execution=True):
    """Detect clothes in an image using Yolo-v3 model trained on DeepFashion2 dataset"""
    img = tf.image.resize(img, (416, 416))

    t1 = time.time()
    if eager_execution == True:
        boxes, scores, classes, nums = model_yolov3(img)
        # change eager tensor to numpy array
        boxes, scores, classes, nums = boxes.numpy(
        ), scores.numpy(), classes.numpy(), nums.numpy()
    else:
        boxes, scores, classes, nums = model_yolov3.predict(img)
    t2 = time.time()
    print('Yolo-v3 feed forward: {:.2f} sec'.format(t2 - t1))

    class_names = ['short_sleeve_top', 'long_sleeve_top', 'short_sleeve_outwear', 'long_sleeve_outwear',
                   'vest', 'sling', 'shorts', 'trousers', 'skirt', 'short_sleeve_dress',
                   'long_sleeve_dress', 'vest_dress', 'sling_dress']

    # Parse tensor
    list_obj = []
    for i in range(nums[0]):
        obj = {'label': class_names[int(
            classes[0][i])], 'confidence': scores[0][i]}
        obj['x1'] = boxes[0][i][0]
        obj['y1'] = boxes[0][i][1]
        obj['x2'] = boxes[0][i][2]
        obj['y2'] = boxes[0][i][3]
        list_obj.append(obj)

    return list_obj


"""
def Detect_Clothes_and_Crop(img_tensor, model, threshold=0.5):
    global img_crop
    global flag
    list_obj = Detect_Clothes(img_tensor, model)

    img = np.squeeze(img_tensor.numpy())
    img_width = img.shape[1]
    img_height = img.shape[0]

    class_names = ['short_sleeve_top', 'long_sleeve_top',
                   'vest', 'short_sleeve_outwear', 'long_sleeve_outwear', 'long_sleeve_dress', 'vest_dress', 'sling_dress', 'short_sleeve_dress']

    flag = 0
    for obj in list_obj:
        if obj['label'] in class_names and obj['confidence'] > threshold:
            # if obj['label'] == 'short_sleeve_top' and obj['confidence']>threshold:
            img_crop = img[int(obj['y1']*img_height): int(obj['y2']*img_height),
                           int(obj['x1']*img_width): int(obj['x2']*img_width), :]
            flag = 1

    return img_crop
"""
MainFunction()
