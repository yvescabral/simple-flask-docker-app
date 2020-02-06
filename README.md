# Simple Python Flask Dockerized Application

Build the image using the following command

```sh
docker build -t yvescabral/cd-testing:latest .
```

Run the Docker container using the command shown below.

```sh
docker run -d -e FLASK_APP=testing_app -e FLASK_ENV=development -p 5000:5000 yvescabral/cd-testing
```

The application will be accessible at http://127.0.0.1:5000
