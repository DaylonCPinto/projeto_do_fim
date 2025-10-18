/**
 * Portal de Análise - Modern JavaScript Features
 * ================================================
 */

// Scroll Progress Bar
(function initScrollProgress() {
    const body = document.body;
    if (!body || body.dataset.scrollProgress === 'false') {
        return;
    }

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
    body.appendChild(progressBar);

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
    const body = document.body;
    if (!body || body.dataset.darkModeToggle !== 'true') {
        return;
    }

    const darkModeToggle = document.getElementById('dark-mode-toggle');
    if (!darkModeToggle) {
        return;
    }

    const iconEl = darkModeToggle.querySelector('i');
    const labelEl = darkModeToggle.querySelector('.dark-mode-label');
    const storedPreference = localStorage.getItem('darkMode');

    if (storedPreference === 'true') {
        body.classList.add('dark-mode');
    } else if (storedPreference === 'false') {
        body.classList.remove('dark-mode');
    }

    const updateToggleLabel = () => {
        const isDark = body.classList.contains('dark-mode');
        if (iconEl) {
            iconEl.classList.toggle('bi-moon-stars', !isDark);
            iconEl.classList.toggle('bi-sun-fill', isDark);
        }
        if (labelEl) {
            labelEl.textContent = isDark ? 'Modo Claro' : 'Modo Escuro';
        }
    };

    updateToggleLabel();

    darkModeToggle.addEventListener('click', () => {
        body.classList.toggle('dark-mode');
        const isDark = body.classList.contains('dark-mode');
        localStorage.setItem('darkMode', isDark);
        updateToggleLabel();
    });
}

function resolveEmbedUrl(url) {
    if (!url) {
        return '';
    }

    let parsedUrl;
    try {
        parsedUrl = new URL(url);
    } catch (error) {
        return url;
    }

    const hostname = parsedUrl.hostname.replace(/^www\./, '').toLowerCase();
    const pathSegments = parsedUrl.pathname.split('/').filter(Boolean);

    const clean = (value) => value ? value.split('?')[0] : '';

    if (hostname.includes('youtube')) {
        let videoId = '';
        if (parsedUrl.pathname === '/watch') {
            videoId = parsedUrl.searchParams.get('v') || '';
        } else if (pathSegments.length) {
            if (['embed', 'shorts', 'live'].includes(pathSegments[0]) && pathSegments[1]) {
                videoId = clean(pathSegments[1]);
            } else {
                videoId = clean(pathSegments[pathSegments.length - 1]);
            }
        }

        if (videoId) {
            return `https://www.youtube.com/embed/${videoId}`;
        }
    }

    if (hostname === 'youtu.be' && pathSegments.length) {
        return `https://www.youtube.com/embed/${clean(pathSegments[0])}`;
    }

    if (hostname.includes('vimeo') && pathSegments.length) {
        const videoId = clean(pathSegments[pathSegments.length - 1]);
        if (/^\d+$/.test(videoId)) {
            return `https://player.vimeo.com/video/${videoId}`;
        }
    }

    return url;
}

function withAutoplay(url) {
    if (!url) {
        return '';
    }

    const separator = url.includes('?') ? '&' : '?';
    const autoplayParams = 'autoplay=1&rel=0&playsinline=1';
    return `${url}${separator}${autoplayParams}`;
}

function extractPlyrConfig(embedUrl) {
    if (!embedUrl) {
        return null;
    }

    let parsed;
    try {
        parsed = new URL(embedUrl);
    } catch (error) {
        return null;
    }

    const hostname = parsed.hostname.replace(/^www\./, '').toLowerCase();
    const segments = parsed.pathname.split('/').filter(Boolean);
    const cleanId = (value) => value.replace(/\?.*/, '');

    if (!segments.length) {
        return null;
    }

    if (hostname.includes('youtube') || hostname.includes('youtube-nocookie')) {
        const lastSegment = cleanId(segments[segments.length - 1]);
        return lastSegment ? { provider: 'youtube', id: lastSegment } : null;
    }

    if (hostname === 'youtu.be') {
        return segments[0] ? { provider: 'youtube', id: cleanId(segments[0]) } : null;
    }

    if (hostname.includes('vimeo')) {
        const candidate = cleanId(segments[segments.length - 1]);
        return /^\d+$/.test(candidate) ? { provider: 'vimeo', id: candidate } : null;
    }

    return null;
}

function normalizeAspectRatio(value, fallback = '16:9') {
    if (!value && value !== 0) {
        return fallback;
    }

    const raw = String(value).trim();
    if (!raw) {
        return fallback;
    }

    const normalized = raw
        .replace(/[xX/]/g, ':')
        .replace(/[^0-9:.]/g, '')
        .replace(/:+/g, ':')
        .replace(/^:|:$/g, '');

    const parts = normalized.split(':').filter(Boolean);
    if (parts.length === 2) {
        const width = parseFloat(parts[0]);
        const height = parseFloat(parts[1]);
        if (Number.isFinite(width) && Number.isFinite(height) && width > 0 && height > 0) {
            return `${width}:${height}`;
        }
    }

    return fallback;
}

function getAspectRatioFromElement(element, fallback = '16:9') {
    if (!element) {
        return normalizeAspectRatio(fallback);
    }

    const safeFallback = normalizeAspectRatio(fallback);

    if (element.dataset.aspectRatio) {
        return normalizeAspectRatio(element.dataset.aspectRatio, safeFallback);
    }

    const ratioContainer = element.closest('[class*="ratio-"]');
    if (ratioContainer) {
        const ratioClass = Array.from(ratioContainer.classList).find(cls => cls.startsWith('ratio-'));
        if (ratioClass) {
            const raw = ratioClass.replace('ratio-', '');
            return normalizeAspectRatio(raw, safeFallback);
        }
    }

    return safeFallback;
}

function initShortVideoModal() {
    const modalEl = document.getElementById('shortVideoModal');
    if (!modalEl || typeof bootstrap === 'undefined') {
        return;
    }

    const modalWrapper = modalEl.querySelector('.video-modal-wrapper');
    const modalDialog = modalEl.querySelector('.short-video-modal');
    const descriptionEl = modalEl.querySelector('.video-modal-description');
    const modalTitleEl = modalEl.querySelector('.modal-title');
    let plyrInstance = null;

    const destroyPlayer = () => {
        if (plyrInstance && typeof plyrInstance.destroy === 'function') {
            try {
                plyrInstance.destroy();
            } catch (error) {
                console.warn('Não foi possível destruir o player anterior.', error);
            }
        }
        plyrInstance = null;
    };

    const renderLoader = () => {
        if (modalWrapper) {
            destroyPlayer();
            modalWrapper.innerHTML = `
                <div class="video-modal-loader">
                    <div class="spinner-border text-economist-red" role="status">
                        <span class="visually-hidden">Carregando...</span>
                    </div>
                </div>
            `;
        }
    };

    const initializePlyr = (selector, options = {}) => {
        if (typeof Plyr === 'undefined') {
            return;
        }

        const element = modalWrapper ? modalWrapper.querySelector(selector) : null;
        if (!element) {
            return;
        }

        destroyPlayer();

        const defaultOptions = {
            controls: [
                'play-large',
                'play',
                'progress',
                'current-time',
                'mute',
                'volume',
                'settings',
                'pip',
                'airplay',
                'fullscreen'
            ],
            tooltips: {
                controls: true
            },
            storage: {
                enabled: false
            },
            resetOnEnd: true,
            ratio: '9:16',
            youtube: {
                rel: 0,
                modestbranding: 1,
                playsinline: 1
            },
            vimeo: {
                byline: false,
                portrait: false,
                title: false
            }
        };

        try {
            plyrInstance = new Plyr(element, Object.assign({}, defaultOptions, options));
            if (options.autoplay) {
                plyrInstance.on('ready', () => {
                    try {
                        plyrInstance.play();
                    } catch (error) {
                        console.warn('Autoplay bloqueado pelo navegador.', error);
                    }
                });
            }
        } catch (error) {
            console.error('Falha ao inicializar o player moderno.', error);
        }
    };

    const renderEmbedWithPlyr = (embedUrl, ratio = '9:16') => {
        const config = extractPlyrConfig(embedUrl);
        if (config && typeof Plyr !== 'undefined') {
            modalWrapper.innerHTML = `
                <div id="short-modal-player"
                     data-plyr-provider="${config.provider}"
                     data-plyr-embed-id="${config.id}"
                     data-aspect-ratio="${ratio}">
                </div>
            `;
            initializePlyr('#short-modal-player', { autoplay: true, ratio });
            return true;
        }
        return false;
    };

    const openModal = (card) => {
        if (!modalWrapper) {
            return;
        }

        const aspectRatio = normalizeAspectRatio(card.dataset.aspectRatio, '9:16');
        const ratioParts = aspectRatio.split(':').map((value) => Number.parseFloat(value));
        const ratioWidth = ratioParts[0];
        const ratioHeight = ratioParts[1];

        if (modalDialog && Number.isFinite(ratioWidth) && Number.isFinite(ratioHeight) && ratioWidth > 0 && ratioHeight > 0) {
            modalDialog.style.setProperty('--short-modal-aspect-width', ratioWidth);
            modalDialog.style.setProperty('--short-modal-aspect-height', ratioHeight);
        }

        const desiredClass = `ratio-${aspectRatio.replace(':', 'x')}`;
        const ratioClasses = Array.from(modalWrapper.classList).filter((cls) => cls.startsWith('ratio-'));
        ratioClasses.forEach((cls) => {
            if (cls !== desiredClass) {
                modalWrapper.classList.remove(cls);
            }
        });
        if (!modalWrapper.classList.contains(desiredClass)) {
            modalWrapper.classList.add(desiredClass);
        }
        modalWrapper.dataset.activeAspect = aspectRatio;

        renderLoader();

        const sourceType = card.dataset.source;
        const cdnUrl = card.dataset.videoUrl;
        const platformUrl = card.dataset.platformUrl;
        const embedUrlFromServer = card.dataset.embedUrl;
        const videoUrl = cdnUrl || '';
        const platformEmbedUrl = embedUrlFromServer || resolveEmbedUrl(platformUrl);
        const mimeType = card.dataset.mimeType;
        const title = card.dataset.title || 'Vídeo';
        const description = card.dataset.description || '';
        const poster = card.dataset.thumbnail || card.querySelector('img')?.src || '';

        if (modalTitleEl) {
            modalTitleEl.textContent = title;
        }
        if (descriptionEl) {
            descriptionEl.textContent = description;
        }

        if ((sourceType === 'cdn' || (!platformEmbedUrl && videoUrl)) && videoUrl) {
            const posterAttr = poster ? ` poster="${poster}"` : '';
            const mimeAttr = mimeType ? ` type="${mimeType}"` : '';
            modalWrapper.innerHTML = `
                <video id="short-modal-player"
                       class="video-modal-player"
                       controls
                       playsinline
                       preload="metadata"${posterAttr}
                       crossorigin="anonymous"
                       data-aspect-ratio="${aspectRatio}">
                    <source src="${videoUrl}"${mimeAttr}>
                    Seu navegador não suporta o elemento de vídeo.
                </video>
            `;
            initializePlyr('#short-modal-player', { ratio: aspectRatio, autoplay: true });
        } else if (platformEmbedUrl) {
            if (!renderEmbedWithPlyr(platformEmbedUrl, aspectRatio)) {
                const autoplayEmbed = withAutoplay(platformEmbedUrl);
                modalWrapper.innerHTML = `
                    <iframe src="${autoplayEmbed}" class="video-modal-iframe" allowfullscreen
                            loading="lazy" allow="autoplay; fullscreen; picture-in-picture"
                            referrerpolicy="no-referrer-when-downgrade"></iframe>
                `;
            }
        } else if (platformUrl) {
            const fallbackEmbed = resolveEmbedUrl(platformUrl);
            if (fallbackEmbed) {
                if (!renderEmbedWithPlyr(fallbackEmbed, aspectRatio)) {
                    modalWrapper.innerHTML = `
                        <iframe src="${withAutoplay(fallbackEmbed)}" class="video-modal-iframe" allowfullscreen
                                loading="lazy" allow="autoplay; fullscreen; picture-in-picture"
                                referrerpolicy="no-referrer-when-downgrade"></iframe>
                    `;
                }
            } else {
                modalWrapper.innerHTML = `
                    <video id="short-modal-player"
                           class="video-modal-player"
                           controls
                           playsinline
                           preload="metadata"${poster ? ` poster="${poster}"` : ''}
                           data-aspect-ratio="${aspectRatio}">
                        <source src="${platformUrl}">
                        Seu navegador não suporta o elemento de vídeo.
                    </video>
                `;
                initializePlyr('#short-modal-player', { ratio: aspectRatio, autoplay: true });
            }
        } else if (videoUrl) {
            modalWrapper.innerHTML = `
                <iframe src="${videoUrl}" class="video-modal-iframe" allowfullscreen loading="lazy"></iframe>
            `;
        } else {
            modalWrapper.innerHTML = '<p class="p-4 text-center text-muted">Não foi possível carregar o vídeo selecionado.</p>';
        }

        bootstrap.Modal.getOrCreateInstance(modalEl).show();
    };

    document.querySelectorAll('.video-short-card').forEach((card) => {
        card.addEventListener('click', () => openModal(card));
        card.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                openModal(card);
            }
        });
    });

    modalEl.addEventListener('hidden.bs.modal', () => {
        renderLoader();
        if (descriptionEl) {
            descriptionEl.textContent = '';
        }
        destroyPlayer();
        if (modalDialog) {
            modalDialog.style.removeProperty('--short-modal-aspect-width');
            modalDialog.style.removeProperty('--short-modal-aspect-height');
        }
        if (modalWrapper) {
            const ratioClasses = Array.from(modalWrapper.classList).filter((cls) => cls.startsWith('ratio-'));
            ratioClasses.forEach((cls) => {
                modalWrapper.classList.remove(cls);
            });
            modalWrapper.classList.add('ratio-9x16');
            modalWrapper.dataset.activeAspect = '9:16';
        }
    });
}

