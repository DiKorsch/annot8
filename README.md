# Annotation tool - Annot8

## Installation

### Backend

1. Install requirements
```bash
sudo apt install -y redis
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
mysql> GRANT ALL PRIVILEGES ON annot8_tests . * TO 'annot8'@'localhost';
mysql> FLUSH PRIVILEGES;
```
*Note: Do not create the database `annot_tests`, django will care about creation and destruction. We just need to grant the privileges to the user.*

3. Set the correct credentials in the `mysql.cnf`
```bash
cp mysql.template.cnf mysql.cnf
chmod 600 mysql.cnf
<edit mysql.cnf accordingly>
```



4. Apply DB migrations and run the Django app

```bash
python manage.py migrate
python manage.py loaddata fixtures/labels.json
python manage.py runserver
```

5. In a separate terminal, start the Django-Q job cluster:

```bash
python manage.py qcluster
```

6. (Optional, recommended) Create a superuser:

```bash
python manage.py createsuperuser
```

#### Known Issues
##### Loading of the fixtures
If you experience this problem loading fixtures:

```bash
django.db.utils.OperationalError: Problem installing fixture [...] Could not load labeltree.Label(pk=4527218): (1366, "Incorrect string value: '[...]' for column 'authors' at row 1"
```

you will need to change the charset of the schema and the labeltree tables. First, login to the mysql server via CLI or some other interface. Then change the charset:

```sql
ALTER DATABASE annot8 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE annot8;
ALTER TABLE labeltree_label CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE labeltree_labelgroup CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE labeltree_labelgroup_species CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Frontend

#### Project setup
```bash
sudo npm install -g @vue/cli
npm install
```

#### Compiles and hot-reloads for development
```bash
npm run serve
```

#### Compiles and minifies for production
```bash
npm run build
```

#### Lints and fixes files
```bash
npm run lint
```

#### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

