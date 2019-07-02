from rest_framework import serializers
from apps.warehouse.models import HashTag, Tweet, TweetUser, TweetMedia


class TweetMediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = TweetMedia
        fields = ('url',)


class TweetUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = TweetUser
        fields = ('screen_name',)


class TweetSerializer(serializers.ModelSerializer):
    user_mentions = TweetUserSerializer(read_only=True, many=True)
    tweet_media = TweetMediaSerializer(read_only=True, many=True)

    class Meta:
        model = Tweet
        fields = ('id', 'tweet_id', 'tip', 'favorite_count', 'retweet_count', 'timestamp', 'user_mentions', 'tweet_media')


class TweetSerializerSearch(serializers.ModelSerializer):
    tweet_media = TweetMediaSerializer(read_only=True, many=True)

    class Meta:
        model = Tweet
        fields = ('id', 'tweet_id', 'tip', 'timestamp', 'tweet_media')


class HashTagSerializer(serializers.ModelSerializer):
    tweets = TweetSerializer(read_only=True, many=True)

    class Meta:
        model = HashTag
        fields = ('id', 'tag', 'tweets')
