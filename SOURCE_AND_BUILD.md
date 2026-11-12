# Corresponding source & build provenance / 对应源码和构建说明

## Exact version inputs / 当前版本输入

- Upstream: https://github.com/huamidev/GestaltX
- Upstream v1.0.7 commit: `dfd4a7e3a8b8a89e76ac025a2a37242a7ed4c41f`
- Modified version patch: [china-unlock-v107.patch](china-unlock-v107.patch)
- Build instructions: [.github/workflows/build-ipa.yml](.github/workflows/build-ipa.yml)
- Upstream build script: `.github/scripts/build-ipa.sh` from the pinned upstream commit
- License: [GNU GPL v3](LICENSE)
- Upstream third-party notices: https://github.com/huamidev/GestaltX/blob/v1.0.7/THIRD_PARTY_NOTICES.md
- Additional notices: [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)

**Do not confuse the automatic GitHub release source archives with a fully assembled source tree.** Those archives contain this build repository and its patch, but not an expanded copy of the upstream tree. For the combination, fetch the exact pinned upstream commit and apply the published patch.

## Reconstruct the modified source tree / 还原修改版源码

Run on macOS with Git, Python 3 and a compatible Xcode toolchain:

```bash
git clone https://github.com/fafa920q-hue/gestaltx-china-unlock-build.git build-inputs
cd build-inputs
git checkout v1.0.7-china-unlock

git clone https://github.com/huamidev/GestaltX.git upstream
git -C upstream checkout --detach dfd4a7e3a8b8a89e76ac025a2a37242a7ed4c41f
git -C upstream apply --check ../china-unlock-v107.patch
git -C upstream apply ../china-unlock-v107.patch

cd upstream
python3 -X utf8 scripts/generate_localization.py
python3 -X utf8 tests/LocalizationTests.py
```

To build an IPA, use the steps in `.github/workflows/build-ipa.yml` and the pinned upstream build script. The exact toolchain, SDK, signing settings and provisioning affect the resulting IPA and installability.

在 macOS 上用适当版本的 Xcode，依照仓库的构建工作流运行上游打包脚本。IPA 是否能在特定安装环境中使用，还取决于签名、App Group、容器和系统版本。

## Binary verification / 二进制核对

The release page states a SHA-256 checksum for its attached IPA. Download the official asset **from this repository's Release page**, then independently verify:

```bash
shasum -a 256 GestaltX_1.0.7_ChinaUnlock.ipa
```

For **v1.0.7-china-unlock**, the checksum published by GitHub for the current asset is:

```text
8906197a6901680fc9bf06e014f086e27071165c03463a0a76756647edb4a60f
```

This checksum authenticates the bytes of **that published asset when compared against a trusted release checksum**. It does not independently prove the asset was built from the disclosed patch. A byte-for-byte reproducible build or attested provenance has **not** been verified by this document.

## GPL v3 distribution reminders / GPL v3 分发说明

When distributing an IPA, provide recipients access to the **complete corresponding source**, not only a README or an unrelated upstream link. GPL v3 section 6 specifies ways of accompanying non-source forms with corresponding source. Preserve copyright and license notices, prominently mark modifications, and do not impose additional license restrictions on GPL-covered work. Keep the exact upstream commit and complete matching patch available for every **published** IPA, including older releases. Consider publishing a conveniently downloadable assembled source archive alongside each IPA.

分发 IPA 时，应同时确保接收者能够获得该二进制实际对应的完整源码、修改和构建所需脚本，并保留原版权声明。建议在每个 Release 中上传与 IPA 匹配的完整修改源码压缩包，不能仅依赖以后会变化的 `main` 分支。

If the release asset was assembled from uncommitted changes, extra generated files, proprietary dependencies, or another build configuration, this repository's patch and instructions may **not** be sufficient; verify against the actual IPA and correct the source distribution before representing it as complete.
