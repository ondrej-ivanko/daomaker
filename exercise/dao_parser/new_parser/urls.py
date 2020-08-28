from django.urls import path
from new_parser.views import ParseURLAjax, GetData

urlpatterns = [
    path("parser/", ParseURLAjax.as_view(), name="parser"),
    path("items/", GetData.as_view(), name="parsed_items"),
]
