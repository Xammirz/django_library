from django.urls import path
<<<<<<< HEAD
from django.urls.conf import include
=======
>>>>>>> b07154f3fcca8999a4ce3efc70d5d1edd3bd6b22

from .views import SignUpView
 
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    
]