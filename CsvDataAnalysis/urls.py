from django.urls import path
from . import views
urlpatterns=[
    path('<actions>',views.home, name='home'),
    path('<region>/<country>',views.UniversityInRegion, name='UniversityInRegion'),
    path('insert/data/<dataframe>',views.Insert, name='Insert')
]