from django.contrib import admin
from django.urls import path, include, re_path
from store.views import ReactAppView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from store.views import PasswordResetAPIView, PasswordResetConfirmAPIView

urlpatterns = [
    # ===== ADMIN =====
    path('admin/', admin.site.urls),

    # ===== API ROUTES =====
    path('api/', include('store.urls')),  # categories & products

    # ===== JWT AUTH =====
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ===== PASSWORD RESET =====
    path('api/password-reset/', PasswordResetAPIView.as_view(), name='password_reset'),
    path('api/password-reset-confirm/', PasswordResetConfirmAPIView.as_view(), name='password_reset_confirm'),
]

# ===== MEDIA FILES (for development) =====

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ===== REACT CATCH-ALL (put last!) =====
urlpatterns += [
    re_path(r'^.*$', ReactAppView.as_view()),  # React handles routing
]
