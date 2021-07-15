// go to top
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

// selection $ event
$(document).ready(function() {
		$('.owl-carousel').owlCarousel({
		autoplay:true,
		nav:true,
		autoplayHoverPause:true,
		autoplayTime:1000,
		dotsSpeed:1000,
		smartSpeed:1000,
		slideBy:2,
		loop:true,
		margin:10,
		nav:true,
		responsive:{
			0:{
				items:1
			},
			600:{
				items:3
			},
			1000:{
				items:5
			},
		}
	});
});