from commitizen.providers import VersionProvider
from commitizen.exceptions import InvalidConfigurationError
from deepmerge import always_merger
from pathlib import Path
import re

class RubyVersionProvider(VersionProvider):
    file = None
    default_config = {
        'file': None
    }
    config = {}
    search_re = r'(\s*)VERSION\s*=\s*"(\d+\.\d+\.\d+)"'

    def __init__(self, config):
        self.config = self.default_config.copy()

        if 'commitizen_ruby' in config._settings:
            self.config = always_merger.merge(self.config, config._settings['commitizen_ruby'])

        if self.config['file']:
            self.file = Path(self.config['file'])
        else:
            for file in Path().glob("lib/*/version.rb"):
                self.file = file
                break

        if self.file == None:
            raise InvalidConfigurationError(f"Can't determine version file and no file path is set in config.")


    def get_version(self) -> str:
        """
        Reads a version string from a ruby module file in the format
            VERSION = "x.y.z"
        """

        contents = self.file.read_text()
        match = re.search(self.search_re, contents)
        if match:
            return match.group(2)

        return "0.0.0"

    def set_version(self, version: str):
        """
        Writes a new ruby version file replacing the version line.
        """
        old_content = self.file.read_text()
        new_content = re.sub(
            self.search_re,
            r'\1VERSION = "%s"' % version,
            old_content
        )

        self.file.write_text(new_content)
