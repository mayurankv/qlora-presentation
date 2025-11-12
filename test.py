from manim import *


class TableWithBooktabs(Scene):
    def construct(self):
        template = TexTemplate()
        template.add_to_preamble(r"\usepackage{booktabs}")

        tex = Tex(
            r"""
            \begin{tabular}{ll}
            \toprule
            A & B \\
            \midrule
            1 & 2 \\
            3 & 4 \\
            \bottomrule
            \end{tabular}
            """,
            tex_template=template,
        )

        self.add(tex)
