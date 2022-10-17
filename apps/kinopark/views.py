from django.shortcuts import render, get_object_or_404
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from rest_framework import status
from apps.kinopark.models import Movie
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from apps.kinopark.serializers import *
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.http import FileResponse
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string

from .models import ContactForm
import io
import jwt, datetime
import pickle
import logging
import re

logger = logging.getLogger(__name__)


# def gen_pdf(request):
#     buf = io.BytesIO()
#     canva = canvas.Canvas(buf, pagesize=letter)
#
#     text = canva.beginText()
#
#     text.setFont("Helvetica", 17)
#     lines = ['the list of text', 'the list of text', 'the list of text']
#     for line in lines:
#         text.textLine(line)
#         canva.drawString(100, 750, lines)


#
# canva.showPage()
# canva.save()
# buf.seek(0)
#
# return FileResponse(buf, as_attachment=True, filename="lines.pdf")
@api_view(['GET'])
def seans_list(request):
    if request.method == 'GET':
        seansy = Seans.objects.all()
        seans_serializer = SeansSerializer(seansy, many=True)
        return JsonResponse(seans_serializer.data, safe=False)


#
# @api_view(['GET'])
# def kinozal_by_id(request, id):
#     try:
#         kinozal = Kinozal.objects.get(id=id)
#     except Kinozal.DoesNotExist:
#         return JsonResponse({"Message": "Kinozal does not exist"}, status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         kinozal_serializer = KinozalSerializer(kinozal)
#         return JsonResponse(kinozal_serializer.data)


@api_view(['GET'])
def seans_by_id(request, id):
    try:
        seans = Seans.objects.get(id=id)
    except Seans.DoesNotExist:
        return JsonResponse({"Message": "Seans does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        seans_serializer = SeansSerializer(seans)
        return JsonResponse(seans_serializer.data)


@api_view(['GET', 'POST', 'DELETE'])
def movies_list(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        movies.query = pickle.loads(pickle.dumps(movies.query))
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
        logging.critical(status)
        return JsonResponse(movie_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        counter = Movie.objects.all().delete()
        return JsonResponse({'message': 'deleted'.format(counter[0])})


@api_view(['POST'])
def create_order(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed("Не авторизованый пользователь")

    payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    user = get_object_or_404(User, pk=payload['id'])

    order_data = JSONParser().parse(request)
    order_data.update(
        {'user': user.id}
    )
    order_serializer = CreateOrderSerializer(data=order_data)

    if order_serializer.is_valid(raise_exception=True):
        order_serializer.save()
        return JsonResponse(order_serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_order_by_id(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return JsonResponse({"message": "Order does not exist"}, status=status.HTTP_404_NOT_FOUND)
    order_serializer = OrderSerializer(order)
    return JsonResponse(order_serializer.data)


# @api_view(['POST'])
# def sign_up(request):
#     registration_data = JSONParser().parse(request)
#     registration_serializer = RegistrationSerializer(data=registration_data)
#     print(registration_data)
#     pattern = "[a-zA-Z0-9]+@[a-zA-Z]+\.(com|edu|net)"
#     pswd = registration_data.get("email")
#     if re.search(pattern, pswd):
#         if registration_serializer.is_valid():
#             registration_serializer.save()
#             return JsonResponse({"message": "successfully registered"}, status=status.HTTP_201_CREATED)
#         else:
#             print("Email is invalid")
#             return JsonResponse({"message": "Wrong email or password"})
#
#     return JsonResponse({"message": "Email or password is incorrect"})

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


class RegisterView(APIView):

    def post(self, request):
        email = request.data['email']
        serializer = UserSerializer(data=request.data)
        pattern = "[a-zA-Z0-9]+@[a-zA-Z]+\.(com|edu|net)"
        if re.search(pattern, email):
            serializer.is_valid(raise_exception=True)
            serializer.save()
            print("OK")
            return Response(serializer.data)
        else:
            raise AuthenticationFailed("Error email")


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("Пользователь не найден")

        if not user.check_password(password):
            raise AuthenticationFailed("Не правильный пароль")

        user.is_active = True
        user.last_login = datetime.datetime.utcnow()
        user.save()
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


def get_login(request):
    # logging.basicConfig(filename='info.log', filemode='w', format='%(asctime)s - %(name)s % - %(level)s - %(message)s')
    # logging.warning('TEST')
    logger.warning('test')
    return render(request, 'login.html')


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Пользователь не авторизован')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Пользователь не авторизован')

        user = User.objects.filter(id=payload['id']).first()

        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        user = User.objects.filter(id=payload['id']).first()
        user.is_active = False
        user.save()
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'вышли успешно'
        }
        return response


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            content = form.cleaned_data['content']

            html = render_to_string('emails/contactform.html', {
                'name': name,
                'email': email,
                'content': content
            })

            send_mail('This is contact form subject',
                      'This is the message',
                      'd.ganiuly@bk.ru',
                      ['daniyal.ganiuly@gmail.com', 'd.ganiuly@bk.ru'],
                      html_message=html)

            return JsonResponse({"message": "success"})

    else:
        form = ContactForm()

    return render(request, 'index.html', {
        'form': form
    })


class SeansView(APIView):

    def get(self, request, *args, **kwargs):
        seans = get_object_or_404(Seans, pk=self.kwargs.get('id'))
        seans_serializer = SeansSerializer(seans)
        return Response(seans_serializer.data)


class TicketView(APIView):
    def get(self, request, *args, **kwargs):
        ticket = get_object_or_404(Ticket, pk=self.kwargs.get('id'))
        ticket_serializer = TicketSerializer(ticket)
        return Response(ticket_serializer.data)

    def post(self, request):
        ticket_data = JSONParser().parse(request)
        ticket_serializer = CreateTicketSerializer(data=ticket_data)
        if ticket_serializer.is_valid():
            ticket_serializer.save()
            return Response(ticket_serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class OrderView(APIView):
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs.get('id'))
        order_serializer = OrderSerializer(order)
        return Response(order_serializer.data)