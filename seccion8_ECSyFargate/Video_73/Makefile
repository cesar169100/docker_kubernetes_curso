none:
	@echo ""

login:
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 590184078061.dkr.ecr.us-east-1.amazonaws.com

build:
	docker build -t default/ecs-imagen .
tag:
	docker tag default/ecs-imagen:latest 590184078061.dkr.ecr.us-east-1.amazonaws.com/default/ecs-imagen:latest

push:
	docker push 590184078061.dkr.ecr.us-east-1.amazonaws.com/default/ecs-imagen:latest

all:	
	login build tag push