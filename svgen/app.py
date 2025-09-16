"""
svgen - This package's command-line entry-point application.
"""

# built-in
import argparse
from copy import deepcopy
from logging import getLogger
from pathlib import Path
from sys import path
from typing import Iterable, cast

# third-party
from vcorelib.dict import GenericStrDict, merge_dicts
from vcorelib.dict.config import Config
from vcorelib.io import DEFAULT_INCLUDES_KEY

# internal
from svgen import PKG_NAME
from svgen.color.theme.manager import THEMES
from svgen.config import add_dimension_args, initialize_config
from svgen.element.svg import Svg
from svgen.generation.images import generate_images
from svgen.script import invoke_script

LOG = getLogger(__name__)


def generate(
    config: Config,
    output: Path,
    cwd: Path,
    scripts: Iterable[Path],
    images: bool = True,
) -> None:
    """Generate a single SVG document."""

    # Set a theme for this variant.
    THEMES.theme = config.data["theme"]

    # Add the specified directory to the import path, so external scripts
    # can load their own dependencies.
    cwd_str = str(cwd)
    if cwd_str not in path:
        path.append(cwd_str)

    doc = Svg.app(cast(GenericStrDict, config))

    # Compose the document, via the external script.
    for script in list(scripts) + [Path(x) for x in config["scripts"]]:
        invoke_script(script, doc, config)

    # Write the composed document to the output file.
    with output.open("w", encoding="utf-8") as output_fd:
        doc.encode(output_fd)
    LOG.info("Wrote '%s'.", output)

    # Generate image outputs.
    if images:
        generate_images(doc, output)


def entry(args: argparse.Namespace) -> int:
    """Execute the requested task."""

    try:
        config = Config.from_path(
            args.config, includes_key=DEFAULT_INCLUDES_KEY
        )
    except AssertionError:
        config = Config()

    initialize_config(config, args.height, args.width)

    # Save the initial configuration data.
    original = deepcopy(config.data)

    scripts = set(x.resolve() for x in args.scripts)

    # Generate the main document.
    generate(config, args.output, args.dir, scripts, images=args.images)

    # Generate any document variants.
    for idx, variant in enumerate(config.get("variants", [])):
        # Load the variant's data.
        config = Config(
            merge_dicts(
                [deepcopy(original), variant.get("data", {})],
                expect_overwrite=True,
            )
        )
        initialize_config(config, args.height, args.width)

        # Set the output name for this variant.
        name = args.output.with_suffix("").name
        output = args.output.with_name(
            f"{name}-{variant.get('name', idx)}.svg"
        )

        generate(
            config,
            output,
            args.dir,
            scripts
            | set(Path(x).resolve() for x in variant.get("scripts", [])),
            images=args.images,
        )

    return 0


def add_app_args(parser: argparse.ArgumentParser) -> None:
    """Add application-specific arguments to the command-line parser."""

    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        default=Path(f"{PKG_NAME}.json"),
        help="top-level configuration to load (default: '%(default)s')",
    )

    add_dimension_args(parser)

    parser.add_argument(
        "--images", action="store_true", help="generate output images"
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path(f"{PKG_NAME}.svg"),
        help="file to write SVG output (default: '%(default)s')",
    )

    parser.add_argument(
        "scripts",
        type=Path,
        nargs="*",
        help="scripts to run for composing the SVG document (in order)",
    )
