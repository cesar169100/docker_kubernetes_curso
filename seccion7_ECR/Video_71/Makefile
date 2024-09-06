none:
		@echo "Ejecuta una tarea"

target1:
	   @echo "Hello!"

target2:
	   @echo "World!"

target3:
	   @echo "All tasks completed!"

target4: target1 target2 target3

login:
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 590184078061.dkr.ecr.us-east-1.amazonaws.com

build:
	docker build -t default/hola-mundo:20.04 .

tag:
	docker tag default/hola-mundo:20.04 590184078061.dkr.ecr.us-east-1.amazonaws.com/default/hola-mundo:20.04

push:
	docker push 590184078061.dkr.ecr.us-east-1.amazonaws.com/default/hola-mundo:20.04

buildandpush: build tag push