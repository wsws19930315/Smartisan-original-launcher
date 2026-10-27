# 全项目架构与执行链审计

日期：2026-10-15；main / 5d13886328d94840391a946132f393ad940a84ba，加任务开始时53项已暂存修改。**这是全项目目录/入口盘点、重点链路深读及可用环境验证；不是对3712个Smali、全部native指令或所有资源逐条安全证明。** 验收状态：PARTIAL / 多ROM及长稳未验收。

## 基线与真实构建边界

- 本工作目录是主main，137个Java、3712个Smali；5256个源码/资源/测试/关键产物已记录SHA256。未暂存差异开始为空；原有暂存包含10月14–15日启动/圆框/备份/壁纸修改，必须作为基线保留。
- git worktree list确认独立 E:/FANG/smartisan/home-root-module，分支codex/root-home-route；实际模块位于modules/home-route，并非假定的root-module目录。当前home-main路径不存在；旧文档路径不能当成当前源码入口。其他detached/历史实验工作区没有清理或修改。
- 远端关系只检查本地upstream引用，HEAD与该引用无提交差异；没有fetch，不能宣称已刷新服务器最新状态。本地暂存差异见staged.txt，未用远程覆盖。
- build.bat → 图标源审计/派生 → maintained与内置搜索资源 → apktool launcher/ → 注入launcher/original/AndroidManifest.xml → Java编译classes2.dex → zipalign →签名。实用JDK E:/Program Files/Android/Android Studio/jbr，SDK D:/sdk，Build Tools37.0.0，android.jar API36。
- original_apks/com.smartisanos.launcher-3.apk是原版归档；clean_launcher/raw是干净代码参考，maintained只能参考。现代备份/搜索索引等Java Owner在原版中没有等价类，不能由原版替代。原版搜索FlingUp的终点为向下越过1/4高度，当前双向适配应保留镜像终点语义。

## 生产执行链与状态 Owner

