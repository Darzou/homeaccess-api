# Dahua VTO Home Access Rest API

## Introduction

This is a Rest API to serve access authorization calls from Dahua's VTO.

## Getting started

First, update your configuration and logging preferences:

1) Copy **config.sample.py** to **config.py**
2) Copy **logging.example.yml** to **logging.yml**
3) Update the new files created above with your preferences
4) Activate a virtualenv (*python3*) and install the **requirements.pip** (*pip install -r requirements.pip*)

### Start the API:

You can start it by **flask run** or using docker (c.f. **Dockerfile**).

Openhab's rule will listen to MQTT *AccessControl* events on *_/DoorCard/Event topic* (through the Dahua2Mqtt app) and call this Rest API's endpoint for access authorizations.
