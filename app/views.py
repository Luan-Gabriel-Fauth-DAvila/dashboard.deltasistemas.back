from distutils.log import error
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import auth
from django.contrib.auth.models import User
import fdb
import json

def conn():
    conn = fdb.connect(
        host='45.232.214.65',
        database='/Ultra/Banco/gestao.fdb',
        user='SYSDBA',
        password='masterkey',
        port=58002,
        charset='UNICODE_FSS'
    )
    return conn

def home(request):
    return redirect('/accounts/login/?next=/painel/comercial/')
    # return render(request, 'home.html')

@csrf_exempt
def login(request):
    try:
        next = request.POST['next']
    except MultiValueDictKeyError:
        next = ''
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        usuario = auth.authenticate(request, username=username, password=password)
        if usuario is not None:
            auth.login(request, usuario)
            if next:
                return redirect(next)
            else:
                return redirect('/painel/comercial/')
        else:
            form_login = AuthenticationForm()
            return render(request, 'accounts/login.html', {'form_login': form_login, 'next': next})
    else:
        form_login = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form_login': form_login, 'next': next})

@csrf_exempt
@login_required
def cadastro(request):
    if request.method == "POST":
        form_usuario = UserCreationForm(request.POST)
        if form_usuario.is_valid():
            form_usuario.save()
            return redirect('/accounts/login/')
    else:
        form_usuario = UserCreationForm()
    return render(request, 'accounts/cadastro.html', {'form_usuario': form_usuario})

@login_required
def comercial(request):
    
    
    return render(request, 'app/comercial.html', {'page': 1})

@login_required
def financeiro(request):
    

    return render(request, 'app/financeiro.html', {'page': 2})

@login_required
def estoque(request):
    

    return render(request, 'app/estoque.html', {'page': 3})




def filters(request):
    try:
        if request.GET['data_ini'] == 'null' or request.GET['data_fim'] == 'null' or request.GET['data_ini'] == 'undefined.undefined.' or request.GET['data_fim'] == 'undefined.undefined.':
            raise MultiValueDictKeyError
        else:
            data_filter = "dtacomp between '" + request.GET['data_ini'] + "' and '" + request.GET['data_fim'] + "'"
    except MultiValueDictKeyError:
        data_filter = '''
        extract(month from v.dtacomp) = extract(month from current_date) and
        extract(year from dtacomp) = extract(year from current_date)'''
    
    return data_filter

def total_vendas(request):
    con = conn()
    cur = con.cursor()
    cur.execute("""
        select 
            sum(total_venda) as total_vendas

        from (select
            venda_id,tipo_nd,
            dtacomp,valor,
            acrescimo,
            desconto,
            total,
            +(+qtd),
            +(+total_venda),
            OBS

        from vendas v

        where
            codfilial = '1' AND
            IDN_CANCELADA = 'N' AND
            TIPO_ND = 'N' and
            """ + filters(request) + """

        union all
        
        select
            venda_id,
            tipo_nd,
            dtacomp,
            valor,
            acrescimo,
            desconto,
            total,
            +(-qtd),
            +(-total_venda),
            OBS

        from vendas v

        where
            codfilial = '1' AND
            IDN_CANCELADA = 'N' AND
            TIPO_ND = 'D' and
            """ + filters(request) + """)""")
    
    for c in cur.fetchall():
        d = {
        'total_vendas': str(c[0])
        }
    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})

# def total_vendas_mensal(request):
#     con = conn()
#     cur = con.cursor()
#     cur.execute("""
#         select 
#             sum(v.total_venda)

#         from vendas as v

#         where 
#             v.dtacomp between '01.03.2020' and '01.04.2022'
#     """)
    
#     for c in cur.fetchall():
#         d = {
#         'total_vendas_mensal': str(c[0]),
#         }
#     con.close()
#     return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})

def total_vendas_mensal(request):
    try:
        if request.GET['data_ini'] == 'null' or request.GET['data_fim'] == 'null' or request.GET['data_ini'] == 'undefined.undefined.' or request.GET['data_fim'] == 'undefined.undefined.':
            raise MultiValueDictKeyError
        else:
            data_filter = "dtacomp between '" + request.GET['data_ini'] + "' and '" + request.GET['data_fim'] + "'"
    except MultiValueDictKeyError:
        data_filter = 'extract(year from dtacomp) = extract(year from current_date)'

    con = conn()
    cur = con.cursor()
    cur.execute("""
    SELECT first 12
        count (Venda_ID) qtd_vendas,
        sum (QTD) qtd_itens,
        sum(total_venda) total_vendas,
        extract(month from dtacomp) mes,
        (case extract(month from dtacomp)
            when 1  then 'Janeiro'
            when 2  then 'Fevereiro'
            when 3  then 'Março'
            when 4  then 'Abril'
            when 5  then 'Maio'
            when 6  then 'Junho'
            when 7  then 'Julho'
            when 8  then 'Agosto'
            when 9  then 'Setembro'
            when 10  then 'Outubro'
            when 11  then 'Novembro'
            when 12  then 'Dezembro'
        end) as dscmes,
        extract(year from dtacomp) ano

    from

        (select
            venda_id,tipo_nd,
            dtacomp,valor,
            acrescimo,
            desconto,
            total,
            +(+qtd),
            +(+total_venda),
            OBS

        from vendas

        where
            codfilial = '1' AND
            IDN_CANCELADA = 'N' AND
            TIPO_ND = 'N' and
            """ + data_filter + """

        union all
        
        select
            venda_id,
            tipo_nd,
            dtacomp,
            valor,
            acrescimo,
            desconto,
            total,
            +(-qtd),
            +(-total_venda),
            OBS

        from vendas

        where
            codfilial = '1' AND
            IDN_CANCELADA = 'N' AND
            TIPO_ND = 'D' and
            """ + data_filter + """)

    group by
        extract(month from dtacomp),
        extract(year from dtacomp)

    order by ano, mes
        """)
    d = {
        'qtd_vendas': [],
        'qtd_itens': [],
        'total_vendas': [],
        'mes': [],
        'dscmes': [],
        'ano': [],
    }
    for c in cur.fetchall():
        d['qtd_vendas'].append(str(c[0]))
        d['qtd_itens'].append(str(c[1]))
        d['total_vendas'].append(float(c[2]))
        d['mes'].append(str(c[3]))
        d['dscmes'].append(str(c[4]))
        d['ano'].append(str(c[5]))

    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})

