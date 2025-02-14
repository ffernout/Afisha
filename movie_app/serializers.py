from rest_framework import serializers
from .models import Movie, Director, Review

class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = "id name movies_count".split()

    def get_movies_count(self, obj):
        return obj.movies.count()


class MovieSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = "id title description duration director average_rating".split()

    def get_average_rating(self, obj):
        return obj.average_rating


class ReviewSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())

    class Meta:
        model = Review
        fields = "id text stars movie ".split()