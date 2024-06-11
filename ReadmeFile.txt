# Accuknox Social Network

# Description:-
This is a Django-based accuknox social network application that allows users to send and accept friend requests, list friends, and search for users.


#Endpoints

Register User: `POST /api/register/`
Allows users to register for the application.

Login User: `POST /api/login/`
Allows users to log in to the application.

Send Friend Request: `POST /api/send-friend-request/`
Allows authenticated users to send friend requests to other users.

Accept Friend Request: `POST /api/friend-requests/<friend_request_id>/accept/`
Allows authenticated users to accept a friend request.

Reject Friend Request: `POST /api/friend-requests/<friend_request_id>/reject/`
Allows authenticated users to reject a friend request.

List Friends: `GET /api/list-friends/`
Allows authenticated users to list their friends.

List Pending Requests: `GET /api/list-pending-requests/`
Allows authenticated users to list their pending friend requests.

Search Users: `GET /api/search-users/?q=query`
Allows authenticated users to search for other users by name or email.