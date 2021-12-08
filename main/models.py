import os
from uuid import uuid4
from django.db import models
from django.db import models
from django.conf import settings
from django.utils import timezone

import time


def upload_to_search(instance, filename):
    prefix = instance.email
    file_name = str(int(time.time()))
    extension = os.path.splitext(filename)[-1].lower() # 확장자 추출
    return ("/".join(
        ["search",prefix, file_name]
    ))+extension


def upload_to_func(instance, filename):
    prefix = instance.email
    file_name = str(int(time.time()))
    extension = os.path.splitext(filename)[-1].lower() # 확장자 추출
    return ("/".join(
        [prefix, file_name]
    ))+extension


def upload_to_posting(instance, filename):
    prefix = instance.writer
    file_name = instance.title
    extension = os.path.splitext(filename)[-1].lower() # 확장자 추출
    return ("/".join(
        ["posting", prefix, file_name]
    ))+extension


# Create your models here.
class Recent(models.Model):
    email = models.EmailField(max_length=255,default="ata97@naver.com")
    image = models.ImageField(upload_to = upload_to_search) # 어디로 업로드 할지 지정
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.email

    def delete(self, *args, **kwargs): #삭제시 해당 경로 파일도 같이 삭제
        os.remove(os.path.join(settings.MEDIA_ROOT, self.image.name))
        super(Recent, self).delete(*args, **kwargs)


# Create your models here.
class Photo(models.Model):
    email = models.EmailField(max_length=255,default="ata97@naver.com")
    image = models.ImageField(upload_to = upload_to_func) # 어디로 업로드 할지 지정
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.email

    def delete(self, *args, **kwargs): #삭제시 해당 경로 파일도 같이 삭제
        os.remove(os.path.join(settings.MEDIA_ROOT, self.image.name))
        super(Photo, self).delete(*args, **kwargs)


class Posting(models.Model) :
    title = models.CharField(max_length=200)    # 제목
    writer = models.CharField(max_length=100)        # 작성자
    pub_date = models.DateTimeField(default=timezone.now)         # 게시물 올린 날짜 자동지정
    body = models.TextField()   #게시물의 내용
    cloth_image = models.ImageField(upload_to = upload_to_posting)

    def __str__(self):
        return self.title # 글의 제목으로 볼 수 있게 만들어줌

    def summary(self):
        return self.body[:100]  # 100자만 볼 수 있도록 설정


