# Android 17 启动、状态栏与图标加载审计

本报告合并记录状态栏重复重载修复，以及默认图标与启动任务排序的验证。各阶段的设备、APK 和结论以对应小节为准。

## 状态栏重复重载修复

## 现场根因

Android17/API37、1440×3120、density420 的独立模拟器中，同一刘海 `cutoutBottom=145`，状态栏 Insets 在63和145间变化。原 `StatusBarHeightCompat.calculate()` 的上限为 `max(safeFloor, system+maxExtra)`。system=63时把刘海安全高度加5px间距的150截到145；system=145时又得到150，启动值与实时值轮流不一致。

日志确认两次自动 `STATUS_BAR_COMPAT_CHANGE` 重载：

| 设备启动后时间(ms) | 事件 |
|---|---|
| 43632 | PID1825请求第一次状态栏兼容冷重载 |
| 48715 | 过渡进程请求结束旧PID1825 |
| 57649 | 第一次重载记录超时 |
| 81524 | PID2304请求第二次状态栏兼容冷重载 |
| 82751 | 过渡进程请求结束旧PID2304 |
| 89809 | 新PID3130报告GL首帧就绪 |
| 110826 | 新PID3130报告桌面数据/页面就绪 |

这不是一次固定很长的返回动画，也不是内存不足的推测。ExitInfo显示旧进程SIGKILL，既有冷重载日志明确记录了对应结束旧进程请求。另有首次模型准备开销，不能把所有等待归于这一公式。

## 最小修正

只修改主分支既有 `StatusBarHeightCompat.java`：计算上限至少容纳已经计算好的安全基准 `base`。不改主题、动画时长、SMEngine或重载协议，不禁用真正的状态栏配置重载。

```
upper = max(base, max(safeFloor, system + maxExtra))
```

system=63和145、cutout=145、gap=5时均得到150。无刘海和关闭自动适配的旧结果保持。原版/clean_launcher没有这层现代Insets校准，maintained也不是该原版GL布局的替代实现；修复放在当前已有兼容拥有者。

## 验证与限制

- 902项生产计算检查通过，包括真实63/145切换、无刘海、关闭自动适配、间距与偏移组合。
- 主分支保留全部既有未提交工作；常规build.bat、v1/v2/v3签名验证通过，保留数据安装到Android17模拟器。
- 新APK SHA256：`dced4a6082ceafedf03ae1d02ceb43bb60cc403e84859ca35c99c91fee25abad`。
- 安装后本次PID6349记录GL首帧889ms、模型/页面就绪6160ms，随后桌面设置→HOME采样前后PID均6349，无对应自动重载。GL日志不等于SurfaceFlinger呈现时间。
- 这组前后还包含不同APK基线和缓存/系统负载差异，因此不以24.2s与6.16s之差宣称补丁整体加速比例；主要确认的是63/145触发的无效冷重启路径已从公式上消除。
- Android9/16实体机、其他ROM、所有主题和手动状态栏偏移仍未在此次实测；不把纯计算回归当成真机非退化。

证据：`home-root-module/build/home-route/api37-test/loading-root-cause.log`、`cold-reload-causes.log`、`launcher-exit-info-current.txt`，以及本主分支 `build/api37-statusbar-audit/after-current.log`。本次未更新MEMORY.md。

## 受控前台测量与残留成本

补充：此前889ms/6160ms和历史24秒等记录包含不同负载及切出桌面时间，不能解释为纯前台模型处理耗时或补丁加速比例。

最终框架重启boot16后，受控前台冷启动PID4870：Surface1153ms、GL首帧完成9276ms、模型9438ms、页面9456ms，无自动冷重载。Perfetto确认首个onDrawFrame持续8123.710ms。该日志仅为绘制完成，不是物理呈现。

独立冷启动PID5379的三次主动SIGQUIT栈分别命中GL线程内PNG压缩（LauncherModel/Utils/Bitmap.compress）、AdaptiveIconDrawable栅格化及模拟器glGenTextures/QemuPipeStream读操作。不是自然ANR，抽样不能量化各项占比。现已修复无效重载，但首帧内图标生成/压缩和纹理准备的长等待仍存在，本次不改原版SMEngine和图标持久化协议。

