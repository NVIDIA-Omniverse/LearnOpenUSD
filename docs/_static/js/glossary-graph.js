/**
 * Interactive Glossary Graph Visualization
 * Requires: Cytoscape.js, Dagre layout, glossaryDefinitions, graphStructure
 */

// Category colors for node visualization
const categoryColors = {
    // CORE 
    'foundational-data-types': '#B4FF00', 
    'document-data-model': '#FF6E00',      
    'path-grammar': '#DDCC00',          
    'resource-interface': '#00EEE7',     
    'composition': '#FFB400',            
    'stage-population': '#FF0901',      
    'value-resolution': '#0094FF',       
    'schemas': '#00FF2A',   
    'multi-domain-schemas': '#8200FF',
    'file-formats': '#011FFF', 

    // SCHEMA DOMAINS 
    'geometry': '#E91E8C', 
    
    // RENDERING 
    'rendering': '#00B4D8', 
    
    // MISCELLANEOUS
    'miscellaneous': '#90C952'
};

// Global Cytoscape instance
let cy = null;

/**
 * Check if we're on mobile/tablet
 */
function isMobile() {
    return window.innerWidth <= 1024;
}

/**
 * Open the mobile drawer
 */
function openDrawer() {
    if (!isMobile()) {
        return;
    }
    
    const sidebar = document.getElementById('glossary-sidebar');
    
    if (sidebar) {
        sidebar.classList.add('open');
        // Prevent body scroll
        document.body.style.overflow = 'hidden';
    }
}

/**
 * Close the mobile drawer
 */
function closeDrawer() {
    const sidebar = document.getElementById('glossary-sidebar');
    
    if (sidebar) {
        sidebar.classList.remove('open');
        // Restore body scroll
        document.body.style.overflow = '';
    }
}

// Make closeDrawer available globally for onclick
window.closeDrawer = closeDrawer;

/**
 * Populate legend colors from categoryColors
 */
function populateLegendColors() {
    // Populate both desktop and mobile legends
    const legendItems = document.querySelectorAll('#glossary-legend-desktop .legend-item[data-category], #glossary-legend-mobile .legend-item[data-category]');
    legendItems.forEach(item => {
        const category = item.getAttribute('data-category');
        const colorBox = item.querySelector('.legend-color');
        if (colorBox && categoryColors[category]) {
            colorBox.style.backgroundColor = categoryColors[category];
        }
    });
}

/**
 * Initialize the interactive glossary graph
 */
function initGlossaryGraph() {
    // Initialize legends
    initializeLegends();
    
    // Populate legend colors
    populateLegendColors();
    
    // Check if required data is available
    if (typeof glossaryDefinitions === 'undefined') {
        return;
    }
    
    if (typeof graphStructure === 'undefined') {
        return;
    }
    
    // Check if Cytoscape is available
    if (typeof cytoscape === 'undefined') {
        return;
    }
    
    // Check if container exists
    const container = document.getElementById('cy');
    if (!container) {
        return;
    }
    
    // Build elements array from structure
    const elements = [
        ...graphStructure.nodes.map(node => ({ data: node })),
        ...graphStructure.edges.map(edge => ({ data: edge }))
    ];
    
    // Initialize Cytoscape
    try {
        cy = cytoscape({
        container: document.getElementById('cy'),
        elements: elements,
        wheelSensitivity: 0.2,
        minZoom: 0.1,
        maxZoom: 10,
        style: [
            {
                selector: 'node',
                style: {
                    'background-color': function(ele) {
                        return categoryColors[ele.data('category')] || '#999';
                    },
                    'label': 'data(label)',
                    'color': '#fff',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'font-size': '18px',
                    'font-weight': 'bold',
                    'width': 120,
                    'height': 120,
                    'border-width': 3,
                    'border-color': '#000',
                    'text-wrap': 'wrap',
                    'text-max-width': '110px'
                }
            },
            {
                selector: 'node:selected',
                style: {
                    'border-width': 4,
                    'border-color': '#FFD700',
                    'background-color': function(ele) {
                        const baseColor = categoryColors[ele.data('category')] || '#999';
                        return baseColor;
                    }
                }
            },
            {
                selector: 'edge',
                style: {
                    'width': 2,
                    'line-color': '#555',
                    'target-arrow-color': '#555',
                    'target-arrow-shape': 'triangle',
                    'arrow-scale': 1.5,
                    'curve-style': 'bezier',
                    'label': 'data(label)',
                    'font-size': '18px',
                    'color': '#bbb',
                    'font-weight': '500',
                    'text-rotation': 'autorotate',
                    'text-background-color': '#2d2d30',
                    'text-background-opacity': 0.95,
                    'text-background-padding': '5px',
                    'text-border-width': 1,
                    'text-border-color': '#3e3e42',
                    'text-border-opacity': 0.5
                }
            },
            {
                selector: 'edge.highlighted',
                style: {
                    'line-color': '#FFD700',
                    'target-arrow-color': '#FFD700',
                    'width': 2
                }
            },
            {
                selector: 'node.highlighted',
                style: {
                    'border-width': 3,
                    'border-color': '#FFD700'
                }
            },
            {
                selector: 'node.dimmed',
                style: {
                    'opacity': 0.3
                }
            },
            {
                selector: 'edge.dimmed',
                style: {
                    'opacity': 0.1
                }
            }
        ],
        layout: {
            name: 'dagre',
            rankDir: 'LR',
            nodeSep: 50,
            rankSep: 250,
            padding: 80
        }
    });
    
    // Set up event handlers
    setupEventHandlers();
    
    // Initial fit
    cy.ready(function() {
        cy.fit();
    });
    
    } catch (error) {
        // Silent fail
    }
}

