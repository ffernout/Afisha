from django.contrib.auth import authenticate, get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, viewsets, generics
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .models import Movie, Director, Review
from .serializers import MovieSerializer, DirectorSerializer, ReviewSerializer, ReviewDetailSerializer, \
    DirectorDetailSerializer, LoginSerializer, ConfirmSerializer, RegisterSerializer


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


class DirectorListView(generics.ListCreateAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer



class DirectorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorDetailSerializer


class MovieListView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieDetailSerializer:
    pass


class MovieDetailView(generics.RetrieveUpdateDestroyAPIView):
        queryset = Movie.objects.all()
        serializer_class = MovieDetailSerializer



class ReviewListView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
        queryset = Review.objects.all()
        serializer_class = ReviewDetailSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User created. Please check your email for confirmation code."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmView(APIView):
    def post(self, request):
        serializer = ConfirmSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            confirmation_code = serializer.validated_data['confirmation_code']

            try:
                user = get_user_model().objects.get(username=username)
                if user.confirmation_code == confirmation_code:
                    user.is_active = True
                    user.save()
                    return Response({"message": "User confirmed successfully."}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid confirmation code."}, status=status.HTTP_400_BAD_REQUEST)
            except get_user_model().DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                return Response({"message": "Login successful!"}, status=status.HTTP_200_OK)
            elif user is not None:
                return Response({"error": "User not confirmed."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created. Please check your email for confirmation code."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConfirmView(APIView):
    def post(self, request):
        serializer = ConfirmSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            confirmation_code = serializer.validated_data['confirmation_code']

            try:
                user = get_user_model().objects.get(username=username)
                if user.confirmation_code == confirmation_code:
                    user.is_active = True
                    user.save()
                    return Response({"message": "User confirmed successfully."}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid confirmation code."}, status=status.HTTP_400_BAD_REQUEST)
            except get_user_model().DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                return Response({"message": "Login successful!"}, status=status.HTTP_200_OK)
            elif user is not None:
                return Response({"error": "User not confirmed."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)