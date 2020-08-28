import requests
from django.http.response import HttpResponseBadRequest, HttpResponse
from django.views import generic
from django.shortcuts import render
from new_parser.models import Task
from bs4 import BeautifulSoup
from new_parser.forms import TaskForm


class ParseURLAjax(generic.View):
    http_method_names = ["get", "post"]

    @staticmethod
    def get_meta_content(page_content, look_up_attr):
        """ Tries to find first meta tag in scrapped content of web page with given 'look_up_attr' """
        meta_attr_value = page_content.find("meta", attrs=look_up_attr)
        if meta_attr_value:
            if meta_attr_value != "image_url":
                return meta_attr_value.get("content")
            else:
                return meta_attr_value.get("src")
        return None

    def prepare_scrapped_data(self, page_content):
        website_data = {"title": "", "description": "", "site_name": "", "image": ""}
        for attribute in ("title", "description", "site_name", "image"):
            # required data can be included in Open Graph meta tags, which have different format therefore
            # second call to 'get_meta_content' function
            attr_value = self.get_meta_content(
                page_content, {"name": f"{attribute}"}
            ) | self.get_meta_content(page_content, {"property": f"og:{attribute}"})
            if attr_value:
                website_data.update({attribute: attr_value})
        return website_data

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if form.is_valid:
            url_to_parse = form.cleaned_data.get("parsed_url")
            response = requests.get(url_to_parse)
            if response != 200:
                response.raise_for_status()
            soup = BeautifulSoup(response.content, "lxml")
            scrapped_data = self.prepare_scrapped_data(soup)
            Task.objects.create(**scrapped_data, parsed_url=url_to_parse)
            return HttpResponse(
                content="Website successfully parsed and saved.", status_code=201
            )
        return HttpResponseBadRequest(content="Please input valid URL.")

    def get(self, request, *args, **kwargs):
        form = TaskForm()
        return render(request, template_name="url_form.html", context={"form": form})


class GetData(generic.ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "task_list.html"
    fields = ("parsed_url", "title", "description", "site_name", )
