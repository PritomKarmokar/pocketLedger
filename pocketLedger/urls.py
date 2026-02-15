from django.contrib import admin
from django.urls import path, include

service_name = 'pocket-Ledger'

urlpatterns = [
    path(f'{service_name}/admin/', admin.site.urls),
    path(f'{service_name}/accounts/', include('accounts.urls'))
]


# Admin Site
admin.site.site_header = "Pocket Ledger"
admin.site.index_title = "Pocket Ledger"
admin.site.site_title = "Pocket Ledger"