function enhanceStaticVideoPlayers() {
    if (typeof Plyr === 'undefined') {
        return;
    }

    const targets = document.querySelectorAll('.hero-video-player, .custom-video-player');

    targets.forEach((videoEl) => {
        if (!(videoEl instanceof HTMLVideoElement) || videoEl.dataset.plyrInitialized === 'true') {
            return;
        }

        const ratio = getAspectRatioFromElement(videoEl, '16:9');

        try {
            const instance = new Plyr(videoEl, {
                controls: [
                    'play-large',
                    'play',
                    'progress',
                    'current-time',
                    'mute',
                    'volume',
                    'settings',
                    'pip',
                    'airplay',
                    'fullscreen'
                ],
                ratio,
                tooltips: {
                    controls: true
                },
                storage: {
                    enabled: false
                },
                youtube: {
                    rel: 0,
                    modestbranding: 1,
                    playsinline: 1
                },
                vimeo: {
                    byline: false,
                    portrait: false,
                    title: false
                }
            });

            videoEl.dataset.plyrInitialized = 'true';

            videoEl.addEventListener('ended', () => {
                try {
                    instance.stop();
                } catch (error) {
                    console.warn('Não foi possível resetar o player após o término do vídeo.', error);
                }
            });
        } catch (error) {
            console.error('Falha ao aprimorar player de vídeo.', error);
        }
    });
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
    initShortVideoModal();
    enhanceStaticVideoPlayers();
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
