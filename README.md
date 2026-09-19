# 🔗 URL Shortener

A full-stack URL Shortener application built using **Python, Flask, SQLite, HTML, CSS and JavaScript**.

The application allows users to convert long URLs into short, shareable links and manage them through a web dashboard. It also provides REST APIs for creating, redirecting, tracking, listing and deleting shortened URLs.

---

## ✨ Features

- Create short URLs
- Automatic 6-character short code generation
- Custom short codes
- URL validation
- URL expiration
- Click tracking
- URL information API
- URL redirection
- Delete short URLs
- View all created URLs
- Search URLs
- Copy shortened URLs
- Analytics dashboard
- Active and expired URL status
- Responsive web interface
- SQLite database
- REST API
- Automated API testing using pytest
- Separate temporary database for tests

---

## 🛠️ Technologies Used

### Backend

- Python
- Flask
- SQLite
- REST API

### Frontend

- HTML
- CSS
- JavaScript

### Testing & Tools

- pytest
- Postman
- Git
- GitHub
- VS Code

---

## 📂 Project Structure

```text
URL_shortner/
│
├── app.py
├── database.py
├── utils.py
├── requirements.txt
├── urls.db
├── README.md
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
└── test/
    ├── conftest.py
    ├── test_shorten.py
    ├── test_redirect.py
    ├── test_expiration.py
    └── test_delete.py

🚀 Installation and Setup
1. Clone the Repository
git clone <your-github-repository-url>
2. Open the Project Folder
cd URL_shortner
3. Install Dependencies
pip install -r requirements.txt
4. Run the Application
python app.py

The application will start at:

http://127.0.0.1:5000

Open the URL in your browser to access the web dashboard.

🌐 Web Dashboard

The application includes a web-based dashboard for managing shortened URLs.

The dashboard provides:

Total URLs
Total clicks
Active URLs
Expired URLs
Search functionality
Copy shortened URL
Delete URL
URL creation date
URL expiration status
Click tracking
Responsive design

Users can enter a long URL and generate a shortened URL directly from the web interface.

🔌 REST API Endpoints
Method	Endpoint	Description
POST	/shorten	Create a short URL
GET	/info/<short_code>	Get information about a short URL
GET	/<short_code>	Redirect to the original URL
DELETE	/delete/<short_code>	Delete a short URL
GET	/urls	Get all short URLs
GET	/	Open the web dashboard
📡 API Usage
1. Create a Short URL
Request
POST /shorten
Content-Type: application/json
Request Body
{
    "url": "https://www.google.com"
}
Example Response
{
    "message": "Short URL created successfully",
    "original_url": "https://www.google.com",
    "short_code": "abc123",
    "short_url": "http://localhost:5000/abc123",
    "created_at": "2026-09-19T15:00:00",
    "expires_at": null
}

The API automatically generates a unique 6-character short code.

🔑 2. Create a Short URL with Custom Code
Request
POST /shorten
Content-Type: application/json
Request Body
{
    "url": "https://www.google.com",
    "custom_code": "google"
}

The API creates:

http://localhost:5000/google

The custom_code must:

Be unique
Contain only letters and numbers

If the custom code already exists, the API returns a conflict response.

⏱️ 3. Create an Expiring Short URL

The API supports temporary short URLs using the expires_in parameter.

Request
POST /shorten
Content-Type: application/json
Request Body
{
    "url": "https://www.google.com",
    "expires_in": 60
}

The expires_in value represents the expiration time in seconds.

For example:

60 seconds = 1 minute

After the specified time, the short URL becomes unavailable.

Expired URL Response
{
    "error": "Short URL has expired"
}

The API returns:

410 Gone
📊 4. Get URL Information
Request
GET /info/abc123

This endpoint provides information about a shortened URL.

The response includes:

Short code
Original URL
Click count
Creation time
Expiration time
Example Response
{
    "short_code": "abc123",
    "original_url": "https://www.google.com",
    "clicks": 3,
    "created_at": "2026-09-19T15:00:00",
    "expires_at": null
}
🔄 5. Redirect to the Original URL
Request
GET /abc123

When the short URL is opened, the application redirects the user to the original URL.

For every successful redirect, the click count is increased by 1.

For example:

http://localhost:5000/abc123

redirects to:

https://www.google.com
🗑️ 6. Delete a Short URL
Request
DELETE /delete/abc123

This permanently deletes the short URL from the database.

After deletion, accessing the short URL returns:

{
    "error": "Short URL not found"
}

with HTTP status:

404 Not Found
📋 7. View All Short URLs
Request
GET /urls

This endpoint returns all shortened URLs stored in the database.

Example Response
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
🏠 8. Web Dashboard
Request
GET /

The root endpoint opens the web dashboard.

The dashboard is built using:

HTML
CSS
JavaScript

It communicates with the Flask REST API using JavaScript fetch() requests.

🧪 Testing

This project uses pytest for automated API testing.

Run Tests
python -m pytest -v
Test Coverage

The project currently contains 11 automated tests covering:

Creating short URLs
Missing URL validation
Invalid URL validation
URL type validation
URL expiration
Negative expiration values
URL redirection
Click counting
URL deletion
Getting all URLs
Home/dashboard endpoint

Example result:

11 passed
🗄️ Test Database

The automated tests use a temporary SQLite database.

This ensures that:

Test data does not affect the main database
Tests can run independently
The development database remains unchanged
🗃️ Database

The application uses SQLite to store shortened URLs.

The main urls table contains:

Field	Description
id	Unique database ID
original_url	Original long URL
short_code	Generated or custom short code
clicks	Number of successful redirects
created_at	URL creation timestamp
expires_at	URL expiration timestamp
🔐 URL Validation

The application validates URLs before storing them.

Only URLs using:

http://
https://

are accepted.

For example:

https://www.google.com

is valid.

An invalid URL returns an error response instead of being stored.

⚡ Custom Short Codes

Users can optionally provide their own short code.

Example:

{
    "url": "https://www.google.com",
    "custom_code": "google"
}

The application checks whether the custom code already exists.

If it already exists, the API returns:

{
    "error": "Custom code already exists"
}

with HTTP status:

409 Conflict
📈 Click Tracking

Every successful visit to a shortened URL increases its click count.

For example:

Initial clicks: 0
First visit:    1
Second visit:   2
Third visit:    3

The click count can be viewed using:

GET /info/<short_code>

and through the web dashboard.

⏳ URL Expiration

A URL can optionally have an expiration time.

Example:

{
    "url": "https://www.example.com",
    "expires_in": 60
}

The application calculates the expiration timestamp and stores it in the database.

After expiration, the URL cannot be used for redirection.

🧰 Postman Testing

The REST APIs can be tested using Postman.

Example workflow:

POST /shorten
       ↓
Create short URL
       ↓
GET /info/<short_code>
       ↓
Check URL information
       ↓
GET /<short_code>
       ↓
Redirect + increase click count
       ↓
GET /urls
       ↓
View all URLs
       ↓
DELETE /delete/<short_code>
       ↓
Delete URL
💡 Project Highlights

This project demonstrates practical understanding of:

Flask application development
REST API design
HTTP methods
JSON request and response handling
URL validation
SQLite database operations
CRUD operations
Database queries
URL redirection
Click tracking
Error handling
Expiration logic
Frontend and backend integration
JavaScript fetch() API
Automated testing with pytest
Git and GitHub
🔮 Future Improvements

Possible future improvements include:

User authentication and authorization
Advanced URL analytics
Click analytics by date
Rate limiting
Swagger/OpenAPI documentation
QR code generation
PostgreSQL database
Redis caching
Docker support
Cloud deployment
Custom domains
User-specific URL management

👩‍💻 Author

Priyanka Patil

BE Computer Engineering Student

⭐ Project

If you find this project useful, feel free to explore the repository and provide fee