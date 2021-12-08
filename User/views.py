from django.shortcuts import render
from django.contrib.auth import authenticate , login,logout
from django.shortcuts import redirect
from .models import users

def index_view(request):
    return redirect('User:login')


def signup_view(request):
    if request.method == 'POST': #회원가입 버튼 눌렀을떄
        email = request.POST.get('email')  # post에 포함된 정보 가져오기
        name = request.POST.get('name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        gender = request.POST.get('gender')
        if password1 == password2:
            user = users.objects.create_user(email, name, password1, gender)
            if user is not None:
                return redirect('User:login')
    elif request.method == 'GET':
        return render(request, 'User/signup.html')


def login_view(request):
    if request.method == "POST": # 요청이 오면 들어옴.
        email = request.POST.get('email') # post에 포함된 정보 가져오기
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            print("yes")
            login(request, user) # 성공시 현재 로그인된 상태임.
            return redirect('main:mainpage')
        else:
            print("no")
            return render(request, 'User/login.html')
    elif request.method == "GET":
        return render(request, 'User/login.html')
    else:
        return render(request, "User/login.html")


