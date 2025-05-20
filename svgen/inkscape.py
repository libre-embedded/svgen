"""
A module for generating image outputs from SVG via Inkscape.

https://gitlab.com/inkscape/inkscape
"""

# built-in
import asyncio

# third-party
from vcorelib.task.subprocess.run import SubprocessExecStreamed

DEFAULT_ENTRY = "inkscape"


class InkscapeTask(SubprocessExecStreamed):
    """A task implementation for invoking inkscape at command-line."""

    async def invoke(self, *cli_args, entry: str = DEFAULT_ENTRY) -> bool:
        """Invoke inkscape."""
        return await self.run({}, {}, *cli_args, args="", program=entry)


INKSCAPE = InkscapeTask(DEFAULT_ENTRY)


async def invoke(*cli_args: str, entry: str = DEFAULT_ENTRY) -> bool:
    """Run an inkscape command-line command."""
    return await INKSCAPE.invoke(*cli_args, entry=entry)


async def invoke_multiple(
    args: list[list[str]], entry: str = DEFAULT_ENTRY
) -> bool:
    """Run multiple inkscape invocations at the same time."""
    return all(await asyncio.gather(*[invoke(*x, entry=entry) for x in args]))
