# 이옷 어디
Deep Learning model을 Web 상에 이식하여 이미지 특징 검색을 바탕으로한 패션 정보 검색 서비스이다.    

이미지 인식을 통한 패션 정보 검색 결과를 제공한다.     

패션 트렌드 정보와 관련된 공유 환경을 제공하고자 해당 플랫폼의 유저간 스타일을 자유롭게 게시할 수 있는 ‘스타일 커뮤니티’를 제공한다.     

## 설치 및 사용 매뉴얼    
### 해당 프로그램의 소스코드를 다운 받는다.    
git clone https://github.com/SSU-opensource-project/Deploy.git    

### 이미지 특징 Feature Map 다운. 
다운로드 후 현 프로젝트 폴더의 main 폴더 내에 삽입.    
https://drive.google.com/file/d/1QqkhMAMvRbJV8gTq_u6C3Pj7-RefTZHo/view?usp=sharing    

### Pretrain 된 모델 다운
압축 해제후 전체 폴더 main 폴더에 삽입     
https://drive.google.com/file/d/1DPydA0FpLYEHaFYDa8_oZAot_Ou5JefK/edit    

### 파이선 가상환경 설정 및 실행 방법. 
* 활성화된 빈 가상환경 이 필요하다.     
참고 링크 : https://dojang.io/mod/page/view.php?id=2470     

1. manage.py 가 존재하는 directory로 이동     

2. ``` pip install -r requirement.txt    ```

3. ``` python manage.py makemigrations     ```

4. ``` python manage.py migrate     ```

5. ``` python manage.py runserver    ``` 

### 실행 후 localhost에서 수행    
1. 회원 가입 필수.     (제품 추천 제외) 
2. 메인 페이지 에서 검색 하고픈 이미지 삽입    
3. 검색 결과 출력, 이미지 클릭시 판매자 링크로 이동함.     

### migration 오류 발생시 대처사항
1. User/migrations에 __init__.py 제외 전부 삭제    
2. main/migrations에 __init__.py 제외 전부 삭제    
3. 아래 명령어 차례대로 수행     
   ```
   python manage.py makemigrations      
   python manage.py migrate     
   python manage.py runserver     
   ```

### 주의사항
temp_media 폴더내 사진 삭제 시 DB오류 발생함.     
해결법 : db.sqlite3 삭제후 migraton 오류 발생시 대처사항 루틴 수행.    


