# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Learn OpenUSD'
copyright = '2025, NVIDIA'
author = 'NVIDIA'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.intersphinx',
    'sphinxcontrib.doxylink',
    # 'myst_parser',
    'sphinxcontrib.quizdown',
    'myst_nb',
    'sphinx_design',
    'directives'
]

templates_path = ['_templates']
exclude_patterns = []

myst_enable_extensions = ["colon_fence", 'html_image', 'attrs_inline']
myst_all_links_external = True
myst_title_to_header = True
myst_number_code_blocks = ['python']
nb_number_source_lines = True
nb_execution_mode = "cache"
# nb_render_markdown_format = "myst"

quizdown_config = {
    'start_on_load': True,			# detect and convert all divs with class quizdown
    'shuffle_answers': True,		# shuffle answers for each question
    'primary_color': '#76b900',     # primary CSS color
    'secondary_color': '#F0F0F0',   # secondary CSS color
    'text_color': 'black',          # text color of interactive elements
    'locale': 'en'                  # language of text in user interface
}

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

html_theme = 'nvidia_sphinx_theme'
html_static_path = ['_static']
html_css_files = ['css/lousd_custom.css']


from pathlib import Path
import posixpath
import shutil
import types
import urllib.parse


from docutils import nodes
from sphinx.transforms import SphinxTransform
from sphinx.util.docutils import SphinxDirective
from sphinx.application import Sphinx

from myst_nb.sphinx_ import SphinxNbRenderer
from myst_parser.mdit_to_docutils.base import token_line
# Store original method
original_render_nb_cell = SphinxNbRenderer._render_nb_cell_code_source

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

class VideoTransform(SphinxTransform):
    default_priority = 100

    def apply(self):
        pass

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
    
    for assets_path in source_dir.rglob('assets'):
        if assets_path.is_dir():
            # Get the relative path from source directory
            rel_path = assets_path.relative_to(source_dir)
            dst_assets = build_dir / rel_path
            
            # Copy the assets folder
            shutil.copytree(assets_path, dst_assets, dirs_exist_ok=True)
            print(f"Copied {assets_path} to {dst_assets}")

def setup(app):
    # Wait for the builder to be initialized
    app.connect('builder-inited', setup_translators)
    app.connect('build-finished', copy_asset_folders)
    # app.add_transform(VideoTransform)