def total_de_valores_de_todos_os_produtos(request):
    con = conn()
    cur = con.cursor()
    cur.execute("""
    SELECT
        SUM(VI.TOTAL) AS VALOR_TOTAL,
        SUM(VI.QTD) AS QUANTIDADE

    FROM VENDAS_ITENS VI
        INNER JOIN VENDAS V ON V.VENDA_ID = VI.VENDA_ID
        INNER JOIN PRODUTOS AS P ON P.CODPRODUTO = VI.CODPRODUTO

    WHERE V.IDN_CANCELADA = 'N'
    """)
    
    for c in cur.fetchall():
        d = {
        'valor_total': str(c[0]),
        'quantidade': str(c[1])
        }
    
    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})

def ranking_produto_mais_comprado(request):
    con = conn()
    cur = con.cursor()
    cur.execute("""
    SELECT FIRST 10
        CI.PRODUTO,
        P.DSCPRODUTO, 
        CI.QUANTIDADE

    FROM COMPRAS_ITEM CI
        INNER JOIN COMPRAS AS C ON C.COMPRA_ID = CI.COMPRA_ID
        INNER JOIN PRODUTOS AS P ON P.CODPRODUTO = CI.PRODUTO

    WHERE 
        C.IDN_CANCELADA = 'N' AND
        C.DATA_ENTRADA BETWEEN CURRENT_DATE -30 AND CURRENT_DATE

    ORDER BY CI.QUANTIDADE DESC
    """)
    d = {
    'produto': [],
    'dscproduto': [],
    'quantidade': [],
    }
    for c in cur.fetchall():
        d['produto'].append(c[0])
        d['dscproduto'].append(c[1])
        d['quantidade'].append(str(c[2]))

    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})

def total_de_recebimentos_por_forma_mensal_resumo_geral(request):
    con = conn()
    cur = con.cursor()
    cur.execute("""
    SELECT
        SUM(TOTAL_CARTAO) as REC_CARTAO,
        (SUM(VALOR) - SUM(TOTAL_CHEQTERC_ENT) - SUM(TOTAL_DEBITOS_BANCARIOS) - SUM(TOTAL_CARTAO)) as REC_DINHEIRO,
        SUM(VALOR) as RECEBIMENTOS,
        SUM(TOTAL_CHEQTERC_ENT) as CHEQUES_RECEBIDOS,  
        SUM(TOTAL_DEBITOS_BANCARIOS) as ENTRADAS_BANCOS
                                                                                                        
    FROM CAIXA_MOVTO 

    where
        extract(month from data) = extract(month from current_date)
    """)
    for c in cur.fetchall():
        d = {
        'rec_cartao': str(c[0]),
        'rec_dinheiro': str(c[1]),
        'recebimentos': str(c[2]),
        'cheques_recebidos': str(c[3]),
        'entradas_bancos': str(c[4]),
        }

    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})
    
def contas_a_receber_a_partir_da_data_atual(request):
    con = conn()
    cur = con.cursor()
    cur.execute("""
    SELECT 
        SUM(SALDO) 

    FROM FATURAS_RECEBER_PARCELAS  
    """)
    for c in cur.fetchall():
        d = {
        'faturas_receber': str(c[0]),
        }

    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})
    
def contas_a_pagar_a_partir_da_data_atual(request):
    con = conn()
    cur = con.cursor()
    cur.execute("""
    SELECT
        SUM(SALDO)

    FROM FATURAS_PAGAR_PARCELAS  
    """)
    for c in cur.fetchall():
        d = {
        'faturas_pagar': str(c[0]),
        }

    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})

def contas_a_receber_do_inicio_ate_a_data_atual(request):
    con = conn()
    cur = con.cursor()
    cur.execute("""
    SELECT
        SUM(SALDO)

    FROM FATURAS_RECEBER_PARCELAS

    WHERE
        DATA_VENCIMENTO  BETWEEN '01.01.1900' AND '19.04.2022'  
    """)
    for c in cur.fetchall():
        d = {
        'faturas_receber': str(c[0]),
        }

    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})

def contas_a_pagar_do_inicio_ate_a_data_atual(request):
    con = conn()
    cur = con.cursor()
    cur.execute("""
    SELECT
        SUM(SALDO)

    FROM FATURAS_PAGAR_PARCELAS

    WHERE
        DATA_VENCIMENTO  BETWEEN '01.01.1900' AND '19.04.2022'  
    """)
    for c in cur.fetchall():
        d = {
        'faturas_pagar': str(c[0]),
        }

    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})

