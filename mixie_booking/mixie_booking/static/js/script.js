// Slideshow functionality
let slideIndex = 0;
const slides = document.querySelectorAll('.slide');
const dots = document.querySelectorAll('.dot');
const slideContainer = document.querySelector('.slide-container');
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');
const slideDuration = 4000;

// Helper function to fetch CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function moveSlides(direction = 1) {
    // Calculate new index
    if (direction > 0) {
        slideIndex = (slideIndex + 1) % slides.length;
    } else {
        slideIndex = (slideIndex - 1 + slides.length) % slides.length;
    }
    
    // Move slide container
    const translateX = -(slideIndex * 100);
    slideContainer.style.transform = `translateX(${translateX}%)`;
    
    // Update active dot
    dots.forEach(dot => dot.classList.remove('active'));
    dots[slideIndex].classList.add('active');
}

// Initialize slideshow
document.addEventListener('DOMContentLoaded', () => {
    // Set initial styles for slide container
    slideContainer.style.display = 'flex';
    slideContainer.style.width = `${slides.length * 100}%`;
    slideContainer.style.transition = 'transform 0.5s ease';
    
    // Set width for individual slides
    slides.forEach(slide => {
        slide.style.flex = `0 0 ${100 / slides.length}%`;
    });
    
    // Show all slides initially
    slides.forEach(slide => {
        slide.classList.add('active');
    });
    
    // Start automatic slideshow
    let slideInterval = setInterval(() => moveSlides(1), slideDuration);
    
    // Navigation handlers
    prevBtn.addEventListener('click', () => {
        clearInterval(slideInterval);
        moveSlides(-1);
        slideInterval = setInterval(() => moveSlides(1), slideDuration);
    });
    
    nextBtn.addEventListener('click', () => {
        clearInterval(slideInterval);
        moveSlides(1);
        slideInterval = setInterval(() => moveSlides(1), slideDuration);
    });
    
    // Dot navigation
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            clearInterval(slideInterval);
            slideIndex = index;
            moveSlides(0);
            slideInterval = setInterval(() => moveSlides(1), slideDuration);
        });
    });
});

// Page Transition Handler
document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('.nav-links a');
    const sections = document.querySelectorAll('section');
    
    // Add transition class to all sections
    sections.forEach(section => {
        section.classList.add('section-transition');
    });
    
    // Handle smooth scrolling and external navigation links
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const target = link.getAttribute('href');

            // Allow normal navigation for external links
            if (target.startsWith('/') || target.startsWith('http')) {
                return; // Let the browser handle it
            }

            // Handle smooth scrolling for internal links only
            e.preventDefault();
            const targetSection = document.querySelector(target);
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Handle scroll-based transitions
    const observerOptions = {
        threshold: 0.2
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('section-transition');
                
                // Update active nav link
                const sectionId = entry.target.id;
                navLinks.forEach(link => {
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    } else {
                        link.classList.remove('active');
                    }
                });
            }
        });
    }, observerOptions);
    
    sections.forEach(section => {
        observer.observe(section);
    });
});

// Smooth scroll for "See the Magic" button
document.addEventListener('DOMContentLoaded', function() {
    const magicButton = document.querySelector('.secondary-btn');
    
    magicButton.addEventListener('click', function(e) {
        e.preventDefault();
        
        // Add a magical sparkle effect before scrolling
        const sparkle = document.createElement('div');
        sparkle.className = 'magic-sparkle';
        this.appendChild(sparkle);
        
        // Remove sparkle after animation
        setTimeout(() => sparkle.remove(), 1000);
        
        // Smooth scroll to gallery
        document.querySelector('#gallery').scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Contact Form Submission
/*document.querySelector('.contact-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        message: document.getElementById('message').value
    };

    try {
        const response = await fetch('/api/contact/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            alert('Message sent successfully!');
            this.reset();
        } else {
            alert('Error sending message. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error sending message. Please try again.');
    }
});*/

document.addEventListener('DOMContentLoaded', function () {
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', async function (e) {
            e.preventDefault();

            const formData = new FormData(contactForm); // Collect form data

            try {
                const response = await fetch('/book/contact/submit/', {  // Update URL
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')  // CSRF token
                    },
                    body: formData
                });

                if (response.ok) {
                    alert('Message sent successfully!');
                    contactForm.reset(); // Clear the form
                } else {
                    alert('Error sending message. Please check your input and try again.');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error sending message. Please try again.');
            }
        });
    }
});



// Handle navigation to booking page
document.querySelectorAll('a[href="./booking.html"]').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        window.location.href = './booking.html';
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const dateInput = document.getElementById('id_date');

    if (dateInput) {
        const today = new Date();
        const minDate = new Date(today);
        minDate.setDate(today.getDate() + 3); // 3 days in advance

        const minDateString = minDate.toISOString().split('T')[0];
        dateInput.setAttribute('min', minDateString); // Enforces 'min' attribute dynamically
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const privacyButton = document.getElementById('privacy-btn');
    if (privacyButton) {
        privacyButton.addEventListener('click', function () {
            window.open(
                '/privacy-policy/', // URL
                'Privacy Policy', // Window Name
                'width=800,height=600,scrollbars=yes' // Features
            );
        });
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        question.addEventListener('click', () => {
            // Close all other FAQs
            faqItems.forEach(innerItem => {
                if (innerItem !== item) {
                    innerItem.classList.remove('active');
                }
            });

            // Toggle active class
            item.classList.toggle('active');
        });
    });
});
