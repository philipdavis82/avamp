from avamp.core.logging import LOG

import os

def get_roboto_font():
    """
    Get the Roboto font path.
    
    :return: The path to the Roboto font.
    """
    # font_path = os.path.join(os.path.dirname(__file__), "fonts", "Roboto" ,"static", "Roboto-Regular.ttf")
    font_path = os.path.join(os.path.dirname(__file__), "fonts", "Roboto","Roboto-VariableFont_wdth,wght.ttf")
    if not os.path.exists(font_path):
        LOG.error(f"Roboto font not found at {font_path}")
        return None
    return font_path