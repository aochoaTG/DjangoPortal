from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

# Vemos a imporimir las rutas a las que se va acceder en la aplicación
urlpatterns = [
    # La ruta / nos debe dirigir al login
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    path('accounts/', include('apps.accounts.urls')),
    path('admin/', admin.site.urls),
    path('suppliers/', include('apps.supplier.urls')),
    path('items/', include('apps.supplier_items.urls')),
    path('logout/', LogoutView.as_view(next_page='/accounts/login/'), name='logout'),

    # Ruta para solicitar el restablecimiento de contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),

    # Ruta para confirmar que el correo ha sido enviado
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),

    # Ruta para ingresar la nueva contraseña
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),

    # Ruta para indicar que la contraseña se ha restablecido correctamente
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    path('notifications/', include('apps.notifications.urls')),
]

# Esto sirve los archivos multimedia durante el desarrollo
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)