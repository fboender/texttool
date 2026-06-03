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
    example_toc = textwrap.indent(
        doc.sel(
            start_after="# EXAMPLE_TOC",
            end="# EO_EXAMPLE_TOC"
        ).extract(),
        prefix="    "
    )

with Text("README.md") as doc:
    doc.sel(
        start_after="<!-- EXAMPLE_TOC -->",
        end="<!-- EO_EXAMPLE_TOC -->"
    ).replace(example_toc)
    doc.save()
