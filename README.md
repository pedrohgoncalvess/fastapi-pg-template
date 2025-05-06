# Readme structure.

## Title

### Short description

### Explain the folder architecture

### Configurations to run tests/project

Use this default, modify with your needs:

Requires make installed.

```bash
make setup
```

Or using uv (requires Python 3.13.3 installed and UV). 
Create a virtual env.
```
uv init
```


## YoYo.

Generate new migration.
```
yoyo new --sql -m "message"
```

Run migration. 

*Configure yoyo.ini.*
```
yoyo apply
```

## Running application

Install docker and docker-compose.
```
docker-compose up -d
```