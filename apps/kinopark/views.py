from django.shortcuts import render
from rest_framework import status
from apps.kinopark.models import Movie
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from apps.kinopark.serializers import *
import pickle
import re



@api_view(['GET', 'POST', 'DELETE'])
def movies_list(request):
    if request.method == 'GET':
        movies = Movie.objects.all()

        movies.query = pickle.loads(pickle.dumps(movies.query))
        print(movies.query)
        movies.reverse()
        print(movies.reverse())

        title = request.GET.get('title', None)
        if title is not None:
            movies = movies.filter(movie__icontains=title)

        movies_serializer = MovieSerializer(movies, many=True)
        return JsonResponse(movies_serializer.data, safe=False)
    elif request.method == 'POST':
        movie_data = JSONParser().parse(request)
        movie_serializer = MovieSerializer(data=movie_data)
        if movie_serializer.is_valid():
            movie_serializer.save()
            return JsonResponse(movie_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(movie_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        counter = Movie.objects.all().delete()
        return JsonResponse({'message': 'deleted'.format(counter[0])})

@api_view(['POST'])
def sign_up(request):
    registration_data = JSONParser().parse(request)
    registration_serializer = RegistrationSerializer(data=registration_data)
    print(registration_data)
    pattern = "[a-zA-Z0-9]+@[a-zA-Z]+\.(com|edu|net)"
    pswd = registration_data.get("email")
    if re.search(pattern, pswd):
        if registration_serializer.is_valid():
            registration_serializer.save()
            return JsonResponse({"message": "successfully registered"}, status=status.HTTP_201_CREATED)
        else:
            print("Email is invalid")
            return JsonResponse({"message": "Wrong email or password"})

    return JsonResponse({"message": "Email or password is incorrect"})

@api_view(['GET', 'PUT', 'DELETE'])
def movie_by_id(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return JsonResponse({'message: Movie does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        movie_serializer = MovieSerializer(movie)
        return JsonResponse(movie_serializer.data)

    elif request.method == "PUT":
        new_data = JSONParser().parse(request)
        movie_serializer = MovieSerializer(movie, data=new_data)
        if movie_serializer.is_valid():
            movie_serializer.save()
            return JsonResponse(movie_serializer.data)
        return JsonResponse(movie_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        movie.delete()
        return JsonResponse({'message: the movie was deleted'})


@api_view(['GET'])
def unpublished_movies(request):
    movies = Movie.objects.filter(published=False)
    if request.method == 'GET':
        movies_serializer = MovieSerializer(movies, many=True)
        return JsonResponse(movies_serializer.data, safe=False)