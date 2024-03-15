<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TripThrive</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
  <link rel="stylesheet" href="{{ url_for('static', filename='review_css.css') }}">
  <link rel="stylesheet" href="{{ url_for('static', filename='swiper-bundle.min.css') }}">
  <!-- Bootstrap Link -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
    integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
  <!-- Bootstrap Link -->
  
  <!-- Bootstrap JavaScript Link -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"
   integrity="sha384-rbs5GBFzTBxCefAqWtDANhTxM4l4xj9iaVbIG63S9yFjroj3sF1dQbZCCmFC6jPx" crossorigin="anonymous"></script>
  <!-- Bootstrap JavaScript Link -->

  <!-- Fontawesome cdn -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css"
    integrity="sha512-z3gLpd7yknf1YoNbCzqRKc4qyor8gaKU1qmn+CShxbuBusANI9QpRohGBreCFkKxLhei6S9CQXFEbbKuqLg0DA=="
    crossorigin="anonymous" referrerpolicy="no-referrer" />
  <!-- Fontawesome cdn -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@500&display=swap" rel="stylesheet">

  {% if username %}
  <script>
    function handleGeolocationPermission() {
      if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(
              position => {
                  const username = sessionStorage.getItem('username');
                  const { latitude, longitude } = position.coords;
  
                  // Send data to Flask app to store in MongoDB
                  fetch('/store_location', {
                      method: 'POST',
                      headers: {
                          'Content-Type': 'application/json',
                      },
                      body: JSON.stringify({ username, latitude, longitude }),
                  })
                  .then(response => response.json())
                  .then(data => {
                      
                      console.log(data);
  
                      // Reverse geocoding using Nominatim
                      fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`, {
                          method: 'GET',
                      })
                      .then(response => response.json())
                      .then(addressData => {
                          console.log(addressData);
  
                          // Make another post request to store the address in MongoDB
                          fetch('/store_address', {
                              method: 'POST',
                              headers: {
                                  'Content-Type': 'application/json',
                              },
                              body: JSON.stringify({ username, address: addressData.display_name }),
                          })
                          .then(response => response.json())
                          .then(data => console.log(data))
                          .catch(error => console.error('Error storing address:', error));
                      })
                      .catch(error => console.error('Error reverse geocoding:', error));
                  })
                  .catch(error => console.error('Error storing location:', error));
              },
              error => {
                  console.error('Geolocation error:', error.message);
              }
          );
      } else {
          console.log('Geolocation is not supported by this browser.');
      }
  }
    // Call the function with a delay on page load
    document.addEventListener('DOMContentLoaded', function () {
        setTimeout(handleGeolocationPermission, 1000); // Delay in milliseconds (adjust as needed)
    });
</script>
{% endif %}
<script>window.embeddedChatbotConfig = {
  chatbotId: "m14tdN_YXri9YwENNda66",
  domain: "www.chatbase.co"
  }
  </script>
  <script
  src="https://www.chatbase.co/embed.min.js"
  chatbotId="m14tdN_YXri9YwENNda66"
  domain="www.chatbase.co"
  defer>
</script>
  
</head>

<body>
    
  
  <!-- Navbar Start -->
  <nav class="navbar navbar-expand-lg ">
    <div class="container" id="container">
      {% if 'username' in session %}
      <img src="https://raw.githubusercontent.com/Mallika2002/OCTANET_JUNE/main/logo_1-removebg%20(1)-Photoroom.jpg" class ="e1" width="120px" height="50px" alt="TripThriveLogo">
      {% else %}
      <img src="https://raw.githubusercontent.com/Mallika2002/OCTANET_JUNE/main/logo_1-removebg%20(1)-Photoroom.jpg" class ="e" width="150px" height="50px" alt="TripThriveLogo">
      {% endif %} 

      <a class="navbar-brand" href="" id="logo"><span>T</span>rip<span>T</span>hrive</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation" onclick="handleNavbarToggle()">
        <span class="fa-solid fa-bars"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          
          {% if 'username' in session %}
          <li class="nav-item">
            <a class="nav-link active" href="{{ url_for('user_page', username=username) }}">Home</a>
          </li>
          
          <li class="nav-item">
          <a class="nav-link" href="{{ url_for('book') }}">Book</a>
          </li>
         {% else %}
         <li class="nav-item">
          <a class="nav-link active" href="{{url_for('index')}}">Home</a>
        </li>
         <li class="nav-item">
          <a class="nav-link" href="{{ url_for('book') }}">Book</a>
         </li>  
         {% endif %}        
          <li class="nav-item">
            <a class="nav-link" href="#packages">Packages</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#gallery">Gallery</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#services">Services</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#reviews">Reviews</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#about">About us</a>
          </li>
        </ul>
        <form class="d-flex" id="f">
          <input class="form-control me-2" type="text" id = "y" placeholder="Search">
          <button class="btn btn-primary me-2" type="button" id="bv"><i class="fa fa-search"></i></button>
           {% if username %}
          <div class="dropdown">
            <button class="btn btn-primary me-2" type="button" id="bu"><i class='far fa-user-circle' style='font-size:24px;'></i></button>
            <div class="dropdown-content">
            <a href="{{ url_for('account_details') }}" target="__blank">Account</a>
            <a href="{{url_for('trip_details')}}"target="__blank">My Trips</a>
            <a href="{{ url_for('logout') }}">Logout</a>
            </div>
          </div>
          {% else %}<button class="btn btn-primary" id="b1" type="button" onclick="window.location.href='{{ url_for('signup') }}';">Sign Up</button>
          <button class="btn btn-primary" id="b" type="button" onclick="window.location.href='{{ url_for('login') }}';">Login</button>
          
          
          {% endif %}
        </form>
      </div>
    </div>
  </nav>


  <script>
    function handleNavbarToggle() {
      const navbarCollapse = document.querySelector('#navbarNav');
      navbarCollapse.classList.toggle('show');
    }
  </script>
  <!-- Navbar End-->

  <!-- Home section start-->
  <div class="home">
    <div class="content">
      <h5>Welcome to <span id="span1">T</span><span id="span2">rip</span><span id="span1">T</span><span id="span2">hrive</span></h5>
      <h1>Visit <span class="changecontent"></span></h1>
      <p>Granting wishes with AI travel magic</p>
      <!--<a href="#book">Book Place</a>-->
      <a href="{{ url_for('book') }}" style="background: #fff;
                        color: #000;
                        padding: 18px 20px;
                        margin-bottom: 1200px; 
                        display: inline-block;
                        border-radius: 200px;
                        text-decoration: none;
                        font-size: 25px;">Plan A Tour</a>
    </div>
  </div>
  <!-- Home section end-->


 
<!-- Geolocation Button Start
<div class="geolocation-container">
  <button id="geoBtn" onclick="handlePermission()">Allow Geolocation</button>
  
</div>
     Geolocation Button End -->


 <!-- Packages section -->
  <section class="packages" id="packages">
    <div class="container">
      <div class="main-txt">
        <h1><span>P</span>ackages</h1>
      </div>
      <div class="cards">
        <div class="card card1" id="card2">
          <div class="contain" id="container2">
            <img src="{{ url_for('static', filename='images/img7.jpg') }}" class="logo" alt="">
          </div>
          <div class="details">
            <h3>Indonesia</h3>
            <p class="o">Bali Indonesia. Also known as the Land of the Gods, Bali appeals through its sheer natural beauty of
              looming volcanoes and lush terraced rice fields that exude peace and serenity. It is also famous for
              surfers' paradise!</p>
            <div class="star">
              <i class="fa-solid fa-star checked"></i>
              <i class="fa-solid fa-star checked"></i>
              <i class="fa-solid fa-star checked"></i>
              <i class="fa-solid fa-star checked"></i>
              <i class="fa-solid fa-star checked"></i>
            </div>
            <h6>Price: <strong>$7000</strong></h6>
            <a href="https://www.makemytrip.com/flight/search?itinerary=VTZ-CGK-18/03/2024&tripType=O&paxType=A-1_C-0_I-0&intl=true&cabinClass=E&ccde=IN&lang=eng" target="_blank">Book Now</a>
          </div>

        </div>
        <div class="card card2" id="card2">
          <div class="contain" id="container2">
            <img src="{{ url_for('static', filename='images/img8.jpg') }}" class="logo" alt="">

          </div>
          <div class="details">
            <h3>Greece</h3>
            <p class="p"> Safe Place for Holidays. Greece is considered one of the safest countries in the world. Regardless of
              time, you always feel safe in Greece. Travelers are, however, advised to use the normal precautions as
              they would in any other European country</p>
            <div class="star">
              <i class="fa-solid fa-star checked"></i>
              <i class="fa-solid fa-star checked"></i>
              <i class="fa-solid fa-star checked"></i>
              <i class="fa-solid fa-star "></i>
              <i class="fa-solid fa-star "></i>
            </div>
            <h6 class="h">Price: <strong>$5000</strong></h6>
            <a href="https://www.makemytrip.com/flight/search?itinerary=VTZ-ATH-18/03/2024&tripType=O&paxType=A-1_C-0_I-0&intl=true&cabinClass=E&ccde=IN&lang=eng" target="_blank">Book Now</a>
          </div>

        </div>
        <div class="card card3" id="card2">
          <div class="contain" id="container2">
            <img src="{{ url_for('static', filename='images/img5.jpg') }}" class="logo" alt="">

          </div>
          <div class="details">
            <h3>United States</h3>
            <p>Often defined as the cultural, financial, media, and entertainment capital of the world, it is one of the
              most expensive real estate in the world. Manhattan hosts the United Nations Headquarters, Wall Street,
              several media conglomerates, Central Park, Broadway, and many famous buildings.</p>
            <div class="star">
              <i class="fa-solid fa-star checked"></i>
              <i class="fa-solid fa-star checked"></i>
              <i class="fa-solid fa-star checked"></i>
              <i class="fa-solid fa-star checked"></i>
              <i class="fa-solid fa-star  checked"></i>
            </div>
            <h6>Price: <strong>$4000</strong></h6>
            <a href="https://www.makemytrip.com/flight/search?itinerary=VTZ-LGA-18/03/2024&tripType=O&paxType=A-1_C-0_I-0&intl=true&cabinClass=E&ccde=IN&lang=eng" target="_blank">Book Now</a>
          </div>

        </div>
        <div class="card card4" id="card2">
          <div class="contain" id="container2">
            <img src="{{ url_for('static', filename='images/img6.jpg') }}" class="logo" alt="">

          </div>
          <div class="details">
            <h3>Japan</h3>
            <p> Japan has 21 World Heritage Sites, including Himeji Castle, Historic Monuments of Ancient Kyoto and
              Nara. Popular foreigner attractions include Tokyo and Hiroshima, Mount Fuji, ski resorts such as Niseko in
              Hokkaido, Okinawa, riding the Shinkansen and taking advantage of Japan's hotel and hotspring network.</p>
            <div class="star">
              <i class="fa-solid fa-star checked"></i>
              <i class="fa-solid fa-star checked"></i>
              <i class="fa-solid fa-star checked"></i>
              <i class="fa-solid fa-star checked"></i>
              <i class="fa-solid fa-star "></i>
            </div>
            <h6>Price: <strong>$5500</strong></h6>
            <a href="https://www.makemytrip.com/flight/search?itinerary=VTZ-NGO-18/03/2024&tripType=O&paxType=A-1_C-0_I-0&intl=true&cabinClass=E&ccde=IN&lang=eng" target="_blank">Book Now</a>
          </div>

        </div>
        <div class="card card5" id="card2">
          <div class="contain" id="container2">
            <img src="{{ url_for('static', filename='images/img4.jpg') }}" class="logo" alt="">
          </div>
          <div class="details">
            <h3 class="k">United knigdom</h3>
            <p>When it comes to one of the top tourist destinations in the world, the United Kingdom is never behind.
              There are plenty of amazing things to see and do in northwestern Europe's island nation, whether it's
              iconic landmarks, breathtaking coastal views, world-class restaurants or international music festivals.
            </p>
            <div class="star">
              <i class="fa-solid fa-star checked"></i>
              <i class="fa-solid fa-star checked"></i>
              <i class="fa-solid fa-star checked"></i>
              <i class="fa-solid fa-star checked"></i>
              <i class="fa-solid fa-star "></i>
            </div>
            <h6>Price: <strong>$5700</strong></h6>
            <a href="https://www.makemytrip.com/flight/search?itinerary=VTZ-LON-18/03/2024&tripType=O&paxType=A-1_C-0_I-0&intl=true&cabinClass=E&ccde=IN&lang=eng" target="_blank">Book Now</a>
          </div>
        </div>
        <div class="card card6" id="card2">
          <div class="contain" id="container2">
            <img src="{{ url_for('static', filename='images/img3.jpg') }}" class="logo" alt="">

          </div>
          <div class="details">
            <h3>France</h3>
            <p class="f">Paris is one of the most distinctive cities in the world. It is a city has its own character, especially
              because it was accompanied by beauty, art, culture and revolution. It embraced the French Revolution which
              has made a very significant shift in the course of history.</p>
            <div class="star">
              <i class="fa-solid fa-star checked"></i>
              <i class="fa-solid fa-star checked"></i>
              <i class="fa-solid fa-star checked"></i>
              <i class="fa-solid fa-star "></i>
              <i class="fa-solid fa-star "></i>
            </div>
            <h6>Price: <strong>$6000</strong></h6>
            <a href="https://www.makemytrip.com/flight/search?itinerary=VTZ-PAR-18/03/2024&tripType=O&paxType=A-1_C-0_I-0&intl=true&cabinClass=E&ccde=IN&lang=eng" target="_blank">Book Now</a>
          </div>

        </div>
      </div>
    </div>
    </div>
  </section>
  <!-- Packages section -->

  <!-- section Gellery -->
  <section class="gallery" id="gallery">
    <div class="container" id="con">
      <div class="main-txt">
        <h1><span>G</span>allery</h1>
      </div>
      <div class="cards">
        <div class="card">
          <a href="https://www.schlossoberhofen.ch/de/home" target="_blank">
            <img src="{{ url_for('static', filename='images/img9.jpg') }}" class="logo" alt="" height="200px">
          </a>
        </div>        
        <div class="card">
          <a href="https://www.hellotravel.com/switzerland/bern-bridge" target="_blank">
          <img src="{{ url_for('static', filename='images/img10.jpg') }}" class="logo" alt="" height="200px">
          </a>
        </div>
        <div class="card">
          <a href="https://book.st-marks-basilica.com/book/21703/select/?_gl=1%2A120djn6%2A_ga%2AMzcxNTcxNjgyLjE3MDgwNDY0Nzc.%2A_ga_Y45PC9R73C%2AMTcwODA0NjQ3Ni4xLjEuMTcwODA0NjUyMy4xMy4wLjA.&cookieBanner=false&date=2024-02-16" target="_blank">
          <img src="{{ url_for('static', filename='images/img11.jpg') }}" class="logo" alt="" height="200px">
          </a>
        </div>
        <div class="card">
          <a href="https://www.expedia.com/Porto-Hotels-Eurostars-Heroismo.h11910759.Hotel-Information" target="_blank">
          <img src="{{ url_for('static', filename='images/img12.jpg') }}" class="logo" alt="" height="200px">
          </a>
        </div>
        <div class="card">
          <img src="{{ url_for('static', filename='images/img13.jpg') }}" class="logo" alt="" height="200px">
        </div>
        <div class="card">
          <a href="https://www.royalparks.org.uk/visit/parks/st-jamess-park" target="_blank">
          <img src="{{ url_for('static', filename='images/img14.jpg') }}" class="logo" alt="" height="200px">
          </a>
        </div>
        <div class="card">
          <a href="https://www.atlasobscura.com/places/hyangwonjeong-pavilion" target="_blank">
          <img src="{{ url_for('static', filename='images/img15.jpg') }}" class="logo" alt="" height="200px">
          </a>
        </div>
        <div class="card">
          <a href="https://english.visitkorea.or.kr/svc/contents/contentsView.do?menuSn=351&vcontsId=87740" target="_blank">
          <img src="{{ url_for('static', filename='images/img16.jpg') }}" class="logo" alt="" height="200px">
          </a>
        </div>
        <div class="card">
          <a href="https://english.visitkorea.or.kr/svc/contents/contentsView.do?menuSn=351&vcontsId=87740" target="_blank">
          <img src="{{ url_for('static', filename='images/img17.jpg') }}" class="logo" alt="" height="200px">
          </a>
        </div>
        <div class="card">
          <a href="https://www.nagoyajo.city.nagoya.jp/en/" target="_blank">
          <img src="{{ url_for('static', filename='images/img18.jpg') }}" class="logo" alt="" height="200px">
          </a>
        </div>
        <div class="card">
          <a href="https://www.japan.travel/en/spot/1365/" target="_blank">
          <img src="{{ url_for('static', filename='images/img19.jpg') }}" class="logo" alt="" height="200px">
          </a>
        </div>
        <div class="card">
          <a href="https://livejapan.com/en/in-kansai/in-pref-kyoto/in-arashiyama_uzumasa/article-a2000690/" target="_blank">
          <img src="{{ url_for('static', filename='images/img20.jpg') }}" class="logo" alt="" height="200px">
          </a>
        </div>
        <div class="card">
          <a href="https://www.toureiffel.paris/en" target="_blank">
          <img src="{{ url_for('static', filename='images/img21.jpg') }}" class="logo" alt="" height="200px">
          </a>
        </div>
        <div class="card">
          <a href="https://www.tripadvisor.in/Tourism-g187073-Colmar_Haut_Rhin_Grand_Est-Vacations.html" target="_blank">
          <img src="{{ url_for('static', filename='images/img22.jpg') }}" class="logo" alt="" height="200px">
          </a>
        </div>
        <div class="card">
          <a href="https://www.viator.com/Santorini-tours/Night-Tours/d959-g12-c96" target="_blank">
          <img src="{{ url_for('static', filename='images/img23.jpg') }}" class="logo" alt="" height="200px">
          </a>
        </div>
        <!--<div class="card">
          <img src="{{ url_for('static', filename='images/img24.jpg') }}" class="logo" alt="" height="200px">
        </div>-->
      </div>
    </div>
  </section>
  <!-- section Gellery -->



  <!-- Services section -->
  <section class="services" id="services">
    <div class="container">
      <div class="main-txt">
        <h1><span>S</span>ervices</h1>
      </div>
      <div class="cards">
        <div class="card" id="card2">
          <i class="fas fa-hotel"></i>
          <h3>Affordable hotel</h3>
          <p>We provide you the top rated Hotel recommendations with affordable price and with best comfort.</p>

        </div>


        <div class="card " id="card2">
          <i class="fas fa-utensils"></i>
          <h3>Dining</h3>
          <p>We provide you the best Food recommendations with affordable price and with best comfort.</p>

        </div>




        <div class="card" id="card2">
          <i class="fas fa-bullhorn"></i>
          <h3>Safety Guide</h3>
          <p>We also provide you safety precautionary measures that provides you the best security.
          </p>
        </div>
        <div class="card " id="card2">
          <i class="fas fa-globe-asia"></i>
          <h3>Around the World</h3>
          <p>We provide accurate trip itinerary all around the world for specified number of days within budget.</p>

        </div>
        <div class="card" id="card2">
          <i class="fas fa-plane"></i>
          <h3>Fastest Travel</h3>
          <p>We provide you the best and affordable transportation options within your give period of time.</p>

        </div>
        <div class="card card7" id="card2">
          <i class="fas fa-hiking"></i>
          <h3>Adventures</h3>
          <p>We support your thirst for adventures, offering the best itineraries, ensuring unforgettable experiences.</p>

        </div>
      </div>
    </div>
  </section>



  <!-- Services section -->



  <!-- Booking section 
  <section class="book" id="book">
    <div class="container">

      <div class="main-text">
        <h1><span>B</span>ook</h1>
      </div>
      <div class="row">
        <div class="col-md-6 py-3 py-md-0">
          <div class="card">
            <img src="{{ url_for('static', filename='images/img2.jpg') }}" class="logo" alt="" height="200px">
          </div>
        </div>
        <div class="col-md-6 py-3 py-md-0">
          <form action="#">

            <input type="text" class="form-control" placeholder="Where To" required><br>
            <input type="text" class="form-control" placeholder="How many" required><br>
            <input type="date" class="form-control" placeholder="Arrivals" required><br>
            <input type="date" class="form-control" placeholder="Leaving" required><br>
            <textarea class="form-control" rows="5" name="text" placeholder="Enter your Name & Details"></textarea><br>
            <input type="submit" value="Book Now" class="submit" required>
          </form>
        </div>
      </div>
    </div>
  </section>
  Booking section -->

  <section class="reviews" id="reviews">
    <div class="main-txt">
      <h1><span>R</span>eviews</h1>
    </div>
  <div class="slide-container swiper">
    <div class="slide-content">
        <div class="card-wrapper swiper-wrapper">
            <div class="card swiper-slide">
                
                    <div class="image-content">
                        <span class="overlay"></span>

                            <div class="card-image">
                              <img src="{{ url_for('static', filename='images/review_pics/img4.jpg') }}" alt=""  class="card-img">
                            </div>
                    </div>
                    <div class="card-content">
                        <h2 class="name"><b>Anakshi Sinha</b></h2>
                        <p class="description">Along with my friends i went to Bali . It was such a pleasant journey , this webiste helped me a lot regarding the day to day planning along with the budget.</p>
                    </div>
            </div>
            <div class="card swiper-slide">
                
                <div class="image-content">
                    <span class="overlay"></span>

                        <div class="card-image">
                          <img src="{{ url_for('static', filename='images/review_pics/img1.jpg') }}" alt=""  class="card-img">
                        </div>
                </div>
                <div class="card-content">
                    <h2 class="name"><b>Somesh Roy</b></h2>
                    <p class="description">Great experience in Dubia along with my family.Very good website.</p>
                </div>
        </div>
        <div class="card swiper-slide">
                
            <div class="image-content">
                <span class="overlay"></span>

                    <div class="card-image">
                      <img src="{{ url_for('static', filename='images/review_pics/img2.jpg') }}" alt=""  class="card-img">
                    </div>
            </div>
            <div class="card-content">
                <h2 class="name"><b>Reshma</b> </h2>
                <p class="description">Absolutely love this AI trip planner! Customized itineraries for any destination, days, and budget. Takes the stress out of travel planning. Five stars!"</p>
            </div>
    </div>
    <div class="card swiper-slide">
                
        <div class="image-content">
            <span class="overlay"></span>

                <div class="card-image">
                  <img src="{{ url_for('static', filename='images/review_pics/img3.jpg') }}" alt=""  class="card-img">
                </div>
        </div>
        <div class="card-content">
            <h2 class="name"><b>Sinhak</b> </h2>
            <p class="description">Exceptional service! The AI-based trip planner is a wizard in crafting perfect itineraries. Delivered an amazing travel experience, from planning to execution. Impressed!</p>
        </div>
</div>
<div class="card swiper-slide">
                
    <div class="image-content">
        <span class="overlay"></span>

            <div class="card-image">
              <img src="{{ url_for('static', filename='images/review_pics/img5.jpg') }}" alt=""  class="card-img">
            </div>
    </div>
    <div class="card-content">
        <h2 class="name"><b>Tanya Merchant</b></h2>
        <p class="description">This website helped me a lot regarding the planning of my trip within budget . This saved me a lot of time and expenses. </p>
    </div>
</div>
<div class="card  swiper-slide">
                
    <div class="image-content">
        <span class="overlay"></span>

            <div class="card-image">
                  <img src="{{ url_for('static', filename='images/review_pics/img7.jpg') }}" alt=""  class="card-img">
            </div>
    </div>
    <div class="card-content">
        <h2 class="name"><b>Prudvi S</b></h2>
        <p class="description">Impressive website; highly recommended.</p>
    </div>
</div>
        </div>
    </div>
    <div class="swiper-button-next swiper-navBtn"></div>
    <div class="swiper-button-prev swiper-navBtn"></div>
    <div class="swiper-pagination"></div>
   </div>
  </section>

   <!-- About section -->
   <section class="about" id="about">
    <div class="container" id="coo">
      <div class="main-txt">
        <h1><span>A</span>bout <span>U</span>s</h1>
      </div>
      <div class="content-section">

        <div class="content">
          <h2><strong>Hello, thanks for visiting our website.
            </strong></h2>
          <p>TripThrive, the AI-based trip planner, revolutionizes travel with personalized itineraries tailored to your destination, days, and budget. Seamlessly blending technology and wanderlust, it crafts unforgettable adventures, recommends affordable accommodations and dining, ensuring a stress-free journey. Elevate your travel experience with TripThrive – your virtual guide to exploration.

          </p>
        </div>
      </div>
      <div class="image-section">
        <img src="{{ url_for('static', filename='images/img25.jpg') }}" class="logo" alt="" height="200px">
      </div>
    </div>
  </section>
  <!-- About section -->

  <script src="{{ url_for('static', filename='script_login.js') }}"></script>
  <script src="{{ url_for('static', filename='script_signup.js') }}"></script>
  <script src="../static/swiper-bundle.min.js"></script>
  <script src="../static/review_script.js"></script>
  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script>
$(document).ready(function(){
    $("#bv").click(function(){
        var searchQuery = $("#y").val();
        $.ajax({
            type: "GET",
            url: "/plan",
            data: { query: searchQuery },
            success: function(response){
                // Assuming response contains the URL to your Streamlit application
               console.log('hii')
            },
            error: function(xhr, status, error){
                console.error("Error:", error);
            }
        });
    });
});
</script>

</body>

</html>
  
</head>

</html>
