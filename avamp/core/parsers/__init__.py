from   avamp.core.logging import LOG
import importlib
import os,glob

# PARSERS = []
ACTIVE_PARSERS = {}
PARSERS = {}
BASE_SEARCH_PATH = os.path.dirname(__file__)
LOG.debug(f"{os.path.join(BASE_SEARCH_PATH, "**/*.py")} - Loading parser modules...")
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