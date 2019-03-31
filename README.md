# Usage

## Build

```sh
docker-compose build
```

## Execute

```sh
#locate account.json and links.txt to script/
docker-compose up -d
docker exec -ti python-gpparse bash
python gpscrape.py
```

