from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.warehouse.models import HashTag, Tweet
from apps.warehouse.serializers import HashTagSerializer, TweetSerializerSearch, TweetSerializer
from daily_python_tips.paginator import StandardResultsSetPagination


class MainViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    pagination_class = StandardResultsSetPagination

    @action(methods=['get'], permission_classes=[AllowAny], detail=False)
    def search(self, request):
        q = request.GET['q']

        vector = SearchVector('tip', weight='A')
        query = SearchQuery(q, search_type='phrase')
        rank = SearchRank(vector, query)
        tweets = Tweet.objects.annotate(rank=rank).filter(rank__gte=0.3).order_by('-rank')
        serializer = TweetSerializerSearch(tweets, many=True)
        return Response({'items': serializer.data})
