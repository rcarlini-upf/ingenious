# Ingenious Project

This is the main repository for the Ingenious European Project. 

This repository contains the different docker containers needed in order to run text-to-speech, translation and speech-to-text. Also, there is an integration component that allows to use all of the other from an integrated service.

Before running the services make sure that:
 - You have the resources in place. You'll have to download and unpack the resources for speech2text and text2speech in their respective directories. You'll find them in the releases section of the Github repository.
 - In order to be able to run the services, you'll have to install docker and docker-compose.

Once those steps are fullfiled, run the following command in the base directory:
```
docker-compose up integration
```

The different services should be build and started and you'll find the integration interface in http://localhost:4100/ .

## Text-to-Speech

TBD

## Speech-to-Text

TBD

## Translation

TBD

## Integration

TBD