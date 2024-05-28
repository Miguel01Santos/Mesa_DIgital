from django.shortcuts import render, redirect
from .models import Tarefa
from restaurante.models import Mesa, Categorias, ItemCardapio, ItemPedido, Comanda
from django.db.models import Count, Q
from collections import namedtuple




def painel_view(request):
    entregas = Tarefa.objects.filter(tipo='entrega' status='pendente')
    prim_atendimentos = Tarefa.objects.filter(tipo='prim_atendimento' status='pendente')
    atendimentos = Tarefa.objects.filter(tipo='atendimento' status='pendente')
    fechamentos = Tarefa.objects.filter(tipo='fechamento' status='pendente')
    qtdd_atendimentos = prim_atendimentos.count() + atendimentos.count()
    print(prim_atendimentos)
    context = {
        'entregas':entregas,
        'prim_atendimentos':prim_atendimentos,
        'atendimentos':atendimentos,
        'fechamentos':fechamentos,
        'qtdd_atendimentos':qtdd_atendimentos,
    }

    return render(request, 'garcom/home.html', context)

#incluido por Miguel dos Santos
def realizar_atendimento(request, tarefa_id):
    garcom = request.user 
    tarefa = Tarefa.objctes.get(id=tarefa_id) 
    tarefa.atender_tarefa(garcom)
    return redirect('novo-pedido-mesa', mesa_slug=tarefa.mesa.slug)


def novo_pedido(request, mesa_slug=None):
    mesa = None
    if mesa is not None:
        mesa = Mesa.objects.get(slug=mesa_slug)

    categorias = Categoria.objects. \
                annotate(ativos=Count('itemcardapio', \
                                      filter=Q(itemcardapio__ativo=True))). \
                                      filter(ativos__gt=0)
    itens_sem_categoria = ItemCardapio.objects.filter(categoria__isnull=True,
                                                      ativo=True)
    return render(request, 'garcom/cardapio_garcom.html',
                  {'mesa':mesa,
                   'categorias':categorias,
                   'itens_sem_categoria':itens_sem_categoria})
    
def confirma_pedido(request):
    Pedido = namedtuple("Pedido", ['id', 'item', 'quantidade'])
    pedidos = []
    num_mesa = int(request.POST.get(num_mesa))
    mesa = Mesa.objects.get(numero=num_mesa)
    for item_id, quantidade in request.POST.items():
        try:
            id = int(item_id)
        except ValueError:
            pass
        else:
            if int(quantidade) > 0:
                pedidos.append(Pedido(id, ItemCardapio.objects.get(id=id), int(quantidade)))
    return render(request,'garcom/confirmar_pedido.html', {'pedidos':pedidos, 'mesa': mesa})



def criar_pedido(request):
    pedidos_dict = request.POST.copy()
    num_mesa = int(pedidos_dict.get('num_mesa'))
    mesa = Mesa.objects.get(numer=num_mesa)
    comanda = Comanda.objects.get(mesa=mesa, status='aberta')
    del pedidos_dict['num_mesa']
    del pedidos_dict['csrfmiddlewaretoken']
    for item_id, quantidade in pedidos_dict.items():
        item_Cardapio = ItemCardapio.objects.get(id=int(item_id))
        for _ in range(int(quantidade)):
            novo_pedido = ItemPedido(
                item = item_Cardapio,
                preco = float(item_Cardapio.preco),
                comanda = comanda,
                status = 'preparo' if item_Cardapio.necessita_preparo else 'pronto'
            )
            novo_pedido.save()
    comanda.atualiza_total()
    return redirect('painel')


#final da inclusão Miguel dos Santos