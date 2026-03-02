from importlib.metadata import metadata, version

__version__ = version("ciopen")

__author__ = metadata("ciopen")["Author-email"]
