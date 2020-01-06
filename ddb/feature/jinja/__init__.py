# -*- coding: utf-8 -*-
from typing import ClassVar, Iterable

from dotty_dict import Dotty

from ddb.action import Action
from ddb.feature import Feature
from .actions import RenderAction
from .schema import JinjaSchema
from ...utils.file import TemplateFinder


class JinjaFeature(Feature):
    """
    Render template files with Jinja template engine.
    """

    @property
    def name(self) -> str:
        return "jinja"

    @property
    def schema(self) -> ClassVar[JinjaSchema]:
        return JinjaSchema

    @property
    def actions(self) -> Iterable[Action]:
        return (
            RenderAction(),
        )

    def _configure_defaults(self, feature_config: Dotty):
        includes = feature_config.get("includes")
        if not includes:
            includes = TemplateFinder.build_default_includes_from_suffixes(feature_config["suffixes"])
            feature_config["includes"] = includes
