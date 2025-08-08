from   avamp.core.logging import LOG
import importlib
import os,glob

# PARSERS = []
ACTIVE_PARSERS = {}
PARSERS = {}
BASE_SEARCH_PATH = os.path.dirname(__file__)
LOG.debug(f'{os.path.join(BASE_SEARCH_PATH, "**/*.py")} - Loading parser modules...')
for file in glob.glob(os.path.join(BASE_SEARCH_PATH, "**/*.py"), recursive=True):
    LOG.debug(f"Loading parser module: {file}")
    if os.path.split(file)[-1].startswith("parser_"):
        file = file.replace(BASE_SEARCH_PATH + os.sep, "")  # Remove the base path
        LOG.debug(f"Processing file: {file}")
        module_name = file[:-3]  # Remove .py extension
        module_name = ".".join(os.path.split(module_name))
        LOG.debug(f"Importing module: avamp.core.parsers.{module_name}")
        module = importlib.import_module(f"avamp.core.parsers.{module_name}")
        if hasattr(module, "PARSER_EXT") and hasattr(module, "PARSER_CLS") and hasattr(module, "PARSER_NAME"):
            for ext in module.PARSER_EXT:
                if( ext not in PARSERS):
                    LOG.debug(f"Adding parser: {module.PARSER_NAME} with extensions: {ext}")
                    PARSERS[ext] = [{
                        "ext": module.PARSER_EXT,
                        "cls": module.PARSER_CLS,
                        "name": module.PARSER_NAME
                    }]
                else:
                    LOG.debug(f"Adding parser: {module.PARSER_NAME} with extensions: {ext}")
                    PARSERS[ext].append({
                        "ext": module.PARSER_EXT,
                        "cls": module.PARSER_CLS,
                        "name": module.PARSER_NAME
                    })
                if( ext not in ACTIVE_PARSERS):
                    ACTIVE_PARSERS[ext] = module.PARSER_CLS
                    LOG.debug(f"Active parser for {ext} is now {module.PARSER_NAME}")
        else:
            raise ImportError(f"Module {module_name} does not have required attributes PARSER_EXT and PARSER_CLS and PARSER_NAME.")

__all__ = ["PARSERS"]



# Parser Interfaces

def extensions():
    """Returns a list of all parser extensions."""
    return list(PARSERS.keys())

def by_extension(ext):
    """Returns the parser class for a given extension."""
    if ext in PARSERS:
        return PARSERS[ext]
    else:
        raise ValueError(f"No parser found for extension: {ext}")

def set_active_parser(ext, parser:object):
    """Sets the active parser for a given extension."""
    if ext in ACTIVE_PARSERS:
        ACTIVE_PARSERS[ext] = parser
        LOG.debug(f"Active parser for {ext} set to {parser}")
    else:
        raise ValueError(f"No parser found for extension: {ext}")