from django.urls import path

from autoapi import views
from autoapi import settings


schema_view = views.get_swagger_view(title='Auto API')

urlpatterns = [
    path('', schema_view),
    path('<app_name>/<model_name>/',
         views.ListCreateAutoView.as_view(), name='list'),
    path('<app_name>/<model_name>/<uuid:pk>/',
         views.RetrieveUpdateDestroyAutoView.as_view(), name='detail'),
]
