from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_user import views


router = DefaultRouter()
router.register('approval', views.FriendRequestViewSet)
router.register('profile', views.ProfileViewSet)

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('myprofile/', views.MyProfileListView.as_view(), name='myprofile'),
    path('token/', views.CreateTokenView.as_view(), name='token'), 
    path('', include(router.urls)),
]