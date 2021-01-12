# Overview
This is a template for generating a reproducible Python environment for data science within a docker environment. The current base setup is like the following:

|Package|Usage|
|-------|-----|
|`docker`| OS environment|
|`poetry`|Python package manager|
|`jupyter notebook`|Development environment|

# Steps for environment creation

0. Create environment files (e.g. copy examples)
```bash
cp env/.jupyter.env.example env/.jupyter.env
```

1. Build docker container
```bash
sudo docker-compose build .
```

2.1 Start `python` within docker container
```bash
sudo docker-compose run code python
```

2.2 Start jupyter notebook
```
sudo docker-compose up --build
```

# Add a python package

1. Use `poetry` to add package and resolve dependencies
```
sudo docker-compose run code poetry add <package>
```

2. Commit changes to git
```
git add code/poetry.lock code/pyproject.toml
```

# New download

To start a new download follow these steps:


1. Stop docker-compose
```shell
docker-compose stop
```
2. Edit python script
```shell
vim code/example.py
```
3. Start worker nodes
```shell
uid=$(id -u) gid=$(id -g) docker-comkkkkpose up -d --build --scale worker=8
```
4. Enter container
```shell
docker exec -it ml-ecmwf_code_1 bash
```
5. Execute script
```shell
python example.py
```

