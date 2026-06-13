from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError('用户名或密码错误')
        if not user.is_active:
            raise serializers.ValidationError('账号已被禁用')
        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=6)

    def validate_old_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('原密码错误')
        return value

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()


class UserSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'role_display', 'phone', 'department', 'department_name',
            'is_active', 'date_joined', 'last_login',
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']

    def create(self, validated_data):
        password = validated_data.pop('password', None) if 'password' in validated_data else '123456'
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserCreateSerializer(UserSerializer):
    password = serializers.CharField(write_only=True, min_length=6, default='123456')

    class Meta(UserSerializer.Meta):
        pass


class UserUpdateSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        pass
