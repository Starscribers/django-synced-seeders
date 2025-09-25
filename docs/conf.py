# Configuration file for the Sphinx documentation builder.
# For the full list of built-in configuration values, see:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
project = "Django Synced Seeds"
copyright = "2025, Starscribers"
author = "Starscribers"
release = "0.2.0"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Project information in templates
html_context = {
    "project_name": "Django Synced Seeds",
    "project_description": "Keep seed data in sync across environments",
}

# -- Options for HTML output -------------------------------------------------
html_theme = "conestack"
html_title = "Django Synced Seeds"
html_short_title = "Django Synced Seeds"
html_logo = "_static/sprout-icon.svg"

# Enable line numbers in code blocks
pygments_style = "default"
highlight_language = "python"
html_show_sourcelink = False

# Add line numbers to code blocks by default
html_codeblock_linenos_style = "table"

# Line numbers for code blocks
html_theme_options = {
    "logo_url": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN5YW4iIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBjbGFzcz0ibHVjaWRlIGx1Y2lkZS1zcHJvdXQtaWNvbiBsdWNpZGUtc3Byb3V0Ij48cGF0aCBkPSJNMTQgOS41MzZWN2E0IDQgMCAwIDEgNC00aDEuNWEuNS41IDAgMCAxIC41LjVWNWE0IDQgMCAwIDEtNCA0IDQgNCAwIDAgMC00IDRjMCAyIDEgMyAxIDVhNSA1IDAgMCAxLTEgMyIvPjxwYXRoIGQ9Ik00IDlhNSA1IDAgMCAxIDggNCA1IDUgMCAwIDEtOC00Ii8+PHBhdGggZD0iTTUgMjFoMTQiLz48L3N2Zz4=",
    "logo_title": "Django Synced Seeds",
    "logo_width": "40px",
    "logo_height": "40px",
}

html_static_path = ["_static"]
html_css_files = ["custom.css"]

# -- Options for MyST parser ------------------------------------------------
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "html_admonition",
    "html_image",
    "substitution",
    "tasklist",
]

# -- Options for intersphinx -------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "django": (
        "https://docs.djangoproject.com/en/stable/",
        "https://docs.djangoproject.com/en/stable/_objects/",
    ),
}

# -- Options for autodoc ----------------------------------------------------
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

# Master doc
master_doc = "index"

# Source suffix
source_suffix = {
    ".rst": None,
    ".md": None,
}
html_favicon = "favicon.ico"
