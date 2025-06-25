# Implement Testing and Validation of the Endpoints

## User:

### Create user
```bash
curl -X 'POST' \
  'http://127.0.0.1:5000/api/v1/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}'
```
### 201 Response
```bash
{
  "id": "cc5706a7-4f93-4700-921f-1c3f90704c8b",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com"
}
```
### Create user(invalid data)
```bash
curl -X 'POST' \
  'http://127.0.0.1:5000/api/v1/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "first_name": "",
    "last_name": "",
    "email": "invalid-email"
}'
```
### 400 Error: BAD REQUEST
```bash
{
  "error": "First name is required and must be 50 characters or fewer"
}
```
### Create user(invalid email)
```bash
curl -X 'POST' \
  'http://127.0.0.1:5000/api/v1/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "invalid-email"
}'
```
### 400 Error: BAD REQUEST
```bash
{
  "error": "Email must be valid and properly formatted"
}
```
## Amenity:
```bash
curl -X 'POST' \
  'http://127.0.0.1:5000/api/v1/amenities/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Wi-Fi"
}'
```
### 201 Response
```bash
{
  "id": "60036cf9-2083-41b4-a970-538a4ae5cd1c",
  "name": "Wi-Fi"
}
```

## Place:

### Create place
```bash
curl -X POST http://localhost:5000/api/v1/places/ \
-H "Content-Type: application/json" \
-d '{
  "title": "Cozy Apartment",
  "description": "A nice place to stay",
  "price": 120.0,
  "latitude": 40.7128,
  "longitude": -74.0060,
  "owner_id": "cc5706a7-4f93-4700-921f-1c3f90704c8b",
  "amenities": ["60036cf9-2083-41b4-a970-538a4ae5cd1c", "2042b796-9bb2-48de-951a-b9352d795db4"]
}'
```
### 201 Response
```bash
{
  "id": "84adff24-3695-48d3-b91a-74ace3d4f62a",
  "title": "Cozy Apartment",
  "description": "A nice place to stay",
  "price": 120.0,
  "latitude": 40.7128,
  "longitude": -74.006,
  "ownder_id": "cc5706a7-4f93-4700-921f-1c3f90704c8b"
}
```
### Create place(empty title)
```bash
curl -X POST http://localhost:5000/api/v1/places/ \
-H "Content-Type: application/json" \
-d '{
  "title": "",
  "description": "A nice place to stay",
  "price": 120.0,
  "latitude": 40.7128,
  "longitude": -74.0060,
  "owner_id": "cc5706a7-4f93-4700-921f-1c3f90704c8b",
  "amenities": ["60036cf9-2083-41b4-a970-538a4ae5cd1c", "2042b796-9bb2-48de-951a-b9352d795db4"]
}'
```
### 400 Error: BAD REQUEST
```bash
{"error": "Title cannot be empty"}
```
### Create place(negative price)
```bash
curl -X POST http://localhost:5000/api/v1/places/ \
-H "Content-Type: application/json" \
-d '{
  "title": "Cozy Apartment",
  "description": "A nice place to stay",
  "price": -100.0,
  "latitude": 40.7128,
  "longitude": -74.0060,
  "owner_id": "cc5706a7-4f93-4700-921f-1c3f90704c8b",
  "amenities": ["60036cf9-2083-41b4-a970-538a4ae5cd1c", "2042b796-9bb2-48de-951a-b9352d795db4"]
}'
```
### 400 Error: BAD REQUEST
```bash
{"error": "Price must be positive"}
```
### Create place(Latitude Out of range)
```bash
curl -X POST http://localhost:5000/api/v1/places/ \
-H "Content-Type: application/json" \
-d '{
  "title": "Cozy Apartment",
  "description": "A nice place to stay",
  "price": 120.0,
  "latitude": 100.7128,
  "longitude": -74.0060,
  "owner_id": "cc5706a7-4f93-4700-921f-1c3f90704c8b",
  "amenities": ["60036cf9-2083-41b4-a970-538a4ae5cd1c", "2042b796-9bb2-48de-951a-b9352d795db4"]
}'
```
### 400 Error: BAD REQUEST
```bash
{"error": "Latitude out of range"}
```
### Create place(Longitude Out of range)
```bash
curl -X POST http://localhost:5000/api/v1/places/ 
-H "Content-Type: application/json" 
-d '{
  "title": "Cozy Apartment",
  "description": "A nice place to stay",
  "price": 120.0,
  "latitude": 40.7128,
  "longitude": -274.0060,
  "owner_id": "cc5706a7-4f93-4700-921f-1c3f90704c8b",
  "amenities": ["60036cf9-2083-41b4-a970-538a4ae5cd1c", "2042b796-9bb2-48de-951a-b9352d795db4"]
}'
```
### 400 Error: BAD REQUEST
```bash
{"error": "Longitude out of range"}
```

## Review:

### Create review
```bash
curl -X POST http://localhost:5000/api/v1/reviews/ \
-H "Content-Type: application/json" \
-d '{"text": "Loved it", "rating": 5, "user_id": "cc5706a7-4f93-4700-921f-1c3f90704c8b", "place_id": "84adff24-3695-48d3-b91a-74ace3d4f62a"}'
```

### 201 Response
```bash
{
  "id": "f3720cf4-62dd-48ca-beb3-037eab3627c2",
  "text": "Loved it", "rating": 5,
  "user_id": "cc5706a7-4f93-4700-921f-1c3f90704c8b",
  "place_id": "84adff24-3695-48d3-b91a-74ace3d4f62a"
}
```
### Create review(Empty text)
```bash
curl -X POST http://localhost:5000/api/v1/reviews/ \
-H "Content-Type: application/json" \
-d '{"text": "", "rating": 5, "user_id": "cc5706a7-4f93-4700-921f-1c3f90704c8b", "place_id": "84adff24-3695-48d3-b91a-74ace3d4f62a"}'
```
### 400 Response
```bash
{"error": "Review text cannot be empty"}
```
### Search review by place
```bash
curl http://localhost:5000/api/v1/reviews/places/84adff24-3695-48d3-b91a-74ace3d4f62a/reviews
```
### 200 Response
```bash
[{"id": "f3720cf4-62dd-48ca-beb3-037eab3627c2", "text": "Loved it", "rating": 5}]
```
