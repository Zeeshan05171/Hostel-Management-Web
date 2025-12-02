/**
 * Animation utilities for HostelEase
 * Handles scroll animations, counters, and transitions
 */

/**
 * Initialize all animations
 */
function initAnimations() {
    initScrollAnimations();
    initCounterAnimations();
}

/**
 * Scroll-based fade-in animations using Intersection Observer
 */
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                // Stop observing after animation
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all elements with .fade-in class
    const elements = document.querySelectorAll('.fade-in');
    elements.forEach(el => observer.observe(el));
}

/**
 * Animated number counters
 * @param {HTMLElement} element - Element containing the number
 * @param {number} target - Target number  * @param {number} duration - Animation duration in ms
 */
function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const increment = target / (duration / 16); // 60fps
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current).toLocaleString();
    }, 16);
}

/**
 * Initialize counter animations for stat cards
 */
function initCounterAnimations() {
    const observerOptions = {
        threshold: 0.5,
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const element = entry.target;
                const target = parseInt(element.getAttribute('data-count'));
                if (!isNaN(target)) {
                    animateCounter(element, target);
                    observer.unobserve(element);
                }
            }
        });
    }, observerOptions);

    // Observe all elements with data-count attribute
    const counters = document.querySelectorAll('[data-count]');
    counters.forEach(counter => observer.observe(counter));
}

/**
 * Smooth scroll to element
 * @param {string} targetId - ID of target element
 */
function smoothScrollTo(targetId) {
    const element = document.getElementById(targetId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

/**
 * Add smooth scroll to all navigation links
 */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#' && href.length > 1) {
                e.preventDefault();
                const targetId = href.substring(1);
                smoothScrollTo(targetId);
            }
        });
    });
}

/**
 * Parallax effect for hero shapes
 */
function initParallax() {
    const shapes = document.querySelectorAll('.hero-shape');

    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;

        shapes.forEach((shape, index) => {
            const speed = 0.5 + (index * 0.2);
            const yPos = -(scrolled * speed);
            shape.style.transform = `translateY(${yPos}px)`;
        });
    });
}

/**
 * Fade in element
 * @param {HTMLElement} element
 */
function fadeIn(element, duration = 300) {
    element.style.opacity = '0';
    element.style.display = 'block';

    let opacity = 0;
    const increment = 16 / duration;

    const timer = setInterval(() => {
        opacity += increment;
        if (opacity >= 1) {
            opacity = 1;
            clearInterval(timer);
        }
        element.style.opacity = opacity;
    }, 16);
}

/**
 * Fade out element
 * @param {HTMLElement} element
 */
function fadeOut(element, duration = 300) {
    let opacity = 1;
    const increment = 16 / duration;

    const timer = setInterval(() => {
        opacity -= increment;
        if (opacity <= 0) {
            opacity = 0;
            element.style.display = 'none';
            clearInterval(timer);
        }
        element.style.opacity = opacity;
    }, 16);
}

/**
 * Slide down element
 * @param {HTMLElement} element
 */
function slideDown(element, duration = 300) {
    element.style.display = 'block';
    element.style.height = '0';
    element.style.overflow = 'hidden';

    const targetHeight = element.scrollHeight;
    const increment = targetHeight / (duration / 16);
    let currentHeight = 0;

    const timer = setInterval(() => {
        currentHeight += increment;
        if (currentHeight >= targetHeight) {
            currentHeight = targetHeight;
            element.style.height = 'auto';
            element.style.overflow = 'visible';
            clearInterval(timer);
        }
        element.style.height = currentHeight + 'px';
    }, 16);
}

/**
 * Slide up element
 * @param {HTMLElement} element
 */
function slideUp(element, duration = 300) {
    const targetHeight = element.scrollHeight;
    let currentHeight = targetHeight;
    const increment = targetHeight / (duration / 16);

    element.style.overflow = 'hidden';

    const timer = setInterval(() => {
        currentHeight -= increment;
        if (currentHeight <= 0) {
            currentHeight = 0;
            element.style.display = 'none';
            element.style.height = 'auto';
            clearInterval(timer);
        }
        element.style.height = currentHeight + 'px';
    }, 16);
}

// Export functions
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initAnimations,
        initScrollAnimations,
        initCounterAnimations,
        initSmoothScroll,
        initParallax,
        animateCounter,
        smoothScrollTo,
        fadeIn,
        fadeOut,
        slideDown,
        slideUp,
    };
}
