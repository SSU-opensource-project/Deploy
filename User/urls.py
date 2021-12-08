from django.urls import path
from . import views

# 다른 파일에서 app_name:name 으로 관리 가능
app_name = "User"
urlpatterns = [
    path("login", views.login_view, name="login"),
    path("signup", views.signup_view, name='signup'),
    path("/",views.index_view,name='index')
]