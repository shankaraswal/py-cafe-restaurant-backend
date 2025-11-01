from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import menu, cart, orders
from app.database import engine
from app import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cafe Order API",
    description="Backend API for cafe/restaurant ordering system",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(menu.router, prefix="/api/v1", tags=["menu"])
app.include_router(cart.router, prefix="/api/v1", tags=["cart"])
app.include_router(orders.router, prefix="/api/v1", tags=["orders"])

@app.get("/")
async def root():
    return {"message": "Welcome to Cafe Order API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}