document.addEventListener('DOMContentLoaded', function () {
  // Ensure Swiper exists
  if (typeof Swiper !== 'undefined') {
    // Testimonials Swiper
    const testimonialsSwiper = new Swiper('.testimonials-swiper', {
      loop: true, // Infinite loop
      speed: 4000, // Smooth transition speed
      autoplay: {
        delay: 5000, // Autoplay delay
        disableOnInteraction: false, // Keep autoplay active after interaction
      },
      slidesPerView: 1, // Show one slide at a time
      pagination: {
        el: '.swiper-pagination',
        clickable: true,
      },
    });
  } else {
    console.error('Swiper is not defined.');
  }
});
