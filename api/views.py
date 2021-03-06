from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route


from .models import Talk
from .serializers import TalkSerializer
from .permissions import IsSuperUserOrReadOnly


class TalkViewSet(viewsets.ModelViewSet):
    queryset = Talk.objects.all()
    serializer_class = TalkSerializer #!!
    permission_classes = (IsSuperUserOrReadOnly,)

    @list_route(methods=['get'] )
    def best_topics(self, request):
        talks = Talk.objects.order_by('-votes')[:3]
        serialized_talk = TalkSerializer(talks, many=True)
        return Response(serialized_talk.data)    

    @detail_route(methods=['get', 'put'], )
    def vote(self, request, pk=None):
        talk = self.get_object()
        if request.method == 'PUT':
            talk.votes += 1
            talk.save()
        serialized_talk = TalkSerializer(talk)
        return Response(serialized_talk.data)