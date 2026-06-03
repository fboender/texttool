A text manipulation tool / python library.

<!-- TOC -->
* [Tools](#tools)
* [Example](#example)
    * [Markdown Table of Contents](#markdown-table-of-contents)
* [!/bin/env texttool](#!/bin/env-texttool)
<!-- EO_TOC -->

# Tools

* `Markdown`: Markdown tools
    * `toc()`: Generate a Table of Contents with hyperlinks from a markdown
      file
* `Text`: Manipulate text using selection cursors.

# Example

## Markdown Table of Contents

The following example generates a table of contents for a markdown file and
replaces an existing ToC in that same file:

<!-- EXAMPLE_TOC -->
    #!/bin/env texttool

    with open("README.md") as fh:
        toc = Markdown(fh.read()).toc()

    with Text("README.md") as doc:
        doc.sel(
            start_after="<!-- TOC -->\n",
            end="\n<!-- EO_TOC -->"
        ).replace(toc)
        doc.save()
<!-- EO_EXAMPLE_TOC -->
