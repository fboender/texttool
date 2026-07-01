import unittest
import texttool

T_SEL_INLINE="""foo bar baz quux"""


class TestMarkdown(unittest.TestCase):

    def test_toc(self):
        with open("test_data/markdown_toc.md", "r") as fh:
            toc = texttool.Markdown(fh.read()).toc()

        self.assertEqual(
            toc,
            """* [Heading 1](#heading-1)\n    * [Heading 1.1](#heading-1.1)\n* [Heading 2](#heading-2)"""
        )


class TestTextTool(unittest.TestCase):

    def setUp(self):
        self.tt = texttool.Text(content=T_SEL_INLINE)

    def test_sel_no_end(self):
        self.tt.sel("baz")
        self.assertEqual(
            self.tt.extract(),
            "baz"
        )

    def test_sel_after(self):
        self.tt.sel(start="baz ", start_after=True).end_re(r"$")
        self.assertEqual(
            self.tt.extract(),
            "quux"
        )

    def test_sel_re(self):
        self.tt.start_re(r"b.r\s*", after=True).end_re(r"ux")
        self.assertEqual(
            self.tt.extract(),
            "baz qu"
        )

    def test_sel_re_multi(self):
        self.tt.start_re(r"(bar|foo)").end_re(" baz")
        self.assertEqual(
            self.tt.extract(),
            "foo bar"
        )

    def test_insert(self):
        self.assertEqual(
            self.tt.sel("baz").insert("baq ").result(),
            "foo bar baq baz quux"
        )

    def test_insert_after(self):
        self.assertEqual(
            self.tt.sel("baz").insert(" baq", after=True).result(),
            "foo bar baz baq quux"
        )

    def test_replace(self):
        self.assertEqual(
            self.tt.sel("baz ").replace("baq ").result(),
            "foo bar baq quux"
        )

    def test_delete(self):
        self.assertEqual(
            self.tt.sel("baz ").delete().result(),
            "foo bar quux"
        )


if __name__ == '__main__':
    unittest.main()
