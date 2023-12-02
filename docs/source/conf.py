import sys
import os

sys.path.append(os.path.abspath('..'))


project = 'Fastapi Docs HW14'
copyright = '2023, Rostyslav'
author = 'Rostyslav'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


html_theme = 'nature'
html_static_path = ['_static']

