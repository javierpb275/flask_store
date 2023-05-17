# CONTRIBUTING

## How to build the image:

### - In the root folder run:
```
docker build -t IMAGE_NAME .
```

## How to run the Dockerfile locally:

### - In the root folder run:
```
docker run -dp 5000:5000 -w /app -v "$(pwd):/app" IMAGE_NAME sh -c "flask run --host 0.0.0.0" 
```

## Flask Migrate:

### How to initialize a database migration environment:
```
docker exec CONTAINER_NAME_OR_ID flask db init
```

### How to generate a new database migration script:
```
docker exec CONTAINER_NAME_OR_ID flask db migrate
```

### How to apply pending database migrations to the database:
```
docker exec CONTAINER_NAME_OR_ID flask db upgrade
```
