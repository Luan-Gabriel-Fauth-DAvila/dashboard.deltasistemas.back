const login ={
    delimiters: ['[[',']]'],
    data () {
        return {
            username: '',
            password: '',
            remember: '',
            next: '',
            hostBackEnd: '',
            hostFrontEnd: '',
        }
    },
    methods: {
    //     async login (e) {
    //         e.preventDefault()
    //         let data = {
    //             username: this.username,
    //             password: this.password
    //         }
    //         const req = await fetch(this.hostBackEnd+'/jwt/create/',{
    //             method: 'POST',
    //             body: JSON.stringify(data),
    //             headers: {'Content-Type': 'application/json'}
    //         })
    //         const res = await req.json()
            
    //         if (req.status == '200') {
    //             sessionStorage.setItem('access', res.access)
    //             sessionStorage.setItem('refresh', res.refresh)
    //             sessionStorage.setItem('username', this.username)
    //             window.location.href = (this.hostFrontEnd+'/painel/comercial/')
    //         }
    //     },
    //     async verifyLogin () {
    //         try {
    //             var token = sessionStorage.getItem('access')
    //         }catch (e) {
    //             console.log(e.message)
    //             var token = ''
    //         }
    //         let data = {
    //             token: token
    //         }
    //         const req = await fetch(this.hostBackEnd+'/jwt/verify/',{
    //             method: 'POST',
    //             body: JSON.stringify(data),
    //             headers: {'Content-Type': 'application/json'}
    //         })
    //         const res = await req.json()
            
    //         if (req.status == '200') {
    //             let data = {
    //                 token: sessionStorage.getItem('refresh')
    //             }
    //             const req = await fetch(this.hostBackEnd+'/jwt/verify/',{
    //                 method: 'POST',
    //                 body: JSON.stringify(data),
    //                 headers: {'Content-Type': 'application/json'}
    //             })
    //             window.location.href = (this.hostFrontEnd+'/painel/comercial/')
    //         }
    //     }
    },
    created () {
        // this.verifyLogin()
    }
}

Vue.createApp(login).mount('#app')