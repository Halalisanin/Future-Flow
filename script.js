// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });

            // Update active nav link
            updateActiveNavLink(this.getAttribute('href'));
        }
    });
});

// Navbar background change on scroll
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 100) {
        navbar.style.background = 'rgba(255, 255, 255, 0.98)';
        navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
    }

    // Update active nav link based on scroll position
    updateActiveNavOnScroll();
});

// Update active navigation link
function updateActiveNavLink(targetId) {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    document.querySelector(`a[href="${targetId}"]`).classList.add('active');
}

// Update active nav based on scroll position
function updateActiveNavOnScroll() {
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav-link');

    let currentSection = '';

    sections.forEach(section => {
        const sectionTop = section.offsetTop - 100;
        const sectionHeight = section.clientHeight;
        if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
            currentSection = '#' + section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === currentSection) {
            link.classList.add('active');
        }
    });
}

// Contact form handling
document.getElementById('contactForm').addEventListener('submit', function(e) {
    e.preventDefault();

    // Get form data
    const formData = {
        name: document.getElementById('name').value.trim(),
        email: document.getElementById('email').value.trim(),
        message: document.getElementById('message').value.trim()
    };

    // Validate form
    if (validateForm(formData)) {
        // Show loading state
        const submitBtn = this.querySelector('.submit-btn');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Sending...';
        submitBtn.disabled = true;

        // Simulate form submission (replace with actual API call)
        setTimeout(() => {
            // Here you would typically send the form data to a server
            console.log('Form submitted:', formData);

            // Show success message
            showNotification('Thank you for your message! I\'ll get back to you soon.', 'success');

            // Reset form
            this.reset();

            // Reset button
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }, 1500);
    }
});

// Form validation
function validateForm(formData) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!formData.name) {
        showNotification('Please enter your name.', 'error');
        document.getElementById('name').focus();
        return false;
    }

    if (!formData.email) {
        showNotification('Please enter your email address.', 'error');
        document.getElementById('email').focus();
        return false;
    }

    if (!emailRegex.test(formData.email)) {
        showNotification('Please enter a valid email address.', 'error');
        document.getElementById('email').focus();
        return false;
    }

    if (!formData.message) {
        showNotification('Please enter your message.', 'error');
        document.getElementById('message').focus();
        return false;
    }

    if (formData.message.length < 10) {
        showNotification('Please write a more detailed message (at least 10 characters).', 'error');
        document.getElementById('message').focus();
        return false;
    }

    return true;
}

// Notification system
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }

    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span class="notification-message">${message}</span>
        <button class="notification-close">&times;</button>
    `;

    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${type === 'error' ? '#e74c3c' : type === 'success' ? '#27ae60' : '#3498db'};
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        z-index: 10000;
        display: flex;
        align-items: center;
        gap: 15px;
        max-width: 400px;
        animation: slideInRight 0.3s ease;
        font-weight: 500;
    `;

    // Close button styles
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.style.cssText = `
        background: none;
        border: none;
        color: white;
        font-size: 20px;
        cursor: pointer;
        padding: 0;
        width: 20px;
        height: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
    `;

    // Add to page
    document.body.appendChild(notification);

    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);

    // Close on click
    closeBtn.addEventListener('click', () => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    });
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }

    .nav-link.active {
        color: #2c5aa0 !important;
        font-weight: 600;
    }