| 模块 | 已核对入口/调用链 | 状态与线程/释放边界 | 当前边界 |
|---|---|---|---|
| Activity/Window | Launcher.onCreate/onResume/onPause/onStop/onDestroy → J → SMGLSurfaceView | Main生命周期；LauncherHomeCompat以弱Activity/Surface引用记录；不是Recents可见性的Owner | 原热场景保留，未加入截图/延时遮盖 |
| 渲染/场景 | J创建vc/Eb并setRenderer；vc.onDrawFrame → Eb.update → SMEngine场景/纹理 | GL线程拥有EGL/场景更新，MAIN不能直接回收GL节点；实际可见仍由WM/SF决定 | 原纹理delete路径在Ea/N/Da/c.*，存在删除方法不证明零泄漏 |
| 动画/帧时间 | Eb.update → Ra.T，Unlock协调器交接 | 已有实际dt/预滚/持指门；不能改成按显示刷新率加倍或提前结束Loading | 60/90/120/144Hz录像和GPU耗时未覆盖 |
| 数据模型 | PackageEventGateway → PackageStateRepository + ProfileRepository → LauncherModelRepository → RemovalGateway → Aa.a(ItemInfo) | key为userSerial/package/component；UNKNOWN/quiet/locked/replacing保留，不把空列表当删除 | 正式删除门188项及SQLite恢复隔离，不等于OEM分身实测 |
| 初始数据库 | data/A DatabaseHandler → 原H/G事务 + StartupPlacementCommitListener | 启动批次有提交/回滚检查；不跨图标worker等待持事务 | 本轮未撤销批量事务和延后持久化 |
| 静态图标 | SourceManager/RedirectIconDB/Pack/online → IconRasterDiagnostics → IconVisualMetrics/Composer | RAW来源与最终几何分离；圆框依据用户主动DEFAULT选择，不以有效DEFAULT回退冒充主动选择 | 本轮几何/圆框/PNG视觉资源未改 |
| 预览/图标库 | IconPreviewRepository → Catalog/SearchIndex → IconLibrarySearchPage | app Context；decode2线程、队列全局512/会话96；online2线程队列24；Session取消+代际门；缓存6–16MiB | 元数据/查询与PNG分离，实际全分类全设备响应未量化 |
| 内置搜索 | FlingUpGesture → VerticalGestureDirectionConfig → Host.openLauncherSearchInternal → OriginalQuickSearchActivity → SearchSnapshot/SharedSearchMatchModel | 字符输入读不可变快照；后台单executor；弱监听；图标hydration按代际取消 | 本轮发现并修正入口终点/时限门；索引API候选未改 |
| 快捷桌面/Magic Flow | RootView原单/多页手势 → QuickDesktopController → Capture → HostView/ContentView | 捕获generation；背景就绪才揭露；View draw消费快照；媒体可见期间单worker，detach停 | 门控99+9项，不等于真实MediaSession与四指矩阵 |
| 主题/壁纸/状态栏 | ThemeChooserActivity/Host/Bridge → 原X/v场景 → 窗口样式/壁纸IO | launcher_theme与launcher_grid_theme区分；串行系统壁纸锁、requestKey和摘要/ID去重 | 普通/透明/毛玻璃不混用；失败不在每次HOME重试是已有有意合同 |
| 光影/动态天气日历 | 原Ra/Qa向量 → IconIlluminationCompat八层投影；WeatherBridge数据 → ActiveIcon | Sensor独立HandlerThread、注册资格/epoch、pause注销；MASKS256上限；GL绑定代际失效 | 向量23011与sensor111项；手持lux/天气/锁屏三现象仍无现场闭环 |
| 设置/配置/重载 | MaintainedLauncherSettingsHost → Bridge/原设置；ColdReloadCoordinator → :reload窗口/退出旧PID/首帧token | UI/Main与后台恢复分开；token超时是失败而非成功；状态栏Insets计算Owner唯一 | Host21431行是维护热点，不能按行数认定运行缺陷或拆Manager |
| 备份恢复 | DesktopBackupController/RestoreController → ArchiveReader/Validator → DB/偏好/图标/主题 → journal/rollback →新首帧 | 后台主体；BackupOperationLock跨进程文件锁；DB前RecoveryGuard仍同步保护；先日志后阶段 | 本轮修复图片校验临时资源，真实整库SAF/断电恢复未验收 |
| 快捷方式/角标/安装 | PinShortcutConfirmActivity校验PinItemRequest/用户确认；ShortcutLaunchActivity按serial启动；Badge服务/Install串行worker | Pin请求类型/有效性、profile身份；通知服务受BIND_NOTIFICATION_LISTENER_SERVICE；安装IO不回MAIN | 未做真实安装/卸载第三方fixture，未修改通知权限 |
| ROOT模块 | 独立modules/home-route → 系统侧GestureHooks/SystemHooks/HomeKeyBridge | 需Xposed/ROOT；不由桌面build.bat构建；仍引用桌面SwitchEx源码 | 只核对来源和发布边界，不启停/刷模块，不承诺OPPO修复 |

## 线程交接与生命周期

```text
MAIN: Launcher → J/Window/触摸/设置 → 原事件队列
GL:   vc.onDrawFrame → Eb.update → SMEngine → texture/buffer
DB:   原DatabaseHandler → Model → 原item-level执行器
IO:   图标有界队列 / 搜索单worker / 备份恢复worker / 壁纸写锁
Sensor: 独立HandlerThread → 资格/epoch → 同向量monitor → GL消费
System: Surface/Window/Recents/SF决定层显隐；buffer完成不等于屏幕呈现
```

冷启动的数据/页面准备与热恢复不能混为一谈；Surface销毁不必然表示Model丢失。onPause/onStop停止功能任务及sensor，onDestroy注销页面/快捷桌面引用；释放后的结果需要token/generation拒收。现有弱引用、取消和边界检查有代码/局部测试，但未证明每个老Smali回调的所有竞态。

## 架构结论

当前总体Owner边界合理，不需要新Launcher框架。已确认缺陷位于备份校验资源分配、搜索输入边界和失效测试夹具；不是SMEngine整体架构错误。Host过大、跨Java/Smali合同和历史文档漂移增加维护成本；优先以可执行不变量和分批差异约束，不能借审计拆分全部兼容逻辑。

具体问题见[问题清单](FULL_STABILITY_AND_BUG_AUDIT.md)，验证与未覆盖项见[回归报告](FULL_FUNCTION_REGRESSION_REPORT.md)。原始清单在build/full-project-audit-20261015/source-inventory.json及baseline-hashes.json。