/**
 * Set up event handlers for the graph
 */
function setupEventHandlers() {
    // Node click handler
    cy.on('tap', 'node', function(evt) {
        const node = evt.target;
        const id = node.data('id');
        const def = glossaryDefinitions[id];
        
        if (def) {
            showDefinition(def);
            
            // Highlight connected nodes and edges
            cy.elements().removeClass('highlighted dimmed');
            cy.elements().addClass('dimmed');
            
            node.removeClass('dimmed').addClass('highlighted');
            node.connectedEdges().removeClass('dimmed').addClass('highlighted');
            node.connectedEdges().connectedNodes().removeClass('dimmed').addClass('highlighted');
        }
    });
    
    // Background click handler
    cy.on('tap', function(evt) {
        if (evt.target === cy) {
            cy.elements().removeClass('highlighted dimmed');
            showPlaceholder();
            
            // On mobile, close the drawer when clicking background
            if (isMobile()) {
                closeDrawer();
            }
        }
    });
}

/**
 * Get legend content HTML (without wrapper - used by both desktop and mobile)
 */
function getLegendContentHtml() {
    return `
        <h3>Core</h3>
        <div class="legend-item" data-category="document-data-model">
            <div class="legend-color"></div>
            <span>Document Data Model</span>
        </div>
        <div class="legend-item" data-category="path-grammar">
            <div class="legend-color"></div>
            <span>Path Grammar</span>
        </div>
        <div class="legend-item" data-category="resource-interface">
            <div class="legend-color"></div>
            <span>Resources Interface</span>
        </div>
        <div class="legend-item" data-category="composition">
            <div class="legend-color"></div>
            <span>Composition</span>
        </div>
        <div class="legend-item" data-category="stage-population">
            <div class="legend-color"></div>
            <span>Stage Population</span>
        </div>
        <div class="legend-item" data-category="value-resolution">
            <div class="legend-color"></div>
            <span>Value Resolution</span>
        </div>
        <div class="legend-item" data-category="schemas">
            <div class="legend-color"></div>
            <span>Schemas</span>
        </div>
        <div class="legend-item" data-category="multi-domain-schemas">
            <div class="legend-color"></div>
            <span>Multi-Domain Schemas</span>
        </div>
        <div class="legend-item" data-category="file-formats">
            <div class="legend-color"></div>
            <span>File Formats</span>
        </div>
        
        <h3 style="margin-top: 12px;">Schema Domains</h3>
        <div class="legend-item" data-category="geometry">
            <div class="legend-color"></div>
            <span>Geometry</span>
        </div>
        
        <h3 style="margin-top: 12px;">Rendering</h3>
        <div class="legend-item" data-category="rendering">
            <div class="legend-color"></div>
            <span>Rendering</span>
        </div>
        
        <h3 style="margin-top: 12px;">Miscellaneous</h3>
        <div class="legend-item" data-category="miscellaneous">
            <div class="legend-color"></div>
            <span>Miscellaneous</span>
        </div>
    `;
}

/**
 * Get legend HTML for desktop (inside sidebar)
 */
function getLegendDesktopHtml() {
    return `<div id="glossary-legend-desktop">${getLegendContentHtml()}</div>`;
}

/**
 * Initialize legends on page load
 */
function initializeLegends() {
    // Initialize mobile legend (fixed overlay)
    const mobileLegend = document.getElementById('glossary-legend-mobile');
    if (mobileLegend) {
        mobileLegend.innerHTML = getLegendContentHtml();
    }
    
    // Initialize desktop legend in sidebar
    const sidebar = document.getElementById('glossary-sidebar');
    if (sidebar) {
        // Check if there's already content, append legend after it
        const existingContent = sidebar.innerHTML;
        sidebar.innerHTML = existingContent + getLegendDesktopHtml();
    }
}

/**
 * Show definition in sidebar
 */
