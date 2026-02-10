# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import importlib.metadata
from pathlib import Path
import posixpath
import re
import shutil
import subprocess
import sys
import types
import urllib.parse
import zipfile

from docutils import nodes
from sphinx.transforms import SphinxTransform
from sphinx.util.docutils import SphinxDirective
from sphinx.application import Sphinx

from sphinxcontrib.doxylink.doxylink import Entry

from myst_nb.sphinx_ import SphinxNbRenderer
from myst_parser.mdit_to_docutils.base import token_line


project = 'Learn OpenUSD'
copyright = '2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved'
author = 'NVIDIA'
release = importlib.metadata.version("lousd")

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.intersphinx',
    'sphinxcontrib.doxylink',
    'myst_nb',
    'sphinx_design',
    'sphinx_copybutton',
    'sphinx_tippy',
    'lousd.directives',
]

# Skip all URLs that don't match glossary term pattern
# This regex matches any URL that does NOT contain 'glossary.html#term-'
tippy_skip_urls = (r"^(?!.*glossary\.html#term-).*$",)

templates_path = ['_templates']
exclude_patterns = ['_includes/**', '_build', 'Thumbs.db', '.DS_Store']
myst_enable_extensions = ['colon_fence', 'html_image', 'attrs_inline', 'attrs_block']
myst_title_to_header = True
myst_number_code_blocks = ['python', 'py', 'usda', 'usd']
myst_links_external_new_tab = True
myst_heading_anchors = 3
nb_number_source_lines = True
nb_execution_mode = "cache"

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'usd': ('https://openusd.org/release', None),
    'usdpy': ('https://docs.omniverse.nvidia.com/kit/docs/pxr-usd-api/latest', None)
}

doxylink = {
    'usdcpp' : ('https://openusd.org/release/USD.tag', 'https://openusd.org/release/api')
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# TODO: Remove the two following parameters when the theme is fixed
toc_object_entries_show_parents = 'hide'
maximum_signature_line_length = 70



html_theme = 'nvidia_sphinx_theme'
html_static_path = ['_static']
html_css_files = ['css/lousd_custom.css']
html_theme_options = {
    "secondary_sidebar_items": {
        "**": ["page-toc"],
        "glossary": ["glossary-toc"],
    },
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/NVIDIA-Omniverse/LearnOpenUSD",
            "icon": "fa-brands fa-github",
        }
    ],
    "extra_head": {
        """
    <script src="https://assets.adobedtm.com/5d4962a43b79/c1061d2c5e7b/launch-191c2462b890.min.js" ></script>
    """
    },
    "extra_footer": {
        """
    <script type="text/javascript">if (typeof _satellite !== "undefined") {_satellite.pageBottom();}</script>
    """
    },
}



def _new_render_nb_cell_code_source(self, token) -> None:
    """Render a notebook code cell's source."""
    cell_index = token.meta["index"]
    line = token_line(token, 0) or None
    node = self.create_highlighted_code_block(
        token.content,
        self._get_nb_source_code_lexer(cell_index, line=line),
        number_lines=self.get_cell_level_config(
            "number_source_lines",
            token.meta["metadata"],
            line=line,
        ),
        source=self.document["source"],
        line=token_line(token),
        emphasize_lines=token.meta["metadata"].get("emphasize-lines", None),
    )
    self.add_line_and_source_path(node, token)
    self.current_node.append(node)


# Store original method
original_render_nb_cell = SphinxNbRenderer._render_nb_cell_code_source
# Replace the method
SphinxNbRenderer._render_nb_cell_code_source = _new_render_nb_cell_code_source


class LOUSDHTMLTranslatorMixin:
    def visit_image(self, node):
        if node['uri'].lower().endswith(('.mp4', '.webm', '.ogg')):
            olduri = node['uri']
            # rewrite the URI if the environment knows about it
            if olduri in self.builder.images:
                node['uri'] = posixpath.join(
                    self.builder.imgpath, urllib.parse.quote(self.builder.images[olduri])
                )
                # Create video tag with attributes
                self.body.append('<video controls autoplay loop width="100%">')
                self.body.append(f'<source src="{node["uri"]}" type="video/webm">')
                self.body.append('Your browser does not support the video tag.')
                self.body.append('</video>')
        else:
            super().visit_image(node)


