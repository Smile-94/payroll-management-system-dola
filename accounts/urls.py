from django.urls import path


# accounts views
from accounts.views import SignupView
from accounts.views import UserLogout
from accounts.views import UserLoginView

app_name = 'accounts'


urlpatterns = [
    path('', UserLoginView.as_view(), name='login'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('logout/', UserLogout.as_view(), name='logout'),

]
