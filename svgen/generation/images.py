"""
A module for generating images from SVG files.
"""

from asyncio import run
from contextlib import suppress
from pathlib import Path

# built-in
import subprocess

# internal
from svgen.display import ICON_SIZES, AspectRatio, common_sizes
from svgen.element.svg import Svg
from svgen.inkscape import DEFAULT_ENTRY, invoke_multiple


def generate_icon(output_dir: Path) -> None:
    """Generate an icon from previously generated PNG outputs."""

    args = ["icotool", "-c"]

    out_name_base = output_dir.name

    # Add size arguments.
    for size in ICON_SIZES:
        args.append(
            str(output_dir.joinpath(f"{out_name_base}-{size}x{size}.png"))
        )

    # Add output argument.
    args += ["-o", str(output_dir.joinpath(f"{out_name_base}.ico"))]
    with suppress(subprocess.CalledProcessError, FileNotFoundError):
        subprocess.run(args, check=True)


def generate_images(
    doc: Svg, output: Path, cli_entry: str = DEFAULT_ENTRY
) -> bool:
    """Generate image outputs for this document."""

    dir_name = output.with_suffix("")
    dir_name.mkdir(parents=True, exist_ok=True)

    arg_sets = []

    out_name_base = dir_name.name
    doc_ratio = AspectRatio(doc.viewbox.width, doc.viewbox.height)
    for ratio in common_sizes(doc_ratio):
        out_path = dir_name.joinpath(
            f"{out_name_base}-{ratio.as_str('x')}.png"
        )

        # Gather sets of arguments for inkscape.
        arg_sets.append(["-o", str(out_path), *ratio.args, str(output)])

    # Run inkscape to generate outputs.
    result = False
    with suppress(FileNotFoundError):
        result = run(invoke_multiple(arg_sets, entry=cli_entry))

    # Also generate an icon for square documents.
    if result and doc_ratio.square:
        generate_icon(dir_name)

    return result
