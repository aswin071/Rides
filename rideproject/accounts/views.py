from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
import jwt,datetime
from .models import Account

# Create your views here.


class RegisterView(APIView):
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        
        if 'email' not in request.data or 'password' not in request.data:
            raise AuthenticationFailed('Please provide both email and password.')

        email = request.data['email']
        password = request.data['password']

        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            raise AuthenticationFailed('User not found.')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password.')

        # Generate JWT payload
        payload = {
            'user_id': user.id,
            'email': user.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        # Create JWT token
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response =Response()

        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data={
            'jwt': token}
        return response

class LogoutView(APIView):

    def post(self,request):
        response=Response()
        response.delete_cookie('jwt')
        response.data ={
            'message':'Success'
        }
        return response

class UserView(APIView):

    def get(self,request):
        token=request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload= jwt.decode(token,'secret',algorthm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user=User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)
        return Response(token)

