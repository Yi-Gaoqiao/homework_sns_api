from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api_dm import views


router = DefaultRouter()
router.register('message', views.MessageViewSet, basename='message')
router.register('inbox', views.InboxListView, basename='inbox')

app_name = 'dm'

urlpatterns = [
    path('', include(router.urls)),
]