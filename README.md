# Ai2 Coding Exercise

For this project. I've chosen to go with a dockerized Flask app using APIFlask and MongoDB. 
I chose this combination for ease of use, being able to quickly set it up, as well as simplicity in running on other machines. 
APIFlask was a choice based on some of the features offered, including built in validation through the APIFlask `Schema`.
The main reason I chose MongoDB was simply to get to play around with it and learn a little bit. I haven't been able to use Mongo in a professional capacity, but I've always wanted to based on things that I've read. 
Depending on requirements learned later in the process, this choice may need to change. 
Postman was used for building requests for localized testing.

## Prerequisites
Docker... that's pretty much it! 
I'm using the image `python:3.10.4-alpine3.16` which has most everything baked in. As long as you have Docker installed you should be good. 

## Running
I've set up a simple `docker-compose` file that spins up both services. 

Build the docker services.
```shell
docker compose build
```

Spin up the services
```shell
docker compose up -d
```
As the services get spun up, the `api/Dockerfile` installs the python requirements and starts the server. 


### Questions:
As I was working on this project... I kept going back and forth on how to handle the callback function. 
I thought it made some sense to have the `tipIdentifier` as part of the path... IE `/api/tip/<tipIdentifier>/callback` but ultimately chose to stick to the explicit instructions instead. 
Also, with more time I would like to better organize the project structure and build the data layer out a bit more with maybe a `tipsService` that abstracts the data layer logic out of the base `api.py` file. 
I felt a bit rushed with our trip to Disneyland approaching, but hopefully it isn't too bad with the little time I had.

Thank you for the opportunity! 