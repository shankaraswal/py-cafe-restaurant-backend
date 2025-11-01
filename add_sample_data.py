#!/usr/bin/env python3
"""
Script to add sample menu data to the cafe API
"""
import requests
import json

API_BASE = "http://localhost:8000/api/v1"

# Sample menu items
MENU_ITEMS = [
    {"name": "Espresso", "description": "Rich and bold espresso shot", "price": 2.50, "image_url": "https://example.com/espresso.jpg"},
    {"name": "Cappuccino", "description": "Espresso with steamed milk and foam", "price": 4.00, "image_url": "https://example.com/cappuccino.jpg"},
    {"name": "Latte", "description": "Espresso with steamed milk", "price": 4.50, "image_url": "https://example.com/latte.jpg"},
    {"name": "Americano", "description": "Espresso with hot water", "price": 3.00, "image_url": "https://example.com/americano.jpg"},
    {"name": "Mocha", "description": "Espresso with chocolate and steamed milk", "price": 5.00, "image_url": "https://example.com/mocha.jpg"},
    {"name": "Croissant", "description": "Buttery, flaky pastry", "price": 3.50, "image_url": "https://example.com/croissant.jpg"},
    {"name": "Blueberry Muffin", "description": "Fresh baked muffin with blueberries", "price": 4.00, "image_url": "https://example.com/muffin.jpg"},
    {"name": "Avocado Toast", "description": "Toasted bread with fresh avocado", "price": 8.00, "image_url": "https://example.com/avocado-toast.jpg"},
    {"name": "Caesar Salad", "description": "Fresh romaine with caesar dressing", "price": 9.50, "image_url": "https://example.com/caesar-salad.jpg"},
    {"name": "Grilled Sandwich", "description": "Grilled cheese and ham sandwich", "price": 7.50, "image_url": "https://example.com/sandwich.jpg"},
    {"name": "Bagel with Cream Cheese", "description": "Fresh bagel with cream cheese", "price": 4.50, "image_url": "https://example.com/bagel.jpg"},
    {"name": "Fruit Bowl", "description": "Mixed seasonal fruits", "price": 6.00, "image_url": "https://example.com/fruit-bowl.jpg"},
    {"name": "Green Tea", "description": "Premium green tea", "price": 2.50, "image_url": "https://example.com/green-tea.jpg"},
    {"name": "Hot Chocolate", "description": "Rich hot chocolate with marshmallows", "price": 4.00, "image_url": "https://example.com/hot-chocolate.jpg"},
    {"name": "Iced Coffee", "description": "Cold brew coffee over ice", "price": 3.50, "image_url": "https://example.com/iced-coffee.jpg"}
]

def add_menu_items():
    """Add sample menu items to the API"""
    print("🍽️  Adding sample menu items...")
    
    for item in MENU_ITEMS:
        try:
            response = requests.post(f"{API_BASE}/menu", json=item)
            if response.status_code == 200:
                print(f"✅ Added: {item['name']}")
            else:
                print(f"❌ Failed to add {item['name']}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error adding {item['name']}: {e}")
    
    print("✅ Sample data loading complete!")

def check_api():
    """Check if API is responding"""
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ API is healthy!")
            return True
        else:
            print(f"❌ API returned status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to API: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Cafe API Sample Data Loader")
    print("==============================")
    
    if check_api():
        add_menu_items()
        
        # Test the menu endpoint
        try:
            response = requests.get(f"{API_BASE}/menu")
            if response.status_code == 200:
                menu_count = len(response.json())
                print(f"🎉 Success! {menu_count} menu items are now available")
                print(f"🌐 Visit: http://localhost:8000/docs to test the API")
            else:
                print("⚠️  Could not verify menu items")
        except Exception as e:
            print(f"⚠️  Error checking menu: {e}")
    else:
        print("💡 Make sure the API is running:")
        print("   - Docker: make all")
        print("   - Local: make dev")