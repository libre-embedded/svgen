"""
A module for generating image outputs from SVG via Inkscape.

https://gitlab.com/inkscape/inkscape
"""

# built-in
import asyncio
from os import process_cpu_count
from typing import Any

# third-party
from vcorelib.task.subprocess.run import SubprocessExecStreamed

DEFAULT_ENTRY = "inkscape"


class InkscapeTask(SubprocessExecStreamed):
    """A task implementation for invoking inkscape at command-line."""

    async def invoke(
        self, *cli_args, entry: str = DEFAULT_ENTRY, **kwargs
    ) -> bool:
        """Invoke inkscape."""
        return await self.run(
            {}, {}, *cli_args, args="", program=entry, **kwargs
        )


INKSCAPE = InkscapeTask(DEFAULT_ENTRY)


async def invoke(*cli_args: str, entry: str = DEFAULT_ENTRY, **kwargs) -> bool:
    """Run an inkscape command-line command."""
    return await INKSCAPE.invoke(*cli_args, entry=entry, **kwargs)


async def invoke_multiple(
    args: list[list[str]],
    entry: str = DEFAULT_ENTRY,
    nproc: int | None = None,
) -> bool:
    """Run multiple inkscape invocations at the same time."""

    if nproc is None:
        nproc = process_cpu_count() or 1

    gen_idx: int = 0
    num_frames = len(args)
    tasks: list[asyncio.Task[bool | None]] = []

    result = True

    kwargs: dict[str, Any] = {"entry": entry}
    if entry == DEFAULT_ENTRY:
        # https://gitlab.com/inkscape/inkscape/-/work_items/4716
        # https://lists.infradead.org/pipermail/barebox/2025-August/052403.html
        kwargs["env"] = {"SELF_CALL": "1"}

    while result and gen_idx < num_frames:
        while len(tasks) < nproc and gen_idx < num_frames:
            tasks.append(asyncio.create_task(invoke(*args[gen_idx], **kwargs)))
            gen_idx += 1

        assert tasks
        result = all(await asyncio.gather(*tasks))
        tasks = []

    return result
