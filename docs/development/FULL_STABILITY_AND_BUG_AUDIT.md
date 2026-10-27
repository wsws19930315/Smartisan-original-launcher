# 全项目稳定性与问题清单（2026-10-15）

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

问题状态：已确认的重复解析局部修复关闭；没有新缓存、数据协议、线程或权限，空几何/无图回退和所有权检查通过。整体冷启动与既有跨设备缺口不关闭。所有无有效应用标记的早期采样留档不计五样本；没有改debuggable/日志属性，诊断输出最终清零且正式包移除。


## 2026-10-23 第十六批：定位静态节点构建耗时，排除把整段归因GL上传

**10/23第十六批当前：耗时定位完成，生产逻辑净改动为零，冷启动未解决。** 当前无真机连接；复用第十五批真机五份trace，解码区间去重中位169.250ms/运行164.903ms，不能解释1065.776ms整帧。另在已有API36只读模拟器/host RTX3060做5次分段诊断，PAGE_READY3479/2468/2185/2496/2392ms，中位2468；静态节点构建中位1153.187ms，而GL位图上传23.637ms、文字23.358ms。单次细分确认静态合成507.151ms、来源307.359ms、准备143.175ms、键135.944ms；圆框127.220ms含在准备阶段，Alpha扫描62.282ms含在合成阶段，均不可重复累加。该单次不是五样本性能收益，更不能与真机1286ms混比。没有证据支持删除原版绘制/上传，本轮不交付臆测修复。9份临时源码逐字节恢复，重建包全部非META-INF成员与本轮原包相同；正式SHA256=4806115c3ea2b32336497c1b3b5857fcd79ed8089a159c7e2abc6d9ad85ca18f，签名/P16/覆盖安装拉回哈希、13静态区域及5轮搜索/设置/返回通过。第5轮ADB中断后同PID重跑，前4轮与中断证据保留。134项原暂存patch保持，MEMORY.md未改。下一项只核对composeTexture中NormalIconRasterSpec和IconVisualMetrics的同次重复几何解析，量化后考虑复用同一快照；不重开来源三查/旧阴影提取/最终磁盘缓存/无条件页延后实验。证据build/startup-cell-content-20261023。

问题状态：冷启动性能仍开放；本轮排除模拟器该路径中GL上传/文字节点作为主因，并未修复新BUG。没有确认可删除的重复绘制，不删除兼容分支或改变圆框/阴影算法。ADB中断为本次测试中断记录，不能冒称应用崩溃；既有Android9/三星Share/首装/长稳/真实16KiB等问题保持原验收状态。


**10/22第十五批当前：静态合成的来源/类型/身份改为复用同次快照。** 生产仅IconRasterDiagnostics.java与MaintainedLauncherSettingsHost.java，复用已有ManagedIconSource和来源解析Owner；未引入跨调用缓存、Bitmap持有、线程或数据协议，纹理键与合成仍各解析一次。实际方法+Android原生Bitmap的480键场景/480合成场景共2631检查通过；自定义图完整key+compose链的文件解码/重编码5→2（不代表全部内存PNG解码），改进图来源请求3→2，缺失图仍保留晚到复查；旧源码负控准确失败。Android16真机V2458A同条件各5启动PAGE_READY中位1321→1286ms，GL构建帧wall1093.780→1065.776ms/运行CPU1002.108→976.637ms；未隔离缓存/顺序/调度，不能将35ms全归因或宣称冷启动解决。首屏13静态区域像素一致，首次8页往返无>50ms GL帧；正式包五轮图标/底部上滑搜索/准确settings查询/设置与返回及文件夹开关通过。最终SHA256=c4b70eb3d537921cabb4982559c82f3931e4f9ebc3217fd0061e8f17b10cd9c0，签名/P16/安装拉回哈希通过，仅classes2.dex变化，临时Trace逐字节恢复，129项暂存patch保持，MEMORY.md未更新。下一项定位首屏GL剩余约1秒中CELL_CONTENT_CREATE的资源解码/纹理创建实际调用，先细分归因，不再重复本批来源快照、磁盘缓存或无条件延后页实验。Folder性能仍暂停；Android9/三星Share/全ROM/首装/长稳/真实16KiB缺口保留。证据build/startup-compose-source-20261022。


**10/22第十四批当前：最终纹理磁盘候选已否决，过期纹理键门禁已最小修复。** 在Android16真机V2458A完成原/候选/空缓存/反向原/门禁修复各5样本。磁盘候选稳定命中67张时PAGE_READY中位1183ms，但受控空缓存1423ms，初始原1339ms、反向原1351ms；首次无缓存更慢，因此撤回全部缓存生产改动并清理测试文件，不再将这条路线作为当前首启优化推进。另确认e.s入口仍硬编码v18，当前Java已v30，导致完整纹理键被重复生成；改为调用Java唯一版本判断，普通/过期键仍构建，保留调用方已解析的当前键。实际入口Smali前缀18检查与旧分支负控通过，有完整日志样本键生成138→70；修后5启动1341/1288/1308/1265/1313ms，中位1308，较相邻修前1351约少3%，不能将整个差值视为已完全隔离的代码收益。最终正式包五轮图标/底部上滑搜索/准确settings查询/设置/返回及文件夹开关通过，首次8页往返无>50ms GL帧；修前反向原/修后13个静态区域像素一致。最终SHA256=59031d278cf0c08f345731399d84376bfd362f7862df5766a14e41c4df1393d4，签名/P16/安装拉回哈希通过；永久生产仅e/s.smali与IconRasterDiagnostics.java，本批无新缓存/线程池/数据协议，临时诊断与持久化Owner逐字节恢复，129项暂存patch保持，MEMORY.md未更新。整体冷启动仍开放；下一项核对跨纹理键生成与正式合成的重复来源解析，区别于本批入口门禁、先计数再最小修复，不重复磁盘缓存实验。Folder性能仍暂停；Android9/三星Share/全ROM/首装/长稳/真实16KiB未验。证据build/startup-final-cache-20261022。

**10/22第十三批当前：缓存持久化准入核对完成，未上线缓存改动。** 提取现有来源解析/纹理键方法，在API36只读模拟器两个独立ART进程各跑480组/1684检查，圆框、透明主题、逻辑/物理尺寸、surface、geometryRevision、宫格、分类、阴影、光影、用户及既有来源替换规则通过；相同安装元数据跨进程键一致。删除圆框区分的负控按预期失败。实际Android Bitmap构造出不同像素但相同32位摘要的反例，非Bitmap颜色改变也未进入类名/尺寸/身份摘要，故禁止直接将当前进程纹理键当作持久化完整性协议。旧三列为带阴影成品，data1～3还参与快捷方式备份/恢复，不因当前为空就占用。未改生产源码/APK/DB协议，没有新五启动或安装/功能回归，也不声称提速；冷启动仍未解决。下一项只做既有Owner内版本化最终PNG磁盘候选：先证明来源强身份、表示/版本、负载SHA256、原子发布、容量与恢复失效，再决定接入；不得先把旧PNG当RAW。证据build/startup-cache-validity-20261022，正式APK仍aa336816…，129项暂存patch未变，MEMORY.md未更新。真机/Share/全ROM/长稳/16KiB缺口保留。

**10/22第十二批当前：** 已修图标数据库保存结果误报：data/a/e只在SQLite更新命中/插入非-1时成功，e.s.a失败告警但保留内存字节，异步日志改CACHE_READY避免冒称落盘；没有新缓存/表结构/重试或页面时序改变。实际e/V/U与完整caller方法+Android SQLite的16检查、第二进程3读回、旧writer/旧caller两个负例及补写队列通过；修正了第十批接口变化后过期的队列夹具，PM/源生成/入口仍为夹具，不是完整存储故障UI。实际应用22条缓存跨原/最终各5启动内容哈希一致，旧三列成品与private iconData有读取链，尚无带版本/来源/尺寸身份的RAW跨进程恢复协议，不是已确认写库丢失。最终API36只读模拟器5启动中位2259ms、正式包五轮图标/底部上滑搜索/设置回归通过，未称提速；拼音恢复。当前SHA256=aa336816dd9bb78b0af196bb13a20cc46fd83fad4bccaa5f06340453c4a1ec72，构建签名P16及安装哈希通过，129项暂存保持，MEMORY.md未更改。冷启动仍开放；下一项为现有Owner下版本化RAW/纹理持久化协议及失效/容量/恢复证明，不能直接塞旧成品或重复延后翻页。真机/Top5/Share/全ROM/长稳/16KiB未验；详见开发日志第十二批、build/startup-source-roundtrip-20261022。

