from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class TweetUser(models.Model):
    screen_name = models.CharField(max_length=140, unique=True)

    def __str__(self):
        return self.screen_name


class HashTag(models.Model):
    tag = models.CharField(max_length=140, unique=True)

    def __str__(self):
        return self.tag


class Tweet(models.Model):

    tweet_id = models.CharField(max_length=140, unique=True)
    tip = models.CharField(max_length=140)
    user_mentions = models.ManyToManyField(TweetUser, blank=True)
    hash_tags = models.ManyToManyField(HashTag, blank=True)
    favorite_count = models.IntegerField(default=0)
    retweet_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField()
    search = SearchVectorField(null=True)

    class Meta(object):
        ordering = ('-favorite_count',)
        default_related_name = 'tweets'

    def __str__(self):
        return self.tip


class TweetMedia(models.Model):
    url = models.URLField(max_length=500)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'tweet_media'

    def __str__(self):
        return str(self.tweet)


@receiver(post_save, sender=Tweet)
def update_search_vector(sender, instance, **kwargs):
    Tweet.objects.filter(pk=instance.pk).update(search=SearchVector('tip'))
