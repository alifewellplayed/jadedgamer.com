from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

from coreExtend import views as coreViews
from aggregator import views as feedViews
from news import views as newsViews

lists_endpoint = [
    path("default/", feedViews.DefaultListView.as_view(), name="DefaultListView"),
    path("all/", feedViews.AllFeedsListView.as_view(), name="AllListView"),
]

news_endpoint = [
    path("latest/", feedViews.FeedItemAPIView.as_view(), name="LatestNews"),
    path("popular/", feedViews.FeedItemPopularAPIView.as_view(), name="PopularNews"),
    path("search/", feedViews.FeedItemAPIView.as_view(), name="Search"),
]

tags_endpoint = [
    path("all/", feedViews.AllTagsView.as_view(), name="TagsListView"),
]

app_name = "jaded.api"
urlpatterns = [
    path("lists/", include(lists_endpoint)),
    path("news/", include(news_endpoint)),
    path("tags/", include(tags_endpoint)),
    path("token_auth/", obtain_jwt_token),
    path("token_verify/", verify_jwt_token),
    path("current_user/", coreViews.current_user.as_view()),
]
