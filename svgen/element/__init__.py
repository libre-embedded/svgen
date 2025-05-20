"""
svgen - Common interfaces and assets for SVG elements.
"""

# built-in
from io import StringIO
import os
from typing import TextIO, TypeVar, cast
from xml.etree import ElementTree as et

# internal
from svgen.attribute import (
    Attribute,
    AttributeValue,
    PossibleAttributes,
    SimpleAttribute,
    attributes,
)
from svgen.attribute.style import Style

INDENT: int = 2
T = TypeVar("T", bound="Element")


class Element:
    """A basic interface for an SVG element."""

    def __init__(
        self,
        tag: str = None,
        text: str = "",
        attrib: PossibleAttributes = None,
        children: list["Element"] = None,
        head_child: "Element" = None,
        tail_child: "Element" = None,
        allow_no_end_tag: bool = True,
        class_str: str = None,
        preformatted: bool = False,
        **extra,
    ) -> None:
        """Construct a new SVG element."""

        if tag is None:
            tag = type(self).__name__
            tag = tag[0].lower() + tag[1:]

        if children is None:
            children = []
        self.children: list[Element] = children
        self.head_child = head_child
        self.tail_child = tail_child

        self.tag = tag
        self.text = text

        self.allow_no_end_tag = allow_no_end_tag

        self.attributes: dict[str, Attribute] = {}
        self.booleans: set[str] = set()

        self.preformatted = preformatted

        for attr in attributes(data=attrib) + attributes(data=extra):
            self.add_attribute(attr)

        # Set a 'class' attribute.
        if class_str:
            self["class"] = class_str

    def add_class(self: T, *data: str) -> T:
        """Add a class string."""

        raw = self["class"]
        classes = set(raw.split())
        for item in data:
            classes.add(item)
        self["class"] = " ".join(classes)

        return self

    def __setitem__(self, tag: str, value: AttributeValue) -> None:
        """Allow adding attributes dict-set style."""
        self.add_attribute(SimpleAttribute(tag, value), strict=False)

    def __getitem__(self, tag: str) -> str:
        """Get an attibute as a string."""

        if tag not in self.attributes:
            self[tag] = ""

        return self.attributes[tag].value

    @property
    def xml(self) -> et.Element:
        """Get this element as an xml element."""

        elem = et.Element(
            self.tag, {x.key: x.value for x in self.attributes.values()}
        )
        elem.text = self.text

        # Add children.
        elem.extend(child.xml for child in self.children)
        return elem

    @property
    def style(self) -> Style:
        """Get the style attribute for this element."""

        if "style" not in self.attributes:
            self.add_attribute(Style())
        return cast(Style, self.attributes["style"])

    def add_attribute(self: T, attr: Attribute, strict: bool = True) -> T:
        """Add an attribute to this element."""

        assert not strict or (
            attr.key not in self.attributes
        ), f"This '{self.tag}' element already has attribute '{attr.key}'!"

        self.attributes[attr.key] = attr

        return self

    def closing(self, indent: int = 0) -> str:
        """Create a string to close this element."""

        close_tag = f"</{self.tag}>"

        if not self.text and not self.children:
            return " />" if self.allow_no_end_tag else ">" + close_tag

        return (
            close_tag
            if self.preformatted
            else (" " * (indent * INDENT)) + close_tag
        )

    def _write_text(
        self, output: TextIO, indent_str: str, newlines: bool = True
    ) -> None:
        """Write the inner-text section of this element."""

        if not newlines or self.preformatted:
            output.write(self.text)
            return

        # Increase indent one level.
        indent_str += " " * INDENT
        for line in self.text.splitlines():
            output.write(indent_str + line)
            output.write(os.linesep)

    def has_children(self) -> bool:
        """Determine if this element has any children."""

        return (
            len(self.children) > 0
            or self.head_child is not None
            or self.tail_child is not None
        )

    def encode(
        self,
        output: TextIO,
        quote: str = '"',
        indent: int = 0,
        newlines: bool = True,
    ) -> None:
        """Encode this element to a string stream."""

        # Indent will matter if we want lines.
        indent_str = " " * (indent * INDENT)
        if newlines and not self.preformatted:
            output.write(indent_str)

        attr_strs = [x.encode(quote) for x in self.attributes.values()] + list(
            self.booleans
        )
        attrs = " ".join(x for x in attr_strs if x)
        output.write(f"<{self.tag}")
        if attrs:
            output.write(f" {attrs}")

        if self.text or self.has_children():
            # Close the opening tag.
            output.write(">")
            if newlines:
                output.write(os.linesep)

            # Write content, if any.
            if self.text:
                self._write_text(output, indent_str, newlines=newlines)

            # Write children.
            if self.head_child:
                self.head_child.encode(output, quote, indent + 1, newlines)
            for child in self.children:
                if child:
                    child.encode(output, quote, indent + 1, newlines)
            if self.tail_child:
                self.tail_child.encode(output, quote, indent + 1, newlines)

        # Close this element tag.
        output.write(self.closing(indent))
        if newlines:
            output.write(os.linesep)

    def encode_str(
        self,
        quote: str = '"',
        indent: int = 0,
        newlines: bool = True,
    ) -> str:
        """Encode this element to a string."""

        with StringIO() as output:
            self.encode(output, quote, indent, newlines)
            return output.getvalue()