def total_de_vendas_por_vendedor(request):
    try:
        if request.GET['data_ini'] == 'null' or request.GET['data_fim'] == 'null' or request.GET['data_ini'] == 'undefined.undefined.' or request.GET['data_fim'] == 'undefined.undefined.':
            raise MultiValueDictKeyError
        else:
            data_filter = "v.dtacomp between '" + request.GET['data_ini'] + "' and '" + request.GET['data_fim'] + "'"
    except MultiValueDictKeyError:
        data_filter = '''
        extract(month from v.dtacomp) = extract(month from current_date) and
        extract(year from v.dtacomp) = extract(year from current_date)'''

    con = conn()
    cur = con.cursor()
    cur.execute("""
    SELECT first 5
        sum(V.VALOR), 
        V.VENDEDOR, 
        PC.NOME 
        
    FROM VENDAS V
        LEFT JOIN PARCEIROS AS PC ON V.VENDEDOR = PC.PARCEIRO

    WHERE 
        V.IDN_CANCELADA = 'N' AND 
        """ + data_filter + """

    group by v.vendedor, pc.nome

    ORDER BY sum(V.VALOR) DESC 
    """)
    d = {
        'valor': [],
        'codvendedor': [],
        'nome': [],
    }
    for c in cur.fetchall():
        d['valor'].append(float(c[0]))
        d['codvendedor'].append(str(c[1]))
        d['nome'].append(str(c[2]))
    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})

def meta_de_vendas(request):
    con = conn()
    cur = con.cursor()
    cur.execute("""
    SELECT DISTINCT
        MV.META_ID,
        MV.CODFILIAL,
        MV.MES,
        MV.ANO,
        MV.VENDEDOR,
        P.NOME,
        MV.VALOR,
        MV.QTD,
        SUM(V.TOTAL) AS TOTAL_VENDIDO


    FROM METAS_VENDAS MV
        INNER JOIN VENDAS AS V ON V.VENDEDOR = MV.VENDEDOR
        INNER JOIN PARCEIROS AS P ON P.PARCEIRO = MV.VENDEDOR

    WHERE
        V.IDN_CANCELADA = 'N' AND

    EXTRACT (MONTH FROM V.DTACOMP) = EXTRACT(MONTH FROM DATE 'TODAY') AND
    EXTRACT (YEAR FROM V.DTACOMP) = EXTRACT (YEAR FROM DATE 'TODAY')

    GROUP BY 1,2,3,4,5,6,7,8
    """)
    d = {
        'meta_id': [],
        'codfilial': [],
        'mes': [],
        'ano': [],
        'vendedor': [],
        'nome': [],
        'valor': [],
        'qtd': [],
        'total_vendido': [],
    }
    for c in cur.fetchall():
        d['meta_id'].append(str(c[0]))
        d['codfilial'].append(str(c[1]))
        d['mes'].append(str(c[2]))
        d['ano'].append(str(c[3]))
        d['vendedor'].append(str(c[4]))
        d['nome'].append(str(c[5]))
        d['valor'].append(str(c[6]))
        d['qtd'].append(str(c[7]))
        d['total_vendido'].append(str(c[8]))

    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})

def mapa_de_locacoes(request):
    con = conn()
    cur = con.cursor()
    cur.execute("""
    SELECT
        C.NUMCONDICIONAL,
        P.PARCEIRO,
        P.NOME,
        'ENDERECO: ' || COALESCE(P.ENDERECO,'') || ' , '
        || 'Nº ' || COALESCE(P.NUMERO,'')  || ' - '
        || 'BAIRRO ' || COALESCE(P.BAIRRO,'')  || ' , '
        || 'MUNICIPIO ' || COALESCE(P.MUNICIPIO,'')  || ' / '
        || 'CEP ' || COALESCE(P.CEP,'')  || ' - '
        || 'UF ' || COALESCE(P.UF,'')
        AS LOCALIZACAO,

        C.CODPRODUTO,
        PR.DSCPRODUTO,
        C.CODPRODUTO_CLAS,
        C.QTD AS QTD_LOCADA,
        C.QTD_SALDO AS QTD_PENDENTE

    FROM CONDICIONAIS C
        INNER JOIN PARCEIROS AS P ON P.PARCEIRO = C.PARCEIRO
        INNER JOIN PRODUTOS AS PR ON PR.CODPRODUTO = C.CODPRODUTO

    WHERE C.QTD_SALDO > 0
    """)
    d = {
        'numcondicional': [],
        'parceiro': [],
        'nome': [],
        'localizacao': [],
        'codproduto': [],
        'dscproduto': [],
        'codproduto_clas': [],
        'qtd_locada': [],
        'qtd_pendente': [],
    }
    for c in cur.fetchall():
        d['numcondicional'].append(str(c[0]))
        d['parceiro'].append(str(c[1]))
        d['nome'].append(str(c[2]))
        d['localizacao'].append(str(c[3]))
        d['codproduto'].append(str(c[4]))
        d['dscproduto'].append(str(c[5]))
        d['codproduto_clas'].append(str(c[6]))
        d['qtd_locada'].append(str(c[7]))
        d['qtd_pendente'].append(str(c[8]))

    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})

def total_cmv(request):
    try:
        if request.GET['data_ini'] == 'null' or request.GET['data_fim'] == 'null' or request.GET['data_ini'] == 'undefined.undefined.' or request.GET['data_fim'] == 'undefined.undefined.':
            raise MultiValueDictKeyError
        else:
            data_filter = "v.dtacomp between '" + request.GET['data_ini'] + "' and '" + request.GET['data_fim'] + "'"
    except MultiValueDictKeyError:
        data_filter = '''
        extract(month from v.dtacomp) = extract(month from current_date) and
        extract(year from v.dtacomp) = extract(year from current_date)'''

    con = conn()
    cur = con.cursor()
    cur.execute("""
    SELECT
        SUM(VI.CMV_TOTAL) AS CMV_TOTAL

    FROM VENDAS_ITENS VI
        INNER JOIN VENDAS AS V ON V.VENDA_ID = VI.VENDA_ID

    WHERE
        V.IDN_CANCELADA = 'N' AND
        V.CODOPER IN (111,107,112,113) and 
        """ + data_filter)
    for c in cur.fetchall():
        d = {
            'total_cmv': str(c[0]),
        }

    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})

