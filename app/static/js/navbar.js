const painelComercial = {
    delimiters: ['[[',']]'],
    data () {
        return {
            total_vendas: '',
        }
    },
    methods: {
        async total_vendas () {
            const req = await fetch('/total_de_vendas_por_mes/', {method: 'GET'})
            const res = await req.json()

        }
    }
}

Vue.createApp(painelComercial).mount('#app')