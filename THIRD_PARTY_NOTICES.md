# Third-party notices / 第三方版权与鸣谢

This repository distributes an unofficial modified build of **GestaltX**, based on [huamidev/GestaltX](https://github.com/huamidev/GestaltX) **v1.0.7**, commit `dfd4a7e3a8b8a89e76ac025a2a37242a7ed4c41f`.

**Build-input distinction:** the published historical `v1.0.7-china-unlock` IPA uses upstream `dfd4a7e` plus its tagged patch. The current unshipped LilaShift development build uses upstream **`c60519c619ced032a0b174c13062b3b9bc9ee86f`** plus the newer `main` patch. Do **not** assert the two builds contain identical source.

本仓库分发的 IPA 是 GestaltX 的**非官方修改版**，并非原作者的官方发行包。

## Original application / 原始应用

- Project: **GestaltX**
- Upstream: https://github.com/huamidev/GestaltX
- Original copyright and contributors: retain the copyright and attribution notices in the upstream source
- License: [GNU GPL v3](LICENSE) (upstream v1.0.7 includes this license)
- Original third-party notices: https://github.com/huamidev/GestaltX/blob/v1.0.7/THIRD_PARTY_NOTICES.md

## Modifications / 修改

- Maintainer of this modified build: **@steam8871** (credited for these changes, **not** as the sole author of GestaltX)
- Modifications: China Unlock presets and validation, settings UI styling, descriptions, build integration, restore/backup and related UX as detailed in [README_ZH-CN.md](README_ZH-CN.md)
- Patch: [china-unlock-v107.patch](china-unlock-v107.patch)
- **Published v1.0.7 source**: upstream commit **dfd4a7e3a8b8a89e76ac025a2a37242a7ed4c41f** plus the **tagged** release patch. **Unshipped LilaShift development source**: upstream **c60519c619ced032a0b174c13062b3b9bc9ee86f** plus the **current main** patch. See [provenance matrix](docs/LILASHIFT_PROVENANCE.md).
- Distribution of the modified combined work remains under **GNU GPL v3**, subject to the individual notices applicable to each included component.

## Important upstream third-party notices / 必须保留的上游声明

The original upstream v1.0.7 `THIRD_PARTY_NOTICES.md` identifies, among others:

- **worse_query** — Taj C / forcequitOS; upstream identifies **GPL-3.0-or-later** for the incorporated implementation: https://github.com/forcequitOS/worse_query
- **NeoSpring/WebKit respring** — references and adapted work credited to neonmodder123, skadz108, rooootdev and Nouvborne/Ketamine; consult upstream's notices for the precise attribution and adaptation details
- **Primer Octicons GitHub mark** — upstream references the MIT license and a bundled `Primer-Octicons-MIT.txt`
- **MGKeys, Nugget, mond and GestaltEdit** — credited by upstream as research/workflow references, not as code bundled simply by naming them.

**This document supplements, and does not replace, original source-file copyright headers, upstream `THIRD_PARTY_NOTICES.md`, or any license notices bundled into the app.** The release build must retain relevant notices, including the Primer Octicons MIT notice if the icon is shipped.

本文件是补充说明，不能代替原始源码中的版权标头、上游第三方声明或 App 包内需随附的许可证文件。每次更新依赖项或替换资源，都必须重新核对授权。

## Erosion-CN references in the **unreleased development patch** / 当前开发补丁中的 Erosion-CN 来源

The **current main branch development patch** (which is *not* identical to the already-published v1.0.7 release patch) documents work adapted from or informed by **[Kianuni/Erosion-CN](https://github.com/Kianuni/Erosion-CN)**, a GPL-3.0 derivative of **[jailbreakdotparty/Erosion](https://github.com/jailbreakdotparty/Erosion)**.

- `GestaltX/DevicePlistWriter.swift`: source comment says the in-place-write approach is adapted from Erosion-CN's `writeFileAtomically` concept.
- `GestaltX/AIReadinessCheckup.swift`: source comment credits Erosion-CN's Apple Intelligence checkup idea.
- `GestaltX/DeviceAIEligibility.swift`: device eligibility identifiers are transcribed and independently implemented from Erosion-CN's `isAppleIntellHD` list.
- `GestaltX/USRegulatoryModelMapping.swift`: regulatory model number mappings are transcribed and reimplemented with Erosion-CN as the recorded source.

**Author / Maintainer:** Kianuni and Erosion-CN contributors; upstream Erosion authors are credited separately.  
**License:** GPL-3.0. This is a source attribution, **not** a claim that all the above files have undergone a line-by-line copying/license audit or that these features are included in the original v1.0.7 IPA. The enhanced app must include this attribution in its in-app Credits/About page before a new release.

当前 `main` 的扩展补丁明确记录了以上借鉴或来源。原 Erosion、Erosion-CN 与 GestaltX 应分别保留贡献记录；**旧版发布附件并不自动具备当前开发补丁中的所有新增功能**。

Additional licenses already credited in the pinned upstream GestaltX app include **Gester (MIT)** and **ZIPFoundation (MIT)**, with their bundled license texts at `GestaltX/Licenses/Gester-MIT.txt` and `GestaltX/Licenses/ZIPFoundation-MIT.txt`. Preserve these as applicable.

## No endorsement / 非官方声明

No endorsement, sponsorship or affiliation by **huamidev**, upstream contributors, Apple Inc., or third-party projects is implied. The original name and credits are used to identify the upstream project; avoid representing this release as an official version.

如发现遗漏版权信息，请通过 GitHub Issue 报告并指明文件和来源，以便核实及更正。
