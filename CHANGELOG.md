# Changelog
All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project follows [Semantic Versioning](http://semver.org/).

## [Unreleased]

## [0.4.1] - 2023-06-07
### Fixed
- Hotfix release because version number was not updated.

## [0.4.0] - 2023-06-07
### Added
- Export methods to library: `exports` to list all exports and `module_export`/`module_item_export` to export multiple or a single item
- New example with a flattend result dict

## [0.3.0] - 2021-10-27
### Changed
- Allow to pass a custom `requests.Session()`-compatible session object. This allows to set custom params like authentication or request headers.

### Removed
- Since it's now possible to pass a custom session object, the parameter `requests_kwargs` has been removed

## [0.2.0] - 2021-09-28
### Changed
- The response schema changed
- Pass `map_function` to response in `module_item()` call

## [0.1.0] - 2021-09-16
### Added
- Add support for pagination
- More examples and documentation
- New error superclass

## [0.0.3] - 2021-09-14
### Added
- Workflows to lint and publish the code

### Fixed
- Wrong version number in __init__.py
- Linting errors in code base

## [0.0.2] - 2021-09-13
### Changed
- Add possiblity to provide a `map_function` to parse custom fields

### Added
- Some examples to show how to use this library
- README describing the library

## [0.0.1] - 2021-09-10
### Added
- Initial release of museumpy



# Categories
- `Added` for new features.
- `Changed` for changes in existing functionality.
- `Deprecated` for once-stable features removed in upcoming releases.
- `Removed` for deprecated features removed in this release.
- `Fixed` for any bug fixes.
- `Security` to invite users to upgrade in case of vulnerabilities.

[Unreleased]: https://github.com/metaodi/museumpy/compare/v0.4.1...HEAD
[0.4.1]: https://github.com/metaodi/museumpy/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/metaodi/museumpy/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/metaodi/museumpy/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/metaodi/museumpy/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/metaodi/museumpy/compare/v0.0.3...v0.1.0
[0.0.3]: https://github.com/metaodi/museumpy/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/metaodi/museumpy/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/metaodi/museumpy/releases/tag/v0.0.1
