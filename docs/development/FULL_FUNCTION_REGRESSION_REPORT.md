# 全功能回归与兼容性报告

## 2026-10-23 第二十三批：录屏定位冷启动结束后的状态栏黑带

**第二十三批当前：vivo X21A/Android9冷启动后顶栏黑带已复现并最小修复，未改加载动画时长或壁纸取色。** 原正式包两段录屏均显示桌面先完成淡入，随后只有顶栏背景变黑再恢复；中央顶栏与下方空白区亮度差最大193/205（0～255），记录到黑带12/11帧。临时去掉e/g跨两帧明暗刷新仍有11帧黑带，该假设排除，Smali逐字节恢复。真正有效的限定修复在OriginalLoadingContentFactory.coverLoadingWindow：仅Launcher Activity、空文案的普通初始化加载窗、且非协调重载黑色覆盖窗，清TRANSLUCENT_STATUS、加DRAWS_SYSTEM_BAR_BACKGROUNDS、透明statusBarColor；原FULLSCREEN、layout flags、导航栏、内容/坐标/动画与dismiss时机不变。Coordinator仅暴露现有sInitialLoadingWindowApplied的包内只读判断，保护协调重载黑色覆盖，不新增状态/Manager。候选5段及正式包1段冷启动录屏均无该黑带，12静态图标区域逐像素一致；2520窗口策略场景12790检查通过、旧源码负控准确失败。正式build.bat、v1/v2/v3、P16、保留数据覆盖安装拉回哈希、五轮底部上滑搜索/settings结果/桌面设置/返回及既有文件夹开关通过，同PID5109；最终SHA256=f58efc77a2b2a9c17608fbe0695b1d4cda38ea963e7f54a5602cdfc4ed2a3901，相对第二十二批非META-INF仅classes2.dex。此前来源查询优化保留、暂存134项保持，MEMORY未改。证据build/startup-statusbar-20261023。

**原版取色与下一项：** 原版clean_launcher的initGaussianDarkLight分别分析桌面、顶部90px带和底栏，保存sGaussianResSuffix/sStatusbarColorSuffix/sNaviBarLightOrDarkSuffix；顶部亮暗经status_bar_icon_color[_light]、status_bar_number_color[_light]由e/s.d→UI线程e/g→ua.setSystemUiDecoration提交，并非故意制造黑背景。普通主题采用主题固定配色；透明/毛玻璃相关路径沿用其壁纸分析分支。当前移植e/g按先前已验证兼容方案用最终app_text_color统一legacy/API30+ appearance，这与原版分区资源策略有差异，本批不撤销已确认的四指/主题兼容修复。用户新增假设已核对源码；本机黑带由保留该取色路径、只改窗口背景声明的对照消除，不能据此关闭透明/毛玻璃深浅壁纸文字颜色矩阵。下一项为该矩阵及切换顺序验收；本轮没切主题/壁纸，Android16/其他ROM、真实16KiB/长稳等仍未验证。整体冷启动仍开放，Folder性能暂停、A22不重开。

逐次录屏、原版取色路径、负控及恢复边界见开发日志第二十三批。


## 2026-10-23 第二十二批：合成诊断复用实际圆框策略，消除额外来源查询

**第二十二批已完成最小修复及Android9真机回归，整体冷启动仍未解决。** reportSourceCanvasOnce在合成之后为日志调用desktopIconSourceType，DEFAULT又经单参desktopDefaultCircleEnabled再查一次；composeTexture此前已有本次实际defaultCircle。生产仅IconRasterDiagnostics.java将该布尔值交给报告，移除报告内来源/圆框重查，不改变绘制、选择/回退/失效、纹理键或Bitmap责任，无新增缓存/Owner。vivo X21A/API28原/新各5启动，每轮31份首次报告的额外来源查询37→0，相关计时段中位73.173→0.093ms；PAGE_READY2165→2148ms，最长GL帧1643.042→1566.377ms/CPU1500.264→1452.809ms，小样本含调度/缓存/ART状态，不能将差值全部归因或宣称整体解决。实际合成/报告方法在ART的1033场景11351检查通过，旧源码负控准确失败；稳定设置下日志/像素一致，另测来源与设置在绘制后变化时报告仍描述本次实际绘制。正式包五轮底部上滑搜索、settings结果启动、桌面设置、返回及既有文件夹开关通过（PID31327）；原/新/正式12静态区域逐像素一致。build.bat、v1/v2/v3、P16、v1.5.8/code33、覆盖安装拉回哈希通过；非META-INF仅classes2.dex，最终SHA256=af813f47e41b91bd36456b8234dc5243846432a32b851d67008a99971d3b5b8e。临时Host/Startup诊断逐字节恢复，dex标记及专属JSON清零，134项暂存patch保持，MEMORY未改。证据build/startup-source-report-20261023。

**接下来：** 用户追加“加载动画结束后状态栏黑一下”，本机录屏已复现桌面内容先稳定、顶栏随后独立变黑约0.3秒；转入该窗口/状态栏交接问题的逐帧对照，不把它归为加载动画时长或以本批性能修复宣称关闭。冷启动剩余GL成本、Android16/三星Share/跨ROM/首装/长稳/真实16KiB仍未全部验收，Folder性能暂停、A22保持关闭。

完整根因、原生负控及验收边界见开发日志第二十二批。


## 2026-10-23 第二十一批：主题资源解码五样本审计，未发现同图重复

**10/23第二十一批当前：本项审计及Android9真机回归完成，生产代码净改动为零，整体冷启动仍未解决。** vivo X21A/API28同条件5次进程启动，在GL线程至PAGE_READY范围记录xa.getBitmap与xa.a(AssetManager,String)实际成功打开的AssetManager身份及资源路径；每次37个实际来源、37次解码，重复来源数均0。解码区间中位203.630ms，诊断PAGE_READY2341/2159/2133/2174/2191ms（中位2174）；含记录/首次调用栈开销，没有候选修复对照，不能算性能收益。原背景、文件夹底图与cover中位65.638/55.455/30.093ms，属于不同素材；20张back1～back20也是独立素材，不能按相同前缀当重复。现有f→Ea按键复用Da纹理；Da上传或释放会回收其持有Bitmap，因此未新增xa裸Bitmap缓存。两份临时诊断源码逐字节恢复，正式build.bat、签名/P16/v1.5.8 code33、保留数据安装及拉回哈希通过；全部非META-INF ZIP成员与本批原正式包相同，重打包整体SHA256为73319f890b86e997ec79c6a488260fafe0508128bd96ed2bd0f9d96025fb62c7，不宣称APK逐字节重现。正式包5轮底部上滑搜索/settings结果真实启动/桌面设置/返回及既有文件夹开关通过，同PID27504；12静态区域一致、截图人工核对。最终dex无本批诊断标记、专属JSON清零、atrace=0，日志开关保持no/log.tag=E；134项暂存patch不变。MEMORY.md未更新。证据build/startup-theme-assets-20261023。

**下一项：** 核对IconRasterDiagnostics.reportSourceCanvasOnce为日志再次调用desktopIconSourceType的成本；composeTexture已有resolved.type和实际defaultCircle结果，先计数验证额外解析，再考虑将同次结果交给报告，保持绘制/回退/来源失效语义，不新增缓存。不要重拆本项资源解码、重开最终磁盘缓存/无条件页延后/前移加join。Folder性能暂停、A22按用户确认关闭；本批未验证其他主题/Android16/三星Share/跨ROM/首装/长稳/真实16KiB，未关闭这些缺口。

完整调用、逐次样本和恢复边界见开发日志第二十一批。


## 2026-10-23 第二十批：跳过普通主题零几何阶段的提前壁纸分析

**10/23第二十批当前：已定位并减少初始化前段的一次完整壁纸解码，整体冷启动仍未解决。** 前批两个约84ms decodeBitmap来自Application/X.da与Activity/Constants.initByTheme，均请求同一私有壁纸URI（只记录URI摘要/size/mtime，无原始路径），各解码1080×2280/9849600字节Bitmap。Application阶段窗口几何为0，Activity阶段1080×2280且有系统栏几何，不能复用整套明暗结果。生产只在theme/X.smali的da入口加限定：Application、宽高均0、非毛玻璃/非透明/非默认固定资源主题、非大屏才跳过早期分析；该普通主题分支仍使用原unsuffixed系统栏资源，后续原initByTheme在有效几何下完整分析后才创建桌面。无Bitmap或结果缓存/新Owner，不改分类算法、URI读取、主题切换或渲染时序。实际X.da Smali在ART的6144场景30744检查及两类负控通过；现有壁纸同步49断言通过。vivo X21A/API28原/新各5启动，分析/解码次数2→1，早期分析中位127.664→0ms，bindApplication443.650→310.130ms；Activity起算PAGE_READY2147→2173ms没有改善，不能宣称整体冷启动解决。正式包五轮搜索/设置/返回与既有文件夹开关、额外冷设置入口通过；壁纸/文字/材质遮罩及12静态区域原/候选/正式逐像素一致。最终SHA256=8d54bbf32de069b4dc10e12e6e7e557b1a2d2e8f690b26fcceefe14702da5528，签名/P16/真实安装拉回哈希通过，非META-INF仅classes.dex变化；诊断3文件逐字节恢复、dex无标记、测试JSON清零，134项原暂存保持，MEMORY未改。证据build/startup-main-decodes-20261023。

**下一项：** 本批主线程两次大解码定位及限定修复收口，不重复拆本微任务。剩余首屏GL仍约1.65秒/运行CPU约1.51秒；先利用已存trace和现有资源Owner，统计同一主题纹理PNG的解码次数、是否有可复用结果及借用/回收约束，再决定最小修复。不得直接新增raw Bitmap缓存、重开最终磁盘缓存/无条件延后页/简单前移加join。Folder性能暂停、A22按用户确认关闭；本批仅Android9普通非默认主题真机，毛玻璃/透明/默认/大屏是代码分支保护和原生夹具覆盖，不是对应主题/ROM实测，Android16、三星Share、全ROM/首装/长稳/真实16KiB仍有缺口。

完整调用依赖、受保护路径、逐次数据、测试夹具及设备验收边界见开发日志第二十批。


## 2026-10-23 第十九批：变体映射直接迭代，消除完整包名数组复制

**10/23第十九批当前：变体表首次加载已完成归因与最小减分配，未证明明显启动提速。** 每进程在GL线程同步加载1次356182字节/4625包的variants.json；原5样本读取/JSON/映射整理中位6.506/15.770/54.817ms，整体73.113ms（各自中位不可相加）。生产仅IconPreviewRepository.ensureVariantsMapLoaded：用已有JSONObject.keys迭代，替代names→JSONArray→索引循环；不移动读取时机、匹配顺序或改变现有Map/错误策略，不新增缓存/Manager/线程。实际加载器/getVariants方法在API28 ART配合受控流的190场景24535检查通过，4625项完整映射/列表顺序一致，names转换1→0，旧源码负控准确失败；现有资源ID/实时catalog/file/variants原生80检查通过。vivo X21A原/新各5启动，加载整体中位73.113→72.483ms、映射54.817→52.041ms，PAGE_READY2191→2176ms；差值很小且含调度/缓存，不记为整体冷启动已解决。正式包五轮底部上滑搜索/settings结果实际启动/设置/返回与既有文件夹开关通过，原/候选/正式12静态区域像素一致。最终签名/P16/覆盖安装拉回哈希一致，非META-INF仅classes2.dex；SHA256=d2c23bfdabed298a5d911229a26df4c1caa4397ba70a671f1e7cf4672298a9b8。诊断源码恢复、最终dex无标记、专属测试JSON清零；134项原暂存保持，MEMORY未改。证据build/startup-variants-20261023。

**下一项：** 现有候选5条trace均出现主线程两次约84ms decodeBitmap（每轮两项均83.9～84.9ms）。先定位其资源名及调用方，确认是否同图重复解码再修，不继续拆本批变体表迭代微任务，不依据同样时长直接认定相同图片。整体冷启动仍开放；Folder性能暂停/A22关闭不重开，三星Share、Android16本批回归、首装/长稳/跨ROM/真实16KiB缺口保留。

详细边界、逐次数据与反例见开发日志第十九批。


## 2026-10-23 第十八批：复用进程Application，消除首屏重复反射

**10/23第十八批当前：已修复Context获取中的重复反射，Android9真机验收通过。** 复用前批五条系统trace确认最长首屏GL帧中位1722.248ms、运行CPU1589.886ms；在线图标线程该区间未运行，不把整段归为模型Worker等待。单独1ms方法采样定位currentApplicationContext反复getMethod，采样仅定位、不充当五样本性能数据。生产仅MaintainedLauncherSettingsHost.java：在现有入口以volatile复用成功的Application，保留原反射以及空值/异常/非Application Context的重试；不缓存Activity、Resources、配置或Bitmap，不新增Manager。实际方法提取后在ART受控反射Provider的216检查/8000暖态并发读取通过，旧源码负控准确失败。vivo X21A/API28原/新各5启动，GL阶段Context读取均375次，反射375→0；该段计时中位78.314→3.412ms，PAGE_READY2254→2207ms、最长GL帧1724.100→1667.255ms/运行CPU1567.050→1526.338ms。小样本差值含调度/缓存，不宣称整体冷启动解决。正式包五轮底部上滑搜索/settings结果实际启动/设置/返回、既有两项文件夹开关通过，同PID15918；修前/候选/正式包12静态区域一致。签名/P16/安装拉回哈希通过，非META-INF仅classes2.dex变更；最终SHA256=544608fcff0035ebc8e023bef9a9b3932d2575671e0e5614d4c6fdc670b24297。临时采样/计数代码恢复且dex无标记，应用专属测试文件清零，134项原暂存patch保持，MEMORY.md未改。证据build/startup-remaining-waits-20261023。

