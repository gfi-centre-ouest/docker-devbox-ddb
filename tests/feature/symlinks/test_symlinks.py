import os

import pytest

from ddb.__main__ import load_registered_features
from ddb.feature import features
from ddb.feature.core import CoreFeature
from ddb.feature.feature import FeatureConfigurationError
from ddb.feature.symlinks import CreateAction, SymlinksFeature


class TestConfigureAction:
    def test_empty_configuration_without_core(self, project_loader):
        project_loader("empty")

        with pytest.raises(FeatureConfigurationError):
            features.register(SymlinksFeature())
            load_registered_features()

    def test_empty_configuration_with_core(self, project_loader):
        project_loader("empty")

        features.register(CoreFeature())
        features.register(SymlinksFeature())
        load_registered_features()

        action = CreateAction()
        action.execute()

    def test_project_1(self, project_loader):
        project_loader("project1")

        features.register(CoreFeature())
        features.register(SymlinksFeature())
        load_registered_features()

        action = CreateAction()
        action.execute()

        assert os.path.exists('test')
        assert os.path.islink('test')
        assert os.path.exists('test')

        assert os.path.exists('test.yml')
        assert os.path.islink('test.yml')
        assert os.path.exists('test.yml')

    def test_project_2_fallback(self, project_loader):
        project_loader("project2")

        features.register(CoreFeature())
        features.register(SymlinksFeature())
        load_registered_features()

        action = CreateAction()
        action.execute()

        assert os.path.islink('test')
        assert os.readlink('test') == 'test.stage'
        assert os.path.exists('test')

        assert os.path.islink('test.yml')
        assert os.readlink('test.yml') == 'test.dev.yml'
        assert os.path.exists('test.yml')

        assert os.path.islink('test2')
        assert os.readlink('test2') == 'test2.prod'
        assert os.path.exists('test2')


        assert not os.path.islink('test3')

    def test_project_4_subdirectory(self, project_loader):
        project_loader("project4")

        features.register(CoreFeature())
        features.register(SymlinksFeature())
        load_registered_features()

        action = CreateAction()
        action.execute()

        assert os.path.islink(os.path.join('subdirectory', 'test.yml'))
        assert os.readlink(os.path.join('subdirectory', 'test.yml')) == 'test.dev.yml'

        assert os.path.exists(os.path.join('subdirectory', 'test.yml'))

        assert not os.path.islink('no.yml')