**10/22第十一批当前：后续页延后候选已否决并完整撤回。** 纠正“只有前两普通页图标初始化”的旧归因：旧统计只覆盖两页，真机实际9个普通页构造时均提前g.create；约640ms主要在余下工厂循环，阴影预载<1ms，Dock约33ms。原/候选/反向原同诊断各5启动中位1325/847/1335ms，但候选首次向前8次翻页出现7个50～173ms长帧，原/反向原同一路径约11～13ms且无>50ms帧，故未交付。候选仅复用ka既有Hn/oo初始化，没有新增缓存，但确实把工作移到首滑；所有实验/临时诊断源码均逐字节恢复。恢复build.bat/签名/P16/安装拉回哈希及正式包五轮图标/常用应用/底部上滑搜索/设置回归通过；恢复APK与原3b827…非签名ZIP全相同，重建容器SHA256=23a889a4cf370d57ef8f2dbf99edb99c3bc1591002eb737f68ed1fe4856ddb20。129项暂存patch保持，MEMORY.md未更新，系统日志保持开启。冷启动仍开放；下一项核实既有异步源补写是否实际持久化并在下次加载恢复iconRawData，先跨两进程读写对照，不重复无条件延后/旧成品直接套用。完整15样本、9页往返、日志漏采与诊断边界见开发日志第十一批、build/startup-bind-tail-20261022。其他ROM/三星Share/首装/长稳/16KiB等缺口保持，Folder暂停。

**10/22第十批当前：** 已否决将旧 dark/light DB 字节直接复用为当前最终纹理（含旧阴影/几何且缺少现有失效身份）；在既有静态合成调用内借用合格 ARGB_8888 BitmapDrawable，保持 DEFAULT 圆框和所有权边界，无新缓存。cached274/uncached311原生检查、两负例、13静态区域像素一致、构建签名安装哈希及真机五轮图标/常用应用/底部上滑搜索/设置回归通过。Android16 V2458A原/最终五次PAGE_READY中位1351/1361ms，GL wall1139.359/1134.758ms、CPU1038.927/1038.559ms；SOURCE_RASTER计数17→1，但未证明整体提速，冷启动仍开放。无日志与cached-only原型保留，不混入有效组；系统日志按用户授权保持开启，5个诊断标签I，其他设置保持。当前APK=3b8276618a2f220b0fb35f91cc4f855aef2d8563c54518cb913a988ed8b2b9be，129项暂存patch保持，MEMORY.md未更改。下一项 Eb.Vh 内两页初始化后至绑定结束约640ms的真实调用；Folder暂停，其他ROM/三星Share/首装/长稳/16KiB仍待验。完整细节和失败边界见开发日志第十批及build/startup-persisted-icon-audit-20261021。

**2026-10-21第九批当前：** 首两页软件准备前移已完成候选验证，81原生所有权/坏键负控/167既有检查、11静态区域像素一致；有效五样本GL缩短但总启动中位2206ms，比原/反向原1751/1800ms慢，故已撤回，不保留新线程/缓存/约4.85MiB暂存。正式源码与0afe93ba…APK恢复；生产净改动零。下一项是现有图标数据库成品的来源/表示/尺寸有效性，禁止重复“每次重算前移+join”当新优化。冷启动仍未解决、Folder暂停、真机/首装/长稳/严格16KiB等缺口保留；暂存129项实验前后保持，详见开发日志第九批与build/startup-raster-handoff-20261021。

**2026-10-21第七批当前：** 构建后旧目录/ready回调、在线与包查询、MAIN分页、保存/恢复及索引ready身份缺口已集中修复。原页面10组负例及旧Manager负控失败，修后15组25检查、ART目录164/构建31/页面16/预览167与构建安装/五轮基础功能通过；真实目录48结果浏览/系统设置BACK保留状态。未做真实UI安装更新时序注入或跨60项边界；真机/Share/Top5/全ROM/长稳缺口仍开放。冷启动五样本中位2185ms，未宣称解决或提速；下一优先项现有trace中的首屏GL剩余CPU热点，不重复目录微任务。SHA256=0afe93ba559f3b5b4b16a2610071d65e5338acbd5d4ae9158b86bd2de64a51d4，Folder暂停；详见开发日志第七批。

**2026-10-21第六批当前：** 目录构建中失效被旧构建覆盖已局部修复；短发布锁+代数校验，过期明确取消，MAIN不等待目录IO。旧源码负例及ART31/目录159/页面14/主机队列167、构建安装哈希/五轮基础功能通过。正式首启动发生取消，其余4轮正常ready，保留所有样本；冷启动仍未解决。下一项检查发布后排队页面回调/搜索快照失效，不将所有旧引用失效链宣称已闭环。SHA256=09f59081322a9bc68105c56ffd4fd49dd90bb968a023bb6b7cbfec92d3a00155；真机/Share/长稳等总缺口及Folder暂停不变，详情同日开发日志第六批。

**2026-10-21第五批当前：** A11/A18目录预热占用解码worker已局部修复，使用既有indexPool并保持低内存开始前暂停。主机/ART各167项与两负例、实际线程归属及构建安装/五轮基础回归通过。未发现Catalog重复图片解码，未删预热/新增缓存。整体冷启动、目录失效并发发布、长稳和真机矩阵仍未关闭。正式SHA256=935efbeecd8bd4ed047651f3b44e0f9b144e55295bcd8e0ddec1815279c5c149，下面旧哈希是历史批次；Folder暂停。

**2026-10-21第四批当前：** A11/A19原版阴影重复Alpha提取4→3、成功路径padding回收已修；363原生像素组/6267检查、实际方法计数/所有权、两个负控、构建安装/五轮基础回归通过。整体启动五样本中位仅2208→2172ms，缓存/调度未隔离，冷启动仍开放。当前SHA256=be4cb7f019cfef1ac66ba9aa527b606999edab8634cf5fa02fc7385a5560199d，下面旧哈希为历史批次。失败/OOM清理、真机多ROM/全主题/长稳仍未验，不称内存风险全关闭；Folder暂停。

**2026-10-21第三批当前：** A11/A19纯诊断同图边界重复扫描局部已修，identity+generation保持变更重扫。1007 Android场景8056检查、两负控、构建安装/五轮基础回归通过；GL CPU未同步改善，不归因启动时间差，冷启动仍开放。正式SHA256=ca7c3c809767cfc0eba9c17d96b116d547472cad7e52254760c3b6c5a17ad266，下面第二批/更早哈希为历史记录。无新缓存或绘制/阴影/圆框改变，Folder暂停。

**2026-10-21第二批：** A11/A19颜色分类≤64×64逐像素JNI局部优化已修，303实际Android等值用例、完整4096→1计数及负控通过；构建/签名/模拟器五轮基础回归通过。旧/新/反向旧启动中位2450/1761/1734ms，未证明整体冷启动提速，A11/A19不关闭。Folder继续暂停；三星Share、完整恢复/长稳/跨ROM和严格16KiB缺口保持。当前正式包SHA256为a4b23942db8647478a6e1bf87161ee8c03f6dd5515a372772532ae8057203711，后文旧343fd257等是历史批次。证据与边界见同日开发日志。

## 2026-10-20 当前验收合并入口

此前A07导出/日志/取消/元信息/权限修复已完成本机本地SAF导出、回读预览、取消、同名保护与授权失效入口验收，详见开发日志“连续验收收口”。本轮无生产代码净修改，21组合同回归及正式343fd257…包五轮基础功能通过。测试目录、临时新增授权、备份记录已恢复，旧撤销档hash保持；诊断全局暂停诱发ANR明确保留为测试失败，不记正式包故障。

剩余统一见LAUNCHER_FIX_AND_OPTIMIZATION_PLAN.md顶部表；本轮不关闭整体冷启动、暂停Folder、真实整库恢复/跨provider中断/硬断电、长稳、多ROM、系统HOME/实体光影或严格16KiB。不再按历史“下一项”重复计数；A22用户清后台恢复不再当当前阻塞。安全覆盖仍不支持，同名要求改名。

## 2026-10-20 A07局部：SAF权限拒绝误报普通失败、rename权限异常误回退（已修）

旧查询权限异常负例已复现；现仅SAF导出边界转权限失效并保留cause，rename权限拒绝禁止fallback；普通IO/本地异常不误分。共用错误展示在用户点击时复用原目录选择器。636导出+8UI夹具+85撤销+122worker共851项及构建签名、Android16基础回归通过；真实共用picker打开/取消已验，未授予目录或真机撤权。

