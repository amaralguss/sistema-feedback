from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views

urlpatterns = [
    
    path('', views.home, name='home'),
    path('lista_disciplinas/', views.lista_disciplinas, name='lista_disciplinas'),
    path('detalhes_disciplina/<int:id>/', views.detalhes_disciplina, name='detalhes_disciplina'),
    path('avaliar_disciplina/<int:id>/', views.avaliar_disciplina, name='avaliar_disciplina'),
    path('editar_feedback/<int:id>/<int:feedback_id>/', views.editar_feedback, name='editar_feedback'),
    path('registro/', views.registro, name='registro'), 
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/profile/', views.profile, name='profile'), 
]
