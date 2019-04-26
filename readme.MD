# Getting started

1. Install Docker and [docker-compose](https://docs.docker.com/compose/install/)

2. Build and run containers.

```bash
docker-compose build
docker-compose up -d
```

3. Open [localhost:5000](http://localhost:5000) in your browser.

4. (optional) Open [localhost:7474](http://localhost:7474) to browse graph database.

# Dumping and loading database

A simple bash script located in `/bin/db` is provided to load and dump databases.

Previously dumped files you wish to load must be placed in the `/import` folder and new dumps will also be created there.

This process will only worked if the `neo4j` container isn't currently running, so make sure to execute `docker-compose down` before running these operations.

## Dumping the current database
This will create a new file at `/import/example.dump`
```bash
bin/db dump example.dump
```

## Loading a new database
This will load the contents of `/import/example.dump`
```bash
bin/db load example.dump
```