下一项专用SAF目录端到端导出/回读/取消验收，先明确目录和授权。真实多provider/撤权/断流/进程退出/断电及安全同名替换仍待办，FileNotFound兼容映射本批未改，Folder性能暂停。

## 2026-10-20 A07局部：失败备份留下指向已删除文件的上次记录（已修）

原先两保存路径在COMPLETE前提交元信息，后续失败删除新文件却保留新引用。现统一以完成journal为提交依据，确认后发布元信息；提交尝试后保留文件和日志供恢复判断，pending元信息失败不删除已完成文件。原cleanup/新备份准入补写并保持完成时间，旧COMPLETE不猜名称。491导出+85撤销+122worker共698项、构建签名和Android16基础入口回归通过。

故障验证为实际方法与受控偏好/provider夹具，新Context不是Android进程重启。下一项为SecurityException权限撤销可能误报通用复制失败；真实provider/非事务URI/断电和安全同名替换仍待办。Folder性能继续暂停。

## 2026-10-20 A07局部：备份日志finish静默失败仍报成功（已修）

旧负例准确复现未发布却true。现FD同步/finish/字节回读全部确认后才发布Entry，过大候选先拒绝，回退异常不覆盖首错。356导出+85撤销+122worker共563项、构建签名及Android16基础入口回归通过。没有真实provider/硬断电故障验收，发布后读取失败返回false不表示磁盘必定仍是旧版本。

下一项：元信息偏好先于COMPLETE日志提交，失败删除新文件后“上次备份”可能仍指它，需负例和最小修复。非事务URI/实际云盘权限和断流/断电、安全同名替换仍待办，Folder性能暂停。

## 2026-10-20 A07局部：备份日志损坏/读取异常被当IDLE（已修）

严格读取base/.bak/.new与父目录条件，损坏或读取异常带明确错误中止；write/reset不覆盖坏/不可读证据。备份准入、预览保存错误处理及checkpoint发布顺序已收口。314导出/85撤销/122worker共521项、构建签名及Android16保数据安装基础入口回归通过。真机未注入日志故障，正常备份页面检查不算备份恢复验收。

下一项：BackupOperationJournal.write仍未检查finishWrite静默失败与写后内容，参照Restore日志的sync/字节回读补证和修复。非事务URI/实际provider断流权限/断电及安全同名替换仍待办；坏日志不自动删，需保留分析；Folder性能暂停。

## 2026-10-20 A07 SAF局部：fallback成功后丢失残留partial追踪（已修）

旧负例：delete拒绝但partial/final都在，方法仍完成。现确认partial已删除或成功空查询确认缺失后才切换追踪，否则pending/FAILED、两URI保留供原恢复入口重试。新增7场景，总247导出+85撤销+122worker检查通过；构建签名、Android16真机安装哈希/基础图标搜索设置回归通过。真机未做provider拒删和备份恢复，不称全SAF验收。

下一项P1：BackupOperationJournal损坏或读取失败被read静默视为IDLE，可能绕过旧操作保护；先故障注入再最小修复。持久化静默失败、非事务URI间隙、真实provider/断电和安全同名替换仍待办，Folder性能暂停。

## 2026-10-20 A07 SAF局部：启动清理失败却reset（已修）

旧cleanup吞delete false/异常后重置日志，失去残留URI。现逐项记录未清理资源、保持非终态、检查IDLE写入；新备份先清理旧操作，失败保留日志并释放本次瞬时锁。空查询确认文件缺失用于删除后checkpoint失败恢复，null/异常保持pending。184导出/85撤销/122worker共391项及构建签名通过，未接真实SAF或设备。

剩余明确边界：fallback成功路径仍quiet删除partial后丢弃追踪，下一批处理；损坏journal/read静默IDLE、持久化静默失败、非事务URI/真实多provider矩阵仍待验。安全同名替换未实现，不能以本批清理修复标记全部数据安全完成。

## 2026-10-20 A07 SAF：破坏性同名覆盖入口已封闭，完整替换待实现

P1已定位：overwrite=true在新文件创建前删除旧备份。旧源码隔离取消负例旧URI丢失；修后同名无论overwrite参数均拒绝并提示换名，旧URI和字节保留；UI取消覆盖入口。目录query失败/null改为后台停止创建。160导出+85撤销+122worker检查及构建签名通过，无真实SAF/设备验收。

功能限制：当前不能同名覆盖，需改名保存，不能将安全替换协议标成完成。TOCTOU并发改动、非事务provider/URI间隙、日志损坏未关闭；下一项处理deleteDocument拒绝时startup仍reset丢失待清理记录。不得据隔离测试宣称全备份恢复安全或Folder提速。

## 2026-10-20 A07 SAF局部：失败.partial遗留、rename URI未跟踪、取消误报（已修）

外层失败时尚未拿到URI，原.partial可遗留；rename URI可能变化且fallback存在第二目标。现writeToTree清理本次对象、成功后使用实际URI、日志增加可选第二URI并由现有startup cleanup处理；关键COPYING/COMPLETE返回失败停止/不报成功，取消归CANCELLED。133新隔离+85撤销+122worker通过，构建签名通过，未连接真机/未访问真实SAF。

仍保留P1：覆盖同名备份会在新文件准备前删除existing，取消/写入失败可能丢旧备份，下一批优先修；provider拒绝清理、非事务URI创建/rename的进程退出小窗口、日志损坏及真实权限/云盘矩阵未关闭。不扫用户目录、不加无限重试，Folder性能暂停。

## 2026-10-19 A07旧撤销快照提前删除、等值token锁释放失败（已修）

取消导出新恢复前快照会先丢旧archive，修为本次独立候选及成功后校验/同步/原子rename发布；checkpoint/启动恢复接管中断。release原CAS按String引用，反序列化同值token会失败，现按内容验证当前owner再CAS，旧token仍不能释新owner。上批“组合夹具遗留owner”结论修正为独立负例确认的生产缺陷。

JVM85+144+122与Android9隔离112检查通过，权限失败旧包完好、测试进程终止后可恢复发布；用户桌面未变且未安装。本批AtomicFile快照发布尝试因API28实际不满足失败保护而撤回，不残留生产。真实SAF/硬断电/空间压力/多ROM全恢复仍未关闭，下一项SAF导出中断及取消清理。

## 2026-10-19 用户回退原图无圆框已修；撤销快照替换边界待处理

旧规则按选中的managed来源禁圆框，和用户本次确认的未匹配回退期望冲突。Host以本次effectiveType判定，准备/合成/key使用同一类型；旧Host负例IMPROVED失败，334策略/59图像/289合成及正式安装一次功能回归通过。设置没有被自动关闭，选择不被回退改写。其他已匹配图案消失不是用户此次现象，不在本批作根因结论。

恢复检查点144/worker122通过，但新建快照先删除旧rollback_latest的取消/失败边界仍需验证与修复；不记为已关闭。补锁断言失败是组合夹具遗留owner，撤回改动，未把它记为生产故障。下一项精确处理旧撤销快照替换，完整真实恢复/多ROM仍开放。

## 2026-10-19 A07局部：预览缺拓扑检查及文件夹环漏检（已修）

孤儿引用修前已被Importer写前门阻止，本批补预览的同Owner调用；不要描述为已复现数据损坏。自引用/双向环因父ID存在漏过原拓扑检查，现源/DB共用迭代查环。143 Android隔离SQLite及144 checkpoint检查通过，构建/签名/100暂存保护通过，未安装或改用户布局。重复位置/特殊页全部语义、真实SAF/中断/多ROM仍开放，损坏有环旧数据会明确拒绝，不静默修写。下一项取消/失败后文件及锁生命周期。

## 2026-10-19 A07局部：纯文件夹页预览漏计（已修）

BackupArchiveReader.pageCount对folderIndex>=0全排除，与itemType=2根文件夹和Importer/Pending占位规则不一致。只修谓词、保留其他边界。修前52项套件首例预期1实得0；修后52预览、25偏好、真实Android独立SQLite120项通过，构建签名/100暂存保护通过。未安装或动用户布局，A07完整归档/SAF/断电/多ROM未闭环。下一项检查异常结构写前校验；Folder性能继续暂停。

## 2026-10-19 A07局部缺陷：缺主题回退写入失败未拦截（已修）

applyArchive在缺主题包时忽略保留原主题的commit(false)，仍可COMMITTED。故障注入修前准确失败，生产最小加返回值检查并抛IOException，复用现有checkpoint/回滚/重试。修后31检查覆盖5场景，既有144/122/25回归通过，构建签名/对包差异/100暂存保护通过。实际用户设备未复现此储存失败，不外推为当前现场根因。

