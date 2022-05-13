const estoque = {
    delimiters: ['[[',']]'],
    data () {
        return {
            colors: [
                '#c438ef',
                '#05cd99',
                '#4318ff',
                '#ffc086',
                '#ff409a',
                '#6452ff',
                '#05cd99',
            ],
        }
    },
    methods: {
        moneyFilter (msg){
            return parseFloat(msg).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
        },
        
        tamanhoBarra (barra,total){
            const tamanho = parseFloat(parseInt(parseFloat(barra)/parseFloat(total)*100))
            if (tamanho < 10) {return 10}
            return tamanho;
        },

        async qtdCilindrosCheios () {
            const req = await fetch('/qtd_cilindros_cheios')
            const res = await req.json()
            
        },

        async ticketMedioDeCompra () {
            const req = await fetch('/ticket_medio_de_compra')
            const res = await req.json()
            
            self.ticket_medio_de_compra_value.innerHTML = this.moneyFilter(res[0].media_compras)
        },

        async valorDeTodosOsProdutos () {
            const req = await fetch('/total_de_valores_de_todos_os_produtos')
            const res = await req.json()
            
            self.prod_em_estoque_value.innerHTML = res.quantidade
            self.vlr_prod_em_estoque_value.innerHTML = this.moneyFilter(res.valor_total)
        },

        async rankingComprasPorFornecedor () {
            const req = await fetch('/ranking_compras_por_fornecedor')
            const res = await req.json()

            const formaRecebimentoTitle = res.nome
            const formaRecebimentosValue = res.valor_nota
            //GRÁFICO
            const data = {
                labels: formaRecebimentoTitle,
                datasets: [{
                    label: 'Valor de Vendas Mensais',
                    data: formaRecebimentosValue,
                    backgroundColor: this.colors,
                    hoverOffset: 4,
                }]
            };
            const config = {
                type: 'pie',
                data: data,
                options: {
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'right'
                        },
                    },
                }
            };
            var chartStatus = Chart.getChart("ranking_compras_por_fornecedor_chart"); // <canvas> id
            if (chartStatus != undefined) {
                chartStatus.data.datasets.data = res.total_vendas
                chartStatus.update()
            }else {
                const total_por_agrupamento = new Chart(
                    document.getElementById('ranking_compras_por_fornecedor_chart'),
                    config
                );
            }
        },

        async rankingProdutoMaisComprado () {
            const req = await fetch('/ranking_produto_mais_comprado')
            const res = await req.json()

            const formaRecebimentoTitle = res.dscproduto
            const formaRecebimentosValue = res.quantidade
            //GRÁFICO
            const data = {
                labels: formaRecebimentoTitle,
                datasets: [{
                    label: 'Produto mais Comprado',
                    data: formaRecebimentosValue,
                    backgroundColor: this.colors,
                    hoverOffset: 4,
                }]
            };
            const config = {
                type: 'pie',
                data: data,
                options: {
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'right'
                        },
                    },
                }
            };
            var chartStatus = Chart.getChart("ranking_produto_mais_comprado_chart"); // <canvas> id
            if (chartStatus != undefined) {
                chartStatus.data.datasets.data = res.total_vendas
                chartStatus.update()
            }else {
                const total_por_agrupamento = new Chart(
                    document.getElementById('ranking_produto_mais_comprado_chart'),
                    config
                );
            }
        }
    },
    mounted () {
        this.ticketMedioDeCompra()
        this.valorDeTodosOsProdutos()
        this.rankingComprasPorFornecedor()
        this.rankingProdutoMaisComprado ()
        setInterval(() => {
            this.ticketMedioDeCompra()
            this.valorDeTodosOsProdutos()
            this.rankingComprasPorFornecedor()
            this.rankingProdutoMaisComprado ()
        },10000)
    },
}
Vue.createApp(estoque).mount('#app')