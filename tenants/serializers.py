from rest_framework import serializers
from tenants.models import Tenant


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ('id', 'name')
