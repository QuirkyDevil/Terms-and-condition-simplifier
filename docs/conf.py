import os
import sys
import inspect
import importlib
from typing import Dict, Any

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath(".."))

project = 'Terms and Condition Simplifier'
copyright = '2023, Soham'
author = 'Soham, Shreyas, Mrinmayee, Aditya'

release = '1.0.0'

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.linkcode",
    "myst_parser",
]

myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

myst_heading_anchors = 3

templates_path = ['_templates']

exclude_patterns = ["build", ".DS_Store"]

html_theme = "furo"

html_static_path = ['_static']

html_title = "Terms and Condition Simplifier"

html_theme_options: Dict[str, Any] = {
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/QuirkyDevil/Terms-and-condition-simplifier",
            "html": """
                <svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
            """,
            "class": "",
        },
    ],
    "source_repository": "https://github.com/QuirkyDevil/Terms-and-condition-simplifier",
    "source_branch": "main",
    "source_directory": "docs/",
}

def linkcode_resolve(domain, info):
    # i absolutely MUST add this here or else
    # the docs will not build. fuck sphinx
    try:
        if domain != "py":
            return None
        if not info["module"]:
            return None

        mod = importlib.import_module(info["module"])
        if "." in info["fullname"]:
            objname, attrname = info["fullname"].split(".")
            obj = getattr(mod, objname)
            try:
                obj = getattr(obj, attrname)
            except AttributeError:
                return None
        else:
            obj = getattr(mod, info["fullname"])

        try:
            file = inspect.getsourcefile(obj)
            lines = inspect.getsourcelines(obj)
        except TypeError:
            # e.g. object is a typing.Union
            return None
        file = os.path.relpath(file, os.path.abspath(".."))
        start, end = lines[1], lines[1] + len(lines[0]) - 1

        return f"https://github.com/QuirkyDevil/Terms-and-condition-simplifier/blob/main/{file}#L{start}-L{end}"
    except:
        pass