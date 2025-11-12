from manim import (
    BLUE,
    DL,
    DOWN,
    DR,
    GREY,
    LEFT,
    ORANGE,
    ORIGIN,
    RED,
    RIGHT,
    UL,
    UP,
    UR,
    WHITE,
    YELLOW,
    BulletedList,
    Circle,
    Dot,
    FadeIn,
    FadeOut,
    LaggedStartMap,
    Line,
    MarkupText,
    MathTex,
    MoveAlongPath,
    Polygon,
    Rectangle,
    ReplacementTransform,
    SVGMobject,
    Tex,
    Text,
    TexTemplate,
    Unwrite,
    VGroup,
    Write,
    config,
    linear,
)
from manim_slides import Slide  # type: ignore
from mayutils.objects.datetime import DateTime

from qlora_presentation.assets import ASSET_DIR
from qlora_presentation.visualisation.styles import FontSize, FontWeight, Style

config.frame_width = 14.2
config.frame_height = 8
config.pixel_width = 2560
config.pixel_height = 1440
config.frame_rate = 120.0


STYLE = Style()

FONT = "Mona Sans"
TITLE_WRITE_TIME = 1


class Main(Slide):
    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(
            *args,
            **kwargs,
        )

        self.tex_template = TexTemplate()
        self.tex_template.add_to_preamble(
            txt=r"""
				\usepackage{amsmath}
				\usepackage{amssymb}
				\usepackage{amsfonts}
				\usepackage{amsthm}
				\usepackage{mathtools}
				\usepackage{array}
				\usepackage{booktabs}
				\usepackage{xfrac}
				\usepackage{multirow}
				\usepackage{newtxmath}
				%\usepackage{unicode-math}
				\AtBeginDocument{%
					\let\mathbb\relax
					\let\mathcal\relax
					\DeclareMathAlphabet{\mathbb}{U}{msb}{m}{n}
					\DeclareMathAlphabet{\mathcal}{OMS}{cmsy}{m}{n}
				}

				\newtheoremstyle{dissertation}
					{0\topsep}	% Space above
					{0.6\topsep}	% Space below
					{}				% Body font
					{}				% Indent amount
					{\bfseries}		% Theorem head font
					{}				% Punctuation after theorem head
					{0.5em}			% Space after theorem head
					{}				% Theorem head spec (can be left empty, meaning ‘normal’)

				\theoremstyle{dissertation}
				\newtheorem*{definition}{Definition}
				\newtheorem*{theorem}{Theorem}
				\newtheorem*{proposition}{Proposition}
				\newtheorem*{lemma}{Lemma}
				\newtheorem*{corollary}{Corollary}
				\newtheorem*{example}{Example}
				\newtheorem*{remark}{Remark}
				%\renewcommand{\thetheorem}{\arabic{theorem}}
				%\renewcommand{\thedefinition}{\arabic{definition}}

				\renewenvironment{proof}[1][\proofname]%
				{\noindent\trivlist\item\ignorespaces{\bfseries #1. }}%
					{\hfill $\square$}

				\newcommand\independent{\protect\mathpalette{\protect\independenT}{\perp}}
				\def\independenT#1#2{\mathrel{\rlap{$#1#2$}\mkern2mu{#1#2}}}
				\newcolumntype{L}{>{\centering\arraybackslash}m{3cm}}
				\newcolumntype{E}{>{\centering\arraybackslash}m{6cm}}
				\newcolumntype{F}{>{\centering\arraybackslash}m{7cm}}
				\newcolumntype{A}{>{\centering\arraybackslash}m{5cm}}
				\newcommand*{\doi}[1]{\href{http://dx.doi.org/#1}{doi: #1}}
			"""
        )
        Text.set_default(
            font=FONT,
            font_size=FontSize.CONTENT,
            disable_ligatures=False,
        )
        MarkupText.set_default(
            font=FONT,
            font_size=FontSize.CONTENT,
            disable_ligatures=False,
        )
        MathTex.set_default(color=WHITE)

    def new_slide(
        self,
        **kwargs,
    ) -> ReplacementTransform:
        self.next_slide(**kwargs)
        old_slide_number = self._slide_number
        self.page += 1

        new_slide_number = (
            Text(
                text=str(self.page),
                font_size=FontSize.CONTENT,
                weight=str(FontWeight.SEMIBOLD),
                color=STYLE.foreground.secondary,
            )
            .scale(scale_factor=0.8)
            .move_to(point_or_mobject=old_slide_number)
        )

        self._slide_number = new_slide_number

        return ReplacementTransform(
            mobject=old_slide_number, target_mobject=self._slide_number
        )

    def back_propagation(
        self,
    ) -> VGroup:
        node_color = STYLE.foreground.primary
        back_arrow_color = GREY

        # --- Node counts ---
        n_input = 3
        n_hidden = 5
        n_output = 3

        # --- Vertical spacing calculation ---
        def vertical_positions(n, height=2):
            if n == 1:
                return [0]
            return [height / 2 - i * (height / (n - 1)) for i in range(n)]

        # --- Nodes ---
        input_nodes = VGroup(
            *[
                Circle(radius=0.3, color=node_color, fill_opacity=0.3).shift(
                    LEFT * 3 + UP * y
                )
                for y in vertical_positions(n_input)
            ]
        )
        hidden_nodes = VGroup(
            *[
                Circle(radius=0.3, color=node_color, fill_opacity=0.3).shift(
                    RIGHT * 0 + UP * y
                )
                for y in vertical_positions(n_hidden, height=3)
            ]
        )
        output_nodes = VGroup(
            *[
                Circle(radius=0.3, color=node_color, fill_opacity=0.3).shift(
                    RIGHT * 3 + UP * y
                )
                for y in vertical_positions(n_output)
            ]
        )

        # --- Connections ---
        forward_arrows_1 = VGroup()
        for i_node in input_nodes:
            for h_node in hidden_nodes:
                forward_arrows_1.add(
                    Line(i_node.get_right(), h_node.get_left(), color=WHITE)
                )
        forward_arrows_2 = VGroup()
        for h_node in hidden_nodes:
            for o_node in output_nodes:
                forward_arrows_2.add(
                    Line(h_node.get_right(), o_node.get_left(), color=WHITE)
                )

        back_arrows_1 = VGroup()
        for o_node in output_nodes:
            for h_node in hidden_nodes:
                back_arrows_1.add(
                    Line(o_node.get_left(), h_node.get_right(), color=back_arrow_color)
                )
        back_arrows_2 = VGroup()
        for h_node in hidden_nodes:
            for i_node in input_nodes:
                back_arrows_2.add(
                    Line(h_node.get_left(), i_node.get_right(), color=back_arrow_color)
                )

        # --- Dots for animation ---
        dots_forward_1 = VGroup(
            *[
                Dot(point=line.get_start(), color=WHITE).scale(0.5)
                for line in forward_arrows_1
            ]
        )
        dots_forward_2 = VGroup(
            *[
                Dot(point=line.get_start(), color=WHITE).scale(0.5)
                for line in forward_arrows_2
            ]
        )
        dots_backward_1 = VGroup(
            *[
                Dot(point=line.get_start(), color=STYLE.foreground.primary).scale(0.5)
                for line in back_arrows_1
            ]
        )
        dots_backward_2 = VGroup(
            *[
                Dot(point=line.get_start(), color=STYLE.foreground.primary).scale(0.5)
                for line in back_arrows_2
            ]
        )

        extra_nodes = VGroup(
            *[
                Circle(radius=0.3, color=RED, fill_opacity=0.3).shift(
                    RIGHT * -6 + UP * y
                )
                for y in vertical_positions(n_output - 1, height=1)
            ]
        )

        extra_arrows = VGroup()
        for i_node in input_nodes:
            for e_node in extra_nodes:
                extra_arrows.add(
                    Line(i_node.get_left(), e_node.get_right(), color=WHITE)
                )

        middle_hidden = hidden_nodes[n_hidden // 2]

        middle_forward_arrows_1 = VGroup(
            *[
                line
                for line in forward_arrows_1
                if line.get_end()[1] == middle_hidden.get_y()
            ]
        )
        middle_forward_arrows_2 = VGroup(
            *[
                line
                for line in forward_arrows_2
                if line.get_start()[1] == middle_hidden.get_y()
            ]
        )
        middle_backward_arrows_1 = VGroup(
            *[
                line
                for line in back_arrows_1
                if line.get_end()[1] == middle_hidden.get_y()
            ]
        )
        middle_backward_arrows_2 = VGroup(
            *[
                line
                for line in back_arrows_2
                if line.get_start()[1] == middle_hidden.get_y()
            ]
        )

        highlight_color = YELLOW
        # Dots along the middle node path (yellow for both directions)
        middle_forward_dots_1 = VGroup(
            *[
                Dot(point=line.get_start(), color=highlight_color).scale(0.5)
                for line in middle_forward_arrows_1
            ]
        )
        middle_forward_dots_2 = VGroup(
            *[
                Dot(point=line.get_start(), color=highlight_color).scale(0.5)
                for line in middle_forward_arrows_2
            ]
        )
        middle_backward_dots_1 = VGroup(
            *[
                Dot(point=line.get_start(), color=highlight_color).scale(0.5)
                for line in middle_backward_arrows_1
            ]
        )
        middle_backward_dots_2 = VGroup(
            *[
                Dot(point=line.get_start(), color=highlight_color).scale(0.5)
                for line in middle_backward_arrows_2
            ]
        )

        # --- Group everything ---
        network_group = VGroup(
            input_nodes,
            hidden_nodes,
            output_nodes,
            forward_arrows_1,
            forward_arrows_2,
            back_arrows_1,
            back_arrows_2,
            dots_forward_1,
            dots_forward_2,
            dots_backward_1,
            dots_backward_2,
            extra_nodes,
            extra_arrows,
            middle_forward_dots_1,
            middle_forward_dots_2,
            middle_backward_dots_1,
            middle_backward_dots_2,
        )
        network_group.scale(
            scale_factor=0.6,
        ).move_to(
            point_or_mobject=ORIGIN,
        ).shift(
            DOWN * 2,
        )

        self.play(
            LaggedStartMap(FadeIn, input_nodes, lag_ratio=0.05),
            LaggedStartMap(FadeIn, hidden_nodes, lag_ratio=0.05),
            LaggedStartMap(FadeIn, output_nodes, lag_ratio=0.05),
            LaggedStartMap(FadeIn, forward_arrows_1, lag_ratio=0.05),
            LaggedStartMap(FadeIn, forward_arrows_2, lag_ratio=0.05),
            LaggedStartMap(FadeIn, back_arrows_1, lag_ratio=0.05),
            LaggedStartMap(FadeIn, back_arrows_2, lag_ratio=0.05),
        )

        self.next_slide(loop=True)

        forward_animations_1 = [
            MoveAlongPath(dot, line, rate_func=linear)
            for dot, line in zip(dots_forward_1, forward_arrows_1)
        ]
        forward_animations_2 = [
            MoveAlongPath(dot, line, rate_func=linear)
            for dot, line in zip(dots_forward_2, forward_arrows_2)
        ]
        backward_animations_1 = [
            MoveAlongPath(dot, line, rate_func=linear)
            for dot, line in zip(dots_backward_1, back_arrows_1)
        ]
        backward_animations_2 = [
            MoveAlongPath(dot, line, rate_func=linear)
            for dot, line in zip(dots_backward_2, back_arrows_2)
        ]

        self.play(*forward_animations_1, run_time=1)
        self.play(*forward_animations_2, run_time=1)
        self.play(*backward_animations_1, run_time=1)
        self.play(*backward_animations_2, run_time=1)

        self.next_slide()

        forward_animations_1 = [
            MoveAlongPath(dot, line, rate_func=linear)
            for dot, line in zip(middle_forward_dots_1, middle_forward_arrows_1)
        ]
        forward_animations_2 = [
            MoveAlongPath(dot, line, rate_func=linear)
            for dot, line in zip(middle_forward_dots_2, middle_forward_arrows_2)
        ]
        backward_animations_1 = [
            MoveAlongPath(dot, line, rate_func=linear)
            for dot, line in zip(middle_backward_dots_1, middle_backward_arrows_1)
        ]
        backward_animations_2 = [
            MoveAlongPath(dot, line, rate_func=linear)
            for dot, line in zip(middle_backward_dots_2, middle_backward_arrows_2)
        ]

        # --- Play middle-node propagation ---
        self.play(*forward_animations_1, run_time=1)
        self.play(*forward_animations_2, run_time=1)
        self.play(*backward_animations_1, run_time=1)
        self.play(*backward_animations_2, run_time=1)

        self.play(
            FadeIn(extra_nodes),
            FadeIn(extra_arrows),
        )

        return network_group

    def construct(
        self,
    ) -> None:
        background = Circle(
            color=STYLE.background.primary,
            radius=10,
            fill_opacity=1,
            z_index=-1,
        )
        self.add(background)
        logo_white = (
            SVGMobject(
                file_name=ASSET_DIR / "images" / "lendable-logo-white.svg",
            )
            .scale(scale_factor=0.15)
            .to_corner(corner=UL)
        )
        title = (
            Text(
                text="Fine-Tuning Large Language Models\nLoRA and QLoRA",
                color=STYLE.foreground.primary,
                font_size=FontSize.TITLE,
                weight=str(FontWeight.SEMIBOLD),
            )
            .to_edge(edge=LEFT)
            .shift(0.3 * UP)
        )

        subtitle = (
            Text(
                text="Lendable Journal Club",
                color=STYLE.foreground.secondary,
                font_size=FontSize.SUBTITLE,
                weight="SEMIBOLD",
            )
            .scale(scale_factor=0.8)
            .next_to(mobject_or_point=title, direction=DOWN)
            .align_to(mobject_or_point=title, direction=LEFT)
        )
        date = (
            Text(
                text=DateTime.today().to_date_string(),
                color=STYLE.foreground.secondary,
                font_size=FontSize.SUBTITLE,
                weight=str(FontWeight.MEDIUM),
            )
            .scale(scale_factor=0.5)
            .to_corner(corner=DL)
        )
        author = (
            Text(
                text="Mayuran Visakan",
                color=STYLE.foreground.primary,
                font_size=FontSize.SUBTITLE,
                weight=str(FontWeight.MEDIUM),
            )
            .scale(scale_factor=0.7)
            .next_to(mobject_or_point=date, direction=UP)
            .align_to(mobject_or_point=date, direction=LEFT)
        )
        self.page = 1
        self._slide_number = (
            Text(
                text=str(self.page),
                font_size=FontSize.CONTENT,
                weight="SEMIBOLD",
                color=STYLE.foreground.secondary,
            )
            .scale(scale_factor=0.8)
            .to_corner(corner=DR)
        )
        slide_title = (
            Text(
                text="Overview",
                color=STYLE.foreground.primary,
                font_size=FontSize.SUBTITLE,
                weight="SEMIBOLD",
            )
            .to_corner(corner=UL)
            .set_stroke(color=STYLE.foreground.primary)
        )
        self.play(
            Write(vmobject=title),
            FadeIn(logo_white),
        )
        self.play(
            Write(
                vmobject=subtitle,
                direction=DOWN,
            ),
        )
        self.play(
            FadeIn(date),
            FadeIn(author),
        )
        self.next_slide()
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            logo_white.animate.scale(scale_factor=0.5).to_corner(UR),
            author.animate.scale(scale_factor=0.5).to_corner(DL),
            date.animate.scale(scale_factor=0.7)
            .to_corner(DL)
            .shift(1.9 * RIGHT)
            .shift(0.03 * UP),
        )

        separator = (
            Text(
                text="|",
                color=STYLE.foreground.secondary,
                font_size=FontSize.CONTENT,
                weight=str(FontWeight.SEMIBOLD),
            )
            .scale(scale_factor=0.35)
            .next_to(mobject_or_point=author, direction=RIGHT)
            .shift(0.1 * LEFT)
        )

        self.play(
            FadeIn(separator),
            FadeIn(slide_title),
            FadeIn(self._slide_number),
        )

        overview_scale = 1.0
        overview = VGroup(
            Text(
                text="- Fine-Tuning",
                weight=str(FontWeight.SEMIBOLD),
                font_size=FontSize.SUBTITLE,
            ).scale(scale_factor=overview_scale),
            Text(
                text="- LoRA (Low Rank Adaptation)",
                weight=str(FontWeight.SEMIBOLD),
                font_size=FontSize.SUBTITLE,
            ).scale(scale_factor=overview_scale),
            Text(
                text="- QLoRA (Quantised LoRA)",
                weight=str(FontWeight.SEMIBOLD),
                font_size=FontSize.SUBTITLE,
            ).scale(scale_factor=overview_scale),
        )
        overview.set_color(color=STYLE.foreground.primary).arrange(
            direction=DOWN,
            aligned_edge=LEFT,
        ).center()

        self.play(
            Write(vmobject=overview, run_time=1),
        )

        slide_transform = self.new_slide()
        old_slide_title = slide_title
        slide_title = (
            Text(
                text="Naive Fine-Tuning",
                color=STYLE.foreground.primary,
                font_size=FontSize.SUBTITLE,
                weight=str(FontWeight.SEMIBOLD),
            )
            .to_corner(corner=UL)
            .set_stroke(color=STYLE.foreground.primary)
        )
        self.play(
            Unwrite(overview, run_time=1),
            ReplacementTransform(old_slide_title, slide_title),
            slide_transform,
        )
        introduction = VGroup(
            Text(
                text="Fine-tuning an LLM is the process of adapting a pre-trained model\nto perform better at a specific task.",
                weight=str(FontWeight.SEMIBOLD),
            ),
            Text(
                text="Naive fine-tuning involves taking a pre-trained model and continuing\nto train the model updating all of its weights.",
                weight=str(FontWeight.SEMIBOLD),
            ),
        )
        introduction.arrange(
            direction=DOWN,
            aligned_edge=LEFT,
        ).center().shift(0.5 * UP)

        self.play(
            Write(introduction, run_time=1.5),  # type: ignore
        )

        total = self.back_propagation()

        transform = self.new_slide()

        old_slide_title = slide_title
        slide_title = (
            Text(
                text="LoRA (Low-Rank Adaptation)",
                color=STYLE.foreground.primary,
                font_size=FontSize.SUBTITLE,
                weight=str(FontWeight.SEMIBOLD),
            )
            .to_corner(corner=UL)
            .set_stroke(color=STYLE.foreground.primary)
        )

        self.play(
            FadeOut(total),
            Unwrite(introduction, run_time=1.2),
            transform,
            ReplacementTransform(old_slide_title, slide_title),
        )

        self.next_slide()
        equation = MathTex(r"\vec{h}=W\vec{x} + \vec{b}")
        self.play(Write(equation))
        self.next_slide()
        old_equation = equation
        equation = MathTex(r"\vec{h}=(W_0 + \Delta W)\vec{x} + \vec{b}")
        self.play(ReplacementTransform(old_equation, equation))
        self.next_slide()
        old_equation = equation
        equation = MathTex(r"\vec{h}=W_0\vec{x} + \Delta W\vec{x} + \vec{b}")
        self.play(
            ReplacementTransform(old_equation, equation),
        )
        self.next_slide()
        additional_equation_1 = MathTex(r"W_0,\Delta W \in \mathbb{R}^{d\times k}")
        additional_equation_2 = MathTex(r"\Delta W = AB")
        additional_equation_3 = MathTex(
            r"A \in \mathbb{R}^{d\times r}, B \in \mathbb{R}^{r\times k}, r \ll \min(d,k)"
        )
        self.play(Write(additional_equation_1.next_to(equation, DOWN, buff=0.5)))

        self.play(
            Write(additional_equation_2.next_to(additional_equation_1, DOWN, buff=0.5))
        )
        self.play(
            Write(additional_equation_3.next_to(additional_equation_2, DOWN, buff=0.5))
        )

        self.next_slide()
        old_equation = equation
        equation = MathTex(r"\vec{h}=W_0\vec{x} + AB\vec{x} + \vec{b}")
        self.play(
            Unwrite(additional_equation_2),
            Unwrite(additional_equation_1),
            ReplacementTransform(old_equation, equation),
            additional_equation_3.animate.next_to(old_equation, DOWN),
        )
        self.next_slide()
        old_equation = equation
        equation = MathTex(r"\vec{h}=AB\vec{x} + (W_0\vec{x} + \vec{b})")
        self.play(
            ReplacementTransform(old_equation, equation),
        )
        self.next_slide()
        self.play(
            equation.animate.shift(UP * 2 + LEFT * 3),
            Unwrite(additional_equation_3),
        )
        x = Rectangle(
            width=0.5,
            height=3,
            color=GREY,
            fill_color=GREY,
            fill_opacity=0.6,
        )
        tex_label_x = MathTex(r"\vec{x}", font_size=48)
        tex_label_x.move_to(x.get_center())
        x = VGroup(x, tex_label_x)
        x.shift(DOWN * 0 + LEFT * 0)
        w = Rectangle(
            width=3,
            height=3,
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=0.6,
        )
        tex_label_w = MathTex(r"W \in \mathbb{R}^{d\times k}", font_size=48)
        tex_label_w.move_to(w.get_center())
        w = VGroup(w, tex_label_w)
        w.next_to(x, RIGHT, buff=0.5)
        h = Rectangle(
            width=0.5,
            height=3,
            color=GREY,
            fill_color=GREY,
            fill_opacity=0.6,
        )
        tex_label_h = MathTex(r"\vec{h}", font_size=48)
        tex_label_h.move_to(h.get_center())
        h = VGroup(h, tex_label_h)
        h.next_to(w, RIGHT, buff=0.5)
        self.play(
            FadeIn(x),
            FadeIn(w),
            FadeIn(h),
        )
        self.next_slide()

        a = Polygon(
            w.get_corner(LEFT + DOWN) + UP,
            w.get_corner(LEFT + DOWN) + 2 * DOWN,
            w.get_corner(LEFT + DOWN) + DOWN + RIGHT,
            w.get_corner(LEFT + DOWN) + RIGHT,
            color=ORANGE,
            fill_color=ORANGE,
            fill_opacity=0.6,
        )
        tex_label_a = MathTex(
            r"A_0\sim\mathcal{N}(0, \sigma^2)^{(d \times r)}", font_size=48
        )
        tex_label_a.move_to(a.get_center())
        a = VGroup(a, tex_label_a)
        b = Polygon(
            w.get_corner(RIGHT + DOWN) + UP,
            w.get_corner(RIGHT + DOWN) + 2 * DOWN,
            w.get_corner(RIGHT + DOWN) + DOWN + LEFT,
            w.get_corner(RIGHT + DOWN) + LEFT,
            color=ORANGE,
            fill_color=ORANGE,
            fill_opacity=0.6,
        )
        tex_label_b = MathTex(r"B_0 \equiv 0", font_size=48)
        tex_label_b.move_to(b.get_center()).shift(DOWN * 0.5)
        b = VGroup(b, tex_label_b)
        self.play(
            w.animate.shift(UP * 2),
            FadeIn(a),
            FadeIn(b),
        )
        self.next_slide()
        new_tex_label_a = MathTex(r"A", font_size=48)
        new_tex_label_a.move_to(tex_label_a.get_center())
        new_tex_label_b = MathTex(r"B", font_size=48)
        new_tex_label_b.move_to(tex_label_b.get_center()).shift(UP * 0.5)
        self.play(
            ReplacementTransform(tex_label_a, new_tex_label_a),
            ReplacementTransform(tex_label_b, new_tex_label_b),
        )
        a = VGroup(a, new_tex_label_a)
        b = VGroup(b, new_tex_label_b)
        self.next_slide()
        # TODO: Finish
        self.play(
            w.animate.shift(DOWN * 2),
            a.animate.shift(UP * 2),
            b.animate.shift(UP * 2),
        )
        new_w = Rectangle(
            width=3,
            height=3,
            color=YELLOW,
            fill_color=YELLOW,
            fill_opacity=0.6,
        )
        tex_label_new_w = MathTex(r"W*", font_size=48)
        tex_label_new_w.move_to(new_w.get_center())
        new_w = VGroup(new_w, tex_label_new_w)
        new_w.move_to(w)
        self.play(FadeOut(a), FadeOut(b), ReplacementTransform(w, new_w))
        transform = self.new_slide()
        self.play(
            FadeOut(x),
            FadeOut(new_w),
            FadeOut(h),
        )


        old_slide_title = slide_title
        slide_title = (
            Text(
                text="LoRA: Advantages & Disadvantages",
                color=STYLE.foreground.primary,
                font_size=FontSize.SUBTITLE,
                weight=str(FontWeight.SEMIBOLD),
            )
            .to_corner(corner=UL)
            .set_stroke(color=STYLE.foreground.primary)
        )

        left_points = BulletedList(
            "True Generalisation of Fine-Tuning",
            "No inference latency",
            "More interpretable weights",
            "Effective even at low ranks",
            font_size=FontSize.CONTENT,
        )
        right_points = BulletedList(
            "Introduces information loss",
            "Determining rank is non-trivial",
            font_size=FontSize.CONTENT,
        )
        columns = VGroup(left_points, right_points).arrange(RIGHT, buff=2)
        columns.move_to(ORIGIN)

        self.play(
            transform,
            Unwrite(equation),
            Unwrite(additional_equation_3),
            ReplacementTransform(old_slide_title, slide_title),
        )
        self.play(
            Write(left_points),
        )
        self.next_slide()
        self.play(
            Write(right_points),
        )

        transform = self.new_slide()

        old_slide_title = slide_title
        slide_title = (
            Text(
                text="LoRA: Performance",
                color=STYLE.foreground.primary,
                font_size=FontSize.SUBTITLE,
                weight=str(FontWeight.SEMIBOLD),
            )
            .to_corner(corner=UL)
            .set_stroke(color=STYLE.foreground.primary)
        )

        self.play(
            transform,
            ReplacementTransform(old_slide_title, slide_title),
            Unwrite(columns),
        )

        table_tex = r"""
        \begin{tabular}{l|r|ccc}
        \hline
        \textbf{Model \& Method} & \# Trainable & WikiSQL & MNLI-m & SAMSum  \\
        \hline
        GPT-3 (FT)                  & 175,255.8M & \textbf{73.8} & 89.5 & 52.0/28.0/44.5 \\
        GPT-3 (BitFit)              & 14.2M      & 71.3 & 91.0 & 51.3/27.4/43.5 \\
        GPT-3 (PreEmbed)            & 3.2M       & 63.1 & 88.6 & 48.3/24.2/40.5 \\
        GPT-3 (PreLayer)            & 20.2M      & 70.1 & 89.5 & 50.8/27.3/43.5 \\
        GPT-3 (Adapter\textsuperscript{H}) & 7.1M  & 71.9 & 89.8 & 53.0/28.9/44.8 \\
        GPT-3 (Adapter\textsuperscript{H}) & 40.1M & 73.2 & \textbf{91.5} & 53.2/29.0/45.1 \\
        GPT-3 (LoRA)                & 4.7M       & 73.4 & \textbf{91.7} & \textbf{53.8/29.8/45.9} \\
        GPT-3 (LoRA)                & 37.7M      & \textbf{74.0} & \textbf{91.6} & 53.4/29.2/45.1 \\
        \hline
        \end{tabular}
        """

        table = Tex(table_tex).scale(0.6)
        table.move_to(UP * 0.5)  # shift up to leave space for caption

        caption_text = (
            r"Performance of different adaptation methods on GPT-3 175B. "
            r"Logical form validation accuracy on WikiSQL, validation accuracy on MultiNLI-matched, "
            r"and Rouge-1/2/L on SAMSum. LoRA performs better than prior approaches, including full fine-tuning."
        )
        caption = (
            Tex(caption_text, font_size=24)
            .next_to(table, DOWN, buff=0.3)
            .scale(0.8)
            .set_color(WHITE)
        )

        self.play(Write(table))
        self.play(Write(caption, shift=DOWN))

        transform = self.new_slide()

        old_slide_title = slide_title
        slide_title = (
            Text(
                text="QLoRA (Quantised LoRA)",
                color=STYLE.foreground.primary,
                font_size=FontSize.SUBTITLE,
                weight=str(FontWeight.SEMIBOLD),
            )
            .to_corner(corner=UL)
            .set_stroke(color=STYLE.foreground.primary)
        )

        self.play(
            Unwrite(caption, run_time=0.5),
        )
        self.play(
            Unwrite(table, run_time=1),
            transform,
            ReplacementTransform(old_slide_title, slide_title),
        )

        transform = self.new_slide()

        old_slide_title = slide_title
        slide_title = (
            Text(
                text="QLoRA: Advantages & Disadvantages",
                color=STYLE.foreground.primary,
                font_size=FontSize.SUBTITLE,
                weight=str(FontWeight.SEMIBOLD),
            )
            .to_corner(corner=UL)
            .set_stroke(color=STYLE.foreground.primary)
        )

        self.play(
            transform,
            ReplacementTransform(old_slide_title, slide_title),
        )

        transform = self.new_slide()

        old_slide_title = slide_title
        slide_title = (
            Text(
                text="QLoRA: Performance",
                color=STYLE.foreground.primary,
                font_size=FontSize.SUBTITLE,
                weight=str(FontWeight.SEMIBOLD),
            )
            .to_corner(corner=UL)
            .set_stroke(color=STYLE.foreground.primary)
        )

        self.play(
            transform,
            ReplacementTransform(old_slide_title, slide_title),
        )

        transform = self.new_slide()

        old_slide_title = slide_title
        slide_title = (
            Text(
                text="Discussion Points",
                color=STYLE.foreground.primary,
                font_size=FontSize.SUBTITLE,
                weight=str(FontWeight.SEMIBOLD),
            )
            .to_corner(corner=UL)
            .set_stroke(color=STYLE.foreground.primary)
        )

        discussion = VGroup(
            Text(
                text="1. It's surprising that LoRA can perform well even at low ranks.\nIs there truly that low dimensionality needed for the task?\nAnd if so how can LoRA find it effectively amongst the heavily overparameterised model?",
                weight=str(FontWeight.SEMIBOLD),
            ),
            Text(
                text="2. Discussion Point 2: TODO",
                weight=str(FontWeight.SEMIBOLD),
            ),
        )
        discussion.arrange(
            direction=DOWN,
            aligned_edge=LEFT,
        ).center().shift(0.5 * UP)

        self.play(
            transform,
            ReplacementTransform(old_slide_title, slide_title),
        )
        self.play(Write(discussion, run_time=2))

        transform = self.new_slide()

        old_slide_title = slide_title
        slide_title = (
            Text(
                text="Questions?",
                color=STYLE.foreground.primary,
                font_size=FontSize.TITLE,
                weight=str(FontWeight.SEMIBOLD),
            )
            .center()
            .set_stroke(color=STYLE.foreground.primary)
        )

        self.play(
            Unwrite(discussion, run_time=1),
        )
        self.play(
            transform,
            ReplacementTransform(old_slide_title, slide_title),
        )