**下一项：** 只核对改进图variants.json首次解析在GL路径中的实际成本和已有预载入口，先用普通计数/区间验证采样提示，不能把单次受采样干扰的110.424ms当稳定耗时或收益；复用现有sVariantsMap，不再重复本批Context微任务。不得重开已否决最终磁盘缓存、无条件延后页或简单前移加join。Folder性能仍暂停，A22按用户确认关闭；本批未跑Android16/其他ROM/首装/长稳/真实16KiB，三星Share现场缺图未关闭。

详细边界、反例和逐次数据见开发日志第十八批；本批不扩大其他未验收项。


## 2026-10-23 第十七批：同次合成复用几何快照，Android9真机完成对照

**10/23第十七批当前：已最小修复同次合成的重复几何解析。** 生产仅IconRasterDiagnostics.java：原composeTexture经NormalIconRasterSpec解析IconVisualMetrics后又直接解析一次，现将同一份metrics交给原spec构造逻辑；公共入口、空几何回退和全部物理字段保持，无跨帧缓存/Manager/Bitmap持有。实际合成/扫描/spec方法配合Android原生Bitmap，1010场景9093检查通过；旧源码负控准确拒绝仍2次解析。vivo X21A/Android9/API28真机原/新各5启动，每次31次合成的解析62→31，解析中位35.209→17.177ms、合成483.848→462.093ms；PAGE_READY2289→2262ms，小差值仍含缓存/调度，不宣称整体冷启动解决。正式包签名/P16/覆盖安装拉回哈希、12静态区域逐像素一致、5轮底部上滑搜索/settings结果/设置/返回与既有两项文件夹开关通过；同PID10769。最终SHA256=7c48aa93836f96e8323dffb6dea7ed66a88530c0b855bbda767e220c165d643e，非META-INF仅classes2.dex变化，所有临时计时/导出源码恢复且最终dex无标记，测试JSON清零。134项原暂存patch保持，MEMORY.md未更新。几何重复本项收口；下一项利用已存真机trace检查模型加载及首屏构建的剩余最长等待，不重拆几何/来源三查或重开已否决缓存。Folder性能仍暂停；三星Share、其他ROM、首装、长稳、真实16KiB等缺口保留。证据build/startup-geometry-snapshot-20261023。

本轮真实覆盖vivo X21A/API28原20宫格、现有主题/圆框与两项文件夹；修前/修后各5启动，正式包5轮设置/底部上滑搜索/提交settings并启动系统设置/返回，同PID10769。12静态区域像素一致、文件夹开关截图正常。未开启常用应用开关/权限，未测试三星Share、多主题、横屏、首装或长稳；XML不可用时明确以查询截图与实际焦点/启动结果核对。


## 2026-10-23 第十六批：定位静态节点构建耗时，排除把整段归因GL上传

**10/23第十六批当前：耗时定位完成，生产逻辑净改动为零，冷启动未解决。** 当前无真机连接；复用第十五批真机五份trace，解码区间去重中位169.250ms/运行164.903ms，不能解释1065.776ms整帧。另在已有API36只读模拟器/host RTX3060做5次分段诊断，PAGE_READY3479/2468/2185/2496/2392ms，中位2468；静态节点构建中位1153.187ms，而GL位图上传23.637ms、文字23.358ms。单次细分确认静态合成507.151ms、来源307.359ms、准备143.175ms、键135.944ms；圆框127.220ms含在准备阶段，Alpha扫描62.282ms含在合成阶段，均不可重复累加。该单次不是五样本性能收益，更不能与真机1286ms混比。没有证据支持删除原版绘制/上传，本轮不交付臆测修复。9份临时源码逐字节恢复，重建包全部非META-INF成员与本轮原包相同；正式SHA256=4806115c3ea2b32336497c1b3b5857fcd79ed8089a159c7e2abc6d9ad85ca18f，签名/P16/覆盖安装拉回哈希、13静态区域及5轮搜索/设置/返回通过。第5轮ADB中断后同PID重跑，前4轮与中断证据保留。134项原暂存patch保持，MEMORY.md未改。下一项只核对composeTexture中NormalIconRasterSpec和IconVisualMetrics的同次重复几何解析，量化后考虑复用同一快照；不重开来源三查/旧阴影提取/最终磁盘缓存/无条件页延后实验。证据build/startup-cell-content-20261023。

功能验收只覆盖本API36只读AVD现有主题/布局：5轮设置、底部上滑搜索、settings查询提交、结果进入系统设置及返回，同PID；第5轮ADB中断后重跑，失败现场保留。13静态区域相同，转场截图不当成静态视觉通过。未开启常用应用权限/开关，未验Share、文件夹、真实天气/日历、真机、多ROM或首装；这些缺口不因本轮基础回归关闭。


**10/22第十五批当前：静态合成的来源/类型/身份改为复用同次快照。** 生产仅IconRasterDiagnostics.java与MaintainedLauncherSettingsHost.java，复用已有ManagedIconSource和来源解析Owner；未引入跨调用缓存、Bitmap持有、线程或数据协议，纹理键与合成仍各解析一次。实际方法+Android原生Bitmap的480键场景/480合成场景共2631检查通过；自定义图完整key+compose链的文件解码/重编码5→2（不代表全部内存PNG解码），改进图来源请求3→2，缺失图仍保留晚到复查；旧源码负控准确失败。Android16真机V2458A同条件各5启动PAGE_READY中位1321→1286ms，GL构建帧wall1093.780→1065.776ms/运行CPU1002.108→976.637ms；未隔离缓存/顺序/调度，不能将35ms全归因或宣称冷启动解决。首屏13静态区域像素一致，首次8页往返无>50ms GL帧；正式包五轮图标/底部上滑搜索/准确settings查询/设置与返回及文件夹开关通过。最终SHA256=c4b70eb3d537921cabb4982559c82f3931e4f9ebc3217fd0061e8f17b10cd9c0，签名/P16/安装拉回哈希通过，仅classes2.dex变化，临时Trace逐字节恢复，129项暂存patch保持，MEMORY.md未更新。下一项定位首屏GL剩余约1秒中CELL_CONTENT_CREATE的资源解码/纹理创建实际调用，先细分归因，不再重复本批来源快照、磁盘缓存或无条件延后页实验。Folder性能仍暂停；Android9/三星Share/全ROM/首装/长稳/真实16KiB缺口保留。证据build/startup-compose-source-20261022。


**10/22第十四批当前：最终纹理磁盘候选已否决，过期纹理键门禁已最小修复。** 在Android16真机V2458A完成原/候选/空缓存/反向原/门禁修复各5样本。磁盘候选稳定命中67张时PAGE_READY中位1183ms，但受控空缓存1423ms，初始原1339ms、反向原1351ms；首次无缓存更慢，因此撤回全部缓存生产改动并清理测试文件，不再将这条路线作为当前首启优化推进。另确认e.s入口仍硬编码v18，当前Java已v30，导致完整纹理键被重复生成；改为调用Java唯一版本判断，普通/过期键仍构建，保留调用方已解析的当前键。实际入口Smali前缀18检查与旧分支负控通过，有完整日志样本键生成138→70；修后5启动1341/1288/1308/1265/1313ms，中位1308，较相邻修前1351约少3%，不能将整个差值视为已完全隔离的代码收益。最终正式包五轮图标/底部上滑搜索/准确settings查询/设置/返回及文件夹开关通过，首次8页往返无>50ms GL帧；修前反向原/修后13个静态区域像素一致。最终SHA256=59031d278cf0c08f345731399d84376bfd362f7862df5766a14e41c4df1393d4，签名/P16/安装拉回哈希通过；永久生产仅e/s.smali与IconRasterDiagnostics.java，本批无新缓存/线程池/数据协议，临时诊断与持久化Owner逐字节恢复，129项暂存patch保持，MEMORY.md未更新。整体冷启动仍开放；下一项核对跨纹理键生成与正式合成的重复来源解析，区别于本批入口门禁、先计数再最小修复，不重复磁盘缓存实验。Folder性能仍暂停；Android9/三星Share/全ROM/首装/长稳/真实16KiB未验。证据build/startup-final-cache-20261022。

**10/22第十三批当前：缓存持久化准入核对完成，未上线缓存改动。** 提取现有来源解析/纹理键方法，在API36只读模拟器两个独立ART进程各跑480组/1684检查，圆框、透明主题、逻辑/物理尺寸、surface、geometryRevision、宫格、分类、阴影、光影、用户及既有来源替换规则通过；相同安装元数据跨进程键一致。删除圆框区分的负控按预期失败。实际Android Bitmap构造出不同像素但相同32位摘要的反例，非Bitmap颜色改变也未进入类名/尺寸/身份摘要，故禁止直接将当前进程纹理键当作持久化完整性协议。旧三列为带阴影成品，data1～3还参与快捷方式备份/恢复，不因当前为空就占用。未改生产源码/APK/DB协议，没有新五启动或安装/功能回归，也不声称提速；冷启动仍未解决。下一项只做既有Owner内版本化最终PNG磁盘候选：先证明来源强身份、表示/版本、负载SHA256、原子发布、容量与恢复失效，再决定接入；不得先把旧PNG当RAW。证据build/startup-cache-validity-20261022，正式APK仍aa336816…，129项暂存patch未变，MEMORY.md未更新。真机/Share/全ROM/长稳/16KiB缺口保留。

**10/22第十二批当前：** 已修图标数据库保存结果误报：data/a/e只在SQLite更新命中/插入非-1时成功，e.s.a失败告警但保留内存字节，异步日志改CACHE_READY避免冒称落盘；没有新缓存/表结构/重试或页面时序改变。实际e/V/U与完整caller方法+Android SQLite的16检查、第二进程3读回、旧writer/旧caller两个负例及补写队列通过；修正了第十批接口变化后过期的队列夹具，PM/源生成/入口仍为夹具，不是完整存储故障UI。实际应用22条缓存跨原/最终各5启动内容哈希一致，旧三列成品与private iconData有读取链，尚无带版本/来源/尺寸身份的RAW跨进程恢复协议，不是已确认写库丢失。最终API36只读模拟器5启动中位2259ms、正式包五轮图标/底部上滑搜索/设置回归通过，未称提速；拼音恢复。当前SHA256=aa336816dd9bb78b0af196bb13a20cc46fd83fad4bccaa5f06340453c4a1ec72，构建签名P16及安装哈希通过，129项暂存保持，MEMORY.md未更改。冷启动仍开放；下一项为现有Owner下版本化RAW/纹理持久化协议及失效/容量/恢复证明，不能直接塞旧成品或重复延后翻页。真机/Top5/Share/全ROM/长稳/16KiB未验；详见开发日志第十二批、build/startup-source-roundtrip-20261022。

**10/22第十一批当前：后续页延后候选已否决并完整撤回。** 纠正“只有前两普通页图标初始化”的旧归因：旧统计只覆盖两页，真机实际9个普通页构造时均提前g.create；约640ms主要在余下工厂循环，阴影预载<1ms，Dock约33ms。原/候选/反向原同诊断各5启动中位1325/847/1335ms，但候选首次向前8次翻页出现7个50～173ms长帧，原/反向原同一路径约11～13ms且无>50ms帧，故未交付。候选仅复用ka既有Hn/oo初始化，没有新增缓存，但确实把工作移到首滑；所有实验/临时诊断源码均逐字节恢复。恢复build.bat/签名/P16/安装拉回哈希及正式包五轮图标/常用应用/底部上滑搜索/设置回归通过；恢复APK与原3b827…非签名ZIP全相同，重建容器SHA256=23a889a4cf370d57ef8f2dbf99edb99c3bc1591002eb737f68ed1fe4856ddb20。129项暂存patch保持，MEMORY.md未更新，系统日志保持开启。冷启动仍开放；下一项核实既有异步源补写是否实际持久化并在下次加载恢复iconRawData，先跨两进程读写对照，不重复无条件延后/旧成品直接套用。完整15样本、9页往返、日志漏采与诊断边界见开发日志第十一批、build/startup-bind-tail-20261022。其他ROM/三星Share/首装/长稳/16KiB等缺口保持，Folder暂停。

**10/22第十批当前：** 已否决将旧 dark/light DB 字节直接复用为当前最终纹理（含旧阴影/几何且缺少现有失效身份）；在既有静态合成调用内借用合格 ARGB_8888 BitmapDrawable，保持 DEFAULT 圆框和所有权边界，无新缓存。cached274/uncached311原生检查、两负例、13静态区域像素一致、构建签名安装哈希及真机五轮图标/常用应用/底部上滑搜索/设置回归通过。Android16 V2458A原/最终五次PAGE_READY中位1351/1361ms，GL wall1139.359/1134.758ms、CPU1038.927/1038.559ms；SOURCE_RASTER计数17→1，但未证明整体提速，冷启动仍开放。无日志与cached-only原型保留，不混入有效组；系统日志按用户授权保持开启，5个诊断标签I，其他设置保持。当前APK=3b8276618a2f220b0fb35f91cc4f855aef2d8563c54518cb913a988ed8b2b9be，129项暂存patch保持，MEMORY.md未更改。下一项 Eb.Vh 内两页初始化后至绑定结束约640ms的真实调用；Folder暂停，其他ROM/三星Share/首装/长稳/16KiB仍待验。完整细节和失败边界见开发日志第十批及build/startup-persisted-icon-audit-20261021。

## 2026-10-21 第九批实验撤回与原包恢复

软件准备移交候选的81项实际Batch/选择/代数/清理代码+原生Bitmap检查、坏键负控、既有主机预览167通过。最终Composer/调度Owner为夹具，真实首屏11静态区域与原包像素相同、有效五次每次21个take；不是主题/分身/光影/多ROM或真实首装矩阵验收。候选PAGE_READY中位2206ms而原/反向原1751/1800ms，性能不准入，已经撤下全部实验源码和正式测试入口，原包0afe93ba…恢复，恢复构建非签名ZIP内容与原包相同，签名/P16通过。

