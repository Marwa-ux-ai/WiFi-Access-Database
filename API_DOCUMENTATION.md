# API Documentation

## Authentication

To access the API, you must provide a valid API key in the header of your requests:

```
Authorization: Bearer <your_api_key>
```

## Endpoints

### 1. Get All WiFi Access Points
- **Endpoint:** `/api/access_points`
- **Method:** `GET`
- **Description:** Retrieve a list of all WiFi access points.
- **Response Codes:**
  - `200`: OK
  - `401`: Unauthorized
  - `404`: Not Found

#### Example Request
```
GET /api/access_points HTTP/1.1
Authorization: Bearer your_api_key
```

#### Example Response
```json
[
  {
    "id": 1,
    "ssid": "WiFi-1",
    "location": "Building A"
  },
  {
    "id": 2,
    "ssid": "WiFi-2",
    "location": "Building B"
  }
]
```

### 2. Add a New WiFi Access Point
- **Endpoint:** `/api/access_points`
- **Method:** `POST`
- **Description:** Add a new WiFi access point.
- **Request Body:**
```json
{
  "ssid": "New WiFi",
  "location": "Building C"
}
```
- **Response Codes:**
  - `201`: Created
  - `400`: Bad Request
  - `401`: Unauthorized

#### Example Request
```
POST /api/access_points HTTP/1.1
Content-Type: application/json
Authorization: Bearer your_api_key

{
  "ssid": "New WiFi",
  "location": "Building C"
}
```

#### Example Response
```json
{
  "id": 3,
  "ssid": "New WiFi",
  "location": "Building C"
}
```

### 3. Delete a WiFi Access Point
- **Endpoint:** `/api/access_points/{id}`
- **Method:** `DELETE`
- **Description:** Delete a specific WiFi access point by ID.
- **Response Codes:**
  - `204`: No Content
  - `401`: Unauthorized
  - `404`: Not Found

#### Example Request
```
DELETE /api/access_points/1 HTTP/1.1
Authorization: Bearer your_api_key
```

#### Example Response
```
(No Content)
```

## Conclusion
This documentation provides a comprehensive overview of the API for managing WiFi access points. Make sure to secure your API key and keep it confidential.
