
from django.urls import path  
from signup_crud import views  
urlpatterns = [    
    path('', views.users_view),
    path('login/', views.login_view),
    path('create/', views.singup_view),
    path('delete/<int:id>', views.destroy),
    path('edit/<int:id>', views.edit_view),
    path('show/<int:id>', views.show_view),
    path('logout/',views.logout_view),
     
] 