def total_cmv_mensal(request):
    con = conn()
    cur = con.cursor()
    cur.execute("""
    SELECT
        SUM(VI.CMV_TOTAL) AS CMV_TOTAL

    FROM VENDAS_ITENS VI
        INNER JOIN VENDAS AS V ON V.VENDA_ID = VI.VENDA_ID

    WHERE
        V.IDN_CANCELADA = 'N' AND
        V.CODOPER IN (111,107,112,113) AND
        EXTRACT (MONTH FROM V.DTACOMP) = EXTRACT(MONTH FROM DATE 'TODAY') AND
        EXTRACT (YEAR FROM V.DTACOMP) = EXTRACT (YEAR FROM DATE 'TODAY')
    """)
    for c in cur.fetchall():
        d = {
            'total_cmv_mensal': str(c[0]),
        }

    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})

def cilindros_em_condicionais(request):
    con = conn()
    cur = con.cursor()
    cur.execute("""
    SELECT DISTINCT
        C.NUMCONDICIONAL,
        P.PARCEIRO,
        P.NOME,
        C.CODPRODUTO,
        PR.DSCPRODUTO,
        C.CODPRODUTO_CLAS,
        SUM(C.QTD) AS QTD_LOCADA,
        SUM(C.QTD_DEV) AS QTD_DEVOLVIDA,
        SUM(C.QTD_SALDO) AS QTD_PENDENTE

    FROM CONDICIONAIS C
        INNER JOIN PARCEIROS AS P ON P.PARCEIRO = C.PARCEIRO
        INNER JOIN PRODUTOS AS PR ON PR.CODPRODUTO = C.CODPRODUTO

    WHERE C.QTD_SALDO > 0

    GROUP BY 1,2,3,4,5,6
    """)
    d = {
        'numcondicional': [],
        'parceiro': [],
        'nome': [],
        'codproduto': [],
        'dscproduto': [],
        'codproduto_clas': [],
        'qtd_locada': [],
        'qtd_devolvida': [],
        'qtd_pendente': [],
    }
    for c in cur.fetchall():
        d['numcondicional'].append(str(c[0]))
        d['parceiro'].append(str(c[1]))
        d['nome'].append(str(c[2]))
        d['codproduto'].append(str(c[3]))
        d['dscproduto'].append(str(c[4]))
        d['codproduto_clas'].append(str(c[5]))
        d['qtd_locada'].append(str(c[6]))
        d['qtd_devolvida'].append(str(c[7]))
        d['qtd_pendente'].append(str(c[8]))

    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})

def qtd_cilindros_cheios(request):
    con = conn()
    cur = con.cursor()
    cur.execute("""
    SELECT
        ESA.CODPRODUTO,
        P.DSCPRODUTO,
        ESA.CODPRODUTO_CLAS,
        ESA.QTD

    FROM ESTOQUE_SALDO_ATUAL ESA
        INNER JOIN PRODUTOS AS P ON P.CODPRODUTO = ESA.CODPRODUTO
        INNER JOIN AGRUPAMENTOS AS A ON A.CODGRUPO = P.CODGRUPO

    WHERE
        CODPRODUTO_CLAS = 1 AND
        ESA.QTD >= 1 AND
        A.CODGRUPO_MESTRE = 1
    """)
    d = {
        'codproduto': [],
        'dscproduto': [],
        'codproduto_clas': [],
        'qtd': [],
    }
    for c in cur.fetchall():
        d['codproduto'].append(str(c[0]))
        d['dscproduto'].append(str(c[1]))
        d['codproduto_clas'].append(str(c[2]))
        d['qtd'].append(str(c[3]))

    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})

def qtd_produtos_em_estoque(request):
    con = conn()
    cur = con.cursor()
    cur.execute("""
    SELECT
        ESA.CODPRODUTO,
        P.DSCPRODUTO,
        ESA.CODPRODUTO_CLAS,
        ESA.QTD

    FROM ESTOQUE_SALDO_ATUAL ESA
        INNER JOIN PRODUTOS AS P ON P.CODPRODUTO = ESA.CODPRODUTO
        INNER JOIN AGRUPAMENTOS AS A ON A.CODGRUPO = P.CODGRUPO

    WHERE CODPRODUTO_CLAS = 1

    ORDER BY ESA.CODPRODUTO ASC
    """)
    d = {
        'codproduto': [],
        'dscproduto': [],
        'codproduto_clas': [],
        'qtd': [],
    }
    for c in cur.fetchall():
        d['codproduto'].append(str(c[0]))
        d['dscproduto'].append(str(c[1]))
        d['codproduto_clas'].append(str(c[2]))
        d['qtd'].append(str(c[3]))

    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})

