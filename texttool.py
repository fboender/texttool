#!/usr/bin/env python3

import sys
import textwrap
import re


class Markdown:
    """
    Markdown tools
    """
    re_heading = re.compile(r"^(#+)\s*(.*)$")

    def __init__(self, body):
        self.body = body

    def toc(self, ignore_headings=[], max_depth=None, links=True):
        """
        Generate a Table of Contents of the headings found in Markdown text.

        `ignore_headings` is a list of case-sensitive headings to ignore. E.g.
        "Table of Contents".

        `max_depth` defines the depth level of headings to include in the ToC. E.g.
        if `max_depth` is 2, headings `###` and deeper are not included. The
        default is `None`, which will include all headings.

        If `links` is True, links to the headings will be included, but whether
        they work depends on the Markdown renderer and Markdown text itself. They
        work with Github.
        """
        md_headings = []

        for line in self.body.splitlines():
            match = re.match(self.re_heading, line)
            if not match:
                continue

            heading_hash, title = match.groups()

            if title in ignore_headings:
                continue

            if max_depth is not None and len(heading_hash) > max_depth:
                continue

            str_indent = "    " * (len(heading_hash) - 1)
            str_href = title.replace(" ", "-").lower()
            if links is True:
                str_heading = f"* [{title}](#{str_href})"
            else:
                str_heading = f"* {title}"
            md_headings.append(
                str_indent + str_heading
            )

        return "\n".join(md_headings)


class TextError(Exception):
    pass


class Text:
    """
    Manipulate text using selection cursors.

    A selection has a start and ending position. Various methods act on the
    current selection.

    This class can operate directly on files or on strings.

    Note that manipulating text (insert, delete) may mess up the current
    selection, so you may need to reselect.
    """
    def __init__(self, path=None, content=None):
        """
        Initialize Text object. You must specify either `path` or `text`.
        """
        if path is not None:
            self.path = path
            with open(self.path, "r") as fh:
                self.content = fh.read()
        elif content is not None:
            self.content = content
        else:
            raise TextError("Either `path` or `content` must be specified")

        # Current selection starting position
        self.start_pos = None

        # Current selection ending position
        self.end_pos = None

        # Current string that was used to set the selection starting position
        self.start_match = None

        # Current string that was used to set the selection end position
        self.end_match = None

    def start(self, match, after=False):
        """
        Set the selection start using a string.

        If `after` is True, set the selection cursor after `match`.
        """
        pos = self.content.find(match)
        if pos == -1:
            raise TextError(f"Start string '{match}' not found")

        self.start_match = match

        if after is True:
            self.start_pos = pos + len(match)
        else:
            self.start_pos = pos

        return self

    def start_re(self, match_re, after=False):
        """
        Set the selection start using a regular expression.

        If `after` is True, set the selection cursor after `match_re`.
        """
        match = re.search(match_re, self.content)
        if match is None:
            raise TextError("Start regexp '{match_re} not found")

        self.start_match = match.group()

        if after is True:
            self.start_pos = match.end()
        else:
            self.start_pos = match.start()

        return self

    def end(self, match, after=False):
        """
        Set the selection end using a string. It is always after
        `self.start_match`.

        If `after` is True, set the selection cursor after `match`.
        """
        pos = self.content.find(match, self.start_pos + 1)
        if pos == -1:
            raise TextError("End string '{match}' not found")

        self.end_match = match

        if after is True:
            self.end_pos = pos + len(match)
        else:
            self.end_pos = pos

        return self

    def end_re(self, match_re, after=False):
        """
        Set the selection end using a regular expression.

        If `after` is True, set the selection cursor after `match_re`.
        """
        match = re.search(match_re, self.content)
        if match is None:
            raise TextError("End regexp '{match_re}' not found")

        self.end_text = match.group()

        if after is True:
            self.end_pos = match.end()
        else:
            self.end_pos = match.start()

        return self

    def sel(self, start=None, end=None, start_after=False, end_after=False):
        """
        Create a selection in the content.

        Convienence method around `start()` and `end()`.

        If `end` is not provided, the ending selection cursor is set to the end
        of the starting selection.
        """
        if start is not None:
            self.start(start, start_after)

        if end is not None:
            self.end(end, end_after)
        else:
            # Set end of selection to end of starting selection
            self.end_pos = self.start_pos + len(self.start_match)

        return self

    def insert(self, content, after=False):
        """
        Insert `content` at the current selection. If `after` is set to True,
        insert `content` at the end of the current selection.
        """
        if after is False:
            pos = self.start_pos
            self.start_pos += len(content)
            self.end_pos += len(content)
        else:
            pos = self.end_pos

        self.content = \
            self.content[:pos] + \
            content + \
            self.content[pos:]

        return self

    def replace(self, content):
        """
        Replace the current selection with `content`.
        """
        self.content = \
            self.content[:self.start_pos] + \
            content + \
            self.content[self.end_pos:]

        self.end_pos = self.start_pos + len(content)

        return self

    def delete(self):
        """
        Delete the current selection.
        """
        self.replace("")

        self.end_pos = self.start_pos

        return self

    def extract(self):
        """
        Return contents of current selection.
        """
        return self.content[self.start_pos:self.end_pos]

    def result(self):
        """
        Return entire current content.
        """
        return self.content

    def save(self, path=None):
        """
        Save current content.

        If `path` is specified, saves to path. Otherwise, saves to the
        originally specified file.
        """
        if path is None:
            if self.path is None:
                raise TextError("No path set. Can't save")
            else:
                path = self.path

        with open(path, "w") as fh:
            fh.write(self.content)

        return self

    def show_selection(self):
        """
        Return the current content, with the current selection marked by {{{
        and }}}.
        """
        return \
            self.content[:self.start_pos] + \
            "\x1b[;93m{{{" + \
            self.content[self.start_pos:self.end_pos] + \
            "}}}\x1b[0m" + \
            self.content[self.end_pos:]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as fh:
            code = fh.read()
    else:
        code = sys.stdin.read()

    vars = {
        "Markdown": Markdown,
        "Text": Text,
    }
    exec(code, vars)
