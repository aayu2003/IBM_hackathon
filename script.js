document.addEventListener('DOMContentLoaded', () => {
    // Floating Particles Interaction
    const floatingParticles = document.querySelector('#background-overlay');

    document.addEventListener('mousemove', (e) => {
        const x = e.clientX / window.innerWidth;
        const y = e.clientY / window.innerHeight;
        floatingParticles.style.backgroundPosition = `${x * 50}% ${y * 50}%`;
    });

    // Fade-In Effects
    const faders = document.querySelectorAll('.fade-in');

    const fadeOptions = {
        threshold: 0.3,
        rootMargin: "0px 0px -100px 0px"
    };

    const fadeObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('appear');
                observer.unobserve(entry.target);
            }
        });
    }, fadeOptions);

    faders.forEach(fader => {
        fadeObserver.observe(fader);
    });

    // Animated Images (Slide-In, Zoom-In/Out)
    const animatedImages = document.querySelectorAll('.slide-in, .zoom-in, .zoom-out');

    const imageOptions = {
        threshold: 0.3,
        rootMargin: "0px 0px -100px 0px"
    };

    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('appear'); // Trigger animation
                observer.unobserve(entry.target); // Stop observing
            }
        });
    }, imageOptions);

    animatedImages.forEach(image => {
        imageObserver.observe(image);
    });
});