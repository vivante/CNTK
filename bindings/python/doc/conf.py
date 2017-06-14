import re
import os
import sys

try:
    import cntk
except ImportError:
    raise ImportError("Unable to import cntk; the cntk module needs to be built "
                      "and importable to generate documentation")

from cntk.sample_installer import module_is_unreleased

try:
    import sphinx_rtd_theme
except ImportError:
    raise ImportError("Unable to import sphinx_rtd_theme, please install via "
                      "'pip install sphinx_rtd_theme'")

IS_SPHINX_DOCFX_BUILD = 'SPHINX_DOCFX_BUILD' in os.environ.keys()

if IS_SPHINX_DOCFX_BUILD:
    sys.path.insert(0, os.path.abspath('.'))
    sys.path.append(os.path.abspath('.'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.extlinks',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

if IS_SPHINX_DOCFX_BUILD:
    extensions.append('docfx_yaml.extension')
    # TODO todo nodes aren't handled yet
else:
    extensions.append('sphinx.ext.todo')

master_doc = 'index'

exclude_patterns = [
    '_build',
    'images',
    'test',
]

autodoc_mock_imports = [
    'tensorflow',
]

needs_sphinx = '1.5'

# TODO nitpick_ignore

project = 'Python API for CNTK'
copyright = '2017, Microsoft'

version = cntk.__version__ # TODO consider shortening
release = cntk.__version__

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# Do not prepend the current module to all description unit titles (such as ..
# function::).
add_module_names = False

# The theme to use for HTML and HTML Help pages.
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# Linkcheck builder options
def re_exact_match(s):
  return re.compile('^' + re.escape(s) + '$')

linkcheck_anchors_ignore = [
  # Important: Github Wiki anchors (for sections refs) yield errors in
  # link-checking and need to be manually checked. Current exception to make
  # the build pass are listed here:
  re_exact_match('21-data-parallel-training-with-1-bit-sgd'),
  re_exact_match('22-block-momentum-sgd'),
  re_exact_match('converting-learning-rate-and-momentum-parameters-from-other-toolkits'),
  re_exact_match('for-python'),
  re_exact_match('base64imagedeserializer-options'),
]

# Used by sphinx-docfx-yaml to prefix source paths:
source_prefix = 'bindings/python'

github_source_prefix = 'https://github.com/Microsoft/CNTK/blob/'
if module_is_unreleased():
    github_source_prefix += 'master'
else:
    # TODO temporary
    github_source_prefix += 'v%s' % (cntk.__version__.replace("rc", ".rc"))

# sphinx.ext.extlinks options
extlinks = {
    'cntk': (github_source_prefix + '/%s', ''),
    'cntktut': (github_source_prefix + '/Tutorials/%s.ipynb', ''),
    # CNTK Wiki has moved to a new site:
    'cntkwiki': ('https://docs.microsoft.com/en-us/cognitive-toolkit/%s', 'CNTK Doc - ')
}

# sphinx.ext.napoleon options
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_use_admonition_for_examples = IS_SPHINX_DOCFX_BUILD

# sphinx.ext.todo options
todo_include_todos = module_is_unreleased()
