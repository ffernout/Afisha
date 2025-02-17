from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404
from .models import Movie, Director, Review
from .serializers import MovieSerializer, DirectorSerializer, ReviewSerializer, ReviewDetailSerializer, DirectorDetailSerializer


@api_view(['GET', 'POST'])
def director_list_view(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        data = DirectorSerializer(directors, many=True).data
        return Response(data)

    elif request.method == 'POST':
        print("POST /api/v1/directors/ -> Data:", request.data)

        name = request.data.get('name')

        if not name:
            return Response({"error": "Name is required"}, status=status.HTTP_400_BAD_REQUEST)

        director = Director.objects.create(name=name)
        serializer = DirectorSerializer(director)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def director_detail_view(request, id):
    director = get_object_or_404(Director, id=id)

    if request.method == 'GET':
        data = DirectorSerializer(director).data
        return Response(data)

    elif request.method == 'PUT':
        name = request.data.get('name')

        if not name:
            return Response({"error": "Name is required"}, status=status.HTTP_400_BAD_REQUEST)

        director.name = name
        director.save()
        serializer = DirectorSerializer(director)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        director.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def movie_list_view(request):
    if request.method == 'GET':
        movies = Movie.objects.select_related('director').prefetch_related('reviews').all()
        data = MovieSerializer(instance=movies, many=True).data
        return Response({'list': data})

    elif request.method == 'POST':
        print("POST /api/v1/movies/ -> Data:", request.data)

        title = request.data.get('title')
        description = request.data.get('description')
        duration = request.data.get('duration')
        director_id = request.data.get('director')

        if not title or not description or not duration or not director_id:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            director = Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            return Response({"error": "Director not found"}, status=status.HTTP_400_BAD_REQUEST)

        movie = Movie.objects.create(
            title=title,
            description=description,
            duration=duration,
            director=director
        )
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def movie_detail_view(request, id):
    movie = get_object_or_404(Movie, id=id)

    if request.method == 'GET':
        data = MovieSerializer(movie).data
        return Response(data)

    elif request.method == 'PUT':
        print("PUT /api/v1/movies/ -> Data:", request.data)

        title = request.data.get('title', movie.title)
        description = request.data.get('description', movie.description)
        duration = request.data.get('duration', movie.duration)
        director_id = request.data.get('director', movie.director.id)

        try:
            director = Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            return Response({"error": "Director not found"}, status=status.HTTP_400_BAD_REQUEST)

        movie.title = title
        movie.description = description
        movie.duration = duration
        movie.director = director
        movie.save()
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def review_list_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewSerializer(instance=reviews, many=True).data
        return Response(data)

    elif request.method == 'POST':
        print("POST /api/v1/reviews/ -> Data:", request.data)

        text = request.data.get('text')
        stars = request.data.get('stars')
        movie_id = request.data.get('movie')

        if not text or not stars or not movie_id:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found"}, status=status.HTTP_400_BAD_REQUEST)

        review = Review.objects.create(
            text=text,
            stars=stars,
            movie=movie
        )
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_view(request, id):
    review = get_object_or_404(Review, id=id)

    if request.method == 'GET':
        data = ReviewSerializer(review).data
        return Response(data)

    elif request.method == 'PUT':
        print("PUT /api/v1/reviews/ -> Data:", request.data)

        text = request.data.get('text', review.text)
        stars = request.data.get('stars', review.stars)
        movie_id = request.data.get('movie', review.movie.id)

        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found"}, status=status.HTTP_400_BAD_REQUEST)

        review.text = text
        review.stars = stars
        review.movie = movie
        review.save()
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DirectorViewSet(viewsets.ModelViewSet):
    queryset = Director.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DirectorDetailSerializer
        return DirectorSerializer


class MovieDetailSerializer:
    pass


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return MovieDetailSerializer
        return MovieSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ReviewDetailSerializer
        return ReviewSerializer