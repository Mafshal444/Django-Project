from http.client import HTTPResponse
import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .PerFormTask import UniversityWithNoCity, GetUniversityByRegion, InsertData, GetData, TopTenCountries

# Create your views here.
def home(request, actions):
    if request.method == 'GET':
        if actions == 'nocity':
            data = UniversityWithNoCity()
            value = data.to_json().replace("\/","")
            return HttpResponse(value, content_type = 'application/json')
        elif actions == 'all':
            data = GetData(actions)
            return JsonResponse({"data":data})
        elif actions == 'Top 10':
            data = TopTenCountries()
            print(type(data))
            return JsonResponse({'data':data})
        else:
            data = GetData(actions)
            return JsonResponse({"data":data})

def UniversityInRegion(request, region, country):
    if request.method == 'GET':
        # data = json.loads(request.body.decode('utf-8'))
        # region  = data.get('region')
        # country  = data.get('country')
        result = GetUniversityByRegion(region, country)
        # my_json = result.replace('\\','')
        # print(type(my_json))
        return JsonResponse({"result": result})
    else:
        return JsonResponse({'res':"Please Send a Get Request"})


def Insert(request, dataframe):
    if request.method == 'GET':
        InsertData(dataframe)
        # data  = GetData()
        # for student in data:
        #     print(student.data)
        return JsonResponse({'res':'data uploaded'})