完整证据在home-root-module/build/home-route/api37-test/cold-foreground和cold-stacks；最终设置返回证据见另一工作区docs/compatibility/ANDROID17_FRAMEWORK_TEST_AND_RECOVERY_20261014.md。


## 默认图标与启动任务排序

## 2026-10-15 续查：场景帧CPU与帧间隔

本轮未再改生产排位、图标外观、SMEngine或Loading门，仅在现有LauncherStartupDiagnostics和vc加入有界启动帧诊断。日志最多记录12个场景帧，页面完成后停止；运行时关闭既有diagnostics开关则不计时。wallMs是onDrawFrame回调墙钟，cpuMs是该GL线程CPU时间，precedingGapMs包含交换缓冲、等待渲染或线程调度，不代表呈现时间。

重要纠正：恢复运行AVD后，旧A35D5B5E包在空目录样本frame-gap-20261015-01已达3849ms页面就绪，DB2561ms、场景绑定3639ms、完成事件3847ms。采样时诊断构建尚未完成，故该样本归属旧包，不能作为新帧探针包结果。它证明此前9–12s不能作为固定代码等待下限，也不能把随后变化归功于新诊断代码。实际卸载首装、宿主GPU缓存和授权状态仍未模拟。

诊断包SHA256 `011641446E2471E4B7FF2E538E09E0486F3A0A38E596E3C8A58CEC3FFE034523`，三轮同条件空目录、无并行构建/录屏/Perfetto：

| 样本 | DB完成 | 场景绑定 | 完成事件 | 页面就绪 | 构建场景帧wall/CPU | 紧接下一帧间隔 |
|---|---:|---:|---:|---:|---:|---:|
| 01 | 2214ms | 3242ms | 3435ms | 3437ms | 1210/844ms | 5ms |
| 02 | 1811ms | 2858ms | 3037ms | 3039ms | 1214/840ms | 1ms |
| 03 | 1929ms | 2904ms | 3160ms | 3174ms | 1220/837ms | 1ms |

场景绑定到完成事件179–256ms，完成事件到页面消息2–14ms。没有复现此前1.56–2.57s空档，不能将旧间隔直接认定为固定延迟、手势后台机制或需移除的引擎安全门。新数据中剩余真实成本是1.8–2.2s数据准备，以及约1.21s首次完整场景帧（CPU约0.84s）；GPU/调度和其他阶段仍需结合实际设备判断，不把wall减CPU全算GPU。

读取旧Perfetto有效：final-page-priority样本GL onDrawFrame约1692ms、eglSwapBuffers约699ms，证明存在显著非纯Java图标计算开销，但它不是本轮同环境收益基线。颜色算法独立探针21次64px样本wall105/CPU103ms、256px样本wall803/CPU684ms；生产已用64px路径。本轮未为这项微基准改动颜色算法或再加缓存，避免破坏颜色排序与图标来源。

标准构建、v1/v2/v3签名及模拟器保留数据安装通过；三轮均恢复原用户0目录和亮屏设置1，无新增AndroidRuntime崩溃。两台实体机未操作；不声称物理呈现、全ROM性能、完整卸载重装或主题全矩阵验收。证据：build/startup-circle-audit/frame-probe-20261015-01..03及frame-probe-20261015-results.json。当前APK包含原先最小性能补丁及本轮诊断，只有诊断变化，不能宣传成新增提速修复。


## 2026-10-14 后续：首次加载分段与最小修复

最新交付APK：`build/launcher-signed.apk`，SHA256 `A35D5B5ECA20977A06D3B66AA9253FC470A3A79DC64D634F18D897A48AA86601`。下文旧交付hash和中间样本属于历史记录。本轮只改home-main/main，ROOT模块未改。

新增轻量一次性时间标记覆盖DatabaseHandler的包查询、初始布局、待同步应用、图标缓存、GL场景绑定与原完成事件；Page诊断增加elapsedRealtime。没有把LAUNCH_FIRST_FRAME、LAUNCH_PAGE_READY或GL完成事件解释为SurfaceFlinger实际呈现。

