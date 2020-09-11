import os
from pathlib import Path

from ddb.__main__ import load_registered_features
from ddb.config import config
from ddb.feature import features
from ddb.feature.certs import CertsFeature
from ddb.feature.core import CoreFeature
from ddb.feature.docker import DockerFeature
from ddb.feature.traefik import TraefikFeature
from ddb.feature.traefik.actions import TraefikInstalllCertsAction, TraefikUninstalllCertsAction, \
    TraefikExtraServicesAction


class TestTraefikFeature:
    def test_empty_project_without_core(self, project_loader):
        project_loader("empty")

        features.register(TraefikFeature())
        load_registered_features()

        assert config.data.get('traefik.disabled') is True

    def test_empty_project_with_core(self, project_loader):
        project_loader("empty")

        features.register(CoreFeature())
        features.register(TraefikFeature())
        load_registered_features()

        assert config.data.get('traefik.disabled') is True

    def test_install_certs(self, project_loader):
        project_loader("install-certs")

        features.register(CoreFeature())
        features.register(TraefikFeature())
        load_registered_features()

        install_action = TraefikInstalllCertsAction()
        install_action.execute(domain="dummy.tld",
                               private_key=os.path.join(".certs", "some-dummy.tld.key"),
                               certificate=os.path.join(".certs", "some-dummy.tld.crt"))

        assert os.path.exists(os.path.join(config.paths.home, "certs", "dummy.tld.key"))
        assert os.path.exists(os.path.join(config.paths.home, "certs", "dummy.tld.crt"))

        with open(os.path.join(config.paths.home, "certs", "dummy.tld.crt")) as crt_file:
            assert 'crt' == crt_file.read()

        with open(os.path.join(config.paths.home, "certs", "dummy.tld.key")) as key_file:
            assert 'key' == key_file.read()

        assert os.path.exists(os.path.join(config.paths.home, "traefik", "config", "dummy.tld.ssl.toml"))

        uninstall_action = TraefikUninstalllCertsAction()
        uninstall_action.execute(domain="dummy.tld")

        assert not os.path.exists(os.path.join(config.paths.home, "traefik", "config", "dummy.tld.ssl.toml"))

    def test_extra_services(self, project_loader):
        project_loader("extra-services")

        features.register(CoreFeature())
        features.register(TraefikFeature())
        features.register(DockerFeature())
        load_registered_features()

        install_action = TraefikExtraServicesAction()
        install_action.initialize()
        install_action.execute()

        api_toml = os.path.join(config.paths.home, "traefik", "config",
                                "sub.project.test.extra-service.api.toml")
        assert os.path.exists(api_toml)

        api_toml_expected = Path(os.path.join(config.paths.home, "traefik", "config",
                                              "sub.project.test.extra-service.api.expected.toml"))

        assert api_toml_expected.read_text() == Path(api_toml).read_text()

        web_toml = os.path.join(config.paths.home, "traefik", "config", "rule.project.test.extra-service.web.toml")
        assert os.path.exists(web_toml)

        web_toml_expected = Path(os.path.join(config.paths.home, "traefik", "config",
                                              "rule.project.test.extra-service.web.expected.toml"))

        assert web_toml_expected.read_text().replace('{{ip}}', config.data.get('docker.debug.host')) == Path(web_toml).read_text()
