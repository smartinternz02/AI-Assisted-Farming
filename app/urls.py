from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import views


urlpatterns = [
               path('', views.index, name='index'),
               path('signin',views.signin, name="signin"),
               path('signup',views.signup,name="signup"),
               path('account',views.account,name='account'),
               path('home',views.home,name="home"),
               path('predict',views.predict,name="predict"),
               path('terminal',views.terminal,name="terminal"),
               path('logout',views.logout,name="logout"),
               path('edit',views.edit,name="edit"),
               path('health/', views.health, name='health'),
               path('schema/', SpectacularAPIView.as_view(), name='schema'),
               path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
               path('404', views.handler404, name='404'),
               path('500', views.handler500, name='500'),
               ]