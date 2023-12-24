from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FilesViewSet
from . import views

router = DefaultRouter()
router.register('files', FilesViewSet, basename='files')


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/all_files/', views.all_files, name='all_files'),
    path('api/download/<int:pk>/', views.download_file, name='download_file'),
    path('api/user/register/', views.user_registration, name='user_registration'),
    path('api/user/login/', views.user_login, name='user_login'),
    path('api/user/logout/', views.user_logout, name='user_logout'),
    path('api/verify-email/<str:verification_token>/', views.verify_email, name='verify_email'),
]