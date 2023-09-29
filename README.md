# Podcast Project
`Podcast Project` is a Parser and written in Django!

## Table of Contents
- [Podcast Project](#rss-feed-django-project)
  - [About the Project](#about-the-project)
  - [Licence](#licence)
  - [Setup](#setup)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Running the Project](#running-the-project)
    - [Contributing](#contributing)



## About the Project
This project is a `RSS Feeds Parser` and create with `Django Rest Framework`; In This project I use powerful tools like `Docker`, `Celery`, `Redis`, `Rabbitmq` and etc; This project show you How rss parsers are parsing xml and rss file!
In this `README` you can see some information about project and how can you SETUP it!


## Licence
`Podcast Project` license is here -> (read more [here](/LICENSE))



## Setup

### Prerequisites
Before setting up the `Podcast Project`, ensure that you have the following prerequisites installed on your machine:

- Python
- Django


### Installation
Follow these steps to set up the project:

Tip: If you use linux you can use `python3` instead of `python`

Clone the repository using Git:

```bash
git clone https://github.com/hosseink9/PodcastProject.git
```
Change into the project directory:
```bash
cd PodcastProject/src
```
Create a virtual environment (optional but recommended):
```bash
python -m virtualenv .venv
```
or

```bash
pipenv shell
```

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

Set up the database:

```bash
python manage.py migrate
```
This will apply the database migrations and create the necessary tables.

Create a superuser account (admin):

```bash
python manage.py createsuperuser
```
Follow the prompts to set a phone number and password for the admin account.
RSS Feed Django project
Congratulations! The Podcast Project has been successfully set up on your machine.


### Running the Project
To run the Podcast Project, follow these steps:

Activate the virtual environment (if not already activated):

For Windows:

```bash
env\Scripts\activate
```
For macOS/Linux:

```bash
source env/bin/activate
```
For use pipenv shell:

```bash
pipenv shell
```
Start the server:

```bash
python manage.py runserver
```


### Contributing
We welcome contributions to the `Podcast Project`.
We use git-flow branching methods to contribute to `Podcast Project`
If you'd like to contribute, please follow these steps:

Fork the repository on GitHub.

Clone your forked repository to your local machine:

```bash
git clone https://github.com/hosseink9/PodcastProject.git
```
Create a new branch for your changes:


```bash
git checkout -b feature/your-feature-name
```
