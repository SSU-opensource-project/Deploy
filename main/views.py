import time
import random

from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import redirect
from numpy.compat import os_fspath

from .models import Photo,Posting,Recent
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime
import csv
import pandas as pd

import tensorflow as tf
import cv2
from PIL import Image
from tensorflow.python.ops.gen_image_ops import image_projective_transform_v3_eager_fallback
from .cloth_detection import Detect_Clothes_and_Crop
from .utils_my import Read_Img_2_Tensor, Save_Image, Load_DeepFashion2_Yolov3

model = Load_DeepFashion2_Yolov3()
# Create your views here.
BASE_DIR = Path(__file__).resolve().parent.parent

def mainpage_view(request):
    if request.user.is_anonymous:  # 로그인확인
        return redirect('User:login')
    print(request.user.username)
    print(request.user.email)

    return render(request, 'main/mainpage.html')

def showpage_view(request):
    if request.user.is_anonymous:  # 로그인확인
        return redirect('User:login')
    if request.method == 'POST':
        myimage = request.FILES.get('uploadImage')
        if myimage is not None:
            name = request.user.username
            save_search_file(request.user,myimage)
            image = Photo()
            image.email = request.user.email
            image.image = myimage
            image.save()
            result = MainFunction(image.image) # all result desc
            return render(request, 'main/showpage.html', {'myImage': image, 'Username': name,'results': result})
        else:
            redirect('main:mainpage')

    return redirect('main:mainpage')


def save_search_file(user,image): #최근 검색기록 3개만 저장
    searched = Recent.objects.filter(email=user.email).order_by('created_at')
    if len(searched) < 3:
        new = Recent()
        new.email = user.email
        new.image = image
        new.save()
    else :
        searched[0].delete()
        new = Recent()
        new.email = user.email
        new.image = image
        new.save()

def mypage_view(request):
    if request.user.is_anonymous:  # 로그인확인
        return redirect('User:login')
    if request.method == 'GET':
        user = request.user
        myimages = Photo.objects.filter(email=request.user.email).order_by('-created_at') #최신순 정렬, 배열로 넘어옴
        images = []
        for i in range(0,len(myimages)):
            images.append({'url': (myimages[i].image.url.replace("%40", "@"))[1:], 'id': myimages[i].id})

        if myimages is not None: # 사진 유무 파악
            return render(request, 'main/mypage.html', {'bool': True, 'images': images, 'user': user})
        else :
            image = ""
            return render(request, 'main/mypage.html', {'bool': False, 'image': image, 'user': user})


def rcmdpage_view(request):
    if request.user.is_anonymous:  # 로그인 안한 유저
        default = Recent.objects.order_by('-created_at')  # 검색 기록 없다면 다른 유저의 가장 최근 검색기록으로
        email = default[0].email
    else:  # 로그인 한 유저
        default = Recent.objects.exclude(email=request.user.email).order_by('-created_at')  # 검색 기록 없다면 다른 유저의 가장 최근 검색기록으로
        email = request.user.email
    print(len(default))
    resent_search_list = Recent.objects.filter(email=email).order_by('-created_at') # 내검색기록 모두 가져오기 .
    print(len(resent_search_list))
    if len(resent_search_list) <= 0 : #한번도 검색 안했음
        result = []
        tmp = MainFunction(default[0].image) #검색 기록 없다면 다른 유저의 가장 최근 검색기록으로
        for i in range(0, 20):
            result.append(tmp[i])
        return render(request, 'main/rcmdpage.html',{'results': result})  # 제품 추천 페이지
    else: #무조건 10개는 뽑힘
        result = []
        for i in range(0, len(resent_search_list)):
            tmp = MainFunction(resent_search_list[i].image)
            for j in range(0,(10 - i*4)): # 가장최신 10개, 6개 4개 순으로 뽑음
                randnum = random.randrange(0,21) #유사도 상위 20개 범위내에서 랜덤 추출
                result.append(tmp[randnum])
        if len(resent_search_list) == 1: # 나머지 10개 추출은 전체 서버에서 가장 최신 검색기록
            tmp = MainFunction(default[0].image)
            for i in range (0,10):
                randnum = random.randrange(0, 21)
                result.append(tmp[randnum])
        elif len(resent_search_list) == 2: # 나머지 4개 추출  전체 서버에서 가장 최신 검색기록
            tmp = MainFunction(default[0].image)
            for i in range(0, 4):
                randnum = random.randrange(0, 21)
                result.append(tmp[randnum])
        return render(request, 'main/rcmdpage.html', {'results': result })

