# CHANGELOG


## v0.5.1 (2025-07-09)

### Bug Fixes

- Python 3.13 support + django version tests + parallel test runs (#115)
  ([#115](https://github.com/NextGenContributions/django2pydantic/pull/115),
  [`8094de0`](https://github.com/NextGenContributions/django2pydantic/commit/8094de0c04af930923fe4323ddc407e470e0cb5a))


## v0.5.0 (2025-06-06)

### Features

- SchemaField + optional contrib 3rd party handlers (#95)
  ([#95](https://github.com/NextGenContributions/django2pydantic/pull/95),
  [`b8bffe7`](https://github.com/NextGenContributions/django2pydantic/commit/b8bffe70bd07deb6a3e20c15b8dad99a003748f2))


## v0.4.4 (2025-06-05)

### Bug Fixes

- JSONField validation should accept python object (#93)
  ([#93](https://github.com/NextGenContributions/django2pydantic/pull/93),
  [`d6dc908`](https://github.com/NextGenContributions/django2pydantic/commit/d6dc9088913b97d5dea4ce4a4d3d2bde6beffd21))


## v0.4.3 (2025-06-03)

### Bug Fixes

- Reverse relation titles more complete (#87)
  ([#87](https://github.com/NextGenContributions/django2pydantic/pull/87),
  [`c6effbe`](https://github.com/NextGenContributions/django2pydantic/commit/c6effbe86f2b515b93deea63933afe075c59df21))


## v0.4.2 (2025-05-30)

### Bug Fixes

- Reverse relation title and description (#83)
  ([#83](https://github.com/NextGenContributions/django2pydantic/pull/83),
  [`018b25f`](https://github.com/NextGenContributions/django2pydantic/commit/018b25f80ceafc576c075d66a6a7819542f51fac))


## v0.4.1 (2025-05-27)

### Bug Fixes

- Various incorrect field types, default value and required status (#75)
  ([#75](https://github.com/NextGenContributions/django2pydantic/pull/75),
  [`6eeb034`](https://github.com/NextGenContributions/django2pydantic/commit/6eeb03461c884c3e48c2395eecc1861da66a668f))


## v0.4.0 (2025-05-21)

### Features

- **#70**: Pydantic Email/URL validation should accept empty string (#69)
  ([#69](https://github.com/NextGenContributions/django2pydantic/pull/69),
  [`1ba4370`](https://github.com/NextGenContributions/django2pydantic/commit/1ba4370809eab3824bb7ac1a8793d8b55e613fc2))


## v0.3.0 (2025-05-05)

### Bug Fixes

- Daily trunk check failure if the commit is already checked (#36)
  ([#36](https://github.com/NextGenContributions/django2pydantic/pull/36),
  [`cf50e0a`](https://github.com/NextGenContributions/django2pydantic/commit/cf50e0a623260352db84b50b768570538e954755))

- Include django-stubs-ext as a non-dev dependency (#16)
  ([#16](https://github.com/NextGenContributions/django2pydantic/pull/16),
  [`b26f36b`](https://github.com/NextGenContributions/django2pydantic/commit/b26f36b80b0ed6e986d5cea8f754ebfebafa8701))

- Trunk permission to create/update label (#55)
  ([#55](https://github.com/NextGenContributions/django2pydantic/pull/55),
  [`e36ed63`](https://github.com/NextGenContributions/django2pydantic/commit/e36ed639cc8e7d17c6e77b8f9104390fe6c55521))

- Trunk's mypy environment missing deps (#26)
  ([#26](https://github.com/NextGenContributions/django2pydantic/pull/26),
  [`383bd51`](https://github.com/NextGenContributions/django2pydantic/commit/383bd51b1e556aad5922affaf5bee301f9c67d95))

- Trunk's mypy incremental cache issue (#34)
  ([#34](https://github.com/NextGenContributions/django2pydantic/pull/34),
  [`85bc639`](https://github.com/NextGenContributions/django2pydantic/commit/85bc639970101332792532b62ff5201fc4da6d12))

### Features

- Add nitpick and configs (#9)
  ([#9](https://github.com/NextGenContributions/django2pydantic/pull/9),
  [`e2949fa`](https://github.com/NextGenContributions/django2pydantic/commit/e2949faf601ff76fadf1a0079b97c47146fe8bce))

- Cache Trunk (#27) ([#27](https://github.com/NextGenContributions/django2pydantic/pull/27),
  [`3e16247`](https://github.com/NextGenContributions/django2pydantic/commit/3e16247ece1fc6e91d0448209cbf77be15ab1ec0))

- Enable workflow_dispatch for cache-trunk (#28)
  ([#28](https://github.com/NextGenContributions/django2pydantic/pull/28),
  [`81356c2`](https://github.com/NextGenContributions/django2pydantic/commit/81356c27f12a8eea9ef6b530fc3876824f5f944f))

- Relation handlers additions/tweaks. Proper annotations/typings (#40)
  ([#40](https://github.com/NextGenContributions/django2pydantic/pull/40),
  [`6a9a05a`](https://github.com/NextGenContributions/django2pydantic/commit/6a9a05ad9779a60aa44603c98538e77bb20ec773))

- Support Trunk.io (#22) ([#22](https://github.com/NextGenContributions/django2pydantic/pull/22),
  [`1b82554`](https://github.com/NextGenContributions/django2pydantic/commit/1b8255416d5f2bd778e457fd6171d7dd7252b3f0))

- Trunk check_mode all for daily check (#29)
  ([#29](https://github.com/NextGenContributions/django2pydantic/pull/29),
  [`6d10fb2`](https://github.com/NextGenContributions/django2pydantic/commit/6d10fb2070fde60e44c25cada39da6c81d454477))

- Validate 'Inferred' relation and return appropriate primary key(s) (#20)
  ([#20](https://github.com/NextGenContributions/django2pydantic/pull/20),
  [`38b38ba`](https://github.com/NextGenContributions/django2pydantic/commit/38b38ba8f0d3aefcf3c0302b8e22900822f40c79))


## v0.2.0 (2024-12-13)

### Features

- Support optional fields (#5)
  ([#5](https://github.com/NextGenContributions/django2pydantic/pull/5),
  [`a1b7a3c`](https://github.com/NextGenContributions/django2pydantic/commit/a1b7a3c49c53a0cdb98d9dd09ea9a819d6c4da00))


## v0.1.3 (2024-12-03)

### Bug Fixes

- DecimalField fix?
  ([`db3e1ba`](https://github.com/NextGenContributions/django2pydantic/commit/db3e1bae28c79223399490cc0be7df0c1a217f20))

- JSONField fix?
  ([`79e1d08`](https://github.com/NextGenContributions/django2pydantic/commit/79e1d083a7bb3683183ab6832e599bd1ac8d77c4))

- Related model inheritance fixes and string format reference support
  ([`fe97eaf`](https://github.com/NextGenContributions/django2pydantic/commit/fe97eaf67209d530589c4eacee245d7d5b0c6e97))


## v0.1.2 (2024-11-29)

### Bug Fixes

- Added pyproject.toml back
  ([`26b2cc0`](https://github.com/NextGenContributions/django2pydantic/commit/26b2cc0733488b8902aa717dd1ff666092d7b675))

- Some default naming of models/related model schemas
  ([`b9fcb76`](https://github.com/NextGenContributions/django2pydantic/commit/b9fcb76944a9a5a8b8e28d13cfd473652da90a3e))


## v0.1.1 (2024-11-21)

### Bug Fixes

- Bump version to skip published v0.1.0 package
  ([`20715a2`](https://github.com/NextGenContributions/django2pydantic/commit/20715a2ccaed13662117492c7ef6ba1a681dee3f))


## v0.1.0 (2024-11-21)


## v0.0.5 (2024-11-21)

### Bug Fixes

- Required dependencies
  ([`aedab64`](https://github.com/NextGenContributions/django2pydantic/commit/aedab64c61c288b3d4057007716aff835d1da5dc))

- Semantic release version_variables for uv.lock
  ([`5d13179`](https://github.com/NextGenContributions/django2pydantic/commit/5d1317923a0f831a82349e9e535f97f414220eba))


## v0.0.4 (2024-11-20)

### Bug Fixes

- Temporarily stop using publish-pypi.yml reusable workflow
  ([`e371d3c`](https://github.com/NextGenContributions/django2pydantic/commit/e371d3cb0e4d4577251b5e51641faee3c4e41228))


## v0.0.3 (2024-11-20)

### Bug Fixes

- Test pipeline by bumping version
  ([`9f449c2`](https://github.com/NextGenContributions/django2pydantic/commit/9f449c262a270956c453308738521c5884311f29))


## v0.0.2 (2024-11-19)

### Bug Fixes

- Fix some errors after rename
  ([`c95ee5a`](https://github.com/NextGenContributions/django2pydantic/commit/c95ee5a73dc88716683e99e35b43582c6fa9342a))


## v0.0.1 (2024-11-18)

### Bug Fixes

- Ci fixes
  ([`9feb63f`](https://github.com/NextGenContributions/django2pydantic/commit/9feb63f7b83af236a067fa3be4affe8bc449a717))

- Update README.md
  ([`bc2ed39`](https://github.com/NextGenContributions/django2pydantic/commit/bc2ed39001e84799e886ea917566c9492fc86dea))


## v0.0.0 (2024-11-18)
