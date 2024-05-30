from django.contrib.auth import authenticate
from datetime import datetime
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.users.authentication_mixins import Authentication
from apps.users.api.serializers import CustomUserSerializer
from apps.users.api.serializers import CustomTokenObtainPairSerializer
from apps.users.models import User

class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(username=username, password=password)
        if user:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                user_serializer = CustomUserSerializer(user)
                return Response({
                    'token': login_serializer.validated_data.get('access'),
                    'refresh_token': login_serializer.validated_data.get('refresh'),
                    'user': user_serializer.data,
                    'message': 'Inicio de Sesión Exitoso'
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Usuario o clave incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Usuario o clave incorrectos'}, status=status.HTTP_400_BAD_REQUEST)


class LogOut(GenericAPIView):
    def post(self, request, *args, **kwargs):
        user = User.objects.filter(id=request.data.get('user', ''))
        if user.exists():
            RefreshToken.for_user(user.first())
            return Response({'message':'Sesión cerrada correctamente'}, status=status.HTTP_200_OK)
        return Response({'error': 'No existe este usuario'}, status=status.HTTP_400_BAD_REQUEST)

# class UserToken(Authentication, APIView):
#     def get(self, request, *args, **kwargs):
#         try:
#             user_token, created = Token.objects.get_or_create(user = self.user)
#             user = UserTokeSerializer(self.user)
#             return Response({
#                 'token': user_token.key,
#                 'user': user.data
#             })
#         except Exception as e:
#             print(e)
#             return Response({
#                 'error': "Credenciales enviadas incorrectas."
#             }, status=status.HTTP_400_BAD_REQUEST)

# class Login(ObtainAuthToken):
    
#     def post(self, request, *args, **kwargs):
#         login_serializer = self.serializer_class(data=request.data, context={'request': request})
#         if login_serializer.is_valid():
#             user = login_serializer.validated_data['user']
#             if user.is_active:
#                 token,created = Token.objects.get_or_create(user=user)
#                 user_serializer = UserTokeSerializer(user)
#                 if created:
#                     return Response({
#                         "token":token.key,
#                         "user":user_serializer.data,
#                         "message": "Inicio de sesión exitoso"
#                     }, status=status.HTTP_201_CREATED)
#                 else:
#                     # Asi validas si hay sesiones para cerrarlas cuando alguien intente ingresar con tus datos
#                     all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
#                     if all_sessions.exists():
#                         for session in all_sessions:
#                             session_data = session.get_decoded()
#                             if user.id == int(session_data.get('_auth_user_id')):
#                                 session.delete()
#                     token.delete()
#                     token = Token.objects.create(user=user)
#                     return Response({
#                         "token":token.key,
#                         "user":user_serializer.data,
#                         "message": "Inicio de sesión exitoso"
#                     }, status=status.HTTP_201_CREATED)
#             else:
#                 return Response({"error":"El usuario no puede iniciar sesión"}, status=status.HTTP_401_UNAUTHORIZED)
#         else:
#             return Response({"error":"Usuario y/o contraseña incorrectos"}, status=status.HTTP_400_BAD_REQUEST)
#         return Response({"message":"Hola desde response"}, status=status.HTTP_200_OK)
    
# class LogOut(APIView):
    
#     def get(self, request, *args, **kwargs):
#         try:
#             token = request.GET.get('token')
#             print(token)
#             token = Token.objects.filter(key=token).first()
#             if token:
#                 user = token.user
#                 all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
#                 if all_sessions.exists():
#                     for session in all_sessions:
#                         session_data = session.get_decoded()
#                         if user.id == int(session_data.get('_auth_user_id')):
#                             session.delete()
#                 token.delete()
#                 session_message = 'Sesiones de usuario eliminadas.'
#                 token_message = 'Token Eliminado'
#                 return Response({'token_message': token_message, 'session_message': session_message}, status=status.HTTP_200_OK)
#             return Response({'error': 'No hay usuario con estas credenciales'}, status= status.HTTP_400_BAD_REQUEST)
#         except:
#             return Response({'error': 'No se ha encontrado token en la petición'}, status= status.HTTP_409_CONFLICT)