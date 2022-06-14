const comercial ={
    delimiters: ['[[',']]'],
    data () {
        return {
            rankingclientes_var: null,
            rankingclientes_total_vendas: null,
            rankingclientes_sum: 0,
            rankingvendedores_var: null,
            rankingvendedores_total_vendas: null,
            rankingvendedores_sum: 0,
            colors: [
                '#c438ef',
                '#05cd99',
                '#4318ff',
                '#ffc086',
                '#ff409a',
                '#6452ff',
                '#05cd99',
            ],
            metadevendas_total: null,
            metadevendas_atual: null,

            class_nav: 'deactive',
        }
    },
    methods: {
        navBar () {
            if (this.class_nav == 'deactive') {
                this.class_nav = 'active'
            } else {                
                this.class_nav = 'deactive';
            }
        },
        moneyFilter (msg){
            return parseFloat(msg).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
        },
        tamanhoBarra (barra,total){
            const tamanho = parseFloat(parseInt(parseFloat(barra)/parseFloat(total)*100))
            if (tamanho < 10) {return 10}
            return tamanho;
        },
        corAleatoria (cores) {
            const num = Math.floor(Math.random() * cores.length)
            return (cores[num])
        },
        async valorVendas () {
            const req = await fetch('/total_vendas')
            const res = await req.json()
            self.total_vendas_value.innerHTML = this.moneyFilter(res.total_vendas)
        },

        async valorCMV () {
            const req = await fetch('/total_cmv')
            const res = await req.json()
            self.total_cmv_value.innerHTML = this.moneyFilter(res.total_cmv)
        },

        async valorLucroBrutoMensal () {
            const req = await fetch('/lucro_bruto_mensal')
            const res = await req.json()
            self.total_lucro_bruto_value.innerHTML = this.moneyFilter(res.valor_total)
        },
        
        async valorVendasMensais () {
            const req = await fetch('/total_vendas_mensal')
            const res = await req.json()

            const data = {
                labels: res.dscmes,
                datasets: [{
                    label: 'Valor de Vendas Mensais',
                    backgroundColor: 'rgb(67, 24, 255)',
                    borderColor: 'rgb(134, 140, 255)',
                    data: res.total_vendas,
                    tension: 0.2,
                    fill: false
                }]
            };
            const config = {
                type: 'line',
                data: data,
                options: {
                    maintainAspectRatio: false,
                }
            };
            var chartStatus = Chart.getChart("total_vendas_mensal_chart"); // <canvas> id
            if (chartStatus != undefined) {
                chartStatus.data.datasets.data = res.total_vendas
                chartStatus.update()
            }else {
                const total_vendas_mensal = new Chart(
                    document.getElementById('total_vendas_mensal_chart'),
                    config
                );
            }
            total = res.total_vendas.length
            if (parseInt(res.total_vendas[total-1]) < parseInt(res.total_vendas[total-2])) {
                self.total_evolucao_arrow.innerHTML = 'arrow_drop_down'
                self.total_evolucao_arrow.style = 'color: red;'
                self.total_evolucao.style = 'color: red;'
                self.total_evolucao.innerHTML = 100 - (res.total_vendas[total-1]/res.total_vendas[total-2]*100).toFixed(2) + '%';                
            }else{
                self.total_evolucao_arrow.innerHTML = 'arrow_drop_up'
                self.total_evolucao_arrow.style = 'color: green;'
                self.total_evolucao.style = 'color: green;'
                self.total_evolucao.innerHTML = (res.total_vendas[total-1]/res.total_vendas[total-2]*100).toFixed(2) - 100 + '%';                

            }
        },

        async valorVendasPorAgrupamento () {
            const req = await fetch('/vendas_por_agrupamento_mensal')
            const res = await req.json()
            
            const data = {
                labels: res.dscagrupamento,
                datasets: [{
                    label: 'Valor de Vendas Mensais',
                    backgroundColor: this.colors,
                    hoverOffset: 4,
                    data: res.total_vendas,
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
            var chartStatus = Chart.getChart("total_vendas_por_agrupamento_chart"); // <canvas> id
            if (chartStatus != undefined) {
                chartStatus.data.datasets.data = res.total_vendas
                chartStatus.update()
            }else {
                const total_por_agrupamento = new Chart(
                    document.getElementById('total_vendas_por_agrupamento_chart'),
                    config
                );
            }
        },

        async metaDeVendas () {
            const req = await fetch('/meta_de_vendas')
            const res = await req.json()

            this.metadevendas_total = parseFloat(res.total_vendido);
            this.metadevendas_atual = parseFloat(res.valor);
        },

        async rankingVendasPorVendedor () {
            const req = await fetch('/total_de_vendas_por_vendedor')
            const res = await req.json()

            this.rankingvendedores_var = res
            this.rankingvendedores_sum = parseFloat(res[0].valor)
            this.rankingvendedores_total_vendas = parseFloat(res.valor).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })

        },

        async rankingVendasPorCliente () {
            const req = await fetch('/ranking_de_vendas_por_cliente')
            const res = await req.json()

            this.rankingclientes_var = res
            this.rankingclientes_sum = parseFloat(res[0].total_vendas)
            this.rankingclientes_total_vendas = parseFloat(res.total_vendas).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
        },
        
        async produtosMaisVendidos () {
            const req = await fetch('/ranking_de_vendas_por_produto')
            const res = await req.json()
            
            const data = {
                labels: res.nome,
                datasets: [{
                    label: 'Valor de Vendas Mensais',
                    backgroundColor: this.colors,
                    hoverOffset: 4,
                    data: res.qtd,
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
            var chartStatus = Chart.getChart("produtos_mais_vendidos_chart");
            if (chartStatus != undefined) {
                chartStatus.data.datasets.data = res.total_vendas
                chartStatus.update()
            }else {
                const total_por_agrupamento = new Chart(
                    document.getElementById('produtos_mais_vendidos_chart'),
                    config
                );
            }
        },

        
    },
    mounted () {
        this.valorVendas()
        this.valorCMV()
        this.valorLucroBrutoMensal()
        this.valorVendasMensais()
        this.metaDeVendas()
        this.rankingVendasPorVendedor()
        this.valorVendasPorAgrupamento()
        this.rankingVendasPorCliente()
        this.produtosMaisVendidos()
        setInterval(() => {
            this.valorVendas()
            this.valorCMV()
            this.valorLucroBrutoMensal()
            this.valorVendasMensais()
            this.metaDeVendas()
            this.rankingVendasPorVendedor()
            this.valorVendasPorAgrupamento()
            this.rankingVendasPorCliente()
            this.produtosMaisVendidos()
        }, 10000)
    }
}

Vue.createApp(comercial).mount('#app')