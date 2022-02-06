# Web-Api

This API is that returns name and surname, accepts only GET method, and returns temperature with /temperature endpoint.

If you want to run this application only with flask


```
 flask export FLASK_APP=api.py
 flask run
```

If you want to run it with docker


```
docker build -t <your_image_name> .
docker container run -d -p 5000:5000 <your_image_name>
```
