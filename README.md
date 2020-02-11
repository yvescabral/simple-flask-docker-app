# Simple Python Flask Dockerized Application

## Run locally

Create a virtual env and activate it
```sh
python -m venv env && source env/bin/activate
```

Install requirements
```sh
pip install -r requirements.txt
```

Install app package
```sh
pip install -e .
```

Export needed environment variables and run it
```
export FLASK_APP=testing_app
export FLASK_ENV=development
flask run
```

## Run on Docker

Build the image using the following command

```sh
docker build -t yvescabral/cd-testing:latest .
```

Edit and run the Docker container using the command shown below.

```sh
docker run -d \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v ./testing_app/templates:/app/testing_app/templates \
    -e FLASK_APP=testing_app \
    -e DOCKER_HUB_USERNAME= \
    -e DOCKER_HUB_PASSWORD= \
    -e GITHUB_ACCESS_TOKEN= \
    -p 5000:5000 \
    yvescabral/cd-testing
```

The application will be accessible at http://127.0.0.1:5000
