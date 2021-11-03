# text_summarization
ML Text Summarization project

This project is to build and deploy:
- [x] A summarization model by using transfer learning from a pretrained T5 model and fine-tuning with BBC News summary dataset. 
- [x] A backend application to initialize and serve the summarization model.
- [x] A REACT web application that input text and output summarized text. The application will provide evaluation metrics when reference summary is provided. 


## Local Setup

The following instructions should work on Linux, Windows and MacOS. If you are a Windows user familiar with Linux, you should check out the [Windows Subsystem for Linux, Version 2 (WSL2)](https://docs.microsoft.com/en-us/windows/wsl/). This allows to use a Linux system on the Windows machine. However, using native Windows should also be no problem.

It is helpful to install `git` on your machine, but you can also download the full repository from Github as a zip file. If you use `git`, run the following commands from the command line:

```sh
git clone https://github.com/furyhawk/text_summarization.git
cd text_summarization
```

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


Login to huggingface as needed:

```sh
huggingface-cli login
```

## Backend Setup

Commandline run
```sh
uvicorn app.text_sum_endpoint:app --host 0.0.0.0 --port 8000
```

or

```sh
python ./app/text_sum_endpoint.py
```

or

Container setup
```sh
docker build -t textsum_endpoint .
docker run -d --name textsum_endpoint -p 8000:8000 textsum_endpoint
```

Test backend on
http://localhost:8000/docs

## Frontend Setup

```sh
cd frontend\textsum
npm install
npm start
```

or

for dockerized dev environment
```sh
cd frontend\textsum
docker-compose -f docker-compose.dev.yml up -d
```
This will create a new browser tab with Summarization App in DEV env. Run again using just 'npm start'.

## Just run
```sh
run
```
