from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from .pucs import views as puc_views
from .users import views as user_views
from .reports import views as report_views
import os

router = DefaultRouter(trailing_slash=False)
router.register(r'users', user_views.UserViewSet)
router.register(r'users', user_views.UserCreateViewSet)

router.register(r'pucs/', puc_views.PucViewSet)
router.register(r'messages/can/', puc_views.CanMessageViewSet)
router.register(r'messages/gps/', puc_views.GpsMessageViewSet)

urlpatterns = [
	# url(r'^$', )
	# path('/', admin.site.urls),
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api-token-auth/', obtain_jwt_token),
    # path('api/v1/', ForgotPasswordFormView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/v1/reports/puc_messages', report_views.PucsMessageReportView.as_view()),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
