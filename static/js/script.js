// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Navbar scrolling effect
    const navbar = document.querySelector('.navbar');
    
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }
    
    // Enable tooltips everywhere
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Enable image gallery functionality
    function initializeImageGallery() {
        const galleryItems = document.querySelectorAll('.gallery-item img, .model-card img, .comparison-item img');
        
        galleryItems.forEach(item => {
            // Add cursor pointer and click event
            item.style.cursor = 'pointer';
            item.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                const src = this.getAttribute('src');
                const alt = this.getAttribute('alt') || 'Image Preview';
                
                // Remove existing modal if it exists
                let existingModal = document.getElementById('imageModal');
                if (existingModal) {
                    existingModal.remove();
                }
                
                // Create new modal
                const modal = document.createElement('div');
                modal.className = 'modal fade';
                modal.id = 'imageModal';
                modal.tabIndex = '-1';
                modal.setAttribute('aria-hidden', 'true');
                modal.setAttribute('aria-labelledby', 'imageModalLabel');
                
                modal.innerHTML = `
                    <div class="modal-dialog modal-xl modal-dialog-centered">
                        <div class="modal-content bg-dark">
                            <div class="modal-header border-0">
                                <h5 class="modal-title text-white" id="imageModalLabel">${alt}</h5>
                                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body text-center p-2">
                                <img src="${src}" class="img-fluid gallery-modal-img" alt="${alt}" style="max-height: 80vh; width: auto;">
                                <div class="mt-3">
                                    <small class="text-muted">Click outside the image or press ESC to close</small>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                
                document.body.appendChild(modal);
                
                // Show the modal
                const modalInstance = new bootstrap.Modal(modal, {
                    keyboard: true,
                    backdrop: true
                });
                modalInstance.show();
                
                // Remove modal from DOM when hidden
                modal.addEventListener('hidden.bs.modal', function () {
                    modal.remove();
                });
                
                // Add click to close functionality
                modal.querySelector('.modal-body').addEventListener('click', function(e) {
                    if (e.target === this) {
                        modalInstance.hide();
                    }
                });
            });
        });
    }
    
    // Initialize gallery on page load
    initializeImageGallery();
    
    // Form validation
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            if (!contactForm.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            contactForm.classList.add('was-validated');
        });
    }
    
    // Animate elements on scroll
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    
    if (animateElements.length > 0) {
        const animateOnScroll = function() {
            animateElements.forEach(element => {
                const elementPosition = element.getBoundingClientRect().top;
                const windowHeight = window.innerHeight;
                
                if (elementPosition < windowHeight - 50) {
                    element.classList.add('animated');
                }
            });
        };
        
        // Run once on page load
        animateOnScroll();
        
        // Run on scroll
        window.addEventListener('scroll', animateOnScroll);
    }
    
    // Add parallax effect to hero section
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        window.addEventListener('scroll', function() {
            const scrollPosition = window.scrollY;
            const heroImage = heroSection.querySelector('.hero-image');
            if (heroImage) {
                // Parallax scrolling effect
                heroImage.style.transform = `translateY(${scrollPosition * 0.2}px)`;
            }
        });
    }

    // Add hover state to gallery items
    const galleryItems = document.querySelectorAll('.gallery-item');
    galleryItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.classList.add('active');
        });
        item.addEventListener('mouseleave', function() {
            this.classList.remove('active');
        });
    });

    // Add scroll animations
    const animatedElements = document.querySelectorAll('.feature-box, .model-card, .pricing-table');
    
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.2
    };
    
    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                // Stop observing after animation is applied
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    animatedElements.forEach(element => {
        observer.observe(element);
    });

    // Add glow effect to buttons on hover
    const cosmicButtons = document.querySelectorAll('.cosmic-btn');
    cosmicButtons.forEach(button => {
        button.addEventListener('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            this.style.background = `radial-gradient(circle at ${x}px ${y}px, #e5a55d, #8a5c98)`;
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.background = 'linear-gradient(45deg, #e5a55d, #8a5c98)';
        });
    });
    
    // Lightbox functionality for all gallery items
    const setupLightbox = () => {
        // Create lightbox elements
        const lightboxOverlay = document.createElement('div');
        lightboxOverlay.className = 'lightbox-overlay';
        
        const lightboxContent = document.createElement('div');
        lightboxContent.className = 'lightbox-content';
        
        const lightboxImg = document.createElement('img');
        lightboxImg.className = 'lightbox-img';
        
        const closeButton = document.createElement('div');
        closeButton.className = 'lightbox-close';
        closeButton.innerHTML = '<i class="fas fa-times"></i>';
        
        const prevButton = document.createElement('div');
        prevButton.className = 'lightbox-nav prev';
        prevButton.style.left = '20px';
        prevButton.innerHTML = '<i class="fas fa-chevron-left"></i>';
        
        const nextButton = document.createElement('div');
        nextButton.className = 'lightbox-nav next';
        nextButton.style.right = '20px';
        nextButton.innerHTML = '<i class="fas fa-chevron-right"></i>';
        
        const imageCounter = document.createElement('div');
        imageCounter.className = 'lightbox-counter';
        
        // Append elements
        lightboxContent.appendChild(lightboxImg);
        lightboxContent.appendChild(closeButton);
        lightboxContent.appendChild(prevButton);
        lightboxContent.appendChild(nextButton);
        lightboxContent.appendChild(imageCounter);
        lightboxOverlay.appendChild(lightboxContent);
        document.body.appendChild(lightboxOverlay);
        
        // Find specific contexts for grouping images
        const findGalleryContext = (element) => {
            // Check if in model detail page
            if (window.location.pathname.includes('/model/') || window.location.pathname.includes('/virtual-model/')) {
                return 'model-gallery';
            }
            // Check if in comparison gallery
            else if (window.location.pathname.includes('/real-comparison')) {
                if (element.closest('.comparison-item')) {
                    return 'comparison-gallery';
                }
                return 'gallery-grid';
            }
            // Default to generic gallery
            return 'gallery';
        };
        
        // Get all gallery items
        const allGalleryItems = document.querySelectorAll('.gallery-item img, .comparison-item img, .gallery-grid img, .card img.img-fluid');
        let currentIndex = 0;
        let galleryImages = [];
        let galleryImageElements = [];
        let currentContext = '';
        
        // Add click handlers to all images
        allGalleryItems.forEach((item, index) => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                
                // Determine the context for grouping images
                const context = findGalleryContext(item);
                currentContext = context;
                
                // Reset and rebuild the gallery array based on context
                galleryImages = [];
                galleryImageElements = [];
                
                // Select the right set of images based on context
                let contextSelector;
                if (context === 'model-gallery') {
                    contextSelector = '.gallery-grid img';
                } else if (context === 'comparison-gallery') {
                    if (item.closest('.comparison-item')) {
                        contextSelector = '.comparison-item img';
                    } else {
                        contextSelector = '.gallery-grid img';
                    }
                } else {
                    contextSelector = '.gallery-item img, .card img.img-fluid';
                }
                
                // Build the gallery array for this context
                const contextItems = document.querySelectorAll(contextSelector);
                contextItems.forEach((img) => {
                    galleryImages.push(img.src);
                    galleryImageElements.push(img);
                });
                
                // Find the index of the clicked image in our new array
                currentIndex = galleryImages.findIndex(src => src === item.src);
                if (currentIndex === -1) currentIndex = 0; // Fallback
                
                openLightbox(item.src);
            });
        });
        
        // Open lightbox function
        const openLightbox = (src) => {
            lightboxImg.src = src;
            lightboxOverlay.style.display = 'flex';
            document.body.style.overflow = 'hidden'; // Prevent scrolling
            
            // Update image counter
            updateCounter();
            
            // Update navigation visibility
            updateNavVisibility();
        };
        
        // Close lightbox function
        const closeLightbox = () => {
            lightboxOverlay.style.display = 'none';
            document.body.style.overflow = 'auto'; // Restore scrolling
        };
        
        // Update image counter
        const updateCounter = () => {
            imageCounter.textContent = `${currentIndex + 1} / ${galleryImages.length}`;
        };
        
        // Update navigation visibility
        const updateNavVisibility = () => {
            prevButton.style.opacity = currentIndex > 0 ? '1' : '0.3';
            nextButton.style.opacity = currentIndex < galleryImages.length - 1 ? '1' : '0.3';
        };
        
        // Event listeners
        closeButton.addEventListener('click', closeLightbox);
        
        prevButton.addEventListener('click', () => {
            if (currentIndex > 0) {
                currentIndex--;
                lightboxImg.src = galleryImages[currentIndex];
                updateCounter();
                updateNavVisibility();
            }
        });
        
        nextButton.addEventListener('click', () => {
            if (currentIndex < galleryImages.length - 1) {
                currentIndex++;
                lightboxImg.src = galleryImages[currentIndex];
                updateCounter();
                updateNavVisibility();
            }
        });
        
        // Close on click outside the image
        lightboxOverlay.addEventListener('click', (e) => {
            if (e.target === lightboxOverlay) {
                closeLightbox();
            }
        });
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (lightboxOverlay.style.display === 'flex') {
                if (e.key === 'Escape') {
                    closeLightbox();
                } else if (e.key === 'ArrowLeft' && currentIndex > 0) {
                    currentIndex--;
                    lightboxImg.src = galleryImages[currentIndex];
                    updateCounter();
                    updateNavVisibility();
                } else if (e.key === 'ArrowRight' && currentIndex < galleryImages.length - 1) {
                    currentIndex++;
                    lightboxImg.src = galleryImages[currentIndex];
                    updateCounter();
                    updateNavVisibility();
                }
            }
        });
    };
    
    // Initialize lightbox
    setupLightbox();
});
