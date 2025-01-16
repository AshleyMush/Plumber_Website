document.addEventListener('DOMContentLoaded', function () {
    // Swiper Initialization
    if (typeof Swiper !== 'undefined') {
        // Testimonials Swiper
        new Swiper('.testimonials-swiper', {
            loop: true,
            speed: 4000,
            autoplay: { delay: 5000, disableOnInteraction: false },
            slidesPerView: 1,
            pagination: { el: '.swiper-pagination', clickable: true },
        });

        // Accreditations Swiper
        new Swiper('.unique-accreditations-swiper', {
            loop: true,
            speed: 30000,
            slidesPerView: 5,
            spaceBetween: 20,
            freeMode: true,
            autoplay: { delay: 0, disableOnInteraction: false },
            breakpoints: {
                320: { slidesPerView: 2, spaceBetween: 10 },
                768: { slidesPerView: 3, spaceBetween: 15 },
                1024: { slidesPerView: 5, spaceBetween: 20 },
            },
        });

        // Gallery Swiper
        // Swiper Initialization for Gallery
new Swiper('.gallery-swiper', {
  loop: true,
  slidesPerView: 3,
  spaceBetween: 20,
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },
  pagination: { el: '.swiper-pagination', clickable: true },
  breakpoints: {
    320: { slidesPerView: 1, spaceBetween: 10 },
    768: { slidesPerView: 2, spaceBetween: 15 },
    1024: { slidesPerView: 3, spaceBetween: 20 },
  },
});

    } else {
        console.error('Swiper is not defined.');
    }

    // Glightbox Initialization
    if (typeof GLightbox !== 'undefined') {
        GLightbox({
            selector: '.glightbox',
            touchNavigation: true,
            loop: true,
            closeButton: true,
            zoomable: true,
            keyboardNavigation: true,
            
        });
    } else {
        console.error('Glightbox is not defined.');
    }

    // Dark Mode Toggle Functionality
    const toggleDarkMode = document.getElementById('toggle-dark-mode');
    const body = document.getElementById('theme-body');

    if (toggleDarkMode && body) {
        toggleDarkMode.addEventListener('click', () => {
            const isDarkMode = body.classList.contains('bg-dark');
            body.classList.toggle('bg-dark', !isDarkMode);
            body.classList.toggle('text-light', !isDarkMode);
            body.classList.toggle('bg-light', isDarkMode);
            body.classList.toggle('text-dark', isDarkMode);
        });
    } else {
        console.error('Dark mode toggle or theme body not found.');
    }

    // TwentyTwenty Before-After Slider Initialization
    const twentytwentyContainers = document.querySelectorAll('[data-twentytwenty="true"]');

    if (twentytwentyContainers.length > 0) {
        twentytwentyContainers.forEach(container => {
            new TwentyTwenty(container, {
                default_offset_pct: 0.5, // Starting position of the slider
                orientation: 'horizontal', // Orientation of the slider
                before_label: 'Before', // Text for the "before" image
                after_label: 'After' // Text for the "after" image
            });
        });
    } else {
        console.error('No TwentyTwenty containers found.');
    }
});