恢复基础回归首次因Gboard拼音把settings变为“s额头听说”失败，窗口和截图留存；临时切同一键盘English保证准确词，重跑五轮并恢复拼音，结果见build/startup-raster-handoff-20261021/functional-five.json。恢复后实际路径是图标/桌面设置BACK/底部上滑搜索/准确settings/结果图标及启动/返回；不把失败轮伪装通过，不给撤回候选补算未做的主题验收。129项暂存实验前后patch保持，无add/reset/提交推送，MEMORY.md未更新，详情开发日志第九批。

## 2026-10-21 第七批：目录投递/查询/分页/恢复一致性

生产仅IconLibrarySearchPage/IconPackManager，补齐目录身份与查询snapshot generation/epoch的MAIN投递判断；保存状态不再把旧rows挂到新peek目录，恢复/索引ready拒绝旧实例。旧源码15组中10组失败，修后实际四个完整方法在受控worker/MAIN夹具中15组25检查通过；普通IO不自动重试，暂停/换owner/旧请求仍丢弃。实际ART目录SQLite164、构建失效31、生命周期16、主机预览167通过，旧Manager负控准确失败。不是全Android真实UI并发故障注入。

build.bat/签名v1-v3/P16/v1.5.8/33与安装拉回哈希通过，SHA256=0afe93ba559f3b5b4b16a2610071d65e5338acbd5d4ae9158b86bd2de64a51d4，仅classes2.dex非签名成员变化。API36模拟器五轮基础图标/设置/底部上滑搜索/结果启动返回，同PID4942、截图核对及限定日志无fatal；实际图标目录chrome 48项、滚动/系统设置BACK状态保留。48结果未跨60项边界；已有坏包夹具失败仍记录。五启动中位2185ms，首轮实际取消、另4轮ready，冷启动不宣称解决。真机/Share/Top5/长稳未验，Folder暂停。100暂存项保持、MEMORY.md未更新，详情开发日志及build/catalog-delivery-20261021/。

## 2026-10-21 第六批：目录构建中失效不重新发布旧标签

旧源码闩锁负例准确失败；修后实际Catalog在API36 ART中31项通过，测试副本仅插入快照闩锁/合成标签与资产流关闭计数，未改真实安装应用。单次/连续失效、非阻塞MAIN失效、明确取消、并发只重建一次及新标签/流关闭通过。原目录159、页面14、主机预览队列167项通过。构建/v1-v3签名/P16/v1.5.8/33与安装哈希一致，SHA256=09f59081322a9bc68105c56ffd4fd49dd90bb968a023bb6b7cbfec92d3a00155。

正式包五轮图标/设置/底部上滑搜索/settings提交/结果图标与启动/返回通过，PID4778、截图核对及限定日志无fatal。实际图标目录Chrome查询由在线4项推进到包就绪日志48项，保留既有坏夹具pack6失败；没有改图标选择。五启动中位2194ms，首轮真实取消过期目录、其余4轮ready；不称五轮目录均成功或冷启动已解决。真实同进程“取消后页面重建”未现场重现，恢复证据来自ART用例。已发布引用到页面回调的失效仍待下一项；Share/Top5/真机/全ROM/长稳未验，Folder暂停。MEMORY.md未更新，100暂存项保持。证据build/catalog-generation-20261021/。

## 2026-10-21 第五批：目录预热线程归属与可见解码隔离

构造实际提交语句及既有request/session/queue方法：主机/ART各167项通过，Catalog/Bitmap/cache/network为受控夹具。阻塞目录+一个decoder，旧源码可见loader不能开始，新源码可开始；去除pauseP2保护的负例也准确失败。真实APK五次ready tid对应icon-directory，旧五次为icon-preview，每次5199条且一条ready；不是全目录内容/安装更新/多语言矩阵验收。

build.bat/签名/P16/v1.5.8/33及安装拉回哈希一致（935efbeecd8bd4ed047651f3b44e0f9b144e55295bcd8e0ddec1815279c5c149），只有classes2.dex非签名成员变化。API36硬件模拟器五轮图标/设置/BACK/底部上滑搜索/settings提交/结果图标/系统设置及显式前台返回通过，同PID5406、限定日志无fatal、截图人工核对。旧/新启动中位2146/2030ms，GL构建帧wall几乎相同，不认定全局提速；真机/三星Share/Top5/全手势HOME/长稳未验。100暂存项保持，MEMORY.md未更新，模拟器测试后关闭。详情build/startup-directory-owner-20261021/；Folder暂停。

## 2026-10-21 第四批：实际原版阴影Smali像素与回收回归

363组原生Bitmap/Canvas/BlurMaskFilter逐像素对照、6267检查通过；实际Smali无遮罩模型替代，公开入口和双色核心尺寸/像素等值。完整trace确认Alpha4→3，局部跟踪副本确认padding成功路径释放、输入/输出存活，旧源码/错误mask两个负例准确失败。58选择管线+24主题+44交接保护检查通过。128px/300次暖态单色微基准不作全局性能结论；早期小样本CPU零值已排除。

build.bat/签名/P16/v1.5.8/33及正式安装拉回哈希一致（be4cb7f019cfef1ac66ba9aa527b606999edab8634cf5fa02fc7385a5560199d），实际指令变化限两个L.a，其他非签名成员仅classes.dex。API36硬件模拟器五轮桌面图标/设置/BACK/底部上滑搜索/settings提交/结果图标/系统设置启动和返回通过，同PID5994/限定日志无fatal，截图人工核对。旧/新五启动中位2208/2172ms，不证明稳定整体提速。常用应用关闭、三星Share/真机/Android9全主题/光影/全手势HOME及异常中断/长稳仍未验。100暂存项保持，MEMORY.md未更新；模拟器测试后关闭，Folder暂停。证据build/startup-shadow-20261021/。

## 2026-10-21 第三批：诊断扫描局部复用验收

实际composeTexture/scanner/report源码配Android Bitmap/Canvas，1007场景8056检查通过；普通图3→2扫描、加角标/像素变更3→3、重复报告2→2，像素/诊断文字/输入所有权一致。受控projection/shadow/geometry/profile不等于原版全矩阵像素证明。旧源码及无generation保护两负例准确失败；负例入口早期只报shell Killed，补明确异常输出后重测，并非Launcher业务崩溃。既有LocalCompose246+Uncached289通过。

构建/签名/P16/最终安装拉回哈希一致（ca7c3c809767cfc0eba9c17d96b116d547472cad7e52254760c3b6c5a17ad266）。API36硬件只读模拟器五轮图标/设置/BACK/底部上滑搜索/输入settings并提交/结果图标及系统设置启动/显式前台返回通过，同PID5728，限定日志无fatal。最初最终截图处于系统转场，保留后补焦点及稳定截图复核正常；不称瞬时返回无闪屏。常用应用未开启、三星/真机/全面HOME/多主题分身仍未覆盖。旧/新五启动中位2368/2138ms，CPU未同步改善，整体冷启动未解决。证据build/startup-bounds-20261021/；MEMORY.md未更新，100暂存项保持。

## 2026-10-21 第二批：颜色分类最小修复回归

生产仅f.d对≤64×64图批量读像素，原分类/顺序/大图路径保留；实际Smali+Android Bitmap 303等值/所有权/异常用例、4096→1完整方法计数和旧源码负控通过，81手势合同+4工具兼容通过。首轮合并计数trace截断，未作成功证据；最终分开追踪且检查每个d完整退出。构建/签名/P16/v1.5.8/33及最终安装APK哈希一致，SHA256=a4b23942db8647478a6e1bf87161ee8c03f6dd5515a372772532ae8057203711。

API36硬件只读模拟器五轮图标、桌面设置、底部上滑搜索、settings提交/结果图标、启动系统设置及BACK/显式前台返回通过，同PID6899，截图人工核对/限定日志无fatal。测试有0.6秒转场等待，不宣称立即首触摸/全部HOME手势/Top5/三星Share/真机/全主题矩阵通过。旧/新/反向旧各5次启动中位2450/1761/1734ms，无稳定整体启动收益证明。暂存100项保持，MEMORY.md未更新；Folder暂停。详情同日开发日志与build/startup-gl-cpu-20261021/。

## 2026-10-21 API36只读模拟器启动与回归工具

5次带系统trace的冷启动和缓冲锁存关联完成，主包未改；不称冷启动已修。修复TouchInput工具在API36的InputManager旧反射入口NoSuchMethodException，仅该异常时用InputManagerGlobal，旧入口保留。实际旧源码负例失败，新源码81手势合同+4兼容夹具场景与API36实际注入通过。新旧API夹具不等于本轮Android9设备验收。

正式343fd257…包最终5轮桌面设置、底部上滑搜索、Gboard组合文字提交、结果图标/启动系统设置和返回，同PID6279、限定日志无fatal。稳态组转场等待0.6秒只用于测试节奏，不计首次交互延迟；单次即时输入另5组中1组时间线不完整，不称全量精确输入测量。AVD常用应用原未开启，不记Top5/三星Share。原坐标越界、focus子命令、旧工具崩溃等失败样本均保留，非Launcher故障结论。100暂存/原APK保持、MEMORY.md未更新，证据及剩余限制见同日开发日志与build/startup-visible-api36-20261021/verification.json。

## 2026-10-20 统一验收：本地SAF与正式包五轮

V2458A/API36真实专用目录授权、3048126字节导出/COMPLETE、74成员ZIP CRC、恢复预览回读9页/2文件夹/70应用、预览取消、创建partial后复制入口取消、同名拒绝且hash保持、撤权后错误重选入口与取消已验证。未执行开始恢复。全线程调试暂停曾诱发ANR并被用户结束；失败样本保留，改event-thread自动取消通过，不能把诊断ANR当正式包故障。撤权后pending保护生效与无pending时权限提示分开验证，测试日志手动隔离有明确记录。

21组主机/Android隔离套件最终通过；正式343fd257…包五轮上滑搜索/常用图标/查询结果启动/桌面设置BACK同PID25008通过、限定日志无fatal。末尾按用户确认恢复“尚未选择/上次备份暂无”，本次新增树授权全部撤销、测试目录清理、旧撤销快照hash不变、正式包恢复。临时诊断标记已撤除，100暂存保持，MEMORY.md未更新。证据build/consolidated-acceptance-20261020/verification.json、regression-final.json、formal-five-rounds.json；细节和未验矩阵见开发日志同日“连续验收收口”及专项计划顶部唯一入口。冷启动/暂停Folder/跨ROM/严格16KiB/长稳/完整恢复未关闭。

## 2026-10-20 A07 SAF权限失效分类和目录重选

两保存路径在SAF边界将直接/包裹SecurityException归LOCATION_PERMISSION_LOST；rename权限拒绝不走第二目标fallback，普通IO/本地快照权限异常负控保持原分类。两错误展示入口共用原风格提示，用户点击后才openBackupTree(false)，不自动授权或继续旧预览。636导出/104场景+8实际UI方法夹具+85撤销+122worker，共851项通过；模拟撤权不可清理保留URI及恢复后仅清候选，旧文件/元信息保持。

构建签名/P16/v1.5.8/33通过，SHA256 343fd257b9b13abb989ff9d09bcb67ab61cb7d242152260e6755abb7ec937bea，仅classes2.dex变，100暂存不变。V2458A/API36保数据安装/拉回哈希一致，基础启动/设置/备份页/底部上滑搜索回归通过；实际共用系统picker打开并BACK取消、位置仍未选，未grant或执行备份。新错误弹窗和撤权流程是夹具验证，非真机故障注入。下一项：专用SAF目录端到端导出/回读/取消验收，新增授权需先明确允许，详见开发日志。

## 2026-10-20 A07上次备份记录发布顺序和失败恢复

先确认COMPLETE再写上次备份信息；提交尝试后保留文件/日志，实际未完成由原恢复入口清本次候选，实际已完成则补写记录。偏好失败明确metadata pending，COMPLETED文件不删；新字段completedFileName可选，旧COMPLETE兼容，完成时间取checkpoint且重试不漂移。两条保存路径均提取实际方法测试，491导出/81场景+85撤销+122worker共698项通过；包括前后文件/元信息保护、回读失败但已提交、补写阻塞和新Context重建。

构建签名/P16/v1.5.8/33通过，SHA256 35c6cf9daa6cb47d93d9cf45b73d0c28da55888b9e9634bbaecb9052d6ee7a2e，仅classes2.dex变、100暂存不变。V2458A/API36保数据安装哈希一致，启动/设置与只读备份页/底部上滑搜索基础回归通过；故障仅JVM夹具，不称真机SharedPreferences失败/实际进程重启验收。下一项为导出中权限失效的错误分类和目录重选入口，详见开发日志。

## 2026-10-20 A07备份日志同步与写后回读确认

写入流程复用Restore日志的FD.sync及字节回读，只在全部确认后更新Entry/返回true；候选大小提前限制于读取上限，failWrite自身异常不掩盖首错。356导出/64场景+85撤销+122worker共563项通过，原54场景保留，新含静默finish、sync失败、读回失败/字节不一致、超大候选、失败Entry不提前发布、COMPLETE/IDLE/PREVIEW静默失败及首写.new保护。AtomicFile/JSON/provider故障是JVM夹具，非真实Android磁盘故障验收。

构建签名/P16/v1.5.8/33通过，SHA256 e2231f7af98254a0d2c37c6f5bb211531d5335239a430459b3a434e3b8c63500，仅classes2.dex变、100暂存不变；V2458A/API36保数据安装哈希一致，正常启动/设置与只读备份页/底部上滑搜索基础回归通过，同PID、限定日志无致命或日志错误，未实际备份恢复。下一项修上次备份时间/名称/URI先于COMPLETE提交、失败后可能指向已删文件的边界，详见开发日志。

## 2026-10-20 A07备份日志严格读取与证据保留

