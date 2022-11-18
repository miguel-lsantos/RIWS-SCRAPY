SHELL := /bin/bash

env: ## Create virtual environment
	if [ ! -d "venv" ]; then \
		python3 -m venv venv; \
		venv/bin/pip install -r requirements.txt; \
	fi

run-scrapy: env elastic-up ## Activate virtual environment and run scrapy
	source venv/bin/activate && \
	scrapy crawl chollometro

elastic-up: ## Start elasticsearch
	docker-compose up -d

elastic-down: ## Stop elasticsearch
	docker-compose down

run-web: ## Run web app
	cd chollometro-react && npm install && npm start