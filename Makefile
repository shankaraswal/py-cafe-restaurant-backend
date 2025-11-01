.PHONY: help start stop restart logs build clean status

# Default target
help:
	@echo "Available Commands:"
	@echo "=================="
	@echo "make start     - Start all services"
	@echo "make stop      - Stop all services"
	@echo "make restart   - Restart all services"
	@echo "make logs      - View service logs"
	@echo "make build     - Build all services"
	@echo "make clean     - Clean up containers and volumes"
	@echo "make status    - Show service status"

# Start all services
start:
	@echo "🚀 Starting services..."
	docker-compose up -d
	@echo "✅ Services started! API: http://localhost:8000"

# Stop all services
stop:
	@echo "🛑 Stopping services..."
	docker-compose down
	@echo "✅ Services stopped"

# Restart services
restart: stop start

# View logs
logs:
	docker-compose logs -f

# Build services
build:
	@echo "🔨 Building services..."
	docker-compose build

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	docker-compose down -v --rmi all
	docker system prune -f

# Show status
status:
	@echo "📊 Service Status:"
	docker-compose ps