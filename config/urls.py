from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="Inventory API",
        default_version='v1',
        description="API documentation for Inventory management",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    # path("admin/", admin.site.urls),
    path('api/inventory/', include('api.inventory.urls')),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
]
