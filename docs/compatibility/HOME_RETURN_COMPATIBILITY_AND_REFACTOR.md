# APP → HOME 系统壁纸闪现：设备结论、证据与重构方案

更新：2026-10-14。范围：`E:\FANG\smartisan\home-main` 主分支；不修改原始工作目录的平板适配。本文汇总 10 月 11–14 日证据。10 月 13 日按用户要求不再连接／操作实体手机，随后单独获准测试 Android16 虚拟机；新增结果见第10–16节。

2026-10-24 补充：用户已重新授权 OPPO 实机安装与回归，当前 original-port 的入口修复及最新闪回证据见第22节。下文10月11–14日的环境限制和失败实验保留为历史，不作为最新设备授权或源码状态。

## 1. 当前结论

**按用户最新授权，已交付“主题与系统壁纸同源同步”的最小候选包，Android16虚拟机普通主题有效返回样本不再露出原先的异色壁纸；OPPO手势最终验收仍未完成。**

此前不改变系统壁纸的方案尚无经过验收的OPPO修复。已经证实交接期间系统 Wallpaper 可见，而 Smartisan 完整桌面图层未连续可见；尚未定位一个能单独消除整个空档的应用侧改动。

vivo Android 9/16 是正常体验基准。OPPO 上 Nova 是正常体验基准，不能因为它的背景包含 Wallpaper，就将其标为“也存在用户可见闪回”。其他未提供现场证据的 ROM 不得填为正常或异常。

“代码能构建”“GL 回调结束”“有 buffer”“窗口已经呈现完整桌面”是不同结论。不能用前三项代替最后一项。

## 2. 机型与导航矩阵

| 设备／系统 | 桌面及场景 | 结论 | 证据及边界 |
|---|---|---|---|
| vivo X21A / PD1728，Android 9 | Smartisan，全面屏手势，普通 APP → HOME | **用户确认正常** | 用户明确两种导航都正常。本次历史最终组主要是 ADB HOME key，不能冒充实际手势逐帧验收。 |
| 同上 | Smartisan，虚拟键，普通 APP → HOME | **用户确认正常；热恢复采样正常** | 10/11 最终稳定组同 PID 3 次 HOME 无新增冷启动／Context／scene 重建。ADB keyevent 不等于点按屏幕上的虚拟键。API28 无 FrameTimeline，缺完整 SF 首呈现对齐。 |
| 同上 | 覆盖安装后的首轮 HOME | **另有启动异常，未解决** | LauncherAlias 任务结束、新 Activity、PID 29882→30180，新进程执行 cold tasks。不能混入稳定热返回 PASS，也不能将它直接认定为壁纸闪现原因。 |
| vivo V2458A，Android 16 | Smartisan，全面屏手势，普通 APP → HOME | **用户确认正常；最终所测 3/3 正常** | 10/11 最终包、同一恢复路径，保留 EGL Context 和 scene。具体 OriginOS 版本未在本轮复核，不把 Android 版本写成 OriginOS 版本。 |
| 同上 | Smartisan，虚拟键，普通 APP → HOME | **用户确认正常；有 HOME key 辅助样本** | 历史候选 HOME key 3 次；不与最终手势包或实际虚拟键点按混称一套完整验收。 |
| OPPO PDCM00，Android 12 / ColorOS V12.1 | Smartisan，全面屏手势，普通 APP → HOME | **异常** | 用户视频；10/12 固定 APK 手势组；主分支后续录像均可见森林系统壁纸。 |
| 同一 OPPO、同一 Smartisan APK | 实际虚拟 HOME 键，普通 APP → HOME | **用户视频正常；同包对照所测正常** | 导航 mode=0，实际点按 HOME 区域 3 次；与手势组同 APK。SF 所采样窗口未观察到 Wallpaper 可见区域，不能保证捕获了任何亚采样间隔的瞬间。 |
| 同一 OPPO，Nova 8.0.18 | 全面屏手势，普通 APP → HOME | **用户确认正常，作为正常参照** | 10/12 同包三轮及后续三轮录像。它的图层角色和背景组成不同，不能直接比较“某个 SurfaceFrame 结束”来给整个桌面排名。 |
| OPPO / ColorOS Android 16，具体机型未知 | ColorHomeFix 1.5，ROOT 模块 | **用户提供的有效效果描述；未由本任务运行验收** | 已静态审计 APK。没有本设备同包前后 trace；不得推广到 Android 12，也不得将 targetSdk36/minSdk29 当作运行兼容证明。 |
| Android 16 模拟器 emulator-5554 | Smartisan，手势返回 | **仍有异常／空档** | 10/11 录屏与图层证据；部分注入手势没有真正回 HOME，应排除这些无效操作。不能用模拟器代替 OPPO 根因。 |
| 同一模拟器 | 三键、HOME key、最近任务及 sleep/wake 辅助采样 | **完成部分操作采样，不等于全正常验收** | 最终 HOME key 3 次；仍有 GL/buffer→可见图层空档。sleep/wake 不等于带凭据的真实锁屏解锁。 |
| 一加、小米／HyperOS、三星／One UI及其他 ROM | 任意导航／主题 | **未验收** | 当前没有可对应机型、APK 和路线的完整现场证据，不能从 OPPO 或模拟器推断。 |

### 其他场景的结论边界

| 场景 | 已有证据 | 仍缺什么 |
|---|---|---|
| 普通应用热返回 | 上表各指定设备与导航组 | 不能覆盖所有应用、主题、低内存和长期后台恢复。 |
| 最近任务 → HOME | vivo9/16 历史候选各 2 次、模拟器辅助样本 | 最新宿主实验没有完整跨设备最近任务回归。 |
| Back 返回 | vivo9 历史候选 2 次 | Back 与 HOME 的窗口路线不同，不替代手势验收。 |
| 锁屏／解锁 | 模拟器 sleep/wake；其他专项历史记录 | 本专项未完成两台 vivo、OPPO 双导航的真实锁屏／凭据及解锁动画矩阵。 |
| 快捷桌面／文件夹／四指／编辑 | 项目其他专项存在历史正常记录 | 不能当作新 HOME 宿主原型的回归；新原型未完整验收。 |
| 普通主题切换 | 模拟器 Blue→Black 及两次 HOME 辅助样本 | OPPO、新宿主及实体机透明／毛玻璃完整矩阵未验收。 |
| 60–144Hz、GPU／内存、后台耗电 | 部分 trace、瞬时 meminfo、attachment 暂停区间 | 未完成完整帧率、长稳、压力和电池前后对照。不得标“全部通过”。 |

## 3. 样本与版本必须分开

| 样本组 | APK SHA256 | 用途 |
|---|---|---|
| 10/11 最终主包 | `4944E939ADBE8E75C78C0A3CDDA06DDF325F852722BAFF01309ABDDDFEEA53EA` | vivo 基准及统一热恢复；不是 OPPO 当时安装包。 |
| OPPO fixed gesture / threebutton | `765DA86BF41A20FBF68C49F8BB1E10B32999504087986A5E854D9E355C47FA60` | 严格同包双导航，来自另一次操作的安装，不是当时 main 产物。 |
| Nova fixed gesture | `262535B90196C651557C1B63D78B80F06D80434DD4E8AA9706639B1E5E9E630B` | Nova 正常参照，8.0.18。 |
| main contract stable off / final on | `891C7D3A5624AEE97D8CEBA3EF097D7479D569565DAB09E40A6BE17CAD287AB2` | 位置回复 A/B；两组各 3 次，均同 PID30905；不是完整 Nova 协议实现。 |
| texture host on / off | `B8CBE0CA3EE26DB0F70481F323E3AE8387AB4AB1FDFCC85A2C40E7A3371CCB8B` | EGL 输出转接 A/B；每组内 PID 稳定，切换宿主重启后跨组 PID 不同。 |

混包、锁屏遮挡、没有回到 HOME、位置回复未实际发出、安装后首轮 PID 更替等样本，保留原件但不计入严格对照。`main-contract-final-off` 的首次 PID更替组不作为稳定关闭基线；替代组为 `main-contract-stable-off`。早回复缓存只准备过 warmup，没有有效 early-on 对照，不得写成“已试无效”。

证据目录：`build/home-unified-20261011/` 和 `build/home-coloros-audit-20261012/`。其中 APK、视频、trace 是忽略目录中的本地证据，不会自动随 Git 文档提交；分享报告时需要单独保留或归档。

本地可查看的主要录像：[Nova 参照](../../build/home-coloros-audit-20261012/nova-record-reference/return.mkv)、[位置回复实验](../../build/home-coloros-audit-20261012/main-contract-final-on/return.mkv)、[Texture 转接开启](../../build/home-coloros-audit-20261012/texture-host-on/return.mkv)、[同包原宿主](../../build/home-coloros-audit-20261012/texture-host-off/return.mkv)。详细机器数据见各组 samples.json、trace-timeline.json、sf-timeline.json；早期 AUDIT_REPORT.md 中“未安装／无录屏”的表述只适用于当时的初始审计阶段，不能覆盖后续诊断与转接实验。

## 4. 已确认的机制与未确认的原因

1. **正常 vivo 也会重建 Surface。**最终稳定样本 EGL Context generation=1，scene identity 不变。Surface 重建不是异常 ROM 的充分原因。
2. **OPPO 手势与真实虚拟 HOME 键的交接不同。**手势经过系统 Quickstep RecentsActivity、Wallpaper 绘制和动画图层，再启动第三方 HOME；同包三键没有观察到相同露底。
3. **已有 buffer 不保证可见。**SF 采样中存在子 buffer 有效但父 Activity／窗口隐藏或可见区域为空的时段。onDrawFrame、swap、FrameTimeline 事件结束均不能代替完整画面呈现。
4. **OPPO 实际发送了手势协议。**主分支诊断三轮均收到有效 `gesture_nav_contract_v1` 和回调。此前“是否发送”已不再是未知项。
5. **首帧内容与呈现仍须分开。**诊断前两次 PixelCopy 为 `ERROR_SOURCE_NO_DATA`，随后成功取得含完整背景／图标的桌面 buffer。这是复制时点的源数据可用性证据，不能直接推断前两次 GL 没有绘制；swap、BLAST 与 latch 都可能影响可读时机。
6. **原恢复任务确有重复工作，已作最小修复。**10/11 删除每次 Resume 无条件重开 cold gate，保留 pending/dirty/TTL 检查。这是确定的重复调度，不是已确认的全部闪回根因。
7. **部分露底早于 HOME Intent 到达应用。**离线重算 `main-probe-gesture` 三轮，首个 Wallpaper 可见采样分别为 270–380、260–320、220–260ms；协议到达分别为 386.201、378.752、369.589ms。这些采样范围均在 Intent 标记之前。因而只修改 Intent 到达后的 onResume／图标准备，不能覆盖这段已经开始的交接。它不证明所有应用侧方案不可能，也不证明 Wallpaper 当时占满屏幕；当前 APP 仍可能覆盖其中一部分。

尚未确认：缺少完整图标 Surface 协议是否影响**后段图标收拢**；框架／ROM 的窗口同步、HOME 显示和动画 alpha 分别占多大比例；怎样以普通 APK 提前完整 HOME 的参与时机。第13节的 Nova 对照进一步限定了协议能解决的时间范围，不能据此宣布“ColorOS 无解”或“重构必定解决”。

从原始 samples／日志／SF 生成的精简可复核数据：[HOME_RETURN_EVIDENCE.json](HOME_RETURN_EVIDENCE.json)。仅重算已有证据，没有追加设备测试。

### 帧时间线

10/11 vivo 数据以 **Resume=0** 为原点：

| 样本 | Surface 创建 | 首 GL 完成 | SF SurfaceFrame 事件结束 | 首有效 buffer 图层可见 |
|---|---:|---:|---:|---:|
| vivo16 最终手势 3 次 | 10.0–13.8ms | 20.9–24.2ms | 25.5–28.6ms | 73.8–88.6ms |
| vivo9 最终稳定 HOME 3 次 | 34.0–42.5ms | 46.1–51.1ms | API28 无此数据 | 缺完整对齐，不能补造 |

OPPO 的原点是 **注入返回输入前采样 BOOTTIME**，包含 ADB 调度，不能与上一表直接比大小，也不能把 200ms swipe 与 tap 的总耗时差当作 ROM 延迟：

