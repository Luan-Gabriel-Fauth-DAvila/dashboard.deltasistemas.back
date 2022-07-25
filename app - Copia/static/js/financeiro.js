const financeiro = {
    delimiters: ['[[',']]'],
    data () {
        return {
            hostBackEnd: '',
            colors: [
                '#c438ef',
                '#05cd99',
                '#4318ff',
                '#ffc086',
                '#ff409a',
                '#6452ff',
                '#05cd99',
            ],
            detalhesFinaciamentoEmprestimo_var: null,
            detalhesFinaciamentoEmprestimo_sum: null,
            detalhesFinaciamentoEmprestimo_total: null, 

            saldoDisponivelEmContas_var: null,
            saldoDisponivelEmContas_sum: null,
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

        async saldoDisponivelEmContas () {
            const req = await fetch(this.hostBackEnd+'/saldo_disponivel_em_contas')
            const res = await req.json()

            this.saldoDisponivelEmContas_var = res
            let sum = 0
            for (let i = 0; i < res.length; i++) {
                sum = sum + parseFloat(res[i].valor)
            }
            this.saldoDisponivelEmContas_sum = sum
        },
        defData () {
            const ini = self.data_ini.value.split('-', 3)
            const fim = self.data_fim.value.split('-', 3)
            window.location.href = ('/painel/financeiro/?data_ini='+ini[2]+'.'+ini[1]+'.'+ini[0]+'&data_fim='+fim[2]+'.'+fim[1]+'.'+fim[0])
        },
        defFilter () {
            const urlParams = new URLSearchParams(window.location.search);
            const data_ini = urlParams.get('data_ini')
            const data_fim = urlParams.get('data_fim')
            const urlFilter = '?data_ini='+data_ini+'&data_fim='+data_fim
            return urlFilter
        },

        async contasReceberAtrasadas () {
            const req = await fetch(this.hostBackEnd+'/contas_a_receber_do_inicio_ate_a_data_atual')
            const res = await req.json()
            
            self.cr_atrasado_value.innerHTML = this.moneyFilter(res.faturas_receber)
        },

        async contasReceberAVencer () {
            const req = await fetch(this.hostBackEnd+'/contas_a_receber_a_partir_da_data_atual')
            const res = await req.json()

            self.cr_vencer_value.innerHTML = this.moneyFilter(res.faturas_receber)
        },

        async contasPagarAtrasadas () {
            const req = await fetch(this.hostBackEnd+'/contas_a_pagar_do_inicio_ate_a_data_atual')
            const res = await req.json()
            
            self.cp_atrasado_value.innerHTML = this.moneyFilter(res.faturas_pagar)
        },

        async contasPagarAVencer () {
            const req = await fetch(this.hostBackEnd+'/contas_a_pagar_a_partir_da_data_atual')
            const res = await req.json()

            self.cp_vencer_value.innerHTML = this.moneyFilter(res.faturas_pagar)
        },

        async contasReceber () {
            const req = await fetch(this.hostBackEnd+'/contas_a_receber_por_ranking_e_dia')
            const res = await req.json()

            let parceiro = []
            res.parceiro.forEach(function (e) {
                parceiro.push(e.substr(0,10))
            })
            const data = {
                labels: parceiro,
                datasets: [{
                    data: res.saldo,
                    label: 'Constas a Receber',
                    borderColor: '#05CD99',
                    backgroundColor: '#05CD99',
                    borderWidth: 2,
                    borderRadius: '5px',
                    borderSkipped: false,
                }]
            };
            const config = {
            type: 'bar',
            data: data,
                options: {
                    maintainAspectRatio: false,
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: false,
                        }
                    }
                },
            };
            var chartStatus = Chart.getChart("contas_a_receber_chart"); // <canvas> id
            if (chartStatus != undefined) {
                chartStatus.data.datasets.data = res.total_vendas
                chartStatus.update()
            }else {
                const contas_a_receber = new Chart(
                    document.getElementById('contas_a_receber_chart'),
                    config
                );
            }
        },

        async contasPagar () {
            const req = await fetch(this.hostBackEnd+'/contas_a_pagar_por_ranking_e_dia')
            const res = await req.json()

            const data = {
                labels: res.nome,
                datasets: [{
                    data: res.saldo,
                    label: 'Constas a Pagar',
                    borderColor: '#FF869C',
                    backgroundColor: '#FF869C',
                    borderWidth: 2,
                    maxBarThickness: 64,

                    borderRadius: '10px',
                    borderSkipped: false,
                }]
            };
            const config = {
            type: 'bar',
            data: data,
                options: {
                    maintainAspectRatio: false,
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        title: {
                            display: false,
                        }
                    }
                },
            };
            var chartStatus = Chart.getChart("contas_a_pagar_chart"); // <canvas> id
            if (chartStatus != undefined) {
                chartStatus.data.datasets.data = res.total_vendas
                chartStatus.update()
            }else {
                const total_vendas_mensal = new Chart(
                    document.getElementById('contas_a_pagar_chart'),
                    config
                );
            }
        },

        async recebimentosPorForma () {
            const req = await fetch(this.hostBackEnd+'/total_de_recebimentos_por_forma_mensal/resumo_geral')
            const res = await req.json()

            const formaRecebimentoTitle = [
                'Recebimentos Cartão',
                'Recebimentos em Dinheiro',
                'Recebimentos',
                'Cheques Recebidos',
                'Entradas em Banco',
            ]
            const formaRecebimentosValue = [
                res.rec_cartao,
                res.rec_dinheiro,
                res.recebimentos,
                res.cheques_recebidos,
                res.entradas_bancos,
            ]
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
            var chartStatus = Chart.getChart("recebimentos_por_forma_chart"); // <canvas> id
            if (chartStatus != undefined) {
                chartStatus.data.datasets.data = res.total_vendas
                chartStatus.update()
            }else {
                const total_por_agrupamento = new Chart(
                    document.getElementById('recebimentos_por_forma_chart'),
                    config
                );
            }
            //FIM GRÁFICO
        },

        async detalhesFinaciamentoEmprestimo () {
            const req = await fetch(this.hostBackEnd+'/detalhes_finaciamento')
            const res = await req.json()
            
            this.detalhesFinaciamentoEmprestimo_var = res
            this.detalhesFinaciamentoEmprestimo_sum = parseFloat(res[0].valor)

            let value = 0
            for (let i = 0; i < res.length; i++) {
                value = value + parseFloat(res[i].valor)
            }
            this.detalhesFinaciamentoEmprestimo_total = this.moneyFilter(value)
        },

        async fluxoDeCaixa () {
            const req = await fetch(this.hostBackEnd+'/fluxo_de_caixa/?dias='+document.getElementById('dias_fluxo_caixa').value)
            const res = await req.json()

            const total_vendas_mensal_chart = Highcharts.chart('fluxo_20_dias_chart', {
                plotOptions: {
                    series: {
                        // general options for all series
                    },
                    spline: {
                    },
                },
                chart: {
                    height: parseInt(window.screen.height)*0.32
                },
                title: {
                    text: undefined,
                },
                xAxis: {
                    categories: res.data,
                },
                yAxis: {
                    title: {
                        text: undefined,
                    }
                },
                series: [{
                    type: 'spline',
                    name: 'Contas a Pagar',
                    data: res.contas_pagar,
                    color: '#FF869C',
                },{
                    type: 'spline',
                    name: 'Contas a Receber',
                    data: res.contas_receber,
                    color: '#05CD99',
                }]
            })
        }
    },
    mounted () {
        document.getElementById('dias_fluxo_caixa').addEventListener("change", () => {
            this.fluxoDeCaixa()
        })

        this.saldoDisponivelEmContas()
        this.contasReceberAtrasadas()
        this.contasReceberAVencer()
        this.contasPagarAtrasadas()
        this.contasPagarAVencer()
        this.contasReceber()
        this.contasPagar()
        this.recebimentosPorForma()
        this.detalhesFinaciamentoEmprestimo()
        this.fluxoDeCaixa()
        setInterval(() => {
            this.saldoDisponivelEmContas()
            this.contasReceberAtrasadas()            
            this.contasReceberAVencer()
            this.contasPagarAtrasadas()
            this.contasPagarAVencer()
            this.contasReceber()
            this.contasPagar()
            this.recebimentosPorForma()
            this.detalhesFinaciamentoEmprestimo()
            this.fluxoDeCaixa()
        }, 10000)
    },
}
Vue.createApp(financeiro).mount('#app')