# OpenUSD Interactive Glossary

Explore the relationships between OpenUSD concepts in this interactive visualization.

## How to Use

- **Click a node** to view its full definition in the sidebar
- **Search** for specific terms using the search box
- **Pan** by clicking and dragging the background
- **Zoom** using your mouse wheel or trackpad
- **Reset View** to return to the default layout

For complete definitions and more details, see the [full Glossary](glossary.md).

```{raw} html
<link rel="stylesheet" href="./_static/css/glossary-graph.css">
<script src="https://unpkg.com/cytoscape@3.28.1/dist/cytoscape.min.js"></script>
<script src="https://unpkg.com/dagre@0.8.5/dist/dagre.min.js"></script>
<script src="https://unpkg.com/cytoscape-dagre@2.5.0/cytoscape-dagre.js"></script>

<div id="glossary-graph-wrapper">
    <!-- Mobile backdrop -->
    <!-- Top toolbar with controls and search -->
    <div id="glossary-toolbar">
        <div id="glossary-controls">
            <button onclick="resetView()">Reset View</button>
        </div>
        <div id="glossary-search">
            <input type="text" id="searchInput" placeholder="Search terms..." onkeyup="searchTerms(event)">
        </div>
    </div>
    
    <!-- Main graph container -->
    <div id="glossary-graph-container">
        <div id="cy"></div>
        <div id="glossary-sidebar">
            <div class="mobile-drawer-handle"></div>
            <div class="glossary-placeholder">
                <h2>USD Glossary Graph</h2>
                <p>Click on any node to see its definition</p>
            </div>
            <!-- Legend will be inserted here by JavaScript -->
        </div>
        
        <!-- Legend - mobile only (inserted by JavaScript) -->
        <div id="glossary-legend-mobile"></div>
    </div>
</div>

<script src="./_static/data/glossary-definitions.js"></script>
<script src="./_static/data/glossary-graph-structure.js"></script>
<script src="./_static/js/glossary-graph.js"></script>
```



