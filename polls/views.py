from django.shortcuts import render
from .serializers import PollSerializer
from tenants.utils import tenant_from_request, set_tenant_schema_for_request
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Poll

# Create your views here.


class PollView(APIView):
    serializer_class = PollSerializer

    def get_queryset(self):
        set_tenant_schema_for_request(self.request)
        tenant = tenant_from_request(self.request)
        return super().get_queryset().filter(tenant=tenant)

    def destroy(self, request, *args, **kwargs):
        set_tenant_schema_for_request(self.request)
        poll = Poll.objects.get(pk=self.kwargs["pk"])
        if not request.user == poll.created_by:
            raise PermissionDenied("You can not delete this poll.")
        return super().destroy(request, *args, **kwargs)

    def get(self, request):
        queryset = Poll.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
