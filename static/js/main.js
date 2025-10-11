/**
 * Portal de Análise - Modern JavaScript Features
 * ================================================
 */

// Scroll Progress Bar
(function initScrollProgress() {
    const progressBar = document.createElement('div');
    progressBar.id = 'scroll-progress';
    progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 0%;
        height: 3px;
        background: linear-gradient(90deg, #E3120B 0%, #a80e08 100%);
        z-index: 9999;
        transition: width 0.1s ease;
    `;
    document.body.appendChild(progressBar);

    window.addEventListener('scroll', () => {
        const windowHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (window.scrollY / windowHeight) * 100;
        progressBar.style.width = scrolled + '%';
    });
})();

// Smooth Scrolling for Anchor Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href === '#' || href === '') return;
        
        e.preventDefault();
        const target = document.querySelector(href);
        
        if (target) {
            const headerOffset = 160; // Account for fixed header
            const elementPosition = target.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// Reading Time Estimator
function estimateReadingTime() {
    const articles = document.querySelectorAll('.article-body, .featured-article');
    
    articles.forEach(article => {
        const text = article.innerText || article.textContent;
        const wordCount = text.trim().split(/\s+/).length;
        const readingTimeMinutes = Math.ceil(wordCount / 200); // Average 200 words per minute
        
        // Create reading time element
        const readingTimeEl = document.createElement('span');
        readingTimeEl.className = 'reading-time text-muted small';
        readingTimeEl.innerHTML = `<i class="bi bi-book"></i> ${readingTimeMinutes} min de leitura`;
        
        // Try to insert after the date/time element
        const timeElement = article.querySelector('.text-muted.small');
        if (timeElement && !article.querySelector('.reading-time')) {
            timeElement.insertAdjacentHTML('afterend', ' • ' + readingTimeEl.outerHTML);
        }
    });
}

// Lazy Loading Images Enhancement
function initLazyLoading() {
    if ('loading' in HTMLImageElement.prototype) {
        const images = document.querySelectorAll('img[loading="lazy"]');
        images.forEach(img => {
            img.src = img.dataset.src || img.src;
        });
    } else {
        // Fallback for browsers that don't support native lazy loading
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/lazysizes/5.3.2/lazysizes.min.js';
        document.body.appendChild(script);
    }
}

// Article Card Hover Effects Enhancement
function enhanceArticleCards() {
    const cards = document.querySelectorAll('.article-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Newsletter Form Handler
function initNewsletterForm() {
    const newsletterForm = document.querySelector('.footer-newsletter form');
    
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const emailInput = this.querySelector('input[type="email"]');
            const email = emailInput.value;
            
            if (email && validateEmail(email)) {
                // Show success message
                showToast('Obrigado! Em breve você receberá nossas análises.', 'success');
                emailInput.value = '';
            } else {
                showToast('Por favor, insira um e-mail válido.', 'error');
            }
        });
    }
}

// Email Validation
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Toast Notification System
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;
    toast.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        background: ${type === 'success' ? '#28a745' : type === 'error' ? '#E3120B' : '#007bff'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        z-index: 9999;
        animation: slideInUp 0.5s ease;
        max-width: 300px;
    `;
    toast.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <i class="bi bi-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOutDown 0.5s ease';
        setTimeout(() => toast.remove(), 500);
    }, 5000);
}

// Add CSS animations for toast
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInUp {
        from {
            transform: translateY(100%);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutDown {
        from {
            transform: translateY(0);
            opacity: 1;
        }
        to {
            transform: translateY(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Share Button Functionality
function initShareButtons() {
    const shareButtons = document.querySelectorAll('.share-button');
    
    shareButtons.forEach(button => {
        button.addEventListener('click', function() {
            const url = window.location.href;
            const title = document.title;
            
            if (navigator.share) {
                navigator.share({
                    title: title,
                    url: url
                }).then(() => {
                    showToast('Compartilhado com sucesso!', 'success');
                }).catch(() => {
                    fallbackShare(url);
                });
            } else {
                fallbackShare(url);
            }
        });
    });
}

function fallbackShare(url) {
    // Copy to clipboard
    navigator.clipboard.writeText(url).then(() => {
        showToast('Link copiado para a área de transferência!', 'success');
    }).catch(() => {
        showToast('Não foi possível copiar o link.', 'error');
    });
}

// Dark Mode Toggle (Optional Feature)
function initDarkMode() {
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    
    if (darkModeToggle) {
        const isDarkMode = localStorage.getItem('darkMode') === 'true';
        
        if (isDarkMode) {
            document.body.classList.add('dark-mode');
        }
        
        darkModeToggle.addEventListener('click', () => {
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
        });
    }
}

// Performance: Defer non-critical resources
function deferResources() {
    // Defer loading of non-critical CSS
    const deferredStyles = document.querySelectorAll('link[data-defer]');
    deferredStyles.forEach(link => {
        link.rel = 'stylesheet';
    });
}

// Initialize all features when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    estimateReadingTime();
    initLazyLoading();
    enhanceArticleCards();
    initNewsletterForm();
    initShareButtons();
    initDarkMode();
    deferResources();
    
    console.log('%c Portal de Análise %c Carregado com sucesso! ', 
                'background: #E3120B; color: white; padding: 5px 10px; border-radius: 3px 0 0 3px;',
                'background: #111; color: white; padding: 5px 10px; border-radius: 0 3px 3px 0;');
});

// Service Worker Registration (for PWA features - optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Uncomment when service worker is ready
        // navigator.serviceWorker.register('/sw.js');
    });
}

// Export functions for use in other scripts
window.PortalAnalise = {
    showToast,
    validateEmail,
    estimateReadingTime
};
