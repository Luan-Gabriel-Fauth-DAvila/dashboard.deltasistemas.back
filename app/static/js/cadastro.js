const login ={
    delimiters: ['[[',']]'],
    data () {
        return {
            username: '',
            password: '',
            username: false,
        }
    },
    methods: {
        validarLogin () {
            const req = await fetch('/')
        }
    }
}

Vue.createApp(login).mount('#app')