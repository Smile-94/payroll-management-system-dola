from django.urls import path

#views
from authority.views import AdminView

app_name='authority'

urlpatterns = [
    path('authority/', AdminView.as_view(), name='authority')
    
]
