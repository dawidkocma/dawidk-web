window.addEventListener('DOMContentLoaded', () => {
    let scrollPos = 0;
    const mainNav = document.getElementById('mainNav');
    const headerHeight = mainNav.clientHeight;
    window.addEventListener('scroll', function() {
        const currentTop = document.body.getBoundingClientRect().top * -1;
        if ( currentTop < scrollPos) {
            // Scrolling Up
            if (currentTop > 0 && mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-visible');
            } else {
                console.log(123);
                mainNav.classList.remove('is-visible', 'is-fixed');
            }
        } else {
            // Scrolling Down
            mainNav.classList.remove(['is-visible']);
            if (currentTop > headerHeight && !mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-fixed');
            }
        }
        scrollPos = currentTop;
    });
})

document.addEventListener('DOMContentLoaded', function () {
  // Select all progress bars
  const progressBars = document.querySelectorAll('.progress-bar');

  // Create an intersection observer
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const progressBar = entry.target;
        const value = progressBar.getAttribute('aria-valuenow');
        progressBar.style.width = value + '%';

        // Stop observing once the animation is triggered
        observer.unobserve(progressBar);
      }
    });
  }, {
    threshold: 0.5 // Trigger when 50% of the element is visible
  });

  // Observe each progress bar
  progressBars.forEach(bar => {
    observer.observe(bar);
  });
});


// About Section Cursor

document.addEventListener('DOMContentLoaded', function() {
  var typed = new Typed('#typed', {
    strings: ["Developer","Designer", "Dog Dad","AI Engineer", "Freelancer", "Photographer",],
    typeSpeed: 100, // Speed of typing
    backSpeed: 50, // Speed of backspacing
    backDelay: 1000, // Time before backspacing
    startDelay: 500, // Time before typing starts
    loop: true, // Loop the typing animation
    showCursor: true,
    cursorChar: '|', // Customize cursor character
    autoInsertCss: true
  });
});

// Home Section Cursor
//
// document.addEventListener('DOMContentLoaded', function() {
//   var typed = new Typed('#typed_home', {
//     strings: ["Thoughts","Dreams", "Discoveries", "Wonders",],
//     typeSpeed: 100, // Speed of typing
//     backSpeed: 50, // Speed of backspacing
//     backDelay: 1000, // Time before backspacing
//     startDelay: 500, // Time before typing starts
//     loop: true, // Loop the typing animation
//     showCursor: true,
//     cursorChar: '|', // Customize cursor character
//     autoInsertCss: true
//   });
// });

document.addEventListener('DOMContentLoaded', function() {
  var typed = new Typed('#typed_home', {
    strings: ["Projects", "Articles", "Designs", "Creations"],
    typeSpeed: 100,
    backSpeed: 50,
    backDelay: 1000,
    startDelay: 500,
    loop: true,
    showCursor: true,
    cursorChar: '|',
    autoInsertCss: true
  });
});
