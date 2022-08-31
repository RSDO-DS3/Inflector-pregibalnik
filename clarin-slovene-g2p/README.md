Slovene G2P converter
======================

# System requirements
- Ubuntu 20.04 (tested), should work with other linux distributions
- Python 3.9 (tested), should work with more recent versions

# Development setup
After cloning the repository one has to install all dependencies that are listed inside `requirements.txt` file.
The preferred way of installing the dependencies is using python virtual environment to avoid version conflicts with already installed system packages.

```bash
# Create virtual environment inside .venv folder
python3 -m venv .env

# Activate virtual environment
source env/bin/activate

# Install required packages inside virtual environment
pip install -r requirements.txt
```

The application also needs following data files and folders to present:
- `dict/` directory
- `mte_6_dict_sl_en.tsv` file

The application expects that the folder named `data` exists on the same level as `src` folder with all of the above listed files and folders nested inside it.
Data files are not versioned inside this repository but are hosted separately on package registry.

# Running the application
## Running directly on the host machine

After installing all required dependencies as described in the previous section, run the following commands to run application from the command line:
```bash
# Move to source directory
cd src

# Run the application
uvicorn service:app --port 8080
```

## Running using docker image
If application is to be deployed using docker then there is no need for python or any of the dependencies to be available on host machine.
One simply has to build docker image with the help of provided `Dockerfile`, which contains all required information to build docker image containing necessary dependencies.
Execute the following command from the root directory to build docker image and save it to the docker daemon:
```bash
docker build -t tag/name .
```

After the image is successfully built, the application can be run by using `docker run` command or with the help of `docker-compose` tool.
Following is the example of `docker-compose.yaml` file that can be used as a starting point when deploying application with `docker-compose`.
Because data files and folders are not baked to the docker image they have to be mounted at runtime:
```yaml
version: '3.3'

services:
  g2p:
    image: tag/name
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
    networks:
      - pregibalnik
    volumes:
      - ./data/dict:/app/data/dict
      - ./data/mte_6_dict_sl_en.tsv:/app/data/mte_6_dict_sl_en.tsv
    ports:
      - '9093:8080'
    expose:
      - '8080'

networks:
  pregibalnik:
    external: true
```