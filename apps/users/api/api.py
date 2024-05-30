from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.users.models import User
from apps.users.api.serializers import UserSerializer, UserListSerializer, UpdateUserSerializer, PasswordSerializer

class UserViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer
    list_serializer_class = UserListSerializer
    update_serializer_class = UpdateUserSerializer
    queryset = None

    def get_object(self, pk):
        return get_object_or_404(self.serializer_class.Meta.model, pk=pk)

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.serializer_class().Meta.model.objects.filter(is_active=True).values('id', 'username', 'email', 'name', 'last_name')
        return self.queryset

    # Asi añades un detalle mas a tu ruta para ejecutar una accion nueva, el param url_path permite ponerle el nombre que quieras
    @action(detail=True, methods=['post'])
    def set_password(self, request, pk=None):
        user = self.get_object(pk)
        password_serializer = PasswordSerializer(data=request.data)
        if password_serializer.is_valid():
            user.set_password(password_serializer.validated_data['password'])
            user.save()
            return Response({
                'message': 'Contraseña actualizada correctamente'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'message': 'Errores en la información enviada',
                'error': password_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    
    def list(self, request):
        users = self.get_queryset()
        user_serializer = self.list_serializer_class(users, many=True)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                'message': 'Usuario registrado correctamente'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'message': 'Errores en el registro',
                'errors': user_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = self.serializer_class(user)
        return Response(user_serializer.data)
    
    def update(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = self.update_serializer_class(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                'message': 'Usuario actualizado correctamente'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'message': 'Errores en la actualización',
                'errors': user_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):
        user_destroy = self.serializer_class.Meta.model.objects.filter(id=pk).update(is_active=False)
        if user_destroy == 1:
            return Response({
                'message': 'Usuario eliminado correctamente'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'message': 'Errores en la eliminación',
                'errors': user_destroy.errors
            }, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['GET', 'POST'])
# def user_api_view(request):
    
#     # Select all
#     if request.method == 'GET':
#         # users = User.objects.all()
#         users = User.objects.all().values('id', 'username', 'email', 'password') # Asi optimizas tu consulta con el serializador
#         users_serializer = UserListSerializer(users, many=True)

#         # test_data = {
#         #     'name': 'María José',
#         #     'email': 'majo@gmail.com'
#         # }

#         # test_user = TestUserSerializer(data= test_data)

#         # if test_user.is_valid():
#         #     user_instance = test_user.save()
#         #     print(user_instance)
#         # else:
#         #     print(test_user.errors)

#         return Response(users_serializer.data, status=status.HTTP_200_OK)
    
#     # Create
#     elif request.method == 'POST':
#         user_serializer = UserSerializer(data = request.data)

#         #Validate
#         if user_serializer.is_valid():
#             user_serializer.save()
#             return Response({'message': 'User created!'}, status=status.HTTP_201_CREATED)
#         return Response({'message': "User couldn't be created!"}, status=status.HTTP_400_BAD_REQUEST)
    
# @api_view(['GET', 'PUT', 'DELETE'])
# def user_detail_view(request, pk): # El pk viene siendo ese parametro que le mandas en la URL
    
#     # user = User.objects.filter(id = pk).first() # La consulta del detalle de usuario
#     user = User.objects.filter(id = pk).first() # Asi optimizas la consulta aqui tambien con el serializador

#     if user:
#         # Select one
#         if request.method == 'GET':
#             user_serializer = UserSerializer(user)
#             return Response(user_serializer.data, status=status.HTTP_200_OK)
        
#         #Update
#         elif request.method == 'PUT':
#             user_serializer = UserSerializer(user, data=request.data)
#             # user_serializer = TestUserSerializer(user, data=request.data)
#             if user_serializer.is_valid():
#                 user_serializer.save()
#                 return Response({'message': 'User updated!'}, status=status.HTTP_200_OK)
#             return Response({'message': "User couldn't be updated!"}, status=status.HTTP_400_BAD_REQUEST)

#         elif request.method == 'DELETE':
#             user.delete()
#             return Response({'message': 'User Deleted!'}, status=status.HTTP_200_OK)
    
#     return Response({'message': 'User not found!'}, status=status.HTTP_400_BAD_REQUEST)