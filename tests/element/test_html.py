"""
Test the 'element.html' module.
"""

# built-in
from io import StringIO

# module under test
from svgen.element.html import Html, div
from svgen.element.style import Style


def test_html_basic():
    """Test basic interactions with an HTML element."""

    doc = Html("test")
    assert doc.encode_str()

    div(parent=doc.body, text="Hello, world! (front)", front=True)
    div(parent=doc.body, text="Hello, world! (back)")

    assert Style.cascadia_font()

    with StringIO() as stream:
        doc.render(stream)
        assert stream.getvalue()
