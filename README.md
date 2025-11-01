# Cafe Order API

A FastAPI backend for a cafe/restaurant ordering system with PostgreSQL database.

## Features

- **Menu Management**: List and view menu items
- **Cart Management**: Add, update, remove items from cart
- **Order Processing**: Place orders and track status
- **Session-based Carts**: Guest user support via session IDs

## Quick Start

### Using Docker (Recommended)

1. Clone and navigate to the project:
```bash
git clone <your-repo>
cd cafe-order-api
```

2. Start the services:
```bash
docker-compose up --build
```

3. The API will be available at `http://localhost:8000`
4. API documentation at `http://localhost:8000/docs`

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

3. Start PostgreSQL and create database `cafe_db`

4. Run the application:
```bash
python run.py
```

## API Endpoints

### Menu
- `GET /api/v1/menu` - List all menu items
- `GET /api/v1/menu/{item_id}` - Get specific menu item
- `POST /api/v1/menu` - Create menu item (admin)

### Cart
- `GET /api/v1/cart/{session_id}` - Get cart contents
- `POST /api/v1/cart/{session_id}/items` - Add item to cart
- `PUT /api/v1/cart/{session_id}/items/{item_id}` - Update item quantity
- `DELETE /api/v1/cart/{session_id}/items/{item_id}` - Remove item from cart
- `DELETE /api/v1/cart/{session_id}` - Clear cart

### Orders
- `POST /api/v1/orders?session_id={session_id}` - Create order from cart
- `GET /api/v1/orders/{order_id}` - Get order details
- `GET /api/v1/orders` - List all orders (admin)
- `PUT /api/v1/orders/{order_id}/status` - Update order status (admin)

## Database Schema

- **menu_items**: Menu items with name, description, price, image_url
- **carts**: User carts identified by session_id
- **cart_items**: Items in carts with quantities
- **orders**: Placed orders with status and total amount

## Sample Usage

1. Get menu: `GET /api/v1/menu`
2. Add to cart: `POST /api/v1/cart/user123/items` with `{"menu_item_id": 1, "quantity": 2}`
3. View cart: `GET /api/v1/cart/user123`
4. Place order: `POST /api/v1/orders?session_id=user123`

## Development

- FastAPI with automatic OpenAPI documentation
- SQLAlchemy ORM with PostgreSQL
- Pydantic for data validation
- Docker support for easy deployment