A07完整旧档/SAF/分身/真实崩溃恢复未关闭；本批未安装或动设备数据。Folder性能按用户要求暂停而非解决。下一项旧格式缺省字段与页面/文件夹布局导入核对；证据及APK身份见同日开发日志。

## 2026-10-19 Folder首次步长漏门已修，主停顿继续开放

已证实移植elapsed时钟在输入创建Folder当帧漏过原有活动门：首动画步63.6–108，后续约20。Ra.T按前后Folder身份且opening条件补门，Eb复用原fx归一化；输入事件/物理回调不变，不加延迟/重试。346分支检查、64数学检查及旧源码负对照完成，Android9候选五次首步均19.999998且逐帧尺寸一致。正式1bb4只classes.dex改变、签名/安装hash/静态像素五对/100暂存保护通过；功能详情见开发日志补充和formal-ui。

仍有72–84ms正式GL长帧，Folder打开前阻塞和冷启动不得关闭。下一项几何复用需覆盖布局/资源/尺寸变化失效与可变数组所有权；不跳过来源校验。原APK归档缺失，参考clean/raw，未冒称新反编译。Android16/高刷/多ROM/长稳未验。

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

## 2026-10-19 图标包失效补齐，搜索回归保持失败状态

resetCache漏清候选、所选包事件漏全局AUTO/无redirect用户已局部修复，复用原Owner/worker/更新队列。修前两组失败、修后18边界与64/12既有检查通过，无新键/Bitmap缓存，文件/异步来源尚无完整失效屏障，保留来源校验。所选包事件会合并全部Launcher包额外重绑一次，来源选择不变。

5297d96f保数据安装API28，五轮Folder/图标/设置BACK同PID通过，五对静态画面相同；搜索开关开启但上滑未打开，查询未执行，不能记完整回归通过。五组GL墙钟仍有58–125ms量级长帧，不是CPU/物理呈现提速证明。真实包替换/卸载/选择矩阵、本轮API36及长稳未验；修前旧总套件提取过期、目录shell权限失败保留。下一项优先定位Android9入口，再回到Folder初始CPU；详情见开发日志10/19及verification.json。

## 2026-10-18 Folder节拍及高刷协商局部修复，初始阻塞未关闭

确认两处兼容差异：GL生产回调时间直接推进动画，与均匀显示节拍产生27.6/7.2的步长摆动；Surface未声明能力时，面板/菜单120也可能应用只60。最小改动仅Bridge、Eb.update、SMGLSurfaceView：Folder过渡按应用当前帧率归一化原fx；既有Surface/可见生命周期声明同分辨率支持能力，由系统政策决定，不修改分辨率或系统设置，无新Manager/监听器/轮询/图像缓存。全局elapsed、恢复0、100ms及按住保护、原版_r/曲线保留。

64/12边界、实际60/120各五组、最终五轮图标/搜索/设置及五轮翻页返回通过，签名/安装hash/53暂存/临时诊断清理通过，刷新率恢复原智能适配及peak/min。保留标准模式CPU50.873ms长帧和高刷录像374ms异常，不能标记Folder整体不卡或冷启动已解决。下一项核对来源更新失效Owner，再评估原版先查纹理热路径；禁止无证据缓存key/Bitmap。90/144实机、多ROM/外接、动态图/九应用、掉帧/温控/耗电/长稳仍开放。详见开发日志最新条及build/folder-open-chain-20261018。

## 2026-10-18 Folder资源表重复查询局部关闭，整体现象保留

当前兼容图标路径对同资源表反复getIdentifier。复用已有Repository保存有界整数ID，按资源身份/AssetManager/Configuration分组，配置及低内存失效，失效竞态禁止旧查询回填；文件/目录/variants及实际Drawable继续实时判断。三组热打开49次ID请求均不再进入原生查表，80边界和1665键来源检查通过，负例证明缺失配置清理会失败。不缓存Bitmap，无新增Manager/延迟/动画改变；未验资源loader/ROM overlay动态注入及长期内存争用，不能声称内存降低。

正式c034c864五组CPU中位略降、五轮功能同PID通过，最坏GL36.629ms仍保留，未证明整体稳定提速或文件夹不卡。DT1902A原版8方法和五轮实际开关对照完成，原版仍同步创建绑定再启动动画；不同设备/数据不作速度比。旧黑屏/未打开样本排除。下一步转首次运动与输入到显示时间线，停止重复已关闭的hash/PM/坐标/ID微优化；系统HWC内部、九应用/动态/多ROM/冷启动仍开放。正式包安装hash/签名/临时诊断清理/53暂存保护通过，详见开发日志最新条。

## 2026-10-18 Folder重复坐标复制局部关闭，CPU长帧仍开放

新增确认：原版逐格ir取得坐标的循环，在当前新增adaptPositions兼容层下放大为每开9次整组复制/81点。只M.fn内对FolderPage持有本次副本，修后1次/9点，每次fn重新取得；普通桌面不复用，原几何/逐格adjustY不变。实际三组次数及10对场景像素、最终5轮图标/搜索/设置返回通过。生产无新字段、缓存、线程或动画改动，正式62e887e1安装hash/签名/临时恢复/53暂存保护通过。

仍有scheduled23.470ms CPU起始帧与31.294ms dequeue等待，整体顺滑/冷启动未关闭。保留第4次日志门超时（PID日志0字节而桌面正常，原因未知）与一次电脑ADB服务中断；后两组性能用截图就绪门，UI完整重跑5轮通过，不掩盖失败。仅API36单机三应用九格，未验九个实际应用/动态图/拖拽/多ROM/长稳/物理显示；不把P16对齐当严格16KiB库验收。证据与下一资源匹配CPU细分见开发日志最新条及build/folder-scene-bind-20261018/verification.json。

## 2026-10-18 Folder风险更新：背压与起始CPU分开

原34.709ms样本的dequeue等待与SF上一HWC帧pending、commit不合成及后续旧缓冲释放直接对应；不再登记为34ms图标持续CPU，但厂商显示延迟内部原因未知。正式同机五组262次桌面锁存可对应显示token，另1次末尾缺失；115次>10ms dequeue均有释放，多数显示更新仍按当前约60/90Hz cadence前进。FrameTimeline缺桌面SurfaceView应用帧，不能使用状态栏的App Deadline Missed给Launcher归因。

另外两次再开起始显示间隔22.203/22.024ms仍未修复；其中23.801ms帧scheduled21.864ms，dequeue仅0.172ms，单列起始CPU问题继续查节点/材质/文字绑定。无新缓存/缓冲参数/动画改动，生产不变；五轮功能与诊断撤回后1轮通过，安装hash/53暂存/临时源码恢复通过。单机三静态图标、缺原APK运行对照/物理显示/全ROM/九应用/长稳，不改变整体未验收状态。详细证据见开发日志最新条及build/folder-buffer-wait-20261018/verification.json。

## 2026-10-18 Folder PM/label重复工作已减，BufferQueue等待仍开放

Host仅复用同一次键生成的已确认ResolveInfo、删除未被使用的label读取，不保留跨调用快照/缓存；二次图标可用性检查及正常Drawable加载保持。480组合完整key相等、1670检查及旧Host负例通过；三组真机每开组件解析7→5、无用label 2→0、hash仍1。正式25d0ab51…构建/签名/安装hash、五对像素、五轮实际搜索查询/设置返回同PID及53暂存保护通过。

正式五组首开中位24.153→21.399ms、再开23.378→24.816ms，最坏首开升至34.709ms，不能宣称全性能改善。该帧GL scheduled约1.920ms、休眠32.789ms，dequeueBuffer外层32.973ms，具体缓冲释放/fence/SF归因未证明。PM/label局部任务收口，下一项转文件夹打开的缓冲获取/释放和可见帧时间线，不重复来源hash或改动画猜测。Folder总体/九应用/全ROM/长稳仍未收口，不增加独立完成编号，完整原始证据见开发日志最新条与build/folder-source-resolution-20261018。

## 2026-10-18 Folder已确认APK回退的重复读取已修，整体性能保留部分完成

真机三应用中翻译机/对讲机虽全局IMPROVED却实际DEFAULT回退，此前指纹漏覆盖；纹理命中前仍加载并hash原图。现复用loadIcon现有强制原图/二次override/最终回退Owner，仅键路径的准确组件/主用户AUTO-IMPROVED确认APK回退可使用原安装/资源指纹；中途来源到达仍取图片，未知元数据仍旧路。无新增缓存/动画改动，弱hash与批量读取候选已撤回。正式仅Host、480/1185检查通过，旧Host新负例失败。

