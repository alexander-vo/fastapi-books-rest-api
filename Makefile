start:
	docker-compose up

stop:
	docker-compose down

isort:
	isort books/

black:
	black books/

format-code:
	make black
	make isort