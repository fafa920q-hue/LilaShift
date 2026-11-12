# GestaltX 1.0.7 — China Unlock Build

> One-tap eSIM, region code and Apple Intelligence setup for China-model iPhones — built from upstream GestaltX v1.0.7.
>
> 国行 iPhone 一键解锁：eSIM、地区码、Apple Intelligence，一次点按完成。基于官方 GestaltX v1.0.7 构建。

English | [简体中文](#这是什么仓库)

## What this repository is

This is the **build repository** for the China Unlock enhanced version of GestaltX. It does not fork the upstream source. Every CI run checks out upstream [huamidev/GestaltX](https://github.com/huamidev/GestaltX) at the pinned commit `dfd4a7e` (tag `v1.0.7`, build `11130112`), applies `china-unlock-v107.patch`, and builds the IPA. The complete modified source is therefore always reproducible from this repository: pristine upstream v1.0.7 + the patch in this repo.

## What's new in this build

- **One-tap China Unlock (9 items).** eSIM switches (green-tea off, not-green-tea on), region code set to US (`LL`, sales region untouched), and six Apple Intelligence capabilities enabled — all staged in one tap, then reviewed and applied.
  - The eSIM cache layout is verified before staging. If it cannot be verified, the whole eSIM group stops and shows the reason; region and AI can still be set individually.
  - Every apply is automatically backed up and read-back verified. One-tap restore reverts all 9 items from the recorded originals.
- **Light-lavender Liquid Glass redesign.** Page background `#F6F3FF`, primary purple `#8652DC`. No large dark backgrounds.
- **One-line purpose description under every feature.** All 33 presets show a Simplified Chinese purpose line under the feature name; device requirements and how the change takes effect live in the details.
- **Author badge and progress cards.** Maintainer `@steam8871` is credited in the header and the About page. Reading and applying show real progress (backup / write / verify / done) driven by the actual operation — never faked.
- **Open-source compliance.** The About page carries an "Open Source & Acknowledgements" section, the full GPL v3.0 text is bundled in the app, and the enhanced source repository (this repo) is linked in the app.

## Download

Built IPAs are published as GitHub Actions artifacts (14-day retention) on the [Actions tab](https://github.com/fafa920q-hue/gestaltx-china-unlock-build/actions). Download the `GestaltX_1.0.7_ChinaUnlock` artifact for the latest successful `Build GestaltX China Unlock` run.

- Bundle ID: `com.huami.gestultx`
- Version: `1.0.7` (build `11130112`), minimum iOS `26.0`
- Size: ~3.6 MB

## Install

1. Install the IPA with [LiveContainer](https://github.com/khanhduytran0/LiveContainer) — it runs the original IPA without re-signing, so the App Group requirement is met without a paid developer account.
2. Open GestaltX and tap **Read Device** first.
3. Open **China Unlock**, review the 9 staged items, then apply.
4. **Restart the device** after applying, then check eSIM and Apple Intelligence in system Settings.
5. To undo everything, use the one-tap restore — it reverts all 9 items from the backup.

## Requirements and caveats

- **eSIM hardware is required.** The unlock only flips the capability flags; it does not add eSIM hardware to a device that has none.
- **Apple Intelligence depends on hardware and Apple's servers.** Turning the flags on does not guarantee the features appear or work.
- **Carrier and location rules still apply.** A foreign eSIM cannot be installed while inside mainland China (Apple rule); installing one abroad generally needs Location Services on. A Chinese carrier eSIM must be activated at a carrier store in China.
- **System updates may revert the changes.** Re-apply after updating iOS if needed.
- **Do not update iOS blindly.** GestaltX relies on an unpatched iOS sandbox-escape vulnerability (`worse_query`). Apple may close it in a future update; confirm compatibility before updating if you rely on this tool.
- **Back up before applying.** The app backs up automatically, but a separate device backup is still good practice.

## Build it yourself

Both workflows are manual-only (`workflow_dispatch`):

- **Build GestaltX China Unlock** (`.github/workflows/build-ipa.yml`) — builds and uploads the IPA.
- **Screenshot GestaltX China Unlock** (`.github/workflows/screenshots.yml`) — builds for the iOS Simulator (iPhone 17) and captures the Tools home, a preset page, and the Confirm Changes page.

The screenshots come from a simulator with no real device document, so they show the "Not read yet" state and a 1-item review — not the 9-item China Unlock summary, which needs a real device.

## Open source and license

This project is distributed under the **GNU General Public License v3.0**. See [LICENSE](LICENSE) (byte-identical to upstream v1.0.7).

- Upstream project: [huamidev/GestaltX](https://github.com/huamidev/GestaltX) (`v1.0.7`, commit `dfd4a7e`)
- Enhanced version maintainer: `@steam8871`
- Modifications in this build: the 9-item China Unlock preset and its safety checks, the light-lavender Liquid Glass redesign, one-line purpose descriptions, the author badge and progress cards, the in-app source-repository link, and the open-source compliance section.
- The complete corresponding source is the pristine upstream v1.0.7 source plus `china-unlock-v107.patch` in this repository.

## Credits

- **huamidev** — GestaltX.
- **forcequitOS** — [`worse_query`](https://github.com/forcequitOS/worse_query), the sandbox escape that makes on-device MobileGestalt editing possible.
- **PoomSmart (MGKeys), leminlimez (Nugget), and the other projects listed in the app's Credits & Licenses page.**

## Disclaimer

This is an unofficial modified build, not affiliated with Apple or endorsed by the upstream author. Use it at your own risk. Capability flags do not guarantee features, and modifying system settings can cause instability — read the on-screen warnings before applying anything.

---

## 这是什么仓库

这是 GestaltX 国行增强版的**构建仓库**，不 fork 上游源码。每次 CI 都会 checkout 上游 [huamidev/GestaltX](https://github.com/huamidev/GestaltX) 的固定提交 `dfd4a7e`（标签 `v1.0.7`，build `11130112`），应用 `china-unlock-v107.patch`，再构建 IPA。因此完整修改源码永远可以从本仓库复现：官方 v1.0.7 原始源码 + 本仓库的补丁。

## 本版新增内容

- **一键解锁（9 项）。** eSIM 两项开关（green-tea 关、not-green-tea 开）、地区码改美国（`LL`，销售地区不变）、6 项 Apple Intelligence 能力——一次点按全部暂存，确认后应用。
  - 暂存前会先校验 eSIM 缓存布局；验不过整组停住并显示原因，地区码和 AI 仍可单独设置。
  - 每次应用都会自动备份并写回校验；一键还原可从记录的原始值恢复全部 9 项。
- **浅紫 Liquid Glass 全新视觉。** 页面背景 `#F6F3FF`，主紫 `#8652DC`，无大面积深色背景。
- **每个功能名下都有一句简体中文用途说明。** 33 个预设全覆盖；设备要求与生效方式放在详情里。
- **作者徽章与进度卡。** 维护者 `@steam8871` 显示在首页与关于页；读取与应用进度（备份 / 写入 / 校验 / 完成）由真实操作驱动，绝不伪造。
- **开源合规。** 关于页有「开源与鸣谢」，App 内置 GPL v3.0 全文，并链接了本增强版源码仓库。

## 下载

构建好的 IPA 发布在 [Actions](https://github.com/fafa920q-hue/gestaltx-china-unlock-build/actions) 的 Artifacts 里（保留 14 天），找最新一次成功的 `Build GestaltX China Unlock`，下载 `GestaltX_1.0.7_ChinaUnlock`。

- 包名：`com.huami.gestultx`
- 版本：`1.0.7`（build `11130112`），最低 iOS `26.0`
- 大小：约 3.6 MB

## 安装

1. 用 [LiveContainer](https://github.com/khanhduytran0/LiveContainer) 安装 IPA——直接运行原始 IPA，无需重签，即可满足 App Group 要求，不需要付费开发者账号。
2. 打开 GestaltX，先点 **Read Device** 读取本机数据。
3. 打开 **China Unlock**，确认 9 项内容后应用。
4. 应用后**重新启动设备**，再去系统「设置」里检查 eSIM 与 Apple Intelligence。
5. 想全部撤销时用一键还原，会从备份恢复全部 9 项。

## 要求与注意事项

- **需要 eSIM 硬件。** 解锁只改能力开关，不能给没有 eSIM 硬件的设备加上 eSIM。
- **Apple Intelligence 取决于硬件与苹果服务器。** 打开开关不保证功能一定出现或可用。
- **运营商与位置规则仍然适用。** 在中国大陆境内无法安装境外 eSIM（苹果规则）；在境外安装通常需要打开定位服务；中国运营商 eSIM 须在中国营业厅激活。
- **系统更新可能还原改动。** 升级 iOS 后如有需要请重新应用。
- **不要盲目升级 iOS。** GestaltX 依赖一个未修复的 iOS 沙盒逃逸漏洞（`worse_query`）。苹果可能在未来版本中修掉它；如果你依赖这个工具，升级前请先确认兼容性。
- **应用前请备份。** App 会自动备份，但另外做一份设备备份仍是好习惯。

## 自己构建

两个工作流均为手动触发（`workflow_dispatch`）：

- **Build GestaltX China Unlock**（`.github/workflows/build-ipa.yml`）——构建并上传 IPA。
- **Screenshot GestaltX China Unlock**（`.github/workflows/screenshots.yml`）——在 iOS 模拟器（iPhone 17）上构建，截取工具首页、单项预设页、更改确认页三张图。

截图来自没有真实设备文件的模拟器，因此显示「Not read yet」状态，确认页为 1 项预览——不是 9 项解锁摘要，9 项摘要需要真机读取。

## 开源与许可证

本项目遵循 **GNU 通用公共许可证 v3.0** 发布，见 [LICENSE](LICENSE)（与官方 v1.0.7 逐字节相同）。

- 上游项目：[huamidev/GestaltX](https://github.com/huamidev/GestaltX)（`v1.0.7`，提交 `dfd4a7e`）
- 国行增强版维护者：`@steam8871`
- 本版修改内容：9 项一键解锁预设及安全检查、浅紫 Liquid Glass 界面、每项功能一句话用途说明、作者徽章与进度卡、App 内源码仓库链接、开源合规栏目。
- 完整对应源码 = 官方 v1.0.7 原始源码 + 本仓库的 `china-unlock-v107.patch`。

## 鸣谢

- **huamidev**——GestaltX。
- **forcequitOS**——[`worse_query`](https://github.com/forcequitOS/worse_query)，让设备端修改 MobileGestalt 成为可能的沙盒逃逸。
- **PoomSmart（MGKeys）、leminlimez（Nugget）** 以及 App 内「Credits & Licenses」页列出的其他项目。

## 免责声明

这是非官方修改版，与苹果公司及上游作者无关，也不代表其立场。使用风险自负。能力开关不保证功能可用，修改系统设置可能导致不稳定——应用前请阅读屏幕上的提示。
