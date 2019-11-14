# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## 1.2.2 - 2019-11-13
### Fixed
- Request by adding User-Agent since PostNL seems to require that now
- Package that is enroute with unknown date

## 1.2.1 - 2019-08-18
### Fixed
- Resolved an issue when there is no delivery date (yet).
- Fixed the test case for letters

## 1.2.0 - 2019-08-08
### Added
- Created packages and letters classes
- Isoformat parsed datetime for delivery and planned dates
- Added properties for is_delivered and delivery_today
- Renamed methods to get_X with X: deliveries, distributions and letters

## 1.0.2 - 2018-05-28
### Fixed
- Traceback when no deliveryDate is found in shipment

## 1.0.1 - 2018-04-28
### Fixed
- Export custom exception

## 1.0 - 2018-04-22
### Added
- Add custom exception
- Add date time parser for status messages
- Initial public release

## 0.3 - 2018-02-04
### Fixed
- Better exception handling & less code duplication

## 0.2 - 2018-01-24
### Added
- Basic test function
- Add function to retrieve letter status
- Add function to retrieve single letter
- Add function to retrieve single shipment

### Fixed
- Fixed the docstring notation
- Better exception handling & less code duplication

## 0.1 - 2017-10-21
### Added
- Initial (private) release