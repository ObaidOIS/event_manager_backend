from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Event, ExternalUser
from .serializers import EventSerializer, ExternalUserSerializer, UserSerializer
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User



@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    try:
        data = request.data
        username = data["username"]
        email = data["email"]
        password = data["password"]
        if not username or not password or not email:
            return Response({'error': 'UserName, Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username is already taken'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email is already taken'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()
        return Response({'email': user.email}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_users(request):
    try:
        user = User.objects.get(id=request.user.id)
        details = UserSerializer(user)
        return Response(details.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_events(request):
    try:
        user = request.user
        event_list = []
        events = Event.objects.all().filter(user=user)
        invited_events = ExternalUser.objects.filter(email=user.email).values_list('events', flat=True)
        # get objects of the invited events
        for event in invited_events:
            event_list.append(Event.objects.get(id=event))
        for event in events:
            event_list.append(event)

        serializer = EventSerializer(event_list, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def create_event(request):
    try:
        user = request.user
        data = request.data
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_event(request, pk):
    try:
        event = get_object_or_404(Event, pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

from datetime import datetime


@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
def update_event(request, pk):
    try:
       # Convert date string to datetime object
        if 'date' in request.data:
            try:
                request.data['date'] = datetime.strptime(request.data['date'], '%Y-%m-%dT%H:%M:%SZ')
            except ValueError:
                try:
                    request.data['date'] = datetime.strptime(request.data['date'], '%Y-%m-%dT%H:%M')
                except ValueError:
                    return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)
        event = get_object_or_404(Event, pk=pk)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
def delete_event(request, pk):
    try:
        event = get_object_or_404(Event, pk=pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def invite_user(request, pk):
    try:
        event = get_object_or_404(Event, pk=pk)
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        external_user, created = ExternalUser.objects.get_or_create(email=email)
        external_user.events.add(event)
        external_user.save()

        # Send invitation email
        subject = f'Invitation to Event: {event.title}'
        message = f'''
        You have been invited to the event: {event.title}
        Date: {event.date}
        Location: {event.location}

        Please login to your account to view the event details.
        http://localhost:3000/login
        '''

        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

        serializer = ExternalUserSerializer(external_user)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
def get_invited_users(request, pk):
    try:
        event = get_object_or_404(Event, pk=pk)
        external_users = ExternalUser.objects.filter(events=event)
        users = [user.email for user in external_users]
        return Response(users)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
