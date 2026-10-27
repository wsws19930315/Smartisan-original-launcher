# 版权、来源与授权边界

本说明用于区分权利范围，不是整个仓库的统一许可证，不替代文件自身的有效许可。

## 原创贡献与授权状态

维护者及其他贡献者独立创作的代码、文档、脚本等，其权利归相应合法权利人。提交账号、文件存放位置、移植或重新签名行为本身不能证明对文件全部内容拥有版权。

本项目尚未发布覆盖整个仓库的统一许可证。[原创部分非商业许可草案](docs/legal/ORIGINAL_NONCOMMERCIAL_LICENSE_DRAFT.md)仅供确认，当前不授予新权利。须先确认权利人、授权范围和生效版本，再由有权授权者发布；未列入有效授权范围的内容不因草案存在而获得许可。依法无需许可的使用、平台条款授予的权利及既有有效许可不受影响。

## 第三方内容

| 内容与位置 | 来源及现有依据 | 使用边界 |
| --- | --- | --- |
| `launcher/smali/com/smartisanos/`、`launcher/smali/smartisanos/`、`launcher/res/`、原版纹理与主题、`clean_launcher/` 等 | 原版 Smartisan Launcher 及相关应用的反编译、恢复或衍生内容；参见 [APK 结构](docs/architecture/APK_STRUCTURE.md) | 原代码、图片、动画、主题、商标等仍归原权利人。本次未找到覆盖移植、公开再分发和商用的完整授权链，非商业研究说明不能代替授权 |
| `launcher/lib/*/liblauncher_opt.so` 及混合 APK | 原应用二进制与重打包产物 | 本项目不为其中原版及第三方部分再授权；不同架构副本不代表不同权利来源 |
| maintained 风格设置资源、组件与参考实现 | 本地参考项目 [smartisan-launcher-maintained](https://github.com/rianlu/smartisan-launcher-maintained)；其 `NOTICE.md` 声明非官方维护，未对整体授予通用开源许可 | 参考、复制、派生须分别核实；不能仅因源码公开而将其归为本项目原创或默认允许商业使用 |
| `launcher/tools/java/com/smartisanos/launcher/theme/IconProjectionBlur.java` | 文件头标明 Android 10 Skia 衍生及 Google / AOSP 版权 | 保留既有代码头和 [Skia 许可全文](launcher/assets/third_party/Skia-LICENSE.txt)，其许可权利不受本项目非商业草案限制 |
| `launcher/smali/android/support/`、`android/arch/`、`androidx/versionedparcelable/`、`com/android/` | Android / AOSP 组件线索；尚未完成各打包版本与上游文件的一一映射 | 按各自实际许可处理；不能将整个 Android 来源内容统一判为同一许可证。须补齐版本、源文件、适用许可证与必要声明 |
| `launcher/smali/aurelienribon/tweenengine/` | Universal Tween Engine 包名与 `BaseTween.java` 等源文件名线索；当前上游有 Apache-2.0 许可 | 当前上游不等于本包历史版本已核实；须完成版本匹配和声明补全，不能改套本项目非商业条款 |
| `tools/apktool.jar` | 构建工具内含 `LICENSE`、`META-INF/LICENSE`、`META-INF/LICENSE.txt`、`META-INF/NOTICE.txt`，涉及 smali/baksmali、Apache 许可和 Commons CLI 声明 | 内嵌许可原样保留；不因随本仓库分发而改用本项目草案，也不能据此把 Launcher 本体标成 Apache-2.0 |
| `icons/drawable/` 及来自下载镜像的图标和元数据 | [下载镜像仓库](https://gitee.com/RANH-F/Smartisan-original-launcher-download)已有 MulanPSL-2.0；本次比对 5,199 张图标字节一致 | 已有效授予的木兰许可不得以搬到主项目为由撤销。逐项素材的作者、来源和授权能力仍须核实；公共仓库与包名不是素材授权证据 |

上述是已识别来源，不是完整、已验收的第三方软件物料清单。未列出的第三方代码与素材同样不归本项目自动所有，也不自动适用新草案。

## 图标、字体、壁纸与其他素材

原版图标、应用商标、壁纸、预览图、截图、主题等可能有不同权利人；修改、裁切、改名或生成索引不会自动消除原作权利。现有图标名称及分类证据仅用于识别应用，不证明图案本身的许可。

本次检查的本地工作树（排除 `.git/`、`build/`、`.idea/`）未发现独立 TTF / OTF / WOFF 文件；这不是对 APK、系统字体或嵌入素材的全量权利保证。后续引入字体、CraftEcho Icons 或其他资源包，须核实具体版本、逐项授权、商业使用、修改和再分发条件，保存适用许可与出处。来源不明项先标记待核实，不擅自补填“原创”“可商用”或“禁止商用”。

## 保留已有权利与声明

本说明及 README 不追溯撤销 MulanPSL-2.0、BSD、Apache 等已经合法授予的权利，不对这些部分追加非商业、强制项目链接、强制公开源码等原许可没有的条件。若有效许可要求保留版权、许可证、NOTICE 或修改声明，应按该许可执行。

无有效授权的原版内容，不因“仅供学习”“免费”“非商业”或免责声明而获得使用、修改、分发许可。对完整 APK 的使用和分发须分别核对其中各组成部分，维护者对原创增量的授权不能代替其他权利人的授权。

## 非官方关系、联系与责任

本项目为非官方兼容移植，不代表 Smartisan、锤子科技或其他权利人，不主张官方授权、合作或背书。不得冒充原作者、官方版本或虚构授权关系；既有开源许可也不当然授予相关商标使用权。

对维护者有权授权的内容，如需超出现有许可范围，或希望报告来源、版权问题，可通过 [主项目 Issues](https://github.com/RANH-F/Smartisan-original-launcher/issues)联系维护者协调。该渠道不代表维护者能代其他权利人授权；已有许可允许的用途无需重复申请。

软件可能存在兼容、稳定性、数据丢失等风险。除适用法律另有要求或另有书面约定外，不对适用性、持续维护和无侵权作保证；本说明不排除或限制适用法律规定不能排除或限制的责任，也不变更第三方既有许可的责任条款。

审计依据与未决事项见 [授权审计报告](docs/legal/LICENSING_AUDIT_20261024.md)。