def lucro_bruto_mensal(request):
    try:
        if request.GET['data_ini'] == 'null' or request.GET['data_fim'] == 'null' or request.GET['data_ini'] == 'undefined.undefined.' or request.GET['data_fim'] == 'undefined.undefined.':
            raise MultiValueDictKeyError
        else:
            data_filter = "v.dtacomp between '" + request.GET['data_ini'] + "' and '" + request.GET['data_fim'] + "'"
    except MultiValueDictKeyError:
        data_filter = '''
        extract(month from v.dtacomp) = extract(month from current_date) and
        extract(year from v.dtacomp) = extract(year from current_date)'''

    con = conn()
    cur = con.cursor()
    cur.execute("""
    SELECT
        SUM(+(+VALOR)) AS VALOR_TOTAL,
        SUM(ACRESCIMO) AS ACRESCIMO,
        SUM(DESCONTO) AS DESCONTO,
        SUM(+(+TOTAL)) AS TOTAL_FINAL

    FROM VENDAS V

    WHERE
        IDN_CANCELADA = 'N' AND
        CODOPER IN (111,107,112,113) AND
        """ + data_filter)
    #UNION ALL

    # SELECT
    #     SUM(+(-VALOR)) AS VALOR_TOTAL,
    #     SUM(ACRESCIMO) AS ACRESCIMO,
    #     SUM(DESCONTO) AS DESCONTO,
    #     SUM(+(-TOTAL)) AS TOTAL_FINAL

    # FROM VENDAS

    # WHERE
    #     CODOPER = 150 AND
    #     IDN_CANCELADA = 'N' AND
    #     EXTRACT (MONTH FROM DTACOMP) = EXTRACT(MONTH FROM DATE 'TODAY') AND
    #     EXTRACT (YEAR FROM DTACOMP) = EXTRACT (YEAR FROM DATE 'TODAY')
    d = {
        'valor_total': [],
        'acrescimo': [],
        'desconto': [],
        'total_final': [],
    }
    for c in cur.fetchall():
        d['valor_total'].append(str(c[0]))
        d['acrescimo'].append(str(c[1]))
        d['desconto'].append(str(c[2]))
        d['total_final'].append(str(c[3]))

    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})

def total_lucro_bruto(request):
    

    con = conn()
    cur = con.cursor()
    cur.execute("""
    SELECT
        SUM(+(+VALOR)) AS VALOR_TOTAL,
        SUM(ACRESCIMO) AS ACRESCIMO,
        SUM(DESCONTO) AS DESCONTO,
        SUM(+(+TOTAL)) AS TOTAL_FINAL

    FROM VENDAS V

    WHERE
        V.IDN_CANCELADA = 'N' AND
        V.CODOPER IN (111,107,112,113) and
        """ + filters())
    d = {
        'valor_total': [],
        'acrescimo': [],
        'desconto': [],
        'total_final': [],
    }
    for c in cur.fetchall():
        d['valor_total'].append(str(c[0]))
        d['acrescimo'].append(str(c[1]))
        d['desconto'].append(str(c[2]))
        d['total_final'].append(str(c[3]))

    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})

def vendas_por_agrupamento_mensal(request):
    try:
        if request.GET['data_ini'] == 'null' or request.GET['data_fim'] == 'null' or request.GET['data_ini'] == 'undefined.undefined.' or request.GET['data_fim'] == 'undefined.undefined.':
            raise MultiValueDictKeyError
        else:
            data_filter = "v.dtacomp between '" + request.GET['data_ini'] + "' and '" + request.GET['data_fim'] + "'"
    except MultiValueDictKeyError:
        data_filter = '''
        extract(month from v.dtacomp) = extract(month from current_date) and
        extract(year from v.dtacomp) = extract(year from current_date)
        '''
    
    con = conn()
    cur = con.cursor()
    cur.execute("""
    select
        sum(vi.total_venda) as total_vendas,
        ag.dscagrupamento

    from vendas_itens vi
        inner join vendas v on (vi.venda_id = v.venda_id)
        inner join produtos as p on (vi.codproduto = p.codproduto)
        inner join agrupamentos as ag on (p.codgrupo = ag.codgrupo)

    where
        """ + data_filter + """ and
        item_devolucao is null

    group by 2
    order by 1 
        """)
    d = {
        'total_vendas': [],
        'dscagrupamento': []
    }
    for c in cur.fetchall():
        d['total_vendas'].append(float(c[0]))
        d['dscagrupamento'].append(str(c[1]))
    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})

def ranking_de_vendas_por_cliente(request):
    try:
        if request.GET['data_ini'] == 'null' or request.GET['data_fim'] == 'null' or request.GET['data_ini'] == 'undefined.undefined.' or request.GET['data_fim'] == 'undefined.undefined.':
            raise MultiValueDictKeyError
        else:
            data_filter = "v.dtacomp between '" + request.GET['data_ini'] + "' and '" + request.GET['data_fim'] + "'"
    except MultiValueDictKeyError:
        data_filter = '''
        extract(month from v.dtacomp) = extract(month from current_date) and
        extract(year from v.dtacomp) = extract(year from current_date)'''

    con = conn()
    cur = con.cursor()
    cur.execute("""
    select first 7
        v.parceiro as codcliente,
        p.nome as nome,
        sum(v.total) as total_vendas

    from vendas as v
        inner join parceiros as p on v.parceiro = p.parceiro

    where
        """ + data_filter + """
    group by 1,2
    order by 3 desc
        """)

    d = {
        'codcliente': [],
        'nome': [],
        'total_vendas': [],
    }
    for c in cur.fetchall():
        d['codcliente'].append(float(c[0]))
        d['nome'].append(str(c[1]))
        d['total_vendas'].append(float(c[2]))
    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})

