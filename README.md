# 이옷 어디
Deep Learning model을 Web 상에 이식하여 이미지 특징 검색을 바탕으로한 패션 정보 검색 서비스이다.    

이미지 인식을 통한 패션 정보 검색 결과를 제공한다.     

패션 트렌드 정보와 관련된 공유 환경을 제공하고자 해당 플랫폼의 유저간 스타일을 자유롭게 게시할 수 있는 ‘스타일 커뮤니티’를 제공한다.     

## 설치 및 사용 매뉴얼    
#### STEP 1. 해당 프로그램의 소스코드를 clone받는다.
git clone https://github.com/SSU-opensource-project/Deploy.git    


#### STEP 2. 이미지 특징 Feature Map 다운로드한다.
   다운로드 후 현 프로젝트 폴더의 main 폴더 내에 삽입한다. <br>
https://drive.google.com/file/d/1QqkhMAMvRbJV8gTq_u6C3Pj7-RefTZHo/view?usp=sharing    


#### STEP 3. Pretrain된 모델을 다운로드한다.
   압축 해제 후 main 폴더에 해당 모델을 삽입한다. <br>
https://drive.google.com/file/d/1DPydA0FpLYEHaFYDa8_oZAot_Ou5JefK/edit    


#### STEP 4. python 가상환경을 설정한 뒤 실행한다.(활성화된 빈 가상환경이 필요) 
   참고 링크 : https://dojang.io/mod/page/view.php?id=2470
   1. manage.py 가 존재하는 directory로 이동     
   2. ``` pip install -r requirement.txt    ```
   3. ``` python manage.py makemigrations     ```
   4. ``` python manage.py migrate     ```
   5. ``` python manage.py runserver    ``` 


#### STEP 5. 실행 후 localhost에서 서버를 실행한다.


#### STEP 6. 서비스 사용을 위해서는 회원 가입이 필수적으로 이루어져야 한다. 
   - 제품 추천 기능은 회원가입 없이 이용 가능<br>
![image](https://user-images.githubusercontent.com/66112716/145233160-988a70e5-e18a-4821-9ef3-a2670132a148.png)
   
   
#### STEP 7. 메인 페이지에서 검색을 희망하는 이미지 파일을 삽입한다.  
   - 파일 삽입 후 검색하기 버튼 클릭<br>
![image](https://user-images.githubusercontent.com/66112716/145233201-42c8051f-cb3b-4e68-a642-c6fbd276be03.png)


#### STEP 8. 출력된 검색결과 중 구매를 희망하는 경우, 
*  해당 제품 이미지 클릭 시 판매자 링크로 이동한다.<br>
![image](https://user-images.githubusercontent.com/66112716/145233245-41c7c244-e992-4342-9e20-548a9bfd1ae0.png)


#### migration 오류 발생시 대처사항
   1. ```User/migrations```에 ```__init__.py``` 제외 전부 삭제    
   2. ```main/migrations```에 ```__init__.py``` 제외 전부 삭제    
   3. 아래 명령어 차례대로 수행     
      ```python manage.py makemigrations```      
      ```python manage.py migrate```     
      ```python manage.py runserver ```    
   
#### 주의사항
   - temp_media 폴더 내 사진 삭제 시 DB 상 오류가 발생한다.
   - 해결법 : db.sqlite3 삭제후 migraton 오류 발생 시 대처사항의 루틴을 수행한다.


