# -*- coding: utf-8 -*-
from typing import Iterable, ClassVar

from .actions import RunAction
from .schema import RunSchema
from ..feature import Feature
from ..schema import FeatureSchema
from ...action import Action
from ...command import LifecycleCommand, Command
from ...phase import Phase, DefaultPhase


class RunFeature(Feature):
    """
    Run some binary
    """

    @property
    def name(self) -> str:
        return "binary"

    @property
    def schema(self) -> ClassVar[FeatureSchema]:
        return RunSchema

    @property
    def phases(self) -> Iterable[Phase]:
        return (
            DefaultPhase("run", "Display command to run project binary",
                         lambda parser: parser.add_argument("name"),
                         allow_unknown_args=True),
        )

    @property
    def commands(self) -> Iterable[Command]:
        return (
            LifecycleCommand("run", "Display command to run project binary",
                             "run"),
        )

    @property
    def actions(self) -> Iterable[Action]:
        return (
            RunAction(),
        )
