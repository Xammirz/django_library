from django.urls import path

from django.urls.conf import include

from .views import SignUpView
 
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    
]