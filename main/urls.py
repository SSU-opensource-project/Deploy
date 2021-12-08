from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    # path('', views.index_view, name='index'),
    path('', views.mainpage_view, name='mainpage'),
    path('showpage', views.showpage_view, name='showpage'),
    path('logout', views.logout_btn, name='logout'),
    path('mypage', views.mypage_view, name='mypage'),
    path('mypage/<int:pid>/delete_photo',views.delete_photo, name='mypagedelete'),
    path('community', views.community_view, name='community'),
    path('rcmdpage', views.rcmdpage_view, name='rcmdpage'),
    path('community_upload',views.community_upload_view, name='community_upload'),
    path('community/<int:post_id>/detail', views.community_detail_view, name='community_detail'),
    path('service_info', views.service_info_view, name="service_info"),
]