旧源码负例证实坏日志被当IDLE。现区分真正无文件与base/.bak/.new存在但不可读；缺字段/未知state/IDLE带资源拒绝，write/reset预读保护原证据。新备份准入明确回调两错误并释放锁；预览后保存的错误记账读失败也不会吞完成回调。state/预览checkpoint检查返回，成功后才发布预览。314导出/54场景+85撤销+122worker共521项通过，含正常缺失/.bak恢复/旧可选字段和原SAF回归。

最终完整构建签名/P16/v1.5.8/33通过，SHA256 67b4e922fcf406a446306072cdcfb96cfa3fb9467d9c161544b04c5563a68b3a，仅classes2.dex变，100暂存不变。V2458A/API36保数据安装哈希一致，正常启动/图标/设置/只读备份页返回/底部上滑搜索常用图标回归，同PID及限定日志无fatal/Journal异常；未在真机造坏日志或操作备份恢复。Android JSON/AtomicFile故障仍是JVM夹具。下一项为finishWrite静默失败的FD.sync和写后回读验证，不把本批说成持久化/真实SAF全部安全完成，详见开发日志。

## 2026-10-20 A07 SAF回退临时文件交接 + Android16真机基础回归

partial删除拒绝后原实现仍报成功并丢失追踪；现复用deletePendingDocument，确认删除或成功空查询后才交接最终URI，否则FAILED/pending且保留两恢复URI。247导出/39场景+85撤销+122worker共454项通过；包括两目标均拒绝删除、查询异常/null、清理后checkpoint失败重试及delete假false/真缺失。真实provider故障仍未验。

构建签名/P16及v1.5.8/33通过，SHA256 950d2d82072097bc76a1e6e0d46d75a5bc80f03b1e5297d85277e2fbcb77e968，仅classes2.dex变，100项暂存不变。V2458A/API36保数据安装成功、拉回哈希一致；图标/文件夹开关、底部上滑搜索常用图标、settings查询及系统设置启动/BACK回Launcher、桌面设置/BACK通过，同PID且限定错误日志无fatal；无真机备份恢复。TouchInput shell被杀后改平台input实际打开搜索，工具按哈希清理，回原桌面页。未改布局/主题/刷新率/导航/默认桌面/权限，Folder性能仍暂停。下一项为损坏BackupOperationJournal被read当作IDLE，详见开发日志。

## 2026-10-20 A07 SAF启动清理拒绝删除与后续重试

实际cleanup保留未删除URI/路径及非终态，成功后才检查IDLE写入；删除后checkpoint失败可用成功空查询确认缺失，null/异常不算缺失。新预览/直接导出worker持原操作锁先清理旧journal，未完成不覆盖，释放瞬时锁并提示pending。COMPLETE成功备份不删。184导出+85撤销+122worker，共391项隔离检查通过；provider/UI为夹具，真实SAF/重启/权限恢复未验。旧源码负例已证实拒绝删除后journal丢失。

构建签名/P16及v1.5.8/33通过；SHA256 50b43d9ee4c0318c0cea142800de24434fda9b61575f8fba645e8b60fc77950e，仅classes2.dex变、100暂存不变。ADB无设备未安装，MEMORY.md未更新。下一项：fallback成功后partial删除失败是否丢失追踪；同名安全替换、损坏journal和真实provider矩阵仍待办，详见开发日志。

## 2026-10-20 A07 SAF同名保存保护（安全覆盖仍未实现）

修前负例证实覆盖后取消删除旧文档。现Controller检测到同名即拒绝，保留旧文件并提示换名；SettingsHost同步去掉覆盖确认、保留预览。严格后台目录枚举在null/异常时停止创建，避免查询失败被视作目标不存在。当前明确禁用同名覆盖，不算完整替换协议验收。

实际方法/真实JVM IO及provider夹具160项/24场景，撤销85、worker122，共367项通过；保留既有20场景断言。构建、签名v1-v3、P16对齐及版本v1.5.8/33通过；SHA256 a79e13dd8937a0ab163778694d95b0657b0469288cc12c741c3ffde9f3fd9ab6，仅classes2.dex变，100项暂存不变。ADB无设备，未安装，UI换名/真实SAF未验。并发目录改动、非事务provider、删除拒绝/日志损坏仍待办。下一项：清理失败时保留待清URI和journal，避免失败却reset。详见开发日志。

## 2026-10-20 A07 SAF导出失败清理、URI追踪及取消状态

写入Owner内部清理本次partial/第二目标，返回后的调用者使用实际finalUri；rename后更新日志，fallback复制期间用可选destinationUri记录第二目标，启动清理两者。预览保存取消归CANCELLED而非普通复制失败。旧源码负例复现.partial遗留；实际方法+真实JVM IO/日志/锁及受控provider133项/20场景、旧撤销85、worker122通过，共340项。真实SAF/进程终止/provider删除拒绝未验，当前ADB无设备，未安装或动用户备份。

构建签名/zipalign-P16/v1.5.8/33通过，8bb7d2b0df9dac5745ee4057e474353e3c44041a700673bb88936b531e667e1b，仅classes2.dex变、100暂存不变。覆盖同名目标仍在写新文件前删除旧备份，下一项优先处理；不得将本批称为全部SAF数据安全完成。MEMORY.md未更新，详细边界见开发日志。

## 2026-10-19 A07旧撤销快照取消保护与token释放

新快照独立preparing_TOKEN，取消/失败不删除旧撤销包；成功恢复后复制/FD同步/SHA校验/Os.rename原子发布，候选保留至journal耐久reset，启动Guard可完成发布或清理。Lock修复等值String token无法CAS释放，过期token不能释放新owner。两项旧源码负例复现；新85/原checkpoint144/worker122最终JVM351项通过，Android9隔离112项（含EACCES、进程SIGKILL、新进程发布恢复）通过，用户PID7133保持。

旧AtomicFile发布尝试因API28真机rename失败后可继续写目标而撤回，最终使用Os.rename；失败日志保留。构建签名/zipalign-P16/v1.5.8/33通过，8b782490cdaf6d615cb4e1a3b8f3e7f80da9b317ac981ba114502ea80b83a36e，仅classes2.dex变，100暂存保持。未安装/恢复用户桌面，完整真实SAF/硬断电/多ROM未验。下一项SAF导出取消/写入中断及未完成文件清理，MEMORY.md未更新，详情见开发日志。

## 2026-10-19 未匹配原图圆框按实际来源修复

用户确认回退应用原图没有圆框。旧Host按所选IMPROVED/PACK等否决，现Raster将既有effectiveType传入同Owner判定，命中managed不加框，DEFAULT回退遵循开关；不写图标选择。实际函数/Android Canvas334、Renderer59、准备合成289通过，旧Host负例IMPROVED失败。正式45859fbfc475cc53b0ef7b3ede348a64964ee13e165da3ce28d007cdcf11e056保数据安装/拉回一致；一次Folder/搜索实际查询启动/BACK/桌面设置通过，同PID7133，不改配置，原100暂存保持。

恢复checkpoint144/worker122通过，未新增备份生产修改；旧撤销包在新快照创建前被替换的取消边界未解决，下一批优先。完整图标包/下载真实时序、多ROM/长稳与真实恢复仍开放，Folder性能暂停。详细证据与范围见同日开发日志，MEMORY.md未更新。

## 2026-10-19 A07结构前置校验与环检查

Exporter.validate复用Topology，孤儿引用从导入前提前至预览校验拒绝；Importer已有写前检查保留。Topology源/DB共用迭代查环，补自引用/双向环，保留无环旧关系。实际Android9隔离SQLite143检查（含原120）、checkpoint144通过，共287；异常源未改隔离表/页面/pending，12000节点无递归溢出，无环及共享链不误拒。修前负例是probe断言失败，非用户桌面崩溃。

构建签名/zipalign-P16/v1.5.8/33通过，82e244dac24e2e698b49d8d8345593f6ef20b71cf1f0873e83f4a56a7b8ca7ff、仅classes2.dex变，100暂存保持。未安装/恢复用户数据，PID5750保持，本批三处测试目录精确清理。完整真实归档/SAF/断电/多ROM仍未验；下一项取消/失败后临时文件及锁清理。MEMORY.md未更新，详情见开发日志。

## 2026-10-19 A07纯文件夹页面预览计数修复

Reader错误将folderIndex=0的根文件夹当子项排除，纯文件夹页显示0；现按既有itemType=2规则计入。仅改预览页数谓词，不改Importer/格式/布局。修前负例失败、修后52预览与25偏好检查通过；API28独立app_process/真实SQLite跑既有页面120项，通过12/20、槽复用/事务回滚、根文件夹占位及实际Exporter→Importer往返。共197检查，Launcher PID5750保持，无安装或用户桌面恢复，临时隔离目录已移除。

build.bat/签名/zipalign-P16/v1.5.8/33通过，SHA256 55eb69082e01dc88ab86b7336e0449b6f6bb9589258004325fb39d3265e647c9；100暂存保持，原Folder classes.dex不变。完整真实备份/SAF/断电/多ROM未验；下一项异常页面/文件夹结构的写前校验，Folder性能暂停。证据及边界见同日开发日志。MEMORY.md未更新。

## 2026-10-19 A07缺主题回退持久化失败修复

生产仅DesktopRestoreController补齐旧主题回退commit返回值检查，失败进入现有回滚，不继续正向图标/壁纸阶段。新增隔离31检查/5场景与修前负例；checkpoint144、worker122、偏好25通过，总322项。build.bat、签名v1/v2/v3、zipalign-P16、v1.5.8/33验证通过，ed227fe97533c1d30d5aebea74310fbeb5e5485333aebf82539487386d6b9ecb，相对1bb4仅classes2.dex变化、100暂存不变。

未安装/未恢复真机用户数据；测试使用实际Controller/Journal/锁/文件实现，DB/归档/Android边界为夹具，不称全恢复验收。A07旧档/SAF/真实断电/分身及多ROM仍开放；Folder专项按用户要求暂停。下一批旧格式缺省字段和页面/文件夹兼容，详见开发日志和build/restore-theme-fallback-20261019。MEMORY.md未更新。

## 2026-10-19 Folder创建当帧动画步长修复

Ra.T/Eb最小补齐新Folder首次动画门，原输入/事件/物理delta保持；实际Smali346及数学64通过，旧源码负对照失败。API28同两应用Folder诊断五次首步统一约20，录像人工前后帧确认首个展开大小一致；五对完整非状态栏静态画面零差异。正式build.bat成功、v1/v2/v3签名及zipalign-P16通过，安装拉回1bb4与根产物一致、仅classes.dex变、无临时诊断标记、100暂存binary patch不变。实际五轮功能结果见同日开发日志补充及build/folder-visible-motion-20261019/formal-ui。

修复不代表打开前CPU阻塞关闭；正式五次仍约72–84ms最大GL。API36/高刷/动态图/九实际应用/TNT/多ROM/长稳未覆盖。下一项验证已适配几何能否按实际输入安全复用，保留布局/主题变化失效，不新增常驻完整场景或Bitmap缓存。MEMORY.md未更新。

**正式功能回归补充：** Android9 X21A正式1bb4五轮同PID1252完成原两应用Folder打开/关闭、图标检查、Dock底部上滑搜索（250/450/700/350/900ms）、实际settings查询及系统设置结果启动、BACK、桌面设置/BACK；已人工查看五组Folder/查询/结果/桌面设置截图。采集窗口无FATAL/Launcher ANR标记。最终回桌面首屏，测试touch DEX移除；未调整默认HOME/布局/主题/权限/导航/刷新率。安装拉回hash一致、临时源码恢复、100暂存binary patch保护通过。此项不覆盖动态图/多页应用/Android16高刷/多ROM长稳；Folder CPU等待仍开放。

## 2026-10-19 Folder绑定细查完成，无新增生产改动

正式4b1/API28两次预热后五次最大GL为75.482/69.272/89.549/77.868/85.881ms，仍有CPU长帧，不与上批会话作速度收益比较。临时逐节点五组确认：2次实际应用纹理/键解析、19次Ba节点；create进入18次，其中9次受iH保护立即返回、合计仅0.044–0.054ms，实际构建9格。动态同步与阴影合计0.407–0.672ms、文字构造1.832–3.523ms，均不足以支持删减原兼容/绑定流程。父子分段不能累加，插桩数据不当正式性能对照。

没有新增可复现错误或重复工作的证据，不强行做亚毫秒微优化；clean/raw/maintained参考已核对，原APK归档缺失未冒称新反编译。所有临时源码、helper及四份正式产物恢复；4b1保数据恢复拉回hash与基线一致、无FDIAG/FCPU_PROBE，五轮Folder/实际settings搜索查询启动/BACK/桌面设置同PID27301通过，UI窗口无FATAL/Launcher ANR标记。配置/布局未改，当前100项暂存binary patch保持，无add/提交推送。MEMORY.md未更新。

本项绑定审计收束；下一项串联同次触摸UP→同步准备→GL/EGL提交→首个运动buffer，定位可见停顿，未证根因不改生产。Folder卡顿/冷启动未解决，本轮API36/多ROM/高刷/动态图/九实际应用/长稳未验。完整分段、失败边界及证据见开发日志最新条和build/folder-cell-bind-20261019/verification.json。

## 2026-10-19 Folder同次几何计算复用：局部下降，整体卡顿保留

正式API28最大帧CPU初组73–92ms，诊断定位9格adjustY和adaptPositions重复验证/计算。仅FolderCellPositionAdapter和FolderVisualGeometry：原身份检查后复用同一调用的几何计算，公开入口/失败回退/公式保留，无跨帧缓存/动画改动。839对照坐标float bit一致，mode查询2700→1548；64/12时钟/Surface及图标审计通过。clean/raw/maintained已核对，原APK归档本轮缺失，沿用已保存原机证据，未冒称新反编译或操作原机。

