# 代码简化与维护审计

## 2026-10-17 A25 保留下载/缓存Owner，补齐有效性门

只修改现有IconPreviewRepository：沿用原CRC/尺寸/字节上限和写盘Owner，补充首个唯一13字节IHDR、实际IDAT数据及IEND边界检查；同Owner的hasValidPngData使用标准Inflater流式验证共享IDAT压缩流，8KiB缓冲、解压输出上限9MiB（涵盖现有1024边长RGBA16与Adam7），finally释放Inflater，不分配像素、不另建PNG像素解码器/缓存/线程。超限只终止当前镜像响应并进入既有备用链；取消仍立即返回且不尝试备用下载。像素文件不重编码，镜像顺序、超时数值、online_icon_cache_v4及负缓存一小时策略不改，原A24修复保留。

现有backup校验面向完整Bitmap，与IO不分配像素的职责不同；native decoder还可能恢复部分坏图，不能把它非空当完整性门。新包内私有辅助方法只调用标准Inflater，不新建Manager、Service、图像缓存或像素解码器。写盘临时文件/rename及负缓存Owner不改；原A24优先级/锁序和用户暂存保留。测试用可控HTTP验证提取的真实fetch方法，补齐旧测试替身漏测的部分。

## 2026-10-17 A24 保留既有队列Owner的可见订阅保护

仅修改现有IconPreviewRepository：PendingCallback携带本次订阅Priority，保留旧双参构造；会话裁剪跳过有有效P0回调的共享批次。会话选择/移除/完成detach和全局检查/淘汰或拒绝/detach在同一pending临界区内完成，避免可见订阅在中间加入旧批次。全局继续renderAdmission→pending顺序，没有解码、网络、等待栅栏或同步UI回调进入锁内，没有增加Manager/队列/线程；既有512全局上限及8槽metadata预留不变，96原本就是低优先级裁剪触发阈值，不把它称为全P0硬上限。P0超出全局容量仍明确回调null，不宣称无限负载全成功。原有7行schedulePersistence保留，未覆盖用户暂存。

生产仅IconPreviewRepository.java；测试沿用tools/tests/icon_preview/run_tests.py，新增可选Android隔离模式，未复制生产队列/Owner到正式APK。旧构造及现有接口保留，不提升或改写整个优先级调度，不改资源/合成器。负例、161项三平台与最终五轮滚动证据见本日功能报告。

## 2026-10-17 GPU后端对照负结论

同诊断包在硬件/软件后端均34个不同纹理miss、4个不同Shader构建；分配调用耗时受后端显著影响，不能据此新增纹理Owner/缓存或删除原复用门。本批无生产代码变更、无构建；原53项暂存保持。停止同路径循环采样，转既有图标预览Owner的压力边界，preview既有61项已通过。

## 2026-10-17 纹理和Shader缓存核对

Ea已按名复用纹理，ta已按名复用Shader，sa.create有mProgram>0返回门，Da.bind有现存纹理ID复用门。raw原版参考的sa.create/Da.bind与本轮修前归一化一致；clean_launcher该部分缺失，改查clean_launcher_raw；原APK仍缺失。maintained有同类缓存和程序门，仅参考。当前证据是首次真实创建/后端调用占用，没有成立的安全删除候选，不新增Owner/缓存/线程，不提前派发完成、不隐藏加载。glGenTextures耗时可能包含后端同步/排队，尚不能定位驱动内根因或外推真机。

34个不同材质miss及4个不同Shader在五轮均只创建一次，21张APK贴图像素哈希无重复；本批无正式简化修改。临时计数源码/产物已逐字恢复，证据build/bind-render-profile-20261017。

## 2026-10-17 补写链路负结论

定点计数确认20项已命中MD5而未重建，只有日历按现有动态/普通交接保护强制重建；三套PNG为不同缓存列，不是所有21项各重建三套。没有证据支持删除内容校验、改变MD5协议或去掉交接保护。本批不修改正式实现，不新增Owner/缓存/线程；临时Aa/e.s计数及APK已恢复原字节。正式b09ead0c…及53项暂存保持，具体计数/五样本/功能边界见本日性能报告和开发日志。

2026-10-17无缓存首建：prepareUncachedStaticSource保留public API、内部重载复用同一门限/条目合并/调度，新增同步入口只在有正式来源时共用StaticSource与上批独占图finally合成边界。合成退出补写锁后执行；fallback继续原分支。scheduleSourceWrites/persistSource及原完整合成体逐字未改，没有复制Owner/新线程/图片队列或全局generation。类型/身份2→1，非圆框正式Drawable请求2→1；原有缓存入口也回归246项。范围及API36实际负载见开发日志/性能报告，不以显式回收宣称整体内存下降。

2026-10-17同步复用：不把准备Bitmap扩展成长期来源缓存，而是在IconRasterDiagnostics内将现有StaticSource局部传给原准备和唯一合成器；新增同步入口与合成内部参数重载，原API保留。Smali仅在原图成功解码/普通静态纹理缺失时尝试，缺源/坏图/补写原路径不变。准备副本finally释放，API借用输入不回收，Smali成功后释放本次新解码输入。未新增Owner、线程或全局generation。原合成体逐行比对一致（承接上批装饰日志参数修复），246项Android9/16隔离、API36五样本及像素/功能回归见开发日志；无缓存首建/补写仍是下一项。

