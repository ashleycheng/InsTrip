import * as Vue from 'vue';
import * as VueRouter from 'vue-router';

const routes = [
    {path:'/', name: 'home', component:home},
    {path:'/country/:country_name', name: 'country', component:country},
    {path:'/city/:city_name', name: 'city', component:city},
  ];
  
  const router = VueRouter.createRouter({
    //use hash character (#) before the actual URL, so the page could be refreshed  
    history: VueRouter.createWebHashHistory(), 
    routes,

  });

const app = Vue.createApp({})
app.use(router)
app.mount('#app')
