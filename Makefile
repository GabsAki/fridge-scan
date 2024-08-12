run-local:
	uvicorn src.main:app --reload

build-image:
	docker build -t gabsaki/fridge-scan:latest .

# Use only if you are logged in to this dockerhub account
push-image:
	docker push gabsaki/fridge-scan:latest

pull-image:
	docker pull gabsaki/fridge-scan

docker-run-local:
	docker run -p 8000:8000 gabsaki/fridge-scan:latest
