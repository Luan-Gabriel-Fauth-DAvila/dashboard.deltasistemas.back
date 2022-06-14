const financeiro = {
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
            const req = await fetch('/saldo_disponivel_em_contas')
            const res = await req.json()

            this.saldoDisponivelEmContas_var = res
            let sum = 0
            for (let i = 0; i < res.length; i++) {
                sum = sum + parseFloat(res[i].valor)
            }
            this.saldoDisponivelEmContas_sum = sum
        },

        async contasReceberAtrasadas () {
            const req = await fetch('/contas_a_receber_do_inicio_ate_a_data_atual')
            const res = await req.json()
            
            self.cr_atrasado_value.innerHTML = this.moneyFilter(res.faturas_receber)
        },

        async contasReceberAVencer () {
            const req = await fetch('/contas_a_receber_a_partir_da_data_atual')
            const res = await req.json()

            self.cr_vencer_value.innerHTML = this.moneyFilter(res.faturas_receber)
        },

        async contasPagarAtrasadas () {
            const req = await fetch('/contas_a_pagar_do_inicio_ate_a_data_atual')
            const res = await req.json()
            
            self.cp_atrasado_value.innerHTML = this.moneyFilter(res.faturas_pagar)
        },

        async contasPagarAVencer () {
            const req = await fetch('/contas_a_pagar_a_partir_da_data_atual')
            const res = await req.json()

            self.cp_vencer_value.innerHTML = this.moneyFilter(res.faturas_pagar)
        },

        async contasReceber () {
            const req = await fetch('/contas_a_receber_por_ranking_e_dia')
            const res = await req.json()

            const data = {
                labels: res.nome,
                datasets: [
                    {
                        data: res.saldo,
                        borderColor: '#05CD99',
                        backgroundColor: '#05CD99',
                        borderWidth: 2,
                        borderRadius: '5px',
                        borderSkipped: false,
                    },
                ]
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
                const total_vendas_mensal = new Chart(
                    document.getElementById('contas_a_receber_chart'),
                    config
                );
            }
        },

        async contasPagar () {
            const req = await fetch('/contas_a_pagar_por_ranking_e_dia')
            const res = await req.json()

            const data = {
                labels: res.nome,
                datasets: [
                    {
                        data: res.saldo,
                        borderColor: '#FF869C',
                        backgroundColor: '#FF869C',
                        borderWidth: 2,
                        borderRadius: '10px',
                        borderSkipped: false,
                    },
                ]
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
            const req = await fetch('/total_de_recebimentos_por_forma_mensal/resumo_geral')
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
            const req = await fetch('/detalhes_finaciamento')
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
            const req = await fetch('/fluxo_de_caixa')
            const res = await req.json()

            const data = {
                labels: ['hoje','+1','+2','+3','+4','+5','+6','+7','+8','+9','+10','+11','+12','+13','+14','+15','+16','+17','+18','+19','+20'],
                datasets: [
                    {
                        label: 'Contas a Receber',
                        data: res.contas_receber,
                        tension: 0.3,
                        borderColor: '#05CD99',
                        backgroundColor: '#05CD99',
                    },
                    {
                        label: 'Contas a Pagar',
                        data: res.contas_pagar,
                        tension: 0.3,
                        borderColor: '#FF869C',
                        backgroundColor: '#FF869C',
                    }
                ]
            };
            const config = {
                type: 'line',
                data: data,
                options: {
                    maintainAspectRatio: false,
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                    }
                },
            };
            const fluxo_20_dias_chart = new Chart(
                document.getElementById('fluxo_20_dias_chart'),
                config
            );
        }
    },
    mounted () {
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