| 组别 | Resume | GL 完成 | 首 SF 事件结束 | 首可见图层采样范围（各轮） |
|---|---:|---:|---:|---|
| fixed 手势 3 次 | 372.2–455.8ms | 415.9–501.4ms | 423.0–508.2ms | 530–590 / 480–510 / 510–540ms |
| fixed 实际三键 3 次 | 196.3–245.0ms | 230.6–289.3ms | 238.1–294.1ms | 380–420 / 290–320 / 350–380ms |
| Texture 输出转接开启 | 367.2–450.0ms | 416.4–505.5ms | 内容进入主窗口，不能套用旧子 Surface 指标 | 主窗口 530–590 / 640–680 / 460–530ms |
| 同 APK 原宿主 | 355.3–397.3ms | 407.3–437.5ms | 原独立 Surface 路径 | 子图层 530–580 / 480–570 / 470–530ms |

SF 可见性是带采样间隔的合成状态，不是显示面板首个完整像素的精确时间。scrcpy 录到了设备编码画面，但其首帧与 trace 的绝对 BOOTTIME 尚未严格对齐，不能逐毫秒硬拼。绿色阈值只用于筛选森林候选帧，候选区间含缩小中的 APP，不能称为“纯壁纸闪现时长”。

## 5. 已做方案的结果

| 方案 | 结果 | 当前处理 |
|---|---|---|
| 场景／Context 热复用、cold gate 收口 | 消除已确认重复工作；保留原动画路径 | 保留 10/11 最小实现；不标 OPPO 已修复。 |
| 整屏截图遮盖、延后 Surface 到 focus | 未消除系统缩窗阶段壁纸，增加显示和截图任务 | 已废弃，不恢复。 |
| Android14+ attachment 生命周期 | vivo16／模拟器仍每次重建 Surface；长时电池未验收 | 关闭。OPPO API31 不适用。 |
| 普通主题关闭 SHOW_WALLPAPER | 模拟器无稳定收益，系统 Recents 自身也请求 Wallpaper | 不正式开启；透明／毛玻璃不能套用。 |
| 只回复图标位置 | 三轮发送成功，录屏仍露系统壁纸；没有系统接收确认，未提供图标 Surface／结束回调 | 实验归档；不能说等同 Nova，也不能说已经改变了系统收拢目标。 |
| EGLWindowSurfaceFactory 转接 TextureView | 画面与点按设置可运行；被比较静态 ROI 像素零差异；原核心 DEX、native 库、资源及 Manifest 相同；三轮仍露壁纸 | 不作为正式修复启用。它仍保留 SurfaceView 壳参与窗口／Surface生命周期，不是完整 TextureView 宿主重构。 |

旧 Texture 转接保留 SurfaceView 壳；第12节记录了随后独立 SurfaceView 图层为0的主窗口宿主实测，仍未消除模拟器闪回。位置回复不足以否定完整图标协议，但第13节的同机 Nova 图层对照说明，完整协议也不能被预先当作早段 Wallpaper 暴露的修复。

## 6. 三个参考项目如何使用

### OpenSmartisanOS

审计版本：`lineage-23.2`，commit `9222aa7dc53edcd84e7d7d1f5ff65706f622bf1b`。