def ranking_de_vendas_por_produto(request):
    try:
        if request.GET['data_ini'] == 'null' or request.GET['data_fim'] == 'null' or request.GET['data_ini'] == 'undefined.undefined.' or request.GET['data_fim'] == 'undefined.undefined.':
            raise MultiValueDictKeyError
        else:
            data_filter = "v.dtacomp between '" + request.GET['data_ini'] + "' and '" + request.GET['data_fim'] + "'"
    except MultiValueDictKeyError:
        data_filter = '''
        extract(month from v.dtacomp) = extract(month from current_date) and
        extract(year from v.dtacomp) = extract(year from current_date)'''

    con = conn()
    cur = con.cursor()
    cur.execute("""
    select first 7
        p.codproduto as codproduto,
        p.dscproduto as nome,
        sum (vi.qtd) as qtd,
        sum (vi.valor) as total_vendas

    from vendas_itens as vi
        inner join vendas as v on vi.venda_id = v.venda_id
        inner join produtos as p on p.codproduto = vi.codproduto
    where 
        """ + data_filter + """

    group by 1, 2
    order by 3 desc
        """)
    d = {
        'codproduto': [],
        'nome': [],
        'qtd': [],
        'total_vendas': [],
    }
    for c in cur.fetchall():
        d['codproduto'].append(str(c[0]))
        d['nome'].append(str(c[1]))
        d['qtd'].append(str(c[2]))
        d['total_vendas'].append(str(c[3]))

    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})

def contas_a_pagar_por_ranking_e_dia(request):
    con = conn()
    cur = con.cursor()
    cur.execute("""
    SELECT DISTINCT
        FPP.FATURAS_PAGAR_ID,
        FP.DOCTO,
        FP.DESPESA_PRINCIPAL,
        DP.DSCDESPESA,
        PC.PARCEIRO,
        PC.NOME,
        FPP.PARCELA,
        FPP.DATA_VENCIMENTO,
        FPP.SALDO,
        FP.HISTORICO

    FROM FATURAS_PAGAR_PARCELAS FPP

        INNER JOIN
            (SELECT
                FATURAS_PAGAR_ID,
                MAX(DATA_VENCIMENTO) AS ULTIMA_PARCELA

            FROM FATURAS_PAGAR_PARCELAS

            GROUP BY FATURAS_PAGAR_ID)
        RECENTES ON
        FPP.FATURAS_PAGAR_ID = RECENTES.FATURAS_PAGAR_ID AND
        FPP.DATA_VENCIMENTO = RECENTES.ULTIMA_PARCELA
        INNER JOIN FATURAS_PAGAR AS FP ON FP.FATURAS_PAGAR_ID = FPP.FATURAS_PAGAR_ID
        INNER JOIN PARCEIROS AS PC ON PC.PARCEIRO = FP.PARCEIRO
        INNER JOIN DESPESAS AS DP ON DP.DESPESA = FP.DESPESA_PRINCIPAL

    WHERE
        FPP.SALDO > 0  and
        FPP.DATA_VENCIMENTO = CURRENT_DATE

    ORDER BY FPP.SALDO DESC
        """)
    d = {
        'fatura_pagar_id': [],
        'docto': [],
        'despesa_principal': [],
        'dscdespesa': [],
        'parceiro': [],
        'nome': [],
        'parcela': [],
        'data_vencimento': [],
        'saldo': [],
        'historico': [],
    }
    for c in cur.fetchall():
        d['fatura_pagar_id'].append(str(c[0]))
        d['docto'].append(str(c[1]))
        d['despesa_principal'].append(str(c[2]))
        d['dscdespesa'].append(str(c[3]))
        d['parceiro'].append(str(c[4]))
        d['nome'].append(str(c[5]))
        d['parcela'].append(str(c[6]))
        d['data_vencimento'].append(str(c[7]))
        d['saldo'].append(str(c[8]))
        d['historico'].append(str(c[9]))

    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})

def contas_a_receber_por_ranking_e_dia(request):
    con = conn()
    cur = con.cursor()
    cur.execute("""
    SELECT DISTINCT
        FPP.FATURAS_RECEBER_ID,
        FP.DOCTO,
        FP.RECEITA_PRINCIPAL,
        R.DSCRECEITA,
        PC.PARCEIRO || '-' || PC.NOME as PARCEIRO,
        FPP.PARCELA,
        FPP.DATA_VENCIMENTO,
        FPP.SALDO,
        FP.HISTORICO

    FROM FATURAS_RECEBER_PARCELAS FPP
        INNER JOIN
            (SELECT
                FATURAS_RECEBER_ID,
                MAX(DATA_VENCIMENTO) AS ULTIMA_PARCELA

            FROM FATURAS_RECEBER_PARCELAS

            GROUP BY FATURAS_RECEBER_ID )
        RECENTES ON
            FPP.FATURAS_RECEBER_ID = RECENTES.FATURAS_RECEBER_ID AND
            FPP.DATA_VENCIMENTO = RECENTES.ULTIMA_PARCELA
        INNER JOIN FATURAS_RECEBER AS FP ON FP.FATURAS_RECEBER_ID = FPP.FATURAS_RECEBER_ID
        INNER JOIN PARCEIROS AS PC ON PC.PARCEIRO = FP.PARCEIRO
        INNER JOIN RECEITAS AS R ON R.RECEITA = FP.RECEITA_PRINCIPAL

    WHERE FPP.SALDO > 0  and FPP.DATA_VENCIMENTO = CURRENT_DATE

    ORDER BY FPP.SALDO DESC
        """)
    d = {
        'faturas_receber_id': [],
        'docto': [],
        'despesa_principal': [],
        'dscdespesa': [],
        'parceiro': [],
        'parcela': [],
        'data_vencimento': [],
        'saldo': [],
        'historico': [],
    }
    for c in cur.fetchall():
        d['faturas_receber_id'].append(str(c[0]))
        d['docto'].append(str(c[1]))
        d['despesa_principal'].append(str(c[2]))
        d['dscdespesa'].append(str(c[3]))
        d['parceiro'].append(str(c[4]))
        d['parcela'].append(str(c[5]))
        d['data_vencimento'].append(str(c[6]))
        d['saldo'].append(str(c[7]))
        d['historico'].append(str(c[8]))

    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})

