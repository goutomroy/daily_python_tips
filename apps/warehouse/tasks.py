from apps.warehouse.models import Tweet, TweetUser, TweetMedia, HashTag
from daily_python_tips import celery_app
from daily_python_tips.settings import twitter_api


class BaseTask(celery_app.Task):

    abstract = True
    autoretry_for = (Exception,)
    max_retries = 3
    trail = True
    retry_backoff = 180
    retry_backoff_max = 720

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        super(BaseTask, self).on_retry(exc, task_id, args, kwargs, einfo)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        super(BaseTask, self).on_failure(exc, task_id, args, kwargs, einfo)


@celery_app.task(bind=True, base=BaseTask)
def data_builder(self):

    tweets = twitter_api.user_timeline(screen_name='python_tip', count=10, tweet_mode="extended",
                                             include_entities=True)
    for each_tweet in tweets:

        if Tweet.objects.filter(tweet_id=each_tweet.id_str).exists():
            continue

        user_mentions = each_tweet.entities['user_mentions']
        users = []
        for each in user_mentions:
            try:
                tweet_user = TweetUser.objects.get(screen_name=each['screen_name'])
            except TweetUser.DoesNotExist:
                tweet_user = TweetUser.objects.create(screen_name=each['screen_name'])
            users.append(tweet_user)

        hash_tags = each_tweet.entities['hashtags']
        tags = []
        for each in hash_tags:
            try:
                tag = HashTag.objects.get(tag=each['text'])
            except HashTag.DoesNotExist:
                tag = HashTag.objects.create(tag=each['text'])
            tags.append(tag)

        new_tweet = Tweet.objects.create(tweet_id=each_tweet.id_str,
                                         tip=each_tweet.full_text,
                                         favorite_count=each_tweet.favorite_count,
                                         retweet_count=each_tweet.retweet_count,
                                         timestamp=each_tweet.created_at)

        if users:
            new_tweet.user_mentions.set(users)
        if tags:
            new_tweet.hash_tags.set(tags)

        media_objects = []
        if hasattr(each_tweet, 'extended_entities'):
            for each in each_tweet.extended_entities['media']:
                media_objects.append(TweetMedia(url=each['media_url_https'], tweet=new_tweet))

        if media_objects:
            TweetMedia.objects.bulk_create(media_objects)


'''

@celery_app.task(bind=True, base=BaseTask)
def data_builder(self):

    latest_tweet = twitter_api.user_timeline(screen_name='python_tip', count=10, tweet_mode="extended",
                                             include_entities=True)[0]

    if Tweet.objects.filter(tweet_id=latest_tweet.id_str).exists():
        return

    user_mentions = latest_tweet.entities['user_mentions']
    users = []
    for each in user_mentions:
        try:
            tweet_user = TweetUser.objects.get(screen_name=each['screen_name'])
        except TweetUser.DoesNotExist:
            tweet_user = TweetUser.objects.create(screen_name=each['screen_name'])
        users.append(tweet_user)

    hash_tags = latest_tweet.entities['hashtags']
    tags = []
    for each in hash_tags:
        try:
            tag = HashTag.objects.get(tag=each['text'])
        except HashTag.DoesNotExist:
            tag = HashTag.objects.create(tag=each['text'])
        tags.append(tag)

    new_tweet = Tweet.objects.create(tweet_id=latest_tweet.id_str,
                                     tip=latest_tweet.full_text,
                                     favorite_count=latest_tweet.favorite_count,
                                     retweet_count=latest_tweet.retweet_count,
                                     timestamp=latest_tweet.created_at)

    if users:
        new_tweet.user_mentions.set(users)
    if tags:
        new_tweet.hash_tags.set(tags)

    media_objects = []
    if hasattr(latest_tweet, 'extended_entities'):
        for each in latest_tweet.extended_entities['media']:
            media_objects.append(TweetMedia(url=each['media_url_https'], tweet=new_tweet))

    if media_objects:
        TweetMedia.objects.bulk_create(media_objects)

'''


@celery_app.task(bind=True, base=BaseTask)
def favourite_retweet_count_updater(self):

    for each in Tweet.objects.all().iterator():
        tweet = twitter_api.get_status(id=each.tweet_id)
        each.favorite_count = tweet.favorite_count
        each.retweet_count = tweet.retweet_count
        each.save()