- [SmartisanHomeView](https://github.com/OpenSmartisanOS/android_packages_apps_Launcher3/blob/9222aa7dc53edcd84e7d7d1f5ff65706f622bf1b/src/com/android/launcher3/smartisan/view/SmartisanHomeView.kt) 是 Launcher3 中的 Android View 桌面层，不是原版 SMEngine。
- [GestureNavContract](https://github.com/OpenSmartisanOS/android_packages_apps_Launcher3/blob/9222aa7dc53edcd84e7d7d1f5ff65706f622bf1b/src/com/android/launcher3/GestureNavContract.java) 和 FloatingSurfaceView 可参考协议解析、目标查找、临时图标 Surface 和清理；当前原版图标是 GL 对象，不能直接调用对应 View.draw。
- HomeLayerCoordinator 可参考图层显隐／输入／无障碍职责划分，但不能代替独立 Surface 的有效性与系统呈现判断。
- [Android.bp](https://github.com/OpenSmartisanOS/android_packages_apps_Launcher3/blob/9222aa7dc53edcd84e7d7d1f5ff65706f622bf1b/Android.bp) 的 Quickstep 构建使用平台 API／特权部署。复制代码或普通安装，不会自动取得系统 Recents 控制权。

### 本地 maintained

`E:\FANG\smartisan\smartisan-launcher-maintained` 的 `res/layout/launcher_view.xml` 明确使用 SMGLSurfaceView；该类仍继承 GLSurfaceView。**修正此前过宽的“maintained 是普通 View 桌面”表述**：设置页可用普通 View，主桌面仍是 GL 链路。

可参考可读的 Launcher／LauncherProxy／SMGLSurfaceView 恢复与任务调度；不能将它当成 OPPO 已验证无闪回版本。目前没有它在同一 OPPO、同主题、同导航的验收结果。不得整块替换原版核心或照搬不相关后台任务。

### SmartisanWeather-Revived

审计版本：commit `f6b21ec549f1700ed5cf80d4f6a402eb1a11ba29`。

- [MainActivity](https://github.com/Mangi-11/SmartisanWeather-Revived/blob/f6b21ec549f1700ed5cf80d4f6a402eb1a11ba29/app/src/main/kotlin/com/smartisan/weather/MainActivity.kt) 将权限、导航、生命周期与 Compose 展示分开。
- [WeatherDrawable](https://github.com/Mangi-11/SmartisanWeather-Revived/blob/f6b21ec549f1700ed5cf80d4f6a402eb1a11ba29/app/src/main/kotlin/com/smartisan/weather/ui/components/WeatherDrawable.kt) 在 Compose Canvas 中复用原版 Drawable／selector／NinePatch，给出了保留素材、分离资源拥有者和展示层的做法。
- 它是现代 UI 重写项目，不是 HOME／Quickstep 兼容案例。只能参考资源复用、生命周期和状态职责，不能据此推断“换 Compose 就无闪回”，也不照搬其数据库、依赖和构建体系。

## 7. 具体修复／重构顺序

**优先重构呈现边界，保留 SMEngine；不直接重写整个 Launcher。**目前没有通过的行为补丁，不继续叠加无证据延迟、图标预热或全屏遮罩。

### R0：先对保存的窗口同步证据定位

区分“没有完整 buffer”“完整 buffer 未被主窗口合成”“窗口／父层仍隐藏”。检查 WM finishDrawing／Surface 同步、Recents HOME task 出现和 alpha 的先后关系。若确认是当前代码迟报绘制或人为隐藏，直接修那个 Owner；缺数据则保留未知，不将一般框架源码当作本 ROM 的执行证据。

尤其要验证 ColorOS 在 Intent 到达前能否使用第三方 HOME 的既有完整画面／窗口或合法的系统缓存画面。仅把后段渲染改快，不会自动改变前段的 Recents 背景选择。若考虑 starting preview，先证明该 ROM 的 HOME 允许所需快照，不把普通应用的 snapshot 行为直接套用到 Launcher。

### R1：把原来的具体类型依赖写成明确兼容合同

原 SMEngine `Ra.FU` 与输入 `v.mView` 都是 GLSurfaceView；还通过原接口取 Context、位置并 requestRender。不能仅把 SMGLSurfaceView 的 superclass 改成 TextureView，也不能为了方便修改原 SMEngine 类型。

宿主适配必须保持原 Renderer、scene、线程／队列语义、输入对象身份、坐标、focus、有效性、上下文世代和时钟。Android 的“Surface 可用”、EGL“目标可用”、scene“资源有效”、窗口“完整帧可见”分别建状态，不能共用一个 ready 位。

### R2：完整宿主原型，排除昨天的 SurfaceView 壳局限

- 真实画面进入 HOME 主窗口；证明原 SurfaceView 不再创建会参与绘制同步的独立显示 Surface，而不只是把 EGL 输出改去另一个 View。
- 如需保留 GLSurfaceView 类型的兼容对象，明确它只服务原接口；其触摸／键盘／尺寸／focus／生命周期由实际宿主适配，不能留下不可见对象导致快捷桌面或解锁资格误判。
- 不建立第二个 scene、图标缓存或常驻全屏覆盖层；只允许一个活跃渲染拥有者。
- 复用原 EGL 配置和 Renderer。真实 Context 丢失才重接资源；resize 不冒充 Context 丢失。后台暂停必须能停止 GL 帧，保留资源也不能常驻全速更新。
- 检查主线程与 GL 线程的同步依赖。原 GLSurfaceView.onWindowResize 会等待绘制完成；TextureView 消费又依赖窗口绘制，不能用固定等待、循环重试或无界阻塞绕开。
- R2 的后续有限原型见第12节：已做到没有独立SurfaceView图层、完整画面进入主窗口，但手势仍露壁纸，已撤回。完整交互／主题／跨ROM验收未完成。10/12仅EGL转接与10/13本原型必须分别记录。

### R3：完整协议与窗口策略分别验证

Nova 的完整目标 Surface／finish 清理与位置回复不同。使用原 ItemInfo、当前用户、实际可见图标和原坐标拥有者；不得猜一个图标位置，或将完整桌面 Surface 当图标 Surface 缩小。普通 APP 返回、第二次 HOME、主题重载和解锁分别处理，保留原 J.a(Intent) 分页与解锁世代。

普通／透明／毛玻璃主题逐类验证窗口和 Wallpaper 策略；不在普通主题有效之后直接全局修改 Surface 格式。若窗口仍由系统隐藏，不继续“优化图标”冒充改善；也不未经验证宣布所有应用侧方案都无效。

### R4：验收门与停止条件

先验收渲染内容／输入／上下文／后台零帧，再比较同 APK 原宿主与新宿主的 APP → HOME 完整录屏和 WM/SF 时序；随后覆盖 vivo9/16 非退化、OPPO 真三键、手势、锁屏、最近任务、快捷桌面、主题及 60–144Hz。

必须同时满足：可见壁纸空档消失或有可复核改善；原图像和动画保持；后台资源／耗电有界。若单一宿主替换仍无改善，不将其作为发布修复。没有新增设备验收时，只能交付设计和构建结果，不能标解决。

**整套现代 UI 重写是另一条工程路线**：参考 OpenSmartisan 的 View 层或天气的 Compose 层重建视觉与交互，会替换原版渲染／动画实现，不能同时承诺 SMEngine 原逻辑保持。当前既有约束未被撤销，因此不默认选择它。

## 8. 本轮交付与限制

本轮整理矩阵、版本、排除项与重构合同，并将没有改善的 EGL 转接原型归档，解除其正式源码接入。保留默认关闭的轻量协议诊断，不写入正式图标位置回复或截图任务。原有 10/11 修改及其他工作区改动保留。

不再连接／操作手机，不改变壁纸、主题、默认桌面或导航。最后一次 OPPO 采样为 Smartisan 默认 HOME、手势，Texture 开关已设 INFO；10/13 没有复核其当前安装或设置。项目与全局 MEMORY.md 不更新；开发日志和索引记录本报告。修复尚未完成，R2–R4 不填造通过结果。

本地收尾验证：标准构建、v1/v2/v3 签名、16KiB 对齐、文档链接／JSON和 diff 检查通过。解除实验后的本地产物 SHA256 为 `B40FA56821D3F797D13C869EC9455878B24DE19934727748F3721EA65D802951`；未安装，不能与昨天的已安装 B8CBE0… 实验包混称。原核心 DEX、资源、Manifest、native 库与 10/11 基线逐项相同。

## 9. 2026-10-13 后续实验：恢复刷新任务的绘制交接门控（已撤回）

状态：本节保存实施阶段记录。后续按用户授权在 Android16 虚拟机安装并对照，三轮仍露壁纸，无稳定改善；已归档并撤回本节运行改动，以第10节为最终状态。第8节为此前收尾包，不是本节候选包。完整宿主重构 R2 仍未实施。

### 本次能确认的问题

原 `vc.onDrawFrame` 在 EGL swap 之前调用 `MaintainedLauncherSettingsHost.onLauncherResumeFrame`，直接向主线程投递 wallpaper pending、badge dirty、weather TTL 刷新。它没有等待主窗口帧提交，也不等待系统正在进行的 Surface 重绘通知。

保存的 `main-probe-gesture` 第 0 轮：GL 日志结束 412.605ms、刷新任务 420.517ms、trace 的 `finish draw` 标记 461.021ms。只能确认任务早于该标记；不能将其直接解释为任务造成了约 40ms 延迟。该 ROM 的标记源码位置尚未取得，不能把它等同于精确的 Binder finishDrawing／显示面板呈现时刻。

离线重算首个 View `draw` 结束到首个 `finish draw` 标记：同包 OPPO 手势 24.932／30.998／28.397ms；同包三键 16.763／22.865／19.206ms；Nova 6.349／4.360／5.799ms。三键也有间隔但体验正常，因此该间隔不是完整根因证明。

### 最小修改及职责

- 保留原 J、Eb、Renderer 绘制逻辑、SMEngine、Surface 创建销毁、EGL 配置、帧率与动画时钟、窗口 flags、主题和解锁路径。
- 恢复刷新内容继续由现有 `MaintainedLauncherSettingsHost` 执行，只将其释放条件交给已有窗口兼容 Owner `LauncherHomeCompat`。删除旧 pending 位／帧内直接投递方法，避免两个调度入口。
- Android 10+ 且窗口硬件加速、Observer 有效时，同时等待：当前 GL 回调后的 swap **尝试**、主窗口 `registerFrameCommitCallback`、本次已登记的 Surface redraw 回调完成。主线程收到任务后再次检查是否新增 redraw 请求；不提前运行原 `finishDrawing` 回调，不伪造帧完成，不通过反射调用 WindowManager。
- Android 9 及以下、软件窗口或失效 Observer 保留此前“GL 更新后投递”的调度边界。这是 API 能力回退，不是认定这些设备有相同系统实现。
- Pause、Stop、Destroy、重新恢复、冷准备和新任务替换会取消旧任务；旧 GL／窗口／Surface 回调不能释放新会话。任务未满足条件时，不增加定时器、轮询或持续渲染。
- `SMGLSurfaceView.surfaceRedrawNeededAsync` 始终委托原 GLSurfaceView，只包装原回调来观察其完成；诊断关闭且无现代恢复任务时返回原 Runnable。新增日志明确保留 `presented=unknown`，这些门控都不是显示面板呈现证明。
- 冷启动／冷重载的既有首帧门、原恢复完成协议不在本次修改范围内。

### 验证与边界

当时的 `tools/tests/home_return/run_tests.py` 编译真实 `LauncherHomeCompat`，以确定性 Android stub 和 GL／主线程队列验证：API23／25／28 旧路径、API29／31／34／36 新路径、两种完成顺序、并发完成、多个／晚到 Surface redraw、重复帧、取消、Activity 替换、旧回调迟到、窗口不可见和回调原样传递。177 项断言通过；测试不模拟真实 EGL／GPU／WM，也不代替真机视觉验收。撤回候选后该专项 runner 与候选源码一起归档到 `build/home-resume-handoff-20261013/retired-candidate/`，不留下针对已撤回行为的正式测试入口。

标准构建、签名与 APK 差异检查结果见开发日志。本次不能提供新的设备前后帧时间线；10/12 为修改前证据，不能挪作修改后结果。预计可减少刷新任务对交接阶段的干扰，但收益大小尚未实测；主窗口隐藏前段的 Wallpaper 暴露不由本补丁直接控制。vivo9/16、OPPO 双导航、真实解锁、主题、快捷桌面和耗电仍需后续验收，当前不标通过。

最终候选 SHA256：`B86FC41F3A28624C0750BEF9604A65D127F5B993CF06741CB4057BEC0AD8527A`。构建、v1/v2/v3签名、16KiB对齐通过；与 B40FA5… 包相比，1,954 项 Manifest／资源／assets／native 内容相同，仅两个 DEX 与签名项变化。未安装。原始资料和本轮定向 diff／测试／构建结果保存在 `build/home-resume-handoff-20261013/`。

## 10. Android16 虚拟机前后对照：补丁无有效收益，已撤回

用户随后明确授权使用此前同样闪回的虚拟机测试；这项授权只用于 `emulator-5554`，没有操作连接的 vivo X21A。Pixel_6_Pro AVD 为 Android16 / API36，导航 mode=2，默认 Smartisan，普通 Black 主题，显示尺寸1080×2400。测试前备份实际安装的 4944E9… APK；保留数据安装 B40FA5… 修改前包、B86FC4… 候选包，分别采三轮 Settings → 手势 HOME。两组各自同 PID、三次都确实回 HOME；安装／冷启动准备不计入热返回。

| 组别 | 可见现象 | 首 SF 桌面 buffer 图层可见，相对 Resume（每轮） |
|---|---|---|
| 修改前 B40FA5… | 3/3 缩小 APP 时露系统壁纸，之后出现完整锤子桌面 | 403.702／494.665／501.581ms |
| 候选 B86FC4… | 3/3 仍露系统壁纸；未消除空档，无稳定改善 | 492.410／453.382／538.629ms |

候选刷新门控按预期执行：第一轮 GL 交换尝试后173.021ms、窗口 commit259.962ms、Surface redraw回调265.418ms、刷新任务307.920ms。但492.410ms才记录到桌面图层可见。第二／三轮也没有由于门控而提前稳定显示。虚拟机负载、软件／虚拟GPU与调度波动明显，不以三轮数据宣称性能退化比例；但“没有消除闪回”已由录屏逐帧确认。

新的关键证据：候选第一轮 Resume 后347.123ms，桌面 BLAST layer已持有1080×2400 buffer，`is_visible=0`；其 `visibility_reason` 为 `hidden by parent`。祖先主窗口 `smt_launcher#296`、HOME Activity `#259`、HOME根任务 `Task=1#44` 仍有 `flag is hidden`。因此这一采样阶段不只是缺 buffer；系统合成状态明确禁止桌面显示。它不证明最早的 buffer 已含全部正确内容，也不单独证明是 ROM 限制或 Launcher 不正确的窗口同步通知，需要继续区分 WM／Shell 的同步与显隐原因。

录屏有 APP 缩小动画，不能说“手势把桌面送后台，所以完全没有过渡动画”。APP 打开后进入后台是正常生命周期；同包实际三键正常也排除了“后台”作为充分原因。所测异常是系统壁纸与完整桌面之间的交接，不能继续只优化图标或刷新任务来冒充解决。

新数据：[HOME_RETURN_EMULATOR_20261013.json](HOME_RETURN_EMULATOR_20261013.json)。本地[修改前录像](../../build/home-resume-handoff-20261013/emulator-before-gesture/video.mp4)、[候选录像](../../build/home-resume-handoff-20261013/emulator-candidate-gesture/video.mp4)及逐帧图、Perfetto完整 trace 均已保存。视频PTS未与trace绝对时钟校准；蓝色阈值仅筛选壁纸候选，区间包含缩小 APP，不能称纯壁纸闪现时长。FrameTimeline事件结束与图层可见仍不当作显示面板呈现。

撤回仅针对本次候选改动：三个Java／Surface文件恢复本次之前的逐字节副本，vc恢复原刷新hook；保留所有既有dirty改动。回退构建 APK SHA256 `ABA68CE1D1CC4064019C46593FB8F5EAD2FA0B50B242F34713C6D5C29CAD7F96`，ZIP条目内容与B40FA5…逐项相同，包含两个DEX；整包SHA不同，未冒充同一安装包。虚拟机恢复测试前4944E9… APK，默认Smartisan／手势保持，诊断设置恢复。未对vivo安装、切导航或操作。本次没有正式闪回修复，MEMORY未更新。

## 11. 手势模式下改用 HOME 键：路径对照有效，普通 APK 接管尚未实现

用户提出“手势能否按照虚拟键返回的方式处理”。本次在同一 Android16 虚拟机、同一安装包4944E9…、同一PID5135、相同Settings应用／Black主题下比较两种输入；导航一直是mode=2，未切三键、未安装APK、未操作实体手机。第一组上滑200ms三轮，第二组直接由ADB注入KEYCODE_HOME三轮。**第二组是手势模式下的HOME键输入，不冒充实际三键导航测试，也不冒充普通应用权限。**

| 输入 | 录屏观察 | 首桌面buffer可见，Resume起算 |
|---|---|---|
| 原生上滑 | 3/3缩小应用后露系统壁纸 | 443.042／378.373／375.659ms |
| ADB HOME键 | 3/3未观察到同类露底；应用退场过程中后面已有桌面 | 287.534／284.970／423.476ms |

逐帧颜色筛选辅助复核：手势录像151个编码帧中32帧为候选；HOME键133帧中0帧为候选。阈值只筛选，不是面板零闪帧证明；已人工查看时序联系图。按键第三轮的可见时间甚至晚于手势第三轮，但没有同类露底，说明“缩窗先露出什么、应用何时退场”不能被简化为GL首帧快慢。两组重日志带来额外开销，数据用于区分机制，不用于性能评级。

本次首次同时采到WM窗口状态、Shell transition和SF层状态，采法参考[AOSP Winscope文档](https://source.android.com/docs/core/graphics/winscope/capture/adb)。手势三轮均先有type1021、handler为RecentsTransitionHandler的transition，再将HOME打开transition合并；HOME键组相应返回为type1，没有这段Recents返回transition。手势第一轮：独立桌面buffer在Resume+190.731ms已存在，但当时仍不可见；WM后续于+286.213ms记录SURFACE SHOW，+330.969ms快照为HAS_DRAWN，SF于+443.042ms首次记录桌面buffer可见。其余两轮也存在DRAW_PENDING→HAS_DRAWN及后续显示阶段。**因此旧的“父层隐藏”证据不足以单独归因为系统故意等待到动画结束：窗口绘制同步和Shell交接都参与其中。**WM快照不能补造精确finishDrawing到达时刻。

ColorHomeFix静态代码核实：`GestureHook.install`通过Xposed挂接`com.android.quickstep.OplusBaseTouchInteractionService.onInputEvent`，其`GestureHook$2.run`以`Instrumentation.sendKeyDownUpSync(3)`发送HOME。它从系统手势输入入口改变路由，不是第三方Launcher恢复后再次startActivity。此结果不等于已经在Android12移植成功，也不证明它的全部效果仅来自这一钩子。

普通APK的限制：跨窗口注入按键受[InputManagerService的INJECT_EVENTS权限检查](https://android.googlesource.com/platform/frameworks/base/+/android16-qpr2-release/services/core/java/com/android/server/input/InputManagerService.java)约束。直接发HOME Intent也不等于撤销已开始的系统手势。已授权的[AccessibilityService.GLOBAL_ACTION_HOME](https://developer.android.com/reference/android/accessibilityservice/AccessibilityService#GLOBAL_ACTION_HOME)可以发起回桌面动作，但这个API本身不赋予第三方桌面拦截原生底部手势的能力；另做无障碍手势入口会改变交互，不能标成原手势的无缝修复。

决策：按键式返回是有录屏收益的兼容路线，若采用，应在系统手势拥有者处转换，不在Launcher.onResume中补发HOME，也不重写SMEngine。当前普通APK尚无已验证的早期接管点；root／系统模块适配属于另一部署方式，未安装、未修改系统或默认导航。免root原生手势问题仍未解决，不用“可以发HOME”代替“已经接管手势”。

文件：`tools/capture_home_return.py`新增默认关闭的`--window-trace`（API35+），有限采样内启用WM／Shell／SF transaction／指定ProtoLog组，随Perfetto会话停止，不改系统常驻日志属性。数据并入[HOME_RETURN_EMULATOR_20261013.json](HOME_RETURN_EMULATOR_20261013.json)的`home_key_route_comparison`。本地[手势录像](../../build/home-resume-handoff-20261013/emulator-wm-gesture/video.mp4)、[HOME键录像](../../build/home-resume-handoff-20261013/emulator-wm-home-key/video.mp4)和trace／联系图均保留。APK仍4944E9…、导航mode2，三项诊断设置已恢复为原来的不存在状态。此次无Launcher运行代码修改，无需重建安装；Python语法、六次实际回HOME和证据JSON检查通过。MEMORY未更新。

## 12. 免 ROOT 主窗口渲染宿主原型：已实施，未消除闪回，已撤回

用户要求按免ROOT方向继续修复。候选仍使用原SMEngine、J/Eb、Renderer、EGL配置、GL线程和输入对象；没有重写主题／动画，没有系统壁纸修改、全屏截图遮罩或固定恢复延迟。实验门默认关闭，仅API36普通Black主题配合`log.tag.HomeTextureHost=DEBUG`启用，实体vivo／OPPO未操作。

### 实现与旧实验的区别

原`SMGLSurfaceView`保留完整尺寸、View可见性、触摸、focus及GLSurfaceView类型。它向SurfaceView基类报告独立窗口不可见，使其不申请native显示Surface；实际可见窗口状态仍交给新宿主处理。TextureView作为同父级真实像素宿主，EGLWindowSurfaceFactory直接绘制到其SurfaceTexture，无Pbuffer预热、无第二场景或第二GL线程。尺寸变化通过原GL队列传递，利用GLSurfaceView支持的GL线程resize避免主线程等待Texture消费；后台通过既有surfaceDestroyed接口解绑EGL输出，恢复时复用保留的Texture、Context和scene。

这解决了10/12原型仍创建独立SurfaceView图层的实验局限。新候选三轮trace中桌面独立SurfaceView图层数量为0；主窗口有完整桌面像素。这是有限宿主原型，不代表全部键盘／拖放／配置变更／解锁合同验收。

构建途中补齐诊断世代访问方法；首次可安装包只支持FrameLayout，现场RootView是RelativeLayout，按预设回退原路径，**该启动不计有效实验**。补齐原RootView布局参数后得到最终候选`FA0A3171…`，正式对照均使用同一个候选APK，仅切实验开关并重启进程；开启PID7375、关闭PID8306，各组内PID稳定。未安装/测试过这些候选的设备不得列为通过。

### 验证结果

- 标准构建通过。与本轮前包比较，仅`classes.dex`、`classes2.dex`和三个签名条目变化；Manifest、资源和native内容相同。保留数据安装成功。
- 完整桌面能正常显示；截图静态第一行图标ROI `[0,140,1080,650]` 与原宿主逐像素一致；实际点按Settings进入系统设置，BACK返回可运行。
- 热返回未记录新的Context或scene创建；三个已解绑后台区间约1699.5／621.1／679.8ms，原GL线程`onDrawFrame`和`eglSwapBuffers`事件计数均为0。这只是短区间停帧证据，不能称长期耗电／内存测试通过。
- **开启组三次手势返回仍露系统壁纸，未达到修复目标。**主窗口有buffer后仍要等待WM／Shell显示；没有因去掉独立Surface就自动参与手势前段合成。

| 组别／轮次 | 首目标buffer快照，Resume起算 | 首目标buffer可见快照 | WM SURFACE SHOW日志 |
|---|---:|---:|---:|
| 主窗口宿主0 | 143.097ms | 283.055ms | 139.115ms |
| 主窗口宿主1 | 272.146ms | 404.214ms | 350.185ms |
| 主窗口宿主2 | 160.217ms | 298.959ms | 195.428ms |
| 原宿主1 | 197.437ms | 368.922ms | 255.839ms |
| 原宿主2 | 219.976ms | 434.458ms | 363.514ms |

关闭组第0轮在HOME完成呈现前已被下一轮启动Settings打断，日志有Resume后401.744ms即Pause、未采到该轮目标图层可见，排除完整返回性能比较；不能因采样时topActivity是HOME就记成功。两种宿主像素图层不同，数字也包含调度／重日志开销，不用少量样本宣称稳定加速百分比。全录像颜色筛选为开启153帧中23候选、关闭115帧中25候选，变量帧率且含缩小APP，不能据此相减得出闪现时长改善。

### 处置和剩余边界

本原型不能作为免ROOT闪回修复发布，已归档并撤回。`LauncherHomeCompat.java`与`SMGLSurfaceView.smali`恢复本轮前逐字节副本，保留已有dirty改动；`HomeTextureHost.java`移至`build/home-texture-window-20261013/retired-candidate/`，正式源码不保留无收益实验分支。虚拟机恢复4944E9…原APK、手势mode2，实验属性恢复空值；没有清数据或改主题、壁纸、默认桌面。

保留的工作区变更是采集脚本`--host-layer window`，用于允许真实画面位于主窗口的样本准备，并记录实验日志；默认仍检查SurfaceView。数据并入`HOME_RETURN_EMULATOR_20261013.json`的`texture_main_window_experiment`，本地[开启录像](../../build/home-texture-window-20261013/window-host-on/video.mp4)、[关闭录像](../../build/home-texture-window-20261013/window-host-off/video.mp4)、trace、时序和源码归档可复核。

结论只到：在当前虚拟机这条系统手势路径中，消除独立SurfaceView同步并把桌面放入主窗口仍不足以消除露底；不能据此宣称所有免ROOT适配无解，也不能继续承诺“重构宿主就能修好”。OPPO Android12、vivo9/16、透明／毛玻璃、60–144Hz、长期GPU资源与耗电未测本原型。正式闪回修复仍未完成，MEMORY未更新。

收尾校验：撤回后标准构建、v1/v2/v3签名和16KiB对齐通过。最终本地APK SHA256为`8D2D77B67283A9BC81D08E9AF6D215596E1B91B7EA558168066ECE8FB027DD56`；ZIP各条目内容与本轮前APK逐项一致，整包hash因重新构建不同。Python采集脚本语法、证据JSON与diff检查通过。最终本地包未覆盖虚拟机已恢复的4944E9…包。

## 13. Nova 与 Smartisan 的同机早段图层对照：缩小图标协议不能单独修复露底

在不再操作实体 OPPO 的前提下，重新计算本地保存的 `nova-fixed-gesture` 和 `main-probe-gesture` 三轮 SurfaceFlinger 采样。两组均为 OPPO PDCM00 / ColorOS 12.1、系统手势 mode=2、组内同一 APK／PID。时间原点都是各轮 ADB 返回输入前的 `actions[].boot_ns`；两组 Launcher APK 不同，也没有对齐实际手指触点或显示面板 present fence，以下仅比较系统交接形态。

| 桌面／轮次 | Wallpaper 有可见区域、HOME 像素图层尚无可见区域的采样窗口 | 首个 HOME 像素图层可见采样窗口 |
|---|---|---|
| Nova 0 | 330–420ms | 510–550ms |
| Nova 1 | 280–320ms、380–430ms | 480–510ms |
| Nova 2 | 190–240ms、310–380ms | 450–490ms |
| Smartisan 0 | 270–380ms | 500–530ms |
| Smartisan 1 | 260–320ms、390–440ms | 500–530ms |
| Smartisan 2 | 220–260ms、330–380ms | 470–510ms |

Nova 的 HOME 主窗口层为 `NovaLauncher#0`，Smartisan 的 HOME 像素层为 `SurfaceView[smt_launcher](BLAST)#0`。上述 Wallpaper 采样都有 `[0,0,1080,2400]` 可见区域；多数采样同时有系统 `RecentsActivity` 图层，因此不能把可见区域误称为“满屏纯壁纸画面”或精确闪回时长。Nova 第2轮 index84 的采样只有 Wallpaper 图层可见。Nova 在用户录像中的**视觉体验正常**，这一判断不因底层 Wallpaper 参与合成而改变；它的桌面背景与系统 Wallpaper 一致，使同一类交接不一定形成可察觉的背景跳变。这是结合用户视频和图层的解释，不是逐像素证明。

两组的 HOME 首可见采样均在约450–550ms，Nova 并未在这批样本里稳定早于 Smartisan 提供完整 HOME 图层。更重要的是，Smartisan 三轮 `gesture_nav_contract_v1` 到达分别为386.201／378.752／369.589ms，晚于各轮至少一个 Wallpaper 可见、HOME 不可见采样。因此只在接到合同后回复目标图标位置、图标 Surface 与 finish callback，不能倒过来覆盖已经发生的早段曝光。系统侧 [FallbackSwipeHandler](https://github.com/OpenSmartisanOS/android_packages_apps_Launcher3/blob/9222aa7dc53edcd84e7d7d1f5ff65706f622bf1b/quickstep/src/com/android/quickstep/FallbackSwipeHandler.java) 使用回复更新收拢目标及可选图标 Surface，并在动画结束时发送 finish；这个合同本身不向第三方 HOME 授予提前显示主窗口或改变 Wallpaper／Recents 图层的控制权。

另核对启动预览假设：原版与当前 Launcher Activity 都引用 `LauncherActivityTheme`，其父主题是 `Theme.DeviceDefault.Wallpaper.NoTitleBar`，并设置 `windowDisablePreview=true`。AOSP 的 [ActivityRecord 启动窗口规则](https://android.googlesource.com/platform/frameworks/base/%2B/a42e14ce6379/services/core/java/com/android/server/wm/ActivityRecord.java) 对 HOME 快照启动窗口限定为直接解锁使用；Wallpaper、translucent 和 preview 属性还参与启动窗口资格判断。这是平台参考，不证明 ColorOS 12 的私有改动逐字相同，但已经不能依据“把 `windowDisablePreview` 改成 false 就能在原生手势前段显示完整 HOME 快照”的猜测改原版主题。10月13日主窗口Texture实验也表明，把像素移到普通主窗口后仍要等系统显示 HOME；因此不再做无证据的窗口属性试错。

**施工决策：**暂停把完整图标协议移植当作“消除壁纸闪回”的主修复。它可能改善后段图标收拢，若将来有独立图标动画需求可单项实验，但现在没有证据支持为了早段闪回引入新图标 Surface、缓存图标重绘和额外生命周期。当前经同机同包验证的免ROOT规避方式仍是实际三键 HOME；普通 APK 的原生手势零闪回仍未交付。也不因此全局改主题为系统壁纸或启用常驻遮罩。

本节为离线复核，无新 APK、源码或设备测试；未变更 OPPO、vivo 或虚拟机状态。采样源：`build/home-coloros-audit-20261012/{nova-fixed-gesture,main-probe-gesture}/{samples.json,sf-timeline.json}`。若未来找到可让第三方 HOME 在 ColorOS 手势前段参与合成的受支持入口，需重新用同机、同主题、双导航和真实录屏／WM／SF时序验收；当前不能宣称所有 ROM 不可能修复。

补充视觉复核：保存的 `nova-record-reference` 第一次返回录像中，PTS4.242／4.307／4.373／4.441s可见森林背景与缩小APP，尚未见Nova的其余桌面图标；PTS4.523s可见Dock和桌面图标。背景连续是这个正常样本的一项明确差异，不能把它标为“用户看见Nova闪回”。这些录像PTS没有与另一批SF采样绝对对齐，也不证明Nova正常的唯一原因是壁纸相同，或其他桌面都使用同一方法。本地逐帧图为 `build/home-draw-sync-20261013/nova-first-return.jpg`。

## 14. 窗口绘制交接：两种最小候选已实施，虚拟机未消除闪回

按用户“按照第一条实现”的授权，复用当前 `LauncherHomeCompat` 与 `SMGLSurfaceView`，逐项处理窗口重绘交接；只操作已授权的Android16虚拟机。当前、clean原版与maintained的Surface宿主都沿用平台GLSurfaceView绘制通知，没有发现原代码直接调用WM私有finishDrawing或固定延迟。平台[GLSurfaceView源码](https://android.googlesource.com/platform/frameworks/base/%2B/master/opengl/java/android/opengl/GLSurfaceView.java)存在两个可测试等待点：重绘finish回调在Renderer返回后、EGL swap之前执行；主线程onWindowResize等待GL完成一次尺寸更新绘制。它们是候选机制，不能仅因存在就认定为OPPO闪回根因。

候选H1：只把有效Surface重绘完成通知排入下一次GL循环，置于本次swap尝试之后；Surface销毁／分离／替换、无新帧和重复重绘请求按世代收尾。候选H2：保持原尺寸处理，改为在GL队列调用同一个super.surfaceChanged；平台检测到自身GL线程后不等待，让主线程及时发出异步重绘请求。没有提前伪造finish回调、固定等待、强制多渲染一帧、修改SMEngine、窗口格式、系统壁纸或动画时钟。

两候选均默认关闭，通过实验log tag单独激活，H2测试时H1关闭。H1同一APK `D3CA8987…`、同PID10772，前后各3次；H2同一APK `EFDEB623…`、同PID13251，前后各3次严格APP→HOME。H2另有一轮中途出现overview控件，作为辅助样本单列；两个未真正回HOME的注入手势排除，不计PASS／FAIL。每轮采样前等待2秒仅为测量隔离，未加入产品恢复路径。原始APK、150项确定性异步／取消测试、源码、Perfetto、录像和无效输入都保留在 `build/home-draw-sync-20261013/`。

以Resume=0，单位ms。数据是trace／图层采样，均不是显示面板present fence：

| 组别 | 实际重绘finish通知（3轮） | 首桌面buffer图层可见（3轮） | 视觉结果 |
|---|---|---|---|
| H1原顺序 | 287.687／241.174／286.615 | 392.137／353.658／469.432 | 3/3露系统壁纸 |
| H1交换尝试后 | 315.187／269.658／316.329 | 432.746／419.417／421.964 | 3/3仍露壁纸 |
| H2原尺寸回调 | 302.382／258.934／268.961 | 473.918／373.210／448.913 | 3/3露系统壁纸 |
| H2异步尺寸处理 | 246.248／217.403／203.244 | 423.286／455.689／390.735 | 3/3仍露壁纸 |

H1确实改变了顺序：三轮对应swap结束为314.454／269.349／316.034ms，finish位于其后；但窗口仍要等后续显示。H2尺寸callback到REDRAW_REQUEST的采样间隔从126.821／96.235／103.015ms变为0.467／0.737／1.982ms；这个间隔包括主线程上的其他Surface工作，不等于精确的单个方法耗时，也不能据此宣称整体HOME加速百分比。GL队列仍需要处理尺寸／EGL输出，完整桌面未连续参与手势前段合成。两组均未出现新Context或scene重建；没有把普通恢复改为冷初始化。

**最终处理：**两项行为候选未达到闪回修复目标，已归档到 `candidate-source/`，不作为正式补丁启用。正式代码只保留默认关闭的 `traceSurfaceRedraw`，标记请求、平台回调开始和结束，原Runnable原线程原时机执行；没有等待、回调门控、尺寸队列或实验开关。虚拟机已恢复测试前4944E9…APK、手势mode2及原实验属性；实体OPPO／vivo未安装或切导航。150项测试适用于已归档候选，不冒充正式诊断逻辑的视觉验收。

最终诊断包标准构建、v1/v2/v3签名、16KiB对齐通过，SHA256 `F8FCA1DA268FD5A2D5B489CFAB4055AB9CF6B0CDC4242A330A4282E68981710F`，未安装到实体机或覆盖已恢复的虚拟机。DEX核对确认不含两实验tag，仅保留重绘诊断入口。证据并入 `HOME_RETURN_EMULATOR_20261013.json` 的 `surface_draw_sync_experiment`。OPPO Android12上这两个候选、vivo非退化、透明／毛玻璃、真实解锁／最近任务／快捷桌面、60–144Hz和长期GPU／耗电未验收；当前仅能判定这两种机制单独不足以消除本虚拟机闪回，不能宣称所有窗口交接修复无效。MEMORY未更新。


## 15. 用户授权的同源壁纸方案与选图生效优化（2026-10-13）

本节依据用户最新明确要求自动切换系统壁纸。它取代此前“不写系统壁纸”的施工范围限制，不把历史失败实验重新标为通过。最终包为 `build/home-background-sync-20261013/final.apk`，SHA256 `6C8E357488FCF9DEADDA1481C6BB563F6356521D0D3A83BFFEC7C271B69AEE44`；同内容正式输出 `build/launcher-signed.apk`。结构化证据见 `HOME_BACKGROUND_SYNC_20261013.json`。

### 根因与采取的改动

1. 手势交接中，系统Recents可先显示Wallpaper，完整GL桌面稍后才可见。此前普通主题只更新自身背景，与系统壁纸不同，形成显著异图跳变。Nova保存录像显示同源背景的连续交接，但这不是Nova全部实现的证据，也不是系统窗口控制权变更。
2. 选图旧链路先复制原图、解码并重编码大PNG、生成缩略图，再通知原版桌面。新链路先后台保存原图并提交现有URI拥有者，立即排入原版场景刷新，再做兼容副本、缩略图和系统写入。选图锁与系统写入锁分离，系统Binder耗时不再阻塞下一张图片提交；最新选择序号淘汰过期任务。
3. 第一版自动同步在API36触发Monet/资源assets配置更新，事件日志明确出现 `wm_relaunch_resume_activity ... 80000000`，原版onDestroy随后SIG9杀进程，造成冷加载。最终二进制HOME Activity在原有效 `0x00003fff` 上仅增加 `CONFIG_ASSETS_PATHS`，变为 `0x80003fff`；文本Manifest同步有效值。经普通Black/Blue/Aero切换、选图和默认恢复，同PID保持。没有修改原版SMEngine或杀进程逻辑。
4. 透明主题包background.png为全透明覆盖层，不是默认壁纸。无自选图片时使用原版保存的底层主题对象 `X.fa(previousTheme)` 的真实资源；自选时仍使用现有原图URI。Android14+不能稳定读回系统壁纸，因此在原设置宿主中后台准备一个默认源文件供现有渲染URI入口读取，自选URI独立保留。未把透明主题ID写入普通主题设置队列。

普通主题读取原版 `X.eg().mResources + mPath + pb.path("background.png")`，按原版全窗口背景尺寸输出。自选壁纸复用现有解码与居中裁切；毛玻璃效果继续由原链路处理，系统写入的是原图背景，非含图标/宫格/Dock的截图。普通主题不会误用之前保存的自选图片。

所有入口最终通过既有原版主题状态栏回调 `e/s -> e/g -> LauncherSettingBridge.applyDesktopStatusBarAppearance -> ensureThemeSystemWallpaper` 读取当前生效主题，包含原版四指切换的共享主题链路，未添加平行主题Manager/Service。相同会话键直接返回，源内容指纹与系统Wallpaper ID避免重复写入；普通APP→HOME不会新排壁纸任务。原版 `M` 壁纸广播接收器原样保留，避免破坏毛玻璃、明暗及原版主题更新。

参考 maintained 的 `data/Utils.syncSystemWallpaper` API24+仅写 `FLAG_SYSTEM`，并避免它异常后可能干扰现代锁屏的legacy回退。复用当前双线程主题执行器，无主线程图片复制/压缩/Binder写壁纸，没有固定等待、常驻全速渲染、全局不透明Surface或额外全屏遮罩。OpenSmartisanOS的FallbackSwipeHandler合同适用于收拢目标/finish回调，不授予第三方HOME提前显示窗口的权限；既有返回合同代码保留，未移植系统Quickstep权限路径。Nova仅借鉴有证据的连续背景交接，不声称复刻闭源实现。

### 有效验证与排除样本

| 场景 | 最终包结果 | 边界 |
|---|---|---|
| Android16虚拟机，Black普通主题，手势APP→HOME | 前一候选3/3到HOME，同PID25438；最终包两次有效HOME，同PID28444；均未露出原先蓝色系统壁纸；零新增壁纸任务/冷场景创建 | 最终组另一轮回到Settings，排除；仍有只有背景、完整图标晚出现阶段 |
| 同机Black→Blue→Aero普通选择 | PID25438不变，系统Wallpaper ID15→16；背景随主题更换 | 实测这三个主题，不代表全部主题资源/ROM |
| 同机透明默认 | 使用保存底层Black，系统ID12；桌面灰色背景正确，排除了全透明资源写成黑底 | 透明开关保留既有冷重载，不能与普通返回的同PID要求混淆 |
| 同机透明选图→恢复默认 | 选图系统ID13，恢复底层Black ID14；选图PID24812不变 | 一次有效选图；恢复采用原版入口 |
| 同机Aero选图 | 选图系统ID17，同PID25438；录像新背景在系统写入完成前已可见 | 一次有效选图；不是零处理时间/不卡顿的全面验收 |
| 同机Aero自选背景手势返回 | 两次到HOME，同PID；背景仍为所选Blue原图，无旧Aero默认图片曝光 | 第一轮回到了Settings，排除；原版格线/毛玻璃与系统原图可能有亮度/模糊差异 |
| 四指横滑 | 静态接线检查，复用同一原版主题回调 | 未做实际多指输入，不写成真机通过 |
| vivo9/16、OPPO12 | 沿用前述历史矩阵 | 最终包未安装/测试实体手机；按用户要求不再要求连接 |

选图时序：透明样本176ms提交、191ms请求场景刷新，系统ID13于15:20:52.644完成；Aero样本167ms提交、182ms请求刷新，ID17于15:27:23.406完成。系统完成分别距源提交约3.65/3.51秒。录像确认新桌面背景先于系统完成出现，但刷新请求不是屏幕呈现时刻，不能把182/191ms宣传为视觉生效时间；也没有同设备同图旧包逐帧选图耗时对照。旧阻塞阶段已移出刷新关键路径，超大图、不同格式、低性能机仍需实测。

静态实际拥有者47项断言通过，涵盖API23/24/28/31/34/36、普通/Aero/透明源、透明默认排除alpha覆盖、同源去重、过期任务和写入中更新、权限拒绝、现代系统不回退锁屏API、普通返回不排任务、平板路径保持。构建、签名验证、16KiB zipalign和最终AXML检查通过。缓存文件I/O与图层视觉以虚拟机记录补充，离线替身不是ROM验收。

`final-aero-pick` 是坐标点错图片的无效样本，采用 `final-aero-pick-verified`；`delivery-aero-selected-gesture` 使用了失效参考模板，不能当通过记录。`switch-black-blue` 属于修复assets配置前的失败包，不与最终包混称。

### 前后窗口/帧时间线（毫秒，相对每次RESUME_BEGIN）

| 样本/轮次 | onResume结束 | Surface创建 | SF首个“有buffer且可见”采样 |
|---|---:|---:|---:|
| 修改前Black 1 | 35.138 | 105.400 | 507.970 |
| 修改前Black 2 | 3.203 | 66.434 | 383.784 |
| 修改前Black 3 | 6.333 | 97.755 | 422.632 |
| 前一候选Black 1 | 34.900 | 98.820 | 721.560 |
| 前一候选Black 2 | 6.662 | 38.834 | 692.398 |
| 前一候选Black 3 | 4.122 | 85.637 | 945.739 |
| 交付包Black有效返回1 | 2.592 | 63.217 | 634.425 |
| 交付包Black有效返回2 | 8.229 | 47.334 | 620.795 |

最终样本未显示完整HOME更早可见，不做性能加速结论。这批是有诊断/录屏的不同运行批次；上述SF时刻为采样边界，不能等同精确屏幕呈现。JSON中的自动提取 `actual_surfaceframe` 有Background辅助层，不足以证明完整GL桌面首帧；GL/onDraw结束也不是呈现证据。普通主题录像逐帧复核支持“先前异色背景不再出现”，尚不支持“窗口交接空档完全消失”。

### 变更范围与剩余验收

本方案修改设置宿主、LauncherSettingBridge、文本/保留二进制Manifest；新增最小AXML补丁工具与47项源/写入测试。已有HOME诊断代码和之前未提交内容保持；SMEngine及壁纸广播接收器未修改。未改 `FLAG_SHOW_WALLPAPER`、Surface透明性、帧率或解锁逻辑。

普通不ROOT手机具备SET_WALLPAPER权限且系统允许设置时可以执行；受策略限制时明确提示同步失败，保留主题，不无限重试。API24+仅写系统壁纸；较早API的legacy系统行为需单独回归。系统Recents的缩放/调暗、毛玻璃与透明原图的差异，以及完整图标较晚出现仍可能造成可见变化。待验：OPPO实际手势和三键、vivo9/16非退化、锁屏解锁、最近任务、快捷桌面、连续实际四指、全主题/超大图、60–144Hz和后台内存/GPU/耗电。无新增系统呈现证据不声称所有ROM完全解决。

最终核对：设备拉回base.apk、最终归档final.apk与build/launcher-signed.apk三者SHA256一致。虚拟机恢复普通Black、清除本轮自选测试图片、移除本轮临时透明主题包与上传图片，保留修复包；诊断/Surface实验设置已由采集器恢复。未操作实体手机。

包与证据最终收口：前一候选F784CDBF...716F4的选图/Aero/Black录像保留，归档为final-before-ui-thread.apk；交付6C8E3574...AEE44仅再将默认恢复的原版场景通知放回MAIN，新增delivery-aero-default、delivery-restored-black与delivery-final-black-gesture记录。默认恢复和切回Black保持PID28444，Wallpaper ID20→21；最终手势组两次到HOME，第一轮回到Settings排除。47项断言和构建签名再次通过，未将前一候选录像冒充交付包录像。

## 16. 2026-10-14：图标随后出现与两条返回路径的证据收口

用户要求的是完整桌面在APP缩小过程中参与过渡，而非动画结束后突然补出图标。切换主题同步系统壁纸仅改善背景连续性，不能按此标准称为修复完成。

此前第11节已有同包、同PID的手势与HOME键差异，OPPO也有实际三键对照。此次只新增前四帧的场景节点只读诊断；重复采集返回路线没有形成行为修复。按用户纠正停止重复测试，撤回临时诊断源码，并将虚拟机恢复本轮前的备份/壁纸功能包。没有操作实体手机，没有改原版SMEngine。

诊断包SHA256 `8B6C0BE5C0C8209853AA99219EFFF24B5644A01700D23E20AE3B67514851EACE`；两组均navigation_mode=2、PID4380，各3次确实到HOME。HOME键组是ADB替代输入，不冒称切换三键导航。数据与录像位于 `build/home-animation-handoff-20261014/`，结构化结论为 `handoff-evidence.json`。

| 路线/轮次 | 首次GL绘制结束 | 首次采到有效buffer但隐藏 | 首次采到有效buffer可见 |
|---|---:|---:|---:|
| 手势1 | 72.064ms | 136.018ms | 330.292ms |
| 手势2 | 117.211ms | 189.115ms | 460.595ms |
| 手势3 | 125.096ms | 172.896ms | 410.402ms |
| HOME键1 | 75.174ms | 148.797ms | 294.952ms |
| HOME键2 | 35.381ms | 66.186ms | 221.187ms |
| HOME键3 | 58.174ms | 93.864ms | 258.966ms |

均相对本轮RESUME_BEGIN，SF值是采样边界，不是物理屏幕呈现时刻。有效buffer为1080×2400的GL BLAST层，排除了Background辅助层。隐藏链从SurfaceView到`smt_launcher`、ActivityRecord及任务父层；其中HOME窗口和ActivityRecord明确有`flag is hidden`。两组都存在buffer先到、父层仍隐藏的阶段，不能仅以隐藏阶段存在来解释导航差异；录像还显示手势缩小先暴露背景，而HOME键退出时桌面随窗口过渡露出。

首帧当前页及祖先`isVisible=true`、scaleX/Y=1，直接子节点可见；场景与EGL Context未重建，原版launch flip关闭。这些排除了已检查节点的显式隐藏/缩放等待，但不证明每个图标纹理像素完整。临时诊断中的`alphaProduct=0`作废：SceneNode.getColor读取材质颜色，无材质分组节点不能按继承透明度相乘，不能据此修改alpha。没有将GL绘制结束当作呈现。

**修复状态仍为未解决完整桌面提前参与手势过渡。** 当前没有证据支持通过改页切换动画、给HOME Intent补FROM_HOME_KEY或在onResume重发HOME，把已运行的系统Recents手势转换成三键返回。下一候选必须指向尚未验证的具体交接机制，并先说明与第10–14节已撤回实验的区别；不再重复同类采样或把背景同步当作完整修复。此记录不证明所有ROM都受系统限制，也不否定有依据的应用侧修复可能。

## 17. 2026-10-14：免ROOT开源方案检索与可实施的替代返回路线

本轮按用户要求联网检索并读源码，未重新采集设备时序、构建或安装APK。主包仍为本轮开始时的C0BEDCEE…69A00，Launcher/SMEngine/Manifest未改。以下是候选机制的适用性结论，不能填入设备PASS矩阵。

### 开源桌面实际提供的机制

| 来源及定位 | 已读到的实现 | 对本问题的适用性 |
|---|---|---|
| [Lawnchair手势故障说明](https://github.com/LawnchairLauncher/docs/blob/main/help/troubleshooting/gesture-navigation-issues.md)；[FloatingSurfaceView](https://github.com/LawnchairLauncher/lawnchair/blob/85335d904a1c8b9790e40c581226684c59166297/src/com/android/launcher3/views/FloatingSurfaceView.java) | 官方记录桌面内容晚出现及OEM差异；免ROOT用GestureNavContract。该View绘制目标图标，并回复图标位置/Surface。 | 可借鉴单图标收拢和收尾；没有提供提前显示整个HOME窗口的应用侧入口。不能把其中避免图标闪烁的单帧移除等待移植为桌面等待方案。 |
| [Neo FloatingSurfaceView](https://github.com/NeoApplications/Neo-Launcher/blob/bc028ddd7737277d2817baba9e768cdbade7b4ff/src/com/android/launcher3/views/FloatingSurfaceView.java) | 同样按目标图标边界绘制、回复Surface、恢复原图标。 | 核对文件未找到覆盖早段完整桌面交接的额外协议，不把同源Launcher3实现重复计为新修复。 |
| [OpenSmartisanOS FallbackSwipeHandler](https://github.com/OpenSmartisanOS/android_packages_apps_Launcher3/blob/9222aa7dc53edcd84e7d7d1f5ff65706f622bf1b/quickstep/src/com/android/quickstep/FallbackSwipeHandler.java) | 系统Recents端创建HOME动画，设置HOME目标alpha、接收task appeared，再应用显示/缩放；第三方合同回复只更新收拢目标和finish消息。 | 具体显示控制在Recents端。把此文件复制进普通APK不会获得当前ROM的远程动画目标。AOSP参考不能认定为ColorOS12私有实现的逐字根因。 |
| [HyperGesture](https://github.com/h3nc4/HyperGesture/tree/b6928e8c00a74398e83cfd4492af7c5c84872786)；[GestureActionPerformer](https://github.com/h3nc4/HyperGesture/blob/b6928e8c00a74398e83cfd4492af7c5c84872786/app/src/main/kotlin/com/h3nc4/hypergesture/service/GestureActionPerformer.kt) | 窄边缘无障碍触摸窗口识别手势，Home映射至performGlobalAction(GLOBAL_ACTION_HOME)。README要求Android11+，作者只列Redmi14/Android16实测。 | **新增可实施候选：替代手势触发按键式HOME**。不需要ROOT；OPPO12可用性、视觉效果、误触及后台稳定性未验。不能把其他机型的导航可用证明成本机无闪回。 |
| [Launcher Lag Guard](https://github.com/fabien0008/launcher-lag-guard) | 首次解锁后用无障碍移除系统桌面最近任务卡；作者仅验证RealmeGT6/Android16三键导航。 | 针对重启后的任务残留/返回延迟，尚无手势验收；不是当前OPPO12手势闪壁纸的现成补丁，不自动清理系统桌面任务。 |

maintained的`smali/com/smartisanos/home/Launcher.smali`仍使用SMGLSurfaceView、保留EGL Context和SMEngine；没有因此获得系统Recents控制权。其已有系统壁纸同步已在第15节借鉴。[SmartisanWeather-Revived](https://github.com/Mangi-11/SmartisanWeather-Revived)是普通天气应用的Compose复刻，其界面迁移不提供HOME/Recents交接权限，不能据此保证Launcher改成Compose即可修复。

### “手势走虚拟键路线”的正确实施位置

这条路线的关键是**在系统原生手势动画开始之前，用替代输入触发HOME动作**；不能在Launcher接到onResume后再补HOME。具体流程：

1. 系统选择三键导航，保持Smartisan为默认HOME，避免原生底部手势与替代识别器同时处理一次触摸。
2. 用户主动开启可选无障碍导航组件，窄边缘区域识别上滑。
3. 手势确认后只调用一次`performGlobalAction(GLOBAL_ACTION_HOME)`；失败明确反馈，不重发HOME、不重建场景。
4. 系统执行HOME动作，继续使用现有Smartisan热恢复链。

平台依据：[Android12 SystemActionPerformer](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-12.0.0_r1/services/accessibility/java/com/android/server/accessibility/SystemActionPerformer.java)的默认HOME动作发送KEYCODE_HOME；[SystemUI SystemActions.handleHome](https://github.com/aosp-mirror/platform_frameworks_base/blob/android-12.0.0_r1/packages/SystemUI/src/com/android/systemui/accessibility/SystemActions.java)的注册动作也发送HOME按键。调用方使用公开无障碍API，由系统执行受控动作，并非给Launcher授予INJECT_EVENTS。[API说明](https://developer.android.com/reference/android/accessibilityservice/AccessibilityService#performGlobalAction(int))。ColorOS可以替换注册动作，仍须核验实际路线。

**这一机制比继续修改GL恢复参数更贴近已有“三键正常”的证据，但当前只是有源码依据的候选规避方案。** 它不保留原生随手指缩小APP的交互，会采用系统HOME动作对应的返回效果；无障碍HOME也不自动保证每个ROM逐帧等同屏幕虚拟键。按键导航栏可能继续占空间，隐藏导航栏是另一项ROM能力，不能承诺普通APK自动隐藏。边缘窗口会影响部分边缘点击，需要有可关闭入口与误触/键盘/横屏回归；不需要常驻全屏图像遮罩或后台全速GL。

如落地，应先用独立可选导航组件验证这一个新输入机制，确认有效再评估是否并入设置。当前项目无现成AccessibilityService，组件需求来自APP在后台接收全局边缘输入，不能让原HOME Activity冒充全局手势拥有者。HyperGesture采用GPL-3.0，不能未经许可评估整块拷入当前工程；可以先独立使用或依据公开Android API实现最小功能。主包未自动新增服务/权限。

Shizuku/ADB还可在获授权后执行HOME按键，但也需要替代手势入口，并不能单独把正在运行的原生Recents动画变为三键。切换Recents提供者的QuickSwitch及ROOT模块属于另一权限路线，不列为免ROOT补丁。

**当前选择：**若接受替代手势和按键式返回，已有可落地的免ROOT方案方向；若必须保持ColorOS原生跟手动画且完整桌面提前出现，本次核对的开源代码仍未提供经本机验证的应用侧补丁。Nova维持正常参照，未将其闭源行为冒称为已复刻。本轮只更新此文档和DEVELOPMENT_LOG，未更新MEMORY.md。

## 18. 2026-10-14：Nova实际APK反编译与Android8–16适用边界

**项目兼容目标是Android8–16，OPPO12只是故障样本。** 本节直接核对保存的同机Nova8.0.18 APK，SHA256 `262535B90196C651557C1B63D78B80F06D80434DD4E8AA9706639B1E5E9E630B`，不只引用开源桌面的相似代码。重新解码资源/Manifest至`build/nova-handoff-audit-20261014/decoded/`，逐项读取既有完整smali。11个关键方法的源码hash/行号和HOME属性记录于同目录`code-evidence.json`。未重新采集、安装或改变手机导航；生产源码及主APK未改，主包仍C0BEDCEE…69A00。

### 入口、窗口与恢复

- HOME是`com.teslacoilsw.launcher.NovaLauncher`，依次调用`w6/h2.onNewIntent`；主桌面为`LauncherRootView → DragLayer → Workspace`普通View树。Nova中存在GL类不等于整个桌面使用GLSurfaceView，不能用壁纸选择器的GLRootView替代主桌面判断。
- 主主题从`AppTheme → LauncherTheme → BaseLauncherTheme`继承透明窗口背景及SHOW_WALLPAPER。`resumeWhilePausing=true`、singleTask、clearTaskOnLaunch、stateNotNeeded等在当前Smartisan已有对应配置，不能再把这些当缺失补丁。运行时主题有切换分支，不能把Manifest默认主题等同所有会话生效值。
- `z7/g.onResume`提交异步MAIN消息到`q0`恢复状态；`w6/h2.onWindowFocusChanged`仅记录焦点时间。`NovaLauncher.Z0`取消自身circle动画、恢复DragLayer进度0。普通热返回不会因此重新创建整个Workspace。Smartisan已经复用J/Eb/Context，尚未发现可通过照搬该Handler消除父窗口隐藏的依据。

### 实际图标合同，不是完整桌面Surface

`w6/h2.onNewIntent`在API30+及用户开关允许时消费`gesture_nav_contract_v1`，验证component/user/message/replyTo。随后创建`FloatingSurfaceView`：

1. 按应用及用户查找当前目标View，取得真实图标边界。
2. 用Picture记录该图标的显示，临时隐藏原图标；Surface尺寸是图标宽高。
3. 通过`FloatingSurfaceView.Z`回复图标位置、SurfaceControl和finish Message；`w6/d1.handleMessage`收到结束消息后关闭图标浮层、恢复原图标。
4. API≤30的合同宿主另走WindowManager应用面板分支；API31+加入DragLayer。Android8–10没有进入此合同分支，不能向旧版本无条件加载SurfaceControl链。

当前Smartisan的`LauncherHomeCompat.inspectGestureContract`只是诊断，未实现以上完整Surface/finish链。它是明确功能差异，但本项目第13节已有早段曝光先于合同到达的证据；完整图标合同可改善目标图标收拢，不能据此声称解决所有图标晚出现。之前位置回复A/B也不等于已经实现Nova完整协议。Nova关闭图标Surface时的短暂移除等待属于局部收尾，不能复制成全桌面固定等待。

### 新追到的Oplus壁纸策略与条件绘制

**明确的厂商策略：**`fh/l.<clinit>`检测`oplus.R`，写入`fh/l.h`；`uf/d3`中`wallpaper_zoom_effects`（索引0x2c）的默认值取反，因此检测到Oplus时默认关闭。`NovaLauncher.onCreate`、`w6/y5`状态转换读取该值，经`ph/g`版本门面调用API30+的`ph/m/ph/l`壁纸zoom传输。该实现使用WindowSession内部Binder事务，值与状态约定必须完整理解，不能直接理解为普通Surface alpha或把数值1改成0。

当前Smartisan相关源码未找到主动调用这一zoom接口；“Nova主动固定zoom状态”与“Smartisan未调用”不是严格等价，但也不能据此认定加同一调用就能提前显示整个HOME。没有保存Nova会话的该偏好实际值；静态默认不能证明录屏时此分支生效。隐藏API、Binder事务号及系统私有修改存在版本边界，不在Android8–16主包中硬编码事务号或反射绕过。

**另一个条件分支：**`Workspace.a1`读取`wallpaper_scrolling_force`（索引0x2b，默认false）。开启、静态壁纸可读且图片宽于Workspace时，保存BitmapDrawable，由`DragLayer.dispatchDraw`按偏移/裁切绘制壁纸，再绘制桌面内容；`w6/g5`同时切换主Window格式为OPAQUE并清SHOW_WALLPAPER。条件不满足则清理副本，恢复TRANSPARENT及SHOW_WALLPAPER。它调整的是主Window及普通View绘制，不是全局把SurfaceView改为不透明，也不是常驻桌面截图。

这补充了“Nova仅使用系统壁纸”的过度简化：Nova确有主动绘制静态壁纸的条件实现。但默认false、缺实际会话偏好，不能当作正常样本的确定原因；Android14+第三方读回系统壁纸也有权限限制。Smartisan自身已绘制主题背景，并已按用户授权同步系统壁纸，不能重复新建壁纸缓存或无条件清SHOW_WALLPAPER。透明/毛玻璃继续保留各自语义，主窗口的透明与内容完整性需单独验证。

### 对项目的借鉴结论与版本门

| Android范围 | 施工边界 |
|---|---|
| 8.0/8.1–10，API26–29 | 保留原J/Eb/SMEngine和标准HOME恢复；不执行不存在的GestureNavContract/zoom接口。Nova此APK最低API27，不提高本项目Android8.0门槛。 |
| 11–13，API30–33 | 仅在实际收到有效合同时讨论图标Surface/finish链；Oplus的zoom策略可作为独立背景动画候选，尚无整桌面闪回修复证据。OPPO12样本不代表全部ROM。 |
| 14–16，API34–36 | 同样保持能力检查；不假设可读系统壁纸，不恢复失败的attachment/Texture实验为默认。保留本项目自选/主题原图拥有者；API34新接口隔离加载。 |
| 正常vivo9/16 | 继续作为非退化基准；本次未安装，不能填写新补丁回归PASS。 |

可以借鉴的合同、窗口内容一致性、版本隔离均已指向具体代码；当前没有确定一个能够单独解除早段HOME父窗口隐藏的Nova调用，因此本轮不盲目新增Handler、全局窗口格式/zoom反射或宣称已修复。此前主Window Texture原型失败也不能被重命名为新方案。后续若做完整合同，验收应限于其真正改善的收拢/收尾阶段，并另验早段完整桌面；若做主题级主窗口策略，需要首先证明该条件在异常样本上生效。**Nova同机正常这一基准保持，Android8–16修复目标保持，根因补丁仍未交付。**

本轮更新本节及DEVELOPMENT_LOG；未更新MEMORY.md。解码器对较新框架属性有未解析警告，仅用于此APK资源/代码审计，不拿解码结果重打包Nova，不分发其反编译实现。

## 19. 2026-10-14：Nova壁纸zoom策略实际A/B，未得到可靠缩短

用户授权先实验，接受可靠的部分缩短。本轮只检验第18节新追到的壁纸zoom机制，未重复attachment、Texture宿主或重绘通知实验。目标仍覆盖Android8–16；仅当前已连接Android16虚拟机可实测，不要求用户重新连接OPPO。

### 最小实验与生效证明

复用`LauncherHomeCompat`增加默认关闭的诊断分支，API26–29直接跳过；API30+在已有HOME窗口有效时，将其zoom请求置为Nova“关闭缩放效果”所用的1，关闭实验恢复0。没有写壁纸图片、改SMEngine/主题/Surface格式/动画时钟或增加服务、遮罩、后台渲染循环。未做独立的图标Surface协议和主窗口壁纸绘制候选，不能据此评价Nova全部方案。

第一版直接反射`IWindowSession.setWallpaperZoomOut`被API36 hiddenapi拦截，出现NoSuchMethodException，WM仍为0。该版DE83711A…3D614的采样不作为效果对照，亦未将“没有变化”解释为策略无效。首次安装后的黑屏准备截图也不算热恢复视觉样本。

随后按Nova实际传输形式做受控候选：测试工具从**当前设备**`IWindowSession$Stub.TRANSACTION_setWallpaperZoomOut`解析出编号，作为临时ADB诊断参数；普通Launcher进程取得自己的WindowSession，验证接口descriptor后，用自己的窗口token发送原AIDL字段。源码没有硬编码编号、修改hiddenapi策略或使用ROOT服务。此参数解析是诊断夹具，**不是已经完成的独立APK跨ROM运行时解析器**。

有效候选APK SHA256 `4AA4982A514DC9B1EB0E4A9E54F01859977021F8F558282FAA4FD71F80BEF9B6`。安装后先等待实际完整HOME并确认截图，再按关闭A→开启B→关闭A2采样；全过程同PID9131、navigation_mode=2、Context/scene不变，系统WindowState明确为0→1→0。每组5次同样的100ms注入手势；A有效5次，B有效3次，A2有效3次，其余4次最终在Settings，排除。测量组之间不并行运行离线Perfetto/视频分析，避免额外分析负载混入组间比较。

### 前后时间线与结果

单位ms；GL/SF相对各次RESUME_BEGIN。视频间隔从背景开始露出、完整桌面图标尚未出现，到匹配到桌面图标；包含APP继续缩小的阶段。候选边界经录像检查，不等同屏幕面板present fence，录屏时间间隔不均匀，不能将细小中位数差值解释为因果提速。

| 组别 | 有效次数 | GL绘制结束范围 | SF有效GL层首可见中位数 | 视频背景/图标空档中位数 |
|---|---:|---:|---:|---:|
| 关闭A | 5 | 118.381–205.710 | 626.684 | 611.411 |
| 开启B | 3 | 117.315–211.779 | 550.006 | 537.389 |
| 再关闭A2 | 3 | 111.913–179.701 | 532.026 | 472.144 |

两关闭组汇总：视频空档553.211ms，对比开启537.389ms，仅差约15.822ms；SF中位数关闭539.270ms、开启550.006ms，开启反而约晚10.737ms。再关闭组比开启组更快，方向未复现。三组录像均仍出现完整图标缺席阶段。

**结论：该请求确实生效，但当前样本没有证明稳定缩短，更没有消除闪回。** 不能宣传“快74ms”：只拿第一关闭组与开启组比较会忽略回关组和运行波动。样本小且有采样误差，也不能据此断言其他ROM都无效。

### 最终处理与兼容边界

实验源码及两个APK归档于`build/nova-zoom-experiment-20261014/`，原始trace/录像在各组目录；逐轮数据见`result.json`及本目录`HOME_NOVA_ZOOM_EXPERIMENT_20261014.json`，最后一轮帧对照为`last-return-comparison.jpg`。候选`LauncherHomeCompat.java`与采集工具保存在`candidate-source/`。

已撤回本轮生产行为改动，源码与任务开始前保存文件hash一致，保留之前的壁纸同步/备份等工作；虚拟机恢复本轮前43A8F180…6F0F2E包。所有新增及既有诊断/实验键恢复缺省，WindowState zoom回到0；未操作实体手机。恢复源码按标准流程重新构建，最终构建状态记录于JSON，不将该重建包冒称为OPPO验收包。

Android8–10的跳过条件只有源码检查，Android11–15、OPPO12、vivo9/16、真实锁屏/最近任务/快捷桌面、多主题及60–144Hz未做该候选验收。由于候选已撤回，不将其引入Android8–16正式行为。未更新MEMORY.md。


## 20. ROOT 手势转 HOME 路线只读审计（2026-10-14）

2026-10-14，用户要求先审计。本轮不创建ROOT分支、不构建／安装候选、不启动或修改模拟器、不改变真机状态。

## 结论

ColorHomeFix 1.5 提供了明确的系统侧参考：在系统桌面手势输入入口接管事件，识别HOME后注入KEYCODE_HOME，同时包含SystemUI过渡适配及system_server默认HOME／任务相关Hook。可将“手势触发按键返回路线”列为ROOT候选，但尚未验证它能在目标OPPO Android12修复现象。

仅给Smartisan APK授予su权限，不会让它自动收到其他应用前台的系统导航触摸，也不会阻止原Recents动画。优先保留现有Launcher APK，另做仅作用于指定ROM和Smartisan默认HOME的系统Hook模块；不改SMEngine，不将ROOT作为普通版本的必要权限。

## 实际反编译依据

参考目录：`build/home-coloros-audit-20261012/ColorHomeFix-reference/smali/co/cocoondesign/homefix/`。

| 位置 | 已确认行为 | 限制 |
|---|---|---|
| `HomeFix.handleLoadPackage` | 分别向`android`、`com.android.systemui`、`com.android.launcher`安装Hook | 不是普通Launcher内的HOME回调补丁 |
| `launcher/GestureHook.install` | 寻找`com.android.quickstep.OplusBaseTouchInteractionService`的`onInputEvent`／`onDispatchInputEvent`；查找Oplus输入注入桥 | 厂商私有类／方法，不能视作Android8–16通用接口 |
| `GestureHook.shouldTrack` | 判断锁屏及第三方默认HOME；含输入接管、镜像事件和状态清理 | 若为我们的模块，应收窄到Smartisan，而不是影响所有第三方HOME |
| `GestureHook` HOME识别分支 | 位移／速度条件满足时设置已触发并调用`injectKey("HOME")` | 必须避免同次手势继续运行原返回动画或重复发送HOME |
| `GestureHook$2.run` | `Instrumentation.sendKeyDownUpSync(3)`；另有APP_SWITCH与快速切换动作 | HOME分支没有该类快速切换分支的90ms等待，不能把该等待移植为返回延迟 |
| `systemui/TransitionHooks` | 包含动画资源重定向、HOME进入动画、layer、Oplus spring与transition相关Hook | 用户反馈的正常效果不能仅归因于HOME注入；应逐项验证必要性，不能全量照搬 |

## 应实施的最小边界（未实施）

1. 确认目标ROM、实际手势处理进程、方法签名及注入权限；不匹配时不拦截原手势。
2. 仅默认HOME为Smartisan、未锁屏且处于目标导航场景时启用。返回HOME、最近任务、快速切换、取消必须分别判定。
3. 在原手势返回动画发起之前决定接管，准确处理事件归属；不能等露底后补发HOME。保留未接管输入的原行为，不吞应用底边普通触摸。
4. 接管的HOME只发送一次，检查实际注入与系统接受结果；失败不循环重试。先独立核验按键路线，再根据时序添加必要的SystemUI动画修正。
5. 不加固定恢复延迟、全屏图像遮罩或全速后台渲染。此候选采用按键路线动画，不承诺原生随手指缩放。

## 环境与验收边界

- 当前ADB仅列出vivo X21A及DT1902A；`emulator-5554`已不在线。因此未确认其当前adbd root／su／Hook框架状态。
- 本地Pixel_6_Pro配置为Android36.1、google_apis、x86_64、PlayStore.disabled。配置不能代替启动后的ROOT检查。adbd以root运行、App可调用su、Xposed成功注入系统组件是不同条件。
- Google APIs模拟器不提供Oplus上述类。不能把ColorHomeFix直接装入模拟器就宣称测试了ColorOS路径；模拟器只可验证另行适配的AOSP入口及按键注入／状态机。
- 同机同APK实际三键正常是选择该候选的依据；手势导航状态下单独发送HOME，不保证系统逐帧等同实际三键，仍需完整路由对照。
- 未来验证应分为原手势、手势转HOME候选、实际三键；核对同APK／主题／导航状态，保留WM／SF／视频证据，并覆盖取消、最近任务、输入法、横屏、锁屏及主题。
- 本轮无修复成效、构建或安装结论，不将ROOT写成完美保证。

## 用户要求删除的横屏分支

`feature/tnt-tablet-launcher`与main同为`5d13886328d94840391a946132f393ad940a84ba`，无独有提交。原项目目录有13个已暂存文件，已备份到：

`E:/FANG/smartisan/branch-archives/tnt-tablet-20261014-134053/`

归档含13个现有文件的副本与SHA256、staged／unstaged源码二进制补丁和原状态。复制后逐文件校验一致；原目录切为同一HEAD的detached状态，再用`git branch -d`删除分支名。前后porcelain状态字节一致；原暂存、工作文件、忽略文件均未清理。`home-main`仍在main。此操作删除分支名，不等于删除原目录内的横屏代码。

未更新MEMORY.md。


## 21. vivo Android 9 正常热返回现场复核（2026-10-14）

2026-10-14，用户连接设备后采集；未安装 APK、未切换默认桌面／导航、未修改壁纸或生产代码。

## 设备与采样

- 指定 ADB serial `b2a4da1c`，vivo X21A / PD1728，Android 9 / API28。
- `navigation_gesture_on=1`，`navigation_mode=null`；旧 vivo 不以较新 AOSP 键判断导航方式。
- 默认 HOME 为 `com.smartisanos.launcher/.Launcher`，v1.5.8 / 33，最后安装时间 2026-10-11 22:42:23。
- 拉取的设备 APK SHA256：`4944E939ADBE8E75C78C0A3CDDA06DDF325F852722BAFF01309ABDDDFEEA53EA`。
- 只操作该设备；DT1902A、模拟器未操作。设备初始息屏、无密码锁屏；唤醒并 dismiss 后采集。
- 复用 `tools/capture_home_return.py`，Settings → 底边中央上滑，三次均返回 HOME，PID23622保持。
- 开启既有轻量诊断，采集后恢复三个实验／诊断键为原来的 absent。测试等待仅在采样脚本中，不是产品延迟。

## 明确看到的差异

后两次热返回录像中，设置窗口开始缩小／淡出时，已经出现完整桌面图标、背景和 Dock，并与尚未消失的设置窗口同时可见。未看到 OPPO 参考视频中那种先显示异图系统壁纸、完整桌面随后补入的过程。这是正常交接的直接视觉证据，不依赖将 GL 完成当作呈现。

第一次在唤醒和前台初始化之后的返回包含缩小设置窗口后的黑底阶段，恢复也较慢；不能将全部三次写成稳定正常，或用该次统计代表纯热返回。后两次正常不代表锁屏恢复正常。

## 时序

单位 ms，各轮 `RESUME_BEGIN=0`；此表各列分别是应用回调、GL CPU 标记和系统 trace 标记，均不是显示面板呈现 fence。

| 返回 | Surface创建 | 首GL绘制完成 | 获取焦点 | 系统AppTransitionReady标记 |
|---|---:|---:|---:|---:|
| 首次唤醒准备后的返回 | 159.611 | 220.391 | 225.524 | 本轮窗口内未配对，不填下一轮事件 |
| 热返回1 | 68.097 | 77.630 | 79.851 | 147.682 |
| 热返回2 | 31.853 | 48.150 | 50.291 | 98.546 |

三次都重新创建 Surface；Context generation始终1，scene identity始终265236151，无热返回场景重建。初始准备阶段有一次Activity／Context／scene初始化，不能误算成返回触发的冷启动。

后两次在恢复之后、下一次Pause之前采到系统 `AppTransitionReady` 和 `AWT#applyAnimationLocked`，首次GL完成早于这些标记。结合录像，支持“完整桌面参与窗口过渡”的解释。仅凭标记名称不能证明厂商内部的等待条件、手势跟手算法、隐藏API调用或精确动画起止。

## 对修复方向的约束

1. vivo正常不依赖Surface始终存在；继续把“禁止Surface重建”当成完整修复不符合现场证据。
2. 当前核查的恢复帮助类、J、Eb、vc及SMGLSurfaceView中，未找到按vivo／OPPO品牌选择另一套HOME恢复路径的直接分支；这不等于已穷尽整个APK与厂商系统实现。
3. 要迁移的是“完整HOME能参与APP退场交接”的条件。尚未证实普通APK可让ColorOS采用相同系统动画流程，也未证明应将Android9厂商行为直接应用Android8–16。
4. 与历史OPPO相比，设备系统、安装包／主题和测量原点不同；不直接相减宣称性能提升。缺少Android9完整合成可见性时间线，不能推算首帧实际呈现时刻。
5. 本轮没有修复补丁、没有OPPO改善证据，也没有新增vivo Android16验证；无需为只读诊断重建或安装APK。

## 证据

本地 `build/vivo-normal-path-20261014/`：设备APK、`timing-summary.json`、系统日志及SF结束快照；`vivo9-gesture/`：原始atrace、HOME日志、samples.json、WindowManager快照、录像、逐帧PTS、overview.jpg及warm-returns.jpg。

录像PTS尚未与trace绝对时间校准，不逐毫秒硬拼。SF结束快照不是动画过程；旧设备SurfaceFlinger latency表缺有效数据，不用零值补造present时间。第一轮异常及后两轮正常均保留，不选择性删除。

未更新MEMORY.md；本结果为有条件的现场观察，非所有vivo／所有ROM的稳定架构结论。


## 22. 2026-10-24：OPPO 入口重复初始化修复与手势闪回复核

### 已修复的额外加载路径

本轮当前工程为 smartisan-launcher-original-port。初始连接 OPPO PDCM00/API31 与 vivo V2458A/API36；后者已断开，最终补丁只在 OPPO 验证。普通返回阶段，两台各五次手势均维持原 PID/Activity；vivo 日志另有两次 grid_migration 协调重载，不归为普通返回或内存回收。

OPPO 现场旧包 SHA256 938942bc197006ed364a5051df958f951c66ec0ba471ee4611b2958a714409dc，与工程原正式包4b7e0a20a441662551acf155f33efb26cb3ffad715a494f8902b65128337452b版本号均为1.5.8/code33。保存旧包后，依据本轮用户“允许 OPPO 保留数据安装与回归”覆盖安装；没有删除数据、切换默认 HOME/导航或主题。用户在分阶段采样间有主题/宫格操作，19:32:55旧主进程退出前出现主题设置和 :reload，不能按 SIG9 或 exit-info 空进程子原因直接定为 OOM。早期12宫格与随后20宫格组不混算性能收益。

更新首次进入发现 LauncherAlias→外部应用→系统 HOME 创建 Launcher，并紧接原主进程退出。另用受控冷入口重复：在设置前台停止本应用，启动 MAIN/LAUNCHER 的 LauncherAlias，设置→HOME 后 PID23793→27728。原版 clean_launcher 的 J.b 保留 PROC_ID/myTid 重复初始化检查，命中即调用 ua.dc→killProcess；J.c/onDestroy 亦保留全局清理/退出。当前源码同样如此。因此不能在重复 Activity 上再初始化原场景，也不能只删除原版退出保护。已处于规范 HOME 任务时再打开别名的热路径没有重启；该反例保留。

最小修复复用现有 LauncherHomeCompat：只识别真实 Activity component 为 LauncherAlias，构造同包 Launcher 的 MAIN/HOME，复制原 extras，使用既有 HOME 路线的 NEW_TASK/CLEAR_TOP/SINGLE_TOP，先 finish 别名再启动目标，避免 singleTask 复用即将关闭的别名。仅这次别名转交的 onDestroy 不进入全局桌面拥有者清理；规范入口的全部原版初始化、退出、绘制和动画保留。启动被拒绝会记录 HOME_ENTRY_REDIRECT_FAILED，已结束的别名不会继续初始化原场景；不无限重试。无新增 Activity/Service/Manager/缓存或 Manifest 修改。因为别名不能创建第二套原场景，需增加这一个入口分支，不能直接复用 J.b 的初始化路径。maintained 只作任务/入口行为参考，没有搬入其核心。

首个候选 f74d5e61…采用先 start 后 finish，因系统复用别名而落回系统桌面，即使 PID相同也判失败并撤回；其五组不算验收。最终3b9d31000166e8596d3463b575e5592383285b6a1562e5c76e61728129ed3efe已覆盖安装，签名v1/v2/v3、16KiB zipalign及设备APK哈希一致；相对修前正式包非META-INF仅classes.dex/classes2.dex变化。真实构建helper在OPPO ART执行27检查，覆盖规范入口不转交、component身份而非可伪造Intent判断、extras不丢失/不共享修改、危险任务flags不复制、finish先于start、拒绝/组件缺失和无Intent等。夹具不代替真实Activity生命周期。

| 最终回归 | 结果 | 边界 |
|---|---|---|
| 受控冷别名→设置→HOME，五个有效样本 | 两阶段PID相同，实际进入同一smt_launcher窗口：5001/5964/11576/12963/13216 | 每次冷入口前在设置前台force-stop本应用，属于确定入口复现；不是随机内存压力。前两轮后主机ADB中断，第三轮无效，补三轮；部分返回截图还处在系统退场动画，不当静态像素基准 |
| 普通底边手势→HOME五次 | 均到桌面，同PID13216 | 原生录屏仍见背景露出/图标补入，闪回未修复 |
| HOME键返回三次 | 均到桌面，同PID13216 | 不曾改三键/手势系统设置；按键输入仅为路线负控 |
| 搜索、桌面设置和既有文件夹 | 收尾记录在final-functional/ | 只记实际完成项目；常用应用/三星Share、主题深浅色和全ROM矩阵不包含在本轮 |

启动 begin 标记现在位于 framework super.onCreate 和别名排除之后，以免临时别名重置全局首屏计时状态；本轮无整体启动提速结论，也不把新旧起点直接相减。Android9/16/其他ROM补丁验收、非默认桌面入口/工作资料环境、配置重建和长稳仍待测。普通系统回收、规范Launcher Activity重建、状态栏高度真实纠正仍可能冷加载；本修复只关闭已复现的别名双初始化路径，不宣称所有偶发加载消失。原APK归档本地仍缺失，原实现依据clean_launcher源码，未声称重解原APK。

### 仍开放的 OPPO 手势闪回

旧包同一录像前五次手势返回均在设置窗口缩小时先出现暗背景，之后完整图标才进入；第一次原生编码帧2.819s仍无图标，2.838s已有图标，但设置缩小窗口尚在，不能称为纯壁纸区间时长。早期旧按键录像与手势录像尾段有录制重叠，不用于性能比较；另外保存单一录像内连续3次手势/3次按键组。最终正式包的5次手势/3次按键录像独立、无重叠。修复入口后手势同类空档仍存在，未把回到桌面或同PID写成闪回PASS。

独立SF单组对照为同包、同布局的正常返回，55次/路线只读proto快照。手势第一次采到SurfaceView BLAST有效1080×2400 buffer且可见为输入后440–480ms；HOME键为220–260ms。按键在160–180ms已采到有效buffer但visible region为空，证明buffer与可见不是一回事。采样间隔与dump执行本身限制精度，不报告显示面板首像素时间，也不与不同录像PTS逐毫秒硬拼。

同一事件日志内，手势server wm_resume_activity→client wm_on_resume_called间隔33ms，按键17ms。事后用epoch与/proc/uptime偏移估算时，应用恢复与SF首次可见窗口接近；这条对齐并非同步采集，不能当精确亚帧证据。下一步重点是系统何时恢复/呈现HOME窗口，不应继续通过延长/缩短加载动画、去掉图标读取或重复失败的PixelCopy/TextureView实验来宣称修复。尚无经过本机验收的新窗口交接方案。

OPPO内置screenrecord缺失，atrace --async_start报record-tgid写入失败。本轮复用已有本地scrcpy编码采集和SF proto；无效trace、无录屏及主机ADB中断样本均保留为失败/限制，不把非空trace文件当成功。没有开启工程模式、修改日志属性或实验开关，未调整刷新率、默认桌面或导航。原148项暂存patch保持，MEMORY.md未改，无add/提交/推送。

本地证据：build/home-reload-audit-20261023，包括oppo-installed-before.apk、pre-entry-fix/、alias-cold-repro/、被否决alias-cold-after-five/、entry-five-valid.json、entry-final-build-proof.json、oppo-entry-final-warm/、oppo-sf-pair/及final-functional/。生产仅Launcher.smali和LauncherHomeCompat.java，长期测试tools/tests/home_entry/；未新增平行审计主文档。

## 23. 2026-10-24：Android9 显式组件任务类型补充

第22节3b9为当时OPPO验证的中间实现，不能代表最终Android9兼容验收。vivo X21A/API28实测显式 Launcher MAIN/HOME 初次生成 standard task，之后系统 HOME 新建 home task，PID15440→15569；前后台前后任务245→246。AOSP9 ActivityRecord.setActivityType 要求非显式组件或允许的系统调用者才视为 HOME，见 https://raw.githubusercontent.com/aosp-mirror/platform_frameworks_base/android-9.0.0_r61/services/core/java/com/android/server/am/ActivityRecord.java 。此为新增入口证据，不重开用户已确认关闭的旧内存现场问题。

最终复用 LauncherHomeCompat 的共享工厂：默认 HOME 确认为本包才以 setPackage 限制自己的 MAIN/HOME、不指定组件；非默认或查询失败保留显式规范入口。Alias 仅在前者转交，协调重载与 maintained 设置页也复用工厂，各自 flags/extras不改。无默认桌面切换、Manifest或系统状态修改。ART入口34项通过；正式包bf07481401187d0e783f352d6d0ddce7da2d52c6ea92d618a3abf81d6d2c38f9安装拉回哈希一致。五轮冷Alias→设置→系统HOME均实际回到同一smt_launcher窗口和PID，16660/16854/17043/17221/17404，componentSpecified=false、mActivityType=home。三轮搜索/桌面设置及一轮既有文件夹开关截图核对通过，最终17404。证据build/default-circle-rounded-20261024/vivo-final-alias-five、home-entry-final-probe、vivo-functional。

OPPO断开后尚未验最终工厂，设备仍有临时图标来源诊断包；用户明确选择先Android9，OPPO稍后。重接后需恢复正式包、清理本轮专属采样并补测，不能把来源重放当整机验收。第22节闪回结论仍开放，本项没有整体冷启动提速结论。Android16/API24/工作资料/非默认入口真机与长稳未补齐。
