import pytest
from src.commitizen_ruby.ruby_version_provider import RubyVersionProvider
from commitizen.config.yaml_config import YAMLConfig
from commitizen.exceptions import InvalidConfigurationError
from unittest.mock import patch

import inspect
import pathlib

version_rb = inspect.cleandoc("""# frozen_string_literal: true

    module MyRubyModule
        VERSION = "1.2.3"
    end
    """)

@pytest.fixture()
def mocker(mocker):
    mocker.patch("pathlib.Path.read_text", return_value = version_rb)
    mocker.patch("pathlib.Path.glob", return_value = [pathlib.Path("lib/my_ruby_module/version.rb")])
    yield mocker

def make_config(overwrite = None):
    yaml = YAMLConfig(data="---\ncommitizen:\n", path="dummy")
    if overwrite:
        yaml._settings['commitizen_ruby'] = {}
        for key in overwrite:
            yaml._settings['commitizen_ruby'][key] = overwrite[key]
    return yaml

class TestRubyVersionProvider:
    def test_init_with_default_without_file_found(self):
        with pytest.raises(InvalidConfigurationError):
            RubyVersionProvider(make_config())

    def test_init_with_default_with_file_found(self, mocker):
        assert RubyVersionProvider(make_config()).file == pathlib.Path('lib/my_ruby_module/version.rb')

    def test_init_with_default(self):
        assert RubyVersionProvider(make_config({'file': '/path/to/file'})).file == pathlib.Path('/path/to/file')

    def test_get_version(self, mocker):
        assert RubyVersionProvider(make_config({})).get_version() == "1.2.3"

    def test_set_version(self, mocker):
        patcher = patch("pathlib.Path.write_text")
        mpatch = patcher.start()

        RubyVersionProvider(make_config({})).set_version("4.5.6")

        mpatch.assert_called_once()
        mpatch.assert_called_with(inspect.cleandoc("""# frozen_string_literal: true

            module MyRubyModule
                VERSION = "4.5.6"
            end
        """))
        patcher.stop()
