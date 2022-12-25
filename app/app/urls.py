"""
path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    # user app url
    path('api/user/', include('user.urls')),
    # recipe app url
    # path('api/recipe/', include('recipe.urls')),

    # drf_spectacular urls

    # generates the schema: YAML file
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # swagger doc to generate documentation
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='api-docs'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='api-redoc'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
