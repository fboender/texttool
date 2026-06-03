#!/bin/env texttool

import textwrap


# EXAMPLE_TOC
with open("README.md") as fh:
    toc = Markdown(fh.read()).toc()

with Text("README.md") as doc:
    doc.sel(
        start_after="<!-- TOC -->\n",
        end="\n<!-- EO_TOC -->"
    ).replace(toc)
    doc.save()
# EO_EXAMPLE_TOC

with Text("example.py") as doc:
    first_line = (
        doc.sel(
            end="\n"
        ).extract()
    )
    example_toc = doc.sel(
        start_after="# EXAMPLE_TOC",
        end="# EO_EXAMPLE_TOC"
    ).extract()

with Text("README.md") as doc:
    example = textwrap.indent(
        f"\n{first_line}\n{example_toc}",
        prefix="    "
    )
    doc.sel(
        start_after="<!-- EXAMPLE_TOC -->",
        end="<!-- EO_EXAMPLE_TOC -->"
    ).replace(example)
    doc.save()