def detalhes_finaciamento(request):
    con = conn()
    cur = con.cursor()
    cur.execute("""
    SELECT distinct
        FP.FATURAS_PAGAR_ID AS FATURA,
        D.DSCDESPESA,
        FP.PARCEIRO,
        P.NOME,
        FP.SALDO,
        FPR.VALOR,
        FPR.DATA_VENCIMENTO AS ULTIMA_PARCELA,
        FP.DOCTO,
        FP.HISTORICO
    FROM FATURAS_PAGAR FP
        INNER JOIN DESPESAS AS D ON D.DESPESA = FP.DESPESA_PRINCIPAL
        INNER JOIN DESPESAS_GRUPO AS DG ON DG.DESPESAS_GRUPO = D.DESPESAS_GRUPO
        INNER JOIN PARCEIROS AS P ON P.PARCEIRO = FP.PARCEIRO
        INNER JOIN FATURAS_PAGAR_PARCELAS AS FPR ON FPR.FATURAS_PAGAR_ID = FP.FATURAS_PAGAR_ID
        INNER JOIN (SELECT
                        FATURAS_PAGAR_ID,
                        MAX (DATA_VENCIMENTO) AS ULTIMA_PARCELA
                    FROM FATURAS_PAGAR_PARCELAS
                    GROUP BY FATURAS_PAGAR_ID ) RECENTES ON FPR.FATURAS_PAGAR_ID =  RECENTES.FATURAS_PAGAR_ID AND
                                                                                    FPR.DATA_VENCIMENTO = RECENTES.ULTIMA_PARCELA
    WHERE
        DG.DESPESAS_GRUPO =  'FINANCIAMENTOS' and
        FP.SALDO > 0

    ORDER BY 6 DESC
        """)
    d = []
    for c in cur.fetchall():
        d.append({
            'id_fatura': str(c[0]),
            'dscdespesa': str(c[1]),
            'parceiro': str(c[2]),
            'nome': str(c[3]),
            'saldo': str(c[4]),
            'valor': str(c[5]),
            'data_vencimento': str(c[6]),
            'docto': str(c[7]),
            'historico': str(c[8]),
        })

    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})

def saldo_disponivel_em_contas(request):
    con = conn()
    cur = con.cursor()
    cur.execute("""
    SELECT
        BM.CONTA,
        CB.NOME_BANCO,
        CB.BANCO,
        CB.CODAGENCIA,
        CB.DVAGENCIA,
        CB.NUMCONTA,
        SUM (BM.VALOR) TOTAL_VALOR

    FROM
        (SELECT
            BM.CONTA,
            CB.NOME_BANCO,
            CB.BANCO,
            CB.CODAGENCIA,
            CB.DVAGENCIA,
            CB.NUMCONTA,
            +(-BM.VALOR) as valor
        FROM BANCOS_MOVIMENTO AS BM
            INNER JOIN CONTAS_BANCARIAS AS CB ON CB.CONTA = BM.CONTA
        WHERE BM.TIPO_DC = 'C' AND BM.DATA_CONCILIACAO IS NULL
        UNION ALL
        SELECT
            BM.CONTA,
            CB.NOME_BANCO,
            CB.BANCO,
            CB.CODAGENCIA,
            CB.DVAGENCIA,
            CB.NUMCONTA,
            +(+BM.VALOR) as valor
        FROM BANCOS_MOVIMENTO AS BM
            INNER JOIN CONTAS_BANCARIAS AS CB ON CB.CONTA = BM.CONTA
        WHERE BM.TIPO_DC = 'D' AND BM.DATA_CONCILIACAO IS NULL) as BM
            INNER JOIN CONTAS_BANCARIAS AS CB ON CB.CONTA = BM.CONTA

    GROUP BY 1,2,3,4,5,6
        """)
    d = []
    for c in cur.fetchall():
        d.append({
            'conta': str(c[0]),
            'nome_banco': str(c[1]),
            'banco': str(c[2]),
            'codagencia': str(c[3]),
            'dvagencia': str(c[4]),
            'numconta': str(c[5]),
            'valor': str(c[6])
        })

    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})

def rankingComprasPorFornecedor(request):
    con = conn()
    cur = con.cursor()
    cur.execute("""
    SELECT FIRST 10 DISTINCT
        C.PARCEIRO,
        P.NOME,
        SUM(C.VLRNOTA) VALOR_NOTA

    FROM COMPRAS C
        INNER JOIN PARCEIROS AS P ON P.PARCEIRO = C.PARCEIRO

    WHERE 
        C.DATA_ENTRADA BETWEEN CURRENT_DATE -30 AND CURRENT_DATE

    GROUP BY 1,2
    ORDER BY VALOR_NOTA DESC
        """)
    d = {
        'parceiro': [],
        'nome': [],
        'valor_nota': [],
    }
    for c in cur.fetchall():
        d['parceiro'].append(str(c[0]))
        d['nome'].append(str(c[1]))
        d['valor_nota'].append(str(c[2]))

    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})