def setup_translators(app: Sphinx):
    """
    This re-uses the pre-existing Sphinx translator and adds extra functionality
    defined in ``LOUSDHTMLTranslatorMixin``.
    """
    if app.builder.format != "html":
        return

    try:
        default_translator_class = app.builder.default_translator_class
    except AttributeError:
        print("No default translator class")
        return

    # Get the current translator class
    current_translator = app.registry.translators.get(app.builder.name)
    if current_translator:
        # If we already have a translator, use it as the base
        base_classes = (LOUSDHTMLTranslatorMixin, current_translator)
    else:
        print("default_translator_class")
        # Otherwise use the default translator class
        base_classes = (LOUSDHTMLTranslatorMixin, default_translator_class)

    translator = types.new_class(
        "LOUSDHTMLTranslator",
        base_classes,
        {},
    )
    app.set_translator(app.builder.name, translator, override=True)


def copy_asset_folders(app, exception):
    if exception is not None:
        return
    
    source_dir = Path(app.srcdir)
    build_dir = Path(app.outdir)
    
    for assets_path in source_dir.rglob('_assets'):
        if assets_path.is_dir():
            # Skip if the assets path is within _build directory
            try:
                assets_path.relative_to(source_dir / '_build')
                continue  # Skip this path as it's in _build
            except ValueError:
                pass  # Not in _build, continue processing
            
            # Get the relative path from source directory
            rel_path = assets_path.relative_to(source_dir)
            dst_assets = build_dir / rel_path
            
            # Copy the assets folder
            shutil.copytree(assets_path, dst_assets, dirs_exist_ok=True)
            print(f"Copied {assets_path} to {dst_assets}")


def create_exercises_archives(app, exception):
    exercises_dir = Path(app.srcdir) / 'exercise_content'
    build_static_dir = Path(app.outdir) / '_static'
    
    for exercises in exercises_dir.iterdir():
        if exercises.is_dir():
            # Create zip file for exercises
            zip_file_name = f"{exercises.name}-exercise-files.zip".replace("_", "-")
            zip_file_path = build_static_dir / zip_file_name
            with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
                for file in exercises.rglob('*'):
                    if file.is_file():
                        zip_file.write(file, file.relative_to(exercises.parent))
            print(f"Created {zip_file_path}")

JUPYTEXT_MARKER = re.compile(r"^jupytext:", re.MULTILINE)

def convert_jupytext_notebooks(app, exception):
    """Convert Jupytext .md files to .ipynb notebooks in the build output."""
    if exception is not None:
        return

    source_dir = Path(app.srcdir)
    build_dir = Path(app.outdir)
    notebooks_dir = build_dir / 'notebooks'

    files = []
    for md_file in source_dir.rglob('*.md'):
        if '.ipynb_checkpoints' in md_file.parts:
            continue
        try:
            md_file.relative_to(source_dir / '_build')
            continue
        except ValueError:
            pass
        try:
            text = md_file.read_text(encoding='utf-8', errors='ignore')
        except OSError:
            continue
        if JUPYTEXT_MARKER.search(text):
            files.append(md_file)

    if not files:
        return

    print(f"Converting {len(files)} Jupytext files to notebooks...")
    for md_file in sorted(files):
        rel = md_file.relative_to(source_dir)
        out_dir = notebooks_dir / rel.parent
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / rel.with_suffix('.ipynb').name
        subprocess.run(
            [sys.executable, '-m', 'jupytext', '--to', 'notebook', str(md_file), '-o', str(out_file)],
            check=True,
        )
        print(f"  {rel} -> {out_file.relative_to(build_dir)}")