旧5d2/新4b1均两次预热后各五次同Folder100ms短按：最重帧CPU中位85.196→76.594ms、GL墙钟91.849→83.090ms，五对非状态栏静态画面逐像素相同。最坏仍94.379ms，未锁温控/调频，不称稳定整体提速或输入到物理首帧闭环。首次未预热组、寄存器/非debuggable trace及ART失败样本分开保留，不按速度筛样。

正式4b1cd416/v1.5.8/33构建签名/对齐、保数据安装拉回hash一致，仅classes2.dex变化、无FDIAG/FCPU_PROBE。五轮Folder/实际settings搜索查询并启动结果/BACK/桌面设置通过，同PID21272，UI窗口无FATAL/Launcher ANR标记。配置/布局未调，临时helper移除，本轮基线97项暂存binary patch保持（历史53不套用本轮）。MEMORY.md未更新，详情与完整五样本数组见开发日志及build/folder-first-motion-20261019/verification.json。

下一项沿cell-create→folder-content-create→g.Ba同步绑定剩余开销推进，不重复已关闭的坐标数组/PM/hash/资源ID微优化。Folder整体卡顿、冷启动和Android16/多ROM/TNT/动态图/长稳仍开放。

## 2026-10-19 Android9搜索测试误判已查清，正式包五轮通过

旧自动化上滑失败由Android9 adb input swipe逐事件更换downTime触发既有异常流保护；临时诊断和AOSP源码一致，不能归因为Launcher业务故障。仅新增search_gesture/TouchInput.java与prepare_touch_input.py，提供同一downTime的shell输入；未删保护或改生产手势。81项隔离检查通过，正式5d2ac17e在API28五轮Folder/底部上滑/实际settings查询/启动结果/BACK/桌面设置通过，同PID16664，截图人工核对。CANCEL/短滑/坏流不打开，随后正常流可用。

诊断已撤除，正式安装拉回hash一致、53暂存逐字保留、临时DEX移除，未改配置或布局。捕获窗口无FATAL/Launcher ANR；不等于全手指中断/全ROM/长稳验收。此前搜索失败仅按当时样本保留，由本轮修正其归因。Folder初始停顿、冷启动和三星Share现场仍未关闭；下一项回到Folder输入至首个运动buffer阻塞。证据及源码链接见开发日志最新条、build/search-entry-20261019。

## 2026-10-19 默认圆框方底延展：同机效果及五轮返回通过

5d2ac17e/API28 X21A保数据安装；仅Renderer v8生产改动，opaque近方形PNG延展原边缘颜色，原完整图案矩阵不变，透明/不规则回退、自适应及managed选择门保留。59项Android Canvas检查通过，修前负例明确失败。11个实际源对照：抖音RGBA相同，其余中央区域和圆mask最大差1，不称全部逐像素相同；桌面天气/相册/电话/视频效果已看图确认，完整文字保留。

五轮Folder图标/开关、桌面设置/BACK同PID14877通过。签名/对齐、仅classes2.dex变化、保留53暂存通过，未改圆框偏好/来源/主题/布局/默认HOME。复杂边缘可能延展色带，多ROM/动态图/分身矩阵未验。搜索入口仍是上批未通过状态，本次未重测，不能称完整回归；Folder卡顿/冷启动未关闭。详情见开发日志最新条及build/default-circle-smart-20261019。

## 2026-10-19 图标包失效修复：Android9局部通过，搜索未通过

5297d96f/API28 X21A保数据安装拉回hash相同；原版锤子未操作。修前db14与修后各5次同两应用Folder有效打开，5对非状态栏静态画面像素相同；另5轮Folder图标/开关/桌面设置/BACK同PID11755通过。默认HOME为vivo原生桌面且未改，不把BACK或直接启动Launcher写作HOME返回。

搜索设置确认为开启，但Dock上滑未打开，查询/结果启动未执行，不能写完整回归通过。失效生产方法18项JVM边界通过，不等同实机图标包替换/卸载/选择矩阵；目录shell probe被Settings provider拒绝，旧总套件提取接口过期，均不计通过。下一项先定位Android9入口，再回到Folder初始CPU。用户主题/布局/来源/权限/刷新率未改；失败与有效证据见开发日志及build/folder-source-invalidation-20261019。

## 2026-10-18 Folder与桌面Surface高刷：最终包五轮功能通过

V2458A/API36最终db14d579，标准60/高120各5次独立时序采样及录像；实际SurfaceView显示间隔中位约16.6/8.3ms，系统标准模式未被Surface能力投票绕过。Folder推进按实际帧率归一化，保留原版曲线/资源/几何，逻辑时长未倍速。64时钟及12 Surface边界通过；API29/30/31仅隔离fixture，90/144实机及多ROM仍未验。

正式包5轮Folder图标/开关、系统设置返回、Dock底部上滑搜索、settings查询并启动结果、桌面设置返回，同PID27461通过；另5轮实际翻页/返回有截图差异与复位确认。同会话5对静态位置目视一致，最大通道差异2/255，未标逐像素相等。临时刷新率已恢复智能适配及原peak/min，应用高刷开关未改，60000ms锁屏不变，正式签名/安装拉回hash/无诊断/53暂存保护通过。

打开前CPU仍有50.873ms长帧，120Hz录像仍有374ms长样本，整体不卡及冷启动没有验收；外接/TNT/九应用/动态图/温控/耗电/长稳未验。原版手机未装包，本轮不可靠的原机录屏排除，不替代先前confirmed-route。详见开发日志最新条及build/folder-open-chain-20261018/verification.json。

## 2026-10-18 资源ID去重：正式包五轮及原机对照

V2458A/API36正式c034c864五轮Folder三图标/开关、系统设置/HOME、Dock底部上滑搜索、实际settings输入及启动设置结果、桌面设置/HOME，同PID4403通过。十对修前后完整非状态栏场景逐像素一致。80项真实Android资源表缓存边界、480组合/1665项键来源检查通过；晚到文件/删除文件/目录/variants保持实时，失效清理负例按预期失败。未覆盖动态图/九实际应用/拖拽/多ROM/长期争用或三星Share现场。

DT1902A原版8.0.4/API29原有两应用Folder五次有效开关，截图确认，同PID22175，未改布局或安装移植版；黑屏/瞬时tap无效样本排除。8个APK关键方法与clean/raw一致。原版与移植机不是同条件性能对照；仍未验首次运动/物理顺滑，不把静态图标相同当整体不卡。最终正式包签名/对齐/安装拉回hash、临时清理与53暂存保护通过；MEMORY未更新。见开发日志最新条与build/folder-resource-match-20261018/verification.json。

## 2026-10-18 Folder坐标复用修复：正式包五轮通过

V2458A/API36原有三应用Folder，25d0ab51→62e887e1。生产仅M.fn方法局部复用本次Folder坐标副本，三组实际获取9→1、点复制81→9，adjustY仍9、PM仍5/hash仍1。十对正式首开/再开书架及非状态栏场景逐像素一致。最终完整5轮Folder开关/图标、桌面系统设置返回、Dock底部上滑搜索/实际settings查询并启动结果、桌面设置返回同PID11664通过。不是九个实际应用、Folder内启动/拖拽/动态图、多ROM或物理顺滑验收。

初轮UI因电脑ADB服务连接中断失败，ui证据保留，完整通过记录另存ui-retry。修后第4次启动缺PAGE_READY日志但桌面正常，失败保留，后两组使用5秒+缩略图像素就绪门；日志缺口限制crash覆盖，不能视作完整冷启动通过。临时诊断构建/安装后已撤回，最终正式APK62e887e18f9133c23027710b9b4bcecebe80c36c80334eeaf10b0db65d5af0ed安装拉回一致，签名/对齐/无FDIAG/53暂存不变通过，未改布局与系统设置。根因、完整样本及未验矩阵见开发日志最新条与build/folder-scene-bind-20261018/verification.json。

## 2026-10-18 Folder系统trace与正式包恢复回归

V2458A/API36原有三应用Folder、正式25d0ab51。正式5组首开/再开系统trace，截图保留；5轮Folder开关及三枚图标、系统设置/HOME、Dock底部上滑搜索/实际settings查询并启动设置结果、桌面设置/HOME通过，同PID24725。临时诊断三组完成后恢复原正式包，另1轮同路径通过，同PID28021。没有测试Folder内部应用启动/九应用/动态图/跨ROM，不把截图或显示FrameTimeline当物理顺滑验收。

7个临时源码及正式产物恢复、安装拉回hash25d0ab51一致，正式DEX无FDIAG，原53暂存不变；未改布局、权限、默认桌面、日志/刷新等系统设置。UI采集窗口无FATAL/Launcher ANR匹配。无生产修复，不新报整体提速；旧长帧显示侧背压已找到直接证据，另两次22ms起始间隔仍开放。证据build/folder-buffer-wait-20261018/verification.json及开发日志最新条。

## 2026-10-18 Folder本次ResolveInfo复用与无用标签移除回归

生产仅Host，既有helper接收本次已确认组件，不跨调用保存；二次override和后续来源重查仍执行，公开普通加载每次仍解析。未使用的label参数传null，原选择方法正文忽略它，必要系统应用识别/显示标题读取不删。提取真实Owner/override/selected方法、真实Bitmap/ART与PM/来源夹具，480组合与当前基线逐一完整key相等、1670检查通过；涵盖源到达、元数据/安装变更、分身/组件旁路、标签异常、两次调用各自刷新及普通Drawable API。旧Host新负例在组件复用计数断言失败。三组实际Folder每开PM 7→5、无用label 2→0、内容hash保持1次。

正式修前/后各五组首开/封面关闭/再开，五对书架及非状态栏场景逐像素一致。五轮Folder开关→桌面系统设置→HOME→底部上滑搜索→实际settings查询/设置结果启动→HOME→桌面设置→HOME同PID19549，窗口内无Launcher FATAL/ANR匹配；不含Folder内部应用启动。修前/后录像各6秒。首开最大GL回调中位24.153→21.399ms，再开23.378→24.816ms，不能宣布整体性能已关闭；34.709ms长帧已定位为dequeueBuffer中的主要休眠等待，具体消费者/SF原因另查。

build.bat、v1/v2/v3签名、zipalign-P16、v1.5.8/33通过；最终25d0ab51437931a3caf6595c0864361c36fc2f63abb92c1851e7a7914acfece4，拉回包一致，相对c7ae5701仅classes2.dex变化。原53暂存binary patch不变，Raster/RedirectDB字节不变，正式无FDIAG，临时源码/产物均恢复；用户布局和系统配置未改。PM/标签重复工作局部验收，Folder可见流畅度/九应用/实际换包/动态图/全ROM及长稳未验。证据build/folder-source-resolution-20261018，MEMORY.md未更新，详见开发日志最新记录。

## 2026-10-18 Folder IMPROVED未命中回退修复与正式真机回归

生产只MaintainedLauncherSettingsHost.java：沿用原loadIcon Owner的强制原图/二次override/最终APK链，普通加载API仍返回图片；键解析才允许已确认APK回退使用既有指纹。Android16真机提取生产方法480组合/1185检查通过，覆盖回退时来源到达、缺元数据、安装替换、延后DB补写及真实Drawable API不变；旧Host在新IMPROVED未命中组合负例失败。PM/资源选择为夹具、像素/ART为真实平台，不等同实际在线到达或全部ROM。批量读取、弱哈希候选未采用；生产Raster与fb6506d5逐字节一致。

同一V2458A原有三应用Folder修前/修后各五组首开/封面关闭/再开有效，五对完整书架及非状态栏场景逐像素一致。无标记正式包另完成五轮Folder开关→桌面系统设置→HOME→Dock底部上滑→实际settings输入/核验EditText→设置结果启动→HOME→桌面设置→HOME，同PID3936，日志窗口无Launcher FATAL/ANR匹配。未在Folder内打开联系人等应用。各6秒开关录像保留，不把录像称物理触屏/显示时延证明。

build.bat、签名v1/v2/v3、zipalign-P16、v1.5.8/33通过；正式c7ae5701ac47ddd8d0f43607b28c11356ac2d58c35eaf289ae4d0c586b56a63d，拉回APK一致，相对fb6506d5仅classes2.dex非签名成员变化。正式DEX无FDIAG和撤回SourceHash类，临时源码/产物恢复，53项暂存binary patch一致，真机保留最终正式包/原布局/系统设置。首开最大GL回调中位28.655→16.922ms，再开36.739→23.334ms；再开仍超一帧，九应用、实际动态图/图标包替换、跨ROM/长稳及物理present仍未验。开发日志与build/folder-open-timeline-20261018保留所有失败及最终verification.json；MEMORY.md未更新。

## 2026-10-18 Folder来源键修复：Android16真机回归通过，整体性能未关闭

正式fb6506d5…/v1.5.8/33，仅Host/Raster生产改动；build.bat、v1/v2/v3、zipalign-P16通过，真机拉回APK一致。现有来源测试扩展到480组合/1168检查：Android9/16及新V2458A Android16真机均通过；安装/配置/资源/路径失效、未知元数据回退、受管到达、原DB补写不驱逐APK身份、分身旁路均有隔离用例，不冒充全部实际ROM场景。静态图标合同PASS，53项原暂存binary patch一致。

新真机用户已有三应用Folder，无布局改动、无虚拟机：基线/正式各五组首开/封面关闭/再开，每对同PID；五对书架及非状态栏场景逐像素一致。正式五轮Folder开关→桌面系统设置→HOME→Dock左侧底部上滑搜索→实际输入settings并核验EditText→点击设置结果并核验系统设置Activity→HOME→桌面设置→HOME，全部同PID14346，捕获窗口无Launcher FATAL/ANR匹配。此组未从Folder内启动应用；三星S25U Share现场、九应用Folder、动态图/图标包实际替换、压力/长稳、全ROM仍未覆盖。新真机ART采样因正式包不可shell profile被系统拒绝，失败留档，未改变系统设置。

