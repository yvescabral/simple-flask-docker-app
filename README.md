# Simple Python Flask Dockerized Application

# Run locally
Create a virtual env and activate it
```sh
python -m venv env && source env/bin/activate
```

Install requirements
```sh
pip install -r requirements.txt
```

Export needed env vars and run it
```
export FLASK_APP=testing_app
export FLASK_ENV=development
flask run
```

# Run on Docker
Build the image using the following command

```sh
docker build -t yvescabral/cd-testing:latest .
```

Run the Docker container using the command shown below.

```sh
docker run -d -e FLASK_APP=testing_app -e FLASK_ENV=development -p 5000:5000 yvescabral/cd-testing
```

The application will be accessible at http://127.0.0.1:5000
