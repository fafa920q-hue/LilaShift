# LilaShift 自签安装与授权检测规格（设计稿）
> 此文档尚未实现 Apple ID 登录、证书签名与 iOS 安装。仅规定用户体验、安全边界、诊断器验收要求。

## 初次安装引导
1. 用户访问 GitHub Releases，先核验 IPA SHA-256 与完整对应源码。
2. 在“我有免费 Apple ID / 我有开发者证书 / 我已安装 SideStore 或 LiveContainer”中选路径。
3. 免费 Apple ID → Windows/macOS 本地助手签名、连接设备、双重认证和首次安装；提醒 7 天续签、个人团队 app/设备/App ID 限额，且某些受限 Entitlements 不能由免费签名获取。**不得向紫序平台网站输入 Apple ID 密码或验证码。**
4. P12 → 由现有可信安装工具或未来本地签名模块持证签名；仅导入本地，密码驻留内存、不入日志和云端；设备必须受 profile 授权。
5. 安装后运行“签名健康”：显示主 App 与 Share Extension 是否同一团队、是否共享至少一个有效 App Group、签名有效期、安装方式、扩展是否可用。没有所需授权时，功能降级并给修复建议。

## 签名校验三层
- **IPA 静态扫描**：Info.plist、主 App/扩展标识、描述文件元数据、授权组相交情况、过期时间。源码里加入无凭据静态检查 CLI；不能把静态扫描称为密码学签名验证。
- **签名后的电脑验证**：使用苹果 `codesign` 等可信签名工具校验实际签名和 Entitlements；核对描述文件授权范围。Windows 按相应受信任工具校验；不提供未经过验证的“签名完成”。
- **iPhone 运行时检查**：App Group 容器是否真实可访问，分享扩展导入是否真能传递数据，重装后数据与备份恢复是否正常。

## 敏感数据保护
默认不联网、不上传证书/私钥/Apple ID/2FA、无账号密码日志、无在线转签网站。证书导入使用设备安全存储及明确删除入口；严防 P12 被备份或上传；不将账号信息收集到匿名诊断包。签名前不自动改变 Bundle ID/Entitlements；变更需要详细预览。
若未来集成第三方本地签名引擎，逐文件确认许可证、维护状态和是否存在遥测或私钥外传，默认在隔离模块中实现。

## UX 显示词语
- “可安装”只有在实际安装成功并能打开时显示；签名结构合理仅显示“静态检查通过”。
- “App Group 已授权”需要运行时与签名共同确认。主 App 存在组字段不代表扩展具备授权。
- “可以使用 Apple ID 自签”不代表“能在未安装 App 前从 App 内直接生成免费签名”，也不意味着永久免费免续签。
- 免费账号不能获得的 Entitlements 将被明确标记“当前签名方式不支持”；不承诺绕过苹果限制。

## 测试矩阵
缺失扩展、嵌套 Bundle ID 变化、无 profile、过期 profile、主与扩展不同团队、App Group 不相交、签名组超出 profile、未签名/adhoc、正常有证书+profile、免费 Personal Team、LiveContainer 宿主/子应用隔离、7 日过期、重签后原有数据兼容、证书撤销。
静态诊断器至少覆盖前 7 项；余项必须在设备或有签名工具的环境测试。应提供 `unknown` 状态，不能把缺少证据定为成功。

## 参考
- Apple Personal Team: https://developer.apple.com/help/account/basics/about-your-developer-account
- GestaltX App Group: https://github.com/huamidev/GestaltX
- Feather: https://github.com/claration/feather （GPL-3.0；先审核再引用代码）
- LiveContainer 官方: https://livecontainer.github.io/docs/installation
- SignTools: https://github.com/SignTools/SignTools （AGPL-3.0，仅参考设计）
