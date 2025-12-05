/**
 * Glossary Graph Structure
 * 
 * This file defines the topology of the interactive glossary graph:
 * - Which terms to include as nodes
 * - How they connect (edges)
 * - Visual categories for color coding
 * 
 * MANUAL CURATION: Edit this file to add/remove terms or change connections.
 * The actual definitions come from glossary.md via auto-generated glossary-definitions.js
 */

const graphStructure = {
    // Nodes - each id must match a term in glossary.md
    nodes: [
        { id: 'Active and Inactive', label: 'Active and Inactive', category: 'stage-population' },
        { id: 'Animated Value', label: 'Animated Value', category: 'value-resolution' },
        { id: 'API Schema', label: 'API Schema', category: 'schemas' },
        { id: 'Assembly', label: 'Assembly', category: 'multi-domain-schemas' },
        { id: 'Asset', label: 'Asset', category: 'multi-domain-schemas' },
        { id: 'Asset Info', label: 'Asset Info', category: 'multi-domain-schemas' },
        { id: 'Asset Resolution', label: 'Asset Resolution', category: 'resource-interface' },
        { id: 'Attribute', label: 'Attribute', category: 'composition' },
        { id: 'Attribute Block', label: 'Attribute Block', category: 'value-resolution' },
        { id: 'Change Processing', label: 'Change Processing', category: 'stage-population' },
        { id: 'Class', label: 'Class', category: 'document-data-model' },
        { id: 'Collection', label: 'Collection', category: 'multi-domain-schemas' },
        { id: 'Component', label: 'Component', category: 'multi-domain-schemas' },
        { id: 'Composition', label: 'Composition', category: 'composition' },
        { id: 'Composition Arcs', label: 'Composition Arcs', category: 'composition' },
        { id: 'Connection', label: 'Connection', category: 'document-data-model' },
        { id: 'Crate File Format', label: 'Crate File Format', category: 'file-formats' },
        { id: 'Def', label: 'Def', category: 'document-data-model' },
        { id: 'Default Value', label: 'Default Value', category: 'value-resolution' },
        { id: 'Direct Opinion', label: 'Direct Opinion', category: 'value-resolution' },
        { id: 'Fallback', label: 'Fallback', category: 'schemas' },
        { id: 'Flatten', label: 'Flatten', category: 'stage-population' },
        { id: 'Gprim', label: 'Gprim', category: 'geometry' },
        { id: 'Group', label: 'Group', category: 'multi-domain-schemas' },
        { id: 'Hydra', label: 'Hydra', category: 'rendering' },
        { id: 'Index', label: 'Index', category: 'composition' },
        { id: 'Inherit', label: 'Inherits', category: 'composition' },
        { id: 'Instanceable', label: 'Instanceable', category: 'stage-population' },
        { id: 'Instancing', label: 'Instancing', category: 'stage-population' },
        { id: 'Interpolation', label: 'Interpolation', category: 'geometry' },
        { id: 'IsA Schema', label: 'IsA Schema', category: 'schemas' },
        { id: 'Kind', label: 'Kind', category: 'multi-domain-schemas' },
        { id: 'Layer', label: 'Layer', category: 'document-data-model' },
        { id: 'Layer Offset', label: 'Layer Offset', category: 'value-resolution' },
        { id: 'Layer Stack', label: 'Layer Stack', category: 'composition' },
        { id: 'List Editing', label: 'List Editing', category: 'value-resolution' },
        { id: 'LIVERPS Strength Ordering', label: 'LIVERPS Strength Ordering', category: 'value-resolution' },
        { id: 'Load and Unload', label: 'Load and Unload', category: 'stage-population' },
        { id: 'Metadata', label: 'Metadata', category: 'composition' },
        { id: 'Model', label: 'Model', category: 'multi-domain-schemas' },
        { id: 'Model Hierarchy', label: 'Model Hierarchy', category: 'multi-domain-schemas' },
        { id: 'Namespace', label: 'Namespace', category: 'path-grammar' },
        { id: 'Opinions', label: 'Opinions', category: 'value-resolution' },
        { id: 'Over', label: 'Over', category: 'document-data-model' },
        { id: 'Path', label: 'Path', category: 'path-grammar' },
        { id: 'Path Translation', label: 'Path Translation', category: 'composition' },
        { id: 'Payload', label: 'Payload', category: 'composition' },
        { id: 'Prim', label: 'Prim', category: 'composition' },
        { id: 'Prim Definition', label: 'Prim Definition', category: 'composition' },
        { id: 'Prim Spec', label: 'Prim Spec', category: 'document-data-model' },
        { id: 'Prim Stack', label: 'Prim Stack', category: 'value-resolution' },
        { id: 'Primvar', label: 'Primvar', category: 'geometry' },
        { id: 'Property', label: 'Property', category: 'composition' },
        { id: 'Property Spec', label: 'Property Spec', category: 'document-data-model' },
        { id: 'Property Stack', label: 'Property Stack', category: 'value-resolution' },
        { id: 'Proxy', label: 'Proxy', category: 'rendering' },
        { id: 'Pseudo-Root', label: 'Pseudo-Root', category: 'stage-population' },
        { id: 'Purpose', label: 'Purpose', category: 'rendering' },
        { id: 'Reference', label: 'Reference', category: 'composition' },
        { id: 'Relationship', label: 'Relationship', category: 'composition' },
        { id: 'Relocate', label: 'Relocate', category: 'composition' },
        { id: 'Root Layer Stack', label: 'Root Layer Stack', category: 'composition' },
        { id: 'Schema', label: 'Schema', category: 'schemas' },
        { id: 'Session Layer', label: 'Session Layer', category: 'stage-population' },
        { id: 'Specialize', label: 'Specialize', category: 'composition' },
        { id: 'Specifier', label: 'Specifier', category: 'document-data-model' },
        { id: 'Stage', label: 'Stage', category: 'stage-population' },
        { id: 'Stage Traversal', label: 'Stage Traversal', category: 'stage-population' },
        { id: 'Subcomponent', label: 'Subcomponent', category: 'multi-domain-schemas' },
        { id: 'Sublayer', label: 'Sublayer', category: 'composition' },
        { id: 'Time Code', label: 'Time Code', category: 'value-resolution' },
        { id: 'Time Sample', label: 'Time Sample', category: 'value-resolution' },
        { id: 'Value Clips', label: 'Value Clips', category: 'value-resolution' },
        { id: 'Value Resolution', label: 'Value Resolution', category: 'value-resolution' },
        { id: 'Variability', label: 'Variability', category: 'value-resolution' },
        { id: 'Variant', label: 'Variant', category: 'composition' },
        { id: 'Variant Set', label: 'Variant Set', category: 'composition' },
        { id: 'Visibility', label: 'Visibility', category: 'geometry' },
    ],
    
    
    // Edges - define relationships between nodes
    edges: [
        // Stage structure
        { source: 'Stage', target: 'Pseudo-Root', label: 'contains' },
        { source: 'Stage', target: 'Composition', label: 'performs' },
        { source: 'Stage', target: 'Value Resolution', label: 'performs' },
        { source: 'Stage', target: 'Namespace', label: 'has' },
        { source: 'Stage', target: 'Flatten', label: 'can be' },
        { source: 'Stage', target: 'Change Processing', label: 'performs' },
        { source: 'Stage', target: 'Stage Traversal', label: 'performs' },
        { source: 'Stage', target: 'Session Layer', label: 'has' },
        { source: 'Stage', target: 'Root Layer Stack', label: 'has' },
        { source: 'Pseudo-Root', target: 'Stage', label: 'top level of' },
        
        // Prim relationships
        { source: 'Prim', target: 'Property', label: 'has' },
        { source: 'Prim', target: 'Specifier', label: 'has' },
        { source: 'Prim', target: 'Metadata', label: 'has' },
        { source: 'Prim', target: 'Schema', label: 'may have' },
        { source: 'Prim', target: 'Kind', label: 'may have' },
        { source: 'Prim', target: 'Path', label: 'identified by' },
        { source: 'Prim', target: 'Prim Stack', label: 'has' },
        { source: 'Prim', target: 'Prim Definition', label: 'has' },
        
        // Property relationships
        { source: 'Primvar', target: 'Attribute', label: 'type of' },
        { source: 'Primvar', target: 'Interpolation', label: 'has' },
        { source: 'Attribute', target: 'Connection', label: 'may have' },
        { source: 'Attribute', target: 'Default Value', label: 'may have' },
        { source: 'Attribute', target: 'Animated Value', label: 'may have' },
        { source: 'Attribute', target: 'Attribute Block', label: 'may have' },
        { source: 'Animated Value', target: 'Time Sample', label: 'contains' },
        { source: 'Time Sample', target: 'Time Code', label: 'contains' },
        { source: 'Time Sample', target: 'Interpolation', label: 'has' },
        { source: 'Property', target: 'Property Stack', label: 'has' },
        { source: 'Property', target: 'Variability', label: 'has' },
        
        // Schema relationships
        { source: 'IsA Schema', target: 'Schema', label: 'type of' },
        { source: 'API Schema', target: 'Schema', label: 'type of' },
        { source: 'IsA Schema', target: 'Prim', label: 'defines type of' },
        { source: 'API Schema', target: 'Prim', label: 'adds to' },
        { source: 'Schema', target: 'Fallback', label: 'provides' },
        { source: 'Fallback', target: 'Value Resolution', label: 'used by' },
        
        // Model hierarchy
        { source: 'Kind', target: 'Model', label: 'organizes' },
        { source: 'Component', target: 'Model', label: 'type of' },
        { source: 'Assembly', target: 'Group', label: 'type of' },
        { source: 'Group', target: 'Model', label: 'type of' },
        { source: 'Component', target: 'Subcomponent', label: 'contains' },
        { source: 'Model', target: 'Model Hierarchy', label: 'assemble into' },
        { source: 'Asset Info', target: 'Metadata', label: 'type of' },
        { source: 'Asset Info', target: 'Model', label: 'used with' },
        { source: 'Asset', target: 'Layer', label: 'identifies' },
        
        // Storage relationships
        { source: 'Asset Resolution', target: 'Layer', label: 'locates' },
        { source: 'Layer', target: 'Prim Spec', label: 'contains' },
        { source: 'Layer', target: 'Sublayer', label: 'can have' },
        { source: 'Layer', target: 'Crate File Format', label: 'can be encoded as' },
        { source: 'Sublayer', target: 'Layer Stack', label: 'forms' },
        { source: 'Prim Spec', target: 'Property Spec', label: 'contains' },
        { source: 'Prim Spec', target: 'Prim', label: 'composes into' },
        { source: 'Property Spec', target: 'Property', label: 'composes into' },
        
        // Composition relationships
        { source: 'Composition', target: 'Composition Arcs', label: 'uses' },
        { source: 'Composition', target: 'Index', label: 'creates' },
        { source: 'Composition', target: 'Layer', label: 'combines' },
        { source: 'Composition', target: 'Stage', label: 'produces' },
        { source: 'Composition', target: 'LIVERPS Strength Ordering', label: 'governed by' },
        { source: 'Composition', target: 'Path Translation', label: 'performs' },
        { source: 'Index', target: 'Prim', label: 'built for' },
        
        { source: 'Composition Arcs', target: 'Sublayer', label: 'includes' },
        { source: 'Composition Arcs', target: 'Inherit', label: 'includes' },
        { source: 'Composition Arcs', target: 'Variant Set', label: 'includes' },
        { source: 'Composition Arcs', target: 'Relocate', label: 'includes' },
        { source: 'Composition Arcs', target: 'Reference', label: 'includes' },
        { source: 'Composition Arcs', target: 'Payload', label: 'includes' },
        { source: 'Composition Arcs', target: 'Specialize', label: 'includes' },
        { source: 'Payload', target: 'Load and Unload', label: 'can be' },
        { source: 'Reference', target: 'Layer Offset', label: 'has' },
        { source: 'Payload', target: 'Layer Offset', label: 'has' },
        { source: 'Sublayer', target: 'Layer Offset', label: 'has' },
        { source: 'Composition Arcs', target: 'List Editing', label: 'supports' },
        { source: 'Relationship', target: 'List Editing', label: 'supports' },
        
        { source: 'Variant Set', target: 'Variant', label: 'contains' },
        
        // Value resolution
        { source: 'Value Resolution', target: 'Property', label: 'resolves' },
        { source: 'Value Resolution', target: 'Metadata', label: 'resolves' },
        { source: 'Value Resolution', target: 'Index', label: 'uses' },
        { source: 'Opinions', target: 'Property', label: 'authored for' },
        { source: 'Opinions', target: 'Metadata', label: 'authored for' },
        { source: 'Direct Opinion', target: 'Opinions', label: 'type of' },
        
        // Namespace
        { source: 'Namespace', target: 'Prim', label: 'organizes' },
        { source: 'Path', target: 'Prim', label: 'locates' },
        { source: 'Path', target: 'Property', label: 'locates' },
        { source: 'Path', target: 'Path Translation', label: 'may undergo' },
        { source: 'Relationship', target: 'Path', label: 'targets' },
        { source: 'Relationship', target: 'Property', label: 'type of' },
        { source: 'Attribute', target: 'Property', label: 'type of' },

        { source: 'Class', target: 'Specifier', label: 'type of' },
        { source: 'Def', target: 'Specifier', label: 'type of' },
        { source: 'Over', target: 'Specifier', label: 'type of' },

        { source: 'Prim', target: 'Active and Inactive', label: 'can be set to' },
        { source: 'Active and Inactive', target: 'Metadata', label: 'is' },

        { source: 'Proxy', target: 'Purpose', label: 'type of' },
        { source: 'Hydra', target: 'Purpose', label: 'renders' },

        { source: 'Instanceable', target: 'Metadata', label: 'type of' },
        { source: 'Instanceable', target: 'Instancing', label: 'controls' },
        { source: 'Visibility', target: 'Property', label: 'type of' },
        { source: 'Gprim', target: 'IsA Schema', label: 'type of' },
        { source: 'Collection', target: 'API Schema', label: 'type of' },
    ]
};

