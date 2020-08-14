from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_post import views


router = DefaultRouter()
router.register('', views.PostViewSet)

app_name = 'post'

urlpatterns = [
    path('', include(router.urls)),
]