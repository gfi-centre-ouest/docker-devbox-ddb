import os

from ddb.__main__ import load_registered_features
from ddb.feature import features
from ddb.feature.core import CoreFeature
from ddb.feature.jsonnet import JsonnetFeature, RenderAction


class TestRenderAction:
    def test_empty_project_without_core(self, project_loader):
        project_loader("empty")

        features.register(JsonnetFeature())
        load_registered_features()

        action = RenderAction()
        action.execute()

    def test_empty_project_with_core(self, project_loader):
        project_loader("empty")

        features.register(CoreFeature())
        features.register(JsonnetFeature())
        load_registered_features()

        action = RenderAction()
        action.execute()

    def test_example1(self, project_loader):
        project_loader("example1")

        features.register(CoreFeature())
        features.register(JsonnetFeature())
        load_registered_features()

        action = RenderAction()
        action.execute()

        assert os.path.exists('example1.json')
        with open('example1.json', 'r') as f:
            example = f.read()

        with open('example1.expected.json', 'r') as f:
            example_expected = f.read()

        assert example == example_expected

    def test_example1_yaml(self, project_loader):
        project_loader("example1.yaml")

        features.register(CoreFeature())
        features.register(JsonnetFeature())
        load_registered_features()

        action = RenderAction()
        action.execute()

        assert os.path.exists('example1.another')
        with open('example1.another', 'r') as f:
            example_another = f.read()

        with open('example1.expected.another', 'r') as f:
            example_another_expected = f.read()

        assert example_another == example_another_expected

        assert os.path.exists('example1.yaml')
        with open('example1.yaml', 'r') as f:
            example_yaml = f.read()

        with open('example1.expected.yaml', 'r') as f:
            example_yaml_expected = f.read()

        assert example_yaml == example_yaml_expected

    def test_example2(self, project_loader):
        project_loader("example2")

        features.register(CoreFeature())
        features.register(JsonnetFeature())
        load_registered_features()

        action = RenderAction()
        action.execute()

        assert os.path.exists('example2.json')
        with open('example2.json', 'r') as f:
            example = f.read()

        with open('example2.expected.json', 'r') as f:
            example_expected = f.read()

        assert example == example_expected

    def test_example3(self, project_loader):
        project_loader("example3")

        features.register(CoreFeature())
        features.register(JsonnetFeature())
        load_registered_features()

        action = RenderAction()
        action.execute()

        assert os.path.exists('uwsgi.ini')
        with open('uwsgi.ini', 'r') as f:
            iwsgi = f.read()

        with open('uwsgi.expected.ini', 'r') as f:
            iwsgi_expected = f.read()

        assert iwsgi == iwsgi_expected

        assert os.path.exists('init.sh')
        with open('init.sh', 'r') as f:
            init = f.read()

        with open('init.expected.sh', 'r') as f:
            init_expected = f.read()

        assert init == init_expected

        assert os.path.exists('cassandra.conf')
        with open('cassandra.conf', 'r') as f:
            cassandra = f.read()

        with open('cassandra.expected.conf', 'r') as f:
            cassandra_expected = f.read()

        assert cassandra == cassandra_expected

    def test_example3_with_dir(self, project_loader):
        project_loader("example3.with_dir")

        features.register(CoreFeature())
        features.register(JsonnetFeature())
        load_registered_features()

        action = RenderAction()
        action.execute()

        assert os.path.exists('./target/uwsgi.ini')
        with open('./target/uwsgi.ini', 'r') as f:
            iwsgi = f.read()

        with open('uwsgi.expected.ini', 'r') as f:
            iwsgi_expected = f.read()

        assert iwsgi == iwsgi_expected

        assert os.path.exists('./target/init.sh')
        with open('./target/init.sh', 'r') as f:
            init = f.read()

        with open('init.expected.sh', 'r') as f:
            init_expected = f.read()

        assert init == init_expected

        assert os.path.exists('./target/cassandra.conf')
        with open('./target/cassandra.conf', 'r') as f:
            cassandra = f.read()

        with open('cassandra.expected.conf', 'r') as f:
            cassandra_expected = f.read()

        assert cassandra == cassandra_expected

    def test_config_variables(self, project_loader):
        project_loader("config_variables")

        features.register(CoreFeature())
        features.register(JsonnetFeature())
        load_registered_features()

        action = RenderAction()
        action.execute()

        assert os.path.exists('variables.json')
        with open('variables.json', 'r') as f:
            variables = f.read()

        with open('variables.expected.json', 'r') as f:
            variables_expected = f.read()

        assert variables == variables_expected