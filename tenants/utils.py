from .models import Tenant
from django.db import connection


def hostname_from_request(request):
    # split on `:` to remove port
    sub_domain = request.get_host().split(':')[0].lower()
    print(f'subdomain: {sub_domain}')
    return sub_domain


def tenant_from_request(request):
    hostname = hostname_from_request(request)
    subdomain_prefix = hostname.split('.')[0]
    print(f'subdomain_prefix: {subdomain_prefix}')
    return Tenant.objects.filter(subdomain_prefix=subdomain_prefix).first()


# Multitenancy 2
def get_tenants_map():
    # url domain to tenant/schema mapping
    return {
        "signals.localhost": "signals",
        "trail.localhost": "trail",
        "localhost": "public",
    }


def tenant_schema_from_request(request):
    hostname = hostname_from_request(request)
    tenants_map = get_tenants_map()
    return tenants_map.get(hostname)


def set_tenant_schema_for_request(request):
    schema = tenant_schema_from_request(request)
    print('schema', schema)
    with connection.cursor() as cursor:
        cursor.execute(f"SET search_path to {schema}")
