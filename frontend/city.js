// const home={template:`<h1>This is Home</h1>`}
// import axios from 'axios';

const city={template:`
<!-- city -->
<section id="city">
    <div class="container my-5 ">
        <div class="city-img row ">
            <div class="col-6 mx-auto">
              <img class="mx-auto d-block img-fluid" :src="info.image"/>
            </div>
            <div class="col-6 mx-auto">
              <h2 class="display-5 my-3"><strong>{{ info.city_name_ch }}</strong></h2>
              <p class="text-muted mb-5">
                {{ info.description_1 }}
                <span class="collapse" id="more">
                  {{ info.description_2 }}
                </span> 
                <span>
                  <a class="link-secondary" href="#more" data-bs-toggle="collapse"><i class="fa fa-caret-down"></i>看更多</a>
                </span>
                <style>
                  .collapse.in { display: inline !important; }
                </style>
              </p>
            </div>

        </div>
    </div>

</section>

<section id="program" class="bg-light">
<div class="container my-5">
    <div class="col-11 mx-auto">
        <h2>人氣景點</h2>
        <p class="text-muted">選擇類型</p>
    </div>  
    <div class="col-11 mx-auto card">
    <div class="card-header">
        <!--   頁籤   -->
        <ul class="nav nav-pills card-header-tabs" data-bs-tabs="tabs">
            <template v-for="(loc, index) in locations">
                <li v-if="index === 0" class="nav-item">
                    <button class="btn btn-default nav-link active" id="1-tab" data-bs-toggle="tab" :data-bs-target="'#'+loc.tag" type="button"
                            role="tab" :aria-controls="loc.tag" aria-selected="true">{{ loc.tag }}</button>
                </li>
                <li v-else class="nav-item">
                    <button class="nav-link btn btn-default " id="2-tab" data-bs-toggle="tab" :data-bs-target="'#'+loc.tag" type="button" 
                            role="tab" :aria-controls="loc.tag" aria-selected="false">{{ loc.tag }}</button>
                </li>
            </template>
        </ul>
    </div>
    <!--  內容  -->
    <div class="card-body tab-content">
    <template v-for="(loc, index) in locations">

        <div :class="{ 'active' : index === 0 }" class="tab-pane" :id="loc.tag" role="tabpanel" aria-labelledby="home-tab">
   
        <template v-for="(item, index) in loc.location">
            <div class="col-12 mt-2">
                <h5>{{ item.rank }}. {{ item.location_name }}</h5>
                <p class="text-muted"><i class="fa-solid fa-location-dot"></i> {{ item.address }}
                    <a class="btn btn-secondary btn-sm" :class="'collapse-'+loc.tag+index" data-bs-toggle="collapse" :href="'#collapse-'+loc.tag+index" role="button" aria-expanded="false" :aria-controls="'collapse-'+loc.tag+index" tabindex="0"  title="Google map">地圖</a>
                    <div :id="'collapse-'+loc.tag+index" class="collapse mapouter w-100 mt-2">
                        <iframe class="gmap_iframe" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" :src="'https://maps.google.com/maps?width=800&amp;height=400&amp;hl=zh-TW&amp;q='+item.location_name+'&amp;t=&amp;z=14&amp;ie=UTF8&amp;iwloc=B&amp;output=embed'"></iframe>
                    </div>
                </p> 
            </div>
        
            <!-- carousel 卡片 -->
            <div id="slider" class="carousel slide" data-bs-interval="false">
              <div class="carousel-indicators">
                <button type="button" data-bs-target="#slider" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
                <button type="button" data-bs-target="#slider" data-bs-slide-to="1" aria-label="Slide 2"></button>
                <button type="button" data-bs-target="#slider" data-bs-slide-to="2" aria-label="Slide 3"></button>
              </div>
              <div class="carousel-inner">
                <div class="carousel-item active">
                  <!-- card  -->
                  <div class="cards-wrapper row g-4 px-4">
                    <template v-for="shortcode in item.posts">
                    <div class="card col-md-6 col-lg-3">
                      <div class="card-body">
                        <iframe width="230px" height="360px"  :src="'https://www.instagram.com/p/'+shortcode+'/embed'" frameborder="0" scrolling="no" ></iframe>
                      </div>
                    </div>
                    </template>
                  </div>
                  <!-- card end -->
                </div>

              </div>
            </div>
        
        </template>
        </div> 
      </template>
  </div>

</div>
</section>
`
,
data(){
    return{
        locations:[],
        info: {},
    }
},

methods:{
    topLocationData(){
        const city_name = this.$route.params.city_name;
        axios.get(variables.API_URL+"top/location/"+city_name)
        .then((response)=>{
            this.locations=response.data;
        }).catch(response => {
            alert('wrong');
          });
        
        axios.get(variables.API_URL+"city/"+city_name+"/info")
        .then((response)=>{
            this.info=response.data;
        }).catch(response => {
            alert('wrong');
        })
    },
},
mounted: function() {
    this.topLocationData();
   },
}
