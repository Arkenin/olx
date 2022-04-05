# OLX scraping app

The application is used to download data from a popular classifieds service: OLX. The purpose is to monitor interesting offers and collect information about prices. The saved data extracted from the offers are stored in a database, allowing for future price and offer comparisons.


## Requirements

To run app you need docker with docker-compose.
You can also use virtual env. Python packages are listed in requirements.txt file


## Building the containers

```sh
make build
make up
# or
make all # builds, brings containers up
```


## Running the tests

```sh
make test
# or, if you have a local virtualenv
pytest tests/unit
pytest tests/integration
```


## Makefile

There are some useful commands in the makefile, have a look and try them out.

