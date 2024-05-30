from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from django.views.static import serve

from apps.users.views import Login, LogOut


# Importante
# Antes de llamar las API que quieras, valida primero que el token actual que tienes no se ha vencido, si es asi
# primero actualizalo y despues llama el API

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api_user/", include("apps.users.api.routers")),
    path("api_products/", include("apps.products.api.urls")),
    path("api_products_view/", include("apps.products.api.routers")), # Asi declaras en tus rutas los viewset
    path("login/", Login.as_view(), name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("logout/", LogOut.as_view(), name='logout'),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]