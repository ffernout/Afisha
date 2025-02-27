
from django.contrib import admin
from django.urls import path
from dotenv import load_dotenv
load_dotenv()

urlpatterns = [
    path('admin/', admin.site.urls),
]
