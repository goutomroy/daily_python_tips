from django.contrib import admin
from apps.warehouse.models import Tweet, TweetUser, TweetMedia, HashTag

admin.site.register(Tweet)
admin.site.register(TweetUser)
admin.site.register(TweetMedia)
admin.site.register(HashTag)