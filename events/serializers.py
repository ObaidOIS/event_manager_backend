from rest_framework import serializers
from .models import Event, ExternalUser
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'user', 'title', 'description', 'date', 'location', 'reminder', 'invited_users']
        read_only_fields = ('user', 'invited_users')

    def validate_date(self, value):
        """
        Validate that the date is in the future.
        """
        if value < timezone.now():
            raise serializers.ValidationError("Date must be in the future.")
        return value
    
    def create(self, validated_data):
        """
        Create and return a new `Event` instance, given the validated data.
        """
        return Event.objects.create(**validated_data)
    def update(self, instance, validated_data):
        """
        Update and return an existing `Event` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.date = validated_data.get('date', instance.date)
        instance.location = validated_data.get('location', instance.location)
        instance.reminder = validated_data.get('reminder', instance.reminder)
        instance.save()
        return instance

class ExternalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalUser
        fields = ['email', 'events']

    def create(self, validated_data):
        events = validated_data.pop('events', [])
        external_user = ExternalUser.objects.create(**validated_data)
        external_user.events.set(events)
        return external_user
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
