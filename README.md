# 🍰 Py Cafe Restaurant Backend

A modern, scalable FastAPI backend for a cafe/restaurant ordering system with comprehensive menu management, shopping cart functionality, and order processing capabilities.

## 📋 Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
  - [Using Docker (Recommended)](#using-docker-recommended)
  - [Local Development](#local-development)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [Contributing](#contributing)

## ✨ Features

### Core Functionalities

- **🍽️ Menu Management**
  - List all available menu items with detailed information
  - View menu item details (name, description, price, category)
  - Categorize items (beverages, food, desserts, etc.)
  - Real-time menu updates

- **🛒 Shopping Cart Management**
  - Add items to cart with quantity specification
  - Update item quantities
  - Remove items from cart
  - View cart summary with total price calculation
  - Persistent cart storage

- **📦 Order Processing**
  - Place orders from cart items
  - Real-time order status tracking (pending, confirmed, ready, completed)
  - Order history and details
  - Automatic order confirmation
  - Order total calculation with tax support

- **👤 Session-Based Guest Carts**
  - Support for guest users without authentication
  - Session ID-based cart persistence
  - Unique shopping experience per session
  - Session expiration and cleanup

- **📊 Order Management**
  - Track orders by status
  - Complete order workflow management
  - Order summary and details retrieval

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend Framework** | FastAPI (modern, fast Python web framework) |
| **ORM** | SQLAlchemy (powerful SQL toolkit and ORM) |
| **Database** | PostgreSQL (robust relational database) |
| **Containerization** | Docker & Docker Compose |
| **Data Validation** | Pydantic (data validation using Python type annotations) |
| **API Documentation** | Swagger UI / ReDoc (auto-generated from FastAPI) |
| **Package Manager** | pip |
| **Python Version** | 3.8+ |

## 📦 Installation

### Prerequisites
- Git
- Docker & Docker Compose (for Docker setup)
- Python 3.8+ (for local development)
- PostgreSQL 12+ (for local development)

### Using Docker (Recommended)

Docker makes it easy to run the application without installing dependencies manually.

#### Step 1: Clone the Repository
```bash
git clone https://github.com/shankaraswal/py-cafe-restaurant-backend.git
cd py-cafe-restaurant-backend
```

#### Step 2: Configure Environment Variables
Create a `.env` file in the root directory:
```bash
cp .env.example .env  # if available
```

Or manually create `.env` with:
```
DATABASE_URL=postgresql://user:password@db:5432/cafe_db
PYTHON_ENV=production
```

#### Step 3: Build and Start Services
```bash
docker-compose up --build
```

This will:
- Build the FastAPI application image
- Start PostgreSQL database
- Start the FastAPI server
- Run database migrations

#### Step 4: Access the Application
- **API Base URL**: http://localhost:8000
- **Swagger Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

### Local Development

For local development without Docker:

#### Step 1: Clone the Repository
```bash
git clone https://github.com/shankaraswal/py-cafe-restaurant-backend.git
cd py-cafe-restaurant-backend
```

#### Step 2: Create Virtual Environment
```bash
python -m venv venv
```

#### Step 3: Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\\Scripts\\activate
```

#### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 5: Setup PostgreSQL Database

Ensure PostgreSQL is running locally:
```bash
# On macOS with Homebrew
brew services start postgresql

# On Linux
sudo service postgresql start
```

Create database:
```bash
psql -U postgres -c "CREATE DATABASE cafe_db;"
```

#### Step 6: Configure Environment Variables
Create `.env` file:
```
DATABASE_URL=postgresql://postgres:password@localhost:5432/cafe_db
PYTHON_ENV=development
```

#### Step 7: Run Database Migrations
```bash
alembic upgrade head
```

#### Step 8: Start the Development Server
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## 🚀 Running the Application

### Using Docker Compose
```bash
# Start all services
docker-compose up

# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

### Local Development
```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Start FastAPI server with auto-reload
uvicorn main:app --reload

# Or specify host and port
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 📡 API Endpoints

### Authentication & Sessions

#### Get or Create Session
```http
GET /api/sessions
Response: { "session_id": "uuid-string" }
```

### Menu Management

#### Get All Menu Items
```http
GET /api/menu
Response: [
  {
    "id": 1,
    "name": "Espresso",
    "description": "Strong coffee shot",
    "price": 2.50,
    "category": "Beverages",
    "is_available": true
  }
]
```

#### Get Menu Item by ID
```http
GET /api/menu/{item_id}
```

#### Get Menu by Category
```http
GET /api/menu?category=Beverages
```

### Shopping Cart

#### Get Cart (Session-based)
```http
GET /api/cart
Headers: { "X-Session-ID": "session-uuid" }
Response: {
  "cart_id": 1,
  "session_id": "uuid",
  "items": [
    {
      "menu_item_id": 1,
      "name": "Espresso",
      "quantity": 2,
      "unit_price": 2.50,
      "total_price": 5.00
    }
  ],
  "total_price": 5.00,
  "item_count": 2
}
```

#### Add Item to Cart
```http
POST /api/cart/items
Headers: { "X-Session-ID": "session-uuid" }
Body: {
  "menu_item_id": 1,
  "quantity": 2
}
```

#### Update Cart Item
```http
PUT /api/cart/items/{item_id}
Headers: { "X-Session-ID": "session-uuid" }
Body: {
  "quantity": 3
}
```

#### Remove Item from Cart
```http
DELETE /api/cart/items/{item_id}
Headers: { "X-Session-ID": "session-uuid" }
```

#### Clear Cart
```http
DELETE /api/cart
Headers: { "X-Session-ID": "session-uuid" }
```

### Orders

#### Create Order (from cart)
```http
POST /api/orders
Headers: { "X-Session-ID": "session-uuid" }
Body: {
  "notes": "No sugar in coffee"
}
Response: {
  "id": 1,
  "session_id": "uuid",
  "order_number": "ORD-001",
  "status": "pending",
  "total_price": 5.00,
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Get Order Details
```http
GET /api/orders/{order_id}
Response: {
  "id": 1,
  "order_number": "ORD-001",
  "status": "confirmed",
  "items": [...],
  "total_price": 5.00,
  "notes": "No sugar in coffee",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Get Order by Session
```http
GET /api/orders?session_id=uuid
```

#### Update Order Status
```http
PUT /api/orders/{order_id}/status
Body: {
  "status": "ready"
}
Response: { "status": "ready" }
```

#### Get All Orders (Admin)
```http
GET /api/orders/admin/all
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/cafe_db
DB_ECHO=False

# Application Configuration
APP_NAME=Cafe Order API
APP_VERSION=1.0.0
DEBUG=False
PYTHON_ENV=production

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Session Configuration
SESSION_TIMEOUT=24  # hours
```

### Database Models

The application uses the following main models:

- **User**: Guest session tracking
- **MenuItem**: Menu item details and availability
- **Cart**: Shopping cart per session
- **CartItem**: Individual items in cart
- **Order**: Customer orders
- **OrderItem**: Items within an order

## 🔧 Development

### Project Structure
```
py-cafe-restaurant-backend/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   ├── schemas/
│   ├── routes/
│   └── services/
├── tests/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

### Running Tests
```bash
pytest
pytest --cov=app  # with coverage
```

### Code Style
Follow PEP 8 guidelines:
```bash
pylint app/
black app/
flake8 app/
```

## 🐛 Troubleshooting

### Docker Issues
- **Port already in use**: `docker-compose down && docker-compose up --build`
- **Database connection error**: Ensure PostgreSQL container is healthy: `docker-compose ps`
- **Permission denied**: Check Docker daemon is running

### Local Development Issues
- **Import errors**: Ensure virtual environment is activated and dependencies installed
- **Database connection error**: Verify PostgreSQL is running and credentials in `.env` are correct
- **Port 8000 in use**: `lsof -i :8000` and kill the process or use different port

## 📝 API Testing

Use the interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Or use curl for testing:
```bash
# Get all menu items
curl http://localhost:8000/api/menu

# Create an order
curl -X POST http://localhost:8000/api/orders \
  -H "X-Session-ID: your-session-id" \
  -H "Content-Type: application/json" \
  -d '{"notes": "Extra hot"}'
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

For issues and questions, please open an issue on the GitHub repository.

---

**Happy coding! 🚀**
