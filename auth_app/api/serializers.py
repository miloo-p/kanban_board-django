from rest_framework import serializers
from django.contrib.auth.models import User
from auth_app.models import UserProfile


class RegistrationSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def save(self):
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']

        if pw != repeated_pw:
            raise serializers.ValidationError(
                {'error': 'Passwords dont match. Please try again!'})

        account = User(
            email=self.validated_data['email'],
            username=self.validated_data['email']
        )
        account.set_password(pw)
        account.save()

        UserProfile.objects.create(
            user=account,
            fullname=self.validated_data['fullname']
        )

        return account