`;
document.head.appendChild(style);

// Blog post interactions
document.addEventListener('click', function(e) {
    // Handle read more clicks
    if (e.target.classList.contains('read-more')) {
        e.preventDefault();
        const blogPost = e.target.closest('.blog-post');
        const title = blogPost.querySelector('h3').textContent;

        // Show a preview modal or navigate to full blog post
        showBlogPreview(title, blogPost);
    }

    // Handle blog post clicks (excluding read more button)
    if (e.target.closest('.blog-post') && !e.target.classList.contains('read-more')) {
        const blogPost = e.target.closest('.blog-post');
        const title = blogPost.querySelector('h3').textContent;
        const excerpt = blogPost.querySelector('p').textContent;

        // Add visual feedback
        blogPost.style.transform = 'scale(0.98)';
        setTimeout(() => {
            blogPost.style.transform = '';
        }, 150);
    }
});

// Blog preview function
function showBlogPreview(title, blogPost) {
    const excerpt = blogPost.querySelector('p').textContent;
    const author = blogPost.querySelector('.author-name').textContent;
    const date = blogPost.querySelector('.post-date').textContent;

    // Create modal overlay
    const modal = document.createElement('div');
    modal.className = 'blog-modal';
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.7);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        padding: 20px;
        animation: fadeIn 0.3s ease;
    `;

    modal.innerHTML = `
        <div class="modal-content" style="
            background: white;
            padding: 2rem;
            border-radius: 10px;
            max-width: 600px;
            width: 100%;
            max-height: 80vh;
            overflow-y: auto;
            position: relative;
            animation: slideUp 0.3s ease;
        ">
            <button class="modal-close" style="
                position: absolute;
                top: 15px;
                right: 15px;
                background: none;
                border: none;
                font-size: 24px;
                cursor: pointer;
                color: #666;
            ">&times;</button>

            <div class="blog-header">
                <img src="profile.jpg" alt="${author}" class="author-img">
                <div class="author-info">
                    <span class="author-name">${author}</span>
                    <span class="post-date">${date}</span>
                </div>
            </div>

            <h2 style="color: #2c5aa0; margin: 1rem 0; font-size: 1.5rem;">${title}</h2>
            <p style="color: #666; line-height: 1.6; margin-bottom: 1.5rem;">${excerpt}</p>

            <div style="text-align: center; padding-top: 1rem; border-top: 1px solid #eee;">
                <p style="color: #999; font-style: italic;">
                    Full blog post coming soon! Follow on Facebook for updates.
                </p>
                <a href="https://facebook.com/YourPageName" target="_blank" 
                   style="display: inline-block; margin-top: 1rem; padding: 10px 20px; 
                          background: #2c5aa0; color: white; text-decoration: none; 
                          border-radius: 5px; font-weight: 500;">
                    Follow on Facebook
                </a>
            </div>
        </div>
    `;

    document.body.appendChild(modal);

    // Close modal events
    const closeBtn = modal.querySelector('.modal-close');
    closeBtn.addEventListener('click', () => closeModal(modal));
    modal.addEventListener('click', (e) => {
        if (e.target === modal) closeModal(modal);
    });

    // Add modal animations
    const modalStyle = document.createElement('style');
    modalStyle.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        @keyframes slideUp {
            from {
                transform: translateY(50px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
    `;
    document.head.appendChild(modalStyle);
}

function closeModal(modal) {
    modal.style.animation = 'fadeOut 0.3s ease';
    const modalContent = modal.querySelector('.modal-content');
    modalContent.style.animation = 'slideDown 0.3s ease';

    setTimeout(() => {
        if (modal.parentNode) {
            modal.remove();
        }
    }, 300);
}

// Add fade-in animation for sections
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe sections for animation
document.querySelectorAll('.blog-section, .contact-section').forEach(section => {
    section.style.opacity = '0';
    section.style.transform = 'translateY(20px)';
    section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(section);
});

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Set initial active nav link
    updateActiveNavLink('#home');

    // Add loading animation to hero section
    const heroContent = document.querySelector('.hero-content');
    heroContent.style.opacity = '0';
    heroContent.style.transform = 'translateY(30px)';
    heroContent.style.transition = 'opacity 0.8s ease, transform 0.8s ease';

    setTimeout(() => {
        heroContent.style.opacity = '1';
        heroContent.style.transform = 'translateY(0)';
    }, 300);

    console.log('Future Flow website loaded successfully!');
});

// Enhanced error handling
window.addEventListener('error', function(e) {
    console.error('Website error:', e.error);
});

// Performance monitoring
window.addEventListener('load', function() {
    const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
    console.log(`Page loaded in ${loadTime}ms`);
});