模拟器旧批最终另有五轮Folder内启动设置/搜索实际查询/桌面设置同PID通过，但初始错误关闭坐标导致相机启动的工具失败不算通过；旧Android9修后UI/五组未完成。不把新真机成功覆盖其他设备未验项。默认来源重复加载局部修复完成，首开中位29.210→26.070ms、再开33.344→34.696ms，不认定全部卡顿解决。证据及边界见开发日志10/18与build/folder-device-api36-20261018/verification.json。MEMORY.md未更新。

## 2026-10-17 Folder首开与功能路径对照

当前88bab291…正式包在API36只读硬件GPU副本保留数据安装并拉回hash一致；未改源码，未重复构建。两应用Folder完成有效五组首开/封面关闭/再开，五对书架图标区域逐像素相同。另五轮文件夹内启动系统设置→HOME→封面关闭→Dock底部上滑搜索/关闭→桌面设置→HOME，同PID7006；UI捕获流无FATAL EXCEPTION。只验搜索入口，未验查询结果。图标静态合同PASS；暂存53项binary patch不变。

BACK未关闭Folder导致标题命名弹窗的早期整组排除，保留原图；有效valid/及ui/路径不与其混算。实际首开长帧仍在，未修复；采样定位/失效边界及原APK缺档见DEVELOPMENT_LOG当前Folder条目。真机未操作，未覆盖九应用、动态图/自定义/图标包、全ROM和SF可见帧。证据build/folder-first-open-20261017；MEMORY.md未更新。

## 2026-10-17 A25 图标库坏响应与跨进程缓存回归

JVM新37项、Android9/16各44项通过：合法RGBA/16位/Adam7、零长分块后有效数据、跨IDAT的zlib头、CRC/结构/截断/损坏压缩流/解压上限、HTML及超限响应回退、404与临时失败区分、读取返回时取消不发布/不负缓存、有效同名替换及坏更新保留旧图/无临时文件残留。HTTP为受控连接，不冒充真实镜像线路。seed/verify在不同进程；Android使用拥有的临时目录内平台SharedPreferencesImpl并等待QueuedWork落盘，新进程确认替换字节、真实解码颜色/Alpha及404标记。JVM偏好为代理夹具。首次平台prefs测试因后台线程存活而超时，未计通过；只修测试进程flush后退出，最终两设备完整通过，超时记录保留。队列161项和提取实际pause/resume/retry的14项共享回归通过。

正式包API36/host GPU中，分类页与全部图标网格各5轮外部设置暂停→BACK恢复，均同PID4483；实际日志确认旧ICON_LIBRARY会话取消及新会话打开，网格截图正常。取消记录pending/extra为0，表示未取得真实socket在途或未完成预览被暂停的样本；不能以此声称慢网在途UI取消也通过，该路径仅受控响应和既有队列测试覆盖。初次网格工具假定设置返回根页，实际正确恢复了库页，工具失败留档后按当前页面进入全部网格重测。未选择或应用任何新图标。

build.bat、v1/v2/v3签名、zipalign-P16、v1.5.8/33通过，正式SHA256 88bab291d7d58fcb5d7dbac81f9821438ae4d78688b11520259744b2b1fa81c8，模拟器保留数据安装拉回一致；对15923f86…仅classes2.dex变化，原53项暂存binary patch不变，无测试连接/探针进入主DEX，无本次Launcher crash/ANR。生产仅IconPreviewRepository.java；新增tools/tests/icon_preview/run_cache_tests.py是因为旧网络fixture替代fetch本体、不能验证真实字节/CRC/发布与跨进程存储；扩展既有tools/tests/icon_library/run_page_state_tests.py覆盖实际pause方法，未复制生产Owner。

同名更新验收仅限显式成功发布后的文件替换和新进程可见性；不新增远端自动刷新，发布同名资源仍遵守原缓存版本机制。本批不批量删除/重验历史缓存，不宣称完整PNG语义验证或全部线上坏包已关闭。原APK归档仍缺失，clean/raw/maintained无同名Java Owner，备用镜像行为按当前规则及PNG规范核对（https://www.w3.org/TR/png-3/）。真实镜像慢网/复杂坏包、旧缓存迁移、跨ROM、三星S25U Share现场及长稳仍未验收；冷启动整体未解决，清后台已恢复的返回现象不再复测。下一项转文件夹首开长帧：先确认实际可见卡顿与调用，不重复本轮缓存采样。 开发日志已更新，MEMORY.md未更新。

## 2026-10-17 A24 可见图标订阅与淘汰竞态回归

既有61项扩展到161项，桌面JVM及Android9真机/API36均通过；覆盖同/跨会话P1共享后可见订阅、取消单订阅后可淘汰、800个P0请求突发及8槽metadata、取消40/80会话后无旧回调/旧任务执行、32轮已完成待主线程投递时取消、会话与全局淘汰窗口中并发加入以及锁顺序终止。Android隔离使用提取的生产方法和真实ART执行器/MAIN Looper，主线程投递用栅栏控制，Bitmap/Drawable/cache/网络为夹具，不等于完整原生图片/GPU。测试门只注入提取副本，正式DEX无evictionGate。初次Android9隔离打印153通过但Killed退出，未算有效完成；只修测试进程退出方式后重新完成，失败日志留档。

最终build.bat、签名v1/v2/v3、zipalign-P16、v1.5.8/33和保留数据安装拉回哈希通过，SHA256 15923f869ab42ebd13b569426fc93cfdf9c99f0046884321848ae13655a77cf6；对b09ead0c…仅classes2.dex变化，53项暂存binary patch不变。API36/host GPU最终五轮Dock底部上滑搜索入口→桌面设置→应用图标页→三组快速上下滚动→HOME完成，每轮中途XML确认可见行变化，起止同PID5555，最终Launcher crash/ANR事件0条，截图/XML保留并人工复核。查询/结果启动未覆盖，不重复冷启动五样本冒充本次队列验收；真机仅读取SDK/锁屏与隔离shell进程，未安装最终主APK或操作UI、未改日志/工程配置。

本批证明并修复设置图标队列的受控可达丢回调路径，不能认定是三星S25U常用Share缺图的同一根因；三星现场、完整图片/全GPU压力、长期锁争用/峰值PSS、真实后台压力、全ROM、完整恢复及严格16KiB仍未验收。冷启动整体仍未解决；用户确认清理后台恢复的返回现象不再单列复测。下一项转图标库坏包隔离、暂停后取消、同名图片替换及跨进程缓存有效性；不重复本批已通过用例制造新进度。 开发日志已更新，MEMORY.md未更新。

## 2026-10-17 GPU后端对照与入口烟测

复用上批诊断APK，无源码插桩或重新构建；正式APK保持b09ead0c…，原53项暂存保持。每个后端随后保留数据恢复正式包，拉回哈希一致，各一次冷启PAGE_READY 1421/4305ms，仅恢复烟测。底部上滑搜索入口/桌面设置入口烟测通过。软件后端初次desktop.png中相机/文件/信息/通讯录等部分前景缺失，较晚desktop-late.png已恢复；没有定出首次完整可见时刻或直接根因，不能称首次视觉验收通过，前后截图保留。host两次查询脚本未通过：截图中settings停留IME候选区、编辑框仍为空；原日志、截图/XML留档，不认定查询结果/启动回归通过，不为本次GPU对照扩展搜索逻辑修复。未重复完整五轮功能，不称全功能验收。

既有preview队列61项通过，不等同实际GPU/主线程压力矩阵。真机未测；跨ROM、三星常用Share现场、完整恢复/长稳/严格16KiB仍未验收。用户已确认返回恢复，A22独立复测撤下。开发日志已更新，MEMORY.md未更新。

## 2026-10-17 首轮渲染采样与正式包恢复回归

正式包仍b09ead0c…/v1.5.8/33，临时P/sa/mymaterial.f计数源码及APK/idsig均恢复原字节，原53项暂存binary patch保持。诊断build.bat通过，恢复后签名v1/v2/v3、zipalign-P16及安装拉回哈希一致。API36/4KiB/SwiftShader、1080×2400/12宫格黑主题/默认圆框，同包五次PAGE_READY为6868/6066/5546/5789/5210ms，中位5789；绑定到PAGE_READY为2365/2137/2098/2022/1823ms。只为同包回归，非新优化前后比较，不等同物理首帧。

五轮Dock底部上滑300/500/800/650/900ms→搜索settings→结果启动设置→HOME→桌面设置→图标查询→HOME完成，逐轮起止同PID5600；最终Launcher am_crash/am_anr事件为空。有效两页截图与上批同哈希包在[0,110,1080,2300]对照：page0变化像素448；page1变化像素448。差异均仅在页码指示器[x517..562,y2006..2021]：当前隐藏、参考可见，原图及局部放大留档，不称整页零差异；独立图标宫格[0,115,1080,1970]两页均零差异。搜索、图标查询及桌面截图人工复核。

34个不同材质纹理未命中、4个不同Shader创建，五轮计数一致，未发现同名重复；没有正式功能修改。API36为SwiftShader模拟器，真机UI本批未测，三星现场/全ROM/长稳/完整恢复/严格16KiB未关闭。证据build/bind-render-profile-20261017。开发日志已更新、MEMORY.md未更新。

## 2026-10-17 补写链路定点核对（无正式代码修改）

临时计数构建后已逐字恢复源码与APK/idsig，正式仍b09ead0c…/v1.5.8/33；签名v1/v2/v3、zipalign-P16再检查通过，安装拉回哈希一致，53项暂存binary patch不变。API36同包恢复回归PAGE_READY为4912/5940/4913/4534/4610ms，中位4912，不具有优化前后比较含义。

五轮Dock底部上滑300/500/800/650/900ms→搜索settings→启动设置→HOME→桌面设置→图标查询→HOME均完成，逐轮同PID5867；搜索结果图标与末次HOME截图人工复核。两页formal-visual截图仍在加载阶段，作废，不宣称本批两页像素一致；模拟器退出后末次事件日志无法补取，不宣称最终crash/ANR日志验收完成。当前ADB仅余真机，未操作真机、未改日志或工程设置。证据build/source-persist-profile-20261017/verification.json及ui/summary.json。

五轮后台精确计数为21项原图校验、20次MD5命中、1次日历重建、24次PNG、1次写库接口返回true；保留动态/普通模式交接保护，没有成立的安全删除候选。冷启动整体、日历模式切换、真机UI/三星Share现场、全ROM/长稳/严格16KiB仍未验收。开发日志已更新，MEMORY.md未更新。

## 2026-10-17 无缓存首建/补写边界

最终b09ead0c…/v1.5.8/33；标准构建、v1/v2/v3及zipalign-P16通过，只有classes.dex/classes2.dex变化，原53项暂存不变。复用现有StaticSource和补写Owner，原有512上限/拒绝重试/旧准备与恢复路径保留；原合成体/分类/阴影/HOME未改。

修前288项对照；Android9/16最终各289项无缓存、246项有缓存入口检查，另原resolver481+生命周期289、补写队列及58+24阴影/图标合同通过。Android隔离合成为记录夹具，GPU边界由API36两页零像素差和五轮300/500/800/650/900ms Dock底部上滑→搜索结果启动→HOME→桌面设置→图标查询→HOME补验，逐轮同PID6637；无本次Launcher crash/ANR。立即搜索额外同PID，通过时仅入口发起处于补写期间，查询输入时已补完，不夸大覆盖范围。

同会话主五样本PAGE_READY中位4667→4436ms，未证整体稳定收益；前后各5次后台观察均21条任务完成，补写工作未移至UI/GL线程。完整数值和RSS/IO限制见性能报告。真机仅隔离，本批未安装到真机验UI；全ROM/原S25U现场/完整恢复/严格16KiB/长稳未关闭。证据build/uncached-source-compose-20261017。

## 2026-10-17 有效缓存静态来源同步复用

最终f2d0af9b…/v1.5.8/33，标准构建、v1/v2/v3及zipalign-P16通过。仅classes.dex/classes2.dex改变，原53项暂存未变。生产仅IconRasterDiagnostics.java和e/s.smali：原图已成功解码、高分辨率静态分支才尝试一次同步来源解析→准备→原分类→原合成；无/坏缓存与正式源缺失继续原补写/恢复，其他入口保留。

Android9/16各246项所有权/同身份换图/恢复/坏PNG隔离检查，原resolver481+生命周期289、键来源480组1093项、Android搜索11项、补写及阴影/图标合同通过。记录合成夹具不等同全GPU；API36两页桌面像素零差异、五轮300/500/800/650/900ms Dock底部上滑搜索→设置结果启动→HOME→桌面设置→图标查询→HOME均同PID5357，截图及XML留证，无本次Launcher crash/ANR。

前后各五次PAGE_READY中位4318→4252ms，范围重叠，不认定整体稳定提速。真机仅隔离用例，未安装本批新包做真机UI；S25U原Share现场、全ROM/长稳/完整恢复/严格16KiB与首次重建风险仍未验。证据build/local-source-compose-20261017，详细样本和失败工具记录见开发日志。

## 2026-10-17 准备/合成生命周期核对与装饰日志复用

最终0e4c466c…/v1.5.8/33，标准构建、v1/v2/v3签名和zipalign-P16通过。对0d9794b8…仅classes2.dex变化，Host/Smali未变，原53项暂存保持。生产仅四行：把合成器已有sourceType传给私有装饰日志，省去一次完整来源判断，不改徽标/像素/回收或跨阶段持有Bitmap。

Android9/16均原481项加新增289项通过：五类非圆框来源两阶段请求2次、独立准备副本/Alpha/Bounds、借用回退、同身份换像素、生产分类入口消费本次Bitmap；80组生产装饰方法对照类型查询1→0、输出像素/对象归属不变。分类器和徽标外围为夹具，非完整GPU及真实分身验证。阴影58/主题24、图标合同通过，原准备/合成请求未擅删。

