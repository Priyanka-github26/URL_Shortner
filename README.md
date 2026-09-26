# 🔗 URL Shortener

A full-stack URL Shortener application built using **Python, Flask, SQLite, HTML, CSS, and JavaScript**.

The application provides REST APIs and a responsive web dashboard for creating, managing, and tracking shortened URLs.

---

## 🚀 Features

### URL Management

* Create shortened URLs
* Automatically generate unique 6-character short codes
* Create custom short codes
* Validate URLs
* Set URL expiration time
* Redirect short URLs to original URLs
* Delete shortened URLs
* View all created URLs
* Search URLs
* Copy shortened URLs

### 📊 Click Analytics

* Track total clicks
* Store individual click events
* Record the timestamp of every click
* Track the most recent click
* View complete click history
* Dedicated analytics APIs

### 🔐 API Security

* Rate limiting using Flask-Limiter
* Different request limits for different endpoints
* Returns `429 Too Many Requests` when limits are exceeded

### 🧪 Testing

* Automated API testing using pytest
* 13 automated tests
* Isolated temporary database for testing
* Tests for URL creation, validation, expiration, redirection, deletion, analytics, and rate limiting

### 🎨 Web Dashboard

* Responsive user interface
* URL creation form
* URL listing
* Search functionality
* Copy shortened URL
* Click statistics
* Active/expired URL status
* Analytics information

---

## 🛠️ Technologies Used

* **Python**
* **Flask**
* **SQLite**
* **REST API**
* **HTML5**
* **CSS3**
* **JavaScript**
* **Flask-Limiter**
* **pytest**
* **Postman**
* **Git**
* **GitHub**
* **VS Code**

---