2026-10-17准备/合成补充：decorateProfileIcon接收已有resolved.type供日志使用，四行改动省一次完整类型解析，不新建缓存或Owner；80组对照及Android9/16隔离、API36五样本/功能回归见开发日志。独立准备副本参与当前分类，缺图分支又可能返回借用输入，禁止以统一recycle或跨阶段裸Bitmap缓存替代所有权分析；Aa.g返回新解码Bitmap，与直接借用区分。

2026-10-17：在既有ManagedIconSource内携带仅供一次纹理键消费的Drawable/type/identity，resolveManagedIconSource与identity仅增加接收已读redirect的内部重载，旧入口保留。避免新增来源Owner、常驻Bitmap缓存或全局临时状态；未命中时metadata为null，保留原检查以覆盖回退期间来源变可用。480组/1093项真实Android隔离、API36两组五样本/两页零像素差及五轮功能回归见性能/功能报告。不把准备与合成阶段也混入本批复用。

日期：2026-10-15；施工与证据见问题清单、build/full-project-audit-20261015。

## 实际简化

- 2026-10-16：Host来源标识复用刚解析的effectiveType，Raster resolver/纹理key两处不再立即重复同一来源解析。新增包内重载保留原单参入口，不引入缓存、Manager、线程或新的来源规则；完整方法修前负对照720组/3690项确认输出一致、paired解析2→1。实际两次真机trace不再出现identity→type子路径，五样本及像素/功能边界见性能报告和开发日志。

- 2026-10-16：真机采样证明受管静态图标在GL内重复走旧PNG缓存生成后再正式合成。只移除prepareUncachedStaticSource的DEFAULT限定，复用既有正式来源和有界延后补写；不新建Owner、不跳过兼容缓存/MD5/SQL，也不宣称总CPU工作减少。原默认图标、来源不可用、已有字节、ActiveIcon/设置与512上限继续原路；测试补充在原deferred_icon_source夹具内。

- 2026-10-16 A19：在现有IconRasterDiagnostics resolver内复用已经用于绘制的有效DEFAULT圆框Bitmap，省掉合成阶段随即被弃用的Drawable加载。没有新增缓存/Manager；其他来源、缺失回退及原阴影不变。计时沿用既有前两普通页诊断Owner，详情与性能收益边界见性能报告。

- 2026-10-16：IconManager.getLableForPackage及Host的displayNameForDesktopItem/isOriginalIconForced/hasManualIconOverride四个元数据消费者，改用现有getRedirectIconMetadata，去除不消费结果的图片解码/PNG压缩。两文件各1/3行替换；没有重写RedirectIconDB读图、迁移文件名、修改源缓存或新增Manager。42项真实Android隔离检查、5轮受控局部耗时及共享回归见性能报告。
- A01将BackupValidator和RestoreIconSourceReconciler的图片校验委托给现有IconBackupCodec中的一个包内方法。它只负责校验临时像素，不增加Manager、缓存、线程池或尺寸Owner；PNG头检查、各自文件字节上限、portable SHA/名称和归档事务继续由原Owner负责。
- 去掉Validator/Reconciler已不使用的Bitmap导入。没有删除任何原版资源、图标、历史分支或所谓无用hook。
- A10复用VerticalGestureDirectionConfig区分起点与终点，修正原Smali调用；没有新增手势系统。
- 三套测试夹具追上当前生产接口，不用放宽断言绕过失败。

## 有证据但未实施的候选

| 候选 | 依据 | 保留原因 |
|---|---|---|
| RedirectIconDB读取自定义图标再PNG编码 | readCustomBytes的完整decodeFile→compress | 四个不消费字节的调用方已消除该工作并测量；真正图片消费者仍需规范化/失败回退，readCustomBytes本体保留，不能直接返回任意文件字节 |
| Host承担设置、主题、图标和恢复UI，21431行 | source-inventory.json | 文件大不是功能BUG；直接拆Manager会放大Smali反射/静态会话/资源入口风险 |
| SearchIndexRepository延迟全量API状态缺口 | 可选--probe-deferred-api确定性负例 | 当前生产入口不可达该组合；候选已撤回，不能将API假设当用户可达故障 |
| 备份文件名32位hash | IconBackupCodec与RedirectIconDB相同命名合同 | 单改其中一处会造成旧档/已存图标找不到；需要独立迁移与旧名读取，不能本轮随意换SHA命名 |
| 多个线程/缓存 | preview decode/online/metadata/index、search、restore、sensor | 职责/优先级/生命周期不同，已有取消和上限；不能机械合成一个阻塞队列 |
| 热恢复/主题/GL回调复杂 | LauncherHomeCompat、ColdReload、ActiveIcon/context generation | 历史真实回归保护，未证明不可达，不删 |
| 壁纸失败同源请求保持去重 | ensureThemeSystemWallpaper requestKey + 测试49项 | 既有合同要求失败不在每次HOME自动重试；新选择/显式失效才重新请求，不当作需无限重试的BUG |

## 维护约束

每批必须写出代码Owner、数据/线程边界、负例、最小差异和未验收矩阵。下一步应补真实SAF恢复、物理光影/锁屏和原生手势时序证据；没有测量证据，不拆SMEngine、不换动画曲线、不压缩图像画质、不扩线程池。

不提交、不推送；全部原有53项暂存blob保留。任务前patch/逐文件快照仅用于本地审查和恢复本次差异，不能用整树restore覆盖其他工作。MEMORY.md未更新，DEVELOPMENT_LOG已记录本轮。
