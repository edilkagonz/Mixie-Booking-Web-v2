// Slideshow functionality
let slideIndex = 0;
const slides = document.querySelectorAll('.slide');
const dots = document.querySelectorAll('.dot');
const slideContainer = document.querySelector('.slide-container');
const prevBtn = document.querySelector('.prev-btn');
const nextBtn = document.querySelector('.next-btn');
const slideDuration = 4000;

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
    
    // Handle smooth scrolling with transitions
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            // Remove transition class to reset animation
            targetSection.classList.remove('section-transition');
            
            // Trigger reflow
            void targetSection.offsetWidth;
            
            // Add class back to trigger animation
            targetSection.classList.add('section-transition');
            
            // Smooth scroll to section
            targetSection.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
            
            // Update active link
            navLinks.forEach(navLink => navLink.classList.remove('active'));
            link.classList.add('active');
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

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll for "See the Magic" button
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

document.querySelector('.contact-form').addEventListener('submit', async function(e) {
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
});

// Handle navigation to booking page
document.querySelectorAll('a[href="./booking.html"]').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        window.location.href = './booking.html';
    });
}); 