V2458A正式各五组首开/再开最大GL回调中位28.655→16.922 / 36.739→23.334ms，五对像素一致、五轮实际搜索查询启动/设置返回同PID；c7ae5701…签名、安装hash及暂存保护通过，临时诊断移除。该具体回退重复工作关闭，Folder总体/冷启动/物理present仍开放，下一步细分剩余PM/label/来源重查；不重做已关hash链或扩大完成编号。原APK缺档、九应用/动态图/其他ROM/长稳仍未验，详见开发日志10/18最新条。

## 2026-10-18 Folder DEFAULT来源键局部修复，性能总体开放

已确认并移除明确DEFAULT在纹理缓存查询前加载APK Drawable的工作，安装/资源配置指纹复用现有Owner；受管来源及元数据不完整仍走旧链。Host/Raster两文件、无新缓存/预热/动画变更，来源1168项在9/16及新Android16真机通过。首次raw DB hash候选导致纹理失效退化已撤回；正式fb6506d5…构建/签名/安装hash与53项暂存保护通过。

Android16真机V2458A原有三应用Folder修前后各5组：首开最大GL回调中位29.210→26.070ms、再开33.344→34.696ms；五对场景像素相同、五轮实际底部上滑搜索/查询启动/系统及桌面设置返回同PID。局部正确性通过，不能宣布整体流畅度/冷启动关闭。系统拒绝正式包ART shell profile，剩余真机子调用未定位；下一步可移除诊断包、采样与正式时长分开，不换任务或盲改原版动画。旧Android9修后、三星Share现场及全ROM仍未验，A01–A25计数不因本子项重复增加。完整失败与证据见开发日志10/18。

## 2026-10-17 Folder首开专项继续开放

API36硬件GPU两应用Folder五组首开/再开最大GL回调中位48.723/17.515ms；两次ART将具体阻塞收敛到Cell.cb在纹理缓存查询前构造来源键时的DEFAULT系统APK资源加载/图片解码。来源哈希承担换图有效性，尚无安全删除/复用候选，未改生产，不增加已完成编号，A01–A25主登记统计不变。

五对图标区域像素相同，另五轮Folder应用启动/搜索入口/桌面设置同进程通过；不是物理可见帧或真机矩阵验收。下一项仅核对现有来源指纹失效Owner与同版本精确读取，不返回已收束的冷启动来源循环。完整数据、无效路径和边界见DEVELOPMENT_LOG当前Folder条目、性能/功能报告及build/folder-first-open-20261017/verification.json。

## 2026-10-17 A25 / P1 / FIXED_CONTROLLED_CACHE_AND_API36_PAUSE

A25：下载校验只验证各PNG分块CRC，缺少图像数据、空IDAT、重复IHDR等仍能被写入缓存并阻止备用镜像；CRC正确而压缩流无效也会被发布。单镜像读入超过512KiB或响应期限时直接return false，跳过备用镜像。原始用例8断言失败，补充压缩流用例又确认2项实际失败。初始测试认为Android一定拒绝坏Deflate，实测9/16均可能返回部分Bitmap；该测试假设已纠正并保留原输出，不把native非空当有效性证明。

只修改现有IconPreviewRepository：沿用原CRC/尺寸/字节上限和写盘Owner，补充首个唯一13字节IHDR、实际IDAT数据及IEND边界检查；同Owner的hasValidPngData使用标准Inflater流式验证共享IDAT压缩流，8KiB缓冲、解压输出上限9MiB（涵盖现有1024边长RGBA16与Adam7），finally释放Inflater，不分配像素、不另建PNG像素解码器/缓存/线程。超限只终止当前镜像响应并进入既有备用链；取消仍立即返回且不尝试备用下载。像素文件不重编码，镜像顺序、超时数值、online_icon_cache_v4及负缓存一小时策略不改，原A24修复保留。

JVM37、Android9/16各44、原队列161/页面14及实际库分类/网格各5轮暂停恢复通过，边界见功能报告。主登记扩至A01–A25：15局部完成、2部分、6开放、1历史现象合并、1候选撤回，不计算总完成百分比。同名更新验收仅限显式成功发布后的文件替换和新进程可见性；不新增远端自动刷新，发布同名资源仍遵守原缓存版本机制。本批不批量删除/重验历史缓存，不宣称完整PNG语义验证或全部线上坏包已关闭。原APK归档仍缺失，clean/raw/maintained无同名Java Owner，备用镜像行为按当前规则及PNG规范核对（https://www.w3.org/TR/png-3/）。真实镜像慢网/复杂坏包、旧缓存迁移、跨ROM、三星S25U Share现场及长稳仍未验收；冷启动整体未解决，清后台已恢复的返回现象不再复测。下一项转文件夹首开长帧：先确认实际可见卡顿与调用，不重复本轮缓存采样。

## 2026-10-17 A24 / P1 / FIXED_CONTROLLED_AND_API36_SCROLL

A24：预览低优先级任务排队期间，可见P0订阅加入相同pending批次，会话96阈值裁剪仍依据原P1/P2任务挑选，给可见行回调null；设置适配器会将该图标清空。另全局淘汰在检查消费者之后、队列移除/批次detach之前释放pending锁，允许P0订阅加入即将被丢弃的批次。前者修前新增用例6断言失败；第一次局部修后再加可控并发门，后者修前仍1断言失败；原始负例/中间APK和首轮UI均保留。

仅修改现有IconPreviewRepository：PendingCallback携带本次订阅Priority，保留旧双参构造；会话裁剪跳过有有效P0回调的共享批次。会话选择/移除/完成detach和全局检查/淘汰或拒绝/detach在同一pending临界区内完成，避免可见订阅在中间加入旧批次。全局继续renderAdmission→pending顺序，没有解码、网络、等待栅栏或同步UI回调进入锁内，没有增加Manager/队列/线程；既有512全局上限及8槽metadata预留不变，96原本就是低优先级裁剪触发阈值，不把它称为全P0硬上限。P0超出全局容量仍明确回调null，不宣称无限负载全成功。原有7行schedulePersistence保留，未覆盖用户暂存。

JVM/Android9/16各161项、正式构建签名和API36五轮滚动回归通过，详见功能报告。主登记扩至A01–A24：14局部完成（新增A24）、2部分、6开放、1历史现象合并观察、1候选撤回；不计算总完成百分比。本批证明并修复设置图标队列的受控可达丢回调路径，不能认定是三星S25U常用Share缺图的同一根因；三星现场、完整图片/全GPU压力、长期锁争用/峰值PSS、真实后台压力、全ROM、完整恢复及严格16KiB仍未验收。冷启动整体仍未解决；用户确认清理后台恢复的返回现象不再单列复测。下一项转图标库坏包隔离、暂停后取消、同名图片替换及跨进程缓存有效性；不重复本批已通过用例制造新进度。

## 2026-10-17 纠正当前任务范围与GPU结论

结论：之前SwiftShader约1秒的纹理分配等待明显受软件后端影响，不能据此认定正式APK存在同名重复纹理/Shader创建，不能外推真机；后端内部排队/同步根因未证明。本项阶段排查收束，无正式修复，不继续围绕同一来源/首轮纹理路径循环采样；整体冷启动仍未验收。

用户再次明确：清理手机后台后返回桌面已恢复。A22撤下当前独立复测/修复，不再要求解锁，历史日志保留；仅将内存压力观察并入A18长稳边界，不把用户恢复现象当已证代码根因。下一项转图标P0可见任务队列峰值、取消与旧回调边界；既有production preview 61项通过，只补缺失压力/真实Android边界。主登记13局部完成、2部分、6开放、1历史现象合并、1候选撤回；不计算总体完成百分比。

本批无正式修复，查询结果输入烟测未通过，入口烟测通过，不能计为全项目验收。细节及数值见性能/功能报告。

## 2026-10-17 用户纠正：返回加载现象已恢复，撤下独立复测

用户此前已说明清理后台应用后返回桌面正常，本次再次明确不需要重复测试该现象。A22历史Create/SIG9证据保留，不继续作为当前独立故障排查，不要求用户解锁或开启日志。未证实的内存压力阈值/长期行为仅并入A18长稳边界，不把恢复现象写成已证代码根因。主登记改为13局部完成、2部分、6开放、1历史现象合并观察、1候选撤回，不计算总完成百分比。GPU对照收束后转图标可见任务队列压力/取消与旧回调边界；旧章节中的“下一项A22”均被本记录覆盖。MEMORY.md未更新。

## 2026-10-17 首轮绘制/纹理/Shader核对