function showDefinition(def) {
    const sidebar = document.getElementById('glossary-sidebar');
    
    // Build links HTML with proper text and URLs
    const linksHtml = def.links.map(link => {
        // Handle both old format (string) and new format (object with text/url)
        if (typeof link === 'object' && link.text && link.url) {
            return `<a href="${link.url}" target="_blank">${link.text}</a>`;
        } else {
            // Fallback for old format
            return `<a href="${link}" target="_blank">${link}</a>`;
        }
    }).join('');
    
    // Use descriptionHtml if available, fallback to description
    const descriptionContent = def.descriptionHtml || def.description || '';
    
    sidebar.innerHTML = `
        <div class="mobile-drawer-handle"></div>
        <h2>${def.title}</h2>
        ${def.aka ? `<div class="aka">Also Known As: ${def.aka}</div>` : ''}
        <div class="description">${descriptionContent}</div>
        <div class="links">
            <strong>Further Reading:</strong>
            ${linksHtml}
        </div>
        ${getLegendDesktopHtml()}
    `;
    
    // Re-populate legend colors after DOM update
    populateLegendColors();
    
    // On mobile, open the drawer
    if (isMobile()) {
        openDrawer();
    }
}

/**
 * Show placeholder in sidebar
 */
function showPlaceholder() {
    const sidebar = document.getElementById('glossary-sidebar');
    sidebar.innerHTML = `
        <div class="mobile-drawer-handle"></div>
        <div class="glossary-placeholder">
            <h2>USD Glossary Graph</h2>
            <p>Click on any node to see its definition</p>
        </div>
        ${getLegendDesktopHtml()}
    `;
    
    // Re-populate legend colors after DOM update
    populateLegendColors();
    
    // On mobile, close the drawer
    if (isMobile()) {
        closeDrawer();
    }
}

/**
 * Reset view to initial state
 */
function resetView() {
    if (cy) {
        cy.elements().removeClass('highlighted dimmed');
        cy.fit();
        showPlaceholder();
    }
}

/**
 * Toggle sidebar visibility
 */
function toggleSidebar() {
    const sidebar = document.getElementById('glossary-sidebar');
    
    if (isMobile()) {
        // On mobile, toggle the drawer
        if (sidebar.classList.contains('open')) {
            closeDrawer();
        } else {
            openDrawer();
        }
    } else {
        // On desktop, toggle visibility
        sidebar.classList.toggle('hidden');
    }
}

/**
 * Fit graph to screen
 */
function fitGraph() {
    if (cy) {
        cy.fit();
    }
}

/**
 * Search functionality
 */
function searchTerms(event) {
    if (!cy) return;
    
    const searchText = event.target.value.toLowerCase();
    
    if (searchText.length === 0) {
        cy.elements().removeClass('highlighted dimmed');
        return;
    }
    
    cy.elements().addClass('dimmed');
    
    const matchingNodes = cy.nodes().filter(function(node) {
        return node.data('label').toLowerCase().includes(searchText);
    });
    
    matchingNodes.removeClass('dimmed').addClass('highlighted');
    
    if (matchingNodes.length > 0) {
        cy.fit(matchingNodes, 50);
    }
}

/**
 * Add swipe-to-close support for mobile drawer
 */
function addSwipeSupport() {
    const sidebar = document.getElementById('glossary-sidebar');
    if (!sidebar) return;
    
    let startY = 0;
    let currentY = 0;
    let isDragging = false;
    
    sidebar.addEventListener('touchstart', (e) => {
        if (!isMobile()) return;
        startY = e.touches[0].clientY;
        isDragging = true;
    }, { passive: true });
    
    sidebar.addEventListener('touchmove', (e) => {
        if (!isMobile() || !isDragging) return;
        currentY = e.touches[0].clientY;
        const diff = currentY - startY;
        
        // Only allow downward swipe
        if (diff > 0) {
            sidebar.style.transform = `translateY(${Math.min(diff, 100)}px)`;
        }
    }, { passive: true });
    
    sidebar.addEventListener('touchend', () => {
        if (!isMobile() || !isDragging) return;
        isDragging = false;
        
        const diff = currentY - startY;
        
        // Reset transform
        sidebar.style.transform = '';
        
        // Close if swiped down more than 80px
        if (diff > 80) {
            closeDrawer();
        }
    }, { passive: true });
}

/**
 * Handle window resize
 */
let resizeTimer;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
        // Close drawer if switching from mobile to desktop
        if (!isMobile()) {
            const sidebar = document.getElementById('glossary-sidebar');
            if (sidebar) sidebar.classList.remove('open');
            document.body.style.overflow = '';
        }
        
        // Resize and refit graph
        if (cy) {
            cy.resize();
            cy.fit();
        }
    }, 250);
});

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        initGlossaryGraph();
        setTimeout(addSwipeSupport, 100);
    });
} else {
    initGlossaryGraph();
    setTimeout(addSwipeSupport, 100);
}

