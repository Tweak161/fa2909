# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Result
from .serializers import StockSerializer

from django.shortcuts import render

# Create your views here.
# stocks/
class ResultList(APIView):
    def get(self, request):
        # Return all Stocks from the database
        stocks = Result.objects.all()  # Get all Stocks from database
        serializer = StockSerializer(stocks, many=True)
        return Response(serializer.data)

    def post(self, request):
        pass
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)