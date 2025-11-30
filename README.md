# Autoresponder

> This application is an automatic email autoresponder web app. If a user does not receive a reply within a specified number of minutes or hours, the system will automatically send a response email.


#### If want to run this application is your local developer sever follow this steps:

##### Instruction:

```bash
git clone https://github.com/mbrsagor/autoresponder.git
cd autoresponder
virtualenv venv --python=python3.12
source venv/bin/activate
pip install -r requirements.txt 
```

###### Copy .sample.env and create `.env` file and paste and set current values.

#### Migrate
```bash
python manage.py makemigrations user
python manage.py migrate
```

#### Finally run this server.

```bash
python manage.py runserver
```

### Dockerization:

```bash
docker compose up --build 
```

#### Manually, create PostgreSql database:

> Open your terminal and run this command like this:

```bash
psql -U postgres  
```
> Then set enter your PostgreSql password

```psql
create database autoresponder;
```
