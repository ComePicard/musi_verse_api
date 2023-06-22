import rest_framework.views
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article, Image

import json

class ArticleCreate(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        data = request.data
        #TODO data valid
        if True:
            new_article = Article()
            new_article.name = data['name']
            new_article.categories = data['categories']
            new_article.descritpion = data['descritpion']
            new_article.price_range = data['price_range']
            new_article.route = data['name'].strip().replace(" ","_").lower()
            new_article.author = request.user
            new_article.save()
            return Response(f"Article {data['name']} created")


class ArticleGetNames(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        values =Article.objects.values_list('name', 'categories',"route")
        Article.objects.values_list('name', 'categories', "route")
        result = []
        for name,categories,route in values:
            result.append({'name': name, 'value': categories, 'route':route })

        return Response(result)


class ArticleGetInfos(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, route):
        article = Article.objects.get(route=route)
        article.views += 1
        article.save()
        article_dict = model_to_dict(article)
        serialized_data = json.dumps(article_dict, ensure_ascii=False)
        return Response(json.loads(serialized_data))


class UploadImageToArticle(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        data = request.data
        #TODO data valid
        if True:
            new_image = Image()
            new_image.name = data['name']
            new_image.image = request.FILES['image']
            new_image.descritpion = data['descritpion']
            new_image.author = request.user
            new_image.article = Article.objects.get(id=data['article'])
            new_image.save()
            return Response(f"Image {data['name']} was uploaded")