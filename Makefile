

up:
	docker compose up --build --remove-orphans -d

down:
	docker compose down

logs:
	docker compose logs --follow

psql:
	docker compose exec db psql -U ytouate -d workout_builder
