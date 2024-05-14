# Commitizen Ruby Version Provider

A commitizen version provider for Ruby projects / gems.

## Installation

    pip install commitizen-ruby

## Usage

### Configuration

There are several ways to configure commitizen.
This example setup uses a local installation of commitizen via python and works  with `yaml` configuration files, but any other format as stated in the commitizen documentation works as well.

In your project root folder, create a `.cz.yaml`:

    ---
    commitizen:
      name: cz_conventional_commits
      tag_format: $version
      update_changelog_on_bump: true
      version_provider: "commitizen-ruby"
      version_scheme: semver

Note: it's not necessary to include a `version` key inside the config file. Best practice is to keep the version in a single source of truth, which is the `version.rb` or similar file inside the ruby project.

By default, a `version.rb` is looked up inside a `lib/*/` folder. If this differs from your project, the version file can be configured:

    ---
    commitizen:
      commitizen_ruby:
        file: /path/to/version.rb

When nothing is configured and no file could be found, an exception is raised.

### Bumping versions

Now

    cz bump

will read the current version from the ruby file, increase it accordingly and write it back to the same file.

## Contribution

Contributions, issues and feature requests are welcome.
For major changes, please open an issue first to discuss what you would like to change.

- Fork the project
- Clone the fork
- Add your changes and update tests as appropriate.
- Create a pull request

## License

This project is [MIT](LICENSE) licensed.
