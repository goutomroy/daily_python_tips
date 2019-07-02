# Daily Python Tips

This server pulls [tweets](https://twitter.com/python_tip) using celery and stores in **postgres** database.
Here we are using postgres full text search for searching tweets with query hashtags.Using [tweppy](https://www.tweepy.org/) for pulling tweets.
We have 2 celery scheduler tasks :

* Pulling tweets at 11:00am UTC.
* Updating favourite and retweet count of every tweets at 5:00am UTC.

#### Apis available

* http://127.0.0.1:8000/ - gives json list of all tweets in DB based on popularity
* http://127.0.0.1:8000/search/?q=pythontip - search api


#### Libraries Used

* celery==4.3.0
* Django==2.2.2
* django-celery-beat==1.5.0
* django-celery-results==1.1.2
* django-redis==4.10.0
* djangorestframework==3.9.4
* psycopg2-binary==2.8.3
* redis==3.2.1
* tweepy==3.7.0

#### Start development server
```
python manage.py runserver
```

#### Start development Celery
```
celery -A daily_python_tips worker -B  -l info
```
