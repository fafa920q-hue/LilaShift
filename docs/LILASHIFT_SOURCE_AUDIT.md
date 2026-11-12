# LilaShift（紫序）源码审查报告 — 2026-11-13

> 状态：**静态审查 / 待编译及真机验证**。本报告审查了本仓库 main 的 `china-unlock-v107.patch`，以及 [huamidev/GestaltX v1.0.7](https://github.com/huamidev/GestaltX/tree/dfd4a7e3a8b8a89e76ac025a2a37242a7ed4c41f)、[Kianuni/Erosion-CN](https://github.com/Kianuni/Erosion-CN)、[Nugget](https://github.com/leminlimez/Nugget) 和 [MGKeys](https://github.com/PoomSmart/MGKeys) 的公开代码/许可证。未在本报告阶段构建 IPA、未在真实 iPhone 上写入系统文件，也未更改正式 Release。

## 一、基线、版本与两个开源来源

- 主工程：**GestaltX**，原作者 **huamidev**，版本 v1.0.7，固定提交 `dfd4a7e3a8b8a89e76ac025a2a37242a7ed4c41f`，许可证 **GPL-3.0**。
- 第二个重点来源：**Erosion-CN**，维护者 **Kianuni**，其上游为 **jailbreakdotparty/Erosion**，许可证 **GPL-3.0**。现有补丁在 `AIReadinessCheckup.swift`、`DevicePlistWriter.swift`、`DeviceAIEligibility.swift`、`USRegulatoryModelMapping.swift` 等位置明确注明借鉴 Erosion-CN 的设计、设备列表或映射。**这不等于对所有实现做过逐行独立性核验**。
- GestaltX 原版本身已经在 `AboutView.swift` 和 App 内 `Licenses/Erosion-GPL-3.0.txt` 给原版 **Erosion** 做许可证鸣谢。**原版 Erosion** 与 **Kianuni 的 Erosion-CN 衍生版** 应分别追溯，不可混淆来源。
- **MGKeys**：MIT，适合键名映射研究；若引入受保护的实质性代码/数据，应保留 MIT 版权和许可证文本。
- **Nugget**：AGPL-3.0；当前建议只学习交互、模块划分与测试策略，不直接复制 AGPL 代码到此 GPLv3 工程。任何实质性代码合并应先单独评估 GPLv3 §13 / AGPLv3 相关义务。
- LilaShift 增强版维护者为 **@steam8871**；不得把 huamidev、Kianuni 或其他贡献者的代码标为自己的原创。

**版本隔离重要事实：** 当前 `main` 分支的 `china-unlock-v107.patch` 已显著不同于旧版 `v1.0.7-china-unlock` 发布标签中的补丁（Git blob SHA 分别为 `ba46079a66d110bf1bf68ae708815928400eec25` 与 `9593bb9ea27083affc463efc09557c2a0c81ce8b`）。**不能声称现在 main 的新能力已经包含在旧版 IPA 中**。原有 v1.0.7 Release 与 IPA 不得改写为新的测试版。

## 二、现有实现（来自当前 main 补丁和固定上游源码）

| 需求 | 当前代码证据 | 初审判断 |
|---|---|---|
| 实时 MG 检测 | `GXLiveGestaltProbe.m`、`LiveGestaltProbe.swift` 使用只读 `MGCopyAnswer`，`AIReadinessCheckup.swift` 展示部分实时状态 | **部分已有**，尚缺通用三源对比列表与真机验证 |
| 安全写入、恢复 | `DevicePlistWriter.swift` 采用 `pwrite`、尾部截断、同步、读回、回滚；`GestaltDocument.swift` 原本有预备份与读回 | **部分已有**，需强化文件身份和故障注入测试 |
| 双重备份 | `GestaltDocument.swift` 补丁中增加系统库镜像和 SHA-256；`SystemVaultTests.swift` 有跨重装模拟 | **已有原型**，需解决脏基线/错误覆盖风险 |
| 智能兼容性 | `AIReadinessCheckup.swift`、`DeviceAIEligibility.swift`、`USRegulatoryModelMapping.swift` | **已有原型**，存在未验证的关键冲突 |
| 中文界面 | 固定上游已有 `Localizable.xcstrings` 和简中；当前补丁加强中文用途说明及浅紫玻璃 UI | **已有基础**，App 内显式三档热切换尚未在补丁确认 |
| 功能预设数据库 | `Capabilities.swift` 的静态枚举及 `MobileGestaltCacheLayout.swift` 动态槽位解析 | **已有代码式目录**，尚无版本化元数据/兼容性证据字段 |
| 壁纸与个性化 | 固定上游已有 `CustomizationStore.swift`、`CustomizationFiles.swift`、`LaunchArtworkStore.swift` 等 | **基础已有**，宜补 UI 整合和安全验证，不从零复制模块 |
| 电池与系统诊断 | Erosion-CN 有 `PowerTelemetryView.swift`、`CrashDiagnosticsView.swift`；未在当前 LilaShift 补丁发现同名实现 | **待开发**，先做只读权限检测 |
| 应用存档与缓存管理 | Erosion-CN 有 `AppDataBackupView.swift`、`CacheCleanerView.swift`；未在当前 LilaShift 补丁发现同名实现 | **待开发**，高风险写操作最后推进 |

## 三、必须优先处理的问题（按风险）

### P0-A：未决 AI 互斥项

当前 `AIReadinessCheckup.swift` 文件头明确标出 **UNRESOLVED CONFLICT (#178)**：Erosion-CN 的槽位观察与本版 9 项一键预设里 `CacheExtra audioIntelligence = 1` 之间，缺少真机因果证据。CacheExtra 与 CacheData 不是同一层。当前代码仅修复槽位、不改 9 项预设，不足以证明组合安全。

**要求：** 在每种实测机型上分别检查原厂、仅读取、暂存、写后、重启、照片功能，记录 OS build、机型、槽位布局和恢复结果。未验证组合不允许显示“完全兼容”，有合理风险的实验项默认不启用。

### P0-B：安全写入文件身份与断电风险

`DevicePlistWriter.openFile` 在带 `O_NOFOLLOW` 的打开失败后，会**无条件退化到不带此保护的打开方式**；原始文件通过路径读取，再打开 fd，存在文件被替换的时间窗口。必须先论证设备环境和 symlink 信任边界，然后增加 `fstat`、路径 `stat` 与文件类型、inode/设备号/权限的校验和合理失败处理。不能把“使用 pwrite”宣传为对断电绝对原子。

**要求：** 提供可注入 `open/pwrite/ftruncate/fsync/pread` 故障的离线测试；覆盖部分写入、短写、EINTR、同步失败、校验失败、回滚失败；并对目标文件权限和路径预期进行检查。失败时默认只允许保留备份并停止写入。

### P0-C：首次备份与“原厂”含义

`SystemVaultTests.swift` 测试损坏摘要或 UUID 不匹配时，应用用**当前正在读取的系统缓存**重建库。若当前缓存早已被其他工具修改，不能把重建结果宣传为“原厂备份”。SHA-256 只提供一致性，不证明备份未经第三方修改；目前没有独立的可信出厂数据。

**要求：** 将状态明确分为 `factory-verified`（有可信证据时）、`first-observed`、`recovered`、`unknown`；对脏基线只标记首次观察快照，拒绝自动覆盖经有效校验的早期备份，未经原厂证明禁止使用“恢复出厂设置”的文案。恢复前强制匹配设备/系统 CacheUUID、CacheVersion、长度及稳定设备身份，支持外部离线导出。

### P0-D：机型兼容表过宽

`DeviceAIEligibility.isNativeAppleIntelligence` 通过 `productType.hasPrefix("iPhone19,")` 将该系列所有未知子型号视为原生 AI 设备，**不符合源码注释所述的未知机型 fail-closed**。应改用精确经核验列表，未知机型展示“不确定”而非“支持”，绝不据此放开高风险写入。

### P0-E：GPL 与上游署名

现有补丁对 Erosion-CN 的来源说明主要在注释里（如 `DevicePlistWriter.swift`），当前 About/Credits 明示的是 **Erosion 上游**。需要在仓库和 App 内分别标注 **Kianuni/Erosion-CN** 的贡献/借鉴范围，并核对实际引用和改写文件，保留原版权标头及 GPL。**README 的简单“灵感借鉴”不能替代已复制代码的版权声明**。升级 `THIRD_PARTY_NOTICES.md`。

## 四、非 P0 风险但需要管理

1. `VersionSupport.swift` 以 27.x 判断，不能代替细粒度机型、系统 build 与授权能力的检查；不同子功能需独立功能矩阵。
2. 实时 `MGCopyAnswer` 返回值不等于服务器服务已启用；用三态 `supported / unsupported / unknown`，不要用虚假的绿色“成功”。
3. App Group 重签/分享扩展要真实授权；不得把未验证容器权限称为必然成功。
4. 电池数据库、Crash/Jetsam、应用容器可能包含敏感数据：默认本地、只读、最小化收集；导出时先脱敏。
5. 用户的正式 Release 当前仍是 GestaltX v1.0.7 China Unlock。改名和新版本必须新建 tag / IPA / 对应源码档案，不覆盖旧包。

## 五、审查完成程度与限制

- **已完成：** 公开源码/许可证核对、原版核心架构抽查、当前补丁的文件清单、关键风险代码静态阅读。
- **尚未完成：** 完整 3MB+ 补丁所有更改逐行审查、Swift 编译、CI 执行结果、IPA 二进制溯源、签名与 App Group 实测、真机写入/恢复及断电测试。
- 任何“完全防白苹果”“100% 兼容”“真正原厂恢复”等绝对性宣传都必须暂停，直到有匹配的验证证据。

后续实施以 [实施路线图](LILASHIFT_IMPLEMENTATION_PLAN.md) 和 [双上游来源清单](LILASHIFT_PROVENANCE.md) 为准。