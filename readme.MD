# Getting started

1. Install Docker and [docker-compose](https://docs.docker.com/compose/install/)

2. Build and run containers, then move inside `app`

```bash
docker-compose build
docker-compose up -d
docker-compose exec app bash
```

3. Set up database
```bash
flask db upgrade
```

4. Open [localhost:5000](http://localhost:5000) in your browser
