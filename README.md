# Annotation tool - Annot8

## Installation

### Backend

1. Install requirements
```bash
cd backend
conda create -n annot8 python~=3.9.0
conda activate annot8
pip install -r requirements.txt
```

2. Create database and the DB user
```bash
sudo mysql
mysql> CREATE DATABASE annot8;
mysql> CREATE USER 'annot8'@'localhost' IDENTIFIED BY '<password>';
mysql> GRANT ALL PRIVILEGES ON annot8 . * TO 'annot8'@'localhost';
mysql> FLUSH PRIVILEGES;
```
3. Set the correct credentials in the `mysql.cnf`
```bash
cp mysql.template.cnf mysql.cnf
chmod 600 mysql.cnf

<edit mysql.cnf accordingly>
```



4. Apply DB migrations and run the Django App

```bash
python manage.py migrate
python manage.py runserver
```

5. (Optional) Create a superuser:

```bash
python manage.py createsuperuser
```

### Frontend

#### Project setup
```
sudo npm install -g @vue/cli
npm install
```

#### Compiles and hot-reloads for development
```
npm run serve
```

#### Compiles and minifies for production
```
npm run build
```

#### Lints and fixes files
```
npm run lint
```

#### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

