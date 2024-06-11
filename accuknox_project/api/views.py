from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from django.core.cache import cache
from .serializers import UserSerializer, FriendRequestSerializer
from .models import FriendRequest

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Authenticate the user
    user = authenticate(request, email=email, password=password)
    
    if user:
        print("done")
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    
    # If authentication failed, check if the email exists
    if not User.objects.filter(email=email).exists():
        return Response({'error': 'Email not found.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response({'error': 'Invalid password.'}, status=status.HTTP_401_UNAUTHORIZED)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request_view(request):
    from_user = request.user
    to_user_id = request.data.get('to_user_id')
    to_user = get_object_or_404(User, id=to_user_id)

    if from_user == to_user:
        return Response({'error': 'You cannot send a friend request to yourself.'}, status=status.HTTP_400_BAD_REQUEST)

    cache_key = f"{from_user.id}_friend_requests"
    requests_in_last_minute = cache.get(cache_key, 0)
    if requests_in_last_minute >= 3:
        return Response({'error': 'You can only send 3 friend requests per minute.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

    friend_request, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user=to_user)

    if not created:
        if friend_request.status == 'accepted':
            return Response({'error': 'You are already friends with this user.'}, status=status.HTTP_400_BAD_REQUEST)
        elif friend_request.status == 'pending':
            return Response({'error': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)

    friend_request.status = 'pending'
    friend_request.save()

    cache.set(cache_key, requests_in_last_minute + 1, timeout=60)

    return Response({'success': 'Friend request sent successfully.'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_friend_request_view(request, pk):
    friend_request = get_object_or_404(FriendRequest, pk=pk)
    if friend_request.to_user != request.user:
        return Response({'error': 'You do not have permission to accept this friend request.'}, status=status.HTTP_403_FORBIDDEN)
    
    friend_request.status = 'accepted'
    friend_request.save()
    return Response({'success': 'Friend request accepted.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_friend_request_view(request, pk):
    friend_request = get_object_or_404(FriendRequest, pk=pk)
    if friend_request.to_user != request.user:
        return Response({'error': 'You do not have permission to reject this friend request.'}, status=status.HTTP_403_FORBIDDEN)
    
    friend_request.status = 'rejected'
    friend_request.save()
    return Response({'success': 'Friend request rejected.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_friends_view(request):
    user = request.user
    friends_ids = FriendRequest.objects.filter(
        Q(from_user=user, status='accepted') | Q(to_user=user, status='accepted')
    ).values_list('from_user_id', 'to_user_id')
    friends_ids = [id for ids in friends_ids for id in ids if id != user.id]
    friends = User.objects.filter(id__in=friends_ids)
    serializer = UserSerializer(friends, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_pending_requests_view(request):
    user = request.user
    pending_requests = FriendRequest.objects.filter(to_user=user, status='pending')
    serializer = FriendRequestSerializer(pending_requests, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_users_view(request):
    query = request.query_params.get('q', '')
    if not query:
        return Response({'error': 'Query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if '@' in query:
        users = User.objects.filter(email__iexact=query)
    else:
        users = User.objects.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        )
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
