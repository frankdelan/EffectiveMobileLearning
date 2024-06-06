"""
URL configuration for dog_classifier project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from dog_app.controllers import DogViewSet, BreedViewSet
from dog_app.views import DogDetailView, DogListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/dogs', DogViewSet.as_view({'get': 'list',
                                         'post': 'create'}), name='dogs'),
    path('api/breeds', BreedViewSet.as_view({'get': 'list',
                                             'post': 'create'}), name='breeds'),
    path('api/dogs/<int:pk>', DogViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('api/breeds/<int:pk>', BreedViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]
