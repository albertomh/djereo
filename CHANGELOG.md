<!-- markdownlint-disable MD013 -->
# Changelog

Notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This file is automatically updated by Release Please.

## [0.9.0](https://github.com/albertomh/djereo/compare/v0.8.0...v0.9.0) (2025-01-26)


### Features

* Add a system check to prevent plural model names ([#47](https://github.com/albertomh/djereo/issues/47)) ([510ef0e](https://github.com/albertomh/djereo/commit/510ef0ef74be19d0b7cc4eac3357c66c54fa9111))
* **ci:** Add a sys-check action to gen. project's pipeline ([#45](https://github.com/albertomh/djereo/issues/45)) ([030b8a9](https://github.com/albertomh/djereo/commit/030b8a9a9560395376f91ef4ea7d4720f1402f94))
* **docs:** Add a mkdocs microsite styled with readthedocs theme ([#50](https://github.com/albertomh/djereo/issues/50)) ([48fd9f9](https://github.com/albertomh/djereo/commit/48fd9f9413c5c41b561ebf587b4bb1805e5b9d3a))
* **docs:** Document GitHub Actions in gen. project's dev README ([#57](https://github.com/albertomh/djereo/issues/57)) ([14f8173](https://github.com/albertomh/djereo/commit/14f8173b934cc50b5d58b7108872f75bd5088f38))
* Set USE_I18N to False in gen. projects for performance ([256a442](https://github.com/albertomh/djereo/commit/256a44235978dd5fd54d1aa481b4db32ea0bf21e))
* Use django-version-checks to alert to version mismatches ([#48](https://github.com/albertomh/djereo/issues/48)) ([293e5cb](https://github.com/albertomh/djereo/commit/293e5cb0b40cbd6231b63120a9b5b8025e5694c6))


### Documentation

* Copier setup questionnaire in mkdocs ([#54](https://github.com/albertomh/djereo/issues/54)) ([087d6e8](https://github.com/albertomh/djereo/commit/087d6e86aac3eb34e2b3dd9f4a40f0b54824fcd6))
* Features implemented from BYDDX in mkdocs ([#53](https://github.com/albertomh/djereo/issues/53)) ([12b4052](https://github.com/albertomh/djereo/commit/12b40520150b667f3ed786ee44882de6cf49f528))
* Generated project's 'justfile' in mkdocs ([#56](https://github.com/albertomh/djereo/issues/56)) ([6f88fae](https://github.com/albertomh/djereo/commit/6f88fae6a2d0cf94f0634917a42bc892d1fd2812))
* Pre-commit git hooks in mkdocs ([#55](https://github.com/albertomh/djereo/issues/55)) ([64c8b0b](https://github.com/albertomh/djereo/commit/64c8b0b5a3e10cdd7f50da093762a93c5f01d8d2))
* Update mkdocs microsite ([#52](https://github.com/albertomh/djereo/issues/52)) ([06a5658](https://github.com/albertomh/djereo/commit/06a56584d50a0e5235b59639894efe9a8e8edb6a))

## [0.8.0](https://github.com/albertomh/djereo/compare/v0.7.0...v0.8.0) (2025-01-23)


### Features

* Add 'just manage' recipe to gen. projects ([#43](https://github.com/albertomh/djereo/issues/43)) ([e0ed5f6](https://github.com/albertomh/djereo/commit/e0ed5f67d0f1813616d89beafca9b8285822be83))
* Allow passing arguments to 'just test' in gen. project ([#39](https://github.com/albertomh/djereo/issues/39)) ([1fcbdcb](https://github.com/albertomh/djereo/commit/1fcbdcb8305b1a15db0c4b22cbf07e43c5c74e08))
* Test suite fails if there are pending migrations in gen. project ([#41](https://github.com/albertomh/djereo/issues/41)) ([937d5c0](https://github.com/albertomh/djereo/commit/937d5c0c3b8c7d5e22787da7ade888cc062ffa82))
* Use django-linear-migrations in generated projects ([#42](https://github.com/albertomh/djereo/issues/42)) ([585b964](https://github.com/albertomh/djereo/commit/585b964f8f610e0c5e2bab3bfe2ea0ec2ff5be56))


### Bug Fixes

* Pass correct default arg to 'just test' recipe ([#44](https://github.com/albertomh/djereo/issues/44)) ([cb4fddf](https://github.com/albertomh/djereo/commit/cb4fddf1e82ff96974beee131509e099dc6c53df))

## [0.7.0](https://github.com/albertomh/djereo/compare/v0.6.0...v0.7.0) (2025-01-21)


### Features

* Add Biome pre-commit hook for frontend formatting & linting ([#38](https://github.com/albertomh/djereo/issues/38)) ([e80536c](https://github.com/albertomh/djereo/commit/e80536c096d2e032f5b9619be58922fec630bd62))
* Format Django templates with Djade via a pre-commit hook ([#34](https://github.com/albertomh/djereo/issues/34)) ([6b78a5d](https://github.com/albertomh/djereo/commit/6b78a5dd9e244b35c43c9f1dabe7d60c229297c9))


### Dependencies

* Upgrade to pycliche v2.13.0 ([#37](https://github.com/albertomh/djereo/issues/37)) ([e855ef3](https://github.com/albertomh/djereo/commit/e855ef35541ca14be6181d081a6a15386c698959))

## [0.6.0](https://github.com/albertomh/djereo/compare/v0.5.0...v0.6.0) (2025-01-19)


### Features

* Ban importing the project settings module directly in gen. projects ([#33](https://github.com/albertomh/djereo/issues/33)) ([1cbf892](https://github.com/albertomh/djereo/commit/1cbf89223d037c880792293a2de9e8138b9dcdb0))
* Read settings from a .env file in generated projects ([#31](https://github.com/albertomh/djereo/issues/31)) ([bcb1dd1](https://github.com/albertomh/djereo/commit/bcb1dd1dc0f8162391723ee6ecf1479786afb655))
* Use sensible defaults instead of .env values in gen. project tests ([#32](https://github.com/albertomh/djereo/issues/32)) ([0f747d8](https://github.com/albertomh/djereo/commit/0f747d8954aa17c6aeeca82a16b0665755c67795))
* Use the django-upgrade pre-commit hook in generated projects ([#29](https://github.com/albertomh/djereo/issues/29)) ([5619083](https://github.com/albertomh/djereo/commit/561908314126a17a84ed719d2b40d4cd2a3624db))

## [0.5.0](https://github.com/albertomh/djereo/compare/v0.4.0...v0.5.0) (2025-01-17)


### Features

* Add Django Debug Toolbar to generated projects ([#25](https://github.com/albertomh/djereo/issues/25)) ([0f5511f](https://github.com/albertomh/djereo/commit/0f5511f014f57ea2ff965c6b74ca52c7e7f8807b))
* Add django-browser-reload for local use in generated projects ([#26](https://github.com/albertomh/djereo/issues/26)) ([3aee383](https://github.com/albertomh/djereo/commit/3aee3831a16516403dc938535198bd69413bd96a))
* Add simple index page to generated project's core app ([#24](https://github.com/albertomh/djereo/issues/24)) ([890b68d](https://github.com/albertomh/djereo/commit/890b68d857b97e401fb0c79f563d84058e27095b))
* Use 'rich' for dev logs when DEBUG is true in generated projects ([#28](https://github.com/albertomh/djereo/issues/28)) ([f5966ba](https://github.com/albertomh/djereo/commit/f5966ba3e5e7b986fbee361ea8922ce4dfb048cd))


### Documentation

* Fix CHANGELOG for v0.4.0 ([#22](https://github.com/albertomh/djereo/issues/22)) ([a4482f2](https://github.com/albertomh/djereo/commit/a4482f235bfaf65cdeadff7050184b2d33b4f93e))
* Mention developer tools included in generated projects ([#27](https://github.com/albertomh/djereo/issues/27)) ([cd09ab3](https://github.com/albertomh/djereo/commit/cd09ab355e399cebfb80e1f0926acd254871474b))

## [0.4.0](https://github.com/albertomh/djereo/compare/v0.3.0...v0.4.0) (2025-01-15)


### Features

* 'test' recipe in generated project uses Django's testrunner ([a43d8cc](https://github.com/albertomh/djereo/commit/a43d8cc601dd1348fe174cab5051c1409ed3ad7f))
* AppConfig for core Django app in generated project ([db43257](https://github.com/albertomh/djereo/commit/db43257674dbac05db1c395c50fc8d15a3668283))
* Dev documentation on using project metadata in an app ([0e5155f](https://github.com/albertomh/djereo/commit/0e5155f203baee85922626993a6cb2e6a91f9600))
* Document using the IPython shell in the project template dev README ([#18](https://github.com/albertomh/djereo/issues/18)) ([ae800d2](https://github.com/albertomh/djereo/commit/ae800d208a2ce5a1a869f55401efd0efbbf07cc0))
* Include the core app in INSTALLED_APPS by default ([14a7a58](https://github.com/albertomh/djereo/commit/14a7a58310ccd765ee7a2c928938578b3543b9f5))
* Just recipe to invoke runserver with Python's Dev Mode ([#15](https://github.com/albertomh/djereo/issues/15)) ([2c057b5](https://github.com/albertomh/djereo/commit/2c057b5755fa651734b6656dc44de81333b81dbf))
* Runserver recipe enables PYTHONDEVMODE by default ([24a27b4](https://github.com/albertomh/djereo/commit/24a27b45264bfd3660d9d5e2d81268fffebf8be6))
* Set DJANGO_SETTINGS_MODULE when running tests for generated project ([6549d22](https://github.com/albertomh/djereo/commit/6549d22f2e2d73d2714fd772079373e02e3b20b9))
* System check to warn of PYTHONDEVMODE being disabled in generated project ([1916c34](https://github.com/albertomh/djereo/commit/1916c3470973eb1500f7fd390a2792b37f045d35))
* Unit tests for the 'Dev Mode' system check in generated projects ([93933f2](https://github.com/albertomh/djereo/commit/93933f25d33a0dd3669108f64e6009b6780153e7))
* Use ipdb as the debugger in generated projects ([#19](https://github.com/albertomh/djereo/issues/19)) ([9d03507](https://github.com/albertomh/djereo/commit/9d0350744f1e76dc4364561a61c9240ccd333163))


### Dependencies

* Upgrade to pycliche v2.12.0 ([#12](https://github.com/albertomh/djereo/issues/12)) ([2ae2d4f](https://github.com/albertomh/djereo/commit/2ae2d4f5d0d298e0dcde8b31f7a6d31288626c9b))


### Documentation

* Flag project is a work in progress in README ([#4](https://github.com/albertomh/djereo/issues/4)) ([aae194f](https://github.com/albertomh/djereo/commit/aae194f60b553625728357b2615c7bbbeb777d5c))
* Updating pycliche from an upstream remote repo ([#13](https://github.com/albertomh/djereo/issues/13)) ([aff9224](https://github.com/albertomh/djereo/commit/aff922467e43935f4963295dceeefeda118eeae3))

## [0.3.0](https://github.com/albertomh/djereo/compare/v0.2.0...v0.3.0) (2025-01-09)


### Features

* Add type annotation for ALLOWED_HOSTS in template settings.py ([fd9e424](https://github.com/albertomh/djereo/commit/fd9e42405225dd30bba6d150a7bb76f289618a2a))


### Dependencies

* Upgrade to pycliche v2.11.0 ([#10](https://github.com/albertomh/djereo/issues/10)) ([45b75df](https://github.com/albertomh/djereo/commit/45b75dfc97680752accac102bb0816c8f6b5ab86))

## [0.2.0](https://github.com/albertomh/djereo/compare/v0.1.0...v0.2.0) (2024-12-19)


### Features

* Accommodate long lines in generated settings.py ([dd188cc](https://github.com/albertomh/djereo/commit/dd188cc9e1896c74e286dacd0303a89ccf6f09b8))
* Add Django 5.1 as a dependency in the template's pyproject.toml ([3233c06](https://github.com/albertomh/djereo/commit/3233c0691f3fa485ef163283f237b5c1eeedbab9))
* Document how to run the generated Django project ([1c8894d](https://github.com/albertomh/djereo/commit/1c8894da6836976e1dd9a172e0be5b3dfcff7b84))
* New Django 5.1 project in template directory ([dc51da3](https://github.com/albertomh/djereo/commit/dc51da3578d909f07971beb842ba5b43b6216d0d))


### Dependencies

* Upgrade to pycliche v2.10.1 ([#1](https://github.com/albertomh/djereo/issues/1)) ([16fb20e](https://github.com/albertomh/djereo/commit/16fb20ec32a80ff83c8b59cc93962e38f6680315))


## [0.1.0](https://github.com/albertomh/djereo/releases/tag/v0.1.0) (2024-12-18)


### Features

* Initial commit using pycliche v2.10.0 as a base.


### Documentation

* Flag project is a work in progress in README ([#4](https://github.com/albertomh/djereo/issues/4)) ([aae194f](https://github.com/albertomh/djereo/commit/aae194f60b553625728357b2615c7bbbeb777d5c))
