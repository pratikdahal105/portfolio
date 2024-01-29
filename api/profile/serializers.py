import re
from django.contrib.auth.models import User
from rest_framework import serializers, validators
from django.contrib.auth.hashers import check_password
from user_profile.models import Profile
from django.core.validators import RegexValidator

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("full_name", "phone_number", "address", "picture", "bio", "verified_at", "status")

class UserRegistrationSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ("username", "password", "email", "profile")
    
        extra_kwargs = {
            "password": {
                "write_only": True,
                "validators": [
                    RegexValidator(
                        regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_])[a-zA-Z\d\W_]{6,}$',
                        message="Password must contain at least one uppercase letter, one lowercase letter, and one digit."
                    ),
                ],
            },
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        queryset=User.objects.all(),
                        message="Email Already Exists"
                    )
                ],
            },
        }

    def create(self, validated_data):
        profile_data = validated_data.pop("profile", {})

        user, created = User.objects.get_or_create(
            username=validated_data["username"],
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])
        user.save()

        if profile_data:
            profile, _ = Profile.objects.get_or_create(user=user)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return user
    
class UserProfileUpdateSerializer(UserRegistrationSerializer):
    class Meta(UserRegistrationSerializer.Meta):
        fields = ("username", "email", "profile")
        read_only_fields = ("username", "password")

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[
        RegexValidator(
            regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_])[a-zA-Z\d\W_]{6,}$',
            message="New password must contain at least one uppercase letter, one lowercase letter, and one digit."
        ),
    ])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not check_password(value, user.password):
            raise serializers.ValidationError("Old password is incorrect")
        return value


class CanadianPhoneNumberValidator:
    def __call__(self, value):
        pattern = re.compile(r'^\+?1?\d{10}$')
        if not pattern.match(value):
            raise serializers.ValidationError("Phone number must be a valid Canadian phone number.")
