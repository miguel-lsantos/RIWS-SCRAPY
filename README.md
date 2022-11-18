# RIWS-SCRAPY

This is a simple web scraper for the RIWS website. It is written in Python and uses the Scrapy framework and elastic search.
Frontend is written in React with reactivesearch.

To run the project you need to have docker and docker-compose installed.

## Run the project
To run the elastic search and the scraper you need to run the following command:
```bash
make run-scrapy # create venv, install dependencies, run elastic search and scrapy
```

To run the frontend you need to run the following command:
```bash
make run-web # runs a web in localhost:3000 
```

To stop the elasticsearch:
```bash
make elastic-down
```

## Issues
If you have any issues with the project related with venv or dependencies you can run the following command:
```bash
make clean # remove venv and dependencies
```

## Dependencies

Python3.9+ (pythonX-venv)
npm 8.19.2
