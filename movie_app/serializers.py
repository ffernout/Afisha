from random import randint

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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


class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = "id name movies_count".split()

    def get_movies_count(self, obj):
        return obj.movies.count()

    def validate_name(self, value):
        if Director.objects.filter(name=value).exists():
            raise ValidationError("Director with this name already exists.")
        return value

class DirectorDetailSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = "id name movies_count".split()

    def get_movies_count(self, obj):
        return obj.movies.count()

    def validate_name(self, value):
        director_id = self.context['view'].kwargs.get('id')
        if Director.objects.filter(name=value).exclude(id=director_id).exists():
            raise ValidationError("Director with this name already exists.")
        return value

    def validate(self, attrs):
        director_id = self.context['view'].kwargs.get('id')
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError("Director with this ID does not exist.")
        return attrs


class MovieSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = "id title description duration director average_rating".split()

    def get_average_rating(self, obj):
        return obj.average_rating

    def validate_description(self, value):
        if len(value) < 10:
            raise ValidationError("Description should be at least 10 characters long.")
        return value

    def validate_director(self, value):
        if not Director.objects.filter(id=value.id).exists():
            raise ValidationError("The director does not exist.")
        return value

    class MovieDetailSerializer(serializers.ModelSerializer):
        average_rating = serializers.SerializerMethodField()

        class Meta:
            model = Movie
            fields = "id title description duration director average_rating".split()

        def get_average_rating(self, obj):
            return obj.average_rating

        def validate(self, attrs):
            movie_id = self.context['view'].kwargs.get('id')
            try:
                Movie.objects.get(id=movie_id)
            except Movie.DoesNotExist:
                raise ValidationError("Movie with this ID does not exist.")

            director = attrs.get('director')
            if director and not Director.objects.filter(id=director.id).exists():
                raise ValidationError("The director does not exist.")

            return attrs

class ReviewSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())

    class Meta:
        model = Review
        fields = "id text stars movie".split()

    def validate_stars(self, value):
        if value < 1 or value > 6:
            raise ValidationError("Rating should be between 1 and 5.")
        return value

    def validate_text(self, value):
        if not value.strip():
            raise ValidationError("Review text cannot be empty.")
        return value


class ReviewDetailSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())

    class Meta:
        model = Review
        fields = "id text stars movie".split()

    def validate(self, attrs):
        review_id = self.context['view'].kwargs.get('id')
        try:
            Review.objects.get(id=review_id)
        except Review.DoesNotExist:
            raise ValidationError("Review with this ID does not exist.")

        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        confirmation_code = str(randint(100000, 999999))
        user = get_user_model().objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=make_password(validated_data['password']),
            confirmation_code=confirmation_code
        )
        print(f"Verification code sent: {confirmation_code} на email {user.email}")

        return user


class ConfirmSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()