两个修前空数据样本页面就绪分别16104/12218ms。第二个样本可拆为：包查询27ms、初始布局151ms、待同步应用3209ms（其中逐项系统应用放置1834ms、普通应用17ms）、图标缓存/颜色1737ms；DB完成6785ms、两页构建2257/1303ms、原MESSAGE_COMPLETE在12218ms。这些样本说明不应继续把全部等待归为首次EGL初始化，也不能把12秒全归因于某个单项。

### 实现

- DatabaseHandler A新增局部placeStartupItems事务边界，仍调用原H/G排位、重复判断、逐项ID分配和Aa模型发布；同一批启动同步只在最外层落盘一次，空批次直接返回。未修改通用TransactionTask、数据库Schema或同步耐久级别，不在颜色线程池等待期间持有事务。
- 复用LauncherModelRepository增加StartupPlacementCommit监听。原嵌套TransactionTask可能吞掉异常而使父事务回滚，监听必须确认提交；回滚不能误报批次成功。显式异常回滚后清除临时Aa映射，沿原启动保护重试；完成消息只在数据准备成功后发送。
- DefaultIconCircleRenderer由两次完整像素遍历改为扫描每行Alpha左右端点，再按每行最远端点求原包围半径。径向平方距离的最大值必在行端点，保持原Alpha阈值、四百分比留白、scale、平移及阴影/几何。外观算法和token不变；40组随机、稀疏、单行、实心、传统/自适应图标与上一版逐像素sameAs通过。
- 新增标记位于A、d/c启动事件和Eb，仅诊断；没有修改SMEngine、Loading关闭门、原动画时长，没有假设数据未就绪也可直接显示可交互桌面。

### 最终包五轮空数据结果

相同AVD Smartisan_API37_Test/API37、用户0、12宫格、黑色普通主题、圆形默认图标，保留运行时权限/全局设置；每轮移动并恢复原应用目录。无Perfetto、录屏、SIGQUIT或并行构建负载。属于空应用目录模拟首次加载，不是卸载重装测试。

| 样本 | 放置批次 | 数据准备完成 | 场景绑定完成 | 原GL完成回调 | 页面就绪 |
|---|---:|---:|---:|---:|---:|
| 01 | 41ms | 4423ms | 7144ms | 8810ms | 8867ms |
| 02 | 168ms | 5128ms | 7762ms | 9323ms | 9325ms |
| 03 | 83ms | 4022ms | 7065ms | 8684ms | 8776ms |
| 04 | 397ms | 4295ms | 7733ms | 10301ms | 10374ms |
| 05 | 156ms | 6438ms | 9551ms | 11900ms | 12144ms |

最终页面就绪中位数9325ms、最坏12144ms，仍有明显等待。修前只有两轮，不宣称严格整体提速比例；批次落盘耗时下降有直接分段证据，不能把所有差异归因于这一个补丁。图标等价优化尚无独立稳定CPU加速比例。

剩余边界已定位：数据准备4.0–6.4s；原场景绑定约2.6–3.4s（含两页图标/阴影/纹理）；场景绑定到下一原GL完成事件仍1.56–2.57s。最后一段在原d/c引擎事件交接，未找到固定sleep证据，不能直接删除安全门。下一步如继续改结构，必须先拆首个完整场景绘制/交换缓冲与该事件调度，不直接把第二页或颜色元数据删掉，避免首次翻页/排序异常。

### 验证与边界

