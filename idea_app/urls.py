from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),  
    path('idea/', views.idea_list, name='idea_list'),
    path('idea/<int:pk>/', views.idea_detail, name='idea_detail'),
    path('idea/new/', views.idea_create, name='idea_create'),
    path('idea/<int:pk>/edit/', views.idea_edit, name='idea_edit'),
    path('idea/<int:pk>/delete/', views.idea_delete, name='idea_delete'),
    path('login/', auth_views.LoginView.as_view(next_page='home'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('signup/', views.signup, name='signup'),
    path('user_profile/', views.user_profile, name='user_profile'), 
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

