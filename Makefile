run-local:
	uvicorn src.main:app --reload

# Command to build a Docker image with a specific version
# Ex: make build-image version=1.0.1
build-image:
	@if [ -z "$(version)" ]; then \
		echo "Error: version is not set. Usage: make build-image version=<version>"; \
		exit 1; \
	fi
	docker build -t fridge-scan:v$(version) .

docker-run-local:
	docker run -p 8000:8000 fridge-scan:v1.0.0
