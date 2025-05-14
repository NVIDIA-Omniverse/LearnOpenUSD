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
    'myst_parser',
    'sphinxcontrib.quizdown',
    # 'myst_nb',
    'sphinx_design'
]

templates_path = ['_templates']
exclude_patterns = []

myst_enable_extensions = ["colon_fence", 'html_image', 'attrs_inline']
myst_all_links_external = True
myst_title_to_header = True
myst_number_code_blocks = ['python']

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

from docutils import nodes
from sphinx.transforms import SphinxTransform
from sphinx.util.docutils import SphinxDirective
from pydata_sphinx_theme.translator import BootstrapHTML5TranslatorMixin
from sphinx.application import Sphinx
import types

class VideoHTMLTranslatorMixin:
    def visit_image(self, node):
        print(node)
        super().visit_image(node)
        print(node)
        if node['uri'].lower().endswith(('.mp4', '.webm', '.ogg')):
            # Create video tag with attributes
            self.body
            self.body.append(f'<video controls autoplay="autoplay" loop width="100%">')
            self.body.append(f'<source src="{node["uri"]}" type="video/mp4">')
            self.body.append('Your browser does not support the video tag.')
            self.body.append('</video>')

class VideoTransform(SphinxTransform):
    default_priority = 100

    def apply(self):
        pass

def setup_translators(app: Sphinx):
    """
    Add video HTML functionality if we are using an HTML translator.
    This re-uses the pre-existing Sphinx translator and adds extra functionality
    defined in ``VideoHTMLTranslatorMixin``.
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
        base_classes = (VideoHTMLTranslatorMixin, current_translator)
    else:
        # Otherwise use the default translator class
        base_classes = (VideoHTMLTranslatorMixin, default_translator_class)

    translator = types.new_class(
        "VideoHTMLTranslator",
        base_classes,
        {},
    )
    app.set_translator(app.builder.name, translator, override=True)

def setup(app):
    # Wait for the builder to be initialized
    app.connect('builder-inited', setup_translators)
    app.add_transform(VideoTransform)