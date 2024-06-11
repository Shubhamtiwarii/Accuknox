from django.urls import path
# from .views import register_view, login_view, search_users_view, send_friend_request_view, accept_friend_request_view, reject_friend_request_view, list_friends_view, list_pending_requests_view
from .views import (
    register_view, login_view, send_friend_request_view, accept_friend_request_view,
    reject_friend_request_view, list_friends_view, list_pending_requests_view,
    search_users_view
)

# urlpatterns = [
#     path('register/', register_view, name='register'),
#     path('login/', login_view, name='login'),
#     path('search/', search_users_view, name='search_users'),
#     path('friend-request/', send_friend_request_view, name='send_friend_request'),
#     path('friend-request/<int:pk>/accept/', accept_friend_request_view, name='accept_friend_request'),
#     path('friend-request/<int:pk>/reject/', reject_friend_request_view, name='reject_friend_request'),
#     path('friends/', list_friends_view, name='list_friends'),
#     path('pending-requests/', list_pending_requests_view, name='list_pending_requests'),
# ]

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('friend-request/send/', send_friend_request_view, name='send_friend_request'),
    path('friend-request/accept/<int:pk>/', accept_friend_request_view, name='accept_friend_request'),
    path('friend-request/reject/<int:pk>/', reject_friend_request_view, name='reject_friend_request'),
    path('friends/', list_friends_view, name='list_friends'),
    path('friend-requests/pending/', list_pending_requests_view, name='list_pending_requests'),
    path('search-users/', search_users_view, name='search_users'),
]