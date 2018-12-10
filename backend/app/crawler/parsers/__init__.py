from .generic import GenericParser

PARSER_MAPPING = {
    "0": GenericParser,
}

__all__ = ["PARSER_MAPPING", ]