def fluxo_de_caixa(request):
    try:
        if request.GET['dias'] == 'null' or request.GET['dias'] =='undefined.undefined.':
            raise MultiValueDictKeyError
        else:
            dias = int(request.GET['dias'])
            sql = """\n(SELECT SUM(SALDO) AS TOTAL_RECEBER_NO_DIA_01 FROM FATURAS_RECEBER_PARCELAS WHERE SALDO > '0' AND DATA_VENCIMENTO = (CURRENT_DATE)),
        (SELECT SUM(SALDO) AS TOTAL_PAGAR_HOJE FROM FATURAS_PAGAR_PARCELAS WHERE SALDO > '0' AND DATA_VENCIMENTO BETWEEN (CURRENT_DATE) AND (CURRENT_DATE)),
        cast(extract (day from current_date) as varchar(2))|| '/' ||cast(extract (month from current_date) as varchar(2)) || '/' || cast(extract (year from current_date) as varchar(4)) as data0"""
            i = 1
            while i <= dias:
                sql = sql + """,\n
        (SELECT SUM(SALDO) AS TOTAL_RECEBER_NO_DIA_01 FROM FATURAS_RECEBER_PARCELAS WHERE SALDO > '0' AND DATA_VENCIMENTO = (CURRENT_DATE +"""+str(i)+""")),
        (SELECT SUM(SALDO) AS TOTAL_PAGAR_NO_DIA_01 FROM FATURAS_PAGAR_PARCELAS WHERE SALDO > '0' AND DATA_VENCIMENTO = (CURRENT_DATE +"""+str(i)+""")),
        cast(extract (day from current_date+"""+str(i)+""") as varchar(2))|| '/' ||cast(extract (month from current_date+"""+str(i)+""") as varchar(2)) || '/' || cast(extract (year from current_date+"""+str(i)+""") as varchar(4)) as data"""+str(i)
                i = i + 1
        
    except MultiValueDictKeyError:
        dias = 20
        sql = """\n(SELECT SUM(SALDO) AS TOTAL_RECEBER_NO_DIA_01 FROM FATURAS_RECEBER_PARCELAS WHERE SALDO > '0' AND DATA_VENCIMENTO = (CURRENT_DATE)),
        (SELECT SUM(SALDO) AS TOTAL_PAGAR_HOJE FROM FATURAS_PAGAR_PARCELAS WHERE SALDO > '0' AND DATA_VENCIMENTO BETWEEN (CURRENT_DATE) AND (CURRENT_DATE)),
        cast(extract (day from current_date) as varchar(2))|| '/' ||cast(extract (month from current_date) as varchar(2)) || '/' || cast(extract (year from current_date) as varchar(4)) as data0"""
        i = 1
        while i <= dias:
            sql = sql + """,\n
        (SELECT SUM(SALDO) AS TOTAL_RECEBER_NO_DIA_01 FROM FATURAS_RECEBER_PARCELAS WHERE SALDO > '0' AND DATA_VENCIMENTO = (CURRENT_DATE +"""+str(i)+""")),
        (SELECT SUM(SALDO) AS TOTAL_PAGAR_NO_DIA_01 FROM FATURAS_PAGAR_PARCELAS WHERE SALDO > '0' AND DATA_VENCIMENTO = (CURRENT_DATE +"""+str(i)+""")),
        cast(extract (day from current_date+"""+str(i)+""") as varchar(2))|| '/' ||cast(extract (month from current_date+"""+str(i)+""") as varchar(2)) || '/' || cast(extract (year from current_date+"""+str(i)+""") as varchar(4)) as data"""+str(i)
            i = i + 1

    con = conn()
    cur = con.cursor()
    cur.execute(""" 
    SELECT
        """ + sql + """
    FROM 
        FATURAS_RECEBER_PARCELAS WHERE SALDO > '0' AND 
        DATA_VENCIMENTO BETWEEN (CURRENT_DATE) AND (CURRENT_DATE)    
    
    group by
        1
    """)
    d = {
        'contas_receber': [],
        'contas_pagar': [],
        'data': [],
    }
    i = 0
    for c in cur.fetchall():
        i = 0
        while i < len(c):
            d["contas_receber"].append(float(c[i]) if c[i] != None else 0)
            i = i + 1
            # print(c[i])
            d["contas_pagar"].append(float(c[i]) if c[i] != None else 0)
            i = i + 1
            d["data"].append(str(c[i]))
            i = i + 1

    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})

def ticket_medio_de_compra(request):
    con = conn()
    cur = con.cursor()
    cur.execute("""
    SELECT
        SUM(VLRNOTA) AS VALOR_NOTA,
        COUNT(COMPRA_ID) AS QTD_DE_NOTAS_COMPRAS,
        (SUM(VLRNOTA) / count(COMPRA_ID)) as MEDIA_COMPRAS

    FROM COMPRAS C

    WHERE
        C.IDN_CANCELADA = 'N' AND
        DATA_ENTRADA BETWEEN (current_date -90) and (Current_date)
        """)
    d = []
    for c in cur.fetchall():
        d.append({
            'valor_nota': str(c[0]),
            'qtd_nota_compradas': str(c[1]),
            'media_compras': str(c[2]),
        })

    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})

def sql(request):
    con = conn()
    cur = con.cursor()
    cur.execute("""
    sql
        """)
    d = {
        'codcliente': [],
        'nome': [],
        'total_vendas': [],
    }
    for c in cur.fetchall():
        d['codcliente'].append(str(c[0]))
        d['nome'].append(str(c[1]))
        d['total_vendas'].append(str(c[1]))

    con.close()
    return HttpResponse(json.dumps(d), status=200, headers={'content-type': 'application/json'})