def extract_glossary_from_html(app, exception):
    """Extract glossary data from the rendered HTML file for interactive graph visualization."""
    if exception is not None:
        return
    
    import json
    from pathlib import Path
    from html.parser import HTMLParser
    
    glossary_html_file = Path(app.outdir) / 'glossary.html'
    
    if not glossary_html_file.exists():
        print("Warning: glossary.html not found, skipping graph data extraction")
        return
    
    class GlossaryHTMLParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.glossary_data = {}
            self.current_term = None
            self.current_aka = None
            self.in_dd = False
            self.in_aka_para = False
            self.in_further_reading_para = False
            self.description_html = []
            self.current_links = []
            self.capture_html = False
            self.html_buffer = []
            
        def handle_starttag(self, tag, attrs):
            attrs_dict = dict(attrs)
            
            # Start of a term
            if tag == 'dt' and 'id' in attrs_dict and attrs_dict['id'].startswith('term-'):
                self.current_term = None
                self.current_aka = None
                self.description_html = []
                self.current_links = []
                
            # Start of definition
            elif tag == 'dd':
                self.in_dd = True
                self.capture_html = False
                
            # Paragraph in definition
            elif tag == 'p' and self.in_dd:
                self.html_buffer = []
                self.capture_html = True
                
            # Links in Further Reading
            elif tag == 'a' and self.in_further_reading_para:
                link_url = attrs_dict.get('href', '')
                self.current_link_url = link_url
                self.current_link_text = []
                
            # Capture HTML for description (but not the <p> tag itself)
            if self.capture_html and not self.in_aka_para and not self.in_further_reading_para and tag != 'p':
                self.html_buffer.append(self.get_starttag_text())
                
        def handle_endtag(self, tag):
            if tag == 'dt':
                pass
                
            elif tag == 'dd':
                # Save the term
                if self.current_term and self.description_html:
                    self.glossary_data[self.current_term] = {
                        'title': self.current_term,
                        'aka': self.current_aka,
                        'description_html': ''.join(self.description_html),
                        'links': self.current_links.copy()
                    }
                self.in_dd = False
                
            elif tag == 'p':
                if self.capture_html:
                    # Check if this paragraph had metadata
                    if not self.in_aka_para and not self.in_further_reading_para:
                        # Wrap content in <p> tags for proper paragraph spacing
                        para_content = ''.join(self.html_buffer).strip()
                        if para_content:
                            self.description_html.append(f'<p>{para_content}</p>')
                    self.html_buffer = []
                    self.capture_html = False
                    self.in_aka_para = False
                    self.in_further_reading_para = False
                    
            elif tag == 'a' and self.in_further_reading_para and hasattr(self, 'current_link_url'):
                link_text = ''.join(self.current_link_text)
                self.current_links.append({
                    'text': link_text,
                    'url': self.current_link_url
                })
                
            # Capture HTML for description (but not the </p> tag itself)
            if self.capture_html and not self.in_aka_para and not self.in_further_reading_para and tag != 'p':
                self.html_buffer.append(f'</{tag}>')
                
        def handle_data(self, data):
            # Extract term name from dt
            if not self.in_dd and data.strip() and not self.current_term:
                # Skip if it's just '#'  (headerlink)
                if data.strip() != '#':
                    self.current_term = data.strip()
                    
            # Check for metadata markers
            if self.capture_html:
                stripped_data = data.strip()
                
                if 'Also Known As:' in data:
                    self.in_aka_para = True
                    self.html_buffer = []  # Clear buffer for this para
                    
                elif 'Further Reading' in data:
                    self.in_further_reading_para = True
                    self.html_buffer = []  # Clear buffer for this para
                    
                # Capture link text
                elif self.in_further_reading_para and hasattr(self, 'current_link_text'):
                    self.current_link_text.append(data)
                    
                # Capture aka text (in emphasis tags)
                elif self.in_aka_para:
                    if stripped_data and stripped_data != 'Also Known As:':
                        self.current_aka = stripped_data
                        
                # Capture description HTML
                elif not self.in_aka_para and not self.in_further_reading_para:
                    self.html_buffer.append(data)
    
    # Parse the glossary HTML
    with open(glossary_html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    parser = GlossaryHTMLParser()
    parser.feed(html_content)
    glossary_data = parser.glossary_data
    
    # Save as JavaScript file
    if glossary_data:
        output_dir = Path(app.outdir) / '_static' / 'data'
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / 'glossary-definitions.js'
        
        # Generate JavaScript content
        js_content = "// Auto-generated glossary definitions from glossary.md\n"
        js_content += "// DO NOT EDIT DIRECTLY - Edit docs/glossary.md instead\n\n"
        js_content += "const glossaryDefinitions = {\n"
        
        for term, data in sorted(glossary_data.items()):
            # Escape strings for JavaScript
            title = data['title'].replace('\\', '\\\\').replace('"', '\\"')
            aka = data['aka'].replace('\\', '\\\\').replace('"', '\\"') if data['aka'] else None
            # For HTML, use JSON.stringify-style escaping for backticks
            description_html = data['description_html'].replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')
            
            js_content += f'    "{title}": {{\n'
            js_content += f'        title: "{title}",\n'
            
            if aka:
                js_content += f'        aka: "{aka}",\n'
            else:
                js_content += f'        aka: null,\n'
            
            # Use template literal for HTML content
            js_content += f'        descriptionHtml: `{description_html}`,\n'
            js_content += f'        links: [\n'
            
            for link in data['links']:
                link_text = link['text'].replace('\\', '\\\\').replace('`', '\\`')
                link_url = link['url'].replace('\\', '\\\\').replace('`', '\\`')
                js_content += f'            {{text: `{link_text}`, url: `{link_url}`}},\n'
            
            js_content += '        ]\n'
            js_content += '    },\n'
        
        js_content += "};\n"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(js_content)
        
        # Count nodes in graph structure for comparison
        graph_structure_file = output_dir / 'glossary-graph-structure.js'
        node_count = 0
        if graph_structure_file.exists():
            try:
                with open(graph_structure_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Count node entries in the nodes array
                    # Look for { id: 'Term', ... } patterns
                    node_matches = re.findall(r'\{\s*id:\s*[\'"]([^\'"]+)[\'"]', content)
                    node_count = len(node_matches)
            except Exception as e:
                print(f"Warning: Could not count nodes in graph structure: {e}")
        
        print(f"Glossary graph data: Extracted {len(glossary_data)} definitions from glossary.md")
        if node_count > 0:
            print(f"                     Graph structure has {node_count} nodes")
            if len(glossary_data) < node_count:
                print(f"                     ⚠️  Warning: {node_count - len(glossary_data)} nodes missing definitions!")
            elif len(glossary_data) > node_count:
                print(f"                     ℹ️  Note: {len(glossary_data) - node_count} definitions not shown in graph")
        print(f"Generated {output_file}")
    else:
        print("Warning: No glossary data extracted from doctree")

def monkey_patch_doxylink(app: Sphinx):
    print("Monkey patching doxylink entries to add details anchor to class and group entries")
    try:
        new_entries = []
        for entry in app.env.doxylink_cache['usdcpp']['mapping']._entries:
            if entry.kind in ("class", "group"):
                new_entry = Entry(name=f"{entry.name} Details", kind="anchor", file=f"{entry.file}#details", arglist=None)
                new_entries.append(new_entry)
        app.env.doxylink_cache['usdcpp']['mapping']._entries.extend(new_entries)
        app.env.doxylink_cache['usdcpp']['mapping']._entries.sort()
    except Exception as e:
        print(f"Warning: Failed to patch doxylink entries: {e}")

def add_glossary_toc(app, pagename, templatename, context, doctree):
    """Extract glossary terms and add them to the template context for the sidebar."""
    if doctree is None:
        return
    
    glossary_terms = []
    
    # Find all definition lists that are glossaries (they have 'glossary' class)
    for deflist in doctree.traverse(nodes.definition_list):
        # Check if this is a glossary (has the 'glossary' class)
        if 'glossary' in deflist.get('classes', []):
            # Iterate through definition list items
            for deflist_item in deflist:
                if isinstance(deflist_item, nodes.definition_list_item):
                    # Get the term node (first child is the term)
                    for term_node in deflist_item.traverse(nodes.term):
                        term_text = term_node.astext()
                        # Look for the target node with the ID
                        term_id = None
                        for target in term_node.traverse(nodes.target):
                            if 'ids' in target and target['ids']:
                                term_id = target['ids'][0]
                                break
                        # If no explicit ID, generate one
                        if not term_id:
                            term_id = 'term-' + term_text.replace(' ', '-')
                        glossary_terms.append({
                            'text': term_text,
                            'id': term_id
                        })
    
    # Add glossary terms to the context
    context['glossary_terms'] = glossary_terms

def setup(app):
    # Wait for the builder to be initialized
    app.connect('builder-inited', setup_translators)
    app.connect('builder-inited', monkey_patch_doxylink)
    app.connect('html-page-context', add_glossary_toc)
    app.connect('build-finished', extract_glossary_from_html)
    app.connect('build-finished', create_exercises_archives)
    app.connect('build-finished', copy_asset_folders)
    app.connect('build-finished', convert_jupytext_notebooks)
    