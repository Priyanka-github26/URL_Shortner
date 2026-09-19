# URL Shortener API

A simple and functional URL Shortener REST API built using Flask and SQLite.

This project allows users to:

- Create short URLs
- Redirect short URLs to original URLs
- Track URL click counts
- Set URL expiration times
- Create custom short codes
- View URL information
- Delete short URLs
- View all created short URLs
- Automatically test API functionality using pytest

## Features

- Create short URLs
- Automatic 6-character short code generation
- Custom short codes
- URL validation
- URL expiration
- Click tracking
- URL information API
- URL redirection
- Delete short URLs
- List all short URLs
- SQLite database
- Automated API testing with pytest
- Separate temporary database for tests

## Technologies Used

- Python
- Flask
- SQLite
- REST API
- pytest
- Postman
- Git & GitHub

## Installation and Setup

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
```

### 2. Open the project folder

```bash
cd URL_shortner
```

### 3. Install the required dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

The API will run at:

```text
http://127.0.0.1:5000
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/shorten` | Create a short URL |
| GET | `/info/<short_code>` | Get information about a short URL |
| GET | `/<short_code>` | Redirect to the original URL |
| DELETE | `/delete/<short_code>` | Delete a short URL |
| GET | `/urls` | Get all short URLs |
| GET | `/` | Check API status |

## API Usage

### 1. Create a Short URL

**Request**

```http
POST /shorten
Content-Type: application/json
```

**Request Body**

```json
{
    "url": "https://www.google.com"
}
```

**Example Response**

```json
{
    "message": "Short URL created successfully",
    "original_url": "https://www.google.com",
    "short_code": "abc123",
    "short_url": "http://localhost:5000/abc123",
    "created_at": "2026-09-19T15:00:00",
    "expires_at": null
}
```

### 2. Create a Short URL with Custom Code

**Request**

```http
POST /shorten
Content-Type: application/json
```

**Request Body**

```json
{
    "url": "https://www.google.com",
    "custom_code": "google"
}
```

The API will create:

```text
http://localhost:5000/google
```

The `custom_code` must be unique and contain only letters and numbers.

### 3. Create an Expiring Short URL

**Request**

```http
POST /shorten
Content-Type: application/json
```

**Request Body**

```json
{
    "url": "https://www.google.com",
    "expires_in": 60
}
```

Here, `expires_in` is the expiration time in seconds.

For example:

```text
60 seconds = 1 minute
```

After the expiration time, accessing the short URL will return:

```json
{
    "error": "Short URL has expired"
}
```

### What this documents

Your API supports **temporary short URLs**. For example, if:

```json
{
    "expires_in": 60
}
```

the URL expires after **60 seconds**.

### 4. Get URL Information

**Request**

```http
GET /info/abc123
```

This returns information about the short URL, including:

- Original URL
- Short code
- Click count
- Creation time
- Expiration time

### 5. Redirect to the Original URL

**Request**

```http
GET /abc123
```

When the short URL is opened, the API redirects the user to the original URL.

Each successful redirect increases the **click count by 1**.

### 6. Delete a Short URL

**Request**

```http
DELETE /delete/abc123
```

This permanently deletes the short URL from the database.

After deletion, trying to access the short URL will return a `404` response.

### 7. View All Short URLs

**Request**

```http
GET /urls
```

This endpoint returns all short URLs stored in the database.

**Example Response**

```json
{
    "count": 2,
    "urls": [
        {
            "short_code": "abc123",
            "original_url": "https://www.google.com",
            "clicks": 3,
            "created_at": "2026-09-19T15:00:00",
            "expires_at": null
        },
        {
            "short_code": "google",
            "original_url": "https://www.google.com",
            "clicks": 1,
            "created_at": "2026-09-19T15:05:00",
            "expires_at": null
        }
    ]
}
```
## Testing

This project uses **pytest** for automated API testing.

### Run Tests

```bash
python -m pytest -v
```

### Test Result

The project currently contains **11 automated tests** covering:

- Creating short URLs
- Missing URL validation
- Invalid URL validation
- URL type validation
- URL expiration
- Negative expiration values
- URL redirection
- Click counting
- URL deletion
- Getting all URLs
- Home/API status

Example result:

```text
11 passed
```

The tests use a **temporary SQLite database**, so running the test suite does not modify the main `urls.db` database.

## Project Structure

```text
URL_Shortner/
│
├── app.py
├── database.py
├── utils.py
├── requirements.txt
├── urls.db
├── README.md
│
└── test/
    ├── conftest.py
    ├── test_shorten.py
    ├── test_redirect.py
    ├── test_expiration.py
    └── test_delete.py
```

### File Description

| File | Description |
|------|-------------|
| `app.py` | Main Flask application and API routes |
| `database.py` | SQLite database connection and helper functions |
| `utils.py` | Short code generation utilities |
| `requirements.txt` | Python project dependencies |
| `urls.db` | SQLite database |
| `test/` | Automated API tests |
| `conftest.py` | Pytest fixture and temporary test database setup |
| `README.md` | Project documentation |

## Future Improvements

Possible improvements for this project include:

- User authentication and authorization
- Web-based frontend interface
- QR code generation for short URLs
- Advanced URL analytics
- Rate limiting
- API documentation using Swagger/OpenAPI
- Docker support
- Cloud database integration
- Deployment to a cloud platform