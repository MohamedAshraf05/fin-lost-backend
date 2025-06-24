from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import ItemType, Ad, ChatMessage, AdInteractionHistory, UserRating

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    # Do NOT include location in the fieldsets
    fieldsets = BaseUserAdmin.fieldsets  # unchanged from default

    # Optionally remove location from list display and search fields
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

@admin.register(ItemType)
class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'item_type', 'status', 'is_resolved', 'created_at')
    list_filter = ('status', 'item_type', 'is_resolved')
    search_fields = ('title', 'comments', 'location_description')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'recipient', 'ad', 'message', 'timestamp', 'is_read')
    search_fields = ('message',)

@admin.register(AdInteractionHistory)
class AdInteractionHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ad', 'interaction_type', 'timestamp')
    list_filter = ('interaction_type',)

@admin.register(UserRating)
class UserRatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'rater', 'rated_user', 'ad', 'rating', 'created_at')
    search_fields = ('review',)
