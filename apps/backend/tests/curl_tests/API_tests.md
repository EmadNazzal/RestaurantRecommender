# Django REST API Testing with `curl`

This document describes the process and results of testing the Django REST API endpoints using `curl`. The testing covers user registration, login, accessing protected resources, refreshing tokens, and more.

## Installing `curl`

`curl` is a command-line tool used for transferring data to or from a server, supporting various protocols like HTTP, HTTPS, FTP, and more.

Install `curl` with:

## Test Scenarios

1. User Registration
2. User Login
3. Accessing Protected Resource
4. Refreshing Token
5. Logging Out
6. Bookmark Operations
7. Profile Operations
8. Testing CORS

### 1. User Registration

**`curl` Command**:

```bash
curl -X POST http://127.0.0.1:8000/api/register/ -H "Content-Type: application/json" -d '{
    "first_name": "John",
    "surname": "Doe",
    "email": "john.doe@example.com",
    "password": "password123"
}'
```

**Expected Output**:

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
    "id": 1,
    "first_name": "John",
    "surname": "Doe",
    "email": "john.doe@example.com",
    "date_joined": "2024-07-08T21:46:58.123456Z"
}
```

### 2. User Login

**`curl` Command**:

```bash
curl -X POST http://127.0.0.1:8000/api/login/ -H "Content-Type: application/json" -d '{"email": "user@user.com", "password": "1securepassword", "remember_me": true}'
```

**Expected Output**:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 3. Accessing Authenticated Resource

**`curl` Command**:

```bash
curl -X GET http://127.0.0.1:8000/api/authenticated-resour es/ -H "Authorization: Bearer <access_token>"
```

**Expected Output**:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "detail": "Authentication credentials were not provided."
}
```

### 4. Refreshing Token

**`curl` Command**:

```bash
curl -X POST http://127.0.0.1:8000/api/token/refresh/ -H "Content-Type: application/json" -d '{"refresh": "<refresh_token>"}'
```

**Expected Output**:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "access": "new_access_token"
}
```

### 5. Logging Out

**`curl` Command**:

```bash
curl -X POST http://127.0.0.1:8000/api/logout/ -H "Content-Type: application/json" -d '{"refresh": "<refresh_token>"}'
```

**Expected Output**:

```http
HTTP/1.1 205 Reset Content
```

### 6. Bookmark Operations

#### Create Bookmark

**`curl` Command**:

```bash
curl -X POST http://localhost:8000/api/bookmarks/ -H "Content-Type: application/json" -H "Authorization: Bearer <access_token>" -d '{"restaurant_ids": [2925]}'
```

**Expected Output**:

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
    "id": 33,
    "user": 38,
    "restaurants": [
        {
            "id": 2925,
            "restaurant_name": "Example Restaurant",
            "primary_cuisine": "Example Cuisine",
            "overall_rating": 4.5,
            "neighborhood": "Example Neighborhood",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "zone": "Example Zone",
            "aspects": [
                {
                    "id": 41134,
                    "aspect": "service",
                    "rating_type": "positive",
                    "count": 178,
                    "restaurant": 2925
                },
                {
                    "id": 41135,
                    "aspect": "food",
                    "rating_type": "positive",
                    "count": 165,
                    "restaurant": 2925
                }
                // Other aspects
            ]
        }
    ]
}
```

#### Get All Bookmarks

**`curl` Command**:

```bash
curl -X GET http://localhost:8000/api/bookmarks/ -H "Authorization: Bearer <access_token>"
```

**Expected Output**:

```http
HTTP/1.1 200 OK
Content-Type: application/json

[
    {
        "id": 33,
        "user": 38,
        "restaurants": [
            {
                "id": 2925,
                "restaurant_name": "Example Restaurant",
                "primary_cuisine": "Example Cuisine",
                "overall_rating": 4.5,
                "neighborhood": "Example Neighborhood",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "zone": "Example Zone",
                "aspects": [
                    {
                        "id": 41134,
                        "aspect": "service",
                        "rating_type": "positive",
                        "count": 178,
                        "restaurant": 2925
                    },
                    {
                        "id": 41135,
                        "aspect": "food",
                        "rating_type": "positive",
                        "count": 165,
                        "restaurant": 2925
                    }
                    // Other aspects
                ]
            }
        ]
    }
]
```

