from rest_framework import serializers
from .models import Poll
from tenants.serializers import TenantSerializer


class PollSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(many=False)

    class Meta:
        model = Poll
        fields = ('__all__')
