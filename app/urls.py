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
               ]