## [1.4.4](https://github.com/PaloAltoNetworks/ansible_panos_policy_orchestration/compare/v1.4.3...v1.4.4) (2026-01-29)


### Bug Fixes

* Fix CI and force release ([911d6aa](https://github.com/PaloAltoNetworks/ansible_panos_policy_orchestration/commit/911d6aae01a6245e7ccc32fbb33adf4d846f48cb))

## [1.4.3](https://github.com/PaloAltoNetworks/ansible_panos_policy_orchestration/compare/v1.4.2...v1.4.3) (2026-01-29)


### Bug Fixes

* Move to protected tags instead of conditional release ([d8a96ab](https://github.com/PaloAltoNetworks/ansible_panos_policy_orchestration/commit/d8a96ab8a3df1982ef11eb0feeff5cdcf750c439))

## [1.4.2](https://github.com/PaloAltoNetworks/ansible_panos_policy_orchestration/compare/v1.4.1...v1.4.2) (2026-01-29)


### Bug Fixes

* Change semantic release token ([fc30ba5](https://github.com/PaloAltoNetworks/ansible_panos_policy_orchestration/commit/fc30ba530b0dc92fa3d633721550d93d1f55cd89))

## [1.4.1](https://github.com/PaloAltoNetworks/ansible_panos_policy_orchestration/compare/v1.4.0...v1.4.1) (2026-01-29)


### Bug Fixes

* Update semantic release CI message so that it correctly triggers release ([f89e4a9](https://github.com/PaloAltoNetworks/ansible_panos_policy_orchestration/commit/f89e4a99682ee8c03b6eb847a2e6fe71a7b3cdd8))

# [1.4.0](https://github.com/PaloAltoNetworks/ansible_panos_policy_orchestration/compare/v1.3.3...v1.4.0) (2026-01-29)


### Bug Fixes

* Several documentation improvements and example playbook provided ([9296e5d](https://github.com/PaloAltoNetworks/ansible_panos_policy_orchestration/commit/9296e5d5f68f12195dce30caf6293a1266407772))
* Update release CI to now correctly trigger on release, not on master ([da2839b](https://github.com/PaloAltoNetworks/ansible_panos_policy_orchestration/commit/da2839bcc39a0ad7433b88e121847fe047a7f9ce))


### Features

* Added ARE support for test command. Note that zone resolution is not supported as FIB Lookup API for ARE is broken. ([c6d546c](https://github.com/PaloAltoNetworks/ansible_panos_policy_orchestration/commit/c6d546cbe6e4157c3c6a6847df07833720347a87))
* Added lookup_policy role ([21c7d9d](https://github.com/PaloAltoNetworks/ansible_panos_policy_orchestration/commit/21c7d9d0e49a870047b491fe7117da5c547b747b))
* Example playbooks are now executable as collection playbooks ([891802d](https://github.com/PaloAltoNetworks/ansible_panos_policy_orchestration/commit/891802d5c4c950ba5d7a4aac62621cc505a2e279))

## [1.3.3](https://github.com/PaloAltoNetworks/ansible_panos_policy_orchestration/compare/v1.3.2...v1.3.3) (2026-01-27)


### Bug Fixes

* Publish content to AAP ([9a423c9](https://github.com/PaloAltoNetworks/ansible_panos_policy_orchestration/commit/9a423c96cc5dc66d62a3608d438449d100c14fcc))

## [1.3.2](https://github.com/PaloAltoNetworks/ansible_panos_policy_orchestration/compare/v1.3.1...v1.3.2) (2026-01-13)


### Bug Fixes

* All content updated to fit the standard for Ansible Validated Content ([#13](https://github.com/PaloAltoNetworks/ansible_panos_policy_orchestration/issues/13)) ([4c224cc](https://github.com/PaloAltoNetworks/ansible_panos_policy_orchestration/commit/4c224cc7aa3677836c22e88f5531bcce8c178c41))

## [1.3.1](https://github.com/PaloAltoNetworks/ansible_panos_policy_orchestration/compare/v1.3.0...v1.3.1) (2025-12-10)


### Bug Fixes

* Update plugin and reference guide ([#12](https://github.com/PaloAltoNetworks/ansible_panos_policy_orchestration/issues/12)) ([01822b5](https://github.com/PaloAltoNetworks/ansible_panos_policy_orchestration/commit/01822b57f638f61ad5f6b3af579c1d5ed0286b85))

# [1.3.0](https://github.com/PaloAltoNetworks/ansible_panos_policy_orchestration/compare/v1.2.1...v1.3.0) (2025-12-09)


### Features

* Refactor for Ansible submission ([#11](https://github.com/PaloAltoNetworks/ansible_panos_policy_orchestration/issues/11)) ([904a782](https://github.com/PaloAltoNetworks/ansible_panos_policy_orchestration/commit/904a7828de2886db603e33c2f490627273467e6a))

## [1.2.1](https://github.com/adambaumeister/ansible_panos_policy_orchestration/compare/v1.2.0...v1.2.1) (2025-09-29)


### Bug Fixes

* Simplified test security policy match playbook ([6d0c7c2](https://github.com/adambaumeister/ansible_panos_policy_orchestration/commit/6d0c7c2a24df51437faf9ca5b00b670d615ea486))
* Test command actually implemented properly ([a496036](https://github.com/adambaumeister/ansible_panos_policy_orchestration/commit/a496036feeaa1ab7f1862cf955bebde5bb58ff38))

# [1.2.0](https://github.com/adambaumeister/ansible_panos_policy_orchestration/compare/v1.1.0...v1.2.0) (2025-09-25)


### Features

* Preset policy now also supports URL category additions ([172f274](https://github.com/adambaumeister/ansible_panos_policy_orchestration/commit/172f27444514a15c7cf1fc737c4571ed23793f41))

# [1.1.0](https://github.com/adambaumeister/ansible_panos_policy_orchestration/compare/v1.0.0...v1.1.0) (2025-09-24)


### Bug Fixes

* Commit and Push now occurs for preset and new policies ([56842ef](https://github.com/adambaumeister/ansible_panos_policy_orchestration/commit/56842efae5530f872e54ddfe1bf9b6a516f485d1))


### Features

* Test process now runs before and after any changes ([cba7db8](https://github.com/adambaumeister/ansible_panos_policy_orchestration/commit/cba7db8e36ce270a750d2eb8538913f0c06c3b99))

# 1.0.0 (2025-09-23)


### Bug Fixes

* Address creation now adds to existing groups instead of overridding ([139bb22](https://github.com/adambaumeister/ansible_panos_policy_orchestration/commit/139bb225d196196bcd32caaa4ae6de5fc2dea850))
* Handle rule location ([ca5545b](https://github.com/adambaumeister/ansible_panos_policy_orchestration/commit/ca5545b708623fa19bc9fcb3c2dae16928f5f4dc))


### Features

* Policy Orchestration with preset and new policy creation ([2ceeb9c](https://github.com/adambaumeister/ansible_panos_policy_orchestration/commit/2ceeb9c6c18604b34c64984ddd780508a31e7158))
