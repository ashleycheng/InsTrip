const country={template:`
<header id="cover1" class="bg-img" :style="{ 'background': 'url(/frontend/img/'+ cities.country_name +'.jpg)' }">
        
<div class="container p-4 d-flex">
    <div class="row align-items-center">
        <article class="article">
            <h1 class="display-2 text-white" ><strong>{{ cities.country_name_ch }}</strong></h1>  
            <h2 class="text-white">熱門旅遊城市推薦</h2>
            
        </article> 
    </div>

</div>
</header>


<section id="city">
<div class="container my-4">

    <h2 class="d-inline-block my-2 mx-3">人氣 Top 5  </h2>
    <a :href="'/analysis/'+cities.country_name" ><button type="button" class="btn btn-outline-primary my-2"><i class="fa-solid fa-wand-magic-sparkles"></i> 行程分析</button></a>
    <p class="text-muted mb-4 mx-3">探索 Instagram 最受歡迎的旅遊城市與打卡地點</p>
    <!-- start event block -->
    <div v-for="city in cities.city" class="city-row row align-items-center event-block no-gutters margin-40px-bottom">
        <div class="col-lg-4 col-sm-12">
            <div class="position-relative">
                <img class="img-fluid" :src="city.image" alt="">
            </div>
        </div>
        <div class="col-lg-7 col-sm-12">
            <div class="padding-60px-lr md-padding-50px-lr sm-padding-30px-all xs-padding-25px-all">
                <h5>#{{ city.rank }}.</h5>
                <h5 class="margin-15px-bottom md-margin-10px-bottom font-size22 md-font-size20 xs-font-size18 font-weight-500">{{ city.city_name_ch }}</h5>
                <div class="row ">
                <i class="col-1 text-end fs-6 fa-solid fa-wand-magic-sparkles" style="color:#566573"></i>
                <p class="col-11 px-0">{{ city.description }}....</p>
                </div>
                <!-- <a class="butn small margin-10px-top md-no-margin-top" href="event-details.html">Read More <i class="fas fa-long-arrow-alt-right margin-10px-left"></i></a> -->
                <div class="mt-2">

                </div>
            </div>
        </div>
        <router-link :to="{ name: 'city', params: {  city_id: '1', city_name: city.city_name }}" class="stretched-link" ></router-link>
    </div>
    <!-- end event block -->
    <p class="text-center small my-5" style="font-size: 10px;color:#566573;"><i class="col-1 text-end fs-6 fa-solid fa-wand-magic-sparkles" style="color:#566573;"></i> Power by ChatGPT</p>
   
</div>
</section>

`
,
data(){
    return{
        cities:[],
    }
},

methods:{
    topCityData(){
        const country_name = this.$route.params.country_name;
        axios.get(variables.API_URL+"top/city/"+country_name)
        .then((response)=>{
            this.cities=response.data;
            // console.log(response.data);
        }).catch(response => {
            alert('wrong');
          })
  
    }
},
mounted: function() {
    this.topCityData();
   },
}