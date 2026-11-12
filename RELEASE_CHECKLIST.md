# Release checklist / 发布前检查表

For maintainers publishing an **unofficial GestaltX derivative**. This is a practical checklist, **not legal advice** or confirmation that a particular binary complies with law or platform rules.

## License and source / 许可证与源码

- [ ] Confirm the exact upstream commit and license; keep original author, contributor and file-level copyright notices.
- [ ] Preserve upstream `THIRD_PARTY_NOTICES.md`, all bundled third-party license texts, and your supplementary [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
- [ ] Mark modified files and describe changes and dates where applicable; **@steam8871 is the enhancement maintainer, not the sole upstream author**.
- [ ] Confirm the complete modified source matches the **actual release IPA**, including all scripts, patches, resources, and build instructions needed for the covered work.
- [ ] Provide source under GPL v3 via an appropriate GPL v3 section 6 distribution method; ideally attach a complete assembled-source archive to the same Release.
- [ ] Never silently relicense GPL-covered upstream work to a proprietary/noncommercial-only license or remove downstream GPL freedoms.
- [ ] Verify license compatibility before adding copied code, icons, fonts or other third-party assets.

## Build and integrity / 构建与校验

- [ ] Build from a pinned full Git SHA (not an unpinned moving branch or mutable tag assumption).
- [ ] Require `git apply --check`; run tests; record Xcode version, SDK, job link, exact inputs and build result.
- [ ] Check the packaged IPA includes the expected app/extension and notices; test App Group entitlements in the actual installation/signing route.
- [ ] Compute SHA-256 for each IPA and source archive; publish filenames and hashes.
- [ ] If source-to-IPA reproducibility or binary provenance was not independently verified, **do not claim** the published IPA is proven reproducible or safe.
- [ ] Retain the source inputs for every previous release.

## Public release page / 发布页面

- [ ] Use a distinct version name such as **GestaltX v1.0.7 China Unlock (unofficial)**; never label it an official release.
- [ ] Give clear upstream credit and link to the tagged original source, your patch, your matching source distribution and GPL v3 license.
- [ ] List only verified features and compatibility; do not claim iOS 26 full device access when on-device MobileGestalt is reported to require iOS 27.
- [ ] State that feature flags cannot add absent hardware, guarantee Apple Intelligence, or override carrier, region or Apple service restrictions.
- [ ] State device instability/restore risk and recommend an independent backup before changes.
- [ ] Do not provide instructions for using misrepresentation to obtain prohibited services or to bypass carrier/local legal requirements.
- [ ] Avoid implying approval by huamidev, Apple, GitHub or credited projects.
- [ ] Review [GitHub Acceptable Use Policies](https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies) and applicable law; GPL permission does not guarantee a release is allowed under other rules.

## Suggested release title / 推荐标题

`GestaltX v1.0.7 China Unlock — Unofficial GPLv3 Build / 非官方增强版`

## Suggested short disclaimer / 推荐简短声明

> **Unofficial modified build / 非官方修改版。** Based on huamidev/GestaltX v1.0.7 (GPL v3). Enhancements maintained by @steam8871. Not endorsed by huamidev, Apple or GitHub. Source: pinned upstream commit plus published patch; see SOURCE_AND_BUILD.md. Modifying device configuration may cause instability or require restore. No feature, carrier access or regional availability is guaranteed. Follow applicable law and service rules.
