# Web-Api

This API is that returns name and surname, accepts only get method, and returns temperature with /temperature endpoint.

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



**What is Flask?**


[Flask ](https://flask.palletsprojects.com/en/2.0.x/)is a web framework, it’s a Python module that lets you develop web applications easily. It has a small and easy-to-extend core: a microframework that doesn’t include an ORM (Object Relational Manager) or such features.

****Installation Flask****

A virtual environment must be set up before downloading the flask. The more projects you have, the more likely it is to conflict with different versions of libraries and themselves. You can use a virtual environment to maintain compatibility in the project. Virtual environments are independent groups of Python libraries, one for each project. Packages installed for one project will not affect other projects or the operating system's packages. Python comes bundled with the venv module to create virtual environments.

**Creating an Environment**

For macOS/Linux
```
$ mkdir <directory-name>
$ cd <directory-name>
$ python3 -m venv venv
```

For Windows
```
> mkdir <directory-name>
> cd <directory-name>
> py -3 -m venv venv
```

Activate the environment

For macOS/Linux
`$ . venv/bin/activate`

For Windows

`$venv\Scripts\activate`

Install Flask Withing the activated environment, use the following command to install Flask:

```
$ pip install flask
$ pip install flask-restful
```


Example:
Now let's look at a simple web application example. When this application runs, let our application work on port 5000.

api.py



  ```
from flask import Flask, request
from flask_restful import Resource, Api
import requests
app = Flask(__name__)
api = Api(app)

class Index(Resource):

    def get(self):

        return {'Atakan': 'Ciftci'}

class Temperature(Resource):

    def get(self):

        args = request.args
        city = args['city']

        response = requests.get(f"https://caseapi.bestcloudfor.me/temperature?city={city}")
        temperature = response.json()

        return temperature


api.add_resource(Index, '/')
api.add_resource(Temperature,'/temperature')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

```

Next we create an instance of this class. The first argument is the name of the application’s module or package. name is a convenient shortcut for this that is appropriate for most cases. This is needed so that Flask knows where to look for resources such as templates and static files.

  `@app.route('/') We then use the route() decorator to tell Flask what URL should trigger our function.`

The function returns the message we want to display in the user’s browser. The default content type is HTML, so HTML in the string will be rendered by the browser.

app.run(debug=True, host='0.0.0.0', port=5000) we set our port
To run the application, use the flask command or python -m flask. Before you can do that you need to tell your terminal the application to work with by exporting the FLASK_APP environment variable:

For Bash:
```
$ export FLASK_APP=api.py
$ flask run
```
For CMD
```
set FLASK_APP=api
flask run
```
For Powershell
```
$env:FLASK_APP = "api"
flask run
```
**Writing Dockerfile and Build Image**

[Docker](https://www.docker.com/) is an open platform for developing, shipping, and running applications. Docker enables you to separate your applications from your infrastructure so you can deliver software quickly. With Docker, you can manage your infrastructure in the same ways you manage your applications. You can download and install Docker on multiple platforms.
Click the link for installation to Docker

_**Dockerize Flask Application**
**What is Dockerfile?**_
****
The Dockerfile is essentially the build instructions to build the image. We provide our images, which we will customize in Docker and use for our own purposes, with a text file called Dockerfile. In the Dockerfile it can contain all the commands that can be used to create an image. We use a structure called Dockerfile to ensure that these are created in one go and automatically
saved.

 Dockerfile


```
FROM python:3.7

LABEL maintainer="Atakan Ciftci"

LABEL maintainer.mail="hatakanciftci@gmail.com"

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD python api.py

```
**Build the image**

We can create the image version of the file named Dockerfile that we wrote with the "docker build" command in Docker. The exact parameter the "docker build" command should take is where the Dockerfile is. For this, there can be a "path" after the "docker builds" command, that is, a path that tells where the file is in our local system, or a "URL" containing a git repository.

`$ docker build image -t <your_image_name> .`

you can check the images this command:

`$ docker images ls`

Now, we need a requirements.txt file again in the same directory. It will be enough to enter our flask version in the file where we can list these dependencies.

requirements.txt

```
aniso8601==9.0.1
certifi==2021.10.8
charset-normalizer==2.0.11
click==8.0.3
Flask==2.0.2
Flask-RESTful==0.3.9
idna==3.3
itsdangerous==2.0.1
Jinja2==3.0.3
MarkupSafe==2.0.1
pytz==2021.3
requests==2.27.1
six==1.16.0
urllib3==1.26.8
Werkzeug==2.0.2
```


Now our app works!

**_Using CI automate the container with GitLab_**

Create the .gitlab-ci.yml file in your repository with the content below. You will have to set your own

DOCKER_REGISTRY : the repository URI without /webapi

AWS_DEFAULT_REGION : you can find it in the DOCKER_REGISTRY i.e eu-central-1

APP_NAME: name of your ECR repository i.e webapi

```
variables:
  DOCKER_REGISTRY: 165130303341.dkr.ecr.eu-central-1.amazonaws.com
  AWS_DEFAULT_REGION: eu-west-1
  APP_NAME: webapi
  DOCKER_HOST: tcp://docker:2375
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: ""

publish:
  stage: build
  image: 
    name: docker:latest
  services:
    - docker:19-dind
  before_script:
    - apk add --no-cache curl jq python3 py3-pip
    - pip install awscli
    - aws ecr get-login-password | docker login --username AWS --password-stdin $DOCKER_REGISTRY
    - aws --version
    - docker info
    - docker --version
  script:
    - docker build -t $DOCKER_REGISTRY/$APP_NAME:$CI_PIPELINE_IID .
    - docker push $DOCKER_REGISTRY/$APP_NAME:$CI_PIPELINE_IID

```
Let's have a deeper look at this gitlab-ci.yml

DOCKER_HOST : This will allow us to use the service docker:19-dind

DOCKER_DRIVER and DOCKER_TLS_CERTDIR : They help us to correct some issues.

docker:19-dind : Means that we use Docker in Docker to log in AWS in the before_script part.

In the before_script section we install awscli in docker:19-dind and create a login session to our AWS ECR. The credentials used will come from the project variables.

apk add --no-cache curl jq python3 py3-pip and pip install awscli : Will install the prerequisites for awscli and awscli itself

aws ecr get-login-password | docker login --username AWS --password-stdin $DOCKER_REGISTRY : Will create an authenticated session to the ECR registry

aws --version, docker info and docker --version : Print some informations

And finally the script section will build the Docker container with the pipeline ID as tag and push it to the ECR

If everything goes well in the CI/CD job output you will find your newly created image in the ECR repository.
