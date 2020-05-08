# -*- coding: utf-8 -*-
from typing import Iterable, ClassVar

from .actions import FixuidDockerComposeAction
from .schema import FixuidSchema
from ..feature import Feature
from ..schema import FeatureSchema
from ...action import Action


class FixuidFeature(Feature):
    """
    Add fixuid to docker-compose services
    """

    @property
    def name(self) -> str:
        return "fixuid"

    @property
    def schema(self) -> ClassVar[FeatureSchema]:
        return FixuidSchema

    @property
    def dependencies(self) -> Iterable[str]:
        return ["docker[optional]"]

    @property
    def actions(self) -> Iterable[Action]:
        return (
            FixuidDockerComposeAction(),
        )
