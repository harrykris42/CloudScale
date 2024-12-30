.PHONY: help install run-dev test lint clean build-images push-images deploy

help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

install: ## Install all dependencies
	@echo "Installing dependencies..."
	@for service in services/*; do \
		if [ -f $$service/requirements.txt ]; then \
			cd $$service && python -m venv venv && . venv/bin/activate && pip install -r requirements.txt && cd ../..; \
		fi \
	done
	cd frontend && npm install && cd ..

run-dev: ## Run the project in development mode
	docker-compose up --build

test: ## Run all tests
	@echo "Running backend tests..."
	@for service in services/*; do \
		if [ -f $$service/requirements.txt ]; then \
			cd $$service && python -m pytest && cd ../..; \
		fi \
	done
	@echo "Running frontend tests..."
	cd frontend && npm test

lint: ## Run linting
	@echo "Linting Python code..."
	@for service in services/*; do \
		if [ -f $$service/requirements.txt ]; then \
			cd $$service && flake8 . && black . --check && cd ../..; \
		fi \
	done
	@echo "Linting frontend code..."
	cd frontend && npm run lint

clean: ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "node_modules" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +

build-images: ## Build all Docker images
	docker-compose build

push-images: ## Push Docker images to registry
	@echo "Pushing images to registry..."
	# Add your image push commands here

deploy: ## Deploy the application
	@echo "Deploying application..."
	# Add your deployment commands here
