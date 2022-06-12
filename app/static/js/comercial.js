const comercial ={
    delimiters: ['[[',']]'],
    data () {
        return {
            hostBack: '',
            hostFront: '',
            rankingclientes_var: null,
            rankingclientes_total_vendas: null,
            rankingclientes_sum: 0,
            rankingvendedores_var: null,
            rankingvendedores_total_vendas: null,
            rankingvendedores_sum: 0,
            colors: [
                '#c438ef',
                '#ff409a',
                '#6452ff',
                '#05cd99',
                '#6452ff',
                '#ffc086',
                '#4318ff',
                '#05cd99',
            ],
            metadevendas_total: null,
            metadevendas_atual: null,
            heightDefined: 0,

            class_nav: 'deactive',
            url: ''
        }
    },
    methods: {
        heightDefine () {
            if (window.screen.width < 630) {
                this.heightDefined = parseInt(window.screen.height)*0.30
            }else {
                this.heightDefined = parseInt(window.screen.height)*0.24
            }
        },
        // async verifyLogin () {
        //     let data = {
        //         "token": sessionStorage.getItem("access")
        //     }
        //     const req = await fetch(this.hostBack+'/jwt/verify/', {
        //         method: 'POST',
        //         body: JSON.stringify(data),
        //         headers: {"Content-type": "application/json"}
        //     })
        //     const res = await req.json()


        //     if (req.status == '200') {
        //         let data = {
        //             "refresh": sessionStorage.getItem("refresh")
        //         }
        //         const req_refresh = await fetch(this.hostBack+'/jwt/refresh/', {
        //             method: 'POST',
        //             body: JSON.stringify(data),
        //             headers: {"Content-type": "application/json"}
        //         })
        //         const res_refresh = await req_refresh.json()
        //         sessionStorage.setItem('access', res_refresh.access)
        //     }else{
        //         // window.location.href = this.hostFront+"/accounts/login/?next=/painel/comercial/"
        //     }
        // },
        defData () {
            const ini = self.data_ini.value.split('-', 3)
            const fim = self.data_fim.value.split('-', 3)
            window.location.href = (this.hostFront+'/painel/comercial/?data_ini='+ini[2]+'.'+ini[1]+'.'+ini[0]+'&data_fim='+fim[2]+'.'+fim[1]+'.'+fim[0])
        },
        defFilter () {
            const urlParams = new URLSearchParams(window.location.search);
            const data_ini = urlParams.get('data_ini')
            const data_fim = urlParams.get('data_fim')
            const urlFilter = '?data_ini='+data_ini+'&data_fim='+data_fim
            return urlFilter
        },
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
            const req = await fetch(this.hostBack+'/total_vendas/'+this.defFilter())
            const res = await req.json()
            self.total_vendas_value.innerHTML = this.moneyFilter(res.total_vendas)
        },

        async valorCMV () {
            const req = await fetch(this.hostBack+'/total_cmv/'+this.defFilter())
            const res = await req.json()
            self.total_cmv_value.innerHTML = this.moneyFilter(res.total_cmv)
        },

        async valorLucroBrutoMensal () {
            const req = await fetch(this.hostBack+'/lucro_bruto_mensal/'+this.defFilter())
            const res = await req.json()
            self.total_lucro_bruto_value.innerHTML = this.moneyFilter(res.valor_total)
        },
        
        async valorVendasMensais () {
            const req = await fetch(this.hostBack+'/total_vendas_mensal/'+this.defFilter())
            const res = await req.json()

            const total_vendas_mensal_chart = Highcharts.chart('total_vendas_mensal_chart', {
                plotOptions: {
                    series: {
                        // general options for all series
                    },
                    spline: {
                        color: 'rgb(67, 24, 255)',
                        colorIndex: 'rgb(134, 140, 255)',
                    },
                },
                chart: {
                    height: this.heightDefined
                },
                title: {
                    text: undefined,
                },
                xAxis: {
                    categories: res.dscmes,
                },
                yAxis: {
                    title: {
                        text: undefined,
                    }
                },
                series: [{
                    type: 'spline',
                    name: 'Meses',
                    data: res.total_vendas
                }]
            })
            let total = res.total_vendas.length
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
            const req = await fetch(this.hostBack+'/vendas_por_agrupamento_mensal/'+this.defFilter())
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
            var chartStatus = Chart.getChart("total_vendas_por_agrupamento_chart");
            if (chartStatus != undefined) {
                chartStatus.data.datasets.data = res.total_vendas
                chartStatus.update()
            }else {
                const total_por_agrupamento_mensal = new Chart(
                    document.getElementById('total_vendas_por_agrupamento_chart'),
                    config
                );
            }
        },

        async metaDeVendas () {
            const req = await fetch(this.hostBack+'/meta_de_vendas')
            const res = await req.json()

            this.metadevendas_total = parseFloat(res.total_vendido);
            this.metadevendas_atual = parseFloat(res.valor);
        },

        async rankingVendasPorVendedor () {
            const req = await fetch(this.hostBack+'/total_de_vendas_por_vendedor')
            const res = await req.json()

            // this.rankingvendedores_var = res
            // this.rankingvendedores_sum = parseFloat(res[0].valor)
            // this.rankingvendedores_total_vendas = parseFloat(res.valor).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
            const total_vendas_mensal_chart = Highcharts.chart('ranking_de_vendas_por_vendedor_chart', {
                plotOptions: {
                    series: {
                        // general options for all series
                    },
                    bar: {
                        color: 'rgb(67, 24, 255)',
                        colorIndex: 'rgb(134, 140, 255)',
                    },
                },
                chart: {
                    height: parseInt(window.screen.height)*0.42
                },
                title: {
                    text: undefined,
                },
                xAxis: {
                    categories: res.nome
                },
                yAxis: {
                    title: {
                        text: undefined,
                    }
                },
                series: [{
                    type: 'bar',
                    name: 'Vendedores',
                    data: res.valor,
                },]
            })

        },

        async rankingVendasPorCliente () {
            const req = await fetch(this.hostBack+'/ranking_de_vendas_por_cliente')
            const res = await req.json()

            // this.rankingclientes_var = res
            // this.rankingclientes_sum = parseFloat(res[0].total_vendas)
            // this.rankingclientes_total_vendas = parseFloat(res.total_vendas).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })

            const total_vendas_mensal_chart = Highcharts.chart('ranking_de_vendas_por_cliente_chart', {
                plotOptions: {
                    series: {
                        // general options for all series
                    },
                    bar: {
                        color: 'rgb(67, 24, 255)',
                        colorIndex: 'rgb(134, 140, 255)',
                    },
                },
                chart: {
                    height: parseInt(window.screen.height)*0.55
                },
                title: {
                    text: undefined,
                },
                xAxis: {
                    categories: res.nome
                },
                yAxis: {
                    title: {
                        text: undefined,
                    }
                },
                series: [{
                    type: 'bar',
                    name: 'Clientes',
                    data: res.total_vendas,
                },]
            })
        },
        
        async produtosMaisVendidos () {
            const req = await fetch(this.hostBack+'/ranking_de_vendas_por_produto')
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
        this.heightDefine()
        setInterval(() => {
            this.heightDefine()
        }, 1000)
        this.valorVendas()
        this.valorCMV()
        this.valorLucroBrutoMensal()
        this.valorVendasMensais()
        this.metaDeVendas()
        this.rankingVendasPorVendedor()
        this.valorVendasPorAgrupamento()
        this.rankingVendasPorCliente()
        this.produtosMaisVendidos()
        
        // this.verifyLogin()
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
            
            // this.verifyLogin()
        }, 30000)
    }
}

Vue.createApp(comercial).mount('#app')