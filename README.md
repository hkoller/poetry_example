[[_TOC_]]

# Project Setup
(written for Ubuntu Linux. Windows might work similarily in principle, but is probably quite different when it comes to details..)
## Install Pyenv, Poetry and setup the project environment

1. Install pyenv 
from https://github.com/pyenv/pyenv-installer

Then: 
```
# Ubuntu: make sure you also have libffi-dev installed (otherwise poetry install will fail, below)
apt install libffi-dev

pyenv install 3.9.6
pyenv global system 3.9.6   # make python 3.9.6 available as python3.9 in your system
```

2. Get Poetry 
see https://python-poetry.org/docs for details but its usually just a
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

3. Initialize the environment 
``` 
# in this directory
poetry install 
```

Now you should be able to start a poetry shell to enter the poetry dev environment:
```
python --version  # Output should be whatevery your regular system Python version is

poetry shell  # start the shell

python --version  # Output should now be: Python 3.9.6 (as defined in pyproject.toml)
```


## Check the project
```
poetry shell  # only if you are not already in a poetry shell
poe check   # not a typo! poe is a neat little task runner for poetry (see https://github.com/nat-n/poethepoet )
```
This runs all unittests, checks the code formatting, code style etc. and FAILS if anything looks funky. 

## Test server locally

```
poetry shell
uvicorn poetry_example.main:app --reload
```
Now:
- go to http://127.0.0.1:8000/redoc  and look at the pretty API docs
- go to http://127.0.0.1:8000/docs  the API docs are less pretty there, but you can directly try out requests

## Using PyCharm
### Setup: make Pycharm use the Poetry environment
This step is required. The poetry environment contains a Python interpreter and all the poetry-managed dependencies. We need to tell Pycharm to use that. 

So first find out where the Poetry environment is stored:
```
poetry env info  # look at the contents of the Path: variable
```
Now, in Pycharm add a "System Interpreter" for the project and point it to the python3.9 binary in the Poetry environment. 

**Warning:** if PyCharm ever suggests to install or update Python packages for you: **DON'T** let it. Python packages **need** to be installed and managed by Poetry (```poetry add some_package```)

### Tools
(Optional, but) your life will become easier if you install the plug-ins _pydantic_, _mypy_ and _pylint_.

#### Black Code Formatter
PyCharm still doesn't support the black code style natively (which we use in this project), so you must follow these instructions to define a black shortcut:

https://black.readthedocs.io/en/stable/integrations/editors.html#pycharm-intellij-idea


#### Uvicorn
Completely optional (I prefer the commandline). But if you want to start uvicorn directly from PyCharm, you can create a Pycharm module configuration with these properties: 
* Module name (**not** script path): uvicorn
* Parameters: poetry_example.main:app --reload


# Dockerize your project
## Build the Docker image
Recommended - use the poe build script:
```
poetry shell  # only if you are not already in a poetry shell
poe docker
```

Manually: (see https://stackoverflow.com/questions/53835198/integrating-python-poetry-with-docker )
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

### Deploy the Docker image on a server
1. Transfer the image to the docker.host
```
docker save -o /tmp/image.docker poetry_example/example:1.2.3
scp /tmp/image.docker  user@docker.host:
```
2. Import and run the image on the docker.host
```
# on the docker.host
docker load -i image.docker

# test the image
docker run --rm -p 8000:8000 poetry_example/example:1.2.3   

# now create a docker container, run your docker compose commands etc.

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