#### Get a Specific Bookmark

**`curl` Command**:

```bash
curl -X GET http://localhost:8000/api/bookmarks/34/ -H "Authorization: Bearer <access_token>"
```

**Expected Output**:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": 34,
    "user": 38,
    "restaurants": [
        {
            "id": 2925,
            "restaurant_name": "Example Restaurant",
            "primary_cuisine": "Example Cuisine",
            "overall_rating": 4.5,
            "neighborhood": "Example Neighborhood",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "zone": "Example Zone",
            "aspects": [
                {
                    "id": 41134,
                    "aspect": "service",
                    "rating_type": "positive",
                    "count": 178,
                    "restaurant": 2925
                },
                {
                    "id": 41135,
                    "aspect": "food",
                    "rating_type": "positive",
                    "count": 165,
                    "restaurant": 2925
                }
                // Other aspects
            ]
        }
    ]
}
```

#### Update Bookmark

**`curl` Command**:

```bash
curl -X PUT http://localhost:8000/api/bookmarks/34/ -H "Content-Type: application/json" -H "Authorization: Bearer <access_token>" -d '{"restaurant_ids": [2926]}'
```

**Expected Output**:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": 34,
    "user": 38,
    "restaurants": [
        {
            "id": 2926,
            "restaurant_name": "New Example Restaurant",
            "primary_cuisine": "New Example Cuisine",
            "overall_rating": 4.6,
            "neighborhood": "New Example Neighborhood",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "zone": "New Example Zone",
            "aspects": [
                {
                    "id": 41136,
                    "aspect": "service",
                    "rating_type": "positive",
                    "count": 180,
                    "restaurant": 2926
                },
                {
                    "id": 41137,
                    "aspect": "food",
                    "rating_type": "positive",
                    "count": 167,
                    "restaurant": 2926
                }
                // Other aspects
            ]
        }
    ]
}
```

#### Delete Bookmark

**`curl` Command**:

```bash
curl -X DELETE http://localhost:8000/api/bookmarks/34/ -H "Authorization: Bearer <access_token>"
```

**Expected Output**:

```http
HTTP/1.1 204 No Content
```

### 7. Profile Operations

#### Get Profile

**`curl` Command**:

```bash
curl -X GET http://localhost:8000/api/profile/ -H "Authorization: Bearer <access_token>"
```

**Expected Output**:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": 1,
    "user": 38,
    "first_name": "John",
   

 "surname": "Doe",
    "email": "john.doe@example.com",
    "avatar": "default.jpg"
}
```

#### Update Profile

**`curl` Command**:

```bash
curl -X PUT http://localhost:8000/api/profile/ -H "Content-Type: application/json" -H "Authorization: Bearer <access_token>" -d '{"first_name": "Jane", "surname": "Doe", "avatar": "new_avatar.jpg"}'
```

**Expected Output**:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": 1,
    "user": 38,
    "first_name": "Jane",
    "surname": "Doe",
    "email": "john.doe@example.com",
    "avatar": "new_avatar.jpg"
}
```

#### Delete Profile

**`curl` Command**:

```bash
curl -X DELETE http://localhost:8000/api/profile/ -H "Authorization: Bearer <access_token>"
```

**Expected Output**:

```http
HTTP/1.1 204 No Content
```

### 8. Testing CORS

#### Preflight Request (OPTIONS)

**`curl` Command**:

```bash
curl -X OPTIONS -i \
  -H "Origin: https://nibbler.rest/api/" \
  -H "Access-Control-Request-Method: GET" \
  -H "Access-Control-Request-Headers: X-Custom-Header" \
  http://127.0.0.1:8000/api/protected-resource/
```

**Expected Output**:

```http
HTTP/1.1 204 No Content
Access-Control-Allow-Origin: https://nibbler.rest/api/
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: X-Custom-Header
```

#### Actual Request (GET)

**`curl` Command**:

```bash
curl -X GET -i \
  -H "Origin: https://nibbler.rest/api/" \
  -H "X-Custom-Header: value" \
  http://127.0.0.1:8000/api/auhtenticated-resource/
```

**Expected Output**:

```http
HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://nibbler.rest/api/
Content-Type: application/json

{
    "detail": "Authentication credentials were not provided."
}
```
