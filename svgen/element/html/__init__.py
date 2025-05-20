"""
A module for html-related elements.
"""

# built-in
from typing import TextIO

# third-party
from vcorelib import DEFAULT_ENCODING

# internal
from svgen.attribute import attributes
from svgen.element import Element

DEFAULT_VIEWPORT = "width=device-width, initial-scale=1"


class Html(Element):
    """A class for html elements."""

    def __init__(
        self,
        title: str,
        viewport: str = DEFAULT_VIEWPORT,
        charset: str = DEFAULT_ENCODING,
        lang: str = "en",
        **kwargs,
    ) -> None:
        """Initialize this instance."""

        self.head = Element(
            tag="head",
            children=[
                Element(tag="meta", attrib=attributes({"charset": charset})),
                Element(
                    tag="meta",
                    attrib=attributes(
                        {"name": "viewport", "content": viewport}
                    ),
                ),
                Element(tag="title", text=title),
            ],
        )

        self.body = Element(tag="body", **kwargs)

        super().__init__(
            attrib=attributes({"lang": lang}), children=[self.head, self.body]
        )

    def render(self, stream: TextIO) -> None:
        """Render a full HTML document to the stream."""

        stream.write("<!DOCTYPE html>\n")
        self.encode(stream)


def div(
    tag: str = "div",
    parent: Element = None,
    allow_no_end_tag: bool = False,
    front: bool = False,
    **kwargs,
) -> Element:
    """Get a new 'div' element."""

    result = Element(tag=tag, allow_no_end_tag=allow_no_end_tag, **kwargs)

    if parent is not None:
        parent.children.insert(0 if front else len(parent.children), result)

    return result