- 五轮数据库完整性均ok，22个条目的ID、包名、组件、用户、pageIndex/cellIndex与修前完全一致，无重复/缺项；检查输出`build/startup-circle-audit/final-placement-integrity.json`。
- Android生产提交监听9项正常提交、嵌套回滚、外层回滚、数据原子性及事务释放通过。可复跑源码`tools/tests/startup_placement/StartupPlacementProbe.java`；运行时CLASSPATH需包含最终Launcher APK。
- 40组图标逐像素等价＋上述9项共49检查通过，探针与原参考Renderer保存在`build/startup-circle-audit/renderer-differential/`。
- 图标合同审计、58项阴影/缓存及24项主题转换通过。标准构建和v1/v2/v3签名验证通过；最终包保留数据安装到模拟器。原用户0数据/默认HOME/亮屏设置已恢复，恢复截图`startup-final-restored.png`检查正常；无新增AndroidRuntime崩溃。
- 全部原始时序在`build/startup-circle-audit/scene-final-01..05/`，汇总`startup-final-results.json`。完整硬件呈现、录屏时间线、实体机Android8–16、全主题/动态图标/备份恢复矩阵本轮未测；不声称首次加载彻底解决、所有ROM提速或壁纸闪回因此修复。


日期：2026-10-14。源码位于home-main/main，模块未修改。原工作区已有未提交内容全部保留。

## 可见问题与根因

默认图标原来使用opaque-cover裁切策略，从原图中心提取圆形区域。电话卡和不规则图案的边角因此丢失。用户明确要求默认圆框内完整保留图案及留白，本轮修改的是来源规范化，不改变最终图标尺寸、阴影或宫格几何。

启动慢存在多个阶段，不能用GL首帧日志代表完整桌面可用。实测主动SIGQUIT栈（非自然ANR）显示DatabaseHandler在IconDB初始化中等待Utils的invokeAll，8个任务生成原图/阴影/PNG；另一个颜色分析批次调用ItemInfo.Oe，能再次迫使缺失缓存生成。初始GL静态图标也会先写PNG再解码，而后高清路径重新读取原图。此外，首次没有刘海缓存时会先按63初始化，实际145到达后主动冷重启；搜索/图标迁移/系统壁纸PNG准备原先早于页面就绪竞争资源。

## 修改

- DefaultIconCircleRenderer：保留固定外部圆框；自适应背景铺圆框，前景和普通图标按所有非透明像素的实际包围半径完整缩放，保留4%径向空隙；应用本身已有的留白保留，只缩小会碰到圆框的内容，不放大已适配的前景。没有按包名特判电话卡，没有修改CUSTOM/PACK/IMPROVED来源。版本token升到v7，旧生成缓存不再命中。
- IconRasterDiagnostics与e/s：只对启动期间的普通DEFAULT来源，把原有持久化缓存任务登记到最多512项的临时表，页面就绪后交给已有IconPreviewRepository的P2后台队列。GL缺失缓存时直接用既有来源解析和唯一Composer显示；失败或超限保留原路径。
- e/q：被延后的默认来源仍提前完成颜色元数据分析，但直接读取位图，不再经Oe触发PNG往返。其他来源、动态图标和特殊路径继续原行为。
- 后台持久化复用原Aa/Utils/IconDB；执行前验证item ID、包名、组件和用户身份，防止已删除/替换条目写回。没有新Service、线程池或图标Manager，没有跨线程使用GL纹理。
- J与MaintainedLauncherSettingsHost：在原MESSAGE_COMPLETE/page-ready边界释放持久化工作；搜索索引预热、搜索资源准备、图标revision迁移和首次系统壁纸同步移到页面就绪后的既有帧回调。自动壁纸请求只合并到最新状态，不在普通HOME上反复写壁纸。不以帧回调证明已物理呈现。
- StatusBarHeightCompat：API29+无缓存时先读DisplayCutout，仍保留系统读取失败后的实时校准。前一轮的安全高度上限修正也保留；Android8/9不调用API29入口。

## 验证方式

仅操作Smartisan_API37_Test/emulator-5554，Android17/16KB、1440×3120。实体手机未操作。为验证缺失缓存，把原模拟器用户0的databases/shared_prefs/files/cache/code_cache/no_backup移出并保存，使用空应用目录采样，结束后恢复原目录。未执行主用户卸载或pm clear，运行时授权和全局设置仍保留，所以不能称为完整卸载重装验证。