五轮诊断均34个不同材质纹理miss、4个不同Shader创建，绑定后36次glGenTextures内部wall合计约1.03–1.24s；未证同名重复或可删除原生成。Ea/ta/程序ID缓存门存在，正式代码和APK恢复b09ead0c…，53项暂存保持。同包API36五样本/五轮功能及两页对照见功能报告。下一项先做Android16硬件GPU后端与当前SwiftShader的同路径对照，或在可用真机采同一GL阶段，分开资源解码、纹理分配/上传及驱动等待，确认可移除工作再最小修复。冷启动整体、可见帧、真机UI/三星Share现场、全ROM/长稳及严格16KiB仍开放；A11/A19部分、A22等开放的登记不变。

## 2026-10-17 补写生成/编码/写库采样收口

正式b09ead0c…未改：五轮每轮21项中20次MD5命中、1次日历强制重建，24次PNG编码、1次写库接口返回true。DONE不是写库次数；现有动态/普通模式交接保护尚无安全替代，不删除。诊断入口与产物已逐字恢复、原53项暂存未变。同包API36五次启动和五轮搜索/设置/图标查询往返完成；本批两页加载中截图作废、最终事件日志未补取，真机UI未测，不扩大验收结论。A11/A19仍部分完成，A22等开放，主登记数量不变。下一项重采绑定后首轮绘制、纹理上传和Shader创建；冷启动整体未解决。

## 2026-10-17 主登记问题进度口径

最新补充（UNCACHED_STATIC_SOURCE_COMPOSITION_AND_POST_READY_LOAD）：b09ead0c…将无缓存普通静态分支也纳入一次同步来源/分类/合成，保留原512补写Owner和fallback，隔离类型/身份2→1，独占准备副本及时释放。Android9/16各289+246项及API36主五样本、独立后台各五、两页像素/五轮同PID6637通过。末项补写仍约1.1s，未证整体冷启动/后台负载/内存稳定降低；A11/19继续部分完成，A22等原风险不撤销、不新增问题编号。下一项定点采样补写原生成/编码/数据库链。详细限制见本日开发日志。

最新补充（CALL_LOCAL_STATIC_SOURCE_COMPOSITION）：最终f2d0af9b…；已有有效缓存的普通静态分支在同一同步调用内传递现有StaticSource，非圆框正式请求2→1，独占准备图finally释放、独占原图解码仅成功后回收。坏缓存、无缓存及缺源保留原路径，无跨调用图像缓存。Android9/16隔离及API36五样本/两页零像素差/五轮同PID5357通过。A11/A19仍按原部分完成口径，无缓存首建/补写、冷启动整体及原A22等未闭环，不增加问题总数。详见本日开发日志及性能报告。

上批0e4c466c…：A11局部补充已量化prepare/compose两阶段来源请求及独占/借用分支；仅消除装饰日志再次解析来源类型，80组输出/归属对照通过。Android9/16隔离、API36前后各5样本/两页像素一致/五轮功能同PID5343通过。A11仍为部分完成，A22等原风险不撤销，不新增编号或夸大进度。详见本日开发日志。

A01–A23按主问题去重：13项局部修复/维护并有对应回归（01/03/09/10/12/13/14/15/16/17/20/21/23），2项部分完成（11/19），7项未闭环（04/05/06/07/08/18/22），1项不可达生产候选撤回（02）。历史A12 legacy标识同号备忘不另计，A18已由用户恢复但压力/系统策略根因仍开放。编号有父子依赖、验收深度不等，不以此计算全项目完成百分比。最新剩余任务按优先顺序集中于LAUNCHER_FIX_AND_OPTIMIZATION_PLAN顶部；旧失败/未验记录不撤销。

## 2026-10-17 单次纹理键来源复用

最新正式APK 0d9794b8…/v1.5.8/33，以下旧包作为历史保留，原53项暂存binary patch不变。

| ID / 优先级 / 状态 | 根因及修改 | 验证与边界 |
|---|---|---|
| A23 / P2 / FIXED_CONTROLLED_AND_API36_PATH | 纹理键hash、type有效性和identity重复请求正式来源；CUSTOM完整读取还解码/重编码PNG。既有ManagedIconSource带本次Drawable/type/identity，内部重载接收已读redirect；只复用单次键内、普通用户精确组件的已命中来源。 | Android9/16各480组/1093项，完整键相同；CUSTOM解码/编码4→1、IMPROVED来源请求2→1。未命中metadata=null，原路径重查，覆盖PACK回退时可用；动态/分身等保留原链。构建/签名与API36前后各5次、两页像素一致、最终五轮功能同PID通过。基线波动大，不能认定整体启动稳定提速；异组件资格探测及全ROM/真机主APK尚未验。 |

A22首次Activity重建风险未关闭，不能用API36同进程结果覆盖Android9历史失败；整机压力、完整恢复、原生16KiB、光影与全ROM边界不变。下一项核对准备/合成阶段剩余来源重复及所有权；细节见本日性能/功能报告与DEVELOPMENT_LOG。MEMORY.md未更新。

## 2026-10-16 剩余路径采样续批

当前正式APK为e3d84deb8fc8157ce2cf5a93945bda5693dee084155e729a4accc512c6d57fe3（v1.5.8/33），以下旧包/阻塞组保留历史。本批只复用既有来源类型，不改原版SMEngine、颜色分类、阴影或生命周期；原53项暂存binary patch对照不变。

| ID / 优先级 / 状态 | 根因与证据 | 修改及验收边界 |
|---|---|---|
| A21 / P2 / FIXED_TESTED_PATH | resolveStaticSource/buildTextureCacheKey刚解析类型，identity又重新调用类型解析和有效来源检查；两次真机trace重复路径一致。 | 原Host增加包内重载，两个调用点传入紧邻已解析类型，保留单参入口。720组/3690项对照及481项Android Bitmap等回归通过；修后两次trace无identity→type子路径。真机各5样本PAGE_READY中位3048→2827ms，桌面两页区域零像素差；首次GL回调基本不变，不外推全ROM/首装。 |
| A22 / P1 / OPEN_FIRST_RETURN_RECREATE | 正式UI首轮旧PID2957重新Create/MAIN_VIEW_INIT后自行SIG9，换为3629；与原重复初始化保护相符，未抓直接调用栈及Activity重建触发条件。 | 保留首轮失败，不归为ABE，不隐藏加载或修改原生命周期。后续补充5轮逐轮记录PID，搜索/结果启动/设置/图标查询均同PID3629；API36另5轮系统设置返回同PID4642。只证明后续稳定路径，重建原因仍待定位。 |

A18清理后台后的稳定返回已取得本批修前5轮同PID及修后补充5轮证据，历史ABE样本不撤销，内存压力/系统策略具体阈值仍未确认。纹理预载已有缓存检查，原颜色分类未证明冗余；后续核对resolvedSourceHash、来源有效性及正式绘制的同图重复读取。完整冷启动、全ROM、长稳及原16KiB/恢复/光影风险仍开放。日志已恢复no、只读AVD已关闭；详见本批性能/功能报告及DEVELOPMENT_LOG。MEMORY.md未更新。

## 2026-10-16 追加审计与最小修复

本节是10月15日基线之后的增量结论，旧章节作为历史保留。最新APK 5e1b3d1b…；真机X21A/Android9。既有53项暂存blob不变。

**A18最新状态：USER_RECOVERED_ROOT_CAUSE_OPEN。** 用户清理手机后台后报告返回正常；当前只读MemAvailable约3.40GiB、Launcher PSS约204.7MiB/Graphics约111.4MiB。下表阻塞样本保留为清理前历史，未追加5轮同PID验收。内存压力/后台负载为优先验证条件；缺触发前压力证据，不能据此确认Launcher泄漏、LMK或ABE具体强停阈值。生产代码未修改。

