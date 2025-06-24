from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .models import ItemType, Ad, ChatMessage, AdInteractionHistory, UserRating



User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'location', 'average_rating']

# Sign Up
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            # role=validated_data['role']
        )
        return user

# Login
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        tokens = RefreshToken.for_user(user)
        return {
            "user": {
                "id": user.id,
                "username": user.username,
                # "role": user.role
            },
            "tokens": {
                "refresh": str(tokens),
                "access": str(tokens.access_token),
            },
        }
    
# Tokens for blacklist
class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()



class ItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemType
        fields = ['id', 'name']

class AdSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    item_type = ItemTypeSerializer(read_only=True)
    item_type_id = serializers.PrimaryKeyRelatedField(
        queryset=ItemType.objects.all(), source='item_type', write_only=True
    )

    class Meta:
        model = Ad
        fields = [
            'id', 'user', 'title', 'item_type', 'item_type_id', 'status',
            'location_description', 'exact_address', 'transportation_type',
            'date_time', 'comments', 'image', 'is_resolved', 'created_at'
        ]

class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'recipient', 'ad', 'message', 'timestamp', 'is_read']

class AdInteractionHistorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = AdInteractionHistory
        fields = ['id', 'user', 'ad', 'interaction_type', 'timestamp']

class UserRatingSerializer(serializers.ModelSerializer):
    rater = UserSerializer(read_only=True)
    rated_user = UserSerializer(read_only=True)

    class Meta:
        model = UserRating
        fields = ['id', 'rater', 'rated_user', 'ad', 'rating', 'review', 'created_at']

    def validate(self, data):
        ad = data.get('ad')
        if ad and not ad.is_resolved:
            raise serializers.ValidationError("You can only rate resolved ads.")
        return data
