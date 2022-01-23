[[_TOC_]]

# Project Setup
1. Install pyenv from https://github.com/pyenv/pyenv-installer
```
# Ubuntu: make sure you also have libffi-dev installed (otherwise poetry install will fail, below)
apt install libffi-dev

pyenv install 3.9.6
pyenv global system 3.9.6   # make python 3.9.6 available as python3.9 in your system
```

2. Get Poetry from here https://python-poetry.org/

3. Initialize the environment 
``` 
 #in this directory
 poetry install 
```

## Check the project
This runs all unittests, checks the code formatting, code style etc. and FAILS if anything looks funky. 
```
poetry shell  # only if you are not already in a poetry shell
poe check
```

## Test server locally

```
poetry shell
uvicorn uvicorn poetry_example.main:app --reload
```
Now:
- go to http://127.0.0.1:8000/redoc  and look at the API docs
- go to http://127.0.0.1:8000/docs , check the documentation and try out a request.

## Using PyCharm?
If you develop using PyCharm, your life will become easier if you install the plug-ins _pydantic_, _mypy_ and 
_pylint_.

### Black
PyCharm still doesn't support the black code style natively (which we use in this project), so you must follow these
instructions to define a black shortcut:

https://black.readthedocs.io/en/stable/integrations/editors.html#pycharm-intellij-idea


### Uvicorn
In order to start uvicorn in PyCharm, create a configuration with: 
* Module name (**not** script path): uvicorn
* Parameters: poetry_example.main:app --reload



# Dockerize
## Build the Docker image
Recommended: use the build script:
```
poetry shell  # only if you are not already in a poetry shell
poe docker
```

Manually: see https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker
```
poetry build
poetry run poetry-lock-package --build

docker build -t poetry_example/example:0.0.1.dev .  # use correct version instead of 0.0.1.dev  !
```

### Test Docker image
```
docker run --rm -p 8000:8000 poetry_example/example:0.0.1.dev   # use correct version instead of 0.0.1.dev  !
```

Now go to http://localhost:8000/docs

### Deploy the image on a server
1. Transfer the image
```
docker save -o /tmp/image.docker poetry_example/example:1.2.3
scp /tmp/image.docker  user@docker.host:
```
2. Import and run
```
# on the docker.host
docker load -i image.docker

# test the container
docker run --rm -p 8000:8000 poetry_example/example:1.2.3   

# now create a docker container or run your docker compose commands

```

# Releasing
First make sure that
- your build is not broken (see CI pipeline in gitlab)
- your working directory is clean (no uncommitted changes in tracked files)
- you are currently working on the .dev version you want to release (e.g. if you are currenlty working on 1.2.3.dev, then the release will become 1.2.3)
- you do not have any .dev dependencies

Then run
``` 
poetry shell
poe release
```
This will do some sanity checks, set the version for release, create a tag and start the next dev version.

Check if you are happy with the changes and commits made by the build script. If everything looks okay run
```
git push origin
git push origin <version tag>
```

or

```
git push origin --follow-tags
```