## 📁 Project Structure

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
```

---

# ⚙️ Installation & Setup

## 1. Clone the repository

```bash
git clone https://github.com/Priyanka-github26/URL_Shortner.git
```

## 2. Navigate to the project

```bash
cd URL_Shortner
```

## 3. Create a virtual environment

```bash
python -m venv venv
```

## 4. Activate the virtual environment

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

## 5. Install dependencies

```bash
pip install -r requirements.txt
```

## 6. Run the application

```bash
python app.py
```

The application will run at:

```text
http://127.0.0.1:5000
```

---

# 🌐 Web Dashboard

Open:

```text
http://127.0.0.1:5000
```

The dashboard allows users to:

* Enter a long URL
* Generate a shortened URL
* Create custom short codes
* Search URLs
* Copy shortened URLs
* View click statistics
* View URL status
* Manage shortened URLs

---

# 🔌 REST API Endpoints

| Method | Endpoint                          | Description              |
| ------ | --------------------------------- | ------------------------ |
| POST   | `/shorten`                        | Create a shortened URL   |
| GET    | `/<short_code>`                   | Redirect to original URL |
| GET    | `/info/<short_code>`              | Get URL information      |
| GET    | `/urls`                           | Get all shortened URLs   |
| DELETE | `/delete/<short_code>`            | Delete a shortened URL   |
| GET    | `/analytics/<short_code>`         | Get click analytics      |
| GET    | `/analytics/<short_code>/history` | Get click history        |
| GET    | `/`                               | API/home status          |

---

# 📝 API Usage

## 1. Create Short URL

### Request

```http
POST /shorten
```

### JSON Body

```json
{
    "url": "https://www.google.com"
}
```

### Example Response

```json
{
    "message": "Short URL created successfully",
    "short_code": "xhc6O3",
    "short_url": "http://localhost:5000/xhc6O3"
}
```

---

## 2. Create Custom Short URL

### Request

```http
POST /shorten
```

### JSON Body

```json
{
    "url": "https://www.google.com",
    "custom_code": "google"
}
```

The generated short URL will be:

```text
http://localhost:5000/google
```

---

## 3. URL Expiration

Expiration can be specified using `expires_in`.

Example:

```json
{
    "url": "https://www.google.com",
    "expires_in": 60
}
```

The URL will expire after **60 seconds**.

Expired URLs cannot be redirected.

---

# 🔀 URL Redirection

When a user opens:

```text
http://localhost:5000/xhc6O3
```

the application:

1. Finds the short code
2. Checks whether the URL exists
3. Checks expiration
4. Increments the click count
5. Stores the click timestamp
6. Updates the latest click time
7. Redirects the user to the original URL

---

# 📊 Click Analytics

The application provides dedicated APIs for monitoring URL usage.

## Get Analytics

```http
GET /analytics/<short_code>
```

Example:

```text
GET /analytics/xhc6O3
```

### Response

```json
{
    "short_code": "xhc6O3",
    "original_url": "https://www.google.com",
    "total_clicks": 3,
    "created_at": "2026-09-26T16:10:00",
    "last_clicked_at": "2026-09-26T16:15:42"
}
```

---

# 📈 Click History

The application stores every successful click event.

### Endpoint

```http
GET /analytics/<short_code>/history
```

Example:

```text
GET /analytics/xhc6O3/history
```

### Response

```json
{
    "short_code": "xhc6O3",
    "total_clicks": 3,
    "click_history": [
        {
            "clicked_at": "2026-09-26T16:15:42"
        },
        {
            "clicked_at": "2026-09-26T16:14:31"
        },
        {
            "clicked_at": "2026-09-26T16:13:20"
        }
    ]
}
```

---

# 🔐 Rate Limiting

The API uses **Flask-Limiter** to prevent excessive requests.

| Endpoint                              |              Limit |
| ------------------------------------- | -----------------: |
| `POST /shorten`                       | 10 requests/minute |
| `GET /info/<short_code>`              | 30 requests/minute |
| `GET /urls`                           | 20 requests/minute |
| `DELETE /delete/<short_code>`         | 10 requests/minute |
| `GET /analytics/<short_code>`         | 30 requests/minute |
| `GET /analytics/<short_code>/history` | 30 requests/minute |

When the configured limit is exceeded, the API returns:

```text
429 Too Many Requests
```

This helps protect the API from excessive requests.

---

# 🗃️ Database

The application uses **SQLite** to store shortened URLs and click analytics.

## `urls` Table

| Field             | Description                        |
| ----------------- | ---------------------------------- |
| `id`              | Unique database ID                 |
| `original_url`    | Original long URL                  |
| `short_code`      | Generated or custom short code     |
| `clicks`          | Number of successful redirects     |
| `created_at`      | URL creation timestamp             |
| `expires_at`      | URL expiration timestamp           |
| `last_clicked_at` | Timestamp of the most recent click |

## `clicks` Table

| Field        | Description                 |
| ------------ | --------------------------- |
| `id`         | Unique click event ID       |
| `short_code` | Short code that was clicked |
| `clicked_at` | Timestamp of the click      |

---

# 🧪 Testing

This project uses **pytest** for automated API testing.

## Run Tests

```bash
python -m pytest -v
```

## Test Coverage

The project currently contains **13 automated tests** covering:

* Creating short URLs
* Missing URL validation
* Invalid URL validation
* URL type validation
* URL expiration
* Negative expiration values
* URL redirection
* Click counting
* Click history
* URL deletion
* Getting all URLs
* Home/dashboard endpoint
* Rate limiting

Example result:

```text
13 passed
```

The tests use a **temporary SQLite database**, so testing does not modify the main application database.

---

# 📮 Postman Testing

The APIs can be tested using **Postman**.

Example requests:

### Create URL

```text
POST http://127.0.0.1:5000/shorten
```

Body:

```json
{
    "url": "https://www.google.com"
}
```

### Get Information

```text
GET http://127.0.0.1:5000/info/<short_code>
```

### Get Analytics

```text
GET http://127.0.0.1:5000/analytics/<short_code>
```

### Get Click History

```text
GET http://127.0.0.1:5000/analytics/<short_code>/history
```

### Delete URL

```text
DELETE http://127.0.0.1:5000/delete/<short_code>
```

---

# 🏗️ Application Flow

```text
                User
                  │
                  ▼
          Web Dashboard / Postman
                  │
                  ▼
              Flask API
                  │
        ┌─────────┼─────────┐
        │         │         │
        ▼         ▼         ▼
   Validation  Rate Limit  Analytics
        │         │         │
        └─────────┼─────────┘
                  │
                  ▼
              SQLite
             /       \
            ▼         ▼
         urls       clicks
```

---

# ⭐ Project Highlights

* Built a complete RESTful URL Shortener using Flask
* Implemented automatic and custom short-code generation
* Added URL validation and expiration
* Implemented click tracking
* Added detailed click analytics and click history
* Implemented API rate limiting using Flask-Limiter
* Created a responsive web dashboard
* Built automated API tests using pytest
* Used an isolated temporary database for testing
* Tested APIs using Postman
* Used Git and GitHub for version control

---

# 🔮 Future Improvements

Possible future enhancements include:

* Redis caching
* Redis-based rate-limit storage
* User authentication
* User-specific URL management
* Advanced date-based analytics
* Swagger/OpenAPI documentation
* QR code generation
* PostgreSQL support
* Docker containerization
* Cloud deployment
* Custom domains

---

# 🎯 Project Objective

The main objective of this project is to demonstrate practical knowledge of:

* Backend development
* REST API design
* Database management
* API security
* Caching concepts
* Automated testing
* Frontend-backend integration
* Git/GitHub workflow

---

# 👩‍💻 Author

**Priyanka Patil**

BE Computer Engineering Student

GitHub:

```text
https://github.com/Priyanka-github26
```
