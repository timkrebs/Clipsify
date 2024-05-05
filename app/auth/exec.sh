docker build -t auth .
docker run --env-file .env -p 5000:5000 -it auth