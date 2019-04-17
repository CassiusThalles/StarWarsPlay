from django.urls import path
from . import views

urlpatterns = [
	path('', views.Index.as_view(), name='index'),
	path('hints/', views.Hints.as_view(), name='hints'),
]