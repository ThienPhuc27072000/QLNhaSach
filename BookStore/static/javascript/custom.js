$(document).ready(function() {
// $('.navbar-toggler').click(function() {
//     $('.navbar-collapse').slideToggle();
//    });

  $("#owl-demo").owlCarousel({
 	  navigation : true, // Show next and prev buttons
      slideSpeed : 300,
      paginationSpeed : 400,
      singleItem:true,
      items : 1,
      autoPlay: 3000,
       loop: true,
  });

  $("#testimonal").owlCarousel({ 
  		 navigation : true, // Show next and prev buttons
      slideSpeed : 300,
      paginationSpeed : 400,
      singleItem:true,
      items : 1,
      autoPlay: 3000,
       loop: true,
  });

});

$(document).ready(function() {
            $(".goToTop > a").hide();
            $(".goToTop > a").click(function() {
                $("html, body").animate({scrollTop:0}, 500);
            });
            $(window).scroll(function() {
                if( $("html, body").scrollTop() > 200)
                 {
                    $(".goToTop > a").fadeIn("slow");
                 }
                 else
                 {
                    $(".goToTop > a").fadeOut("slow");
                 }
            });
        });

