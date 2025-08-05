from avamp.core.logging import LOG
import os

def dark():
    stylesheet = os.path.join(os.path.dirname(__file__),"dark-blue","stylesheet.qss")
    stylesheet_path = os.path.dirname(stylesheet)
    if not os.path.exists(stylesheet):
        LOG.error(f"Stylesheet not found: {stylesheet}")
        return
    with open(stylesheet, "r") as f:
        stylesheet = f.read()
        stylesheet = stylesheet.replace("url(':/dark-blue/", f"url('{stylesheet_path}{os.path.sep}")
        stylesheet = stylesheet.replace("\\", "/")
    return stylesheet

def light():
    return ""