from dataclasses import dataclass, field
from manim import ManimColor
from enum import IntEnum, StrEnum


@dataclass
class Colour(object):
    primary: ManimColor
    secondary: ManimColor
    tertiary: ManimColor


class FontSize(IntEnum):
    TITLE = 48
    SUBTITLE = 38
    CONTENT = 28
    INFO = 20
    SOURCE = 10


class FontWeight(StrEnum):
    THIN = "THIN"
    ULTRALIGHT = "ULTRALIGHT"
    LIGHT = "LIGHT"
    BOOK = "BOOK"
    NORMAL = "NORMAL"
    MEDIUM = "MEDIUM"
    SEMIBOLD = "SEMIBOLD"
    BOLD = "BOLD"
    ULTRABOLD = "ULTRABOLD"
    HEAVY = "HEAVY"
    ULTRAHEAVY = "ULTRAHEAVY"


@dataclass
class Style(object):
    foreground: Colour = field(
        default_factory=lambda: Colour(
            primary=ManimColor("#24FFB6"),
            secondary=ManimColor("#2FBE8E"),
            tertiary=ManimColor("#016141"),
        )
    )
    background: Colour = field(
        default_factory=lambda: Colour(
            primary=ManimColor("#000000"),
            secondary=ManimColor("#212121"),
            tertiary=ManimColor("#424242"),
        )
    )
