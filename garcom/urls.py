from django.urls import path
from . import views

urlpatterns = [
    path('', views.painel_view, name='painel'),
    path('atender-tarefa/<int:tarefa_id>/', views.realizar_atendimento, name='realizar_atendimento'),
    path('novo-pedido/', views.novo_pedido, name='novo-pedido')
    path('novo-pedido/<slug:mesa_slug>', views.novo_pedido, name='novo-pedido-mesa' )
    path('confirmacao/', views.confirma_pedido, name='confirmacao')
    path('criar_pedido/', views.criar_pedido, name='criar-pedido')
]