API36/4KiB/SwiftShader、12宫格黑主题和默认圆框，正式基线/最终包拉回hash一致，各5次冷启动PAGE_READY中位4621→4295ms，范围重叠不认定整体稳定提速。两页桌面区域像素零差异。最终5轮底部上滑搜索settings、结果图标/启动系统设置、桌面设置和应用图标查询往返通过，均同PID5343。候选首次采集握手失败无有效样本，保留原输出；只改测试工具的限时连接就绪探针，重新五样本，不混入安装启动记录。

证据build/prepared-chain-audit-20261017；真机主APK/UI和全ROM/恢复/分身/压力/长稳仍未验，A22首次返回重建未关闭；只读AVD测试结束关闭、不保存快照。总体13局部完成/2部分/7开放/1撤回的登记口径见计划顶部，不等于全项目验收。DEVELOPMENT_LOG已更新，MEMORY.md未更新。

## 2026-10-17 单次键来源复用最终回归

最终0d9794b8…/v1.5.8/33，标准构建、v1/v2/v3签名、zipalign-P16通过；对e3d84deb…仅classes2.dex变化，无临时采样入口，原53项暂存不变。现有ManagedIconSource只供一次纹理键消费，不改变原阴影、几何或HOME生命周期。API28真机/36各480组/1093项提取生产方法的真实PNG隔离，完整键相同，CUSTOM解码/编码4→1、IMPROVED来源请求2→1；身份720组/3690项、来源481、搜索11、补写队列/阴影/合同回归通过。图标包回退时变可用、损坏/缺图、用户/组件及动态旁路均有用例。

按用户允许的Android16测试路径，API36/4KiB/SwiftShader、12宫格黑主题、默认圆框，保留数据安装前后hash拉回一致。最终基线/候选各5次进程冷启动PAGE_READY中位5495→4710ms；初始基线4390ms与9104ms长样本揭示波动，所有样本及非最终候选保留，不宣称整体稳定提速。两页[0,110,1080,2300]区域逐像素相同，未把程序标记等同物理首帧。

最终5轮Dock上滑300/500/800/650/900ms→搜索settings（图标可见）→实际启动系统设置→HOME→桌面设置→应用图标查询→HOME完成，逐轮起止均PID7279。搜索及末轮图标查询截图人工检查，设置/桌面兼容两项图标及勾选可见，未应用新选项。非最终脚本第二轮因保留查询被再次追加为settingssettings而失败，原截图/XML/输出在ui-pre-final；工具先清空已有输入后，最终包5轮重新通过。最终回归期间未见Launcher am_crash/am_anr；冷样本主动force-stop记录另存，不算崩溃。

证据build/source-key-reuse-20261017；真机仅做隔离PNG测试，最终包尚未做Android9 UI/五样本，不改变用户配置或日志开关。只读AVD退出不保存快照。A22、三星Share现场、全ROM/完整恢复/压力/长稳/严格16KiB仍开放，不能称全项目验收完成；DEVELOPMENT_LOG已更新，MEMORY.md未更新。

## 2026-10-16 修后剩余路径采样与来源类型复用

正式包e3d84deb8fc8157ce2cf5a93945bda5693dee084155e729a4accc512c6d57fe3，v1.5.8/33；build.bat、v1/v2/v3签名、zipalign-P16通过，两设备安装包拉回hash一致。相对本轮5e1b3d1b…基线，非签名成员仅classes2.dex变化；临时采样入口已移除，诊断源码逐字恢复，原53项暂存内容不变。

两次修前及两次修后采样确认identity中重复进入类型解析的路径已消除。720组/3690项生产方法对照、481项Android Bitmap、补写队列/拒绝重提、阴影58项/主题24项、搜索PNG/Looper11项及图标合同检查通过。纹理预载已有缓存门，颜色分类仍是原版嵌套调用，未取得重复工作的充分证据，本批不改。

vivo X21A/Android9紧邻基线与候选各5次进程冷启动，PAGE_READY中位3048→2827ms，约减少221ms/7.3%；首次GL回调388→387ms。两页桌面比较区域逐像素相同。正式功能首轮出现Launcher重新Create后自行SIG9、PID2957→3629；保留失败，未抓到直接调用栈，不等同于之前ABE强停。逐轮记录起止PID的补充5轮Dock上滑→搜索settings及图标→结果启动系统设置→HOME→桌面设置→应用图标查询→HOME均完成，始终PID3629。不能以补测覆盖首轮重建风险或宣称冷启动全部解决。

Android16/API36、4KiB、SwiftShader只读副本完成5次冷启动（PAGE_READY中位5099ms）、5次桌面设置图标启动系统设置后返回HOME（同PID4642），另完成底部上滑搜索、结果图标/启动系统设置及桌面设置往返，同PID4642。没有同会话修前对照，仅记兼容回归；首次logcat握手失败保留，不计样本。

测试结束已在手机系统UI停止日志，计时归零，persist.sys.log.ctrl=no；回到桌面，关闭本批创建的只读模拟器且不保存快照。未调整主题、导航、默认桌面、后台管理或清数据。证据build/startup-remaining-20261016；三星Share现场、全ROM、长稳及严格16KiB仍未验。下一项检查resolvedSourceHash、来源有效性与实际绘制是否重复读图，确认后再最小修复及五样本回归。MEMORY.md未更新。

## 2026-10-16 Android9外部返回阻塞复核

**最新用户反馈：** 清理手机后台后外部返回恢复正常；未由Agent追加5轮测试，不覆盖下方历史失败样本。随后只读快照MemAvailable约3.40GiB、Launcher PSS约204.7MiB/Graphics约111.4MiB。支持优先检查内存压力/后台负载参与条件，但缺触发前同条件采样，未证明泄漏、LMK或ABE具体阈值。设备配置未变，生产源码未改，MEMORY.md未更新。

追加授权自启动开启5轮、恢复关闭5轮，均真实桌面点击系统设置→HOME、全部换PID；开关已在系统UI恢复关闭，日志保持关闭。按用户要求换用10/11交接实验前50a8befb…APK，再5轮全部换PID；反编译确认该包没有后续HOME生命周期/截图交接实验，J.onPause/onResume及Eb.onResume与现行方法去行号后相同。已恢复最新5e1b3d1b…安装，自启动开关和交接动画实验均未获得因果证据，不修改生产动画。相应样本和方法比较在build/android9-home-regression-20261016，外部热恢复继续FAIL；MEMORY.md未更新。

已从v1.5.8标签（5d138863）提取APK，确认与上述50a8befb…归档SHA256相同，旧包5轮确为仓库标签包对照；未校验远程Release资产或其他同号包。最新5e1b3d1b…恢复后拉回hash一致，final-restored-routes再5轮仍换PID。额外final-ui脚本完成Dock上滑、输入settings和结果图标截图后，点击结果等待系统设置焦点失败、回到桌面，未完成后续设置/图标查询步骤，不记整轮PASS；截图与失败保留，生产源码未修改。

当前外部应用→HOME不能记为功能回归通过。vivo桌面真实点击系统设置→HOME，最新5e1b3d1b…与优化前旧4944e939…各5次均换PID；恢复最新包，用户授权临时打开系统日志后追加5次，am_kill均为stop by com.vivo.abe。退出发生在离开桌面后，包stopped由false变true，返回实际重新启动，不能仅改动画处理。原有图标/搜索/设置局部验证不撤销，但不代表正常外部热恢复已验收。当前尚未修复；暂停后续性能修改，先做授权范围内后台控制单变量对照并恢复测试状态。证据build/android9-home-regression-20261016，MEMORY.md未更新。

## 2026-10-16 真机PNG补写关键路径修复

最终5e1b3d1b…/v1.5.8/33，正常保留数据安装且拉回APK hash与文件一致；build.bat、v1/v2/v3签名、zipalign-P16通过。临时自采样构建仅用于定位，未修改debuggable/系统策略，生产LauncherStartupDiagnostics恢复原字节，正式DEX无TEMPORARY_PROFILE标记。原SMEngine创建/完成链路不改。

生产prepareUncachedStaticSource提取方法的新夹具在修前IMPROVED缺旧缓存时失败，修后覆盖五类来源、已有字节、来源缺失、非静态/设置、512限额；原有界批次/暂停P2/拒绝重提/替换身份检查继续通过。Android真实Bitmap resolver481项、搜索PNG/Looper11项、图标合同静态、阴影58项/Smali主题24项和图标库恢复重试6项通过。首次搜索隔离探针因刚安装后Launcher尚未运行、pidof为空而未执行；启动后重跑通过，保留失败输出，不记生产崩溃。

vivo同机基线/修后各5次完整进程冷启动：PAGE_READY中位6315→4553ms，scene task到bind5377→3646ms；回调/缓存和顺序限制见性能报告。前两页截图最大通道差2/255，未见视觉/几何变化；第五次29项兼容补写全部DONE，0失败/缺失。另一次在PAGE_READY观测时尚无补写DONE便从Dock上滑，搜索settings及结果图标可见、PID保持，未用固定延时等待补写。

最终包五轮Dock 300/500/800/650/900ms→搜索settings→结果启动系统设置→HOME→桌面设置→应用图标查询com.android.settings→HOME完成，图标/名称/选中状态与此前模板核对，末轮截图和即时搜索截图人工查看。外部往返仍有com.vivo.abe杀进程，未记热恢复PASS；没有调整Usage Access、常用应用、布局、主题、图标选源或导航。

API36/4KiB同包5次启动PAGE_READY中位5028ms（4885–5272），正式采集前的SystemUI无响应通过“等待”恢复，XML/events另存，不算Launcher故障。底部上滑搜索settings图标、结果启动系统设置及桌面设置往返完成。这里未重做API36同会话A/B，不报模拟器优化收益。

证据build/startup-gpu-vivo-20261016；完整ROM/图标包/分身/SAF恢复、首交互帧/帧率及长稳仍未验。下一项为修后MainView.oh纹理预载/解码及颜色分类的重新采样，证据确认后最小修复并回归。MEMORY.md未更新。

## 2026-10-16 A19 圆框来源复用与完整专项回归

交付APK4979fc9b…/v1.5.8/33。标准build.bat、v1/v2/v3验签、zipalign -P16、aapt2版本确认通过；两设备保留数据安装，vivo拉回APK hash一致。新增resolver真实Android Bitmap隔离481项通过；原图标合同静态审计、阴影58项和主题Smali24项、补写并发/拒绝重提、搜索真实PNG/Looper11项、图标库恢复/重试6项通过。此次未重复无关模块的全部29组测试，不把局部结果扩为全项目PASS。

同一API36临时副本和vivo分别完成带相同诊断的基线/修后5次进程冷启动；全部有效冷样本保留，首开负载组另存。API36每轮21图标来源加载42→21，桌面区域像素完全一致；其整体PAGE_READY仍波动，中位基线续组5378/候选5881ms，不记整体启动性能PASS。vivo未命中DEFAULT圆框分支、来源加载48不变，同诊断基线6392/最终候选6283ms不作收益声明。阴影与绑定后render驻留详见性能报告。

API36实际从底部上滑进入搜索、settings结果图标及启动系统设置、回桌面、桌面设置和应用图标查询可见；查询包名时输入法把点替成中文标点/空格产生无结果，留原截图，清空改用settings后设置/桌面兼容两项图标可见，未为测试改输入法或导航。一次过早点击仍在系统设置时进入导航模式页面，未点选任何导航模式；确认HOME窗口后再点击桌面设置，未算作桌面设置入口失败。

vivo最终包5轮Dock上滑300/500/800/650/900ms→搜索settings→点结果启动系统设置→HOME→桌面设置→应用图标查询com.android.settings→HOME完成。每轮结果/原图与已选改进版图标截图保留并与此前模板核对；末轮人工查看名称、选择状态、图标可见。外部设置返回每轮PID变化，events均有stop by com.vivo.abe，不记同进程热恢复PASS；未见对应Launcher am_crash/am_anr。原临时Usage Access仍default，常用应用开关未重新开启；不改主题/布局/导航/圆框配置。

证据build/startup-owner-20261016（包括第一次安装-200与提前采样被判无效的记录）。三星Share原现场、手持光影、严格16KiB与整库恢复仍未验。下一项：真实GPU纹理/Shader首次创建及重复工作定位，取得具体调用证据后最小修复，再同条件五样本及来源/像素/搜索/设置回归。MEMORY.md未更新。

## 2026-10-16 Android 16 启动补测

Pixel_6_Pro只读临时副本实测Android16/API36、4KiB、SwiftShader、12宫格黑主题，保留数据安装同一2b8d3fad…包并拉回hash一致。5次进程冷启动PAGE_READY为5221/5433/5037/5222/5033ms；系统设置→HOME 5/5同PID5269，最终截图完整桌面可见，正式捕获流无FATAL EXCEPTION。前置SystemUI无响应弹窗和脚本窗口标题识别失败均保留日志，未混入正式组。详见性能报告和build/startup-api36-20261016。没有生产改动，因此未重复构建；本次为启动/返回专项，并非全功能矩阵或16KiB验收。下一项A19细分来源/阴影及绑定后完成区段，完成后同条件五样本和图标/搜索/设置回归。MEMORY.md未更新。

## 2026-10-16 真机启动及恢复分层续测

同一vivo X21A和2b8d3fad…包，持续捕获已有诊断日志的5次进程冷启动完成，页面就绪标记5414/5433/5509/5781/5655ms；首GL回调标记不作为完整桌面首帧。另5次桌面实际点击系统设置→HOME均被com.vivo.abe后台结束进程，必须记录为外部热恢复不成立；内部桌面设置→HOME 5/5同PID20828。没有把系统杀后台记成Launcher主动重载/崩溃，也没有为通过而调整电池/后台设置。原截图和数据位于build/startup-vivo-20261016，详细性能分段与限制见PERFORMANCE_BASELINE_AND_OPTIMIZATION。生产代码/APK未变，本批无需重复构建；下一项明确为来源解析/阴影子调用定位，之后再进入文件夹首开。MEMORY.md未更新。

