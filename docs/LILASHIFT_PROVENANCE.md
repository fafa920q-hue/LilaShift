# LilaShift 双上游与第三方来源清单

本文件把“主要源代码来源”和“研究参考”明确分开。**两个重点源项目**分别为 **GestaltX**（当前应用主架构）与 **Erosion-CN**（当前补丁的若干安全、AI 和设备型号设计来源）。GestaltX 自身还包含原版 Erosion 等第三方署名，不应把 Erosion、Erosion-CN 当成同一个作者或同一个仓库。

| 来源 | 地址 / 许可 | 当前用途与证据 | 原作者/保留声明 |
|---|---|---|---|
| **GestaltX (primary)** | [huamidev/GestaltX](https://github.com/huamidev/GestaltX/tree/v1.0.7) · GPL-3.0 | 主 SwiftUI App、MobileGestalt 文件模型、备份/恢复与分享扩展，固定 SHA `dfd4a7e3a8b8a89e76ac025a2a37242a7ed4c41f` | **huamidev** 与已有贡献者；保留源文件 SPDX/版权标头及 GPL |
| **Erosion-CN (second studied source)** | [Kianuni/Erosion-CN](https://github.com/Kianuni/Erosion-CN) · GPL-3.0 | 当前 LilaShift 补丁已有 Erosion-CN 相关注释：`DevicePlistWriter.swift` 借鉴原位写入设计；`AIReadinessCheckup.swift` 借鉴体检卡思路；`DeviceAIEligibility.swift` 和 `USRegulatoryModelMapping.swift` 据其列表/映射重实现 | **Kianuni**、其上游和相应贡献者；标注具体来源和许可。逐行代码相似性尚待复核，不可声称绝对独立原创 |
| **Erosion upstream (already credited by GestaltX)** | [jailbreakdotparty/Erosion](https://github.com/jailbreakdotparty/Erosion) · GPL-3.0 | 固定上游 GestaltX v1.0.7 `AboutView.swift` 中已有单独的 Erosion 引用及 `GestaltX/Licenses/Erosion-GPL-3.0.txt` | **lunginspector**、**jailbreak.party** 及贡献者；保持原上游声明 |
| **worse_query** | [forcequitOS/worse_query](https://github.com/forcequitOS/worse_query) · upstream notes GPL-3.0-or-later | 由 GestaltX 主源包含 `worse_query.m/.h` | **Taj C / forcequitOS**；继承并保留头文件原始声明 |
| **MGKeys** | [PoomSmart/MGKeys](https://github.com/PoomSmart/MGKeys) · MIT | 键名/映射参考；此阶段不把整个数据集复制到仓库 | **PoomSmart**；实际复制实质性内容时，包含 MIT 版权和许可文本 |
| **Nugget** | [leminlimez/Nugget](https://github.com/leminlimez/Nugget) · AGPL-3.0 | 仅作为产品设计、分类、可用性和安全门禁参考；当前无新增 Nugget 源码拷贝计划 | **leminlimez** 与贡献者；若复用 AGPL 代码，需另外确认 AGPL/GPL 组合义务 |
| **Gester** | [sasobhabha/Gester](https://github.com/sasobhabha/Gester) · MIT（GestaltX app credits） | 固定上游已内置 `GestaltX/Licenses/Gester-MIT.txt` | 保留上游署名及 MIT notice |
| **ZIPFoundation** | [weichsel/ZIPFoundation](https://github.com/weichsel/ZIPFoundation) · MIT（GestaltX app credits） | 固定上游已内置 `GestaltX/Licenses/ZIPFoundation-MIT.txt` | 保留上游署名及 MIT notice |
| **Primer Octicons** | [primer/octicons](https://github.com/primer/octicons) · MIT | GitHub 标识图标，固定上游附有 `Primer-Octicons-MIT.txt` | 保留 MIT notice，不暗示 GitHub 官方认可 |

## 当前代码中可定位的 Erosion-CN 参考

- `GestaltX/DevicePlistWriter.swift`：首部注释标示适配自 Erosion-CN 原位写入思路 `writeFileAtomically`。
- `GestaltX/AIReadinessCheckup.swift`：首部说明借鉴 AppleIntelligenceCheckupCard 的四项诊断理念，且明确指出 #178 有未决问题。
- `GestaltX/DeviceAIEligibility.swift`：注释注明机型列表来自 Erosion-CN 的 `isAppleIntellHD`。
- `GestaltX/USRegulatoryModelMapping.swift`：注释注明型号映射据 Erosion-CN 的 `usRegulatoryModelNumber`。
- 这些文件是本仓库 `china-unlock-v107.patch` 所记录的**修改后源码路径**，不是构建仓库根目录里的实际 Swift 文件。构建需先取固定的 GestaltX 源码，再应用此补丁。

## 版本识别与下一步

旧版 Release `v1.0.7-china-unlock` 的补丁 Git blob：`9593bb9ea27083affc463efc09557c2a0c81ce8b`；当前 `main` 补丁 Git blob：`ba46079a66d110bf1bf68ae708815928400eec25`。只有后者包含本审查提到的多项新版诊断和写入改进。**不得把后者的功能描述加到未重新构建、未测试的旧 IPA 中。**

下一步需要按文件逐项比对当前修改版与相应 Erosion-CN 源码，决定哪些是**复制、改写、纯事实性映射、独立重新实现、仅有灵感**，分别完善 SPDX/版权声明；同时在 **LilaShift About/Credits** 中单独加入 Kianuni/Erosion-CN，确保最终新 IPA 中也可查看。详细门禁见 [源码审查报告](LILASHIFT_SOURCE_AUDIT.md)。
