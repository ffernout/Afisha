from django.contrib import admin
from django.urls import path, include

from movie_app.views import RegisterView, ConfirmView, LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('movie_app.urls')),
    path('api/v1/', include('directors.urls')),
    path('api/v1/users/register/', RegisterView.as_view(), name='register'),
    path('api/v1/users/confirm/', ConfirmView.as_view(), name='confirm'),
    path('api/v1/users/login/', LoginView.as_view(), name='login'),
]