# Aqui es donde se trata el modelo como un formato JSON
from rest_framework import serializers
from apps.users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'last_name')

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'username': instance['username'],
            'email': instance['email'],
            'name': instance['name'],
            'last_name': instance['last_name']
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__' # Asi si quieres todos los campos del modelo, para especificar debes colocar array ['name', 'classname']

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password']) # Asi encriptas una clave
        user.save()
        return user
    
class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)
    passwordDos = serializers.CharField(max_length=128, min_length=6, write_only=True)

    def validate(self, data):
        if data['password'] != data['passwordDos']:
            raise serializers.ValidationError({'password':"Las contraseñas no coinciden"})
        return data

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'last_name')

    def update(self, instance, validated_data):
        updated_user = super().update(instance, validated_data) # Asi actualizas los campos que te envien sin tener que especificar
        updated_user.save()
        return updated_user

    
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__' # Asi si quieres todos los campos del modelo, para especificar debes colocar array ['name', 'classname']

    def to_representation(self, instance): # Asi representas la información como tu gustes
        # return super().to_representation(instance) # Asi se muestran todos de una vez con to_representation
        return { # Si lo haces asi en la API debes especificar estos campos
            'id': instance.id,
            'username': instance.username,
            'email': instance.email,
            'password': instance.password
        }

class TestUserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    email = serializers.EmailField()

    # Las validaciones se recomiendan colocarlas en su respectivo metodo create o update porque a veces pueden ser especificas
    
    def validate_name(self, value):
        # if value != "María José":
        #     raise serializers.ValidationError('Error')
        return value
    
    def validate_email(self, value):
        return value
    
    def validate(self, data):
        # if data['name'] in data['email']:
        #     raise serializers.ValidationError('Error general')
        return data
    
    def create(self, validated_data):
        return User.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance