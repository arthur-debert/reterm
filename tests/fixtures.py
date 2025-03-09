"""Fixtures for tests."""

import os

import pytest


def get_project_root():
    """Get the absolute path to the project root directory."""
    # The project root is three directories up from this file
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def get_path_from_root(relative_path):
    """Get the absolute path from a path relative to the project root."""
    return os.path.join(get_project_root(), relative_path)


 