## 2026-10-16 元数据优化及真机连续回归

最新正式包v1.5.8/33，SHA256 `2b8d3fad0f0cf36a1a45ed2b77c1c0ccdeba67d812e0e5a8cdd4aa354b042b99`，vivo X21A保留数据安装成功并拉取APK校验一致。相对ca263178…仅classes2.dex变化。四个纯元数据读取改用已有接口，42项真实Android隔离与29组主机回归、图标合同静态审计、标准构建、签名/zipalign通过；局部5轮耗时证据详见性能报告，不声称整机性能已验收。

真机正式包5轮Dock 300/500/800/650/900ms→搜索settings→点击设置启动com.android.settings→HOME→桌面设置→应用图标→包名com.android.settings查询→HOME全部完成，PID12016保持。每轮搜索结果、应用图标查询及返回截图保留于build/icon-metadata-20261016/phone-ui；名称“设置”和原图/改进版图标可见。此前同包已验证图标库weixin八项及返回。未应用新图标，未切真机宫格/主题/壁纸/导航，Usage Access保持default。

首轮自动化因uiautomator导出失败后读取旧XML而中止，之后用唯一文件和成功标识排除旧树；该ROM随后仍无法稳定导出设置页控件树，最终采用真实窗口焦点、截图核对和结果目标Activity确认。失败未计入5轮PASS，未为自动化放松生产手势/布局规则。临时API37只读副本另补充PAGE_SIZE16384下启动与12→20重载可见，但未禁用系统兼容模式；按用户要求停止模拟器后继续真机测试，不能据此关闭A04或替代实体机验收。三星、真实恢复/分身、全主题、物理光影与长稳仍按原边界保留。

## 2026-10-16 图标库页面续测

本批APK v1.5.8/33，SHA256 `ca2631786eacbb18cdd97d86f1cd686de25ff0cd77be57faa4e50852962c81b6`，相对下方f9e…仅`classes2.dex`变化。页面恢复和目录失败处理的修前负例失败、修后6项通过；图标源目录10项、预览队列61项、完整构建、签名及图标资源审计通过。vivo X21A/Android9保留数据覆盖安装，虽然ROM安装器使ADB返回`-200`，最终从设备拉回的APK与本地SHA一致。真机进入图标库，`weixin`查询返回8项并可见图标，未改变用户选中的图标。真实待查询时的pause/resume及目录损坏重试未用用户数据做故障注入，状态仍为`CONTROLLED_REGRESSION_PASS / DEVICE_PATH_PARTIAL`。三星S25 Ultra原现场与旧完整矩阵边界不变；证据见`build/icon-library-resume-20261016`与DEVELOPMENT_LOG本日新节。

## 2026-10-16 后续修复与真机回归

最终v1.5.8/33，SHA256 `f9e30adc3a79100560ffa9e2dc295749f5fa956e653ccec92e212c429d57b88a`，vivo X21A / Android9 / 1080×2280 / density480。build.bat、签名、zipalign和保留数据安装通过，设备拉取APK hash一致；相对10月15日669d…载荷仅classes2.dex变化。下方10月15日结论保留为历史，不代替本日验收。

证据目录：build/search-icon-fix-20261016。28组主机回归通过；Dock修正后搜索图标、补写队列及手势81项再次通过（post-dock-tests.json）。新增实际Android图标11项，加上journal平台/worker/重进/撕裂写、启动清理112、SQLite身份83、安装worker39、QD99、向量23011、壁纸归档56，共8组隔离检查通过。各夹具的模型/包/偏好/合成或场景边界见对应summary，不能把隔离通过写成用户整库恢复或所有ROM通过。

| 功能/现场 | 本日结果 | 证据与限制 |
|---|---|---|
| 搜索图标缓存压力 | HOST + ANDROID ISOLATED PASS | 48张真实262948字节PNG超过encoded上限；Top5和可见cache miss可补载，逐行不重扫模型；缺少旧PNG调用最终合成边界。模型/合成器受控，图像解码/Looper真实。 |
| 暂存启动补写任务 | HOST PASS | 原方法暂停P2后pending滞留负例已复现；修后单槽批次、重复pageReady、满队列拒绝后真实事件重提、替换身份均通过。未删除用户缓存做冷缺失实验；队列满时等待后续真实page/source事件。 |
| Dock上滑搜索/常用图标 | DEVICE PASS 所测 | ui-repeat.json及topapps-repeat-1..5.png；300/500/800/500/650ms五轮全部打开，每轮五个图标均有可见像素，PID6653稳定。旧起点排除底部96dp，诊断包确认2201高/3密度/2100起点有效；正式包无诊断输出。 |
| 查询/结果/历史 | DEVICE PASS 所测 | settings、743944都匹配设置且图标显示；无匹配不残留旧行；点击结果启动系统设置，历史显示设置图标；search-settings-result/search-t9-result/search-no-match及topapps-settled.png。测试产生正常“设置”历史记录，没有清理用户历史。 |
| Back/关闭/HOME/设置/分页 | DEVICE PASS 所测 | T9 Back先收键盘、再次Back回桌面；关闭搜索后恢复桌面，系统设置/指南针HOME返回；三页横向翻页和第三页Dock入口已测。一个过早焦点采样仍显示转场中搜索窗口，不当作关闭失败；后续点击落在已恢复的指南针上，随后HOME返回，没有修改应用数据。 |
| 1000ms完成窗 | DEVICE PASS 所测 | 固定downTime输入1100ms未打开；后续500ms可打开。Android9原input swipe会重置每次事件downTime，最终工具以同一downTime按目标时刻注入；不放松生产单手势身份门。 |
| 临时授权恢复 | RESTORED | 明确授权后临时开启Usage Access及常用应用；结束GET_USAGE_STATS精确恢复default，config-restored.png确认常用应用关闭。T9/联系人/快捷桌面/动态项保持原设置；主题/壁纸/默认HOME/系统导航未改。 |
| 启动/主界面图标/日志 | DEVICE SMOKE PASS | 原数据安装、桌面主体/静态图标及设置入口可见；首装后的两张默认源图标外形与10月11日手机旧包有差异，属原有暂存来源/圆框修正，不宣称全屏像素一致。最终目标进程未见FATAL/ANR/图标加载失败；LauncherEvent null、memtrack噪声仍有，未认定根因。未量化启动/帧率提升。 |
| 三星S25 Ultra / Share | NOT TESTED | 未连接对应设备，不能证明其具体包/源图/缓存状态；已修可复现的通用丢载链路，不写三星现场已彻底验收。 |
| 全主题/12↔20/Folder/分身/整库SAF/锁屏/长稳 | NOT COMPLETELY TESTED | 保留原主题/布局，不建立或重排文件夹、不切系统导航、不操作真实恢复或用户分身；当前三页无现成Folder。原生HOME壁纸空档、16KiB native、手持Sensor及其他ROM仍按旧清单保留。 |

结论：本批最小修复及上述可行真机路径通过；没有把用户要求的完整功能矩阵或先前性能方案标为全部完成。具体问题A12/A13/A14及文件见稳定性清单和DEVELOPMENT_LOG；MEMORY.md未更新。

## 2026-10-15 历史验收

日期：2026-10-15。状态：**本轮修复的可行验证完成；全功能、全ROM、长稳验收未完成**。最终v1.5.8/33，min23/target28/compile36，SHA256 `669d1cc29f1458c44db47809ddab60da9f82548212b67f13070c9984e46bc48c`。未提交/推送，未清数据。

## 分批证据

| 批次 | 改动 | 结果 | 限制 |
|---|---|---|---|
| 1 / A03 | journal夹具新壁纸/归档签名；Model补SQLiteTransactionListener夹具 | journal144、restore worker122、Model188通过 | 不把测试javac失败说成生产崩溃 |
| 2 / A01 | 三个备份Owner先读边界、验证采样、finally释放 | 旧分配负例失败，新184项通过；API36真实PNG/ZIP/SHA/旧档56项；标准构建/签名/zipalign/保留数据安装 | 受控偏好/布局，不是整库SAF恢复 |
| 撤回 / A02 | 搜索索引延迟全量候选 | API负例复现，生产可达性未证，改动完整撤回；普通路径6项通过 | --probe-deferred-api预期失败，不纳入已修BUG或通过项 |
| 3 / A10 | FlingUp 500→1000ms；镜像终点谓词 | 76项边界/接线；真实300ms中段、250ms高位、650/900ms进入，1100ms拒绝；Chrome提交结果正确 | 反转方向仅离线边界，实体/所有输入法未验 |
| 4 / A09 | 当前版本文档对齐v1.5.8/33 | badging/XML复核和diff检查 | 没改APK版本和历史示例 |

## 自动化

accepted-host-tests.json：最终源码 **27/27组通过**。涵盖删除门/用户身份/卸载桥、下载异常、设置读取/恢复监听、journal/worker、偏好、壁纸顺序与失败去重、Insets902、预览取消/队列、设置会话/底部手势、解锁时间、搜索图标、候选、Sensor注册111、几何/主题/透明布局、目录、图片184、索引正常状态6和搜索手势76。组数不是独立端到端功能数，公式/桩测试不是视觉验收。

final-device-tests.json：journal平台57/线程7/清理13、重进6/6、撕裂写4；真实SQLite pending身份17/重进3；QD捕获99/代际9；Sensor向量23011。隔离批次前后Launcher PID7972保持；夹具使用独立/data/local/tmp，不修改Launcher数据库。Android壁纸/源归档56项前后PID1942保持。它们的UI/偏好/部分包状态是受控边界，不能称完整真实恢复。

图标合同审计通过；图源5199、应用4720、包4625，errors=0、1个LEGACY_IDS告警。没有删除/重命名长期资源。

## 真实模拟器功能矩阵

| 功能 | 结果 | 证据/尚缺 |
|---|---|---|
| 12宫格进程冷启动/保留数据安装 | PASS 所测功能 / 性能未关闭 | delivered及补充ab-final各五个新PID有PAGE_READY，桌面可见；A/B尾部波动，耗时不等于呈现时间 |
| Android设置→Back / HOME键 / 原生上滑 | PASS 最终状态 | 每路3次，共9次，焦点smt_launcher且PID不变；accepted-ui-regression.json；不说明中间无闪壁纸 |
| 桌面设置打开/返回 | PASS 所测 | settings-retry.png实际设置页；初次截图在转场中，未误判通过 |
| 搜索入口、Chrome查询 | PASS 所测 | search-gesture-runtime.json、search-result-committed.png/XML；input text的IME组合态不计查询完成，Enter提交后确认结果 |
| 静态图标像素 | PASS 三处ROI | camera/settings/maps三个210×210区域与任务前RGB零差异；等待转场稳定后比较 |
| 备份原图/壁纸/失败恢复 | ISOLATED PASS | 旧档、PNG/ZIP/SHA/journal；没有对用户整库恢复或模拟生产断电 |
| QD/Magic Flow | ISOLATED PASS | 门控/代际；用户关闭项未开启，真实音乐授权与首次揭露未全面验收 |
| Folder/拖动/20宫格/50或150% | NOT TESTED 完整UI | 不创建/重排用户布局；几何检查不替代交互 |
| 白/透明/毛玻璃/四指/自选壁纸 | STATIC/ISOLATED ONLY | 不改变用户主题/壁纸以跑矩阵 |
| 天气/日历/手持光影/锁屏解锁 | STATIC/ISOLATED ONLY | 当前动态图标关闭，不改开关；真实lux/姿态/天气/解锁录像仍缺 |
| 应用安装/更新/卸载/分身 | ISOLATED ONLY | 未安装第三方夹具或切用户，Model/SQLite不代替ROM事件 |
| 网络异常/坏文件 | ISOLATED PASS | 下载/PNG/ZIP/checksum负例，未覆盖全部真实提供器 |
| 长稳/低内存/配置重建/HOME切换 | NOT TESTED 完整矩阵 | 不清数据/切HOME/导航/分辨率，未伪造LMK或长期泄漏结论 |

## Android/ROM/显示矩阵

| 环境 | 本轮状态 |
|---|---|
| Android16 API36 AOSP x86_64，1080×2400/density480/4KiB | 上述输入/安装/隔离覆盖 |
| Android8–15其他版本 | 本轮设备NOT TESTED；保留既有兼容门与历史记录 |
| Android17 API37 | 本轮NOT TESTED；旧记录不能冒充当前结果 |
| vivo/OPPO/HyperOS/OneUI/原锤子 | 本轮没有实体机；OPPO合成和vivo手持光影均未关闭 |
| 720p/1080×1920/1440×3200、90/120/144Hz | 未切换/穷举组合 |
| 16KiB页面 | NOT TESTED；x86_64 ELF仍4KiB，ZIP检查不能关闭风险 |

## 构建、安全与审查

各生产批次标准build.bat通过，最终v1/v2/v3签名和16KiB ZIP检查通过；二进制Manifest/badging已导出。检查了Provider签名权限、非导出reload、PinItemRequest有效性/用户确认、ZIP canonical path/条目/总量/SHA保护；这不是全部导出组件的渗透测试。

最终非签名载荷相对任务前改变classes.dex（两处手势指令）和classes2.dex（验证/终点谓词），Manifest、resources.arsc、PNG/assets/native库保持。53项原有暂存blob保留，本轮差异未暂存。

采集窗口无新增AndroidRuntime FATAL；没有完整自然ANR/native tombstone/长期LMK采样，不因此宣布零崩溃。未获物理呈现Trace、长稳功耗和跨ROM矩阵，不能标记全项目FINAL/PASS。
