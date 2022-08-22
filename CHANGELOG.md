# Changelog of action-checkout-repo
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.3] - 2022-08-22

### Fixed
- checkout problem (in case of the same branch)
- bugfix at github runner, relates to select right regex: [release](https://github.com/actions/runner/releases/tag/v2.295.0), [fix](https://github.com/actions/runner/pull/1794)

### Added 
- if regex sha is same to the current default head, take the last possible regex

## [1.3.2] - 2022-05-13

### Fixed
- error if ref not existing -> alt ref should be taken

## [1.3.1] - 2022-05-10

### Fixed
- using a no path input
- submodules checkout possible

## [1.3.0] - 2022-05-05

### Fixed
- test: added ref name checks to all action calls

### Added
- regex option to checkout reference
## [1.2.0] - 2022-05-04

### Fixed
- ref name
- check out this own repo at action

## [1.1.0] - 2022-04-28

### Added
- support for windows and mac
- changelog file

## [1.0.0] - 2022-04-28

### Added
- total functionality
 - git lfs
 - submodules
 - python code for handling ref

## [0.1.0] - 2022-04-27

### Added
- init releas