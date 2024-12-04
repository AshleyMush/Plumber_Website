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



    document.addEventListener('DOMContentLoaded', function () {
        // Initialize Unique Swiper for Accreditations
        new Swiper('.unique-accreditations-swiper', {
            loop: true, // Infinite loop
            speed: 30000, // Speed for continuous smooth scrolling
            slidesPerView: 5, // Display five slides at a time
            spaceBetween: 20, // Space between slides
            freeMode: true, // Enable free mode for continuous scrolling
            autoplay: {
                delay: 0, // No delay for continuous scroll
                disableOnInteraction: false, // Keep autoplay active after interaction
            },
            breakpoints: {
                320: {
                    slidesPerView: 2,
                    spaceBetween: 10,
                },
                768: {
                    slidesPerView: 3,
                    spaceBetween: 15,
                },
                1024: {
                    slidesPerView: 5,
                    spaceBetween: 20,
                },
            },
        });
    });
 // Dark Mode Toggle Functionality
        document.getElementById('toggle-dark-mode').addEventListener('click', () => {
            const body = document.getElementById('theme-body');
            const isDarkMode = body.classList.contains('bg-dark');

            if (isDarkMode) {
                // Switch to light mode
                body.classList.remove('bg-dark', 'text-light');
                body.classList.add('bg-light', 'text-dark');
            } else {
                // Switch to dark mode
                body.classList.remove('bg-light', 'text-dark');
                body.classList.add('bg-dark', 'text-light');
            }
        });