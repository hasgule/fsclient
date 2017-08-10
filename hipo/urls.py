from django.conf.urls import include, url
import django.contrib
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _
from wheretoeat.views import index

urlpatterns = [
    url(r'', include('wheretoeat.urls', namespace="wheretoeat")),
     url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

