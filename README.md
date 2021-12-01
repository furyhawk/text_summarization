# text_summarization
ML Text Summarization project

This project is to build and deploy:
- [x] A summarization model by using transfer learning from a pretrained T5 model and fine-tuning with BBC News summary dataset. 
- [x] A backend application to initialize and serve the summarization model.
- [x] A REACT web application that input text and output summarized text. The application will provide evaluation metrics when reference summary is provided. 

![Example](https://github.com/furyhawk/text_summarization/blob/main/img/example00.png?raw=true)

## Local Setup

The following instructions should work on Linux, Windows and MacOS. If you are a Windows user familiar with Linux, you should check out the [Windows Subsystem for Linux, Version 2 (WSL2)](https://docs.microsoft.com/en-us/windows/wsl/). This allows to use a Linux system on the Windows machine. However, using native Windows should also be no problem.

It is helpful to install `git` on your machine, but you can also download the full repository from Github as a zip file. If you use `git`, run the following commands from the command line:

```sh
git clone https://github.com/furyhawk/text_summarization.git
cd text_summarization
```


Skip to [Backend](https://github.com/furyhawk/text_summarization#backend-setup) and [Frontend](https://github.com/furyhawk/text_summarization#frontend-setup) setup if you do not need to run the notebooks.

### Jupyter notebooks setup
For local setup, we recommend to use [Miniconda](https://docs.conda.io/en/latest/miniconda.html), a minimal version of the popular [Anaconda](https://www.anaconda.com/) distribution that contains only the package manager `conda` and Python. Follow the installation instructions on the [Miniconda Homepage](https://docs.conda.io/en/latest/miniconda.html).

After installation of Anaconda/Miniconda, run the following command(s) from the project directory:

```sh
conda env create --name text --file text.yml
conda activate text
```

For windows:
download git-lfs from https://git-lfs.github.com/
and install

```sh
git lfs install
```

Now you can start the Jupyter lab server:

```sh
jupyter lab
```

If working on WSL under Windows, add `--no-browser`.


If you need to fine tune your own model, sign up free at https://huggingface.co/ . Login to huggingface as needed:

```sh
huggingface-cli login
```

# Container for backend and front setup
```sh
docker-compose -f docker-compose.yml up -d
```
Test frontend on
http://localhost:3000/
Test backend on
http://localhost:8000/docs

Do note that the Transformer will download up to 2GB of models.
![Container Init](https://github.com/furyhawk/text_summarization/blob/main/img/endpoint_docker_init.png?raw=true)

You can skip below container setup.

## Backend Setup

#### Commandline run

 from /backend
```sh
cd backend
```
run
```sh
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
or
```sh
python ./app/main.py
```

## Frontend Setup

#### npm dev env
```sh
cd frontend\textsum
npm install
npm start
```
This will create a new browser tab with Summarization App in DEV env. Run again using just 'npm start'.

<!-- or
docker network create --driver bridge localnetwork
#### for dockerized dev environment
```sh
cd frontend\textsum
docker-compose -f docker-compose.dev.yml up -d
```

Test frontend on
http://localhost:3000/

## Just run
```sh
run
``` -->

# Pushing a Docker container image to Docker Hub
To push an image to Docker Hub, you must first name your local image using your Docker Hub username and the repository name that you created through Docker Hub on the web.

You can add multiple images to a repository by adding a specific :<tag> to them (for example docs/base:testing). If it’s not specified, the tag defaults to latest.

```sh
docker build . -t <hub-user>/textsum_endpoint:latest
docker push <hub-user>/textsum_endpoint:latest
```

# Dataset

This dataset was created using a dataset used for data categorization that onsists of 2225 documents from the BBC news website corresponding to stories in five topical areas from 2004-2005 used in the paper of D. Greene and P. Cunningham. "Practical Solutions to the Problem of Diagonal Dominance in Kernel Document Clustering", Proc. ICML 2006; whose all rights, including copyright, in the content of the original articles are owned by the BBC. More at http://mlg.ucd.ie/datasets/bbc.html

# Credits

https://github.com/huggingface/notebooks/blob/master/examples/summarization.ipynb

https://github.com/blueprints-for-text-analytics-python/blueprints-text

https://github.com/jessevig/bertviz.git

