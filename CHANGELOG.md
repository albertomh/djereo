<!-- markdownlint-disable MD013 -->
# Changelog

Notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This file is automatically updated by Release Please.

## [3.3.0](https://github.com/albertomh/djereo/compare/v3.2.0...v3.3.0) (2025-03-15)


### Features

* Add a 'django_checks' job to the on-tag workflow ([#186](https://github.com/albertomh/djereo/issues/186)) ([d80dd57](https://github.com/albertomh/djereo/commit/d80dd57b1462cf1f7ee4c958c5458e62a2671a33))
* **ci:** Add 'service-health' action to check deployed service ([#184](https://github.com/albertomh/djereo/issues/184)) ([a5f9ea5](https://github.com/albertomh/djereo/commit/a5f9ea5fb7821e7b622c77bf2dcd0e81c21ff638))
* **ci:** Sys-check action can also run in deploy mode ([#183](https://github.com/albertomh/djereo/issues/183)) ([1053b3a](https://github.com/albertomh/djereo/commit/1053b3a9bb82a27d01a6b4f66464a19612d3894d))
* Make app metadata available to templates via a context processor ([#175](https://github.com/albertomh/djereo/issues/175)) ([7ac7b2a](https://github.com/albertomh/djereo/commit/7ac7b2aef6f4f34c267be7fe859fade3d4bb428b))
* Silence W008 SECURE_SSL_REDIRECT sys check as handled by nginx ([#182](https://github.com/albertomh/djereo/issues/182)) ([8f6aa27](https://github.com/albertomh/djereo/commit/8f6aa27dd7ed87db6a6a75ec74c34f3a2a3fd41f))


### Bug Fixes

* **ci:** Avoid redundant 'CI' workflow if merged PR was from Release Please ([#179](https://github.com/albertomh/djereo/issues/179)) ([076956d](https://github.com/albertomh/djereo/commit/076956da07b334c0d1d79511defc8d5bb33b341e))
* **ci:** Pass SERVICE_URL as an input to service-health GH Action ([#187](https://github.com/albertomh/djereo/issues/187)) ([4c41382](https://github.com/albertomh/djereo/commit/4c4138284ed42f9c361ed4d7b606369c9261981a))

## [3.2.0](https://github.com/albertomh/djereo/compare/v3.1.1...v3.2.0) (2025-03-08)


### Features

* Add option to add feature flags via django-waffle to gen. projects ([#172](https://github.com/albertomh/djereo/issues/172)) ([b4f25ef](https://github.com/albertomh/djereo/commit/b4f25ef14e1313b88da67c6a2d7af62b26594c59))
* **ci:** Add a reusable 'containerise' GitHub Action ([#173](https://github.com/albertomh/djereo/issues/173)) ([f7878c3](https://github.com/albertomh/djereo/commit/f7878c32ded84a2c2ab9cd345653be1b27e86472))
* **ci:** Run 'containerise' action after merges & tag creation ([#174](https://github.com/albertomh/djereo/issues/174)) ([fe8e8f4](https://github.com/albertomh/djereo/commit/fe8e8f45b08fa8106c6c6fd9f091741a0840c353))
* Enable postgres pooling by default in gen. projects ([#167](https://github.com/albertomh/djereo/issues/167)) ([e9b20e4](https://github.com/albertomh/djereo/commit/e9b20e40345844b8790d28fce16a4dd95c930ecb))


### Bug Fixes

* Set INTERNAL_IPS only when relevant - if dev tools enabled ([#170](https://github.com/albertomh/djereo/issues/170)) ([67292a5](https://github.com/albertomh/djereo/commit/67292a55a9867605d91170098e9c90250823e9b6))

## [3.1.1](https://github.com/albertomh/djereo/compare/v3.1.0...v3.1.1) (2025-03-05)


### Bug Fixes

* **ci:** Bump uv.lock only if release-please updated its PR ([#164](https://github.com/albertomh/djereo/issues/164)) ([#165](https://github.com/albertomh/djereo/issues/165)) ([81354fc](https://github.com/albertomh/djereo/commit/81354fc2c131ef28fa0ee23b78d8a6d35cd30c3b))

## [3.1.0](https://github.com/albertomh/djereo/compare/v3.0.0...v3.1.0) (2025-03-04)


### Features

* Add healthchecks to gen. projects via django-alive ([#153](https://github.com/albertomh/djereo/issues/153)) ([c0103bf](https://github.com/albertomh/djereo/commit/c0103bf2217614d5d76a1b1f24421659118aa3f8))
* **ci:** Release-please GitHub action updates uv.lock in gen. projects ([#160](https://github.com/albertomh/djereo/issues/160)) ([ed045d2](https://github.com/albertomh/djereo/commit/ed045d2d56d69890532cc5b033776051595e07a0))
* Shuffle django test order in generated projects ([#150](https://github.com/albertomh/djereo/issues/150)) ([f0df83b](https://github.com/albertomh/djereo/commit/f0df83b29adcbea1949338f6ef94d2e6ea6d849f))


### Dependencies

* Add pytest-randomly ([#152](https://github.com/albertomh/djereo/issues/152)) ([4831241](https://github.com/albertomh/djereo/commit/4831241b56aef8c0e39498e865511f7750c87ba1))

## [3.0.0](https://github.com/albertomh/djereo/compare/v2.0.0...v3.0.0) (2025-03-03)


### ⚠ BREAKING CHANGES

* use email, not username for (super)user creation ([#141](https://github.com/albertomh/djereo/issues/141))

### Features

* Add middleware to set missing Cross-Origin headers (COEP & CORP) ([#149](https://github.com/albertomh/djereo/issues/149)) ([c0ea6e5](https://github.com/albertomh/djereo/commit/c0ea6e55ee7b389dc8e1564fab7e844b5f82af29))
* Bump Strict-Transport-Security duration to 3600 seconds ([#147](https://github.com/albertomh/djereo/issues/147)) ([d381c5b](https://github.com/albertomh/djereo/commit/d381c5b7d4c9e385516f3291abd96254d3979d9d))
* **chore:** Enable branch coverage measurement in gen. projects ([#137](https://github.com/albertomh/djereo/issues/137)) ([67826bd](https://github.com/albertomh/djereo/commit/67826bd520420f9fc3b4da8b7d008460cce5e28a))
* Enable Strict-Transport-Security in hosted environments ([#142](https://github.com/albertomh/djereo/issues/142)) ([b49995e](https://github.com/albertomh/djereo/commit/b49995e4c52de9e59719096cae5694075b433555))
* Ensure Django detects secure connection behind reverse proxy ([#148](https://github.com/albertomh/djereo/issues/148)) ([933880b](https://github.com/albertomh/djereo/commit/933880b4a5e67c6274bc0c5f70c59f202dacee30))
* Redirect HTTP requests to HTTPS in hosted environments ([#143](https://github.com/albertomh/djereo/issues/143)) ([31fdcf2](https://github.com/albertomh/djereo/commit/31fdcf261e40f9cf4c19f6d1d927c9b41fe26b9d))
* Remove SECURE_SSL_REDIRECT and handle in reverse proxy ([#145](https://github.com/albertomh/djereo/issues/145)) ([fba942e](https://github.com/albertomh/djereo/commit/fba942e01fa694477c4011e4c3bc67c82692dd4a))
* Set a locked-down Content-Security-Policy in gen. projects ([#144](https://github.com/albertomh/djereo/issues/144)) ([d280e7d](https://github.com/albertomh/djereo/commit/d280e7dbb4bab99ce64f933489df514dcbdc9911))
* Set Permissions-Policy header to sensible restrictions ([#146](https://github.com/albertomh/djereo/issues/146)) ([5f6e381](https://github.com/albertomh/djereo/commit/5f6e38104dcae51d5328896d873f94e7940aacfc))


### Bug Fixes

* Use email, not username for (super)user creation ([#141](https://github.com/albertomh/djereo/issues/141)) ([ee3d6f1](https://github.com/albertomh/djereo/commit/ee3d6f161c321377e2f8c6e550f2b22678e71d31))

## [2.0.0](https://github.com/albertomh/djereo/compare/v1.1.0...v2.0.0) (2025-02-28)


### ⚠ BREAKING CHANGES

* make email AuthUser's username field ([#131](https://github.com/albertomh/djereo/issues/131))

### Features

* Add custom error view templates to gen. projects ([#133](https://github.com/albertomh/djereo/issues/133)) ([1adf2d6](https://github.com/albertomh/djereo/commit/1adf2d637dadb03aa817dba5a68370b8c6c0f286))
* **chore:** Add django-debug-toolbar config to work with htmx boosting ([#130](https://github.com/albertomh/djereo/issues/130)) ([1b552f3](https://github.com/albertomh/djereo/commit/1b552f3bfe79ab7c3a9419ed805e36755bad5bf8))
* Htmx requests automatically pass a header with the CSRFToken ([#128](https://github.com/albertomh/djereo/issues/128)) ([cc755b2](https://github.com/albertomh/djereo/commit/cc755b2f203e2003725e0919c5e42ac6b00d61a9))
* Make email AuthUser's username field ([#131](https://github.com/albertomh/djereo/issues/131)) ([c84b195](https://github.com/albertomh/djereo/commit/c84b195272e9106231ce6eae28f2e6e93905dae4))
* Use email for AuthUser in admin forms ([#132](https://github.com/albertomh/djereo/issues/132)) ([13c8f39](https://github.com/albertomh/djereo/commit/13c8f39243043dc2c738a02a732543200c8c0057))

## [1.1.0](https://github.com/albertomh/djereo/compare/v1.0.0...v1.1.0) (2025-02-25)


### Features

* Add an updated_at timestamp field to the user model ([#126](https://github.com/albertomh/djereo/issues/126)) ([d950c67](https://github.com/albertomh/djereo/commit/d950c67f43d1191d7267fa5f07c8bfd08f52a046))
* Add optional vendorised htmx  ([#127](https://github.com/albertomh/djereo/issues/127)) ([f555ff2](https://github.com/albertomh/djereo/commit/f555ff2fc2e618ad622df5ad63464109dcf66270))
* Add timestamp models to the core app ([#124](https://github.com/albertomh/djereo/issues/124)) ([d597a78](https://github.com/albertomh/djereo/commit/d597a788c63e43f00afd3f8df49c054c84b32c9a))

## [1.0.0](https://github.com/albertomh/djereo/compare/v0.16.0...v1.0.0) (2025-02-23)


### ⚠ BREAKING CHANGES

* add an abstract 'UuidModel' with UUID as primary key ([#121](https://github.com/albertomh/djereo/issues/121))

### Features

* Add 'new project' welcome index page ([#114](https://github.com/albertomh/djereo/issues/114)) ([1726992](https://github.com/albertomh/djereo/commit/172699264fa639d98c00068b92d43b2d45749765))
* Add an abstract 'UuidModel' with UUID as primary key ([#121](https://github.com/albertomh/djereo/issues/121)) ([76f1b69](https://github.com/albertomh/djereo/commit/76f1b699855e2cc19cafe6197df595b8660eec9c))
* **docs:** Add badges to gen. project's README ([#123](https://github.com/albertomh/djereo/issues/123)) ([58651d3](https://github.com/albertomh/djereo/commit/58651d3b07ad3e59bcaeab67d928bfaac636a90e))
* **fix:** Cachebust the collectstatic layer in deployment Dockerfile ([#119](https://github.com/albertomh/djereo/issues/119)) ([184eaef](https://github.com/albertomh/djereo/commit/184eaefdadde03f07a9d8253314df513e0df0579))
* **fix:** Link to index in _base.html's navbar ([#120](https://github.com/albertomh/djereo/issues/120)) ([c402cb9](https://github.com/albertomh/djereo/commit/c402cb9e4317f81bb6026dc6d3c68d65f46aa24f))
* **fix:** Use default staticfiles backend when running tests ([#117](https://github.com/albertomh/djereo/issues/117)) ([451f79f](https://github.com/albertomh/djereo/commit/451f79f8f3d818e8042deb26855d3cf3a2d49247))
* Override and customise django-allauth's base template ([#116](https://github.com/albertomh/djereo/issues/116)) ([6d58fc5](https://github.com/albertomh/djereo/commit/6d58fc5ebe39ac2c9a9d0c17587f4137126f4c5d))


### Bug Fixes

* Avoid loading .env for all justfile recipes ([#118](https://github.com/albertomh/djereo/issues/118)) ([6fccc7c](https://github.com/albertomh/djereo/commit/6fccc7ca7237a45b5a73a75bca6f5e8c1e3263cf))

## [0.16.0](https://github.com/albertomh/djereo/compare/v0.15.0...v0.16.0) (2025-02-19)


### Features

* Add SECRET_KEY_FALLBACKS to settings, default to empty list ([#110](https://github.com/albertomh/djereo/issues/110)) ([2c33ac9](https://github.com/albertomh/djereo/commit/2c33ac92a3d84c4888eb1a32d16d67c25e812818))
* Add the _deploy/ dir. and production-ready Dockerfile template ([#113](https://github.com/albertomh/djereo/issues/113)) ([802851a](https://github.com/albertomh/djereo/commit/802851a2471629b53c0db80ab65bb14cf3672ef3))
* **chore:** Set CSRF and secure cookie settings in response to check --deploy ([#111](https://github.com/albertomh/djereo/issues/111)) ([7de08d5](https://github.com/albertomh/djereo/commit/7de08d5aa5364e67c2418bab07d08b6a67566201))
* **chore:** Update pre-commit hooks in gen. project ([#112](https://github.com/albertomh/djereo/issues/112)) ([5ff1348](https://github.com/albertomh/djereo/commit/5ff1348e47d394f959890ada3f4394468529a71e))
* Collectstatic locally if DEBUG=False ([#102](https://github.com/albertomh/djereo/issues/102)) ([1651db9](https://github.com/albertomh/djereo/commit/1651db90ba195df9cddb3474e5a4c988cc0c168e))
* **docs:** Document GitHub RELEASE_PLEASE_TOKEN in gen. project ([#105](https://github.com/albertomh/djereo/issues/105)) ([95e56ac](https://github.com/albertomh/djereo/commit/95e56acb4dee062105e523dadd45d7f2cb0b8cf4))


### Bug Fixes

* Delete static folder before collectstatic to avoid prompting ([#103](https://github.com/albertomh/djereo/issues/103)) ([843db06](https://github.com/albertomh/djereo/commit/843db06ba45640e658d11d1bc489938ad478fcb7))
* Dev logging handlers use NullHandler if DEBUG=False ([#106](https://github.com/albertomh/djereo/issues/106)) ([11d4622](https://github.com/albertomh/djereo/commit/11d46222649b07cedda2937be3858f66e5f42d8e))
* Override Django's admin.site instead of creating new instance ([#99](https://github.com/albertomh/djereo/issues/99)) ([76e3f36](https://github.com/albertomh/djereo/commit/76e3f364c6edd77e6c795521a282c11b7f373e1d))
* Re-register default models (User, Group) in custom admin ([#108](https://github.com/albertomh/djereo/issues/108)) ([d49e383](https://github.com/albertomh/djereo/commit/d49e38327faa575ae3e0d64cb61b4e9db42afb3e))
* **test:** Do not consider prompt codes in SeedDatabaseTests ([#107](https://github.com/albertomh/djereo/issues/107)) ([e0fb9ad](https://github.com/albertomh/djereo/commit/e0fb9ad527ff49291b5e5e6bb05cddaeaf5f5d41))

## [0.15.0](https://github.com/albertomh/djereo/compare/v0.14.0...v0.15.0) (2025-02-13)


### Features

* Add disable_authuser_signal context manager ([#92](https://github.com/albertomh/djereo/issues/92)) ([91aa68c](https://github.com/albertomh/djereo/commit/91aa68c7555bd021b7fbdbfa58bf8d7accf54488))
* Add factories for AuthUser and UserProfile in gen. projects ([#93](https://github.com/albertomh/djereo/issues/93)) ([abc1f5c](https://github.com/albertomh/djereo/commit/abc1f5cda40a579932c85462bb1c2604f00f9b76))
* Django admin login form reads 'Email' instead of 'Username' ([#98](https://github.com/albertomh/djereo/issues/98)) ([0ffba64](https://github.com/albertomh/djereo/commit/0ffba6494d1b06666e856f6f7f4d086ef0f0b7b0))
* **docs:** Add 'migrate' step to gen. project's README quickstart ([#89](https://github.com/albertomh/djereo/issues/89)) ([3ced1ca](https://github.com/albertomh/djereo/commit/3ced1caa4ffa2dcd33d92b113988a5f98b8d6a9d))
* Seed_database management command creates users for local dev ([#91](https://github.com/albertomh/djereo/issues/91)) ([3f34372](https://github.com/albertomh/djereo/commit/3f343727e7491cece83fbe26e87df9ce9bac55f8))


### Documentation

* 'users' app model factories ([#94](https://github.com/albertomh/djereo/issues/94)) ([4b58765](https://github.com/albertomh/djereo/commit/4b58765abce831e4b1edd9197e06f3e8ec491232))

## [0.14.0](https://github.com/albertomh/djereo/compare/v0.13.0...v0.14.0) (2025-02-10)


### Features

* Add custom auth user ([#83](https://github.com/albertomh/djereo/issues/83)) ([dc3ab41](https://github.com/albertomh/djereo/commit/dc3ab419fe57eddeef111e579ff063be9af9cd8d))
* Add django-allauth to generated projects ([#85](https://github.com/albertomh/djereo/issues/85)) ([3c8aa2e](https://github.com/albertomh/djereo/commit/3c8aa2e2d335dcab245ae11c56bd855771be8970))
* Add UserProfile model to gen. project's 'users' app ([#86](https://github.com/albertomh/djereo/issues/86)) ([719daf1](https://github.com/albertomh/djereo/commit/719daf100fca1e65de77f9a74d2a605ba9589e7b))


### Documentation

* Custom User model & django-allauth in mkdocs ([#87](https://github.com/albertomh/djereo/issues/87)) ([db25189](https://github.com/albertomh/djereo/commit/db25189a6703e033d8ea3f732f5ec5094b3ccb7f))

## [0.13.0](https://github.com/albertomh/djereo/compare/v0.12.0...v0.13.0) (2025-02-06)


### Features

* Add postgres service to gen. project's GitHub Actions workflows ([#82](https://github.com/albertomh/djereo/issues/82)) ([364f68e](https://github.com/albertomh/djereo/commit/364f68ec4b88479ead322d01cf378196d6987f4f))
* Postgres version is configurable via copier questionnaire ([#81](https://github.com/albertomh/djereo/issues/81)) ([1992064](https://github.com/albertomh/djereo/commit/199206466f44bea472eed846306ebf3468f22847))


### Bug Fixes

* Allow editable installs to find the top-level djereo package ([#78](https://github.com/albertomh/djereo/issues/78)) ([6881720](https://github.com/albertomh/djereo/commit/6881720b14cc147c9a57a6388830ee1c2b9c878f))


### Documentation

* Add postgres to featurelist in mkdocs ([#80](https://github.com/albertomh/djereo/issues/80)) ([21b353a](https://github.com/albertomh/djereo/commit/21b353a07789c0fac2e3f2a520d04bb05b9e0dbe))

## [0.12.0](https://github.com/albertomh/djereo/compare/v0.11.0...v0.12.0) (2025-02-05)


### Features

* Add 'tear down' script for postgres database ([#72](https://github.com/albertomh/djereo/issues/72)) ([fe2d8e5](https://github.com/albertomh/djereo/commit/fe2d8e584352e03c97e1d3d94a498f3b6cf253b9))
* Add a .env.test file to generated projects ([#73](https://github.com/albertomh/djereo/issues/73)) ([907ddff](https://github.com/albertomh/djereo/commit/907ddffc2ab0c66ca8fdd71a31d8f74de53e2d88))
* Add postgres as the default database to gen. projects ([#70](https://github.com/albertomh/djereo/issues/70)) ([f0ef8f2](https://github.com/albertomh/djereo/commit/f0ef8f262cb55ed070937eba90e108233d8a709d))


### Bug Fixes

* **test:** Database use in gen. project integration tests  ([#74](https://github.com/albertomh/djereo/issues/74)) ([c32ce13](https://github.com/albertomh/djereo/commit/c32ce133987a4dd8ef8e12eb60525600cd25c79d))

## [0.11.0](https://github.com/albertomh/djereo/compare/v0.10.0...v0.11.0) (2025-01-30)


### Features

* Settings.DEBUG toggles between structlog and rich logging ([#69](https://github.com/albertomh/djereo/issues/69)) ([4928e29](https://github.com/albertomh/djereo/commit/4928e29d96b503aa2f4311d043d072005dcbf402))


### Bug Fixes

* Just 'test' recipe's check for installed dependencies ([#67](https://github.com/albertomh/djereo/issues/67)) ([74bd056](https://github.com/albertomh/djereo/commit/74bd056446c2ab9b75ba207d66cc9f32ec5aa538))

## [0.10.0](https://github.com/albertomh/djereo/compare/v0.9.0...v0.10.0) (2025-01-29)


### Features

* Serve static files from gen. project using whitenoise ([#61](https://github.com/albertomh/djereo/issues/61)) ([bf4e64b](https://github.com/albertomh/djereo/commit/bf4e64b489578eafcc80fa930bc20db58e72f28a))


### Bug Fixes

* **docs:** Correct 'Edit on GitHub' path in mkdocs ([#58](https://github.com/albertomh/djereo/issues/58)) ([4616074](https://github.com/albertomh/djereo/commit/461607474841aea33463b443b1dbd03f0704690a))
* Provide default value to SECRET_KEY when running tests ([#64](https://github.com/albertomh/djereo/issues/64)) ([aab7803](https://github.com/albertomh/djereo/commit/aab7803389de8cb9410945a82280bf3f5460fdfb))
* Remove default value for SECRET_KEY setting ([#60](https://github.com/albertomh/djereo/issues/60)) ([c0d7643](https://github.com/albertomh/djereo/commit/c0d76433d0b064cc8f6be93e5f9d820e88756e40))
* Use djereo tag in settings.py docstring ([#66](https://github.com/albertomh/djereo/issues/66)) ([dda2136](https://github.com/albertomh/djereo/commit/dda2136d32a68be90fa1c904e89b2d96e73a79cf))

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