曾建立临时测试用户10，但多用户切换/锁屏影响样本，未据此做性能结论；该测试用户已删除。熄屏样本、混有构建负载的样本及不同GPU缓存样本均不用于宣称提速比例。证据保存在build/startup-circle-audit。

检查包括生产Renderer的Android像素探针：正方/横长/竖长、传统/自适应图标四角颜色全部保留，31项通过（含保留应用已有留白）；902项状态栏计算、58项阴影/缓存选择及24项主题转换、49项主题壁纸选择/写入/启动门控、图标合同静态审计通过。常规build.bat、签名及保留数据安装另行记录最终结果。

## 已证实与未完成部分

最终补丁前一版本的空数据无录屏诊断样本PID16316，GL完成3268ms、页面17277ms；SIGQUIT栈中DatabaseHandler已不在invokeAll等待。带完整追踪/录屏样本仍出现约35秒页面等待，不能把两者相减作为加速比例。另一个样本Creating EGLContext达15.08秒，表明模拟器图形初始化有显著波动。

已确认后台21项原缓存补写完成、无补写失败记录。没有证明所有首次安装等待已经消除；剩余数据准备、当前页面场景/阴影/纹理及模拟器图形开销仍需进一步拆分。不能通过提前隐藏Loading、空白占位、缩短原动画或跳过必要布局来伪装完成。

本次不把保留原代码路径当作图标包/自定义/改进版完整运行时回归，不把模拟器结果推广为Android8–17全ROM性能保证。未新增完整备份恢复、所有主题、动态图标或vivo非退化验收。

MEMORY.md未更新；DEVELOPMENT_LOG.md及文档索引更新。未暂存、提交或推送。

## 最后一次空数据验证与交付核对

启动改动相同、最后添加“只缩小不放大”约束前的样本PID18131（不带Perfetto/录屏）记录：Surface2484ms、GL绘制完成2641ms、模型12177ms、页面12178ms、可延后任务12386–12460ms。21项缓存补写完成，失败0，无状态栏自动重载；证据final-thumbnail/result.json与startup.log。该样本APK为574D9563…，最终交付另行记录SHA256；不能把中间样本与不同追踪/图形缓存条件的旧样本作严格加速百分比。

带追踪/录屏的final-page-priority样本仍达32120ms，另有模拟器图形和当前页面准备成本；此处明确保留慢样本，不声称性能问题整体验收。必要布局/当前页面纹理仍是Loading的条件，没有提前移除Loading冒充可用。

隔离测试的原用户0目录已恢复，测试用户已删除，屏幕供电设置恢复原值1。恢复数据后实图确认电话卡完整边角/齿轮与模块触角嘴部保留；最后“只缩小”约束需以交付截图为准。数据库抽查table_icons有22行（含设置入口），原缓存补写仍通过既有IconDB，没有弃用图标备份来源。

### 最终交付状态

- APK：build/launcher-signed.apk，SHA256 `10ea06ce4886a3475def28d3fe3a04ac4a1f2d69b4fff56f93c0e2035d70e112`。常规构建、v1/v2/v3签名与保留数据安装通过。
- 最终像素探针31项通过，交付截图build/startup-circle-audit/default-circle-delivery.png：SIM卡和齿轮完整，Phone/Gmail等原有留白保持。未修改模块图标或模块代码。
- 原用户0的数据已两次正确归位，当前仅Owner，stay_on_while_plugged_in恢复1。测试缓存另存/data/local/tmp，未删除原桌面布局。
- 多用户测试恢复后的手势复核曾出现BYPASS，未据此直接判定生产补丁故障。重启现有框架后boot17确认KEY_OBSERVER_AND_HOME_BRIDGE_READY；系统设置→上滑HOME记录HOME_SENT/BRIDGE_HOME_SENT，Launcher PID1698前后不变，前台恢复Smartisan。仅证明本次返回路线恢复，未据此证明物理呈现或所有动画矩阵。
- 初次加载仍为部分优化：12.178秒样本与32.120秒带追踪样本均保留，未宣称秒开或整体性能验收。完整卸载首装（含运行时权限初态）、更多安装应用、各managed图标来源、多主题及实体Android8–17需补充验证。