| ID / 优先级 / 状态 | 实际根因 | 最小修复与验收边界 |
|---|---|---|
| A20 / P2 / FIXED_STATIC_CACHE_MISS_PATH | 真机两次采样的GL PNG压缩约1.2s；受管静态图标无旧iconRawData时被DEFAULT专属门挡回旧缓存/三套图像生成，然后再次正式合成。软件GPU的GL创建热点不能外推该真机。 | 只去掉prepareUncachedStaticSource的DEFAULT限定，复用既有正式来源和页面就绪后的有界补写，不改DB阶段门/原阴影/数据格式。修前IMPROVED负例失败、修后及相关回归通过；真机同机5样本PAGE_READY6315→4553ms，29项补写全DONE、五轮UI及即时搜索通过，API36同包5次完成。页面就绪不是物理呈现/低CPU证明，后台帧率/全来源ROM矩阵仍未验。 |
| A12 / P1 / FIXED_IN_TESTED_PATHS | SearchIconBackend全量hydration挤出encoded LRU；Top5只读LRU，visible miss直接返回null；Oe为空无来源恢复。代码负例确定复现，不能据此断言S25U的Share现场只有这一原因。 | 原worker内补载、按模型ID定点clone并校验身份、沿原最终合成器恢复；缓存容量保持。主机负例和真机真实PNG/Looper11项、正式UI常用图标5轮均通过。三星/Share原现场未验。 |
| A13 / P1 / FIXED_CONTROLLED_REGRESSION | 暂存启动优化使用会被P2暂停/队列策略丢弃的必要PNG补写任务，pending/pageReady阻止恢复。 | 原有界IO池单批提交、明确接纳结果、拒绝后在真实page/source事件重提；不改变预览P2丢弃策略。暂停、单槽批次、重复事件、队列拒绝/重提、替换身份检查通过；未删除真机图标缓存强行制造冷缺失。 |
| A14 / P1 / FIXED_VIVO_PATH | 正常起点排除底部96dp，与Dock上滑提示冲突；X21A 2100起点超过旧1913上限。 | 允许应用表面内Dock起点，其他手势校验不变。旧Owner负例失败、修后81项通过，正式包Dock上滑5/5；1100ms仍拒绝。Android9 ADB事件downTime问题在测试工具解决，未放宽生产身份门。 |
| A15 / P2 / FIXED_CONTROLLED_REGRESSION | 图标库防抖/查询被pause取消后，resume只重绑旧rows，当前输入可能一直显示旧结果。 | 页面Owner内记录查询是否待发布；仅待发布时恢复查询。生产方法修前负例失败、修后6项通过；真机已完成查询和图标可见，但未让真实后台查询稳定命中暂停窗口。 |
| A16 / P2 / FIXED_CONTROLLED_REGRESSION | 图标目录加载失败时重试文字写到此前GONE的loading.message，提示不可见。 | 同一失败处理方法将文案设为VISIBLE；生产方法负例/点击回归通过。未在真机故意破坏目录注入故障。 |
| A17 / P2 / OPTIMIZED_MEASURED_LOCAL | IconManager应用名、Host桌面别名/强制原图/手动覆盖四个元数据调用，CUSTOM时触发完整读图/解码/PNG编码且不消费字节。 | 四行改用已有getRedirectIconMetadata；42项Android隔离、29组主机回归与合同审计通过。相同512PNG、24个名称读取的5轮wall中位2314.076→0.773ms，图片IO24→0；只证明局部工作消除，不宣称整机提速。真正读图/备份消费者不改。 |
| A18 / P1 / BLOCKING_EXTERNAL_RETURN | 用户反馈Android9外部返回出现加载动画。当前vivo离开桌面后进程消失、包stopped由false变true，实时am_kill确认stop by com.vivo.abe。新5e1b3d1b…与旧4944e939…各5次均换PID；更早10/11交接实验前50a8befb…APK也5次均换PID，J/Eb普通恢复方法与现行相同。 | 暂停后续性能修改。授权自启动开启5次、恢复关闭5次均失败，已恢复关闭，不能认定该开关为根因；交接实验未获因果证据，API34/36实验不适用API28。继续定位ABE具体触发条件，外部热恢复仍FAIL；5次真实返回同PID且无冷加载及相关回归才解除阻塞。不得用保活/重复HOME/固定延时或隐藏Loading规避。 |
| A19 / P2 / PARTIAL_LOCAL_OPTIMIZATION | DEFAULT圆框已有有效Bitmap，合成阶段仍加载Drawable后立即弃用；API36前两页21图标每轮加载42次。绑定后的完成事件0–2ms已入队，额外ART采样约1.92s在首帧render，重点纹理/Shader创建。 | 仅省掉该组合第二次加载，每轮42→21、局部中位283→142ms、桌面区域像素一致；481项Android分支检查和两设备各5次冷启动、vivo五轮搜索/设置/图标查询完成。软件GPU整体候选中位仍高于基线续组，未证明启动提速或不退化；原阴影/投影/GL完成门不改。下一项真实GPU调用与重复创建定位。 |
| A03补充 / TEST_FIXTURE_FIXED | pending_worker Android夹具缺IconPackManager.invalidateIconPackPackage及Host.onIconPackOverridesChanged。 | 只补当前接口，重跑39项通过；不是生产安装崩溃。 |

A04–A08继续保留风险边界；A11的四个元数据消费者已按A17窄优化，图片读取Owner仍保留。A04补充实际API37/PAGE_SIZE16384/x86_64启动与12→20重载可见，系统记录pageSizeCompat=4，未禁用兼容模式，不能据此关闭原生ELF合规缺口；按用户要求已停止只读副本，后续完成vivo正式包5轮回归。完整恢复、系统原生HOME交接、光影手持与全ROM不随此批关闭。详细实现、APK身份及修改文件见DEVELOPMENT_LOG本日记录。

状态：只读盘点及重点执行链深读已完成；完整设备矩阵未完成，不能称全功能已验收。当前 137 Java / 3712 Smali；没有逐条证明全部 Smali/native/资源语义安全。基线 main / 5d13886328d94840391a946132f393ad940a84ba，保留全部既有暂存内容。证据在 build/full-project-audit-20261015。

## 修改前登记

| ID / 优先级 / 状态 | 位置与调用链 | 现象、证据与根因 | 最小方案、风险、验证 |
|---|---|---|---|
| A01 / P1 / CONFIRMED | DesktopRestoreController.validate → BackupValidator.validateCustomIcons:163 / validatePortableSources:191；IconBackupCodec.encode:38 / restore:110 | 验证使用完整解码且不释放临时 Bitmap，portable 在解码后才检查48..1024尺寸；RestoreIconSourceReconciler.validSource:242虽释放但同样事后检查尺寸。压缩字节上限不限制解码内存；确认分配路径缺陷，尚未复现生产OOM，不标永久泄漏。 | 复用IconBackupCodec集中边界校验、按需采样验证并finally释放；原图字节不改。风险为损坏图片识别边界；负例/字节/Android PNG回归。 |
| A02 / P2 / SUSPECTED_API_ONLY | SearchIndexRepository.rebuildAsync:250 → finishIncremental:386 | 增量待执行时rebuildAsync只置fullRebuildRequested；最后一次finishIncremental看到该标志仍设DIRTY，没有调度全量任务，后续warmup被DIRTY挡住。公开API组合负例能复现；后续追踪发现当前生产warmup持stateLock且主动拒绝DIRTY，未找到实际生产调用能设置这组状态。不得按可达生产BUG报告。 | 候选已完整撤回，SearchIndexRepository与任务前逐字节一致；保留可选--probe-deferred-api负例和正常路径6项检查，不为假设调用新增状态推进。 |
| A03 / P2 / CONFIRMED | tools/tests/restore_journal/run_tests.py:87-94，restore_worker复用同夹具 | 基线两套测试均javac失败；集中检查另发现test_uninstall_model缺SQLiteTransactionListener夹具：ThemeBackupCodec.encode/restoreWallpaper与encodePortableSources旧签名。不是生产崩溃证据。 | 仅更新夹具接口，保留故障断言；逐套重跑。 |
| A04 / P1 / CONFIRMED_COMPAT_GAP | build/launcher-signed.apk → lib/x86_64/liblauncher_opt.so | ELF LOAD p_align=4096，arm64为65536。ZIP对齐成功不证明ELF适配。当前模拟器page size待记录，不能证明16KiB运行。 | 不二进制盲改；保留原库，记录需相应ABI构建来源及真实16KiB设备验收；不扩大为所有ARM设备失败。 |
| A05 / P1 / KNOWN_BOUNDARY | LauncherHomeCompat / SMGLSurfaceView / HOME_RETURN_COMPATIBILITY_AND_REFACTOR | 历史SF父窗口/Task隐藏时已有buffer仍不可见；普通APK不拥有Recents合成权限。本轮没有OPPO现场。 | 不重做截图/固定延时/TextureView旧实验，不改SMEngine；模拟器键HOME不能充当原生手势修复验收。 |
| A06 / P1 / NOT TESTED | Sensor注册/八层投影、ActiveIcon/Folder callback与主题交接 | 当前具备callback线程资格、epoch、层完整性/Context失效门；手持光影三现象缺同一事件录屏和sensor→GL→SF对齐，本轮不凭代码确认根因。 | 原公式/材质/时机保留；隔离sensor与原主题合同检查；实体机矩阵待验。 |
| A07 / P1 / NOT TESTED | RestoreRecoveryGuard.beforeDatabaseOpen / BackupOperationLock跨进程writer | 保留同步数据恢复安全门；真实大备份/提供器/崩溃恢复等待上限无当前数据。不能为提速跳过安全门。 | 回归journal/worker/真实PNG归档隔离；用户原布局不恢复测试。 |
| A08 / P2 / SUSPECTED | IconBackupCodec customFile=Integer.toHexString(identity.hashCode())；RedirectIconDB同命名 | 32位hash存在碰撞可能，属于现有存储合同；未发现用户具体冲突，不能仅改备份名称导致恢复不一致。 | 独立迁移专项，保持旧档读取；本轮不改。 |
| A09 / P2 / CONFIRMED_MAINTENANCE | BUILD_GUIDE当前版本v1.5.4/29、APK_STRUCTURE v1.5.7/32 vs 当前源码v1.5.8/33 | 文档版本过期；最终badging为准。 | 本轮报告记录真实版本；不对文档里的历史命令作全量替换。 |

