# -*- coding: utf-8 -*-
import fnmatch
import os
import re
from pathlib import Path
from typing import List, Union, Optional, Tuple

from braceexpand import braceexpand

from ddb.context import context


def has_same_content(filename1: str, filename2: str) -> bool:
    """
    Check if the content of two files are same
    """
    with open(filename1, 'rb') as file1:
        with open(filename2, 'rb') as file2:
            return file1.read() == file2.read()


class FileWalker:
    """
    Walk files inside project directory.
    """

    # pylint:disable=too-many-arguments
    def __init__(self,
                 includes: Optional[List[str]],
                 excludes: Optional[List[str]],
                 suffixes: Optional[List[str]],
                 rootpath: Union[Path, str] = Path('.'),
                 recursive=True,
                 skip_processed_sources=True,
                 skip_processed_targets=True):
        if includes is None:
            includes = []
        if excludes is None:
            excludes = []
        includes, excludes = self._braceexpand(includes, excludes)
        self.includes = list(map(lambda x: re.compile(fnmatch.translate(x)), includes))
        self.excludes = list(map(lambda x: re.compile(fnmatch.translate(x)), excludes))
        self.suffixes = suffixes if suffixes is not None else []
        self.rootpath = rootpath if isinstance(rootpath, Path) else Path(rootpath)
        self.recursive = recursive
        self.skip_processed_sources = skip_processed_sources
        self.skip_processed_targets = skip_processed_targets

    @property
    def items(self):
        """
        Yields over a tuple (template, target) with found templates.
        """

        for source in self._walk(str(self.rootpath), recursive=self.recursive):
            yield from self._do_yield(source)

    def _do_yield(self, source):  # pylint:disable=no-self-use
        yield source

    def _walk(self, *args, recursive=True, **kwargs):
        _walk_generator = os.walk(*args, **kwargs)
        if not recursive:
            try:
                _walk_generator = next(_walk_generator)
            except StopIteration:
                return
        for root, dirs, files in os.walk(*args, **kwargs):
            for dirs_item in list(dirs):
                dirpath = os.path.join(root, dirs_item)
                if self._is_excluded(dirpath, *self.excludes):
                    dirs.remove(dirs_item)

            for files_item in list(files):
                filepath = os.path.join(root, files_item)
                if self._is_included(filepath, *self.includes) and \
                        not self._is_excluded(filepath, *self.excludes):
                    yield filepath

    @staticmethod
    def _braceexpand(includes, excludes):
        expanded_includes = []
        for include in includes:
            expanded_includes.extend(braceexpand(include))

        expanded_excludes = []
        for exclude in excludes:
            expanded_excludes.extend(braceexpand(exclude))

        return expanded_includes, expanded_excludes

    @staticmethod
    def _is_excluded(candidate: str, *excludes: List[str]) -> bool:
        excluded = False
        norm_candidate = None
        if not excludes:
            return False
        for exclude in excludes:
            if not norm_candidate:
                norm_candidate = os.path.normpath(candidate)
            if exclude.match(candidate) or exclude.match(norm_candidate):
                excluded = True
                break
        return excluded

    @staticmethod
    def _is_included(candidate: str, *includes: List[str]) -> bool:
        included = False
        norm_candidate = None
        if not includes:
            return True
        for include in includes:
            if not norm_candidate:
                norm_candidate = os.path.normpath(candidate)
            if include.match(candidate) or include.match(norm_candidate):
                included = True
                break
        return included

    @staticmethod
    def build_default_includes_from_suffixes(suffixes: List[str], extensions=(".*", "")):
        """
        Build default includes configuration from suffixes configuration.
        """
        if extensions:
            extensions_pattern = "{" + ",".join(extensions) + "}"
        else:
            extensions_pattern = ""

        if len(suffixes) > 1:
            joined_suffixes = ','.join(suffixes)
            return ["**/*{" + joined_suffixes + "}" + extensions_pattern]
        if len(suffixes) > 0:
            return ["**/*" + suffixes[0] + extensions_pattern]
        if extensions_pattern:
            return ["**/*" + suffixes[0] + extensions_pattern]
        return []


class TemplateFinder(FileWalker):
    """
    Find templates sources inside project directory.
    """

    def _do_yield(self, source):
        target = self.get_target(source, check=False)
        if target:
            if self.skip_processed_targets:
                if target in context.processed_targets:
                    return
            yield source, target

    def get_target(self, source, check=True):
        """
        Get the target of given source, or None if it doesn't match suffixes.
        """
        if check:
            if not self._is_included(source, *self.includes) or \
                    self._is_excluded(source, *self.excludes):
                return None

        if self.skip_processed_sources:
            if source in context.processed_sources.keys():
                return None

        target, suffix = self._get_target_and_suffix(source, self.suffixes)

        if self.skip_processed_targets:
            if target in context.processed_targets.keys():
                previous_source = context.processed_targets[target]
                _, previous_suffix = self._get_target_and_suffix(previous_source, self.suffixes)
                if previous_suffix not in self.suffixes or \
                        self.suffixes.index(previous_suffix) <= self.suffixes.index(suffix):
                    return None

        return target

    @staticmethod
    def mark_as_processed(source, target):
        """
        Mark sources and target as processed, for them to be skipped by other file template finders.
        """
        context.processed_sources[source] = target
        context.processed_targets[target] = source

    @staticmethod
    def _get_target_and_suffix(template_candidate: str, suffixes: List[str]) -> Optional[Tuple[str, str]]:
        basename, ext = os.path.splitext(template_candidate)
        if ext in suffixes:
            return basename, ext

        if not ext and basename.startswith("."):
            ext = basename
            basename = ""

        for suffix in suffixes:
            if basename.endswith(suffix):
                return template_candidate[:len(basename) - len(suffix)] + ext, suffix

        return None, None
