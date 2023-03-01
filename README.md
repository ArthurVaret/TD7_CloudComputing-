# TD7-CloudComputing

## Docker volumes

To enable the automatic refreshing of the page when the contents of the text file are changed, you can use a bind mount when running the Docker container.

Run the Docker container using the following command:

```bash
docker run -p 5000:5000 -v /path/to/local/dir:/app flask-docker-app
```

Replace `/path/to/local/dir` with the absolute path of the directory containing the `text_file.txt` file on your host machine.

If you’re executing the command in the folder already, you can use :

```bash
docker run -d -p 5000:5000 -v .:/app tp6-flask
```

Now, any changes made to the `text_file.txt` file on your host machine will be displayed on the web page when you refresh it.

## Make a mongo database persistent. (by using Volume)

Create a bridge network for the containers to connect to!

I created a bridge named `bridgeTP6` on Docker.

```bash
docker network create --driver bridge bridgeTP6
```

Run mongo with volumes

```bash
docker run -d --name mongodb --network bridgeTP6 -v ./db:/data/db mongo:latest
```

The db is created.

Modify `[app.py](http://app.py)` to add a mongo db

```python
from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://mongodb:27017/")

db = client.td6db

collection = db.td6_collection
collection.insert_one({"test":"blaaaaa"})

@app.route('/')
def read_data():
    # retrieve data from MongoDB
    mongo_data = ""
    for data in collection.find():
        mongo_data += str(data) + "<br>"

    # read content from text file
    with open('text_file.txt', 'r') as f:
        text_file_data = f.read()

    # combine the two data sources
    content = mongo_data + text_file_data

    return content

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
```

Modify the `Dockerfile` so that it does not take the bd directory

```docker
FROM python:latest

WORKDIR /app

COPY app.py .
COPY requirements.txt .

RUN pip3 install -r requirements.txt

EXPOSE 5000

VOLUME /app

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
```

Run the flask app with connection to the bridge

```bash
docker run -d --network bridgeTP6 -p 5000:5000 -v .:/app tp6-flask
```

The app works !

### Explain how you can migrate it! How to share it with another instance of the same database engine.

If you have a Docker container running an application that uses a MongoDB database, and you want to migrate the database volume to another container without losing any data, you can achieve this by pointing the new container at the same folder path where the previous container stored the database data. This is possible because Docker containers are designed to be portable, and their data can be persisted outside the container in the form of volumes.

Here's an example of how you can migrate the MongoDB database volume to another container:

1. Stop the existing container that is running the MongoDB database:
    
    ```bash
    docker stop <container-name>
    ```
    
2. Start a new container with the same volume configuration, but using a different image or tag. You can do this by passing the **`v`** flag with the path to the data directory and the new image or tag name:
    
    ```bash
    docker run -d --name <new-container-name> -v <path-to-data-dir>:/data/db <new-image-or-tag>
    ```
    
    Here, **`<path-to-data-dir>`** is the path to the directory where the MongoDB database data is stored on the host machine, and **`<new-image-or-tag>`** is the name or tag of the new MongoDB Docker image that you want to use.
    

### Docker-compose

Modify `docker-compose.yml` to create both containers with the volumes

```docker
version: '3'

services:
  mongodb:
    image: mongo:latest
    networks:
      - bridgeTP6
    volumes:
      - ./db:/data/db
  web:
    build: .
    container_name: tp6-flask
    ports:
      - "5000:5000"
    networks:
      - bridgeTP6
    volumes:
      - ./text_file.txt:/app/text_file.txt
    depends_on:
      - mongodb
networks:
  bridgeTP6:
    driver: bridge
```

Run the compose
```bash
	docker-compose up -d
```
