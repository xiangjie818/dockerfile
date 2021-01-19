# encoding: utf-8

from django.urls import path
from api import views

urlpatterns = [
    path('generate_cert', views.generate_cert, name='generate_cert'),
    path('revoke_cert', views.revoke_cert, name='revoke_cert'),
    path('verify_cert', views.verify_cert, name='verify_cert'),
    path('verify_cert_file', views.verify_cert_file, name='verify_cert_file'),
    path('query_cert_url', views.query_cert_url, name='query_cert_url'),
    path('hello', views.hello, name='hello')
]
