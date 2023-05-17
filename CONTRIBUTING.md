# CONTRIBUTING

## Add environment variables:

### Create .env file in root folder and add these environment variables:
```
DATABASE_URL=your_db_url
JWT_SECRET_KEY=your_secret_key
```

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

## SWAGGER:

### How to access swagger:

#### - Locally:
```
http://localhost:5000/api/swagger-ui
```
#### - Production:
```
your-api-url/api/swagger-ui
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
