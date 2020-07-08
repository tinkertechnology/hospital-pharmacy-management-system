from django.shortcuts import render
from .serializers import RouteSerializer, RouteDetailSerializer
from .models import Route, RouteDetail
from store.models import Store

from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView,ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from django.http import JsonResponse

#http://localhost:8000/api/route/
class RouteListCreateApiView(ListCreateAPIView):
    serializer_class = RouteSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        title = request.data.get('title', None)
        route_id = request.data.get('route_id', None)
        route_code = request.data.get('routeCode', None)
        fk_store = Store.objects.filter(fk_user_id=request.user.id).first()
        if not fk_store:
            return Response({"Fail": "Couldn't find any Depo associated with your account"}, status.HTTP_400_BAD_REQUEST)
        if not title:
            return Response({"Fail": "Insert title "}, status.HTTP_400_BAD_REQUEST)
        if not route_code:
            return Response({"Fail": "Insert title"}, status.HTTP_400_BAD_REQUEST)
        if route_id:
            route = Route.objects.filter(pk=route_id).first()
        else:
            route = Route()
        route.title = title
        route.code = route_code
        route.fk_store_id = fk_store.id
        route.save()
        return Response({
                        'status': True,
                        'detail': 'Route Added',
                        'fk_route_id': route.id
                        })

    def get_queryset(self, *args, **kwargs):
        routes = ""
        fk_store = Store.objects.filter(fk_user_id=self.request.user.id).first()
        if fk_store:
            routes = Route.objects.filter(fk_store_id=fk_store.id)
        return routes

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


class StoreWiseRouteListApiView(ListAPIView):
    serializer_class = RouteSerializer

    def get_queryset(self, *args, **kwargs):
        store = Store.objects.filter(fk_user_id=self.request.user.id).first()
        print(store)
        storewise_route = Route.objects.filter(fk_store_id=store.id)
        print(storewise_route)

        return storewise_route

    

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def route_detail_view(request):
    if request.method == 'POST':
        rec_json = json.loads(request.body)
        fk_route_id = rec_json['fk_route_id']
        fk_route_details = rec_json['fk_route_details']
        
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
        return JsonResponse({'success':'true'})
    else:
        context={}
        fk_route_id = request.GET.get('fk_route_id')
        context['fk_route_details'] = RouteDetail.objects.filter(fk_route_id=fk_route_id)
        return render(request, 'route_detail_view.html', context)
