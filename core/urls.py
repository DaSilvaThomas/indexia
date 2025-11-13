from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from apps.views import home_view, login_view, logout_view, upload_view, delete_file_view, delete_all_files_view, document_view, download_view, statistic_view, cloud_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view, name='home'),
    path("connexion/", login_view, name="login"),
    path("déconnexion/", logout_view, name="logout"),
    path("importer/", upload_view, name='upload'),
    path('supprimer/<int:pk>/', delete_file_view, name='delete_file'),
    path('supprimer/', delete_all_files_view, name='delete_all_files'),
    path("documents/", document_view, name='document'),
    path("téléchargement/<int:pk>/", download_view, name='download'),
    path("statistiques/", statistic_view, name='statistic'),
    path("nuage/<int:pk>/", cloud_view, name='cloud'),
]

# Fichiers media en mode développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
