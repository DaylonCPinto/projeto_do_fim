/**
 * Header Padding Calculator
 * 
 * This script dynamically calculates the header height and applies
 * appropriate padding to the main content to prevent overlap.
 * 
 * Features:
 * - Automatically adjusts on page load and window resize
 * - Applies a 1.25x multiplier (25% extra spacing) for better visual separation
 * - Responsive across all screen sizes
 * - Uses CSS custom properties for smooth updates
 */

(function() {
    'use strict';
    
    /**
     * Calculate and apply header padding
     */
    function updateHeaderPadding() {
        const header = document.querySelector('.modern-header');
        const mainContent = document.querySelector('main.container');
        
        if (!header || !mainContent) {
            return;
        }
        
        // Get the actual height of the header
        const headerHeight = header.offsetHeight;
        
        // Apply multiplier for extra spacing (1.25 = 25% extra)
        const paddingMultiplier = 1.25;
        const calculatedPadding = headerHeight * paddingMultiplier;
        
        // Set CSS custom property
        document.documentElement.style.setProperty('--site-header-height', `${headerHeight}px`);
        document.documentElement.style.setProperty('--calculated-padding', `${calculatedPadding}px`);
        
        // Apply the padding directly as fallback
        mainContent.style.paddingTop = `${calculatedPadding}px`;
        
        // Log for debugging (can be removed in production)
        if (window.location.search.includes('debug')) {
            console.log('Header Padding Updated:', {
                headerHeight: headerHeight + 'px',
                calculatedPadding: calculatedPadding + 'px',
                multiplier: paddingMultiplier
            });
        }
    }
    
    /**
     * Debounce function to limit resize event frequency
     */
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // Apply on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', updateHeaderPadding);
    } else {
        updateHeaderPadding();
    }
    
    // Update on window resize (debounced to avoid performance issues)
    window.addEventListener('resize', debounce(updateHeaderPadding, 150));
    
    // Also update after images load (in case header height changes)
    window.addEventListener('load', updateHeaderPadding);
    
})();
