const home={template:`
<header id="cover" class="bg-img">
        
<div class="container p-4 d-flex">
    <div class="row align-items-center">
        <article class="article col-lg-6 col-md-6 order-2">
            <h1 class="display-4">InsTrip</h1>  
            <h2>Start your interested trip!</h2>
            <!-- <p class="lead">Explore popular Instagram locations, to inspire travelers to find destinations for their trips.</p> -->
            <p class="lead">安排行程的時間有限，想知道大家出國必去哪裡嗎？<br>一起發現 Instagram 的熱門景點，馬上開啟你的旅程！</p>
       
            <p><a href="#" class="btn btn-outline-light btn-sm">&darr;</a></p>
        </article> 
        <div class="col-lg-6 col-md-6 order-1 order-lg-2 order-md-2 d-sm-none d-md-block d-none d-sm-block">
            <img src="/frontend/img/ig_frame2.png" alt="sea tulule" class="img-fluid">
        </div>
    </div>

</div>
</header>

<!-- card -->
<section id="animals" class="bg-white">
<div class="container my-4">
    <h2 class="display-6">探索最多遊客造訪的國家</h2>
    <p class="lead text-muted-mb-4 px-4"> 資料來源是 Instagram 的公開貼文，統計和旅遊相關的主題標籤做排名</p>
    <div class="row g-4 px-4">
        <div class="col-md-12 col-lg-12">
            <article class="card shadow mb-4 w-50 mx-auto">
                <img src="/frontend/img/japan.jpg" alt="country pic" class="card-img-top">
                <div class="card-body card-img-overlay d-flex">
                    <h1 class="card-text  display-5 mt-auto text-white"><strong>#1 日本</strong></h1>
                    <router-link to="/country/japan" class="stretched-link" ></router-link>
                </div>
            </article>
        </div>

        <div class="col-md-12 col-lg-12">
            <article class="card shadow mb-4 w-50 mx-auto">
                <img src="/frontend/img/korea.jpg" alt="country pic" class="country-img card-img-top">
                <div class="card-body card-img-overlay d-flex">
                    <h1 class="card-text display-5 mt-auto text-white"><strong>#2 韓國</strong></h1>
                    <router-link to="/country/korea" class="stretched-link" ></router-link>
                </div>
            </article>
        </div>

        <div class="col-md-12 col-lg-12">
            <article class="card shadow mb-4 w-50 mx-auto">
                <img src="/frontend/img/vietnam.jpg" alt="country pic" class="country-img card-img-top">
                <div class="card-body card-img-overlay d-flex">
                    <h1 class="card-text display-5 mt-auto text-white"><strong>#3 越南</strong></h1>
                    <router-link to="/country/vietnam" class="stretched-link" ></router-link>
                </div>
            </article>
        </div>

        <div class="col-md-12 col-lg-12">
            <article class="card shadow mb-4 w-50 mx-auto">
                <img src="/frontend/img/thailand.jpg" alt="country pic" class="country-img card-img-top">
                <div class="card-body card-img-overlay d-flex">
                    <h1 class="card-text display-5 mt-auto text-white"><strong>#4 泰國</strong></h1>
                    <router-link to="/country/thailand" class="stretched-link" ></router-link>
                </div>
            </article>
        </div>

</div>
</section>

<!-- quote -->
<section id="quote" class="bg-info text-light p-2 my-5">
<div class="container my-2">
    <blockquote class="blockquote text-center mb-0 fs-6">
        <i class="fas fa-heart text-light"></i>
        <p class="mb-2">Travel not only broadens the mind, but also the heart.</p>
        <footer class="blockquote-footer text-light">Marco Polo</footer>
    </blockquote>
</div>

</section>
    `
}