def delete_photo(request,pid):
    curphoto = Photo.objects.get(id=pid)
    curphoto.delete()
    return redirect('main:mypage')


def logout_btn(request):
    logout(request)
    return redirect('User:login')


def community_view(request):
    if request.user.is_anonymous:  # 로그인확인
        return redirect('User:login')
    if request.method == 'GET':
        postings = Posting.objects.order_by('-pub_date') # 최신순으로 가져옴
        if postings is None:
            return render(request, 'main/community.html',{'posts': False}) #배열로 넘김
        else :
            for post in postings:
                if post.cloth_image == "": #오류방지:사진 없다면 삭제해버림
                    post.delete()
            return render(request, 'main/community.html',{'posts': postings}) #배열로 넘김


def community_upload_view(request):
    if request.user.is_anonymous:  # 로그인확인
        return redirect('User:login')
    if request.method == 'GET':
        return render(request, 'main/community_post.html')
    elif request.method == 'POST':
        inputImage = request.FILES.get('inputImage')
        post = Posting()
        post.title = request.POST['title']
        post.writer = request.user.email
        post.body = request.POST['body']
        post.cloth_image = inputImage
        post.save()
        return redirect('main:community')


def community_detail_view(request,post_id):
    if request.user.is_anonymous:  # 로그인확인
        return redirect('User:login')
    if request.method == 'GET':
        post = Posting.objects.get(id=post_id)
        return render(request, 'main/community_detail.html',{'post':post})

def service_info_view(request):
    if request.user.is_anonymous:  # 로그인확인
        return  render(request, 'main/service_info.html',{'username':False})
    else:
        return render(request, 'main/service_info.html',{'username':True})    #서비스 소개 페이지


class FeatureExtractor:
    def __init__(self):
        print(os_fspath(os.getcwd()+"Total(Crop).npy"))
        base_model = VGG16(weights='imagenet')
        self.model = Model(inputs=base_model.input,
                           outputs=base_model.get_layer('fc1').output)
        self.features = np.array(
            np.load("main/Total(Crop).npy"))  # 이미지의 특징이 저장된 npy파일 load 할떄 미리 load를 한 상태면 좋을듯
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


def MainFunction(user_image):  # 인자로 사용자가 넣을 이미지 이름 / 링크 넣어주면 ㅇㅋ

    fe = FeatureExtractor()
    FEATURES = fe.features  # FEATRUES는 특징들이 들어가있는 Total.npy
    # Read image
    image_path = (user_image.url.replace("%40", "@"))[1:]

    #print(image_path)
    try:  # 자를 사진 ( 사용자가 넣을 이미지 )
        img = cv2.imread(image_path)
        #print(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_tensor = Read_Img_2_Tensor(image_path)
        img_crop = Detect_Clothes_and_Crop(img_tensor, model) #'main\\38165_crop2.jpg'
        Save_Image(img_crop,os.path.join(BASE_DIR,'main\\temp.jpg')) #임시 사진 -> 무조건 삭제될 예정
        img = Image.open('main/temp.jpg')  # 궁금한 이미지
    except Exception as e:
        img = Image.open(image_path)  # 상의 인식못하면 원본사진 넣음
        print(e)
        pass
    query = fe.extract(img)  # 이 작업까지 서버 실행 시 미리 해놓으면 그나마 빠를것같..
    # img_paths = fe.Img_features
    dists = np.linalg.norm(FEATURES - query, axis=1)
    ids = np.argsort(dists)[:30]

    # print(ids)
    ids_list = ids.tolist()
    df = pd.read_csv("main/train_top50000.csv", index_col=0)
    # print(df)

    # return 해줄 것
    result_img_arr = []
    for i in range(0, len(ids_list)):
        result_img_arr.append({'image': df.iloc[ids_list[i]]['img_url'],'siteurl': df.iloc[ids_list[i]]['url']})

    """for i in range(0, len(ids_list)):
        result_img_arr[1].append()"""

    #  결과 테스트
    """ for i in range(len(result_img_arr)):
        print(result_img_arr[i])
    for i in range(len(result_img_arr[1])):  # 출력
        print(result_img_arr[1][i])"""
    os.remove('main/temp.jpg') # 전처리 이미지 삭제

    return result_img_arr


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



