from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'app'

urlpatterns = [
    
    path('', views.home),
    # path('accounts/login/', views.login),
    # path('accounts/cadastro/', views.cadastro),
    # path('painel/comercial/', views.comercial),
    # path('painel/financeiro/', views.financeiro),
    # path('painel/estoque/', views.estoque),


    path('total_vendas/', views.total_vendas),                                                                                  ##utilizado
    path('total_vendas_mensal/', views.total_vendas_mensal),                                                                    ##utilizado
    path('meta_de_vendas/', views.meta_de_vendas),                                                                              ##utilizado
    path('total_vendas_mensal/', views.total_vendas_mensal),                                                                    ##utilizado
    path('total_de_vendas_por_vendedor/', views.total_de_vendas_por_vendedor),                                                  ##utilizado
    path('lucro_bruto_mensal/', views.lucro_bruto_mensal),                                                                      ##utilizado
    path('total_lucro_bruto/', views.total_lucro_bruto),
    path('total_cmv/', views.total_cmv),                                                                                        ##utilizado
    path('total_cmv_mensal/', views.total_cmv_mensal),
    path('agrupamentos/', views.agrupamentos),                                                                                  ##utilizado
    path('vendas_por_agrupamento_mensal/', views.vendas_por_agrupamento_mensal),                                                ##utilizado
    path('ranking_de_vendas_por_cliente/', views.ranking_de_vendas_por_cliente),                                                ##utilizado
    path('ranking_de_vendas_por_produto/', views.ranking_de_vendas_por_produto),                                                ##utilizado


    path('total_de_recebimentos_por_forma_mensal/resumo_geral/', views.total_de_recebimentos_por_forma_mensal_resumo_geral),    ##utilizado
    path('contas_a_receber_a_partir_da_data_atual/', views.contas_a_receber_a_partir_da_data_atual),                            ##utilizado
    path('contas_a_pagar_a_partir_da_data_atual/', views.contas_a_pagar_a_partir_da_data_atual),                                ##utilizado
    path('contas_a_receber_do_inicio_ate_a_data_atual/', views.contas_a_receber_do_inicio_ate_a_data_atual),                    ##utilizado
    path('contas_a_pagar_do_inicio_ate_a_data_atual/', views.contas_a_pagar_do_inicio_ate_a_data_atual),                        ##utilizado
    path('contas_a_pagar_por_ranking_e_dia/', views.contas_a_pagar_por_ranking_e_dia),                                          ##utilizado
    path('contas_a_receber_por_ranking_e_dia/', views.contas_a_receber_por_ranking_e_dia),                                        ##utilizado
    path('detalhes_finaciamento/', views.detalhes_finaciamento),                                                                ##utilizado
    path('saldo_disponivel_em_contas/', views.saldo_disponivel_em_contas),                                                      ##utilizado
    path('fluxo_de_caixa/', views.fluxo_de_caixa),                                                                              ##utilizado

    
    path('mapa_de_locacoes/', views.mapa_de_locacoes),
    path('cilindros_em_condicionais/', views.cilindros_em_condicionais),
    path('ticket_medio_de_compra/', views.ticket_medio_de_compra),                                                              ##utilizado                                                 
    path('qtd_cilindros_cheios/', views.qtd_cilindros_cheios),
    path('qtd_produtos_em_estoque/', views.qtd_produtos_em_estoque),
    path('ranking_compras_por_fornecedor/', views.rankingComprasPorFornecedor),                                                 ##utilizado
    path('ranking_produto_mais_comprado/', views.ranking_produto_mais_comprado),                                                ##utilizado                                              
    path('total_de_valores_de_todos_os_produtos/', views.total_de_valores_de_todos_os_produtos),
    

    path('notas_nao_emitidas/', views.notas_nao_emitidas),
]