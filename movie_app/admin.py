from django.contrib import admin
from .models import Movie, Director, Review

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'stars', 'movie')
    list_filter = ('stars', 'movie')
    search_fields = ('text',)