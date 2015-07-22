## Welcome

This tutorial is a work in progress.

## Tutorial

### 1. Clone (or fork and clone) this repository to your development box

### 2. Initialize the Django development server environment

#### Install

Install PostgreSQL and Python 3.4.x.
Optionally install pyenv, virtualenv, etc. to manage python environments.

#### Python packages

Install Django and the PostgreSQL database adapter.

```bash
$ pip install Django
$ pip install psycopg2
```

#### Setup database

Create login role.

```sql
CREATE ROLE leaderboard_django LOGIN
  PASSWORD 'leaderboard_django'
  NOSUPERUSER INHERIT CREATEDB NOCREATEROLE NOREPLICATION;
```
Create database.

```sql
CREATE DATABASE leaderboard_django
  WITH OWNER = leaderboard_django
       ENCODING = 'UTF8'
       TABLESPACE = pg_default
       LC_COLLATE = 'en_US.UTF-8'
       LC_CTYPE = 'en_US.UTF-8'
       CONNECTION LIMIT = -1;
```

Create table structure.

```bash
$ python manage.py migrate
```

#### Start server

```bash
$ python manage.py runserver
```

### 3. Add some initial data

Hit the server in your browser at http://localhost:8000/.  It will immediately
redirect to the company leaderboard for the fictitious company
"Vandalay Industries".

In your browser javascript console, add scores to leaderboard:

```javascript
window.leaderboard.add({name: 'George Costanza', score: 10});
window.leaderboard.add({name: 'Elaine Benes', score: 105});
```

You can also add more than one employee at a time by passing an array of 
objects to `leaderboard.add()`.

```javascript
window.leaderboard.add([{name: 'Jerry Seinfeld', score: 110},{name: 'Cosmo Kramer', score: 100}]);
```

Note that you are adding scores to the leaderboard, not updating the score
value. If we add another 10 "points" to Kramer, his score updates to
110.

```javascript
window.leaderboard.add({name: 'Cosmo Kramer', score: 10});
```

The `leaderboard` object updates the scores on the server and emits
events for leaders who were added or updated along with their new total
score.

### 4. Understanding the template app

The template application comes with 3 models and a couple of really simple
views and actions to update those models.

`Company` is the root object for any organization and its leaderboard.
We identify companies by a `uid` field (which doubles as name in the
"Vandalay Industries" example.)

`Leader` is a person that belongs to a company, and a company can have
many leaders.

`Score` is a number and a timestamp that belongs to a leader. A leader
can have many scores over time. Additionally, scores can have an
arbitrary `category`.

In this example, the category is hard-coded in a few places to "close"
so that we create a leaderboard of "closers." Coffee is for closers.

### 5. Register your app in the Spiceworks Developer Edition

TODO

### 6. Change the index.html redirect logic to redirect per company

TODO

### 7. Extend the leaders.html logic to update leaders with Spiceworks app data

TODO
