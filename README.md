# text_summarization
ML Text Summarization project

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

Now you can start the Jupyter lab server:

```sh
jupyter lab
```

If working on WSL under Windows, add `--no-browser`.