## 施工顺序

批次1：A03回归基础；批次2：A01图片验证资源与边界；批次3：A10搜索入口手势（A02候选撤回）。每批保存差异并回归。无已测性能瓶颈证据的候选不做优化，P3删除不强行凑数。A04–A09保持明确边界，后续更新结果追加于本文件。


## 后续定位与实际施工

| ID / 优先级 / 状态 | 代码位置/触发 | 证据、根因、方案与风险 |
|---|---|---|
| A10 / P1 / CONFIRMED → FIX_IMPLEMENTED | launcher/smali/com/smartisanos/launcher/a/a/a.smali private a(FFJFFJZZ):140/196；gesture/VerticalGestureDirectionConfig | 当前模拟器1080×2400/density480：1800→1100/300ms进入搜索；1800→800/250ms未进入，1700→900/650ms未进入。私有方法p5是终点Y，却调用passesSearchStartRegion（高密度下终点必须>840）；同时仍是500ms时间门，违反当前搜索冻结文档1000ms。原版clean方法要求向下终点>=H/4。本批复用方向Owner新增镜像终点谓词，原向下>=H/4、向上<=3H/4；DOWN的起点、单指、方向/距离、去重门保留，完成时间恢复1000ms。76项生产Java边界与Smali接线检查，运行时结果见回归报告。风险：慢滑/反转方向的厂商触摸分发，需要跨ROM实测。 |
| A11 / P2 / PARTIALLY_OPTIMIZED / 读图Owner保留 | RedirectIconDB.readCustomBytes:331 → decodeFile/compress，再交下游解码 | 四个纯元数据消费者的重复工作已由A17消除并量化；真正图片/备份消费者仍需规范化/损坏回退。不能直接返回任意文件字节，本体未改。 |
| A12 / P3 / KNOWN_LEGACY / 保留 | tools/icon_library.py source-audit / LEGACY_IDS | 5199图源审计errors=0，有1个旧标识符INVALID_NAME告警（com.miui. delock.theme），代码明确列入LEGACY_IDS。保留sourceId/PNG/兼容引用，不自动重命名或删除。 |

A01：三个Owner的校验分配已经收敛到IconBackupCodec.isValidImage。先读尺寸，portable的48..1024规则在像素分配前执行；custom不新增尺寸拒绝，验证解码最大边采样到1024以内，原始归档字节不改；所有临时Bitmap在finally释放。184项故障/边界检查及56项真实Android图像/归档检查通过。它修的是验证峰值及回收，不是对全部自定义图像运行时解码路径的安全证明；RedirectIconDB等路径仍有完整解码。

A03：三套过期夹具已更新，journal144、restore worker122、Model188项检查通过。夹具范围保持受控，不把它们称为完整布局恢复。

原有F01–F15保留并重跑适用检查：恢复journal/跨进程重进、SQLite pending身份/事务、Sensor向量、快捷桌面捕获及设置监听等见回归报告。没有重做旧HOME遮盖/TextureView实验，没有修改二进制Manifest、版本、DB schema、主题参数、阴影材质、默认圆框来源规则或用户备份。

## 当前关闭边界

关闭的是A01/A03的本轮实现和适用隔离验证；A10以最终真实输入结果收口。A02保持SUSPECTED而非“修复完成”。A04原生库16KiB、A05系统合成、A06实体光影、A07全恢复和A08命名迁移没有关闭。未发现本轮足以确认的P0，不等于全项目没有Crash/ANR/数据丢失。

最终补充：A10已在API36真实输入验收上述四条有效路径，并验证1100ms拒绝与Chrome提交结果；A09当前版本字段已同步最终badging。A01/A03/A10是本轮实际修复，A09是文档校准。其余保持各自证据状态，不把12项混称12个已修BUG。

## 最终十问

| 问题 | 基于本轮证据的回答 |
|---|---|
| 1. 架构合理吗？ | 当前Model/Profile/Removal、图标四层、SearchSnapshot、ColdReload Owner总体合理。真实缺陷是局部验证资源与手势门槛，不支持整体重写SMEngine。Host职责集中和Java/Smali合同容易漂移是维护风险。 |
| 2. 功能逻辑完整吗？ | 不能证明全功能完整。已修图片验证和可达搜索入口缺陷；整库恢复、真实分身、手持光影、所有中断路径仍有明确未验范围。 |
| 3. 有哪些冗余？ | 校验解码已收敛；RedirectIconDB的decode→PNG编码仍是额外工作，但保留其规范化语义。没有证明旧兼容hook不可达，未安全删除它们。 |
| 4. 各场景瓶颈在哪里？ | 历史启动证据指向数据准备/图标栅格与场景绑定；HOME有系统层显隐边界；当前没有动画/文件夹/全库搜索的有效Trace占比。性能报告列明代码位置及本轮未量化部分。 |
| 5. 泄漏/线程/耗电呢？ | 确认校验临时Bitmap未释放，现修正；不能将它叫作已证永久堆泄漏。Sensor/投影/队列隔离检查通过，没有长稳纹理计数或功耗数据，不能宣布无GL泄漏或低耗电。 |
| 6. Android兼容性？ | 本轮实际API36/4KiB；其他版本/ROM未冒充通过。x86_64 ELF 16KiB未关闭；原生手势Recents/WM/SF控制权超出普通APK。ROOT模块独立且未刷入。 |
| 7. 哪些历史修复易回归？ | 默认圆框的主动选择vs有效来源、事务提交监听、UNKNOWN保留、分身身份、sc[0]几何、主题透明ID、光影八层/epoch、QD捕获generation、解锁会话、冷重载token均需保护；本轮测试覆盖其中适用部分。 |
| 8. 哪些值得最小修改？ | 图片验证和已复现手势门值得修；过期夹具必须修才能回归。不可达索引API候选已撤回；无测量依据的缓存/线程/SMEngine重构不实施。 |
| 9. 实际收益与数据？ | 搜索原失败路径恢复，184资源检查/56Android图像检查、27组离线和适用设备隔离通过；三个静态ROI零像素差。PAGE_READY中位2119→2426ms只是有缓存/历史差异的现场数据，未证明启动提速或不退化。 |
| 10. 距质量目标差什么？ | 真实SAF全恢复/断电、大数据布局、OEM分身、物理Sensor/锁屏、四指主题、多刷新率/尺寸、SF可见和长稳功耗仍未关闭。当前是可审查最小修复交付，不是全项目无缺陷认证。 |

## 实际修改范围

生产源码仅五个：`backup/BackupValidator.java`、`backup/IconBackupCodec.java`、`backup/RestoreIconSourceReconciler.java`、`gesture/VerticalGestureDirectionConfig.java`（均位于launcher/tools/java/com/smartisanos/launcher/），以及`launcher/smali/com/smartisanos/launcher/a/a/a.smali`。

测试：既有restore_journal/run_tests.py、stability/test_uninstall_model.py、backup_wallpaper/WallpaperBackupProbe.java；新增backup_images/run_tests.py、search_gesture/run_tests.py、search_index_state/run_tests.py。最后一项保留公开API调查能力，默认只检查正常状态；可选已知负例不列为PASS。

文档：本次五份报告、INDEX、DEVELOPMENT_LOG、BUILD_GUIDE/APK_STRUCTURE当前版本字段。MEMORY.md未更新。标准构建产生四个APK/idsig中间与最终产物变更，不是手工改二进制。原始APK、clean参考、图源、用户备份和独立模块未改。

交付证据：build/full-project-audit-20261015/delivery-verification.json；53项原暂存blob未变，最终安装hash与产物一致，载荷仅classes.dex/classes2.dex变化。源码回看与风险详见同目录其他报告。
