# Mini Social App API Documentation

A simple social media application that demonstrates basic API concepts including authentication, database integration, and frontend-backend communication.

## Features

- User registration and authentication
- Post creation and retrieval
- Token-based authentication
- SQLite database storage
- Simple frontend interface

## Getting Started

### Prerequisites

- Python 3.x
- SQLite3

### Installation

1. Clone the repository
2. Navigate to the project directory
3. Run the server:
   ```bash
   python server.py
   ```
4. Access the application at `http://localhost:8000`

## API Endpoints

### Authentication

#### Register a New User

- **URL:** `/register`
- **Method:** `POST`
- **Content-Type:** `application/json`
- **Data Params:**
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Success Response:**
  - **Code:** 201
  - **Content:**
    ```json
    {
      "message": "Registered"
    }
    ```
- **Error Response:**
  - **Code:** 400
  - **Content:**
    ```json
    {
      "error": "Username already exists"
    }
    ```

#### User Login

- **URL:** `/login`
- **Method:** `POST`
- **Content-Type:** `application/json`
- **Data Params:**
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    {
      "token": "string"
    }
    ```
- **Error Response:**
  - **Code:** 401
  - **Content:**
    ```json
    {
      "error": "Invalid credentials"
    }
    ```

### Posts

#### Get All Posts

- **URL:** `/api/posts`
- **Method:** `GET`
- **Success Response:**
  - **Code:** 200
  - **Content:**
    ```json
    [
      {
        "user": "string",
        "msg": "string"
      }
    ]
    ```

#### Create New Post

- **URL:** `/api/posts`
- **Method:** `POST`
- **Headers Required:**
  - `Authorization: Bearer <token>`
- **Content-Type:** `application/json`
- **Data Params:**
  ```json
  {
    "message": "string"
  }
  ```
- **Success Response:**
  - **Code:** 201
  - **Content:**
    ```json
    {
      "id": "number",
      "message": "Post created"
    }
    ```
- **Error Response:**
  - **Code:** 401
  - **Content:**
    ```json
    {
      "error": "Unauthorized"
    }
    ```

## Database Schema

### Users Table

```sql
CREATE TABLE users (
    username TEXT PRIMARY KEY,
    password TEXT
);
```

### Posts Table

```sql
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    message TEXT
);
```

## Frontend Pages

1. `/login` - User login page
2. `/register` - New user registration
3. `/posts` - Main posts feed

## Security Notes

Current implementation is basic and includes:

- Simple token-based authentication
- SQLite database storage
- Basic error handling

For production use, consider implementing:

- Password hashing
- Input validation
- Rate limiting
- HTTPS
- Session management
- Proper error handling

## Project Structure

```
api-final-project/
├── README.md
├── server.py        # Main server implementation
├── app.db          # SQLite database
├── login.html      # Login page
├── register.html   # Registration page
└── posts.html      # Posts feed page
```

## Contributing

This is a learning project demonstrating basic API concepts. Feel free to suggest improvements or submit pull requests.

## Learning Resources

- [HTTP Methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)
- [REST API Best Practices](https://restfulapi.net/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Python HTTP Server](https://docs.python.org/3/library/http.server.html)
