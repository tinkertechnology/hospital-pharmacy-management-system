from django.shortcuts import render
from .serializers import RouteSerializer, RouteDetailSerializer
from .models import Route, RouteDetail

from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView,ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
import json
from django.http import JsonResponse

#http://localhost:8000/api/route/
class RouteListCreateApiView(ListCreateAPIView):
    serializer_class = RouteSerializer

    def get_queryset(self, *args, **kwargs):
        return Route.objects.all()

#http://localhost:8000/api/route/<pk>/
#
class RouteRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = RouteSerializer
    def get_queryset(self, *args, **kwargs):
        return Route.objects.all()

# http://localhost:8000/api/routedetail/
class RouteDetailListCreateApiView(ListCreateAPIView):
    serializer_class = RouteDetailSerializer

    def get_queryset(self, *args, **kwargs):
        return RouteDetail.objects.all()

# http://localhost:8000/api/routedetail/<pk>/
#
class RouteDetailRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = RouteDetailSerializer
    def get_queryset(self, *args, **kwargs):
        return RouteDetail.objects.all()

from django.views.decorators.csrf import csrf_exempt

# http://localhost:8000/route_detail_view?fk_route_id=2
@csrf_exempt
def route_detail_view(request):
    if request.method == 'POST':
        rec_json = json.loads(request.body)
        fk_route_id = rec_json['fk_route_id']
        fk_route_details = rec_json['fk_route_details']
        
        remain_undel_ids = [];
        for d in fk_route_details:
            print(fk_route_id, d['order_latitude'], d['order_longitude'], d['fk_route_detail_id'])

            fk_route_detail = None
            
            id = d['fk_route_detail_id']
            if id:
                fk_route_detail = RouteDetail.objects.filter(pk=id).first()
            else:
                fk_route_detail =  RouteDetail()
            fk_route_detail.order_latitude = d['order_latitude']
            fk_route_detail.order_longitude = d['order_longitude']
            fk_route_detail.fk_route_id = fk_route_id
            fk_route_detail.save()

            remain_undel_ids.append(fk_route_detail.id) #natra new id , create / delete huncha

        # delete ids which are not sent by form/web page
        RouteDetail.objects.filter(fk_route_id=fk_route_id).exclude(id__in=remain_undel_ids).delete()

        return JsonResponse({'success':'true'})
    else:
        context={}
        fk_route_id = request.GET.get('fk_route_id')
        context['fk_route_details'] = RouteDetail.objects.filter(fk_route_id=fk_route_id)
        return render(request, 'route_detail_view.html', context)