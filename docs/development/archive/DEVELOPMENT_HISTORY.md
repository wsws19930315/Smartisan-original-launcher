> 历史证据归档，截止 2026-10-26 本次整理前。这里保留完整旧日志和旧专项计划，停止追加日常记录。历史“当前”“最终”“下一项”只表示当时状态，不能覆盖[当前开发日志](../DEVELOPMENT_LOG.md)及[当前专项计划](../LAUNCHER_FIX_AND_OPTIMIZATION_PLAN.md)。
>
> 日期、机型、原始样本、失败尝试、哈希及废弃标记均保留；不要把旧候选包当作当前交付包。

# 开发与修复记录

## 当前状态总览

更新日期：2026-10-26。当前版本 **1.6.0-T / versionCode 34（测试版）**；正式发布时才去掉 `-T`。

- 原生批量节点越界及主线程越权读取修复保留，内存分配已收敛到三类批量节点；Android9 三动画及五次启动有限回归完成，不能代替整体启动性能验收。
- 默认圆框已修复 Drawable 包装分支及大圆底留白差异；Android9 原生绘制通过，截图所涉两台故障手机仍未直接验收。
- 整体冷启动、Folder 可感知停顿、OPPO 手势闪回、目标 iQOO 百叶窗以及完整跨 ROM／长稳／16KiB 内核矩阵仍未全部关闭。Android9 本轮搜索上滑入口未通过，保留为待核对项。
- 当前剩余顺序和停止条件只维护在[专项计划](../LAUNCHER_FIX_AND_OPTIMIZATION_PLAN.md)。历史记录中的“下一项”是当时的安排，不覆盖当前计划；A22 按用户确认不重开。

## 本文档职责

这是修复根因、修改、验证、风险及证据的唯一流水入口。每个日期只保留一个 `### YYYY-MM-DD`，日期倒序；当天新增事项放在该日期下，使用四级标题，不在总览前插入正文。同一事项更新已有记录，跨日更新注明范围；已废弃方案不得恢复，未验证边界不得删成“通过”。

只在长期内容实际变化时更新其他文档：构建流程见 [BUILD_GUIDE](../../build/BUILD_GUIDE.md)，资产身份见 [APK_STRUCTURE](../../architecture/APK_STRUCTURE.md)，稳定合同见专项合同，README 只写面向用户的信息。不要把本日志同一条记录复制到这些文档；历史审计报告保持取证时的日期范围。`MEMORY.md` 不保存每日流水。

阅读顺序：当前状态 → 专项计划中的剩余事项 → 当天修复记录 → 必要的历史证据。冲突时以最新真实设备证据及后续日期的明确纠正为准。

## 日期入口

- **2026-10**：[26](#2026-10-26) · [25](#2026-10-25) · [24](#2026-10-24) · [23](#2026-10-23) · [22](#2026-10-22) · [21](#2026-10-21) · [20](#2026-10-20) · [19](#2026-10-19) · [18](#2026-10-18) · [17](#2026-10-17) · [16](#2026-10-16) · [15](#2026-10-15) · [14](#2026-10-14) · [13](#2026-10-13) · [11](#2026-10-11) · [09](#2026-10-09) · [08](#2026-10-08) · [07](#2026-10-07) · [05](#2026-10-05) · [04](#2026-10-04) · [03](#2026-10-03) · [02](#2026-10-02) · [01](#2026-10-01)
- **2026-09**：[30](#2026-09-30) · [28](#2026-09-28) · [27](#2026-09-27) · [24](#2026-09-24) · [16](#2026-09-16) · [15](#2026-09-15) · [14](#2026-09-14) · [13](#2026-09-13) · [12](#2026-09-12) · [09](#2026-09-09) · [08](#2026-09-08) · [07](#2026-09-07) · [06](#2026-09-06) · [05](#2026-09-05) · [04](#2026-09-04) · [03](#2026-09-03) · [02](#2026-09-02) · [01](#2026-09-01)
- **2026-08**：[31](#2026-08-31) · [30](#2026-08-30) · [29](#2026-08-29) · [25](#2026-08-25) · [24](#2026-08-24) · [23](#2026-08-23) · [21](#2026-08-21) · [20](#2026-08-20) · [15](#2026-08-15) · [12](#2026-08-12) · [11](#2026-08-11) · [10](#2026-08-10) · [09](#2026-08-09) · [08](#2026-08-08) · [03](#2026-08-03) · [02](#2026-08-02) · [01](#2026-08-01)
- **2026-07**：[31](#2026-07-31) · [30](#2026-07-30) · [29](#2026-07-29) · [28](#2026-07-28) · [27](#2026-07-27) · [24](#2026-07-24) · [23](#2026-07-23) · [21](#2026-07-21) · [19](#2026-07-19) · [18](#2026-07-18) · [17](#2026-07-17) · [16](#2026-07-16) · [15](#2026-07-15) · [13](#2026-07-13) · [12](#2026-07-12) · [11](#2026-07-11) · [10](#2026-07-10) · [03](#2026-07-03) · [02](#2026-07-02) · [01](#2026-07-01)
- **2026-06**：[30](#2026-06-30) · [29](#2026-06-29) · [28](#2026-06-28) · [26](#2026-06-26) · [25](#2026-06-25) · [24](#2026-06-24) · [22](#2026-06-22) · [21](#2026-06-21) · [20](#2026-06-20) · [19](#2026-06-19) · [17](#2026-06-17) · [16](#2026-06-16) · [07](#2026-06-07) · [06](#2026-06-06) · [04](#2026-06-04) · [03](#2026-06-03) · [02](#2026-06-02) · [01](#2026-06-01)

## 每日修复记录（倒序）

### 2026-10-26

#### 测试版命名与文档职责收敛

按用户要求，当前开发测试包使用 1.6.0-T，versionCode 保持 34；只有明确正式发布时才改为 1.6.0，不因本地构建成功自动去掉 -T。通过 set_launcher_version.py 同步文本 Manifest、设置页版本与二进制 Manifest；README 和构建指南标明测试版身份。

开发日志恢复固定结构：当前状态、文档职责、日期入口、倒序每日记录；每个日期只有一个三级标题，新旧记录按日归组，修复正文保留。移除重复的长篇每日摘要，旧日期标题保留锚点；QuickSearch 历史补录归入原记录日期。专项计划只维护当前剩余事项／验收条件，原计划整体归档到 DEVELOPMENT_HISTORY.md#历史专项计划，保留旧章节跳转。构建指南及 APK 结构中原生补丁的重复日期流水收敛为当前构建／资产说明，详细经过只见本日志。

日常根因、修改、验证、风险只在本日志记录一次。只有构建步骤、架构合同或当前任务状态真正变化时，才更新对应文档；不能要求每次修复同步抄写多份。历史审计报告保持其范围及证据日期，不作为滚动施工入口，不为减少文件数混合不同职责。文档校验确认 96 个日期唯一且倒序，96 条近期详细记录及 86 份旧日正文逐段保留，新链接目标存在；git diff --check 通过。MEMORY.md 未更新。

#### 关于我们：编译作者整行跳转 B 站

旧实现把监听绑定在右侧 about_author_link 文字，并将该文字设为可聚焦，导致左侧“编译作者”和中间留白均不能打开主页。复用现有 setting_follow_weixin 整行容器及 click 点击保护，仅把监听移至整行，移除子文字单独的 focusable；保留原背景、布局、文字、author_bilibili_url 及缺少处理应用时的提示。maintained 原设置同样使用该整行容器，未新建行或导航入口。修改仅 MaintainedLauncherSettingsHost.java 和 setting_follow_view.xml，标准构建、v1／v2／v3 签名和 P16 对齐通过；Android9 保留数据覆盖安装并拉回哈希一致。左侧标题 x160、中间空白 x510、右侧名字 x875（均 y1125）实点均跳至浏览器，Intent 目标均为 https://space.bilibili.com/284480387，左侧实屏已显示主页标题；逐次返回关于我们正常。最终 1.6.0-T／34 包 SHA256 4b7e244037a8fc47a33d91035a78c9460f0f1fe98d45e088155b7cc1556e06b3，设置页显示 1.6.0-T；本次安装后 crash buffer 无新增 Launcher 崩溃，旧 app_process 字体探针／屏幕共享代理历史错误不计入本轮。证据 build/docs-order-20261026；其他 ROM 及已安装 B 站客户端的处理分支未实际测试。

#### 默认圆框：统一 Bitmap／Adaptive 包装与圆底留白处理

同一应用版本及相同图标方案，系统返回的 Drawable 包装仍可能不同。旧 v9 只有 Bitmap 路径执行实心底板延展，Adaptive 前景路径跳过；原图已有大圆形底板但带透明留白时，再叠加白色圆底会留下外圈。DefaultIconCircleRenderer 复用既有行扫描，统一两条路径的底板判定；只对轮廓连续、面积及边缘颜色满足条件的大底板延展背景，替换前清空本次私有画布，避免双重抗锯齿边缘。主体位置、借入 Bitmap 和 Drawable bounds 不变；小图案、孔洞、复杂边缘保留原策略，匹配图标及用户自定义图不受此默认来源分支影响。版本标识升为 default-circle:v10-wrapper-and-circular-plate，使既有缓存键自然失效，不新增缓存或来源 Owner。

修改文件：DefaultIconCircleRenderer.java；DefaultCircleProbe.java、CircleVisualProbe.java 和 run_device_tests.py 仅用于原生绘制及对照。Android9 原生 Canvas 88 项、来源回退策略 334 项通过；旧 v9 同图跨包装负控及旧圆底白边负控均准确失败。合成素材的原生截图对照见 build/default-circle-wrapper-20261026/native-comparison.png，不是用户 NewBox 真机截图。正式流程构建及 Android9 保留数据安装已完成；用户故障手机／NewBox 原始 Drawable 尚未接入，因此不能宣称两台故障手机均已验收。APK 同时包含用户新增的赞助者文字，已保留，未回滚无关改动。

<a id="2026-10-26-原生批量节点按需扩容保留越界修复撤销普通节点额外分配"></a>

#### 原生批量节点按需扩容：保留越界修复，撤销普通节点额外分配

此节为上一日“全部节点0x2040”修复的后续内存收口，取代旧“下一项内存增量核对”。前一版修复了越界，但每个SceneNode都多分配6216字节。Android16同一隔离进程、相同5000节点、交替顺序各五样本确认，全扩容可用分配41280000字节；只有5%节点需要批量存储的固定场景改为11906000字节，39.37→11.35MiB，中位创建4.601→1.740ms。这是原生分配场景，不是实际桌面节点数量、总内存或整体冷启动提速。

最终仅PageWithRenderTarget（含子类）、BatchBackground和BatchShadow使用0x2040；普通节点恢复0x818。静态遍历确认这三类是现有矩阵／光照数组全部写入者。SceneNode构造中识别现有类，复用原库C++构造函数创建同一对象；释放仍由原finalize→nReleaseNative→原析构／operator delete持有，没有新增节点缓存、Manager、绘制器或另一套变换算法。原私有固定分配入口无法接收节点类型，因此增加很小的JNI分配桥；普通节点不再因81格存储付额外内存，批量节点新存储清零。进程位数只判定一次，32位及旧API不加载arm64桥，返回原分配入口。

原arm64库现在只保留4条数组地址迁移指令，分配及初始化入口逐字节恢复原版；SHA256为0bc34c572dab1c1374a410072d1ac738a37bf3e8a15e90c17984cf425c515b08。新增liblauncher_batch_compat.so为214640字节，SHA256 424193dc1f19018816f5c80410ea3a74b2279ef625a3ab66676ac347f2840cf8；现有NDK28构建、minAPI23、LOAD按0x4000对齐。新代码位于NativeBatchAllocation.java、launcher/tools/native/launcher_batch_compat.cpp、SceneNode.smali、tools/build_native_batch_compat.py；build.bat先检查精确底库再按既有SDK位置检测NDK编译桥，后续打包／签名入口不变。没有动32位库或版本号。

验证：Android16及Android9真实库162项边界、扩容存储清零、10000轮普通／批量对象混合构造与原析构、三类写入者覆盖通过；原库负控复现第17格起写出对象。API19／22／23／28／36受控加载边界共15项通过，旧API不访问Process.is64Bit，32位不加载新库。首轮Android9夹具把malloc_usable_size硬编码成2072而失败，修为同机原分配器对照后通过；产品没有按分配器规格放大或改行为。

最终v1.6.0/34 APK SHA256 4df00ecaff7d4da75d2848053e5fee05434fcae0226cb7f590d2b7f905f4c604，build.bat、v1/v2/v3及P16对齐通过。10/26连接换成vivo X21A/API28/arm64，原APK已保存before.apk；按既有授权保数据覆盖安装，系统安装确认按允许安装范围操作，Success后拉回包逐字节一致。最终包默认／百叶窗／立体翻转各四去四回实屏录屏，PID16408一致；用户单独允许临时切换后恢复原默认动画0，宫格仍为20、HOME仍为锤子，没有改布局／主题／壁纸／日志开关。随后五次重新启动均成功、对应新PID未见crash；am TotalTime为1218／1206／985／1240／1203ms，只计启动检查。截图可能含任务快照，系统日志关闭未采得PAGE_READY，不能据此宣称首帧或全冷启动达标。

文件夹打开及点击外部关闭、设置进入返回、横向翻页通过。搜索手势本轮上滑未打开，设置页显示开关开启；未修改搜索代码／设置，暂不记通过，需另查原包对照；不能用搜索页可直接启动替代手势入口。Android9首次UI树读取为空，相关检查改用实际截图，不把空树作控件不存在。

Android16手机在最后一次安装后断开，无法核对该机最后候选包和完整实屏，按未验保留；故障iQOO11、32位设备实装、12宫格切换、长稳、整机冷启动同条件收益和16KiB内核仍待验。证据build/blinds-video-20261025/selective-allocation。用户随后新增圆框跨机型、圆角矩形与白边反馈，当前优先审计该项；原优化清单其余边界不因本批而关闭。MEMORY.md未更新；用户在跨日间将既有文件暂存，本批保留其索引，没有自行add／提交／推送。

### 2026-10-25

<a id="2026-10-25-百叶窗文字异常与安装后闪退arm64-批量光照越界main-坐标读取"></a>

#### 百叶窗／文字异常与安装后闪退：arm64 批量光照越界、MAIN 坐标读取

本批按用户要求同时排查百叶窗黑条／缺图、偶发标题镜像，以及测试期间报告的闪退和默认桌面回退。没有限制桌面页数，没有改变12／20宫格、主题或布局，没有关闭百叶窗；当前只关闭这两处已确认的代码缺陷，故障iQOO11不在场，不能宣称所有用户机型已验收。

**证据与原因：** V2458A／Android16在21:19曾记录百叶窗旋转链的TempVars.release顺序异常；21:20和21:47记录ReferenceQueueDaemon在NativeThemeDestroy释放时检测到Scudo堆头损坏。后者是发现损坏的位置，不能据此直接改主题；隔离主题复制／回收测试未复现。系统21:47:23更新包，native崩溃发生于21:47:16，二者不能笼统算作“覆盖安装必然闪退”。用户确认后查询HOME角色已是vivo系统桌面，未发现本批测试前修改HOME的命令，回退的系统触发原因未单独证实。

1. QuickDesktopController.workspaceMode此前由MAIN触摸回调反射调用PageView.sr→Ib→Jb，读取SceneNode全局mTmpData并借用进程级TempVars；GL动画也使用同一数据。临时实测记录MAIN与GL两个调用者，未在诊断窗口抓到实际同时借用，故不伪称已捕获每次竞争。改为vc在Eb.update之后由GL发布弱引用页面身份＋标量资格快照，MAIN只读取快照；编辑、页面身份、停止／销毁失效逻辑保留。旧源码在新线程边界负控中失败，修后不再从MAIN进入几何读取。没有把整个原引擎改为ThreadLocal，也没有新增场景缓存。
2. 随包arm64 liblauncher_opt.so原生对象分配0x818字节，批量光照写入位置为0x758＋12×index，第17格（index16）恰好写到对象之外；实际二十宫格会传入20格。隔离调用原库，在额外保护区中复现index16写越界12字节、index19写0x83c；不是模拟Java数组或猜测分辨率。旧库更大模式的矩阵写入也可越出对象。此缺陷足以造成别的对象损坏，和稍后释放主题时才崩溃相符，但没有堆写入追踪证明每一条历史Scudo都唯一来自它。

**最终修改：** arm64库只修改6条既有指令，保持ELF长度109128、符号／ABI／绘制算法／动画资源不变：对象0x818→0x2040；矩阵数组迁移到0xc00，光照数组迁移到0x818，并同步现有初始化范围、写入和uniform读取。内存容量覆盖Constants现有最大81格；这是单次绘制的内部存储，不是桌面页数上限。新增tools/patch_native_batch_capacity.py按原SHA和每条指令校验，未知库拒绝修改，可幂等检查。没有修改armeabi-v7a库。扩充每个native节点增加6216字节，必须计入内存／冷启动后续性能边界，不能称本批提升性能。

曾尝试原版逐格绘制回退，但实屏出现黑页，未接受；Constants／ka／BatchBackground／BatchShadow相关实验全部按本批备份逐字节撤回。没有将黑页候选留在最终源码或APK。TempVars与StartupDiagnostics临时线程采样也已逐字节移除。

**最终验证：** build.bat成功，v1/v2/v3签名及P16对齐通过；v1.6.0／34。最终APK SHA256 d2bf6af8e583b10f304d5dcab9fce1375323bad7edb37a66fb881493d7f1886e，保数据覆盖安装Success，拉回base.apk逐字节一致；库SHA256 cced991322ab5aa885f47da5ff02b4f3a5870f3b61056296adb1fe9f54204342。与本批协调前正式包比较只允许classes.dex、classes2.dex及arm64库变化，其他聊天的About资源和接线保留。

- 原库越界负控通过；修后真实native 0..80矩阵／光照写入共162项通过，原场景字段及对象外保护区不变；新增数组零初始化和10000轮原生创建／释放通过。
- 原控制器UI读取负控失败；修后快照边界10022项、既有手势300项、截图世代33项通过，静态检查发布位于GL update后、截图检查前。
- 最终包V2458A上百叶窗／默认／立体翻转各四次去程与四次回程录屏，覆盖现有五页；所查动态帧和稳定帧图标、标题正常。恢复动画原值4=百叶窗。再做20组快速往返、12轮设置进入／返回，PID31649保持；最终进程崩溃缓冲未见新条目。只说明本次有限路线，不等于长期稳定或故障iQOO验收。
- 文件夹实际打开、点击外部关闭，首页上滑进入搜索及图标显示、首页右滑真实快捷桌面窗口与HOME关闭通过实屏核对。首轮BACK没有关闭文件夹、后续误在文件夹内尝试快捷桌面，已排除该轮“首页返回通过”的表述，并补做实际首页路线。
- 用户随后明确授权恢复默认桌面，执行set-home-activity后系统解析确认com.smartisanos.launcher/.Launcher；没有更换壁纸、主题、宫格或刷新率。原绿色刷新率覆盖层保留。

证据位于build/blinds-video-20261025：原视频帧、线程采样、真实native旧／新对照、构建日志、最终包哈希、final-louver／final-default／final-3d录屏及final-functional实屏。REA原生提供器在Windows不支持此ELF目标，实际反汇编／原库隔离执行使用现有NDK工具，未安装新提供器。原APK缺失／参考不完整的边界仍保留，clean_launcher和maintained只作只读对照。

**剩余：** 故障iQOO11／其他ROM、32位Android9、新12宫格实屏、长稳、内存与冷启动同条件五样本仍未验收。本批不宣称全项目或全部黑条／镜像反馈关闭；下一项为当前正式包的内存增量和长期翻页稳定性，再补故障机回传。MEMORY.md未更新，无git add／提交／推送，保留原暂存与其他聊天改动。

<a id="2026-10-25-关于我们编译作者文字链接到b站主页"></a>

#### 关于我们编译作者文字链接到B站主页

仅给“编译作者”右侧既有TextView增加about_author_link标识及键盘焦点，通过About原click／guardedSettingsClick绑定ACTION_VIEW＋CATEGORY_BROWSABLE，目标为用户指定的https://space.bilibili.com/284480387。保留文字、颜色、大小、布局、QQ群和支持开发者顺序，不增加整行误触热区，不使用B站私有scheme、WebView或SDK；由系统选择能够处理HTTPS链接的应用，没有对应应用或被系统拒绝时显示本地中英文错误提示。

修改MaintainedLauncherSettingsHost.java的About点击接线、setting_follow_view.xml的原TextView标识，以及values／values-en／values-zh-rCN下author_homepage.xml。URL位于默认非翻译字符串，提示按语言资源加载；不增加权限／组件，不改打赏页离线实现。build.bat及签名通过，Manifest逐字节不变，非签名条目仅设置资源包和classes2.dex变化。首轮覆盖安装返回User rejected permissions，用户明确允许重新安装后Success；首轮UI查询仍是旧安装包，不计新功能验证。重装后的UI审计未找到About入口，未执行有效点击／返回核验，不以源码绑定或构建通过冒充真机成功。

收到另一个聊天基于用户“允许协调暂停和恢复”的同工程／V2458A占用通知后，当前命令结束即暂缓新的构建、安装、ADB与设备状态操作，等待动画修复占用结束；不向其他聊天发送回复，不改其动画原值4、主题、壁纸或刷新率。保留可审查APK为build/author-link-20261025/launcher-author-link.apk，实际跳转与返回待后续资源恢复后另行授权测试。证据及状态见同目录validation.json；没有额外截图。MEMORY.md未更新，无add／提交／推送。

<a id="2026-10-25-关于我们官方网站条目改为qq群"></a>

#### 关于我们官方网站条目改为QQ群

按用户要求，仅修改maintained设置资源的values、values-en和values-zh-rCN/strings.xml：中文“QQ群”、英文“QQ Group”，号码1108127974。保留既有follow_website_title／content资源名及公开ID，不改布局、底部圆角、支持开发者位置、导航或Java代码。当前About宿主没有给该行绑定网站跳转，本次也不新增QQ拉起、网络或权限。沿用build.bat构建并保数据安装，以UI树核对文案，不额外截图；验证证据在build/qq-group-20261025。MEMORY.md未更新，无add／提交／推送。

<a id="2026-10-25-关于我们本地支持开发者页原设置导航白色选项卡与咖啡文案"></a>

#### 关于我们本地支持开发者页：原设置导航、白色选项卡与咖啡文案

先审计main分支／HEAD 5d138863及大量既有暂存、未暂存改动后实施，未覆盖、清理或提交用户改动。实际链为ThemeChooserActivity→MaintainedLauncherSettingsHost主设置→showAboutPage→setting_about_us中的setting_follow_view→setting_developer_support点击→DeveloperSupportPage.show。不是Gradle项目，沿用build.bat／apktool／Java8 helper；最终compileSdk36、minSdk23、target28，维持工作区已有v1.6.0／34，不升版。原主APK归档缺失，clean_launcher无对应About布局；核对了当前宿主及maintained参考About布局，没有声称新反编译原APK。

按用户最后指定顺序，在“官方网站”下面增加“支持开发者”行：网站改中间背景，新入口复用原底部圆角／箭头，原编译作者、微博、网站及赞助名单保留。About主布局逐字节恢复为任务前版本，新增行只在既有follow include中。独立页复用Title、ScrollView、SmartisanSettingsRowTitle、原蓝色勾选、setting_item_up／more_item_middle／setting_item_down_normal；标题栏固定返回About，前进／后退使用原宿主动画与滚动恢复。

用户指出初版重复标题、二维码过宽及白底不同：实屏采样原single子卡为#FAFAFA，选项与PNG白边为#FFFFFF。最终删去重复“支持Smartisan Original Launcher”，把两选项和二维码组成同一纯白圆角组，二维码下部直接复用原setting_item_down_normal，保留内边距及fitCenter。没有重画背景、改变全局主题或给二维码加滤镜。最新说明为“如果你喜欢这份熟悉的桌面体验，欢迎请开发者喝杯咖啡。你的支持，是继续打磨它的一份动力。”，中英文均来自资源；完全自愿／不影响功能说明保留。

用户提供两张真实JPEG：仅提取完整码区及静区、保留原头像与所有码模块，微信加8px、支付宝加48px纯白外边，转换到drawable-nodpi的donate_wechat.png（432²）与donate_alipay.png（944²）。工具侧离线ZXing核验原附件、PNG、实屏扫码内容摘要一致，不输出收款链接；AAPT产物路径为drawable-nodpi-v4，打包像素与源PNG完全一致。扫码核验工具仅在build证据目录，不引入APK第三方依赖；未执行转账。

页面仅持有两份按需加载Drawable，同一选项重复点击直接返回，反复切换复用；detach释放ImageView和本页引用，不recycle资源共享Bitmap，重新attach恢复原选项。没有静态Bitmap缓存、Service、Receiver、Provider、线程、轮询、SDK、权限、网络地址或外部应用启动。Host仅增加About入口接线和forward参数，图像解码复用IconBitmapDecoder。既有Manifest与任务前APK逐字节相同；非签名APK条目仅classes2.dex及内嵌设置资源包变化，原SMEngine／classes.dex／图标／主题／数据库不变。

实际源文件与原因：

| 文件 | 本次内容 |
| --- | --- |
| `.gitignore` | 仅放行两张新PNG，避免被已有全局PNG忽略规则漏收；未git add |
| `launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java` | About点击及返回方向接线，其他既有改动保留 |
| `launcher/tools/java/com/smartisanos/launcher/theme/DeveloperSupportPage.java` | 本地切换、错误提示、释放与返回，功能不继续堆入Host |
| `launcher/tools/maintained_settings_res/res/layout/setting_follow_view.xml` | 网站下入口、箭头和整组底部圆角 |
| `launcher/tools/maintained_settings_res/res/layout/setting_developer_support.xml` | 固定标题、可滚动内容、原勾选行及完整等比码图 |
| `launcher/tools/maintained_settings_res/res/values/developer_support.xml` | 默认英文文案 |
| `launcher/tools/maintained_settings_res/res/values-en/developer_support.xml` | 英文文案，与默认键集合一致 |
| `launcher/tools/maintained_settings_res/res/values-zh-rCN/developer_support.xml` | 简体中文与咖啡文案 |
| `launcher/tools/maintained_settings_res/res/drawable-nodpi/donate_wechat.png` | 用户微信码，本地无密度缩放资源 |
| `launcher/tools/maintained_settings_res/res/drawable-nodpi/donate_alipay.png` | 用户支付宝码，本地无密度缩放资源 |
| `tools/tests/developer_support/run_tests.py` | 提取真实选择／detach／attach方法，含重复加载、失败恢复、资源及布局合同 |
| 本开发日志 | 调用链、变更范围、结果及未验矩阵 |

构建build.bat成功，v1／v2／v3、P16对齐通过；最终咖啡文案包的哈希与差异见build/donation-20261025/apk-proof.json。新页面15项检查、既有默认桌面64项和设置会话33项／接线检查通过；测试覆盖两次解码后20轮切换不重复加载、单独资源异常不崩溃及重挂载恢复。初版reattach负控在真实方法夹具失败，修复后通过，不把该中间包记为最终验收。

V2458A／Android16／1260×2800保数据安装成功。真实About入口顺序／箭头／底部圆角、相同卡片宽度、默认微信、支付宝切换、20次切换输入、重复开关、系统BACK及标题BACK通过；两种实屏二维码离线解码与原附件一致。最后咖啡文案包再次安装后，以新鲜UI树确认文案已显示，按用户要求停止额外截图。关闭该USB手机Wi-Fi及移动数据，离线打开／切换／重新打开和侧滑返回About通过，全程PID17418一致，finally恢复两项原值1／1。前一轮离线测试因初始停留页面不符而无效，已恢复网络并补跑，不计为功能失败或通过。

回归边界：桌面正常显示、现有文件夹打开实屏通过；本次限定DeveloperSupport／AndroidRuntime日志未见错误，不扩大为全日志无异常。文件夹关闭后的横滑序列未确认翻页，主题实际切换、锁屏／解锁、长稳及启动耗时未验收，不能从classes.dex不变推导全部回归通过。Android10／KANT_360安装客户端长期未完成，已只停止本次精确命令对应客户端，没有卸载／清数据／改设置，不计该设备通过；其他Android版本、不同字体缩放和大屏仍待测。

最终证据build/donation-20261025，包括源图／资源／APK证明、各轮截图XML、coffee-final.xml、offline-results.json、tests与构建日志。原暂存patch对象da64c1fbabfbc12b678efe043375663637736f19保留，无add／提交／推送；构建APK及idsig为派生产物。MEMORY.md未更新。后续仅对实际发现的兼容问题做有界回归，不恢复已否决的多余标题／双层异色卡片。

<a id="2026-10-25-快捷桌面分段定位保留精确商表优化模糊中位665308ms"></a>

#### 快捷桌面分段定位：保留精确商表优化，模糊中位6.65→3.08ms

承接“继续下一项”，完成截图返回后worker排队、可见内容检查、缩放、模糊准备/横向/纵向/写回、MAIN排队/绑定及背景就绪回调分段。仅V2458A/API36（10AG6F1XUR00DD0）实测，KANT_360未操作。原主APK归档仍缺；clean_launcher的vc.b读回和maintained的GaussianBlurEffectMaterial/TwoPassFilterMaterial参考已核对，后者是GL材质，不直接替换当前Bitmap背景Owner或其既定算法。保留240px模糊宽度、半径14、两轮、锐利原尺寸/垂直翻转、图标/布局/主题/手势及窗口关闭合同。

**定位与否决候选：** 原实现worker排队中位0.460ms、MAIN排队0.080ms、绑定0.146ms，主要工作是模糊与onBackgroundReady内窗口链。先尝试将横纵滑动窗口的边界索引预计算，clamp调用1068194→47926，像素相同，但原生五对内核中位4.611→4.638ms，无稳定收益，完整撤回且未作为Launcher包安装。不能把操作计数减少本身当提速。

**保留的最小优化：** 原横/纵两个方向、两轮每个像素对四个通道重复整数除法。240×533时共2046720次，但每个通道和只落在0..(29×255)=7395。沿原QuickDesktopBackgroundCapture.blur在一次调用内生成7396项精确整数商表，四次方向调用共用；输出改为查同样的整数商。半径、轮数、窗口累加顺序、边界clamp、Alpha及每轮取整不变，没有改成近似倒数或不同滤镜。额外29584字节（约28.89KiB）int数组只活在本次blur调用，不跨截图保留，不引入Manager、线程、Bitmap缓存或此前否决的DirectByteBuffer池。生产仅此Owner私有blur及两个方向方法变化；原取消世代门禁保留，vc.smali逐字节不变。

**像素与工作量测试：** 新QuickDesktopBlurProbe及冻结的旧内核QuickDesktopBlurReference.java.txt，通过原runner的--blur运行真实Capture私有方法/Android Bitmap；覆盖1×1、单行/列、小图和240×533、半径0/1/14/31、0/1/2轮、随机Alpha与透明/黑/白/半透明边界，共76个像素场景逐像素相同，外加1项重复除法预算，共77检查。预算检查的两个工作量计数类只在测试复制的内核中将整除调用换成计数边界；未计数的旧内核才参与时间对照，不将计数开销算优化。旧源码负控在像素检查后准确失败于repeated channel division was not reduced，不能说旧算法像素错误。原生五对静态输入也呈现约4.8–5.8→2.0–2.5ms局部收益；实际Launcher分段单列如下。

**真实五样本（相同临时诊断口径）：** 每组保数据重启、等待5秒，同一主题/1260×2800/450ms滑动，连续五次正常开关；不再运行上一批meminfo高频采样。诊断仅单调时钟和14个long的分段记录，在背景绑定/就绪回调后写专属JSON，均先安装Success并拉回核对再测试。首次候选采样与本代理app_process测试重叠，已标candidate/INVALID-PERFORMANCE.txt，不计A/B；重采candidate-valid期间无其他设备原生测试。

| 中位耗时 | 原实现 | 保留候选 |
|---|---:|---:|
| 缩放 | 1.203ms | 1.395ms |
| 模糊准备（含商表构建） | 0.210ms | 0.368ms |
| 横向两轮合计 | 3.218ms | 1.269ms |
| 纵向两轮合计 | 3.180ms | 1.465ms |
| 模糊整体（准备＋两方向＋写回，各样本先求和再取中位） | 6.645ms | 3.079ms |
| MAIN排队 / 绑定 | 0.080 / 0.146ms | 0.062 / 0.131ms |
| onBackgroundReady窗口链 | 11.354ms | 11.703ms |
| 截图返回→背景就绪回调 | 18.735ms | 16.441ms |

就绪回调不是SurfaceFlinger实际可见时刻；这不是整体冷启动、稳定120FPS或首装验收。组内第一次模糊19.778→18.780ms仍有尖峰，第一次总链31.320→35.855ms反而更长，不能宣称首次打开卡顿已经解决。后四次模糊成本稳定降低，保留本次局部优化；窗口链未改，下一项只拆其资格检查、Popup创建/showAtLocation及动画启动。若仅剩系统添窗等待且无可删除工作，就冻结该链，不反复将同样调用换标题采样。

**正式恢复与回归：** 临时诊断完整撤下，生产Capture与候选原源备份逐字节相同，最终DEX无QD_STAGES_DIAGNOSTIC_FAILED/qd-stages-benchmark.json/旧池化标记。build.bat、v1/v2/v3、P16通过，v1.6.0/34不变，SHA256=af03262473ffd2fb2129e9664c31ec1bea249bed4b91a63eb042823f77d7ad99；保数据覆盖安装Success、拉回同哈希，非META-INF仅classes2.dex变化。33项世代、300项手势、4项静态顺序合同通过。首次正式功能脚本起点为系统文件管理器，首页像素门禁中止，保留formal-start-invalid.png；默认HOME仍是Launcher，显式回到原桌面后有效完整路线一轮（快捷桌面开关/短拖反向/再开/HOME、底部上滑搜索settings、设置/HOME、Folder外点关闭、第二页往返）及额外四轮快捷桌面通过。PID989保持，截图人工核对，当前PID crash缓冲为空。保留用户白盘、快捷桌面ON及peak120/logno，未改设备状态，专属JSON/dex已清理。

修改生产Capture；扩展tools/tests/quickdesktop/run_capture_gate_probe.py，新增QuickDesktopBlurProbe.java、冻结旧内核夹具；更新本日志和专项计划。MEMORY.md未更新，无add/提交/推送；170项原暂存patch边界保留。证据build/quickdesktop-stages-20261025：baseline/candidate-valid、comparison.json、division-negative/quotient-positive/final-kernel、formal、apk-check及final-verification。Android9/其他ROM未实测，长稳/内存峰值、整体冷启动、Folder首开等仍未完成；本批只关闭“截图后分段与重复整除”这一项。

<a id="2026-10-25-快捷桌面单缓冲复用五样本收益不足候选撤回"></a>

#### 快捷桌面单缓冲复用五样本：收益不足，候选撤回

承接“继续下一项”，执行正常有效截图的DirectByteBuffer复用对照，不重开图标来源/PNG逐图审计。仅操作V2458A/API36（10AG6F1XUR00DD0），KANT_360未操作。保留用户布局、RESOURCE白盘、格子12宫格/透明OFF、快捷桌面ON及设备peak120/logno；未进工程模式、未改默认HOME或清数据。主原APK归档仍缺；沿上一批clean_launcher原vc.b读回及maintained无可直接替换的Owner参考，不声称重新解包原APK。

**候选及所有权检查：** 在既有QuickDesktopBackgroundCapture内尝试只复用一块GL线程DirectByteBuffer，按线程身份、真实宽高、RGBA字节数匹配，最多保留32MiB；Bitmap仍每次独立创建，copyPixelsFromBuffer之后worker/ImageView不引用缓冲。尺寸/Surface创建销毁、pause/detach、Launcher stop/destroy及内存回调释放；stop后不发布缓存，重新resume才恢复。分配在锁外，epoch防止分配期间失效或stop→resume后旧分配重新入池。复用Host原ComponentCallbacks注册点，不新增Manager/线程/Bitmap池；通用vc.b(III)保持原独立分配合同，新增私有可选缓冲入口仅快捷桌面使用。上述均为已撤回候选，不能当当前生产实现。

原生Probe最初错误地把native字节直接视作固定ARGB整数，像素断言失败；修正为比较Bitmap复制后、缓冲重写前后的实际像素，不改生产色序。修后22项通过，补分配边界受控阻塞后共30项通过：仍使用真实allocateDirect，仅在测试复制源码的分配调用边界加闸门，确定性覆盖释放/stop→resume发生在分配期间，不冒充未经修改整个类的黑盒测试。另33项世代、300项手势及4项静态顺序合同通过。这些不证明EGL像素输出或真实长期内存。

**五样本实机对照：** 同机、同1260×2800/主题/布局/450ms滑动，每组保数据重启单进程后等待5秒，连续五次正常开/左滑关；Popup和首页固定图标像素门禁均通过。系统关闭日志，shell方法采样尝试先被存储上下文拒绝，再明确返回“not debuggable, and not profileable by shell”；未改Manifest/日志设置绕过。随后旧实现与候选均临时加同口径计数/单调时钟，后台准备并MAIN绑定后写专属JSON；每次安装均先Success、拉回核对再运行。诊断不持有新增Bitmap，不作为正式包交付。

| 指标 | 原实现 | 单缓冲候选 |
|---|---:|---:|
| 五次DirectByteBuffer实际分配 | 5 | 1 |
| 分配调用累计耗时 | 0.303154ms | 0.072077ms |
| 每次完成后Owner保留缓冲 | 0 | 14112000字节（约13.46MiB） |
| 读回调用中位（含取得/分配缓冲） | 17.165769ms | 12.211000ms |
| 请求发布→背景绑定/就绪回调中位 | 49.111154ms | 46.211462ms |
| meminfo采样期间GC次数增量 | 37 | 37 |

**限制与决定：** 就绪回调不是SurfaceFlinger实际可见时刻，不能称用户首次揭露延迟改善；样本小且调度/读回波动明显。meminfo约每0.5秒采样本身会扰动运行，GC增量不当作常规使用结论。两组起始PSS不同，原组收尾还有一次ADB服务采样失败，严格峰值及十秒空闲A/B不验收：采样最大658258/680358KiB、关闭PSS中位581407/596295KiB仅留原始观察，不把差值精确归因于缓存，也不补造无缺口曲线。分配调用本身五次仅约0.30ms，未证明少四次分配的收益值得额外长期保留整屏缓冲。因此候选不采用、冻结；没有新证据不再重复这套单缓冲实验。S1b整体长期内存仍开放，但本候选已完成评估，不继续挂成“待实现”。

**恢复与最终验证：** 五个生产文件、原runner/世代Probe共七个文件按任务前备份逐字节恢复，新ReadbackBufferProbe从tools精确撤下，试验仅显式归档build/quickdesktop-buffer-20261025。正式重新build.bat成功，v1/v2/v3、P16校验通过；重建包非META-INF成员与原正式包全部一致（封装哈希不同，单列rebuilt-formal-equivalent.apk），最终build/launcher-signed.apk沿用原e94a73f04823769bcb20c293bb50dba263addf9979511a96585b39ba4cb733d6，v1.6.0/34，设备保数据恢复同包并拉回核对。最终一轮快捷桌面开/关/短拖反向/再开/HOME、底部上滑搜索settings/X返回、设置/HOME、Folder外点关闭及第二页往返通过；PID26525保持，汇总截图人工核对，crash缓冲为空。不是再做五次冷启动或全ROM验收。原取消世代检查保留，最终DEX不含缓冲池和本批诊断标记；专属JSON、安装XML及失败采样trace已清理。

仅更新本日志和专项计划，MEMORY.md未改；170项暂存patch仍99c15a2f09120a9eca33a64939614a19a702ac6a500d5592a39742e7687bb284，无add/提交/推送。证据：comparison.json、baseline/candidate/result.json、buffer-races、各诊断/正式构建日志、formal/review.jpg、final-verification.json。下一项拆分截图返回后的worker模糊计算与MAIN排队/绑定，不重复缓冲分配计时；整体冷启动、Folder首开和其他ROM现场仍未解决。

<a id="2026-10-25-快捷桌面取消请求在场景更新后跳过整屏读回"></a>

#### 快捷桌面取消请求在场景更新后跳过整屏读回

承接“继续下一项”，限定快捷桌面截图取消后的无效分配，不重复图标来源/逐图解码任务。当前V2458A/API36已连接并解锁；KANT_360只列举未操作。安装前正式包71d77a…拉回归档，原170项暂存patch仍为99c15a2f09120a9eca33a64939614a19a702ac6a500d5592a39742e7687bb284，无add/提交/推送。

**根因与最小修复：** Renderer在Eb.update前取走请求世代，必须保留这一顺序以处理根场景CANCEL；但MAIN若在update期间取消/替换请求，Renderer仍进入vc.b，分配整屏DirectByteBuffer与ARGB Bitmap、glReadPixels，再由onGlFrame丢弃。1260×2800时两份像素存储合计28224000字节，约26.9MiB，仅为这次调用的理论分配量，不是实测PSS降幅或全部峰值。复用现有QuickDesktopBackgroundCapture的REQUEST_LOCK/generation/pendingHost，新增无副作用isGlCaptureCurrent；Renderer在update后、vc.b前检查，已失效则跳过。不在锁内执行GPU读回，不添加缓存/Owner/线程，也不改变Host显示中Bitmap的回收。检查后才发生的取消仍可能完成读回，原onGlFrame/worker/MAIN世代保护继续负责丢弃；不能声称所有取消都不分配。

对照clean_launcher，原vc.b也是整屏读回；当前此前已移除原版多余byte[]初始化，本批不改该方法，修前后逐方法字节文本一致。主原APK归档仍缺，未声称新解包；maintained的smali参考未提供可直接替代该快捷桌面Owner的实现，未搬用其核心。锐利层尺寸、垂直翻转、240px模糊层及参数、手势/动画均保持。本次不引入DirectByteBuffer池，正常打开时的分配成本和S1b长期内存验收仍开放。

**验证：** 实际Capture/Controller在Android ART运行33项世代检查（含有效请求、取走标记后仍有效、0值、取消、替换、完成及旧结果/失败回调不抢新Owner）；既有手势门禁300项通过。Renderer/Root四项为静态顺序合同，旧Renderer准确失败于“update后、readback前必须检查”，不是原生性能负控。没有声称真机每次短拖都命中了update内部竞态。build.bat、v1/v2/v3签名、zipalign-P16通过，v1.6.0/code34不变，APK SHA256=e94a73f04823769bcb20c293bb50dba263addf9979511a96585b39ba4cb733d6，保数据安装Success并拉回同哈希；非META-INF仅classes.dex/classes2.dex变化。正式包五轮正常开/左滑关、短拖反向/再打开、HOME关闭、底部上滑搜索settings/X返回、设置/HOME、Folder外点关闭、第二页往返通过，Popup窗口与首页固定图标像素门禁通过，30张汇总截图人工复核。PID18449保持，crash缓冲为空；仅为短时功能回归，不冒充五次冷启动/性能A/B或长稳。peak120/logno保留，临时XML精确清理，用户布局、主题、图标选择及快捷桌面开关不变。

修改生产Capture与vc，扩展原世代Probe/runner；更新本日志和专项计划，MEMORY.md未更新。证据build/quickdesktop-preread-20261025（source-check、apk-check、generation-final、gate、formal/result.json、review.jpg）。下一项仍是正常有效截图的S1b缓冲生命周期：先证明单个DirectByteBuffer在尺寸/Surface重建、后台和内存压力时安全失效，再用同条件分配/GC/延迟与峰值对照决定是否保留。整体冷启动、Folder首开尖峰、其他ROM现场均未因此关闭。

<a id="2026-10-25-图标冷资源表入口修复纠正对白色表盘的误判"></a>

#### 图标冷资源表入口修复；纠正对白色表盘的误判

承接用户“继续下一项/继续”，本轮限定图标选图与主题往返一致性，不恢复已关闭的图标逐图读取任务，不改主题动画、用户选择、宫格/布局、光影或系统刷新率。主设备仍指定10AG6F1XUR00DD0 V2458A/API36；另出现192.168.50.151:5555 KANT_360，仅识别未安装/操作。暂存170项边界保持99c15a2f09120a9eca33a64939614a19a702ac6a500d5592a39742e7687bb284。

**重要纠正：** 单独经典黑→格子、毛玻璃→格子未复现白盘；毛玻璃→透明ON→OFF→格子可看到白盘。然而诊断读取实际持久选择为RESOURCE/IMPROVED:com.android.BBKClock，不是AUTO；icons/drawable/com.android.BBKClock.png正是512px白盘，而维护设置资源clock.png是黑盘。白盘与当前选择一致，不能仅凭切换前后外观就判为缓存残留，也不能把重启出黑盘当正确目标。当前诊断进程重启同样取得RESOURCE/白盘。此前“白盘异常”的结论撤销；历史黑盘出现时没有同刻持久选择/有效来源证据，不能反推用户当时选择、认定手工改过或宣称同一根因已完全修复。

**否决候选：** 对照clean_launcher的原ThemeHandler.bx，它直接从ItemInfo.Oe解码上传；尝试让普通非黑白Cell在此复用composeCurrentStaticApplicationIconTexture，保留原active/Dock分支。实际完整路线仍显示白盘，并未解决所假设问题；该候选完整撤回，生产Smali逐字节恢复。首个ART夹具在D8合并时因DEX039与min-api23不匹配失败，未算通过，试验runner只留build归档，未交付工具目录。不能把该源码推测作为最终根因。原APK主归档仍缺，本轮没有声称新解包；maintained只有参考，不移植其核心主题行为。

**临时诊断与失败边界：** 仅临时在Host、IconRasterDiagnostics和ThemeHandler记录BBKClock的PID/阶段/当前主题/全局类型/持久mode及取样像素，输出本批external files JSON；不持有新Bitmap、不改选择、无性能收益计时。初诊断只覆盖compose-current/bx，不能覆盖所有启动路径，补了来源snapshot和mode。一次安装未等Success就开启路线脚本，安装最终INSTALL_FAILED_ABORTED，diagnostic-snapshot目录标作无效新包验收，仅为旧包运行留证；重发安装，在现有vivo风险页确认后Success，diagnostic-snapshot-valid才采用。有效诊断显示512px RESOURCE白盘源，原DB缓存344px白盘；不是白盘误读成系统原图。所有临时源码按diag-before备份和SHA256逐字节恢复，最终无traceClockRefresh/CLOCK_REFRESH_TRACE/theme-bx-raw标记，专属JSON精确路径清理，用户其他文件不动。

**实际修复与原因：** Host.iconOverrideDrawable此前sSettingsResources==null时异步预热，却在当前调用立即改用context.getResources()，这属于Launcher APK资源表；手动/内置维护图标由设置资源表定义，冷/热状态可能返回不同Drawable或null而回退。loadIconForDesktopItem已经通过createSettingsContext使用正确表，本批让另一个入口直接调用同一个settingsResources(context) Owner，不再以不同资源表替代。没有新增缓存、线程/Manager或第二套加载器，不改selectedIconDrawable的优先级。原入口的null/排除项/资源不可用处理保留。首次真正需要图标时可能同步读取设置资源档，已有Owner缓存后复用；未做首装、磁盘冷缓存或首交互时延对照，不承诺提速、零等待或全ROM无影响。这个确定性表选择缺陷与白盘外观的误判分开记录，不声称已证明所有黑盘历史现象都由它引起。

**测试：** tools/tests/icon_metadata/run_override_resources_tests.py提取真实入口，Resources/Context/选择器为边界替身；修前准确失败cold explicit choice uses its defining resource table。修后33项覆盖冷/热同表、复用、空Context/空Activity/排除项、加载失败不偷用Launcher表及下次重试、未管理/Drawable不可用回退与并发共享Owner。此为JVM入口合同，不冒充Android像素测试。现有主题壁纸Owner49检查通过。真实白盘像素由正式APK单列验收。

**正式产物与设备：** build.bat、v1/v2/v3签名、zipalign-P16通过，v1.6.0/code34不变，最终SHA256=71d77a968b0a0e943ecfeb570110527bf318860ffd2a7009cfe807c62e361c60。保留数据install-r Success、installed-formal.apk拉回核对。五次保数据进程重启均新PID，1260×2800、格子12宫格原数据，白盘固定内部区域灰度均值约211.986，均匹配保存的白色RESOURCE；仅为选图一致性检查，不是五次启动耗时或首装冷缓存基准。正式毛玻璃→透明ON→OFF→格子返回实屏白盘，已恢复格子/透明OFF。绿色刷新率叠层由设备当前状态出现，本代理未设置/关闭，peak120、日志no、atrace0保留。

本批生产仅MaintainedLauncherSettingsHost入口改动，新加资源Owner测试及更新日志/专项计划；原A08存储修复、高刷等既有工作保留，MEMORY.md未改，无add/提交/推送。冷启动慢、Folder尖峰、长期内存/S1b、其他ROM及严格16KiB仍开放。证据build/theme-icon-refresh-160-20261025：baseline/baseline-full、被否决candidate、有效/无效诊断分开、resource-negative/positive、formal-cold、formal-full与最终构建/签名/安装证据。

最终基础回归补齐：正式包五轮Folder开/外点关闭、快捷桌面打开/左滑关闭及Popup门禁、底部上滑搜索settings的匹配图标/X关闭、桌面设置滚动/HOME、第二页往返通过，PID14721保持；formal-regression/review.jpg人工核对全部五组查询及主要页面，crash缓冲为空。非META-INF ZIP成员相对本批baseline仅classes2.dex变化。此前五次进程重启是选图检查，本五轮是同PID功能检查，两者不混作性能五样本。正式运行无再生成专属诊断JSON，设备临时XML/截图已精确清理；表盘最终保留用户保存的白盘，未为了还原任务前黑盘而重写其选择。资源入口注释在构建后仅修正文义，不影响字节码。暂存patch SHA256仍99c15a2f09120a9eca33a64939614a19a702ac6a500d5592a39742e7687bb284。

<a id="2026-10-25-真机集中批修复自定义图标身份碰撞补压力主题folder现场"></a>

#### 真机集中批：修复自定义图标身份碰撞，补压力/主题/Folder现场

用户新指令“真机连接了，全部帮我解决”，重新纳入Folder审查。仅检测到V2458A/API36，已解锁，安装前base.apk SHA256=bc68b1…，与上一正式包一致。既有暂存170项binary patch边界99c15a2f09120a9eca33a64939614a19a702ac6a500d5592a39742e7687bb284保留。本批不宣称其他机型现场已解决，也不将未完成项目标为全完成。

**A08根因与最小修复：** RedirectIconDB.customFile和IconBackupCodec导出/恢复以Integer.toHexString((pkg+";"+cmp).hashCode())作PNG名；真实Java字符串fixture.Aa;Main与fixture.BB;Main碰撞，写第二张时覆盖第一张。新Android shell app_process负控编译修前完整DB/Codec与实际Bitmap/JSON/文件工具，准确失败于colliding identities preserve first image，不是编译失败。沿原DB Owner增加唯一文件名函数v2_+SHA256(UTF8身份)+.png，DB新写入、Host图片选择预保存、备份导出与恢复共用。没有新增Manager/索引/位图缓存，也不改绘制或图标来源优先级。原版主APK仍缺；clean目录无当前移植Java文件Owner，maintained是SQLite型RedirectIconDB，不照搬为第二套存储。

读取先查新文件；不存在时依次读原redirect_icons/hash.png与更旧custom_icons/hash.png，旧目录读取不再rename/delete共享文件。reset只删当前身份的新文件，旧文件保留，防止重置一个身份误删另一个的旧图。不批量扫描/搬迁数据，旧备份customFile仍按归档实际文件名读取，恢复输出统一新名。不能修复旧算法已经覆盖、没有副本的原像素；旧残留不会自动清理，降级到旧APK不能保证读新文件。SHA256是实际降低文件名碰撞风险，不作数学上绝对无碰撞承诺。

**验证与工具边界：** tools/tests/icon_metadata/run_custom_storage_tests.py新增实际DB/Codec/FileUtils的Android原生隔离检查，Context/SharedPreferences为替身，像素、文件IO、JSON、rename真实；不读写用户Launcher私有目录。29检查覆盖两旧目录兼容、两碰撞身份分别写/读、reset不破坏另图/旧文件、导出成员分离、实际Codec恢复两图及旧hash名称归档恢复；导入UI共享命名接线静态1检查。修前负控与修后两次通过日志保留。backup_images184、undo85、theme_wallpaper49通过；后者不等于OEM像素验收。另尝试app_icon_candidates旧runner在提取已改可见性的ManagedIconSource时ValueError，属于先前夹具漂移，本批未修、未计通过。theme_wallpaper第一次漏必填android-jar参数exit2，补参数后49通过，失败日志保留。没有以旧“903全部通过”覆盖本次失败。

**真机压力：** 初版脚本错误用BACK关闭Folder，随后截图仍在Folder，立即停止，将全部初轮记为无效，不能据其推断快捷桌面内存。换成实屏确认有效的外部空白点击关闭，再加每轮首页固定图标像素门禁和PopupWindow存在门禁。修前bc68正式包20轮Folder开/外点关闭→快捷桌面右滑打开/左滑关闭→底部上滑搜索/X关闭→翻页往返，PID6033始终保持，84张图留证。周期0/5/10/15/20的PSS KiB=650835/787379/789204/841671/852297，Graphics=444770/509066/513730/514050/514054；15秒后PSS756081、Graphics482278。该基线之前已有UI操作，不是干净冷进程；循环峰值约832MiB、空闲回落约738MiB，不足以证明无泄漏或改善，更不把后续新进程较低内存当修复收益。新文件名改动不解决截图分配/GC，S1b和长稳仍开放。

**构建安装：** build.bat成功，v1/v2/v3签名与zipalign-P16通过，v1.6.0/code34不变；最终SHA256=c9fd1a158c41fdd1d3b583104ac287aac2516a1619b40bd55254c2f2a345f49a。相对任务前包非META-INF仅classes2.dex变。按既有安装授权在本次系统外部来源提示勾选风险知悉并继续安装，未更改安装安全设置，install-r Success并拉回installed-final.apk哈希一致。生产净修改三文件：RedirectIconDB、IconBackupCodec、MaintainedLauncherSettingsHost（仅导入文件名两行）；本批无Smali或Manifest改动。

**Folder现场：** 安装后PID21840同进程五次打开现有三应用Folder，正常atrace gfx/view/sched/freq/wm/am/input/dalvik，五次最大onDrawFrame=37.812/12.796/13.303/12.181/11.496ms。第一长帧内dequeueBuffer4.628ms，并有多次decodeFileDescriptor；不能将37.812全部归因缓冲或CPU。不是五次独立冷开、不是修前/后Folder优化对照，未改动画/原几何。其余某帧11.496ms中dequeue约10.130ms，再次说明等待与计算需区分；首开尖峰与整体顺滑仍未解决。

**主题实屏与恢复：** 正常UI依次选经典黑、毛玻璃、透明覆盖ON/OFF、原格子，黑主题顶栏白字，毛玻璃/现有壁纸透明顶栏黑字，基础显示可见；没有另选壁纸/改所存URI，没有改锁屏壁纸（ID30保持）。系统桌面壁纸ID45→48是主题Owner重新应用原格子资产，不宣称系统状态字节相同。当前格子/12宫格/透明OFF恢复，快捷桌面与天气日历开关保留原ON。主题往返后时钟表盘从原黑盘变白盘，格子单次进程重启后恢复黑盘，未修改图标选择或用清数据规避；这是新增未定位主题刷新现象，不把它说成“主题矩阵通过”。深浅自选壁纸、切换全帧黑带、高刷真实FPS与其他ROM仍未验。

**正式回归：** 原格子恢复后五轮实际Folder开/外点关闭、快捷桌面及Popup移除后首页、settings实际查询图标/关闭、桌面设置打开滚动/HOME、第二页往返均通过，PID24335保持；review.jpg人工核对全部查询及主要页面。回归后上述单次重启是主题残留的独立对照，不混进五轮同PID结果。crash缓冲为空不等于完整系统日志无错；persist.sys.log.ctrl仍no、peak120、省电0、atrace tags0，默认HOME/导航/分辨率密度/用户布局保留，没有备份恢复真机桌面、清数据、清后台或进入工程模式。

证据build/finish-real16-20261025：collision-before/negative/final、pressure-valid/result.json、folder-trace/result.json、主题截图/XML、formal-regression/result.json与review.jpg、签名/构建/installed-final.apk。当前冷启动、Folder尖峰、S1b/长稳、主题时钟刷新、其他机型与严格16KiB仍未完成；不会把代码审计当作解决。MEMORY.md未改；本日志及专项计划更新，无add/提交/推送。

<a id="2026-10-25-合并收口实际备份恢复撤销通过停止无收益读图实验"></a>

#### 合并收口：实际备份恢复/撤销通过，停止无收益读图实验

按用户“有些东西来回测很多遍，一次性解决”的要求，将专项计划顶部设为唯一执行入口，历史批次“下一项”不再作为待办。已验收实现冻结；仅新失败、相关代码变化或新增目标设备才重开对应验证。没有把冷启动、Folder、OPPO闪回或跨ROM矩阵写成完成，也没有用改动文件数推算完成百分比。

**PNG候选关闭：** 延续上一批八层PNG成本，只在独立shell app_process比较BitmapFactory.decodeFile与FileInputStream/decodeStream。使用生产IconProjectionBlur的8种sigma输出、520个独立文件；逐像素及尺寸/config/density/alpha/premultiplied一致。五组交替顺序：file CPU221.749/225.046/221.119/218.295/227.028ms，stream CPU227.649/227.793/223.982/223.992/233.059ms；wall亦无稳定收益。候选拒绝，没有修改生产调用/像素格式/Bitmap所有权，没有新增缓存。样本为生成的生产模糊输出，不是真机私有原图或整体启动对照，不宣称冷启动改善。精确专属探针目录已由脚本清理；此假设不再拆成后续微任务。

**真实恢复闭环：** 原临时模拟器因会话中断已消失，ADB无设备；重新启动Pixel_6_Pro/API36/x86_64 read-only、no-snapshot、host GPU独占实例。首次包服务尚未就绪安装失败，启动完成后重试Success，不将失败安装当作有效回归。安装现有正式v1.6.0/code34，未构建/改生产包。只在模拟器Documents/SmartisanBatchAudit通过系统picker选择并确认目录授权，正常UI导出6587字节、10成员归档，ZIP CRC通过；布局2页22应用、无文件夹/自定义图标。

为提供可辨认的恢复前后负例，只修改临时模拟器DB的相机/设置cellIndex互换，ID/应用数保持。首次force-stop后默认HOME立即重启，早于DB替换，mutated-home.png仍旧布局，该次不算有效前置；随后仅对任务独占模拟器停Framework、写入同一完整DB、恢复原UID10226:10226及660权限并重启Framework。mutated-home-valid.png确认设置在0、相机在1；不修改真机DB/布局。通过正常“从备份恢复”→SAF选归档→预览→开始恢复→确认，实屏恢复相机0/设置1。恢复后再走“撤销上次恢复”→确认，实屏回到设置0/相机1。对四份DB比较22项title/intent/itemType/pageIndex/cellIndex/folderIndex/packageName/componentName/user全量排序结果：原布局=恢复结果、交换布局=撤销结果。只比较应用身份与摆放，不冒充全部设置/图标像素/保留页ID字节等值或异常恢复验收。

恢复/撤销后实际第二页图标、底部上滑搜索Maps及结果图标、关闭搜索、桌面设置与HOME通过，截图人工确认；crash缓冲为空，不等于长稳无崩溃。所有SAF授权、测试目录、DB变动和查询仅存在read-only临时实例，退出不保存快照，原AVD及真机不保留本批变更。缺真机不再反复询问接入或把模拟器结果冒充OPPO/魅族验收。

**回归工具修复：** 导出636+错误UI8、撤销保护85、预览52先通过；restore_worker首次因现有Coordinator调用LauncherHomeCompat而夹具缺依赖，javac失败，旧“122通过”不能当本次结果。只在tools/tests/restore_worker/run_tests.py补HOME入口边界替身并注明范围，复用原Intent夹具；修后122项及Activity定时器静态合同通过，共903项。此套验证worker/MAIN交接，不验证真实HOME路由；真实恢复UI结果单独列证。未修改LauncherHomeCompat或Coordinator。

证据build/consolidated-finish-160-20261024：read-device.log、acceptance-result.json、before/mutated/restored/undone.db、导出归档、restore-preview/confirm与undo-page/confirm XML、mutated-home-valid/restored-home/undone-home及post-undo截图。APK仍bc68b1d9850275746678e482b4f3f1299bd6920e19854e66963daaf60d12db71；170项暂存patch仍99c15a2f09120a9eca33a64939614a19a702ac6a500d5592a39742e7687bb284，未add/提交/推送。本批修改限测试runner、本日志和专项计划；MEMORY.md未更新。整体冷启动仍未解决，Folder保持暂停，OPPO闪回/魅族60Hz/三星Share现场、严格16KiB、长稳/实体光影和完整主题矩阵等明确保留在计划顶部，不再用“继续下一项”隐藏这些边界。

### 2026-10-24

<a id="2026-10-24-投影预载逐图消费审计排除重复解码保留跨配置八层纹理"></a>

#### 投影预载逐图消费审计：排除重复解码，保留跨配置八层纹理

承接上一项317.554ms采样热点，在V2458A/API36同一12宫格/grid主题/120Hz/光影配置下，临时复用LauncherStartupDiagnostics记录Eb.oh预载查表/实际decodeFile及mymaterial/f.1材质查表/缺失解码。只保留路径、计数、尺寸、时间与成功标记，不持有Bitmap/Da对象，不改纹理键、上传、Tb/Sb或回收。两入口仍只调用一次原BitmapFactory.decodeFile；metadata定期写专属JSON是诊断开销，不计生产提速。未增加持久生产Manager/Service/缓存，未改主题、权限、日志或系统刷新率。

五进程启动逐图结果一致：每次520次预载查表、0命中、520个不同路径各解码一次、0失败；另外18个Dock路径在材质端首次解码，之后命中，未与预载重复。所有538张均256×256，同路径重复解码数始终0。预载解码CPU=285.933/283.741/287.619/287.574/285.013ms，中位285.933ms；这是插桩计时，不能与上批单次ART采样317.554ms相减当优化。520张累计解码像素分配136314880字节（130MiB），不等于同时驻留内存/PSS或GPU峰值。

启动快照有72个预载路径被材质使用；第5进程再向前8页、返回8页，16张图人工确认9个不同正常页，PID23240保持。结束共390个预载路径被消费，剩130个恰为65组的第6/8层；期间未新增材质解码、未发生同路径重复解码。这里的消费是实际材质查表，不当成GPU可见像素/物理呈现帧证明。后续不再把此链按“重复读取同一图片”反复排查。

源头解释：Cell.lm固定返回1～8，Eb按全部八图预载；实际材质路径取World/Ra.lm映射。对实际Ra.st直线Smali初始化作符号求值，四组原配置分别[1,1,2,2,3,4,5,7]、同前、[1,2,3,4,5,6,7,8]、同前。当前读取的六种物理层与前两组一致，但后两组明确需要6/8；Ra的配置应用将Na.jU写入现有UU，并由forceUpdateShadowMap刷新材质。不能把当前未消费130图判为全局死资源。直接删除或仅预载当前映射会把两层成本移到后续配置切换，本批不交付这种未经对照的时延转移。四组为真实Smali的静态求值，不冒充真机切换过全部天气。clean_launcher Cell.lm/Eb预载对照保留，干净World/Ra参考文件缺失；maintained World/MainView无同名八层文件预载可直接替换，原APK主归档仍缺，不声称新解包。

本轮审计关闭重复解码假设，尚无可安全删除的无效工作，生产净改动零，未声称冷启动提速或已解决。三份临时Java/Smali逐字节恢复，正式重建非META-INF ZIP成员与任务前包全部一致；最终v1.6.0/code34 SHA256=bc68b1d9850275746678e482b4f3f1299bd6920e19854e66963daaf60d12db71。构建/签名/P16通过，保数据安装Success并拉回installed-formal.apk哈希核对；正式基础回归一轮翻页→快捷桌面→搜索关闭→设置滚动→HOME通过，实屏拼图人工确认，PID24525保持。五次启动是逐图插桩样本，正式包不是修前/修后五组性能对照。安装诊断时仅在既有系统确认页勾选本次风险知悉并继续安装，没有修改安装安全设置；正式恢复安装直接Success。两份专属JSON按精确路径清除，正式dex/源码无审计标记，设备留在首页，开关/布局/默认HOME/1260×2800/560dpi/peak=120/省电0均保留。

证据build/projection-consumption-160-20261024：五份startup.json、summary.json、forward/back-consumption.json及paging-overview、preset-proof.json、diagnostic/formal-restore构建、installed-formal.apk、formal-regression及final-proof.json。原170项暂存patch仍99c15a2f09120a9eca33a64939614a19a702ac6a500d5592a39742e7687bb284；原高刷和前批修复保留，无add/提交/推送。只更新本日志及现有性能报告，MEMORY.md未更新。下一项限定PNG读取/像素格式本身的同画质成本对照，先证明与现有8层表示、失效及Da生命周期兼容，再决定最小优化；不新增无证明的裸Bitmap缓存、不恢复已否决延页/关光影。冷启动、其他ROM、首装冷缓存和长稳仍开放。

<a id="2026-10-24-冷启动剩余路径复采定位原版投影png预载热点未改生产逻辑"></a>

#### 冷启动剩余路径复采：定位原版投影PNG预载热点，未改生产逻辑

V2458A/API36、12宫格、grid主题、原图标/光影/默认HOME/120Hz与数据状态不改，使用上批正式v1.6.0/34 f0729e…经包限定MAIN/HOME入口取五次进程重启。OS/ART/磁盘缓存保留，不清后台或数据，不当作首装/断电冷缓存。PAGE_READY=1884/1830/1833/1794/1817ms，中位1830、最慢1884；最长构建帧wall=1645/1612/1612/1577/1599ms，CPU=1499/1520/1516/1473/1512ms。前两页计时结束至bind结束=1120/1109/1090/1077/1105ms；既有Page诊断只覆盖前两普通页，不能据此说其余页没有初始化。静态合成日志63～66条，源/异步缓存状态非完全相同，不强行当作逐调用等量性能实验。原先后续页延迟导致首滑长帧的否决继续有效，不恢复该方案。

为定位使用现有LauncherStartupDiagnostics临时加2000us ART自采样，单独诊断APK、不混入上述五正式样本。profile.log在此设备为空，STOPPED日志断言失败；随后实际文件存在，拉回检查trace完整、data-file-overflow=false，GL线程CPU计数有效。历史解析器将本机wall/header时间当微秒，出现wall远小于CPU的矛盾；全部sampledWallMs/windows us明确标为不可用，不修饰单位后当精确时延。profile-cpu-proof.json只用dual CPU计数：GL采样CPU1609.862ms，nativeDecodeFileDescriptor合计383.787ms，其中直接Eb.oh→decodeFile的投影预载317.554ms、其他文件解码66.233ms；单份含诊断开销的采样不是五组CPU收益或精确调用计数。

源码确认具体路径为Eb.oh里SHOW_ICON_SHADOW_LIST分支，遍历原Page/Cell，取Pe和lm的8层列表，按filesDir/shadow/<key>_<layer>.png先Ea.bb查表，缺失才decodeFile→Da→Tb(true)/Sb(true)上传，并以同完整路径Ea.a登记。clean_launcher同原预载，mymaterial/f.1也按原Ea键查找；未发现可直接认定的键错配重复读取。Da上传后回收其持有Bitmap，不能添加无所有权证明的裸图缓存。maintained仍为另一套已合成图标/纹理路径，无对应八层投影预载可直接替换；原主APK归档缺失，未声称重新反编译。此热点与上一批Android9的不同主题Asset解码、来源报告重查不是同一调用；旧机预载<1ms结论不能覆盖本机活跃投影路径。

本批没有已证实可无损删除的重复工作，生产净改动零，不关光影、不减少八层或提前隐藏Loading，也不将工作延后到首滑。临时Startup源码逐字节恢复；正式重建的全部非META-INF ZIP成员与任务前APK一致，容器SHA256为3d4dfb5596e5b471eb499a1c8ec99ce7bfb6e3e949f5b2e455665499e5e691c6，不能称APK逐字节相同。构建、签名、P16通过。首次正式恢复安装被手机拦截，代理在结果返回前启动的regression目录两轮明确作废；停止该脚本后使用同一既有安装授权重发，系统安装页完成后Success，拉回installed-formal.apk哈希一致才运行regression-final。五轮四页实际翻页/快捷桌面/搜索/设置滚动与返回截图及Window/Display通过，PID16845保持；拼图人工核对。未输入查询或改变历史，所有开关保留，临时trace设备文件按精确路径清理，未进入工程模式或改变日志策略。当前persist.sys.log.ctrl=no，不能声称完整系统日志无错；正式dex无TEMPORARY_PROFILE与专属文件名。

证据build/startup-remaining-160-20261024：baseline-summary.json、五份正式启动日志/截图、startup.trace、profile-cpu-proof.json、分析失效注记、diagnostic/formal-restore构建、install-retry、installed-formal.apk、regression-final及final-proof.json。170项原暂存patch哈希仍99c15a2f09120a9eca33a64939614a19a702ac6a500d5592a39742e7687bb284，原窗口高刷改动保留，不add/提交/推送。仅更新本日志和现有性能总报告，MEMORY.md未更新。冷启动仍开放；下一项限定核对每个投影层的预载与实际材质消费/重复读取次数及所有权，取得可删除重复工作的证据后才最小修复，不重做已否决的全量前移加join、无条件页面延后或裸Bitmap缓存。其他ROM/首装/长稳/真实16KiB未验。

<a id="2026-10-24-全窗口刷新率交接修复vivo设置页90120hz五轮对照"></a>

#### 全窗口刷新率交接修复：vivo设置页90→120Hz五轮对照

承接上一批下一项，使用当前V2458A/API36，不启动虚拟机、不调整系统刷新率/省电/日志/默认HOME。安装前为v1.6.0/34正式8a2f90…，保留原包到build/refresh-window-160-20261024/before.apk。修前五轮桌面翻页→快捷桌面→快捷搜索→关闭→Dock设置滚动→HOME，每轮截图与窗口/Display实测：桌面、快捷桌面、搜索均120.00001Hz，设置每轮90Hz；peak_refresh_rate=120.0，low_power=0。设置真实窗口没有preferredRefreshRate，既有GL Surface请求不覆盖独立UI窗口。clean_launcher与maintained的现有原版按需渲染/elapsed时钟没有对应公共窗口请求可直接搬运；原APK主归档仍缺失，不声称新解包。

生产仅LauncherSettingBridge.java与MaintainedLauncherSettingsHost.java：抽出已有同物理分辨率最高支持率选择给Surface/Window共用；在原Activity resume/focus共享窗口策略入口补preferredRefreshRate，覆盖搜索与设置，不创建ActivityLifecycleCallbacks/Manager/Observer。未attached无Display不申请，取得焦点时沿现有入口再用；相同请求不重复setAttributes，已有非零preferredDisplayModeId由原Owner继续负责。主GL的API30/31门控与无缝Surface请求保留，Window所用公共API兼容项目API23基线。不写全局设置、不硬编码120、不改分辨率/动画/按需渲染/状态栏逻辑；隐藏或销毁窗口由系统停止其可见窗口投票。本方法只有窗口能力请求，不保证厂商策略采用。

build.bat成功；最终badging仍v1.6.0/code34，v1/v2/v3与P16 zipalign通过；保数据覆盖安装Success，拉回APK哈希一致f0729e654d63e05a2cdcd020c6ed3fa274074276bb0840c4d55c37600a23ca37。相对before.apk，非META-INF仅classes2.dex变化。扩展既有run_surface_tests.py，生产方法提取JVM夹具22检查通过，涵盖API23窗口/29/30/31 Surface、60/90/120能力、同分辨率、无效数值、未附着、幂等和既有模式Owner；原Folder timing64、settings session33及接线检查通过。此处不是Android9实机ART验收，当前Android9未连接。

修后同一真机五轮四页面共20路由样本全部完成，四类页面每轮系统renderRate均120.00001Hz，搜索/设置实际可见窗口preferredRefreshRate=120.00001；PID7236全程保持。前后拼图人工核对实际页面、图标、搜索及设置滚动返回；首轮设置起始滚动位置不同，故不用于动画耗时性能对比。Settings gfxinfo滚动窗口119条Flags=0样本，FrameInterval中位修前11.097436ms、修后8.322414ms；这是UI调度间隔，不是五组独立实际呈现帧率。搜索不输入查询、不改历史，主题/布局/权限/快捷桌面原ON均未改。外部系统设置覆盖→HOME和Folder打开后最终返回桌面也核对；Folder短延时BACK截图仍在过渡，未作为关闭时延验收，后续点击误进入浏览器后用HOME退出，最终实屏为原桌面，未更改布局。

采样边界：首份Perfetto因设备采集延迟，仅有动作结束后系统尾段切片，没有目标路由的Launcher帧，不作为本批APP FrameTimeline证据；历史TimeStats也未清空，不能用其累计平均FPS证明本批改善。设备gfxinfo DisplayPresentTime为无效占位，未取得可靠逐buffer呈现证据，不写稳定满120fps。Android官方说明setFrameRate为请求且系统不保证满足：https://developer.android.com/media/optimize/performance/frame-rate 。全窗口120Hz能力在当前vivo获得验证，魅族/Flyme、其他ROM、API23/Android9真实窗口、省电/温控限制、可见期间系统动态改档和长稳仍未验收。没有将旧MEMORY中的已移除LauncherRefreshRateCompat重新引入。

证据build/refresh-window-160-20261024：comparison.json、before/after四页五轮图与Window/Display、gfx-baseline.txt和after/*-gfx.txt、拼图、安装前后APK、build.log、policy夹具、proof.json。系统peak/low_power、分辨率1260×2800/560dpi与默认HOME核对保持，测试perfetto配置/trace已从设备按精确路径移除，不操作全局TimeStats或用户文件。170项原暂存binary patch仍99c15a2f09120a9eca33a64939614a19a702ac6a500d5592a39742e7687bb284，未add/提交/推送。MEMORY.md未更新，本日志和启动专项当前边界更新。下一项回到未关闭的整体冷启动剩余耗时定位；魅族60Hz须目标机对照，OPPO闪回及正式包恢复仍待对应设备，不重复本批已完成五轮。

<a id="2026-10-24-v160与快捷桌面截图失败清理android16真机五轮覆盖返回通过"></a>

#### v1.6.0与快捷桌面截图失败清理：Android16真机五轮覆盖返回通过

版本通过tools/set_launcher_version.py同步文本Manifest、最终二进制Manifest和设置资源为v1.6.0/code34；README、BUILD_GUIDE和APK_STRUCTURE同步。build.bat成功，最终badging、v1/v2/v3签名及P16 zipalign通过。build/launcher-signed.apk SHA256=8a2f90a86b156a42a692ec3bc14ae3f6197201cefc291cda9ef15d4bc6f25352；相对上一正式包非META-INF仅Manifest、设置资源资产和classes2.dex变化。未发布。

根因：QuickDesktopBackgroundCapture的当前截图为null或无可见内容时只回收/记录，没有通知Controller撤销openAfterBackgroundReady及微小进度宿主状态。下一次DOWN虽能自愈，本次手势仍停在等待完成状态。生产只改Capture及Controller两文件：在主线程通知当前Host失败、复核generation与当前capture Owner后，复用closeImmediately→onHostClosed→cleanup；保留Root原GL CANCEL终止保护，迟到失败不能关闭新手势。不新增定时器、重试、Manager或Bitmap缓存，不改变原触摸方向和动画。对照延续前两节clean_launcher与原Magic Flow缓存；原APK归档缺主包，未声称新解包，maintained无对应Popup Owner可替换。

扩展既有QuickDesktopCaptureGateProbe至300检查、CaptureGenerationProbe至26检查及runner的旧源码负控入口：覆盖stop/HOME/外部覆盖/搜索ready/resume-before-stop、detach、null/blank失败、迟到回调与下一DOWN恢复。Android9真机及Android16模拟器ART分别300+26通过，Root顺序3项通过。旧生产Capture实际运行准确失败于failed capture retained deferred opening，非编译失败。夹具通过不等于生产APK强制失败注入；未在正式包增加测试入口。

Android16模拟器实际APK：外部系统设置覆盖返回五个有效样本、熄屏唤醒返回五样本，Popup在离开时移除，返回可翻页，PID4390保持。原covered-4返回截图在系统转场中，剔除其视觉验收，补covered6等待转场完成并人工核对；开关从原OFF临时ON后恢复OFF。read-only/no-snapshot实例结束不保存快照。无PIN模拟器熄屏不等于物理加密锁屏验收。

用户指定改用当前vivo：V2458A/API36，1260×2800/560dpi，默认HOME仍本包。手机已有包拉回哈希即最终8a2f…，无需重装；快捷桌面原本ON，全程保留ON。五轮真实右滑打开→系统设置覆盖→HOME→首页翻页，逐轮WindowManager与截图人工核对通过，PID559不变。快捷桌面搜索入口实际进入，常用图标可见，Popup已移除，关闭搜索返回及Dock桌面设置打开/滚动/版本v1.6.0实屏通过；未输入查询或改变历史。原主题、动态天气日历、布局、默认HOME、分辨率、密度、导航和日志策略未改。一次shell TouchInput退出137，不计APP崩溃或有效手势样本，后续使用系统input完成测试。

Android9 X21A在断连前完成正式包安装及拉回哈希核对，原快捷桌面OFF未改；额外实际覆盖回归由用户后指定的V2458A完成。当前真机和模拟器专用shell探针按精确路径清理；断开的X21A本批CaptureGate/Generation探针文件待重连清理。真实PIN锁屏、其他ROM、高刷和长稳未验收，不能写全项目完成。OPPO仍待接入恢复正式包并补闪回对照，魅族60Hz与整体冷启动继续开放。

证据build/quickdesktop-failure-160-20261024：build-proof.json、native/旧源码负控、lifecycle16、emu-covered6截图、lifecycle-real16/results.json及real16-overview.jpg、v2458a/search-window.txt与开关前后实屏。执行期间索引由外部从156项变为170项；本代理未运行add/reset/commit/push，记录新的170项边界SHA256=99c15a2f09120a9eca33a64939614a19a702ac6a500d5592a39742e7687bb284，保留现有暂存。MEMORY.md未更新。下一项核对桌面、快捷桌面、搜索和设置窗口之间的刷新率申请交接；魅族实际ROM验收仍需对应设备。

<a id="2026-10-24-快捷桌面半开多指交接与android16回归未发现新增生产缺口"></a>

#### 快捷桌面半开多指交接与Android16回归：未发现新增生产缺口

本批承接零进度修复后的下一项，审查半开快捷桌面转多指、编辑/Folder/离开首页时的取消责任。当前Controller在openingGesture期间收到第二指会撤销capture、清opening tracker、立即关闭宿主并把事件交回原多指Owner；onProgress/onBackgroundReady在workspaceMode失效时复用closeImmediately。clean_launcher RootView原门控仍要求单指及首页/J.Ta/sLeftScreenEnabled，当前Smali仍在原GL目标CANCEL后才发截图请求。未发现需新增生产修改的证据；QuickDesktop各生产文件与任务前哈希一致，保留上一批Host零进度修复，没有重写手势/动画/窗口Owner。

扩展QuickDesktopCaptureGateProbe，从99增至219检查，Android9真机与Android16模拟器ART均通过，Root截图/取消顺序3检查仍通过。新增覆盖2/3/4指、背景尚未就绪/已就绪、迟到背景、下一次DOWN重新获取，及半开时编辑标志/Folder模式8/离开page0后的撤销与原GL终止保护。Host/截图及编辑状态为受控夹具，不能当作所有真实编辑转场验收。扩展既有TouchInput的multi-cancel-2/3/4测试模式：同一downTime、端点保持2.5秒供采样、依次POINTER_DOWN后CANCEL；复用既有prepare脚本，不增加生产注入或诊断。

Pixel_6_Pro/API36/x86_64，任务独占read-only/no-snapshot/host-GPU虚拟机，原1440×3120模式与1080×2400覆盖、480密度和默认HOME不改，沿用9c14721e92355db58d8d76b28511954a5c915d4e114001649a707c2945011ff3正式包，保数据安装并拉回核对一致，生产无变化不重复构建。先补五轮完整打开→左拖至-200归零松手→窗口移除→首页翻页，均通过；再五轮180→600半开停留→2/3/4/2/4指+CANCEL→首页翻页，均截图和WindowManager核对：半开时本包Popup存在且NOT_TOUCHABLE，取消后移除，日志逐轮出现multi-touch-owner，PID始终4288。五组截图人工核对不同页实际图标，未仅凭像素非零差异/时钟变化判断翻页。

另一次真实长按设置图标时截图确认Cell浮起与垃圾桶编辑态，随后双指+CANCEL恢复，未残留Popup且可翻页；半开时由外部强制改编辑状态仍只有隔离测试覆盖，不扩展为所有编辑转场通过。实际进入/关闭搜索和打开/滚动桌面设置正常。快捷桌面原本关闭，测试环境临时开启后按原行恢复关闭；结束关闭本任务虚拟机、不保存快照，安装及瞬态编辑状态不落回原AVD。vivo仅运行无用户配置写入的控制器隔离测试，未改其UI、总开关或包。没有主题/默认HOME/权限/系统日志修改。

失败与边界保留：Android16的app_process真实Host/Content探针在Typeface未初始化处失败；尝试只在探针调用平台loadPreinstalledSystemFontMap又遇初始化NPE，该尝试逐字撤回，未引入生产字体shim。两次不计740项通过；本批API36验收依据真实APK窗口回归，API9上一批740项保持。平台懒初始化机制参考 https://android.googlesource.com/platform/frameworks/base/+/refs/heads/master/graphics/java/android/graphics/Typeface.java 。未将模拟器结果扩展为其他ROM、高刷、任意进程回收或长稳验收。

证据build/quickdesktop-owner-audit-20261024：controller9/controller16、zero-formal16、multi-formal16/results.json及host.log、multi-overview.jpg、edit-held/取消后翻页截图、proof.json、两次失败探针目录。仅改三份测试源码/使用说明以及本日志和快捷桌面专项注记；专用shell探针清理，生产/正式APK无新增改动，156项原暂存patch仍7ac2e41db67cd4fca5d311f96fa5269b8a80018fcbaff3f7606d1a1879f70e19，无add/提交/推送，MEMORY.md未更新。下一项是锁屏/外部应用覆盖与截图失败时的窗口清理异常路径；魅族60Hz、OPPO闪回与整体冷启动仍开放。

<a id="2026-10-24-版权声明与使用规则审计保留既有木兰许可原创非商业条款待确认"></a>

#### 版权声明与使用规则审计：保留既有木兰许可，原创非商业条款待确认

按用户最终指定的两个本地工作区审计：桌面主项目与C:/Users/ck/Desktop/Smartisan-original-launcher-download。主项目无根级统一许可，但含Skia许可、原版Smartisan、maintained参考和Android／Tween等第三方来源；图标库已有2026-06-30加入的完整MulanPSL-2.0，不能通过README撤销其有效授予的商用等权利。素材扫描／哈希确认下载库5205张PNG，其中5199张与主项目同路径文件一致，另6张在归档目录；不能将这些图片重新概括为维护者原创或统一禁止商用。

两个中文README仅追加版权章节，图标库英文README追加一致说明；主项目新增NOTICE、docs/legal/LICENSING_AUDIT_20261024.md和ORIGINAL_NONCOMMERCIAL_LICENSE_DRAFT.md，图标库新增NOTICE、ASSET_LICENSES及5205条逐图asset-rights.csv。草案未生效、授权范围清单为空，等待权利人／适用文件片段／生效版本确认，不新增正式LICENSE，不覆盖木兰或Skia文本，不自动给第三方素材授权。PNG、索引、程序、APK、版本、安装和原有未提交文件均不属于本次修改范围。

验证为README原文字节前缀、现有许可证及素材／二进制哈希、台账覆盖、Markdown／本地链接、暂存patch保持检查；完整内容与证据在build/licensing-audit-20261024。未运行无关构建或设备测试，无add／提交／推送／发布。原版再分发授权、maintained复制范围、第三方组件版本和逐图证据仍未核实；免责声明不等于这些缺口已消除。MEMORY.md未更新。

<a id="2026-10-24-快捷桌面零进度触摸终止修复android9正式包五轮窗口释放通过"></a>

#### 快捷桌面零进度触摸终止修复：Android9正式包五轮窗口释放通过

承接上一条只读审查，本批生产仅QuickDesktopHostView.onTouchEvent的一处门控：只有openProgress<=0且没有正在进行的touchSequenceActive才拒绝事件。拖到底归零后继续处理当前MOVE/UP/CANCEL，复用原settleTo→onHostClosed→cleanup→禁用触摸/移除PopupWindow，不改方向门控、首页限制、动画曲线、阈值、布局或截图管线，不新增Manager/重试/延迟。与clean_launcher和原Magic Flow缓存的窗口/触摸区域交接对照延续上一条；普通Android不能照搬其私有Dock服务，本修复保留原版手势和当前公开Popup宿主。

扩展既有run_refresh_probe及QuickDesktopTouchTerminalProbe：真实生产Host/Content、原生View/Looper/MotionEvent，Controller回调和外部媒体/动作受控，无用户数据写入。Android9/ART的740检查通过：20轮UP/CANCEL到零终止、释放序列/Tracker、单次清理、闭合后拒绝新DOWN/游离MOVE/重复终止、零点反向连续及再CANCEL。旧生产源码负控准确失败于zero-progress terminal must be consumed，非编译失败。原Controller 99项及Root取消顺序3项仍通过。测试runner提供touch-terminal/host-source，补finally清理专用dex/ART产物；夹具不等于真实窗口验收，后者单独如下。

build.bat成功，v1/v2/v3、P16 zipalign、保留数据安装及拉回哈希通过。正式1.5.8/code33 SHA256=9c14721e92355db58d8d76b28511954a5c915d4e114001649a707c2945011ff3，相对任务前设备包非META-INF仅classes2.dex变化，已有其他设置页改动保留。首轮安装确认超时-200，重试在系统现有“继续安装”页确认后Success，不改安装安全设置。一次修前TouchInput shell生产者被Killed，未计为APP故障或有效旧版整机复现；修前根因负控仍由原生Host断言支持。

vivo X21A/API28、1080×2280、任务前即20宫格，用户明确授权临时开启原本关闭的快捷桌面。正式五轮首页右滑打开→左拖1000至-200到底→松手→首页左滑翻页，每轮截图人工核对，WindowManager均见本包全屏PopupWindow打开且关闭后消失、下一页实际显示，全程PID31169。另BACK/HOME各一次窗口释放通过。桌面设置打开/滚动通过；第一次stock swipe未进入搜索，不计PASS，改用已有单downTime TouchInput后实际进入搜索，截图核对并关闭返回。未输入查询或改历史。随后从同一原设置行关闭快捷桌面，quick-restored-off.png证明恢复原值，保留原主题/默认HOME/导航/布局/权限/日志策略，无清数据或其他后台。当前日志开关no，不能据此声称完整系统日志无错。

证据build/quickdesktop-zero-touch-fix-20261024：native9/old-negative/controller9、formal-five/results.json与开/关WindowManager文本、formal-five-overview.jpg、final-routes、installed-hash.json、build-proof.json。专用shell探针按文件哈希和精确路径清理。任务起点原156项暂存binary patch SHA256=7ac2e41db67cd4fca5d311f96fa5269b8a80018fcbaff3f7606d1a1879f70e19保持；无add/提交/推送，MEMORY.md未更新。只更新本日志及快捷桌面专项的限定验收注记。本项关闭已确认零点终止缺口；Android16/其他ROM、高刷、真实多指与编辑模式中断、锁屏/异常detach/长稳矩阵仍未覆盖，不写“全部触摸问题彻底解决”。下一项是快捷桌面半开时多指/编辑模式取消交接的针对性审查与Android16回归；魅族60Hz、OPPO闪回等既有任务继续开放。

<a id="2026-10-24-快捷桌面触摸遮挡只读审查确认零进度终止事件遗漏"></a>

#### 快捷桌面触摸遮挡只读审查：确认零进度终止事件遗漏

用户要求复核首页与快捷桌面切换是否仍可能阻断滑动，并比较原版。本批只审查，不改生产源码/正式APK、不安装、不切开关/布局。既有Launcher Stop/Destroy、HOME、异常detach、重新attach的cleanup以及迟到截图generation保护仍在；当前控制器99项CAPTURE_GATE和3项Root取消顺序检查在vivo X21A/API28通过。它们使用受控Host，不能覆盖真实Host自己的触摸状态。

发现P1：QuickDesktopHostView.onTouchEvent开头只检查openProgress<=0便return false。已打开页收到DOWN后touchSequenceActive=true；左拖MOVE将contentTranslation夹到-width时进度为0，但setContentTranslation为了等当前触摸终止，保留VISIBLE且不回调onHostClosed。接下来的UP/CANCEL又被顶部零进度判断丢弃，导致touchSequenceActive、VelocityTracker及全屏Popup清理链不释放；符合透明窗口可能遮住首页触摸的条件。不是旧修复删除，也不是GL卡住的证据。

实际生产Host/Content在Android9原生View/Looper/MotionEvent执行，外部Controller/media/weather/actions受控、不附着真实Popup：UP与CANCEL均得到accepted=false、progress=0、visibility=VISIBLE、touchSequenceActive=true、trackerRetained=true、controllerClosed=0；Launcher PID前后28083。此证明Host终止事件遗漏，尚非用户整机偶发现象的InputDispatcher抓取复现。测试副本仅把guard限定为openProgress<=0且!touchSequenceActive，两个路径均变为accepted=true、GONE、序列false、tracker释放、关闭回调1次；候选只保存在build证据目录，尚未写回生产，更未构建/安装验收。下一项明确是将该最小改动落到现有Host，并扩展零点反向/快切/BACK/HOME/窗口异常及真实Popup关闭后滑动回归。

原版对照使用clean_launcher RootView与e/e→e/b：原首页门控负责方向/单指/J.Ta/sLeftScreenEnabled，ContentResolver调用Magic Flow的request_show。原Magic Flow缓存build/magicflow-audit-20260906的b/o/n、service/MagicFlowService$b和view/RootView显示其独立系统侧边栏/Dock窗口，关闭维护窗口flags/触摸区域，HOME有forceHideDockWindowForHomeKey。当前移植为无系统权限的应用内PopupWindow，不能照搬其私有Dock服务；应复用当前dismissHostWindow先setTouchable(false)/update再dismiss的责任链。本地原APK归档当前仍缺主包，未声称新解包；maintained MainView未找到相同QuickDesktopHost替代，不迁移其分页核心。

证据build/quickdesktop-touch-audit-20261024/{native9,candidate-native9,capture-gate9}、测试脚本与副本。两个专用shell测试目录/探针按精确路径清理；连接中的emulator-5560未操作。原生产Host文件哈希与审查前一致，原暂存binary patch保持；其他并行默认桌面设置改动保留，不add/提交/推送。MEMORY.md未更新，仅更新本日志。快速多指交接、真实Popup WindowManager残留、跨ROM/高刷/长稳矩阵未完成，因此不能称触摸修复已完善。

<a id="2026-10-24-默认桌面文案本地化与页面职责拆分"></a>

#### 默认桌面文案本地化与页面职责拆分

用户接受标准设置行布局后，指出提示缺少英文、功能继续集中在MaintainedLauncherSettingsHost.java中。本批将页面绑定、三态检测、品牌提示选择、系统跳转与返回复核移动到DefaultHomeSettingsPage.java，只有这一份实现；Host仅保留入口、返回路由和原生命周期接线，复用既有资源加载与设置导航，没有新增Manager／Service或平行导航体系。

全部默认桌面文案移到default_home_guidance.xml：values／values-en为英文、values-zh-rCN为简体中文，共16个键，集合一致。标题、状态、品牌提示、错误信息无Java中文硬编码；英文用于无对应翻译时回退。未设置提示明确为“点击默认桌面，在系统页面选择锤子桌面，再返回本页”，无法确认时另提示核对／重新检测。其他设置功能文案不在本批范围。

生产涉及DefaultHomeSettingsPage.java、MaintainedLauncherSettingsHost.java和三份资源；tools/tests/default_home/run_tests.py读取真实中英文XML及独立页面真实方法，64项通过；原settings_session的33项与接线检查通过。build.bat、v1／v2／v3签名和P16对齐通过，版本维持1.5.8／33，APK SHA256为fb05d84afa21353d3e21221499bcf29842f77cca25eb107db8318d51177fcdea。

Android16只读模拟器应用语言en实屏确认Back／Default launcher／Smartisan Launcher及箭头；系统角色选择器取消后显示Not set和英文说明。角色弹窗选中本包并确认，系统HOME持有者为本包，再次进入显示Smartisan Launcher。系统选择器由系统语言控制，仍为中文，不属于本应用翻译遗漏。英文vivo／OPPO提示仅真实资源夹具验证，没有对应ROM英文实屏验收。

vivo X21A／Android9保留数据安装，中文页面截图正常；实际桌面Dock图标进入设置，打开AdvancedAppsActivity后系统BACK回同任务293的ThemeChooserActivity。未改物理手机语言、默认HOME、主题、宫格、权限或日志开关。上一节返回复核补充：ADB显式组件NEW_TASK创建的独立任务曾回HOME；实际Dock入口两轮均返回默认桌面页，两种任务栈不能混为同一验收。非标准独立任务、其他ROM、未知状态实机及完整动画／手势长稳仍未验收。

证据在build/default-home-page-20261024：build-localized.log、english-confirmed.png、english-unset.png、english-grant-reopen.xml、localized-phone-confirmed.png及本批测试／签名／哈希记录。上一节1823开头APK是布局阶段产物，本节是本地化／拆分后最终包。保留既有暂存，不add／提交／推送；MEMORY.md未更新。只读模拟器退出丢弃测试语言与默认桌面变更。

<a id="2026-10-24-默认桌面设置界面收敛复用原设置行移除多页帮助与重复操作"></a>

#### 默认桌面设置界面收敛：复用原设置行，移除多页帮助与重复操作

**本节替代下方默认桌面初版的多页帮助／状态卡方案。** 用户明确否决自定义状态卡、居中“完成”按钮、无箭头的操作标签、重复系统设置／检测入口和高级帮助。不得根据历史记录恢复这些界面。最新要求优先于最初任务中保留高级帮助的可选方案。

当前界面只有一个“设置默认桌面”页面：保留既有Title返回，主行“默认桌面”复用后台运行设置中的SmartisanSettingsRowTitle／Value／Arrow、72dp行高及原背景／setting_next资源，右侧显示“锤子桌面／尚未设置／无法确认”。主行是唯一系统选择入口，已设置时用于用户主动管理系统默认应用，不再另加“完成”或“打开系统设置”按钮。只在接口无法确认时显示“重新检测”行及原箭头；正常已设置／未设置不会重复显示检测按钮。未设置时以原TipsView／SettingItemTipsStyle、SettingItemTitleStyle显示简短操作和本机品牌提示，已设置时这些提示隐藏。整个高级帮助、独立帮助页面及其资源和代码已删除，不新增图标、皮肤或UI体系。

返回流程复用既有设置导航：DEFAULT_HOME页面支持无action的同组件返回Intent，保留页面及原返回动作；原MAIN／LAUNCHER返回协议不变，搜索、快捷桌面及自定义安装更新action不被该规则截获。进入系统前同步保存待复核及返回目的页；结果码与Resume仍共用系统事实检测，不凭RESULT_OK或跳转成功报成功。结果消费与返回目的页分开：返回HOME时静默消费结果，目的页保留到设置页真正恢复，再清除，支持进程中断后重新打开。顶部返回会结束本次流程并通过既有backToMainAction还原主设置页位置。

移除默认桌面检测中的全部成功Toast和自动失败弹窗，只更新本页右侧值及必要提示。旧pending在无关页面被消费时不显示任何界面，因此不会在后来进入主设置页时补弹“系统已确认…”的迟到提示。RoleManager／旧版HOME候选校验沿用前批实现，没有改Launcher核心、动画、壁纸、手势、Manifest或权限，没有新Service／Manager／轮询／延迟任务。

生产涉及MaintainedLauncherSettingsHost.java、setting_default_home.xml及default_home_guidance.xml；删除本任务早先新增的setting_default_home_help.xml。测试扩展tools/tests/default_home/run_tests.py，真实生产方法58项检查及原设置会话33项通过：三态值／可见性、仅未知显示检测、非默认页面不发UI、立即结果与Resume去重、返回目的页只在默认页恢复后清理、同组件Intent保页、搜索／快捷桌面／安装action排除等。构建、v1／v2／v3签名、P16对齐通过，版本保持v1.5.8／33；最终APK SHA256=`1823f33c6f8cf27d62497300bbe22d40ea3f9063e12699ec21394e2b613f17b1`。构建曾因多写一个未定义的间距dimen失败，已删除该覆盖并直接继承原标题样式，不新增猜测尺寸。

Android16只读无快照Pixel_6_Pro最终包实测：已设置页仅有返回、标题和一行状态／箭头；系统设置BACK回到同一页，同组件再次进入保留该页，顶部BACK回主设置；改为系统桌面后请求角色并取消，回到“尚未设置”和内联提示，没有结果弹窗或重复检测；系统角色弹窗真实选择锤子桌面成功，再次进入显示本包；两轮外部系统设置／返回均保持该页且无自动提示。XML确认可点击主行有原箭头。未知接口仅夹具验证，不冒充真实ROM异常。

额外的进程中断测试保留了无效断言：在系统DefaultAppActivity前台force-stop Launcher后，直接发启动Intent时仍显示系统页面，初始cold-return.xml不能记为应用页面失败或恢复通过；此命令不等同用户退出系统设置。实际按系统BACK先回HOME，再主动打开本应用设置，cold-reopen.xml恢复DEFAULT_HOME。此为只读模拟器的受控中断，不推广为所有ROM内存回收或所有冷启动路径验收，也不通过强拉Activity抢占系统页面来掩盖。

vivo X21A／Android9保留数据安装，并核对真实截图的行样式／右侧箭头。系统默认应用AdvancedAppsActivity按BACK后回到默认桌面设置页；真机默认HOME保持原本的com.smartisanos.launcher/.Launcher，未为测试切换用户桌面、主题、宫格、权限或日志开关。该机UIAutomator返回null root时不用旧XML代替结果，以截图与焦点为据。最终安装和设备哈希检查、收尾证据保存在build/default-home-page-20261024；旧自定义卡片截图保留为已否决草稿，最终标准行截图以final-standard-*为准。

其他品牌／OPPO、Android6～8实体机、未知接口实机状态、分身与受管设备、完整解锁／壁纸／手势长稳仍未验收。现有暂存patch不变，无add／提交／推送；MEMORY.md未更新。只读模拟器本次状态退出丢弃，不改AVD配置或快照。

<a id="2026-10-24-默认桌面设置引导返回复核与独立帮助"></a>

#### 默认桌面设置引导、返回复核与独立帮助

审计确认当前入口为 maintained 主设置页 `setting_switch_launcher → showDefaultHomeOptions → openDefaultHomeSettings`，优先请求 ROLE_HOME，再尝试 HOME_SETTINGS、MANAGE_DEFAULT_APPS_SETTINGS、既有 MIUI 入口和系统设置。旧实现的角色请求使用请求码0，onActivityResult没有默认桌面分支，onSettingsHostResumed也没有对应复核。ThemeChooserActivity已有完整结果／Resume接线，桌面内设置覆盖层也复用Host，不新增生命周期体系。NativeLauncherSettingsHost的同名实现未找到实际调用入口，本批不扩展该备用宿主。原APK归档仍缺失；对照clean_launcher的HOME候选查询与maintained的系统设置入口，未声称重新反编译原APK。

生产仅修改 MaintainedLauncherSettingsHost.java，新增 `setting_default_home_help.xml` 和 `default_home_guidance.xml`，继续使用既有Smartisan确认弹窗、标题／返回、行背景与页面导航。首次明确点击设置时简短说明需要在系统选择，继续后记录已看引导；没有启动自动弹窗。再次点击仍可主动查看帮助。普通帮助按实际品牌补充vivo／iQOO或OPPO相关系统的搜索词、版本差异及“系统提供该选项时再调整”的说明，不按品牌判定成功或失败；CTS等内容在独立高级帮助页，既不作为必需步骤，也不自动修改相关开关。帮助页“打开系统默认应用设置”直接走系统设置兼容链，跳过可能已被拒绝的角色申请；始终保留重新检测。

检测为1已确认、0系统未确认、-1无法可靠确认。Android10+角色可用时使用RoleManager.isRoleHeld(ROLE_HOME)；服务缺失／角色不可用才采用兼容查询，角色查询异常保留未知。旧系统通过不带包名或Component限制的MAIN/HOME resolveActivity，并要求结果准确匹配queryIntentActivities中的HOME候选，避免把系统Resolver／Chooser当成已选桌面；空结果、候选不可见或查询异常均为未知。只有系统确认本包才显示成功；其他结果显示“系统尚未确认默认桌面设置生效”，不归因于Launcher故障或未经证实的ROM限制。依据：[RoleManager](https://developer.android.com/reference/android/app/role/RoleManager)。未改核心LauncherHomeCompat的默认桌面门控。

跳转前同步保存pending标记，专用请求码54041接入现有onActivityResult及onSettingsHostResumed；两条返回路径共用一次性消费，不信任RESULT_OK，也不把startActivity成功当成设置成功。结果回调可覆盖系统立即拒绝而没有完整Pause／Resume的情况；持久pending允许进程中断后重检。消费后不会因后续Resume反复弹失败提示。帮助页当前状态也在重检时刷新，避免成功后保留旧的未确认文字。无新Manager／Service／轮询／延迟任务／权限／Manifest或桌面动画、手势、壁纸改动。

验证：生产方法夹具37项通过（角色true／false／不可用／异常、Resolver／空候选、查询异常、跳转回退、所有入口不可用、pending一次性消费、结果回调独立于Resume及忽略RESULT_OK、无关请求码不拦截、帮助直达设置绕过角色请求及品牌文案）；既有设置会话33项及生命周期接线检查通过。Android16／Pixel_6_Pro只读无快照模拟器覆盖首次引导、系统Role选择器取消、未生效提示／重检、帮助与高级帮助、系统默认应用页选择成功、实际默认HOME核对、后续进入设置不再弹失败结果；最终日志记录state=0与state=1，不能以一个ROM推广全部兼容。通过ROLE_HOME系统弹窗真实选中锤子桌面并确认后，系统HOME解析为本包，重新打开设置检查为state=1。界面截图／XML和构建日志在 `build/default-home-guidance-20261024/`。

vivo X21A／Android9保留数据覆盖安装：原锁屏时返回-200，解锁并完成vivo原生“继续安装”后，拉回APK验证实际安装，不把首次失败当成功。旧版兼容检测显示本包已确认；打开流程实到系统“默认应用”AdvancedAppsActivity并显示主屏幕应用为锤子桌面，BACK返回设置正常，vivo帮助文案已截图检查。真机默认HOME保持原本的com.smartisanos.launcher/.Launcher，没有为测试取消用户的默认桌面或调整桌面切换限制。该机UIAutomator多次返回null root，失败XML不作为证据，采用实际截图与焦点／HOME查询；既有系统日志限制未调整，不宣称完整日志无异常。

最终build.bat、v1／v2／v3签名、P16对齐及差异检查通过，版本保持v1.5.8／33，APK SHA256=`091f3d03f1353c2cf6c60d0487a82a82fea55733f2ce45e68d1aefd16fb0cc39`。相对任务前已构建包，非META-INF仅classes2.dex和assets/settings_maintained/maintained-settings-res.apk变化；原Smali、Manifest、资源素材和核心库保持。原暂存patch哈希保持54558ff3e07f7c8c006ef5e82331ba9681ccaf71，无add／提交／推送，MEMORY.md未更新。

最终APK补测：帮助页内将测试默认HOME从本包改为Pixel启动器后，手动重检显示未确认；恢复本包再重检，帮助正文即时更新为已确认。随后两轮进入外部系统设置并返回均未重复出现失败结果。真机与模拟器分别拉回base.apk，均与上述091f3d03…最终哈希相同。真机系统默认应用往返前后PID23237不变。模拟器只读实例使用独立5560端口，不修改AVD配置或保存快照。

“不再询问”补测：XML确认系统角色弹窗复选框checked=true后取消，再次申请时本AOSP16仍显示选择器；原测试对“必然立即拒绝”的断言失败，保留deny-6-checked.xml与deny-12-immediate-result.xml，不能据此声称立即拒绝实机分支通过。再次取消仍显示中性的未确认结果，帮助按钮直接进入系统DefaultAppActivity；无Pause／Resume的立即结果路径由上述生产代码夹具覆盖，其他ROM实际行为待测。

边界：Android6～8、Android10～15实体机、OPPO／ColorOS／其他品牌私有开关、受管设备／多用户、真实角色服务异常、完整解锁／壁纸／手势长稳矩阵尚未验收；异常与不可用分支是受控夹具验证，不冒充目标ROM实测。模拟器测试状态随本次只读实例退出丢弃。无新增环境依赖，CTS只提供说明。

<a id="2026-10-24-android16虚拟机刷新率实测3060节拍跟随120hz未验收"></a>

#### Android16虚拟机刷新率实测：30/60节拍跟随，120Hz未验收

按用户要求使用Pixel_6_Pro/API36/x86_64，两个独立read-only/no-snapshot/host-GPU冷启动，默认vsync60与临时命令行-vsync-rate30；同一正式bf07481401187d0e783f352d6d0ddce7da2d52c6ea92d618a3abf81d6d2c38f9保留数据安装测试，最终拉回APK校验。未改AVD配置或保存快照；退出后丢弃本轮安装/设备状态，不操作连接的vivo。宿主实际2560×1440/60Hz，模拟器-help-vsync-rate明确高于宿主刷新率可能undefined behavior，因此未用强制120值冒充120Hz验收。guest物理模式1440×3120，原wm覆盖1080×2400保持。

每档五次左右翻页、底部上滑实际打开搜索、BACK、Dock设置与滚动/返回，截图核对；没有改主题、布局、默认HOME或权限。SurfaceFlinger保存display/surface模式、TimeStats，23秒Perfetto含FrameTimeline/gfx/view并保存原始trace：60档系统renderRate60.000004、GL实际vote60.00；30档系统30.000002、GL vote30.00。搜索/设置expected-frame预算中位分别16.666666ms→33.333333ms，说明两个固定虚拟档位下可随系统节拍运行，没有发现固定60调度。TimeStats主GL分别304/269帧，present2present量化直方图中位18/33ms；总平均FPS含静止、ADB及dump耗时，不作为持续动画FPS。

必须保留限制：模拟器GL未提供完整buffer FrameTimeline token（仅TX事务不可当GL呈现帧）；旧--latency只有period无有效帧，第一次未正确转义层名的调用shell语法失败，均不作为实际呈现证据。UI FrameTimeline确有Late Present/Deadline Missed，TimeStats间隔也非全都等于面板周期，所以没有“所有动画稳定满帧”结论；宿主模拟器调度/采样开销不能归因魅族。两次独立boot不是同一多模式面板运行时切换；120Hz、魅族ROM裁决、文件夹120帧与全窗口高刷协商仍未验收。设置60档有框架60投票、30档为0，搜索两档0；不能把系统自动采用当前节拍等同应用已补齐统一请求。

本批生产代码/资源/正式APK未改，不重复构建；只更新此日志。证据build/refresh-audit-20261024/{60hz,30hz}/及summary.json、proof.json、capture.py、analyze.py。专用perfetto配置/trace与触摸dex清理，任务启动模拟器关闭，MEMORY.md未更新；148项index binary patch仍2c528b1e1aa8193bfd32c8208ba31d62bb1f34363a43d8f8bd85b429fa5797f2，无add/提交/推送。下一项仍为魅族连接后核对应用可见模式及主GL请求是否被ROM覆盖，再决定最小补齐各窗口高刷请求；本批不能关闭60Hz反馈。

<a id="2026-10-24-魅族仅60hz反馈刷新率覆盖只读审查待目标设备"></a>

#### 魅族仅60Hz反馈：刷新率覆盖只读审查，待目标设备

用户反馈魅族安装后仅60Hz，期望支持120Hz的手机在桌面各动画/页面都可高刷。本次只读核对当前源码与正式APK，不安装、不改生产代码或设备设置。目前ADB仅vivo X21A/API28，未连接魅族，机型/Flyme/Android、安装包身份及“60”测量方式待补，不能定性为Flyme限帧。

已确认覆盖缺口：当前LauncherSettingBridge.applyLauncherSurfaceRefresh仅API30+，同分辨率supportedModes取最高rate，向有效GL Surface投票；API31+限制无缝切换。仅SMGLSurfaceView.surfaceChanged和重新可见调用。未找到窗口preferredRefreshRate/preferredDisplayModeId或Application ActivityLifecycleCallbacks统一请求；搜索/设置等独立窗口不在此Surface请求范围，API30以下直接返回。正式bf074814…的classes2.dex含该Surface方法、不含旧LauncherRefreshRateCompat或preferredRefreshRate/preferredDisplayModeId字符串，与源码一致；这不是“全界面自动120Hz”的完整实现。

Eb.update真实elapsed推进、Folder归一化里的60f是原版时间单位基准，不是60fps上限；J设置原版GLSurfaceView按需渲染，动画期间update→Ra.wt→requestRender，没有在这条链找到固定16.67ms sleep限速。原版clean_launcher及maintained没有可直接复用的全窗口高刷适配。10/15旧运行记录中的独立刷新率控制器已不在当前源/正式dex，不能把历史V2458A高刷结论当当前全窗口证明；10/18当前有效日志明确收敛为Surface能力投票。没有为恢复旧控制器而删除当前兼容逻辑或新增Manager。

当前桌面主Surface没有主动锁60的代码证据，但应用可见supportedModes仅60、ROM忽略请求、仅无缝模式约束或静止降频均需要目标设备区分。官方说明setFrameRate是请求、不保证获得；见 https://developer.android.com/media/optimize/performance/frame-rate 。手机面板120Hz不等于每次合成都有120份新应用内容，静止按需不出帧也不能直接判失败。

下一步须在魅族同条件采集安装包哈希、应用可见模式/窗口与Surface请求、系统模式政策、持续翻页/Folder/搜索/设置实际buffer呈现间隔；分别判定无请求、请求被覆盖和渲染耗时，确认后最小补齐现有Bridge与各窗口接线。未连接目标机，未构建/安装/目标机回归，不报告修复通过。当前148项暂存保持，MEMORY.md未更新，仅更新本开发记录。

<a id="2026-10-24-默认圆框圆角底板修复android9-home-任务类型补测"></a>

#### 默认圆框圆角底板修复；Android9 HOME 任务类型补测

本批默认圆框修复已构建并安装 vivo X21A/API28；OPPO 已断开，按用户要求先验 Android9、OPPO 稍后补测。实际 Launcher 来源链捕获的 OPPO 九份原图及 Settings 两个 adaptive 子层表明：旧 V8 仅接受覆盖率99.5%的不透明方底板，93%～96%的圆角底板落回白圆；Settings 的 adaptive 背景 Bitmap 自带内缩，旧实现未按平台 extra inset 展开。早先 shell ResolveInfo.loadIcon 得到机器人占位图，不能用作真实应用来源证据。

DefaultIconCircleRenderer 复用既有完整 artwork 的矩阵与边界：只对高覆盖、逐行连续、近水平对称、中段铺满、上下单调收窄的圆角底板，在私有像素副本延展行端底色；允许上下圆角不同，圆形、孔洞和不规则轮廓保持原分支。自适应背景按 API26 getExtraInsetFraction 展开，再单次圆形遮罩；前景完整绘制、源 Bitmap/Drawable 边界与原阴影不改。版本升为 v9-rounded-background-and-adaptive-inset，经现有缓存身份失效旧圆框，不新增 Manager/缓存、不重绘素材、不整体放大裁切主体。原 APK 归档缺失，对照 clean_launcher 和 maintained 已有图标链，未声称新反编译原 APK。平台参考：https://developer.android.com/reference/android/graphics/drawable/AdaptiveIconDrawable#getExtraInsetFraction() 。

Android9 原生 Canvas 74项检查通过，旧 V8 负控准确失败于圆角底板边缘延展。九份真实 OPPO 来源在 Android9 同一原生绘制器重放，accepted-before/after 各九图；中心128区域最大通道差0～2，八个 legacy 外圈 alpha 差不超过1，adaptive 修正旧双遮罩。accepted-comparison-five.png 为来源重放对照，不是 OPPO 整机最终截图验收。证据 build/default-circle-rounded-20261024/actual-sources、replay-accepted-before/after、accepted-pixel-comparison.json、native-final、old-renderer-negative。

回归另发现上一节3b9入口在 Android9 显式 component 创建 standard task，系统 HOME 再建 home task，触发同进程重复初始化；15440→15569 且任务245→246，不按内存回收解释。复用 LauncherHomeCompat.createLauncherHomeIntent：仅当前默认 HOME 为本包时用同包限制的 MAIN/HOME 隐式组件，使系统按 HOME 类型建任务；非默认/无法确认时保留显式入口。Alias 仅在确认默认时转交；LauncherColdReloadCoordinator 与 MaintainedLauncherSettingsHost 共用工厂并保留各自 flags/extras，正常 Launcher 原版退出保护不删。AOSP9 ActivityRecord.setActivityType 对 componentSpecified 的限制与现场一致。最终34项入口协议检查通过；五次冷 Alias→外部设置→系统 HOME 均同 PID/同桌面窗口：16660/16854/17043/17221/17404，任务为 componentSpecified=false、mActivityType=home。此为受控入口复现，不是随机内存压力或所有加载动画消失的证明。

最终正式包 SHA256=bf07481401187d0e783f352d6d0ddce7da2d52c6ea92d618a3abf81d6d2c38f9，1.5.8/code33。build.bat、v1/v2/v3、P16 对齐、保留数据安装及设备拉回哈希通过；相对3b9非 META-INF 仅 classes2.dex 变化。本批临时 CircleSourceAudit 已删除、IconRasterDiagnostics 逐字节恢复，最终 dex 无采样类/标记。生产涉及 DefaultIconCircleRenderer、LauncherHomeCompat、LauncherColdReloadCoordinator、MaintainedLauncherSettingsHost 及上一节 Launcher.smali；长期测试扩展 default_icon_circle 和 home_entry。Android9 搜索底部上滑进入/关闭、桌面设置进入/BACK各三轮、既有两图标文件夹开关一轮已截图核对，未改设置或布局；最终会话 PID17404。系统日志开关仍 no，有限日志不作为完整系统无错证明。

OPPO 仍装临时来源采样包，重接后必须覆盖无诊断正式包并清理专属采样文件，再验九图实屏和新 HOME 工厂；手势闪回、整体冷启动、API24、Android16本批及跨ROM/长稳仍开放。未调整主题/默认HOME/导航/权限/日志开关，未清用户数据或其他应用后台。原148项暂存保留，不 add/提交/推送；MEMORY.md 未更新。下一项为 OPPO 重接后的正式包恢复和实屏验收，再继续其窗口交接时间线，不能以本批圆框修复关闭闪回。

<a id="2026-10-24-home-别名入口重复初始化修复oppo-手势闪回仍开放"></a>

#### HOME 别名入口重复初始化修复；OPPO 手势闪回仍开放

本批抓到一种额外加载的确定触发条件：OPPO PDCM00/API31 从 LauncherAlias 冷启动后，经外部设置返回系统 HOME，创建独立的 Launcher Activity，命中原版 J.b 的同进程重复初始化保护并由 ua.dc 结束进程。受控修前 PID23793→27728；升级后首次进入亦有30673→30765的同类链路。直接复用既有 HOME 的普通返回未触发。不能把这些 SIG9 仅按 exit-info 的 TOO MANY EMPTY PROCS 字段归为内存不足，也不能扩展为所有偶发加载的统一原因；用户已关闭的 Android9 内存现场结论不重开。

生产仅改 LauncherHomeCompat.java 和 Launcher.smali：应用图标别名先结束自身，再将原 extras 交给同包 MAIN/HOME 的规范入口，随后不进入原版场景初始化；该临时 Activity 的 onDestroy 跳过原版全局桌面清理，正常 Launcher 的 J.b/J.c/ua.dc 原样保留。无新 Manager、缓存、组件、Manifest、延迟或帧率改动。首版“先启动再结束”因 singleTask 复用别名而返回系统桌面，已否决，相关五组不算通过。启动诊断 begin 现在位于 super.onCreate 和别名排除之后；本批不对比旧计时起点宣称冷启动提速。原 APK 归档仍缺失，对照 clean_launcher 的原初始化/销毁及 maintained 入口实现，未声称重新反编译原 APK。

build.bat、v1/v2/v3、P16 对齐、保留数据安装及设备拉回哈希通过。最终 APK SHA256=3b9d31000166e8596d3463b575e5592383285b6a1562e5c76e61728129ed3efe；相对任务前4b7e0a20…非 META-INF 仅 classes.dex/classes2.dex 变化。构建后的真实 helper dex 在 OPPO ART 的27项入口协议检查通过。真机五个有效冷别名→设置→HOME样本均实际进入 smt_launcher，返回保持相同 PID 和同一窗口：5001、5964、11576、12963、13216。前两轮后电脑端 ADB 中断，第三轮作废，补齐三轮；未把短暂无连接当应用崩溃。另五次普通手势与三次 HOME 键返回均 PID13216，录像仍有背景先出现、图标随后补入，故 OPPO 闪回没有解决。搜索/设置收尾及完整证据见 HOME 专项第22节和 build/home-reload-audit-20261023。

此前 OPPO 旧包938942bc…与工程包虽同为1.5.8/code33但哈希不同，先保留旧包取现场基线，再按用户明确授权安装当前正式包及候选；旧包与修前正式包均已保存。没有更改默认 HOME、导航、主题、布局或系统日志开关，未清应用数据或其他应用后台；受控冷入口测试仅在设置前台 force-stop Launcher，不能冒充随机内存回收复现。Android9/16 等其他 ROM 未运行本补丁，内存回收、规范入口自身配置重建、状态栏高度自动纠正等仍可触发真实冷加载；不移除加载动画。MEMORY.md 未更新；原148项暂存内容保留，无 add/提交/推送。

下一项是 OPPO 的系统窗口交接，不再把该空档归入图标解码或加载动画时长。SF 单组对照首次采到有效且可见的桌面内容：手势为输入后440–480ms、HOME键220–260ms；仅为采样区间，非精确呈现时间。应用恢复时机与合成时间线尚缺严格同步，未找到已验收的新闪回修复。

### 2026-10-23

<a id="2026-10-23-第二十四批多页总览-dock-圆形比例与大小"></a>

#### 第二十四批：多页总览 Dock 圆形比例与大小

已按用户截图修复Dock应用图标压扁，并仅在多页模式13/10等比增大15%。既有preserveOverviewIconAspect只接受PageWithRenderTarget(M)父节点，明确排除了Dock(V)；原版clean_launcher CellAnimation使用eH/dH的cell_width与cell_height分别缩放，现代屏幕下两轴比例不同。现复用同一Bridge与弱引用元数据：页面仍按page尺寸补偿Y；Dock按cell尺寸补偿Y，再将sc[0]/sc[7]的X/Y等比乘1.15。记录原X/Y及最后提交X/Y，重复调用不叠乘，重绑定替换比例时以新值为基准，退出恢复。格子位置、触摸范围、页面比例、普通桌面策略、Bitmap/阴影资源与全局图标大小不改；左侧独立设置控制按钮非应用Cell，不扩大。本修改不进入Folder内容或大屏模式。原APK归档仍缺失；对照clean_launcher相同CellAnimation和maintained CellStatusForDock参考，没有直接替换原版核心。

生产文件仅launcher/tools/java/com/smartisanos/launcher/theme/LauncherSettingBridge.java。扩展tools/tests/geometry/OverviewAspectProbe.java及run_overview_probe.py，使用构建后的真实helper dex在Android16 ART执行，103检查通过：页面既有补偿、Dock独立cell/page比例、两种宫格对应模式、20次重复、ActiveIcon模拟重绑定和退出恢复；同时清理探针临时dex。夹具不代表真实Dock动态图标/20宫格全部视觉验收。

真机V2458A/API36、1260×2800，当前12宫格同一主题/布局/图标；保留数据安装成功，真实双指捏合进入、双指张开退出5轮。每轮总览电话图标裁片与修后参考逐像素一致，退出普通桌面电话裁片与张开后的参考逐像素一致；普通桌面修前独立截图未采到，因此不声称修前/修后普通桌面已逐像素对照。原生还原测试与本机五轮退出验证共同支撑还原结论。before.png/pinch-after.png、valid-overview/normal-1..5.png及comparison.png保存真实效果，不以亮度阈值下的渐变局部区域冒充完整圆形轮廓。之前BACK未退出总览的5组截图保留为无效进出尝试，不计入有效五轮；退出方式已纠正。一次中途点击相机仅打开界面，随即BACK返回，未拍照或更改其设置。

Dock桌面设置入口使用100ms实际触摸成功，初次过快input tap未触发；未动设置项。额外搜索尝试中stock swipe没打开，旧TouchInput shell探针被系统Killed，因此本批不报告搜索通过、不据此修改搜索代码。专属双指探针正常，设备最终留在总览供用户检查；临时shell dex清理。构建build.bat、签名、16KiB对齐、覆盖安装拉回哈希一致，最终SHA256=4b7e0a20a441662551acf155f33efb26cb3ffad715a494f8902b65128337452b。无新增生产Manager/缓存、未更改主题/宫格设置/布局/权限、未清数据或后台。原暂存patch哈希与任务前相同；MEMORY.md未更新，无add/提交/推送。证据build/dock-overview-20261023。其他ROM/Android9、20宫格真实切换、Dock动态图标/文件夹/通知角标拖放及透明/毛玻璃完整矩阵未测，不扩展为全场景完成。此前冷启动和主题取色待办保留。

<a id="2026-10-23-第二十三批录屏定位冷启动结束后的状态栏黑带"></a>

#### 第二十三批：录屏定位冷启动结束后的状态栏黑带

**第二十三批当前：vivo X21A/Android9冷启动后顶栏黑带已复现并最小修复，未改加载动画时长或壁纸取色。** 原正式包两段录屏均显示桌面先完成淡入，随后只有顶栏背景变黑再恢复；中央顶栏与下方空白区亮度差最大193/205（0～255），记录到黑带12/11帧。临时去掉e/g跨两帧明暗刷新仍有11帧黑带，该假设排除，Smali逐字节恢复。真正有效的限定修复在OriginalLoadingContentFactory.coverLoadingWindow：仅Launcher Activity、空文案的普通初始化加载窗、且非协调重载黑色覆盖窗，清TRANSLUCENT_STATUS、加DRAWS_SYSTEM_BAR_BACKGROUNDS、透明statusBarColor；原FULLSCREEN、layout flags、导航栏、内容/坐标/动画与dismiss时机不变。Coordinator仅暴露现有sInitialLoadingWindowApplied的包内只读判断，保护协调重载黑色覆盖，不新增状态/Manager。候选5段及正式包1段冷启动录屏均无该黑带，12静态图标区域逐像素一致；2520窗口策略场景12790检查通过、旧源码负控准确失败。正式build.bat、v1/v2/v3、P16、保留数据覆盖安装拉回哈希、五轮底部上滑搜索/settings结果/桌面设置/返回及既有文件夹开关通过，同PID5109；最终SHA256=f58efc77a2b2a9c17608fbe0695b1d4cda38ea963e7f54a5602cdfc4ed2a3901，相对第二十二批非META-INF仅classes2.dex。此前来源查询优化保留、暂存134项保持，MEMORY未改。证据build/startup-statusbar-20261023。

**原版取色与下一项：** 原版clean_launcher的initGaussianDarkLight分别分析桌面、顶部90px带和底栏，保存sGaussianResSuffix/sStatusbarColorSuffix/sNaviBarLightOrDarkSuffix；顶部亮暗经status_bar_icon_color[_light]、status_bar_number_color[_light]由e/s.d→UI线程e/g→ua.setSystemUiDecoration提交，并非故意制造黑背景。普通主题采用主题固定配色；透明/毛玻璃相关路径沿用其壁纸分析分支。当前移植e/g按先前已验证兼容方案用最终app_text_color统一legacy/API30+ appearance，这与原版分区资源策略有差异，本批不撤销已确认的四指/主题兼容修复。用户新增假设已核对源码；本机黑带由保留该取色路径、只改窗口背景声明的对照消除，不能据此关闭透明/毛玻璃深浅壁纸文字颜色矩阵。下一项为该矩阵及切换顺序验收；本轮没切主题/壁纸，Android16/其他ROM、真实16KiB/长稳等仍未验证。整体冷启动仍开放，Folder性能暂停、A22不重开。

**原版来源与责任边界：** 查阅clean_launcher/data/Constants.smali、e/s.smali的k(Bitmap)/n(Bitmap)、e/g.smali及theme/X.smali，顶部裁片高度为min(90,bitmapHeight)，普通屏亮度阈值0.6×256、大屏0.85×256；主题trans/aero参考colors的status_bar_icon_color为白、_light为深色，数字颜色可独立配置。原版使用Smartisan自有装饰接口，不能把其调用等同于普通Android已实际显示正确颜色；当前兼容提交还维护透明窗口flag、legacy明暗和Insets。原APK归档仍缺失，未声称本批重新反编译；maintained的LoadingUI/SmartisanProgressDialog仅作原加载结构/标志参考，未替换当前核心逻辑。加载本体慢仍有首屏构建耗时，不能把顶栏闪黑当作动画时长问题，也未用提前隐藏Loading伪造完成。

**可复核实验：** cold-1/cold-2录屏中，桌面区域亮度≥220后顶栏低于邻近背景50以上的捕获帧分别12/11，PTS区间3.940～4.160/3.985～4.191s，完全恢复约4.230/4.244s；视频PTS与trace未精确对时，不虚构SurfaceFlinger因果时间。no-crossframe-1仍有11帧（4.214～4.404s），直接颜色提交保留，故未保留该临时修改。只补透明背景声明后5段记录的顶栏/邻近背景最大亮度差0.956/0.440/0.202/0.504/0.587，均0黑带帧；正式包第六段同样通过。原片/候选均native分辨率1080×2280、8Mbps/12秒screenrecord，系统设置→force-stop Launcher→显式启动，不清系统/ART/磁盘缓存，录屏可能扰动耗时；这是视觉问题验收，不替代性能五样本或实际HOME手势。截图裁片statusbar-before-after.png保存正常→黑带→恢复→修后对照，不依靠仅一张最终截图证明无闪烁。原明暗刷新已恢复，排除“顺带删掉刷新才消除”的混淆。

**最小修改与测试：** Factory复用现有Window owner，不改SmartisanProgressDialog Smali、J.b窗口全屏流程或原画面；Coordinator getter只读已有volatile applied标志，不增加持久状态。新增tools/tests/theme_wallpaper_sync/run_loading_window_tests.py，提取实际coverLoadingWindow及getter，JDK受控Window/View/Context夹具覆盖API23/24/26/28/29/30/36、Launcher/其他Activity/普通Context/null、空/主题切换/初始化文字/其他/null文案、重载覆盖所有权、不同窗口/导航/外观标志和空Window。确认仅限定冷启动增加透明背景声明，原FULLSCREEN/导航/UI标志/切口/动画与其他场景保持；2520场景12790检查通过。旧Factory负控在cold startup must own transparent bar backing准确失败，非编译失败。夹具不是对应API/ROM实测；重载黑覆盖、主题切换和Android16本轮无UI验收，不把条件保护写成设备通过。

**正式交付与恢复：** 正式五轮查询/设置截图已人工核对；12静态区域一致，动态时钟排除，文件夹仅开关功能回归不重启性能任务。系统窗口原默认桌面/主题/壁纸/布局/权限/刷新率保持，未清后台/数据或进工程模式；日志开关仍no、log.tag=E，当前PID AndroidRuntime无错误输出不代表完整系统日志验收。atrace最终0，所有本批设备录屏文件拉回后按精确文件名删除，shell helper清理；源码无临时诊断，源报告修复逐字节保留。原暂存binary patch SHA256仍3619c27785b0898dc8d46da403e9f9380276a9b136ccb682e9359e5d4d3f83fb，无add/提交/推送；项目及全局MEMORY均未更新。

<a id="2026-10-23-第二十二批合成诊断复用实际圆框策略消除额外来源查询"></a>

#### 第二十二批：合成诊断复用实际圆框策略，消除额外来源查询

**第二十二批已完成最小修复及Android9真机回归，整体冷启动仍未解决。** reportSourceCanvasOnce在合成之后为日志调用desktopIconSourceType，DEFAULT又经单参desktopDefaultCircleEnabled再查一次；composeTexture此前已有本次实际defaultCircle。生产仅IconRasterDiagnostics.java将该布尔值交给报告，移除报告内来源/圆框重查，不改变绘制、选择/回退/失效、纹理键或Bitmap责任，无新增缓存/Owner。vivo X21A/API28原/新各5启动，每轮31份首次报告的额外来源查询37→0，相关计时段中位73.173→0.093ms；PAGE_READY2165→2148ms，最长GL帧1643.042→1566.377ms/CPU1500.264→1452.809ms，小样本含调度/缓存/ART状态，不能将差值全部归因或宣称整体解决。实际合成/报告方法在ART的1033场景11351检查通过，旧源码负控准确失败；稳定设置下日志/像素一致，另测来源与设置在绘制后变化时报告仍描述本次实际绘制。正式包五轮底部上滑搜索、settings结果启动、桌面设置、返回及既有文件夹开关通过（PID31327）；原/新/正式12静态区域逐像素一致。build.bat、v1/v2/v3、P16、v1.5.8/code33、覆盖安装拉回哈希通过；非META-INF仅classes2.dex，最终SHA256=af813f47e41b91bd36456b8234dc5243846432a32b851d67008a99971d3b5b8e。临时Host/Startup诊断逐字节恢复，dex标记及专属JSON清零，134项暂存patch保持，MEMORY未改。证据build/startup-source-report-20261023。

**接下来：** 用户追加“加载动画结束后状态栏黑一下”，本机录屏已复现桌面内容先稳定、顶栏随后独立变黑约0.3秒；转入该窗口/状态栏交接问题的逐帧对照，不把它归为加载动画时长或以本批性能修复宣称关闭。冷启动剩余GL成本、Android16/三星Share/跨ROM/首装/长稳/真实16KiB仍未全部验收，Folder性能暂停、A22保持关闭。

**测量与验证边界：** 原PAGE_READY2451/2179/2139/2165/2161ms，候选2294/2148/2084/2179/2078ms；原报告策略段74.799/75.086/72.044/73.173/71.182ms，候选0.093/0.089/0.086/0.093/0.095ms。计数仅GL首屏、报告once gate通过后的策略查询区间，非整份报告时间；候选剩余为空区间的临时计时成本，不是正式包业务耗时。每组五样本保留首轮慢值，未清OS/ART/磁盘缓存，2MiB per-CPU atrace，PAGE_READY记时后导出JSON；不是首装/物理呈现测量或随机因果实验。报告37次源查询由31份报告中的6个DEFAULT再查所致。debugMetrics另有查询但DEBUG_RASTER_DUMP=false，不借机改动未运行路径。

**测试与参考：** 扩展既有tools/tests/icon_raster/run_bounds_tests.py的source-report-snapshot模式，不新建生产系统。提取实际compositor/report/scanner配合Android原生Bitmap/Canvas；源/几何/光影Owner为受控夹具，检验DEFAULT/CUSTOM/RESOURCE/PACK/IMPROVED/null来源、圆框开关、重复report gate、图像Alpha阈值、Drawable边界、角标/投影/阴影原地突变、空图及几何不可用、借用输入不回收、输出/临时图释放；稳定条件日志公式不变，晚到设置/来源变化时以当前绘制快照为准。旧源码负控为设备断言candidate report must reuse selected policy，非编译失败；正式生产源码复跑同样通过。该诊断Owner为当前移植兼容层，clean_launcher与maintained无同名原实现可替换；原APK归档仍缺失，未声称重新反编译。本批只改方法参数和删除查询，不改变任何纹理像素或缓存版本。

**交付与风险：** 正式包回归截图已人工核对，UIA XML本机不可得；返回是BACK加显式Launcher前台，非系统HOME手势验收。AndroidRuntime无错误输出但persist.sys.log.ctrl=no/log.tag=E限制保留，无工程模式/日志开关更改。atrace最终0、测试JSON与shell helper清理；无清数据/后台、布局/权限/刷新率/默认桌面调整。134项暂存binary patch SHA256仍3619c27785b0898dc8d46da403e9f9380276a9b136ccb682e9359e5d4d3f83fb；不add/提交/推送，项目及全局MEMORY均未更新。用户追加状态栏调查后会发生额外冷启动，PID31327仅代表本批五轮回归会话。

<a id="2026-10-23-第二十一批主题资源解码五样本审计未发现同图重复"></a>

#### 第二十一批：主题资源解码五样本审计，未发现同图重复

**10/23第二十一批当前：本项审计及Android9真机回归完成，生产代码净改动为零，整体冷启动仍未解决。** vivo X21A/API28同条件5次进程启动，在GL线程至PAGE_READY范围记录xa.getBitmap与xa.a(AssetManager,String)实际成功打开的AssetManager身份及资源路径；每次37个实际来源、37次解码，重复来源数均0。解码区间中位203.630ms，诊断PAGE_READY2341/2159/2133/2174/2191ms（中位2174）；含记录/首次调用栈开销，没有候选修复对照，不能算性能收益。原背景、文件夹底图与cover中位65.638/55.455/30.093ms，属于不同素材；20张back1～back20也是独立素材，不能按相同前缀当重复。现有f→Ea按键复用Da纹理；Da上传或释放会回收其持有Bitmap，因此未新增xa裸Bitmap缓存。两份临时诊断源码逐字节恢复，正式build.bat、签名/P16/v1.5.8 code33、保留数据安装及拉回哈希通过；全部非META-INF ZIP成员与本批原正式包相同，重打包整体SHA256为73319f890b86e997ec79c6a488260fafe0508128bd96ed2bd0f9d96025fb62c7，不宣称APK逐字节重现。正式包5轮底部上滑搜索/settings结果真实启动/桌面设置/返回及既有文件夹开关通过，同PID27504；12静态区域一致、截图人工核对。最终dex无本批诊断标记、专属JSON清零、atrace=0，日志开关保持no/log.tag=E；134项暂存patch不变。MEMORY.md未更新。证据build/startup-theme-assets-20261023。

**下一项：** 核对IconRasterDiagnostics.reportSourceCanvasOnce为日志再次调用desktopIconSourceType的成本；composeTexture已有resolved.type和实际defaultCircle结果，先计数验证额外解析，再考虑将同次结果交给报告，保持绘制/回退/来源失效语义，不新增缓存。不要重拆本项资源解码、重开最终磁盘缓存/无条件页延后/前移加join。Folder性能暂停、A22按用户确认关闭；本批未验证其他主题/Android16/三星Share/跨ROM/首装/长稳/真实16KiB，未关闭这些缺口。

**范围与原版核对：** 实际loader为xa.1.smali，xa.smali是另一个大小写相邻类。当前xa.1与clean_launcher相同；Ea查找/添加仍为原版按键Map逻辑，保留现有resetProjectionBindings；Da与原版干净参考相同，Tb(true)指定上传后回收，Ka也释放持有图。xa正常化转换也可能回收输入，不能改变借用责任。原APK归档缺失，本批未声称重新反编译原APK；maintained未找到对应LauncherAssetManager Java实现，未搬运其核心逻辑。来源识别基于实际成功open而不是只记请求名称，排除主题fallback混算；五轮资源集合一致，未解析来源数0。记录只保留元数据不持有Bitmap，不覆盖所有框架/托管图标解码，也不代表后续滚动或打开文件夹路径；文件夹纹理作为启动资源统计，不恢复已暂停的Folder性能任务。

**验证与恢复：** 五次解码总区间206.323/200.711/198.387/203.630/214.937ms，均37来源/37调用。正式包12静态图标与第5样本一致，动态时钟排除；UIA XML本机不可得，保留截图及焦点验证边界；返回为BACK加显式Launcher前台，不冒充系统HOME手势验收。PID AndroidRuntime未见错误输出，但系统日志被设备策略限制，不能作为完整系统日志无错证明。未清数据、后台或改主题/布局/默认桌面/权限/刷新率；两项文件夹为用户既有文件夹。暂存binary patch SHA256仍3619c27785b0898dc8d46da403e9f9380276a9b136ccb682e9359e5d4d3f83fb，无add/提交/推送。仅更新本节涉及的五份既有文档；项目及全局MEMORY均未更新。

<a id="2026-10-23-第二十批跳过普通主题零几何阶段的提前壁纸分析"></a>

#### 第二十批：跳过普通主题零几何阶段的提前壁纸分析

**10/23第二十批当前：已定位并减少初始化前段的一次完整壁纸解码，整体冷启动仍未解决。** 前批两个约84ms decodeBitmap来自Application/X.da与Activity/Constants.initByTheme，均请求同一私有壁纸URI（只记录URI摘要/size/mtime，无原始路径），各解码1080×2280/9849600字节Bitmap。Application阶段窗口几何为0，Activity阶段1080×2280且有系统栏几何，不能复用整套明暗结果。生产只在theme/X.smali的da入口加限定：Application、宽高均0、非毛玻璃/非透明/非默认固定资源主题、非大屏才跳过早期分析；该普通主题分支仍使用原unsuffixed系统栏资源，后续原initByTheme在有效几何下完整分析后才创建桌面。无Bitmap或结果缓存/新Owner，不改分类算法、URI读取、主题切换或渲染时序。实际X.da Smali在ART的6144场景30744检查及两类负控通过；现有壁纸同步49断言通过。vivo X21A/API28原/新各5启动，分析/解码次数2→1，早期分析中位127.664→0ms，bindApplication443.650→310.130ms；Activity起算PAGE_READY2147→2173ms没有改善，不能宣称整体冷启动解决。正式包五轮搜索/设置/返回与既有文件夹开关、额外冷设置入口通过；壁纸/文字/材质遮罩及12静态区域原/候选/正式逐像素一致。最终SHA256=8d54bbf32de069b4dc10e12e6e7e557b1a2d2e8f690b26fcceefe14702da5528，签名/P16/真实安装拉回哈希通过，非META-INF仅classes.dex变化；诊断3文件逐字节恢复、dex无标记、测试JSON清零，134项原暂存保持，MEMORY未改。证据build/startup-main-decodes-20261023。

**下一项：** 本批主线程两次大解码定位及限定修复收口，不重复拆本微任务。剩余首屏GL仍约1.65秒/运行CPU约1.51秒；先利用已存trace和现有资源Owner，统计同一主题纹理PNG的解码次数、是否有可复用结果及借用/回收约束，再决定最小修复。不得直接新增raw Bitmap缓存、重开最终磁盘缓存/无条件延后页/简单前移加join。Folder性能暂停、A22按用户确认关闭；本批仅Android9普通非默认主题真机，毛玻璃/透明/默认/大屏是代码分支保护和原生夹具覆盖，不是对应主题/ROM实测，Android16、三星Share、全ROM/首装/长稳/真实16KiB仍有缺口。

**根因与原版依赖：** 复用第十八批方法采样，85ms decodeStream祖先为e.s.n→Constants.initGaussianDarkLight→initByTheme→initLayoutParams→J.b→Launcher.onCreate。普通计数补齐更早的Application路径，唯一X.da调用在ja.onCreate；X.da先更新主题/资源/壁纸URI，再分析明暗，而普通分支随后直接调用原e.s.n(theme)/c(theme,"")，不消费亮暗后缀。Activity的J.b先执行initLayoutParams→initByTheme，再new J、setContentView和K创建场景。Constants.initByTheme中X.h为true的默认固定资源分支不会同样再分析，所以候选明确保护默认主题；毛玻璃/透明会使用早期后缀，同样保留；大屏及任何非0/部分/异常几何保留；非Application Context也保留。后缀/覆盖值的Smali读者主要在Constants、X、J、view和交互Action，桌面J/场景读取前原布局初始化已完成。没有跨阶段复用不完整的零几何结果，更没有按URI缓存易失效的结果或保留9.85MB原图。减少一次临时Bitmap分配不等于常驻或峰值内存减少9.85MB，不重开A22内存现象。

**参考和范围：** clean_launcher同样有X.da及Constants明暗分析链，maintained Constants也保留同名分析，不搬其核心流程。原版APK归档仍缺失，未声称重新解包。当前兼容层已有isDesktopWallpaperDark在无窗口几何时返回false，但原full-image cover/top/bottom分析仍会解码；因此没有简单复用第一次全部输出。改动只有X.da一个调用前的限定分支，仍保留壁纸URI发布、材质资源注册、原正常系统栏分支与Activity完整算法；无新Manager/Service/helper、线程、timer、Manifest或Java生产变化。几何0且普通非默认主题时分析发生在其原本已有的后续布局阶段，不移动场景创建、不改变GL可见页面数量、也不改WallpaperManager写入策略。

**普通五样本数据：** 先用1次baseline-gaussian路径探针确认来源与几何，单独保留不计五样本。baseline-fix原PAGE_READY2147/2209/2182/2119/2125ms，candidate-fix2513/2182/2173/2165/2150ms；中位2147→2173，没有改善。候选首轮2513ms保留，没有剔除慢样本。两组采用同一API28/vivo X21A/b2a4da1c/4KiB/20宫格/原壁纸与设置，force-stop进程、OS/ART/磁盘缓存保留、2048KiB/CPU atrace；基线此前有1次路径发现启动，安装/ART状态与调度不构成严格因果随机对照，不扩大收益归因。每轮原2次、候选1次明暗分析/完整解码；原总解码中位167.776→84.055ms，总分析246.370→128.450ms，早期127.664→0；前者是后者的子区间，不能相加。bindApplication443.650→310.130ms、activityStart294.761→294.635ms；最长GL帧1615.260→1652.529ms、运行CPU1490.810→1507.658ms，GL没有改善。bind开始至首个最长GL帧结束2583.735→2491.057ms仅是框架/GL构建代理区间，不能当物理呈现或PAGE_READY。PAGE_READY时钟从Launcher Activity.begin开始，早期Application分析不在其中；不把前段改善说成2147ms页面本身提速。数据及限制一起保留。

**来源与标量证据：** 所有基线两条记录请求同一URI摘要且file长度1332307/mtime一致，源在应用private files内；这是请求身份与文件元数据对照，不是文件内容SHA256。每次原解码尺寸1080×2280/9849600字节，第一条Application窗口0×0/系统栏0，第二条Launcher1080×2280/状态栏103/导航栏90。候选只剩同样的Launcher有效几何行，10次有效样本最终sGaussianResSuffix=_light、status/nav后缀为空、sGaussianBackGray=0.29843098、sEyeCoverPageColor=0.9均一致。临时计时仅包围原decodeStream和原分析方法，流关闭及Bitmap recycle仍走原方法；诊断未额外导出原始图片或原始私人路径，仅保留正常界面回归截图。元数据取样及URI摘要在计时前，仅诊断使用；JSON在PAGE_READY时钟记录后写app专属目录。三个临时Owner Constants.smali/e.s.smali/LauncherStartupDiagnostics已逐字节恢复，正式dex无gaussianAudit/GAUSSIAN_AUDIT/专属导出名。

**验证与测试边界：** 新增tools/tests/theme_wallpaper_sync/run_initial_analysis_tests.py，复用项目SmaliBuilder→DEX→app_process，提取真实完整X.da指令；仅把主题/资源/引擎/分类Owner改为受控夹具，Context/Application/Activity与Dalvik为实际API28。6144场景30744检查覆盖3类Context、4类几何值的宽高组合（负数/0/部分/有效）、毛玻璃/透明/大屏/默认标志全组合和8种亮暗结果；比较主题/源/材质/系统栏操作，允许的0几何路径少一次分类、后续布局分类结果保持。旧源码负控和故意删去height保护的mutant均准确失败classification gate exact scope，不能把编译失败当反例。测试夹具初版未prepare Looper且缺setIconType方法桩，修补后才得到有效结果，不当作Launcher运行崩溃。另跑现有壁纸同步实际Host方法49断言，受控输入而非OEM像素证明；没有实际切换用户毛玻璃/透明/默认/大屏设置。

**正式包和真机回归：** build.bat、v1/v2/v3、P16、aapt2 v1.5.8/code33、pm path拉回SHA256通过；原/新非META-INF仅classes.dex，classes2.dex/Manifest/resources/assets全相同。正式5轮桌面设置/BACK、单downTime底部上滑搜索、settings提交/查询图标/系统设置结果实际启动与返回均同PID24303，5张查询与设置截图已核对；原/候选/正式12静态图标区域一致。额外比较桌面y140..2239整片RGB，排除动态时钟面但保留壁纸/文字/材质，候选、正式首次就绪及文件夹返回后均逐像素一致。既有文件管理+日历文件夹只测功能，不恢复卡顿试验。为保护非HOME进程入口，另force-stop冷启动ThemeChooserActivity，截图/20宫格状态正常，再BACK/显式Launcher同新PID25394进入桌面且整片RGB遮罩一致；没有把此额外重启混入五轮同PID验收。没有OEM快捷服务/所有设置子页的完整冷入口验收，不扩大成全矩阵通过。PID AndroidRuntime未见错误输出但log.tag=E/persist.sys.log.ctrl=no边界保留；无日志开关/工程模式/清后台/默认桌面/权限/主题/刷新率/用户布局修改。最终atrace0、专属JSON0、shell probe清理，134项原index patch SHA256仍3619c27785b0898dc8d46da403e9f9380276a9b136ccb682e9359e5d4d3f83fb；无add/提交/推送，项目与全局MEMORY未改。

<a id="2026-10-23-第十九批变体映射直接迭代消除完整包名数组复制"></a>

#### 第十九批：变体映射直接迭代，消除完整包名数组复制

**10/23第十九批当前：变体表首次加载已完成归因与最小减分配，未证明明显启动提速。** 每进程在GL线程同步加载1次356182字节/4625包的variants.json；原5样本读取/JSON/映射整理中位6.506/15.770/54.817ms，整体73.113ms（各自中位不可相加）。生产仅IconPreviewRepository.ensureVariantsMapLoaded：用已有JSONObject.keys迭代，替代names→JSONArray→索引循环；不移动读取时机、匹配顺序或改变现有Map/错误策略，不新增缓存/Manager/线程。实际加载器/getVariants方法在API28 ART配合受控流的190场景24535检查通过，4625项完整映射/列表顺序一致，names转换1→0，旧源码负控准确失败；现有资源ID/实时catalog/file/variants原生80检查通过。vivo X21A原/新各5启动，加载整体中位73.113→72.483ms、映射54.817→52.041ms，PAGE_READY2191→2176ms；差值很小且含调度/缓存，不记为整体冷启动已解决。正式包五轮底部上滑搜索/settings结果实际启动/设置/返回与既有文件夹开关通过，原/候选/正式12静态区域像素一致。最终签名/P16/覆盖安装拉回哈希一致，非META-INF仅classes2.dex；SHA256=d2c23bfdabed298a5d911229a26df4c1caa4397ba70a671f1e7cf4672298a9b8。诊断源码恢复、最终dex无标记、专属测试JSON清零；134项原暂存保持，MEMORY未改。证据build/startup-variants-20261023。

**下一项：** 现有候选5条trace均出现主线程两次约84ms decodeBitmap（每轮两项均83.9～84.9ms）。先定位其资源名及调用方，确认是否同图重复解码再修，不继续拆本批变体表迭代微任务，不依据同样时长直接认定相同图片。整体冷启动仍开放；Folder性能暂停/A22关闭不重开，三星Share、Android16本批回归、首装/长稳/跨ROM/真实16KiB缺口保留。

**根因、参考与保留边界：** 旧方法先把JSONObject的4625个key复制成JSONArray，然后逐项optString再建HashMap。前批1ms方法采样提示ensureVariants约110.424ms、names约85.633ms，不能当普通运行中的稳定耗时或可删除收益；本批去掉方法采样，普通分段计时确认文件读取不是大头，但没有独立隔离names本身的时间。查阅本地SDK org.json实现，names通过ArrayList/keySet和JSONArray复制；生产改为直接keys迭代，复用当前Owner，IconLibraryCatalog.readMap也已有相同写法。原版clean_launcher/maintained没有本兼容层同名加载器；原APK归档仍不存在，不声称重新解包。现有indexPool只预载IconLibraryCatalog并非可供此方法复用的已就绪variants结果，未添加简单前移加join或以线程竞争遮盖等待。候选优先级、精确组件/系统别名/包名/变体判断、getVariants defensive copy、流关闭和错误空Map处理均保留。JSON对象key原本即字符串，迭代同一对象，既不删除字段也不新增解析器/资源生成协议；assets、缓存版本和来源身份未改。

**五样本：** 原PAGE_READY2324/2126/2181/2191/2199ms；候选2287/2158/2176/2179/2123ms，中位2191→2176。原总加载73.113/77.309/68.761/116.388/73.072ms；候选69.703/74.747/85.549/72.483/71.215ms，中位73.113→72.483。读取中位6.506→6.036、JSON15.770→14.303、映射54.817→52.041ms；阶段是整体子区间，各列中位不可相加。最长GL帧中位1661.694→1639.666ms，GL运行CPU1512.780→1507.630ms；15ms总就绪差和微小分段差无法隔离调度、缓存、GC及顺序效应。保留修改的理由是去掉实证无必要的names数组转换/中间复制并保持语义，不能宣传明显提速，更不能用前批采样85.633ms减去本批差值。每轮解析恰1次、结果4625包，仍在GL；未声称异步化或重复文件读取。两组同一API28/4KiB/vivo X21A/b2a4da1c，原20宫格/图标/布局/设置，force-stop进程但OS/ART/磁盘缓存保留，2048KiB/CPU atrace；PAGE_READY先记录时钟再导出小JSON。不把am start/首帧当就绪、不把进程重启当首装。

**原生测试和负控：** 新增tools/tests/icon_preview/run_variant_tests.py，复用现有block提取/Java→D8→app_process，不新建生产系统。提取实际ensureVariantsMapLoaded、stripPng和getVariantsForPackage，真实Android JSON/TextUtils/流语义，Asset提供方受控；190场景24535检查含实际4625包全表、列表顺序、空/损坏/非数组JSON、null/空/混合值、大小写.png/重复值/空键、读取失败和关闭失败、重复调用只开流1次、调用方改返回列表不影响Map。names调用仅测试中计数，旧源码当前后版本负控在ART准确失败ASSERTION_FAILED candidate must avoid names array，非编译失败；正式源码复跑通过。包数从当前生成asset计算，避免为未来新增图标硬编码4625。额外现有run_resource_id_tests原生80检查覆盖真实resource identity/config/trim/races/live file/catalog/variants，未把受控Asset等同于完整ROM行为。

**正式交付：** build.bat构建、v1/v2/v3、P16、v1.5.8/code33及真实安装拉回哈希通过，非META-INF仅classes2.dex变更，assets和Manifest逐项哈希不变。IconPreviewRepository仅保留直接迭代的生产修改，LauncherStartupDiagnostics逐字节恢复；最终dex无variantsAudit/VARIANTS_AUDIT/smartisan-variants-20261023标记。候选及正式包各12静态区域与原包逐像素相同，排除动态时钟。正式5轮桌面设置/BACK、稳定downTime底部上滑搜索、settings输入提交、系统设置结果实际启动/返回均同PID20170，保存的5张查询/设置截图已人工核对；既有文件管理+日历文件夹开关仅功能验收，不重开Folder性能。设备UIA XML不可得边界保留，不捏造断言。PID AndroidRuntime日志无错误输出，但log.tag=E/persist.sys.log.ctrl=no限制保留；本批未开日志/工程模式。atrace最终0，本批专属JSON和shell probe文件已清理；无清数据/后台、权限、默认桌面、主题、刷新率或用户布局调整。134项index binary patch SHA256仍3619c27785b0898dc8d46da403e9f9380276a9b136ccb682e9359e5d4d3f83fb；没有add/提交/推送，项目及全局MEMORY未改。

<a id="2026-10-23-第十八批复用进程application消除首屏重复反射"></a>

#### 第十八批：复用进程Application，消除首屏重复反射

**10/23第十八批当前：已修复Context获取中的重复反射，Android9真机验收通过。** 复用前批五条系统trace确认最长首屏GL帧中位1722.248ms、运行CPU1589.886ms；在线图标线程该区间未运行，不把整段归为模型Worker等待。单独1ms方法采样定位currentApplicationContext反复getMethod，采样仅定位、不充当五样本性能数据。生产仅MaintainedLauncherSettingsHost.java：在现有入口以volatile复用成功的Application，保留原反射以及空值/异常/非Application Context的重试；不缓存Activity、Resources、配置或Bitmap，不新增Manager。实际方法提取后在ART受控反射Provider的216检查/8000暖态并发读取通过，旧源码负控准确失败。vivo X21A/API28原/新各5启动，GL阶段Context读取均375次，反射375→0；该段计时中位78.314→3.412ms，PAGE_READY2254→2207ms、最长GL帧1724.100→1667.255ms/运行CPU1567.050→1526.338ms。小样本差值含调度/缓存，不宣称整体冷启动解决。正式包五轮底部上滑搜索/settings结果实际启动/设置/返回、既有两项文件夹开关通过，同PID15918；修前/候选/正式包12静态区域一致。签名/P16/安装拉回哈希通过，非META-INF仅classes2.dex变更；最终SHA256=544608fcff0035ebc8e023bef9a9b3932d2575671e0e5614d4c6fdc670b24297。临时采样/计数代码恢复且dex无标记，应用专属测试文件清零，134项原暂存patch保持，MEMORY.md未改。证据build/startup-remaining-waits-20261023。

**下一项：** 只核对改进图variants.json首次解析在GL路径中的实际成本和已有预载入口，先用普通计数/区间验证采样提示，不能把单次受采样干扰的110.424ms当稳定耗时或收益；复用现有sVariantsMap，不再重复本批Context微任务。不得重开已否决最终磁盘缓存、无条件延后页或简单前移加join。Folder性能仍暂停，A22按用户确认关闭；本批未跑Android16/其他ROM/首装/长稳/真实16KiB，三星Share现场缺图未关闭。

**根因、原版与生命周期：** 当前兼容Host的currentApplicationContext每次Class.forName(ActivityThread)+getMethod(currentApplication)+invoke，来源类型/身份、合成及光照判断反复经过入口。真实计数每次GL首屏375次；缓存成功的进程Application后仍375次读取，GL反射0次，首次获取已在更早调用完成。原版clean_launcher/smali/com/smartisanos/launcher/ja.1.smali已有Jg:Application与getApplication；maintained的LauncherApplication也有mSelf，但不照搬其核心生命周期。当前入口保留原反射Owner以兼容已有调用，新增的单个volatile Application字段只持有本进程已有Application，避免新增Manager或Activity静态引用；空值/失败不负缓存，返回其他Context保持原行为且不保留。Application的Resources/locale配置仍动态使用原对象，未缓存资源/主题/用户选项。原APK归档仍缺失，没有声称本批重新反编译APK。生产新增8行，只改Host；测试新增tools/tests/icon_metadata/run_context_tests.py，复用已有提取block和现有Java→D8→app_process流程。

**五样本与计时限制：** 原PAGE_READY2314/2188/2254/2277/2217ms，候选2296/2207/2204/2173/2294ms，中位2254→2207。原Context区间78.733/78.314/78.559/74.663/75.864ms，候选3.372/3.594/3.356/3.412/4.266ms，均含相同临时计数器/线程判断/计时开销；不是正式包纯函数纳秒成本。每次force-stop进程、不清OS/ART/磁盘缓存、2048KiB/CPU atrace、保留原20宫格/图标/布局/设置；PAGE_READY在记录时钟后再写专属JSON。方法采样单独启动，采样无溢出，只找调用栈；其反射耗时不能替代普通计数对照。GL/来源/解码存在嵌套，不相加成收益；JSON没有绝对就绪时间，不伪造物理首屏或模型阶段绝对对齐。Context重复工作明确减少，但47ms总就绪差不全归因。

**原生反例与正式验收：** 提取真实currentApplicationContext方法，唯一受控替换是ActivityThread反射Provider；真实Android Application/ContextWrapper在API28 ART执行。覆盖早期null后成功、抛异常后成功、非Context后成功、普通Context不保留、100次重复身份和16线程共8000次暖态读取。216检查通过；该测试不验证各ROM隐藏API策略，实际应用安装/运行另验。首次负控因app_process未捕获AssertionError只得到Killed，未作为有效反例；调整测试输出后重跑旧源码，明确ASSERTION_FAILED successful application reused。正式生产源码再跑原生检查通过。最终构建、v1/v2/v3、P16、v1.5.8/code33、设备安装pm path拉回哈希通过，原/新非META-INF仅classes2.dex；诊断Startup类逐字节恢复，Context临时计数/方法采样标记不在最终dex。12静态图标区域原/候选/正式一致，排除动态时钟；五轮桌面设置/BACK、单downTime底部上滑搜索、settings提交和系统设置结果实际启动/返回均同PID15918，截图核对文本/图标，未伪造本机缺失的UIA XML。既有文件管理+日历文件夹仅功能开关，不恢复卡顿试验；使用权限/常用应用开关未改，不据此关闭三星Share。PID日志未见AndroidRuntime，但设备log.tag=E/persist.sys.log.ctrl=no限制保留，不冒称完整系统日志验收。atrace tags最终0，所有本批context JSON及采样trace已清理；测试前系统安装自动产生的一份13743 JSON也按本批精确文件名清理。没有进入工程模式、改日志开关、清后台或调整电池/默认桌面/刷新率。134项暂存binary patch SHA256仍3619c27785b0898dc8d46da403e9f9380276a9b136ccb682e9359e5d4d3f83fb；无add/提交/推送，项目及全局MEMORY未改。

<a id="2026-10-23-第十七批同次合成复用几何快照android9真机完成对照"></a>

#### 第十七批：同次合成复用几何快照，Android9真机完成对照

**10/23第十七批当前：已最小修复同次合成的重复几何解析。** 生产仅IconRasterDiagnostics.java：原composeTexture经NormalIconRasterSpec解析IconVisualMetrics后又直接解析一次，现将同一份metrics交给原spec构造逻辑；公共入口、空几何回退和全部物理字段保持，无跨帧缓存/Manager/Bitmap持有。实际合成/扫描/spec方法配合Android原生Bitmap，1010场景9093检查通过；旧源码负控准确拒绝仍2次解析。vivo X21A/Android9/API28真机原/新各5启动，每次31次合成的解析62→31，解析中位35.209→17.177ms、合成483.848→462.093ms；PAGE_READY2289→2262ms，小差值仍含缓存/调度，不宣称整体冷启动解决。正式包签名/P16/覆盖安装拉回哈希、12静态区域逐像素一致、5轮底部上滑搜索/settings结果/设置/返回与既有两项文件夹开关通过；同PID10769。最终SHA256=7c48aa93836f96e8323dffb6dea7ed66a88530c0b855bbda767e220c165d643e，非META-INF仅classes2.dex变化，所有临时计时/导出源码恢复且最终dex无标记，测试JSON清零。134项原暂存patch保持，MEMORY.md未更新。几何重复本项收口；下一项利用已存真机trace检查模型加载及首屏构建的剩余最长等待，不重拆几何/来源三查或重开已否决缓存。Folder性能仍暂停；三星Share、其他ROM、首装、长稳、真实16KiB等缺口保留。证据build/startup-geometry-snapshot-20261023。

**根因与参考：** resolveNormalIconRasterSpec(int)内部调用IconVisualMetrics.resolve，composeTexture随后再次调用同一resolve；后者含布局反射、Surface实际宽度、图标大小首选项及日志。不是图标画两次或GPU重复上传。当前Owner为现代兼容层，clean_launcher/maintained没有可直接替换的同名几何Owner；本轮对照既有Cell/Texture链，原APK归档仍缺失，未声称重新解包。新增的private重载只接受当前调用已有metrics，复用原构造表达式，不引入重复几何计算系统；int/public入口仍自行解析一次。未改layoutSize、百分比、素材、DEFAULT圆框、阴影、来源或绑定时序。

**原生证据与所有权：** 扩充已有tools/tests/icon_raster/run_bounds_tests.py，不新建并行测试框架。提取实际NormalIconRasterSpec类及两个重载、完整compose/report/scanner；源/geometry数据提供方、badge、projection与原阴影仍为受控Owner，真实Android Canvas/Bitmap逐像素比较。1010组9093检查覆盖现有alpha/随机/BitmapDrawable/不同来源、修前修后扫描次数不变、三个物理尺寸跨调用切换、Drawable bounds归还、借用源未回收、几何不可用返回原输入且只查一次、无图跳过几何。有效合成2→1；空几何1→1。旧源码同时充当前后版本的负控在实际ART失败于before=2/after=2断言，不把编译失败当有效负控。不是完整主题/横屏/全ROM矩阵，真实前台像素由真机另验。

**同条件真机五样本：** 仅使用已连接并由用户解锁的vivo X21A/b2a4da1c，Android9/API28/arm64-v8a/4KiB，1080×2280/480dpi，原20宫格、图标大小、两项文件夹和其他用户布局保留；已停止前批自己启动的模拟器。原PAGE_READY2385/2289/2477/2206/2257ms，中位2289；修后2439/2237/2262/2281/2245，中位2262。原几何次数每轮62/31次合成，耗时34.022/35.209/38.020/31.893/41.035ms；修后每轮31/31次，16.599/17.242/17.177/16.593/18.267ms，中位35.209→17.177ms。每次force-stop重启但不清OS/ART/磁盘缓存，同样2MiB/CPU atrace和临时计数/计时；没有整体模型/GL CPU分段收益归因，合成及解析是父子区间，不可相加。27ms就绪差不能全部归因，不与Android16模拟器/其他手机历史中位混比。

**采样失败与Android9边界：** 初始32MiB/CPU atrace缓冲分配失败，未计样本；改2MiB后成功。旧设备adb shell传输压缩atrace发生二进制损坏，改exec-out后调度数据有效；损坏探针保留并排除。首个应用Trace诊断包在该ROM/当前配置下只取得系统事件，未出现LAUNCH/AUDIT标记，缺失原因未完全确认；baseline-1保留但不计5次，未设debuggable/profileable、未改Manifest或开启系统日志来绕过。最终配对诊断复用LauncherStartupDiagnostics现有Context，在public PAGE_READY回调记录时钟后写应用专属目录小JSON，只含PID、就绪耗时、合成/解析次数与纳秒总量；计数按当前合成ThreadLocal作用域，AtomicLong汇总，不保留几何/Bitmap。文件写入不计入已记录的就绪耗时，不冒充首个可见buffer或物理屏幕时刻。baseline-file/candidate-file才是有效10样本，各PID文件及时回读后删除，最终确认0残留；这些诊断字段/方法已从正式源码及dex全部删除。系统persist.sys.log.ctrl始终no、log.tag始终E，atrace标记测试后0，未进入工程模式或清理后台。

**正式包验收：** 保留IconRasterDiagnostics的7增/4删生产变更；IconVisualMetrics与LauncherStartupDiagnostics逐字节恢复本批前状态。构建、v1/v2/v3签名、P16 zipalign、aapt2 v1.5.8/code33、安装pm path拉回SHA256通过；非META-INF ZIP只有classes2.dex变更。修前第5次/修后第5次/正式包12静态图标区域完全一致（排除时钟）；正式首次就绪以相同区域出现真实像素为门，未把am start第一帧当PAGE_READY。五轮桌面设置/BACK、单downTime底部上滑搜索、输入并提交settings、结果图标和系统设置实际启动/返回均同PID；此API28 uiautomator未给出XML，查询文本/图标以保存的5张截图核对，未伪造XML断言。既有“文件管理+日历”文件夹仅开关功能与截图，未改用户创建布局，不恢复Folder卡顿试验。原常用应用/使用权限未改，不据本轮关闭三星Share缺图等现场缺口。最终metadata脚本发现旧系统无getconf，改读/proc/self/smaps的KernelPageSize为4kB；这不是Launcher错误。全局及项目MEMORY不改，134项原暂存binary patch哈希仍3619c27785b0898dc8d46da403e9f9380276a9b136ccb682e9359e5d4d3f83fb，无add/提交/推送。

**下一项：** 本次重复几何解析及其原生/真机验收已收口；不得继续拆同一微任务。下一项先复用已保存真机系统trace，定位模型加载与首屏构建中剩余最长主线程/模型Worker等待，再决定是否有必要修复。已否决的最终磁盘缓存、无条件延后页、简单前移加join不重开；内存清理后恢复的A22返回现象不再复测。总体冷启动、跨ROM、首装、长稳和真实16KiB尚未关闭。

<a id="2026-10-23-第十六批定位静态节点构建耗时排除把整段归因gl上传"></a>

#### 第十六批：定位静态节点构建耗时，排除把整段归因GL上传

**10/23第十六批当前：耗时定位完成，生产逻辑净改动为零，冷启动未解决。** 当前无真机连接；复用第十五批真机五份trace，解码区间去重中位169.250ms/运行164.903ms，不能解释1065.776ms整帧。另在已有API36只读模拟器/host RTX3060做5次分段诊断，PAGE_READY3479/2468/2185/2496/2392ms，中位2468；静态节点构建中位1153.187ms，而GL位图上传23.637ms、文字23.358ms。单次细分确认静态合成507.151ms、来源307.359ms、准备143.175ms、键135.944ms；圆框127.220ms含在准备阶段，Alpha扫描62.282ms含在合成阶段，均不可重复累加。该单次不是五样本性能收益，更不能与真机1286ms混比。没有证据支持删除原版绘制/上传，本轮不交付臆测修复。9份临时源码逐字节恢复，重建包全部非META-INF成员与本轮原包相同；正式SHA256=4806115c3ea2b32336497c1b3b5857fcd79ed8089a159c7e2abc6d9ad85ca18f，签名/P16/覆盖安装拉回哈希、13静态区域及5轮搜索/设置/返回通过。第5轮ADB中断后同PID重跑，前4轮与中断证据保留。134项原暂存patch保持，MEMORY.md未改。下一项只核对composeTexture中NormalIconRasterSpec和IconVisualMetrics的同次重复几何解析，量化后考虑复用同一快照；不重开来源三查/旧阴影提取/最终磁盘缓存/无条件页延后实验。证据build/startup-cell-content-20261023。

**范围与参考：** 在第十五批之后保留最新P10/API24现场修复，不退回旧版源文件；本轮开始暂存已为134项，其patch SHA256为3619c27785b0898dc8d46da403e9f9380276a9b136ccb682e9359e5d4d3f83fb。原包415e8643…已保存。对照clean_launcher的g.Ba/ca/ga.create与maintained Cell.createNode/createDisplayRect/Utils.loadIconToTexture，原APK归档本地仍缺失，未声称重新解包。maintained旧成品图解码不等价于当前RAW/圆框/阴影合同，没有整块搬运。真机不存在时采用用户已授权的Android16模拟器；Pixel_6_Pro只读/no-snapshot/host GPU，原1080×2400/480 override保留，API36/x86_64/4KiB。未改主题、数据、默认HOME、权限、刷新率或设备密度。

**方法与调用链：** 临时在g.create、g.Ba(kind)、ll、Zx、ca/ga.create、P.texImage2D/glTexImage2D及既有Java Owner内分段；不改变Drawable选择、Bitmap所有权或绘制顺序。五样本沿用force-stop进程重启、保留OS/ART/磁盘缓存、相同10秒Perfetto/LAUNCH_PAGE_READY；不是首装。AUDIT_CELL_CREATE记录49次进入，但内容体24普通格+1 Dock、其余iH门禁返回，不是49次重复构图。NODE_0为22个静态图标，NODE_1为22个文字；57次GL Bitmap API调用覆盖图标、文字与已有其他资源，未据总数臆称重复上传。上传时间是GLUtils调用返回的CPU/driver区间，不是硬件GPU全部执行/屏幕呈现。

**细分与归因：** 五次GL构建帧wall2420.662/1556.029/1343.372/1581.485/1643.381ms，中位1581.485；NODE_0 wall1153.187/运行726.195ms，NODE_1 wall23.358/运行15.693ms，GL Bitmap上传wall23.637/运行17.800ms，边界计算wall0.686ms。Zx22次和sync/shadow各88次多为无动态Root的检查；本AVD未验证真实原版天气/日历实例，不扩大为动态图标性能结论。补充细分仅1次，PAGE_READY2388ms、整帧1733.172ms，不作为候选收益/五样本中位：合成507.151/运行368.761ms、来源307.359/141.947、准备143.175/105.162、键135.944/55.506；圆框21次127.220/100.469ms在准备内，Alpha44次62.282/32.683ms在合成内，source hash仅1次0.519ms。前两普通页原阴影细项合计233.941ms也包含在合成内；不能再与其父区间累加或把未覆盖项全算GPU。由此排除本设备上“主要卡在纹理上传/文字创建/来源hash”的归因，主路径仍为静态来源获取及软件合成。未发现本批可直接安全删除的重复绘制。

**失败与回归边界：** 细分脚本初次遗漏re导入，未写入细分标记；该次无标记重建保存在build-fine-uninstrumented.log，未进入fine采样。修正后实际标记存在，fine-1单独保留。正式功能第1～4轮完成后ADB连接中断，第5轮未完成；保留functional-first-four-before-adb-interruption及interrupted-round5，恢复连接后仅重跑第5轮，PID6168未变。五轮均验证桌面设置/BACK、同一downTime底部上滑搜索、提交settings（文本trim后准确）、结果图标与系统设置启动、返回。第3轮设置截图含转场缩放，不能当静态视觉一致性证据；第5轮稳定设置图可核对。13个首屏静态区域按baseline-5与最终桌面逐像素一致；未启用原先关闭的常用应用，也无Share/文件夹/真实动态实例回归，不据此关闭这些设备与路径缺口。

**交付与下一项：** build.bat成功，v1/v2/v3、P16、aapt2 v1.5.8/code33及pm path拉回哈希一致；9个临时源码全部逐字节恢复，最终dex不存在本批AUDIT_CELL_/AUDIT_STATIC_标记，非META-INF ZIP成员全部与415e8643…原包一致。容器重建SHA变化不代表生产功能改变。远端临时手势/采样文件清理；MEMORY.md与全局memory不改，不add/提交/推送。五样本+1细分完成的是本次定位，未完成冷启动优化验收。下一项的具体代码线索为composeTexture先由resolveNormalIconRasterSpec调用IconVisualMetrics.resolve，又直接调用同一resolve；该重复已从源码确认，尚未量化耗时，应先计数/量化，再在同一调用内复用，不能引入跨帧几何缓存或重开Folder性能。Android9/真机/全ROM/首装/长稳/真实16KiB仍待对应验证。

### 2026-10-22

<a id="2026-10-22-p10android-70-现场启动阻断低密度资源与文件夹背景"></a>

#### P10/Android 7.0 现场：启动阻断、低密度资源与文件夹背景

**范围与当前结论：** P10/API24/armeabi-v7a，实际屏幕与 GL activeBuffer 均为 800×1280、210dpi，SurfaceFlinger 矩阵为 1:1。修复两个已复现启动阻断；保留用户数据，按用户选择保留12宫格，并通过原设置页将图标调为-20/80%。文件夹边缘露桌面已实机复现并修复。此批是旧系统现场兼容，不是整体启动性能验收，也没有扩大 Android/ROM 支持声明。

**启动与原版边界：** `DatabaseHandler → d.j.Pf → ShortcutQuery.setQueryFlags` 在API24抛出 NoSuchMethodError；该旧核对还会删除未查询到的Shortcut，故复用已有 `ShortcutCompatBridge.suppressLegacyPf`，API25以下整个跳过，保留API25旧路径和API26以上原有抑制。继续启动后，GL线程在 `DefaultIconCircleRenderer` 的 AdaptiveIconDrawable 类型判断抛出 NoClassDefFoundError；三个判断均补API26保护，旧系统走原有普通Drawable绘制。对照clean_launcher的旧Shortcut查询及maintained源码；本地原版APK归档缺失，未声称重新解包或原版同机A/B。

**文件夹：** `FolderSceneMetrics` 为书架/标题/内容提供的安全区根变换，连同其子节点全屏背景一起缩小，P10四周露出桌面。仅在原 `t._r` 背景Owner中按已有sceneMetrics逆变换背景quad；F.a原以半宽/半高设置scale，本次由完整viewport及根scale重新推导，避免累乘。保留书架、标题、内容和裁剪、开关动画，large-screen原分支不进入此修复；P10截图确认原书架位置不变且背景覆盖边缘。

**设置资源与本轮纠正：** 前期错误地把背景差异当成控件/高度问题，曾临时改通用行高、模板、分组并安装候选。用户指出手机正常、不得乱改高度后，已撤销这些候选：SettingItemTextVertical、SettingItemSwitch、attrs/styles及六份设置页XML恢复本批开始index原始字节，设备也恢复原布局包，再做密度探针。运行时确认210dpi选择了xhdpi普通PNG `sub_item_back_ground_single`，而正常分组行是NinePatchDrawable。最终只在build.bat既有资源暂存中排除三份同名普通PNG，让原选择器使用已有xxhdpi原版9-patch。旧/新资源APK仅resources.arsc及删除的三个错误变体不同，既有XML/字体/高度未变；480/640dpi配置输出相同。不能将候选改行高描述为交付修复。

**完整资源核对与位图清晰度：** 扫描42份设置相关布局、26种直接背景，检查全部资源中普通PNG/9-patch同名冲突，仅上述三项；P10上的原生Resources/Drawable探针覆盖210/320/480/640dpi、按下/禁用/普通状态、intrinsic尺寸及About ImageView测量，共484检查通过。这是资源/测量覆盖，不是42页逐项交互验收。About标志确为maintained中的原1080×556整图，原centerCrop布局也相同；210dpi常规解码先变473×243，再显示到全宽。时钟实际选择RESOURCE:clock，原192×192在解码后仅84×84，绘制到123×123。复用IconBitmapDecoder增加仅对密度缩小的普通位图保留原像素的入口，接入已有资源图标Owner、Repository内置资源和About标志；不改PNG、9-patch、XML/vector选择、intrinsic布局尺寸或用户来源。新增About图片ID仅用于绑定高清解码，不改layout参数。该入口不另建缓存；保留原像素会增加瞬时解码内存，未完成低内存/长稳专项。

**图标链路的已证与未证：** 临时复用原栅格诊断及GL回调，源码结束时逐字节撤回。图库/日历/系统设置实际IMPROVED源512×512→123×123 artwork→157×157纹理；旧/新123px合成图逐像素相同，不能称这些图标也因本改动变清晰。时钟资源修后保留192×192，artwork仍123×123，消除SOURCE_LIMITED；音乐实际RESOURCE来源192，未按全局开关臆称每个图标都是IMPROVED。SC0实际local scale约78.72（宽157.44），Cell scale=1；world rect探针为空，未伪称取到world bounds；SurfaceFlinger实际800×1280/1:1排除系统整体放大。素材透明留白本身不同：本地时钟宽约76%、音乐约77%、通讯录约96%，不据此按包加倍率/裁边。未重写统一几何、未再次应用用户百分比，也不宣称所有主观模糊已解决。

**验证与边界：** build.bat、签名v1/v2/v3、P16 zipalign及保数据覆盖安装/拉回哈希核对；启动修复包与后续正式包做过三次进程冷启动、应用打开/返回、文件夹开关、设置页/原图标调整检查。原生圆框API24共43检查、API36共59检查通过；旧renderer在API24的缺类负控准确失败。资源与原像素入口另有484原生检查及实际时钟前后采样。手机后续断开，480/640dpi是P10上的配置探针，不冒称手机About/所有设置页视觉验收。API25、其他旧ROM、全部主题/横屏/长稳仍需对应现场。证据集中在build/android7-startup-20261022（before/after崩溃、原生探针、截图、临时诊断及最终交付记录）；项目MEMORY.md与全局memory均未更新；原暂存区保持，不add/提交/推送。

**正式交付复核：** 最终v1.5.8/code33包SHA256=`415e8643005b615b2a10eea94ef5637edfda4fc88bef641e0353d05b805cdbb0`，安装拉回逐字节一致，v1/v2/v3和P16通过；三个临时诊断源码逐字节恢复，远端本批诊断文件及空目录清除。十份曾错误改动的设置控件/布局/attrs/styles与本批初始index逐字节一致，About XML仅增加图片绑定ID。最终三次启动均等待图库可见区域出现真实图像并保存截图；检测耗时约10.49/10.59/10.58秒，含ADB截图采样开销，不能当精确首帧/性能收益。早期仅等3秒的Activity前台检查截到黑屏，未当成可见就绪验收；冷启动仍慢，未宣称本批解决性能。正式文件夹截图无边缘露桌面，系统设置打开/返回、About页和图片绑定已验，最新crash buffer无AndroidRuntime项；原暂存binary patch哈希保持。全量设置检查指资源路径/类型/测量合同，不等于所有设置功能、手机或多ROM完整通过。

<a id="2026-10-22-第十五批静态绘制复用同次来源快照保留缺失别名回退"></a>

#### 第十五批：静态绘制复用同次来源快照，保留缺失/别名回退

**10/22第十五批当前：静态合成的来源/类型/身份改为复用同次快照。** 生产仅IconRasterDiagnostics.java与MaintainedLauncherSettingsHost.java，复用已有ManagedIconSource和来源解析Owner；未引入跨调用缓存、Bitmap持有、线程或数据协议，纹理键与合成仍各解析一次。实际方法+Android原生Bitmap的480键场景/480合成场景共2631检查通过；自定义图完整key+compose链的文件解码/重编码5→2（不代表全部内存PNG解码），改进图来源请求3→2，缺失图仍保留晚到复查；旧源码负控准确失败。Android16真机V2458A同条件各5启动PAGE_READY中位1321→1286ms，GL构建帧wall1093.780→1065.776ms/运行CPU1002.108→976.637ms；未隔离缓存/顺序/调度，不能将35ms全归因或宣称冷启动解决。首屏13静态区域像素一致，首次8页往返无>50ms GL帧；正式包五轮图标/底部上滑搜索/准确settings查询/设置与返回及文件夹开关通过。最终SHA256=c4b70eb3d537921cabb4982559c82f3931e4f9ebc3217fd0061e8f17b10cd9c0，签名/P16/安装拉回哈希通过，仅classes2.dex变化，临时Trace逐字节恢复，129项暂存patch保持，MEMORY.md未更新。下一项定位首屏GL剩余约1秒中CELL_CONTENT_CREATE的资源解码/纹理创建实际调用，先细分归因，不再重复本批来源快照、磁盘缓存或无条件延后页实验。Folder性能仍暂停；Android9/三星Share/全ROM/首装/长稳/真实16KiB缺口保留。证据build/startup-compose-source-20261022。

**根因与原版边界：** 上批仅修e.s当前纹理键门禁；本批确认静态绘制仍依次查询type、identity、Drawable，自定义图的Redirect读取会实际执行文件PNG解码及重编码。clean_launcher/maintained的旧成品解码不是当前高分辨率RAW/圆框合同，不能直接替换。本地原版APK缺失，本批参考现有clean_launcher与maintained源码，没有声称新解包或原版同机A/B。

**最小修复：** 将已有desktopSourceForTextureKey的解析核心复用于desktopSourceForComposition；在resolveStaticSource内使用同一次ManagedIconSource的Drawable、desktopType、desktopIdentity。user0、精确Activity及精确Redirect才可直接采用Drawable；无精确Redirect保留单Activity别名回退，missing/late仍让原loader重查。显式DEFAULT类型仍在PM前确定；准备好的DEFAULT圆框不接新快照；分身/组件不符/上下文缺失走原查询。无来源/选项/Bitmap跨调用保留，不改阴影、几何、颜色分类、所有权或键协议；key和绘制并未合并成整个调用图一次读取。

**计数与反例：** counters顺序为redirectReads/fileDecodes/pngEncodes/managedLoads/pmCalls，基线同时对照无改动源码，两边相同。修复CUSTOM完整key+compose由[5,5,5,0,2]至[2,2,2,0,2]；IMPROVED[6,0,0,3,3]至[2,0,0,2,2]；缺失来源[9,0,0,6,5]至[8,0,0,6,5]，保留复查。key单独计数不变。480组键+480组合成/2631检查包含模式/全局选择/可用性/pack/profile/组件/实际原生像素和借用源存活；PM、来源选择和几何是受控夹具，并非安装应用IO全量埋点。fileDecodes只计readCustomBytes实际文件解码，不能漏掉未计的byte-array内存解码而声称全部PNG5→2。旧源码负例失败在CUSTOM两次文件解码断言，作为有效负控保存。记录型compositor的借用/准备源检查282/未缓存311通过，不冒称真实GL；完整UI像素由真机另验。

**真机五样本：** 同一V2458A/Android16/API36/arm64/4KiB，既有1260×2800/12宫格数据，force-stop进程启动，OS/ART/磁盘缓存保留，相同10秒Perfetto。原1321/1329/1324/1313/1273，中位1321；修1313/1280/1247/1294/1286，中位1286。原第4/5、修第3/4轮日志marker缺失，以配对临时LAUNCH_* Trace补齐，不丢弃或伪造样本；persist.sys.log.ctrl始终no，未进入工程模式。GL运行CPU中位1002.108→976.637ms，binder区间71.022→63.019ms，decodeBitmap87.556→87.335ms，不能相加嵌套区间或把全部差值归因本改动。修第1轮前两页SOURCE_SNAPSHOT共17次，SOURCE_DRAWABLE余1次；对照原type/identity/drawable各17次，说明实际快路径生效16次，未证明所有67图均具相同计数收益。

**正式验收与范围：** 相邻原第5/修第5轮13静态区域逐像素一致（排除时钟/日历动态区域）；首次前8页/后8页原最大12.60ms、修17.42ms，均无>50ms onDrawFrame，不等于全GPU呈现时间。临时Trace已逐字节移除，build.bat、v1/v2/v3签名、P16 zipalign、aapt2 v1.5.8/code33、最终保数据安装及pm path拉回哈希通过；非签名ZIP只classes2.dex不同。正式包5轮设置/BACK/底部上滑搜索/准确settings查询/结果图标与系统设置启动/返回均同PID；既有文件夹3图标开关仅功能验收。未改主题、刷新率、默认HOME、权限、用户布局或清理后台/应用数据；PID限定日志未见AndroidRuntime异常，不扩大成全ROM稳定性。保留129项原暂存，未提交推送，项目与全局MEMORY均未改。两个现有测试脚本随实现扩充，没有新增生产Manager/缓存/Service。

**后续：** 本批来源解析收口；冷启动仍开放。下一项只细分CELL_CONTENT_CREATE内的资源解码/纹理创建，定位剩余GL CPU；不重复已经否决的磁盘缓存/无条件页延后/单纯前移加join。Folder性能暂停、Android9、三星Share、首装、长稳、全ROM和真实16KiB仍需对应设备/路径，不算本批完成。

<a id="2026-10-22-第十四批否决最终纹理磁盘候选修复过期版本门禁的重复解析"></a>

#### 第十四批：否决最终纹理磁盘候选，修复过期版本门禁的重复解析

**10/22第十四批当前：最终纹理磁盘候选已否决，过期纹理键门禁已最小修复。** 在Android16真机V2458A完成原/候选/空缓存/反向原/门禁修复各5样本。磁盘候选稳定命中67张时PAGE_READY中位1183ms，但受控空缓存1423ms，初始原1339ms、反向原1351ms；首次无缓存更慢，因此撤回全部缓存生产改动并清理测试文件，不再将这条路线作为当前首启优化推进。另确认e.s入口仍硬编码v18，当前Java已v30，导致完整纹理键被重复生成；改为调用Java唯一版本判断，普通/过期键仍构建，保留调用方已解析的当前键。实际入口Smali前缀18检查与旧分支负控通过，有完整日志样本键生成138→70；修后5启动1341/1288/1308/1265/1313ms，中位1308，较相邻修前1351约少3%，不能将整个差值视为已完全隔离的代码收益。最终正式包五轮图标/底部上滑搜索/准确settings查询/设置/返回及文件夹开关通过，首次8页往返无>50ms GL帧；修前反向原/修后13个静态区域像素一致。最终SHA256=59031d278cf0c08f345731399d84376bfd362f7862df5766a14e41c4df1393d4，签名/P16/安装拉回哈希通过；永久生产仅e/s.smali与IconRasterDiagnostics.java，本批无新缓存/线程池/数据协议，临时诊断与持久化Owner逐字节恢复，129项暂存patch保持，MEMORY.md未更新。整体冷启动仍开放；下一项核对跨纹理键生成与正式合成的重复来源解析，区别于本批入口门禁、先计数再最小修复，不重复磁盘缓存实验。Folder性能仍暂停；Android9/三星Share/全ROM/首装/长稳/真实16KiB未验。证据build/startup-final-cache-20261022。

**参考与范围：** 延续第十三批协议准入，在当前Owner中制作候选，没有照搬maintained旧iconData/clean_launcher的三列成品，也未将旧PNG解释为RAW。原版APK本地缺失，沿用clean_launcher和maintained源码对照。候选只允许已有普通静态管线、user=0、itemType=0；动态包、特殊入口、文件夹mode8、多用户、光影、失效来源以及未知Drawable走原链路。未启用模拟器，不修改真机主题、默认HOME、刷新率、使用情况权限或系统日志；persist.sys.log.ctrl开始/结束均no。设备Android16/API36/arm64-v8a/4KiB，既有1260×2800与12宫格；真实16KiB不在本批覆盖。

**已撤回的缓存实现：** IconPreviewRepository内有界64条/8MiB最终Bitmap副本，持久化复用既有onlinePool、串行drain，并在真实onLauncherPageReady后释放，不新增线程池；GL结果和Drawable的Bitmap不被Worker保留或回收。文件codec为FINAL表示、SHA256完整键文件名、头部身份/尺寸/长度/PNG SHA256、解码前bounds校验、同目录临时文件sync后Os.rename，磁盘64MiB逐出。实际来源像素和BitmapDrawable原生绘制分别摘要，覆盖隐藏常量tint，继承完整几何、阴影、圆框和渲染版本；应用安装路径变化也拒收旧构建。旧队列拒绝/满额不重试或阻塞，缺失/损坏回原合成。该方案实际需要额外来源扫描/绘制/解码，是本轮被否决的候选，不是当前生产架构。

**协议/所有权证据：** 独立app_process真实Android Bitmap/文件codec与提取的实际Repository队列方法56检查，第二进程3读回；准入方法27检查含常量tint、ARGB +1/-31碰撞、来源/边界排除和bounds/输入所有权；调度、PackageManager和几何键仍是受控夹具，不能冒称完整并发/全ROM/存储故障UI矩阵。移除文件键身份校验的负控准确失败在头部身份被破坏；原借用源cached274/uncached311检查仍通过（其最终compositor为记录夹具，本轮显式绕过磁盘，文件/准入由另外探针验证）。提取复用后的完整键方法与旧版480场景/1684检查、两个ART进程核对通过；没有宣称旧32位纹理摘要变为持久化强摘要。

**保留失败原型：** v1追加完整Configuration字符串，真机含非语义配置序号s.…，两次1520/1481ms均67 miss；该原型有跨进程键不稳定，不能把它的未命中当最终缓存收益。v2复用现有渲染键生成函数并直接接收本次来源强摘要，去掉序号和重复来源重读。v2新安装初次1473ms，67 miss/24 saved/43 cap；后两次1356ms（24 hit/43 miss/25 saved/18 cap）、1255ms（49 hit/18 miss/18 saved），这三轮是有界缓存建立过程，未混入稳定五样本。

**同条件有效五样本：** 同一真机、同一数据/布局/设置，force-stop进程启动，OS/ART/磁盘缓存保留，均相同10秒Perfetto；有配对的临时LAUNCH_*应用标记补偿vivo日志缺失。初始原1326/1335/1357/1339/1355，中位1339；稳定候选1170/1191/1183/1192/1175，中位1183，5次各67 hit。另用临时审计入口仅删除本次final_icon_v1文件，在begin计时前清理后制造受控空缓存：1434/1426/1418/1418/1423，中位1423，每轮67 miss/24 saved/43 cap。不是实际首装、物理首次开机或清除ART缓存实验，清理开销不计入PAGE_READY。反向原1351/1369/1350/1343/1365，中位1351。稳定缓存约快12%，受控空缓存约慢6%，不符合当前首次加载目标，故全部缓存生产代码撤回，停止此路线而非继续细化缓存微任务。

**独立最小修复及根因：** 在回退核对中确认g.1/la调用方已产生当前v30完整键，e.s.a(ItemInfo,String,boolean,int)却仍用#raster:v18-icon-contract:判断。当前键被重建、再次解析来源/计算摘要；过期v18反而被误认为ready。新增IconRasterDiagnostics.hasCurrentTextureCacheKey作为唯一版本Owner，2参纹理键API也复用该判断；Smali入口调用它，保持原版已完成键直接复用的意图。普通base或其他版本仍按既有显式pageMode生成；调用方负责场景模式和来源失效重建，保留共享Folder/Active后缀不被二次剥离。本批不新增合成算法，不改Bitmap所有权，不改原始强制重载开关，不宣称解决其他跨key→绘制重复解析。

**门禁验证及实际收益边界：** run_entry_key_tests.py原样组装实际e.s入口前缀（停止在既有cache lookup之前）与实际Java版本谓词，在ART完成18检查；来源生成是计数夹具。四类当前键原来各重建1次、修后0，raw/v17/过期v18仍1次，1/8/9/12/20调用方表示与null保护验证；将After替回旧入口，负控准确在current key reused断言失败。完整实际日志中修前138、修后70次ICON_CACHE_PIPELINE_KEY（修前有日志漏采，不把0算作真实计数）；完整键矩阵480场景/1684检查×2进程仍通过。修后真实五次1341/1288/1308/1265/1313，中位1308；相邻反向原1351，约少43ms/3%。相邻原/修后GL场景构建帧中位1139.756/1091.143ms，scheduled CPU1040.257/995.421ms，binder切片79.655/70.522ms；解码86.914/86.706ms几乎不变。计数减少和版本逻辑修复可确认，DVFS/缓存/轮次等未全隔离，不能把整个43ms归为唯一代码收益，更不能称整体冷启动已经解决。PAGE_READY是逻辑页面就绪，不是录屏/SurfaceFlinger物理首帧。

**功能、像素与环境恢复：** 缓存候选与最终正式包各五轮桌面设置BACK、底部上滑自绘搜索、XML核对准确settings、结果图标启动系统设置、BACK加明确回桌面通过；正式包PID828稳定，限定PID AndroidRuntime日志为空。未打开常用应用开关/增加权限，未覆盖三星Share或Top5特定场景。普通首次向前8页/返回8页：初始原约10.94–13.09ms、缓存候选10.16–12.86ms、门禁修后9.99–12.58ms，各窗口均无>50ms onDrawFrame；不是完整展示帧率或Folder性能验收。最终现成3应用文件夹tap/BACK、截图显示翻译机/对讲机/联系人均有图标，未移动布局；Folder卡顿专项仍暂停。最初基线/缓存候选13静态区域一致；最初基线/门禁修后12/13，差异是企业微信20角标，它在修前反向原中已消失，保留该非等价证据，不冒充13/13。反向原/门禁修后13/13逐像素一致。测试UI截图与final-functional-review.png已人工核对。

**清理、构建与交付：** 缓存源/Owner和诊断文件快照对比证明：IconPreviewRepository和LauncherStartupDiagnostics均逐字节恢复本批开始状态，FinalIconTextureFile.java从launcher移除；仅证据目录保留已否决源码与APK供复核。缓存清理两次Trace分别count=24与count=0，第二进程证明已无本轮匹配文件；临时清理Intent和LAUNCH Trace钩子均未进入正式dex。正式build.bat、签名v1/v2/v3、zipalign-P16、badging v1.5.8/33通过；APK与本批前aa336816…相比非签名ZIP仅classes.dex/classes2.dex变化，资源/Manifest/native完全相同；临时类/FINAL_DISK/清理入口字符串均不在最终dex。最终APK SHA256=59031d278cf0c08f345731399d84376bfd362f7862df5766a14e41c4df1393d4，安装后pull的base.apk相同。系统日志保持本次开始的关闭状态，未进入工程模式；设备停回原桌面，探针DEX/XML/Perfetto配置/trace远端文件清理。本批保留2个生产文件改动、3个测试脚本及既有2套夹具适配，5份既有报告更新；原129项暂存patch SHA256=f386b4d82f1c0e7b26f84785e81133bf2727697781140da6a3e6f782ec700d1e保持，无add/reset/提交/推送。MEMORY.md未更新。

**下一项：** 只调查当前纹理键生成→正式合成之间是否仍重复解析同一来源，尤其resolveStaticSource的类型检查/正式Drawable路径；先建立同Cell/同图的实际调用与IO次数，再用调用内既有来源快照最小复用。区别于已完成的“键内部hash/type/identity复用”及本批“入口版本门禁”；不再重测A22内存回桌面、不再无条件延后页面、不再继续磁盘缓存。整体首启、首装、其他ROM/Android9/三星Share/长稳/真实16KiB缺口仍开放。

<a id="2026-10-22-第十三批跨进程缓存协议准入与失效负控"></a>

#### 第十三批：跨进程缓存协议准入与失效负控

**10/22第十三批当前：缓存持久化准入核对完成，未上线缓存改动。** 提取现有来源解析/纹理键方法，在API36只读模拟器两个独立ART进程各跑480组/1684检查，圆框、透明主题、逻辑/物理尺寸、surface、geometryRevision、宫格、分类、阴影、光影、用户及既有来源替换规则通过；相同安装元数据跨进程键一致。删除圆框区分的负控按预期失败。实际Android Bitmap构造出不同像素但相同32位摘要的反例，非Bitmap颜色改变也未进入类名/尺寸/身份摘要，故禁止直接将当前进程纹理键当作持久化完整性协议。旧三列为带阴影成品，data1～3还参与快捷方式备份/恢复，不因当前为空就占用。未改生产源码/APK/DB协议，没有新五启动或安装/功能回归，也不声称提速；冷启动仍未解决。下一项只做既有Owner内版本化最终PNG磁盘候选：先证明来源强身份、表示/版本、负载SHA256、原子发布、容量与恢复失效，再决定接入；不得先把旧PNG当RAW。证据build/startup-cache-validity-20261022，正式APK仍aa336816…，129项暂存patch未变，MEMORY.md未更新。真机/Share/全ROM/长稳/16KiB缺口保留。

**本批修改：** 仅扩展tools/tests/icon_metadata/run_key_source_device_tests.py的可选--validity-matrix；保留既有480场景，增加可变几何/圆框/主题等受控输入、真实ARGB像素碰撞与非Bitmap反例、两个新ART进程相同元数据键核对，并在finally清理本次dex/PNG。解析/键函数从当前源码提取，Android Bitmap为原生；PackageManager/来源调度/设置和几何是夹具，不代表整机来源广播或真实UI切换均通过。常量版本在夹具中是占位值，本批未证明版本变更后的旧磁盘文件清理。

**证据与边界：** key-matrix-verified/result.log与fresh-process.log各1684检查；negative-matrix/result.log及negative-control.log定位到circle preference invalidates DEFAULT。负控只改build证据目录内的候选副本，不改生产。32位反例是在同一不透明ARGB行的两个像素分别+1/-31，实际getPixel确认改变而完整纹理键不变；ColorDrawable在相同来源身份/尺寸下改变颜色也不改变键。这证明它不是磁盘字节完整性摘要，不证明该碰撞曾导致用户图标故障，也不要求为本批审计扩大热路径耗时。相同元数据键的跨进程一致性只是身份稳定，未写入或恢复最终纹理。

**复用边界：** 当前ItemInfo.Oe/旧IconDB持有主题成品；clean_launcher同样保留三列与data1～3，maintained IconDB以已准备iconData解码，不能直接替换当前高分辨率RAW/圆框合成。ShortcutIconBackupCodec导出与恢复data1～3，LayoutSnapshotImporter会删除重建table_icons，因此持久化候选必须明确与恢复、源重选、卸载/替换、主题/圆框/尺寸变化的失效契约。原版APK文件当前不在本地，未新增APK二进制对照。

**下一项验收约束：** 复用IconPreviewRepository的既有持久化Worker所有权，先评估版本化最终PNG候选，不另建RAW Bitmap缓存/线程池或占用旧三列。须具备强来源身份（不只当前32位摘要）、显式FINAL表示与渲染版本/完整几何键、文件长度和SHA256、同目录临时文件原子发布、有界磁盘容量，以及写中断/损坏/来源变更/恢复后拒收证明；不满足则原链路即时生成。动态/特殊/多用户边界未证实前排除。准入后才接入GL既有消费点，做相同条件原/候选/反向原五启动和图标/搜索/设置及首次翻页回归；首次安装无缓存的收益必须单独报告。当前仅完成协议审计，尚未实现该候选，不能将启动问题标为解决。

**验证/恢复：** 本轮未改生产，不重建或安装APK，不重复无变更五启动。verification.json核实正式APK SHA256=aa336816dd9bb78b0af196bb13a20cc46fd83fad4bccaa5f06340453c4a1ec72，暂存129项/patch SHA256=f386b4d82f1c0e7b26f84785e81133bf2727697781140da6a3e6f782ec700d1e。独立探针文件已清理，关闭本次只读AVD，不改底层AVD和真机状态。MEMORY.md未更新。

<a id="2026-10-22-第十二批图标数据库结果误报修复跨进程缓存边界核对"></a>

#### 第十二批：图标数据库结果误报修复，跨进程缓存边界核对

**结论：** 现有异步补写经 e.s.a(ItemInfo,true)→Aa生成ContentValues→data.a.h.a→data.a.e/V.execute，确实具备数据库写入路径；MD5一致时可直接取得既有成品而跳过写入。读取方 ItemInfo.Oe / IconDB 按主题列恢复private iconData，未建立带当前来源/尺寸身份的跨进程RAW协议。不能把这点直接称为“写库丢失”，也不能把旧dark/light字节直接塞进iconRawData以求命中。本批修的是独立的失败误报，不是冷启动优化完成。

**确认的继承缺陷与最小修复：** 当前、clean_launcher、maintained IconDB事务都忽略SQLite insert/update返回值，非抛异常的insert=-1或update=0最终仍写result.b=true。只改data/a/e.run：更新至少命中1行、插入行ID不为-1才报告成功，沿用已有V事务/异常路径。e/s.a读取保存结果，失败时增加ICON_SOURCE_DATABASE_WRITE_FAILED警告，同时继续返回可用字节保留既有内存回退；不新增重试。IconRasterDiagnostics.persistSource的DONE更名ICON_SOURCE_CACHE_READY，只表示字节已准备，避免把“有内存字节”冒充已验证落盘。没有改数据库结构、缓存目录、来源选择、RAW表示、图标合成或页面加载顺序；第十一批延后候选保持撤回。

**真实SQLite与调用链检查：** 新测试复用tools/tests/deferred_icon_source目录，用项目apktool内SmaliBuilder原样组装实际e/V/U及完整e.s.a方法，在Android16 ART中运行独立SQLite文件。PM/来源生成/数据库入口是夹具，入口最终调用实际e事务；不是完整Launcher磁盘故障UI或真实并发竞态注入。旧版记录4个误报：重复约束插入、更新不存在owner、无效列插入、RAISE(IGNORE)更新。修后16项检查通过，包括正常插入/更新、SQL异常旧处理、数据库保持、保存失败仍返回内存字节、不持久化调用和MD5不变返回；另一个独立app_process只读打开同一文件，3项读回通过。这些是检查数，不是19种独立场景。替回旧e的负例准确在constraint insert断言失败，替回旧e.s的负例准确因缺少唯一失败警告而失败。前者shell显示137，已按对应PID保存AndroidRuntime断言，不把137本身当OOM/系统杀进程证据；失败试验进程不是Launcher。独立文件/DEX测试后清理，没有给已安装桌面制造数据库故障。

**回归夹具修正：** 原有deferred_icon_source/run_tests.py未跟上第十批borrowed-source接口，首次编译在缺少borrowedCompositionSource及5参compositor处失败。已只同步该队列夹具接口并重跑通过，借用Bitmap真实所有权仍由既有prepared_icon_source设备测试覆盖；这个队列夹具不冒充原生渲染检查。新run_database_tests.py独立验证真实SQLite/Smali，并保存按PID限定的警告/断言日志。

**真实应用跨进程核对：** 按用户最新指示使用Android16 Pixel_6_Pro/API36/x86_64/4KiB/host GPU，read-only/no-snapshot，保持已有1080×2400/480及原数据。补写前、原包5次启动后、最终包5次启动后的table_icons均22条，owner/MD5/三种PNG/data1～3排序内容SHA256都为865f0043d3987da3f506fbf6d5c0ca025a6f81c5043ba4e5c17ee24e3273ecb0；扩展3列均空。原每轮21个DONE、最终每轮21个CACHE_READY，最终无数据库失败或源缺失日志。本场景内容本已存在且MD5一致，这证明缓存未在重启后丢失，不证明每轮重新写入了RAW。新增写入/失败返回由上面的隔离真实SQLite验证；没有动态枚举所有ItemInfo字段，不把源码的读取目标推断写成运行时RAW空值统计。

**启动与功能：** 最终正式包5次force-stop进程启动，OS/ART/磁盘缓存保留、相同10秒Perfetto，PAGE_READY=2596/2251/2214/2259/2306ms，中位2259。此前5次用于缓存往返观察，首轮还与隔离故障负例有重叠，不作严格性能前后对照；本批没有提速结论，不与真机数据混比。最终五轮桌面图标/桌面设置BACK/底部上滑搜索/准确settings查询提交/结果图标启动系统设置/返回通过，PID6017保持，截图复核，限定PID无AndroidRuntime fatal。Gboard测试临时切English后恢复拼音，截图留证，未改系统IME配置；输入DEX/XML清理。AVD常用应用未开启，未改权限或开关，不覆盖Top5/三星Share/真机/全ROM/全主题/长稳/真实16KiB。

**构建与交付：** build.bat（含图源审计/生成检查）、签名v1/v2/v3、zipalign-P16、v1.5.8/33通过。最终SHA256=aa336816dd9bb78b0af196bb13a20cc46fd83fad4bccaa5f06340453c4a1ec72，模拟器拉回base.apk相同；相对上一正式包仅classes.dex/classes2.dex的非签名ZIP内容变化，Manifest/资源/native不变。3个生产文件及2个既有目录内测试文件；此前借用源Bitmap等无关工作区修改保留。129项暂存binary patch仍f386b4d82f1c0e7b26f84785e81133bf2727697781140da6a3e6f782ec700d1e，无add/reset/提交/推送。MEMORY.md未更新；主日志/性能/回归/问题清单/统一计划更新。证据build/startup-source-roundtrip-20261022/verification.json、roundtrip-baseline.json及所有原始输出。

**剩余与下一项：** 本批关闭SQLite成功标志及失败日志缺口，不关闭冷启动。若要跨进程免重做高分辨率合成，下一项必须先在现有Owner内验证版本化RAW/纹理持久化协议：表示类型、来源/组件/用户身份、主题/圆框/尺寸版本、容量和失效/清理/备份恢复边界。旧三种PNG缺少这些身份，直接读回字段和把工作推迟到首次翻页均已不准入。先确定协议和失效证明，再决定是否增加存储，不继续无证据调整加载时序。Folder暂停、A22不重测及其他矩阵缺口保持。

<a id="2026-10-22-第十一批全页计时纠偏延后图标内容候选因首滑长帧撤回"></a>

#### 第十一批：全页计时纠偏，延后图标内容候选因首滑长帧撤回

**本批结论：** 约640ms不是“两页初始化后”的独立收尾/纹理预载热点。旧 StartupPageSceneDiagnostics 明确只记录前两个 status=0 工厂，真机有9个普通页；补齐工厂计时后其余7页仍提前完成图标内容。原版的“前两个普通页 Hn”与“只初始化前两页图标”不是同一概念，纠正此前第八/十批对此的范围描述。整体冷启动仍未解决；没有交付把启动等待转移到首次翻页的方案。

**来源与计时：** 当前 fa.a 根据 Eb.Jx 选择普通分页，本次候选实际作用于 ka（PageWithRenderTarget），不是把 O（PageNoRenderTarget）的静态阅读当作真机路径证明。M 构造器 fn 虚调用 ka.a，ka.a 末尾直接 g.create；ka.gn/oo 又有既有的按页 Hn 初始化链。对照 clean_launcher（原 APK 当前缺失）、maintained 的 MainView/PageNoRenderTarget/Page 等原有路径，未直接替换核心。临时在 Eb.Vh 的 oh/zx/Dx/Z/几何/Gx 等后插标记，并将逐页统计上限临时由2提高到64。初步细分 oh约1021ms，Dock zx33ms，其余收尾约0～1ms；阴影预载开始/结束同一毫秒。完整一轮9页工厂耗时314/102/98/36/176/49/59/138/37ms，静态源/阴影调用分别10/7/8/2/10/5/5/6/3，共56次；各数值只指该轮、该阶段，不把外层与内层或不同样本中位数相加。

**候选最小范围：** 只在 ka.a 控制普通图标 create 时机；构造时保留 ItemInfo、子节点、相机、坐标和布局，通过既有 Hn→gn→oo 创建内容。vI已初始化的运行时插入、大屏以及Gaussian（含透明/毛玻璃）仍立即创建。文件夹单独构造分支不改，没有新线程/缓存/Manager。此处是已撤回的实验，不是当前正式实现；保护分支仅做源码核对，不冒称已做各主题/大屏运行矩阵。

**同条件15次启动：** Android16真机V2458A，1260×2800/560、12宫格/light_blue/原数据及权限，force-stop重启但保留OS/ART/磁盘缓存，每次相同10秒Perfetto。原1387/1337/1324/1315/1325ms，中位1325；候选896/821/855/846/847ms，中位847；反向原1397/1333/1305/1335/1339ms，中位1335。GL构建帧wall中位1096.050/615.896/1114.143ms，scheduled CPU1002.716/567.377/1013.693ms。三组均为带相同诊断的APK；全局日志级别在三组中均I。系统总日志yes、单标签I时仍发生整进程日志缺失，未继续将空日志当有效标记：在原有 LauncherStartupDiagnostics.markLocked 临时增加相同 Perfetto app section，以其中的 sinceLaunchMs 和PID核对全部15组。早期无标记/漏日志采集及失败脚本保留，不混入有效组。不能把 am start 的 TotalTime 或首个空帧当 PAGE_READY，也未声称首装/物理屏幕呈现验收。

**否决依据：** 同一真机每组从第0页向前连续8次滑动到第8页，再返回8次，每步截图并保存输入时间窗及32秒Perfetto。原首次向前8次最大GL onDrawFrame约10.73～12.14ms，均无>50ms帧；候选为109.03/50.26/172.81/65.17/79.33/88.84/64.59/12.03ms，前7次各有一次>50ms帧，回程恢复约10～12ms。反向原首次向前最大10.24～13.25ms，回程最大18.07ms，全部无>50ms帧。9页截图人工复核最终图标显示齐全，但不以等待后的截图掩盖首滑长帧；onDrawFrame不是SF/物理呈现耗时。方向和路径由截图顺序确认，没有通过改刷新率/清数据换取差值。结论是工作从启动移到了首次页初始化，因此候选不准入。

**撤回与最终验证：** ka、Eb、两个Diagnostics源码均按实验前快照逐字节恢复，不保留延后策略、额外标记或64页统计。恢复build.bat、签名v1/v2/v3、zipalign-P16通过；恢复APK与实验前3b827661…全部非签名ZIP成员（包括classes.dex/classes2.dex）一致。重建容器因包装/签名元数据不同，最终SHA256=23a889a4cf370d57ef8f2dbf99edb99c3bc1591002eb737f68ed1fe4856ddb20，真机拉回哈希相同。最终正式包五轮桌面图标/桌面设置BACK/底部上滑搜索/常用五图标/准确settings查询/结果启动系统设置/返回通过，PID6887保持，截图复核。正式包这五轮是功能回归；上述15次性能为同诊断对照，不能改写成撤去诊断后新采15次。

暂存129项binary patch仍f386b4d82f1c0e7b26f84785e81133bf2727697781140da6a3e6f782ec700d1e，无add/reset/提交/推送；MEMORY.md未更新，主日志/性能/回归/问题清单/统一计划更新。系统通用日志按用户授权保持persist.sys.log.ctrl=yes，全局log.tag恢复本批前M，原5个Launcher标签I保持；未上传厂商反馈，未改默认HOME/主题/宫格/布局/刷新率。Folder继续暂停，A22不重测，三星Share/全ROM/完整恢复/首装/长稳/严格16KiB仍未验。

**下一项：** 核实既有 PENDING_SOURCE_WRITES→persistSource→e.s.a 的异步补写是否实际落入持久化存储、下次模型加载是否恢复 iconRawData；先做相同图标跨两次进程的写入/读取对照。这与“直接复用缺少身份的旧dark/light成品”和本次“延后所有后续页”不同。没有先证明命中/版本失效/所有权前，不增加新的缓存，也不再次把延后工作当作启动收益。

证据总目录：build/startup-bind-tail-20261022/，入口summary.json、restoration.json、paging-frame-comparison.json；保留三组全部原始trace/日志/截图、失败采集、实验源码及各构建日志。

<a id="2026-10-22-第十批同次静态合成借用源-bitmap冷启动仍开放"></a>

#### 第十批：同次静态合成借用源 Bitmap，冷启动仍开放

核对了原版 clean/raw、maintained 和实际数据库：dark_icon/light_icon/transparent_icon 已包含旧几何与阴影，data1～3为空，未携带当前 RAW 来源/圆框/尺寸/主题失效身份；不能直接当作当前最终纹理，也不能再当原图重复加阴影。原版 APK 本地当前缺失，本轮参考为现有 clean/raw，未声称重新检查原始 APK。没有增加数据库列、持久缓存或并行 Bitmap Owner。

最小修改仅 IconRasterDiagnostics：在同一次调用中借用 BitmapDrawable 已有的有效 ARGB_8888 Bitmap，供分类和原 Composer 使用；不缓存、不移交、不回收借用输入。DEFAULT 圆框、其他配置和普通持久化准备继续原有自有拷贝；几何 fallback 返回输入时先复制，确保返回值仍归调用方。首次进入实际走 uncached 入口，最初仅优化 cached 入口的候选未减少启动工作，已作为失败原型单独保留，不能混入最终五样本。

同一 Android 16 真机 vivo V2458A、1260×2800/560、12宫格/light_blue、原数据和设置，force-stop 重启进程，保留 OS/ART/磁盘缓存，每次相同10秒 Perfetto：修前 PAGE_READY=1340/1347/1357/1361/1351ms，中位1351；最终1366/1375/1359/1361/1357ms，中位1361。首屏 GL 构建帧 wall 中位1139.359→1134.758ms，scheduled CPU1038.927→1038.559ms。两页 SOURCE_RASTER 准备计数每次17→1，证明避免16次重复准备；不是实际 GPU 总耗时或整体提速证明。整体冷启动没有解决。采样顺序、缓存和 DVFS 未完全隔离，也未做本批反向原包样本。

真实安装包 SHA256=3b8276618a2f220b0fb35f91cc4f855aef2d8563c54518cb913a988ed8b2b9be（v1.5.8/33），构建、v1/v2/v3签名、P16对齐、拉回安装哈希通过；相对原0afe93ba…非签名 ZIP 仅 classes2.dex 不同。实际原生 Bitmap 所有权检查 cached274/uncached311通过，旧源码和删 fallback 拷贝负例准确失败；Composer/调度内容是 recording 夹具，不冒称完整渲染矩阵。13个静态图标区域像素相同，排除时钟及角标格。额外软件分类302项等值；可选硬件分类探针在 Mali/FORTIFY 析构阶段中止，属于独立探针失败，未计硬件通过，也未归为 Launcher 崩溃。

已完成真实五轮桌面图标/桌面设置/BACK/底部上滑搜索/常用五图标/准确 settings 查询/结果图标启动系统设置及返回，PID保持，截图逐一复核；无 Share 应用，不覆盖三星 Share、完整主题/分身/ROM/长稳/严格16KiB/真实首装矩阵。首轮构建曾与安装重叠出现文件占用，后等待安装结束重新完整构建通过；无日志轮次和 cached-only 原型均保留且不计有效样本。经用户授权在系统自带“日志信息采集”开启通用抓取，persist.sys.log.ctrl=yes；仍有全局 log.tag=M 抑制，最终为5个 Launcher 诊断标签单设 I 后补齐五次。与基线日志输出条件不能视为完全受控相等，未以这10ms差值归因。未上传厂商反馈，按用户要求保持系统抓取开启；详细供应商日志临时检查后已恢复关闭。

证据：build/startup-persisted-icon-audit-20261021/（baseline/final 五份 trace 与标记、所有失败原型、所有权负例、安装哈希、functional-real-five.json、最终日志恢复后再次五轮的functional-final-five.json、截图；最终PID17673的限定AndroidRuntime日志无fatal）。暂存129项的 binary patch SHA256=f386b4d82f1c0e7b26f84785e81133bf2727697781140da6a3e6f782ec700d1e 保持，无 add/reset/提交/推送；MEMORY.md 未更新。

下一项：细查 Eb.Vh() 内两页初始化结束至 LAUNCH_SCENE_BIND_END 的剩余 GL 工作，当前样本约637～643ms；标记前后顺序证明它在 Vh 返回之前，不能先归因 Ra.wt、纹理上传或 GPU。先加必要细分证据，再决定最小修复，避免重复已收口的来源微优化。Folder 继续暂停，A22 用户确认的内存压力返回问题不重测。

### 2026-10-21

<a id="2026-10-21-第九批实验已否决软件准备前移成功移交但完整启动变慢"></a>

#### 第九批实验已否决：软件准备前移成功移交，但完整启动变慢

**任务/候选范围：** 按第八批结论验证在现有Owner内前移首屏软件图标准备，不直接套用maintained的旧字节协议。实验借用IconPreviewRepository既有2-worker解码池，数据库/模型Worker只提交2个有准入结果的任务并join；没有新增线程池/Manager。候选只处理前两个status=0页面的普通静态应用，排除文件夹子项、动态/特殊入口、大屏与开启光影的路径；既有Composer和源规则复用。短期Batch以模型对象身份和既有完整纹理键保护最终Bitmap，最大8MiB；GL只取一次，未取/键变化/重复offer/取消/销毁/低内存均释放，已转交GL的结果不再由Batch回收。原版GPU纹理强制重建仍走原创建/绑定路径，首次新生成的软件纹理可交给这次GPU重建。两个优先级任务在执行期间临时恢复为DEFAULT，finally恢复解码线程原优先级；拒绝准入时仍在后台模型Worker执行，MAIN不等待。所有这些均为本轮已撤下的实验，不是当前正式实现。

**先验证再决定：** 实际Batch/选择/代数/一次性移交/清理方法提取到隔离ART环境，使用原生Bitmap，81项通过；包括take/close竞争20轮、8MiB容量、共享输入不回收、已转交不回收、取消后迟到结果释放、来源键中途变化、持久化512项满额保护、首两页/文件夹/特殊排除、池拒绝后台回退、优先级恢复及大屏/光影原路径保护。实际资源解析/最终Composer和调度Owner是受控夹具，不称完整真机渲染矩阵。删除键匹配保护的负控准确失败。原预览队列主机167项仍通过。候选实际21张纹理每进程全部被接收，持有5083344字节（约4.85MiB）；第一屏除时钟/状态/导航外11个静态区域与原包逐像素相同。未做候选主题/图标包/分身/真机及长稳矩阵，性能准入已经失败，未继续推广候选。

**失败样本保留：** 初始原型读取private sPageMode，落入-1默认几何，2731ms试跑全部键不匹配而被拒收；改用原版getSinglePageMode后键匹配。随后错误将forceReload当作拒收条件，五次3670/3276/2995/2875/2819ms，prepare完成但21项均未接收；已移除该错误条件并另采有效候选。另保留有效接收但尚未临时恢复线程优先级的单次2472ms。上述记录分别位于pilot-1、candidate-1..5、pilot2-1，不并入有效五样本，也未删除失败采集。它们不能作为正式包性能/功能故障报告。

**有效原/候选/反向原五样本：** 同一只读Pixel_6_Pro/API36/x86_64/4KiB/host GPU，原1080×2400/480、图标/主题/默认HOME/权限/刷新率保持；进程重启，OS/ART/磁盘缓存保留，均相同Perfetto配置。原0afe93ba… PAGE_READY=2404/2386/1751/1718/1582ms，中位1751；有效候选adopted=2165/2206/2176/2230/2236ms，中位2206；装回原包reference=1769/1847/1737/1842/1800ms，中位1800。候选五次各21个take。GL场景构建帧wall三组中位1128.766/571.420/1182.578ms，scheduled CPU861.831/385.779/798.752ms，两页初始化899/227/930ms。数据库结束到SCENE_TASK_BEGIN却从11/21ms增加为候选1021ms；候选软件准备duration中位1014ms，join挡在场景之前。各阶段中位不能机械相加；缓存/顺序/DVFS仍非完全隔离，但反向原包仍明显快于候选，足以否决交付收益，不能只展示GL帧下降称优化完成。整体冷启动仍未解决，首装/物理首帧仍未验。

**撤回和正式交付边界：** 已只撤下本轮在IconRasterDiagnostics/IconPreviewRepository及Launcher/data.A/d/e.s四份Smali中的实验，保留进入本实验前所有代码。临时源码/候选APK/测试脚本与Fixture归档到build/startup-raster-handoff-20261021/experimental-sources等位置，未遗留引用已移除方法的正式测试入口。恢复源码build.bat通过，重建包与原包全部非签名ZIP成员（含classes.dex/classes2.dex、Manifest、资源/native）字节相同；重建容器哈希因包装/签名元数据不同，另存rebuilt-restored.apk，不把它冒称原哈希。正式build/launcher-signed.apk已恢复为原0afe93ba559f3b5b4b16a2610071d65e5338acbd5d4ae9158b86bd2de64a51d4，匹配的idsig/unsigned/aligned也从本实验前的暂存对象恢复到工作区；只读git show，未写index。签名v1/v2/v3、zipalign-P16通过，最终安装仍为原包。

**暂存与回归记录：** 本轮初始读到100项，此后检测到129项；实际实验前快照已是129项，实验前/后cached binary patch均f386b4d82f1c0e7b26f84785e81133bf2727697781140da6a3e6f782ec700d1e。未执行add/reset/提交/推送，保留外部暂存变化，不恢复到旧100项。恢复后基础回归首次被Gboard拼音把settings转成“s额头听说”阻断，窗口/截图证明是错误查询，不记搜索崩溃；失败截图及XML保留，临时在同一键盘切English输入后重跑，完成后恢复拼音。最终五轮基础图标/设置/BACK/底部上滑搜索/准确settings查询/结果图标启动及返回的结果、PID与截图见functional-five.json；不新增主题/全手势/真机验收结论。MEMORY.md未更新，主日志/性能/回归/问题清单/统一计划更新；临时输入DEX清理、只读模拟器测试后关闭。

**下一项/禁止重复：** “每次重新软件合成，只是搬到进入GL前再等待”的候选已经否决，不恢复为默认方案或再以相同实验反复计进度。下一项先核对现有图标数据库dark_icon/light_icon及ItemInfo.Oe()成品数据的来源/表示/尺寸有效性，确认有没有可证明有效的结果可复用；原有RAW契约不改，未知/旧尺寸/已留白图不能当当前高分辨率RAW再加工，也不直接新增另一套无失效证明的Bitmap缓存。目标是减少实际重复合成/等待，而不是单独降低GL线程数字。Folder仍暂停、A22不重测，其他总验收缺口不变。

<a id="2026-10-21-第八批调查首屏gl耗时与maintained预合成图标链对照"></a>

#### 第八批调查：首屏GL耗时与maintained预合成图标链对照

**任务与已有证据：** 用户要求回到冷启动主线，并明确对照E:/FANG/smartisan/smartisan-launcher-maintained，尤其首次进入。先读近期性能记录和第七批现存五份Perfetto，没有重新重复目录/颜色/哈希/阴影去重实验。10/17的约5.8秒软件GPU结果、绑定后glGenTextures/Shader采样是旧环境证据，不能移作10/21硬件GPU当前结论；既往ART同线程wall倒退的排他wall排名继续无效。本轮用Perfetto slice/sched/thread_state及已有PAGE_INIT_END/PAGE_OWNER_DETAIL，不使用失真排名，不更新生产源码/APK或maintained项目。

**当前五样本量化：** 复用build/catalog-delivery-20261021的正式0afe93ba…/API36/只读Pixel_6_Pro/host GPU五样本，PAGE_READY仍3123/1994/2195/2150/2185ms，中位2185。覆盖SCENE_TASK_BEGIN的GL onDrawFrame为2533.570/1463.284/1507.262/1582.319/1498.808ms，中位1507.262；同区间实际Running中位918.533ms，Runnable R+R+按每样本合并后中位479.495ms，睡眠中位124.830ms。三项独立中位不要求相加严格等于frame中位；Runnable仅证明未获调度，不凭此指控某个后台线程/驱动。LAUNCH_MODEL_READY在本链是场景完成通知附近的标记（中位2184），不是“后台模型花了2184ms”，不能从标签字面重新归因数据库慢。

**阶段归属：** 各样本两页durationMs先合计再取中位为1205ms；两页来源ICON_SOURCE_RESOLVE=450ms、SMARTISAN_SHADOW=429ms、CELL_CONTENT_CREATE=238ms、SMENGINE_TEXTURE_CREATE=70ms。第0页单独805ms、来源306/阴影286/内容164/纹理41ms；第1页432ms、来源151/阴影161/内容70/纹理26ms。独立中位不可机械相加。细分SOURCE_DRAWABLE两页中位254.066ms、SOURCE_RASTER129.716ms、ORIGINAL_SHADOW238.523ms，来源身份1.038ms/类型3.136ms；细分是上层阶段内的区间，不能再次加到上层。GL frame中binder transaction中位190.945ms，decodeBitmap105.505ms（每次25），ImageDecoder_nDecodeBitmap72.285ms；这些与上层阶段重叠，不能据此说“只解码约178ms，其余全是GPU”。纹理阶段70ms也不是整个GPU执行/呈现时间。当前主要可定位负担是首屏GL上的来源获取和软件图标准备/阴影，以及显著调度等待，未证明首屏显示在PAGE_READY后又等待数秒。

**maintained精确源码路径：** Launcher.onCreate仍创建并显示LoadingUI，使用SMGLSurfaceView/SMRenderer/原SMEngine，不是普通Android View桌面。DatabaseHandler.dataInit→IconDB.loadIconToItem加载已有图标表；缺失项交Utils.generateIconDataList，newFixedThreadPool(3)+invokeAll调用GenerateShadowIconTask。LauncherModel.getIconDataContentValues(Bitmap)在模型准备链执行颜色分类、generateShadowIcons，并编码dark_icon/light_icon（LauncherModel.smali:2341/2351/2360/2421/2428）。模型getBitmap(id)读取ItemInfo.iconData并iconDataToBitmap（:1632–1674）；Utils.loadIconToTexture在TextureManager未命中时优先调用该getBitmap（:10551–10571），随后创建/绑定Texture。其GL热路径因而可消费已带阴影的准备数据；这与当前e/s纹理未命中进入IconRasterDiagnostics.composeUncachedStaticApplicationIconTexture或iconRawSource→composeCurrentStaticApplicationIconTexture→resolveStaticSource/软件栅格/当前圆框/原版阴影的路径不同。当前这一流程在GL执行，21个静态纹理首轮均miss，已有trace直接记录其阶段成本。

**不能据此误改：** maintained的3线程工作属于缺失图标生成，不是“所有启动都重算3线程”或“GL没有工作”；它仍要解码成Bitmap、创建/上传纹理，缓存不存在时也有首次生成成本。maintained MainView.createPages:5590–5599已有只初始化前两个正常页的门，Page.initPageContent:7866有已初始化保护；当前实测同样只初始化第0/1页，不能再把“移植版启动加载所有页”当根因。maintained是9/16宫格，当前12/20、RAW来源/分身角标/高分辨率/圆框/光影等合同不同，不能直接把dark_icon/light_icon旧字节或整块核心复制过来。静态源码支持预合成路径降低GL临界区负担的解释，但本轮未运行maintained APK、未做同机同图标同布局首次安装A/B；既有五样本是保留应用数据的进程重启，不是清数据后的首次安装，不能给maintained捏造速度数字或认定全部差距已被解释。

**交付与下一步：** 调查脚本/每样本slice、调度、并发线程CPU和阶段汇总位于build/startup-gl-hotspots-20261021/。原正式APK仍0afe93ba559f3b5b4b16a2610071d65e5338acbd5d4ae9158b86bd2de64a51d4；本轮没有新的构建、安装或功能验收结果，不把上批五轮重复记为新回归。100暂存项保持，MEMORY.md未更新；只更新本日志/性能报告/统一计划。下一项应沿用当前加载Owner和Composer，验证可在进入GL前准备的同一来源软件栅格/阴影及其移交条件；必须先证明来源/组件/用户/主题/宫格/比例变化的失效与Bitmap所有权，不新建并行raw Bitmap缓存，也不把GL纹理创建移到非GL线程。整体冷启动未解决，Folder仍暂停、A22不重测。

<a id="2026-10-21-第七批目录发布到页面投递的失效链收口"></a>

#### 第七批：目录发布到页面投递的失效链收口

**根因与参考：** 承接第六批，只检查已经发布的Catalog到MAIN回调/查询快照/分页绑定之间的缺口。原initializeDirectory回调只有active/request/session校验，旧ready回调会把当前searchGeneration写成“就绪”；scheduleFilter仅在packsReady时检查索引，在线结果先返回时可绕过；readSearchPage虽在IO结束前检查epoch，排队MAIN之后仍可能失效；saveResultState还会把旧rows标记为新peek目录的revision。IconPackManager的ready判定仅比revision/generation，不能拒绝同内容revision但已失效的旧Catalog实例。clean/raw/maintained没有本移植自绘图标目录同名Owner，原APK归档仍缺；未修改原版动画、GL、资源或来源优先级。

**最小修复与范围：** 生产仅IconLibrarySearchPage与IconPackManager。目录接受/ready回调核对当前Catalog身份；ready还须现有索引确实就绪，不能用新generation替旧任务背书。查询投递无论在线/包阶段都校验目录身份，有包结果时再校验snapshot generation/epoch；分页在MAIN绑定前再次校验；旧错误回调检测真实目录版本变化后走既有initializeDirectory。保存状态只用页面实际directoryCatalog且必须仍current，恢复/暂停后返回同样核对当前身份及ready。索引构建入口拒绝旧Catalog，结束前再次检查会话/代数/目录身份，ready判定也要求当前Catalog。不新增Manager、缓存、线程、定时重试或生产延时。旧request/session先被丢弃；只有仍属当前页面的结果检测到版本失效时重新初始化，新的request令其余旧回调失效。普通IO失败仍走既有提示/点击重试，不自动循环重试。

**受控负例与实际Android：** 新增run_publication_tests.py及PublicationFixture.java.txt，从实际源码提取initializeDirectory/scheduleFilter/requestPackPage/saveResultState完整方法，用显式worker/MAIN队列构造“读完后、投递前失效”。旧源码15组中10组准确失败；修后15组25检查通过，涵盖目录/ready/在线结果/包epoch/同revision新实例/失败回调/分页/状态保存，以及正常结果、过期请求、暂停和更换owner的负向保护。UI/Catalog/IO/队列是夹具，不称真实Android UI故障注入。既有pause/resume/retry测试补充目录替换和索引未就绪，16项通过。实际ART目录/SQLite164项通过（含旧Catalog拒绝/新Catalog重建），旧IconPackManager负例失败于“invalidated catalog cannot remain index-ready”；实际Catalog构建失效31项与主机预览队列167项保持通过。较早生命周期夹具缺新依赖的编译失败已修夹具声明，未绕过生产判断。

**构建和五样本：** build.bat、v1/v2/v3签名、zipalign-P16、v1.5.8/33通过。正式SHA256=0afe93ba559f3b5b4b16a2610071d65e5338acbd5d4ae9158b86bd2de64a51d4；安装拉回一致，非签名ZIP成员仅classes2.dex变化。只读Pixel_6_Pro/API36/x86_64/4KiB/host GPU，保留1080×2400/480及数据/主题/图标选择/默认HOME/权限/刷新率。五次PAGE_READY=3123/1994/2195/2150/2185ms，中位2185；保留OS/ART/磁盘缓存、相同Perfetto配置。首轮实际发生构建失效取消，没有ready；另4次各一次5199项ready。未删除首轮或用目录ready替代首屏验收。与上一批中位2194的9ms差异不作性能收益，整体冷启动仍未解决。

**真实UI回归与限制：** 正式包五轮桌面图标/桌面设置BACK/底部上滑搜索/settings提交/结果图标及启动系统设置/返回通过，PID4942保持，五结果和桌面截图核对。另通过实际Chrome替换页→搜索更多图标→分类→chrome查询：在线4项后图标包目录ready为48项，滚动后进入系统设置再BACK，查询/滚动位置截图保持，未选择图标；此48项不构成跨60项边界分页验收，MAIN分页失效由受控完整方法检查覆盖。包目录14311条/24929ms，既有坏夹具pack6失败1项仍记录，不当成本批新崩溃。限定进程日志无AndroidRuntime fatal；真实UI未注入安装/更新时序，真机/三星Share/Top5/完整ROM及长稳未验，常用应用仍关闭。100暂存项patch SHA256仍3a9a19cd102879ecd9e67a5dd9ad269420ee3bbf111839845da1fcad4ac488de，无add/提交/推送；MEMORY.md未更新。证据build/catalog-delivery-20261021/summary.json及原始日志/trace/截图。

**状态与下一项：** 本轮已把构建后投递、查询、分页及恢复的已确认缺口一起修复和回归，不再拆成后续目录微任务。下一优先项回到整体冷启动：先用本轮已采集五份Perfetto重新定位首屏GL构建的剩余CPU热点，再根据证据决定最小修改；不重复已关闭的来源哈希/颜色扫描/阴影/目录竞态。Folder保持暂停，A22不重测；真实整库恢复、严格16KiB、HOME系统交接及长稳/真机矩阵仍按统一计划开放。五份现有审计文档更新，临时工具清理、任务只读模拟器测试后关闭。

<a id="2026-10-21-第六批目录构建期间失效禁止旧快照重新发布"></a>

#### 第六批：目录构建期间失效，禁止旧快照重新发布

**根因与范围：** IconLibraryCatalog.load持有类锁读资产、采集安装标签并构建；invalidateInstalledLabels只写volatile instance=null，不参与发布同步。失效发生在标签快照采集后、instance赋值前时，旧构建会覆盖失效结果。两个IconPackManager失效入口和三个load调用方已核对。该Java目录属于移植新增Owner，clean/raw/maintained没有同名实现；原APK归档仍缺失，未把参考目录当成已完成原APK对照。不改原版GL/资源/动画或图标来源优先级。

**最小修复：** 复用现有单构建者类锁；新增仅保护代数/发布的短锁。失效递增代数并清空instance；后台捕获代数，先构建局部candidate，发布时核对代数，过期则抛OperationCanceledException，finally仍关闭资产流。不让失效回调等IO/PM/ICU，不新增缓存/Manager/自动重试。旧load调用方已有异常日志与页面点击重试入口；构建中发生失效的请求会被取消，下一次请求重新加载。已发布引用到页面异步回调之间的版本检查不属于本项已验收范围。

**先负例后验证：** 扩展现有run_directory_probe.py，增加generation-only/catalog-source入口；CatalogGenerationProbe编译实际Catalog/JSON/拼音代码，在测试副本的真实安装标签快照后插入闩锁，并注入一个合成应用名称；资产流仅包裹关闭计数。旧源码确定失败于“invalidated build must not republish old snapshot”。修后API36 ART 31项检查通过：1次/连续3次失效、MAIN失效无需等待后台、旧结果不发布且明确取消、后续两并发调用只重建一次、新名称有效、MAIN缓存读、取消/成功均关闭流。测试未修改用户应用、Launcher私有数据或真实PM标签。原目录SQLite/中文/安装标签/图标包异常隔离159项、页面pause/resume/retry14项、预览队列主机167项通过；不是全ROM/安装更新故障矩阵验收。

**正式包与五样本：** build.bat、v1/v2/v3签名、zipalign-P16、v1.5.8/33通过；SHA256=09f59081322a9bc68105c56ffd4fd49dd90bb968a023bb6b7cbfec92d3a00155，拉回安装包一致，非签名ZIP成员仅classes2.dex变化。只读Pixel_6_Pro/API36/x86_64/4KiB/host GPU，保留1080×2400/480、数据/主题/默认HOME/权限。相同Perfetto配置下五次PAGE_READY=2860/2194/2124/2080/2382ms，中位2194；保留OS/ART/磁盘缓存，无旧新A/B性能归因，整体冷启动仍未解决。第1次正式进程4378实际记录Catalog invalidated during build，旧构建被取消，没有ready；失效调用来源未单独跟踪，不猜测具体系统广播。其余4次各一次ready/5199项。不把缺少ready当“5次目录均成功”，也不删除首轮样本。

**功能与边界：** 正式包五轮桌面图标/桌面设置BACK/底部上滑搜索/settings提交/结果图标启动系统设置/返回通过，同PID4778，截图人工核对，限定日志无fatal。另实际进入Chrome→替换图标→搜索更多图标，分类和chrome查询图标正常；先在线结果4项，包索引就绪后日志48项。14311包目录耗时23725ms，保留既有损坏夹具pack6读取失败1项，未隐瞒或删除。真实页面本次未在同一进程重现“失效后再次加载”；该恢复由ART闩锁用例证明，实际UI是普通加载路径。没有选择/更改图标，常用应用开关仍关闭，三星Share/Top5/真机/全手势HOME/长稳未验。100暂存项patch哈希保持，无add/提交/推送，MEMORY.md未更新。证据build/catalog-generation-20261021/。

**下一项：** 核对已发布目录到排队MAIN页面回调、搜索快照之间的版本校验，防止发布之后再次失效时旧回调覆盖新页面；不重复本批构建中失效实验。Folder继续暂停，A22不重测。更新统一计划、性能/回归/问题清单；任务模拟器和临时工具测试后关闭/清理。

<a id="2026-10-21-冷启动第五批目录预热改用既有目录线程释放解码容量"></a>

#### 冷启动第五批：目录预热改用既有目录线程，释放解码容量

**审计结论与根因：** 本项核对首屏资源装载与后台预热。IconLibraryCatalog.installedLabels仅遍历应用名称/分类与拼音，不读取图标Drawable/PNG；load以现有instance+synchronized合并构建，settingsResources已有单份Resources缓存，不能把两条线程加载同一APK的不同资源当作已证明的重复图片解码。本轮未删除预热、未扩大图标/PM/hash缓存，也不重复既有来源哈希优化。实际异常是IconPreviewRepository构造时将IconLibraryCatalog.load作为P2任务投给仅2个worker的decodePool；目录/ICU约1秒在该池内执行，可与另一解码任务一起堵住可见图标。项目已存在indexPool（icon-directory、单worker、有界4、后台优先级/超时退出）负责目录IO，此构造入口未遵守该分工。原APK归档仍缺；clean/raw/maintained没有本移植构造Owner，不为此改原版GL/动画核心。

**先负例后最小修复：** 既有tools/tests/icon_preview/run_tests.py增加--source及提取实际构造提交语句的测试入口，保留既有request/session/queue/RenderTask等实际方法。用CountDownLatch阻塞目录构建和另一decoder，旧源码显示owner=probe-render/renderActive=2/directoryActive=0/visibleWhileBlocked=false，两项失败；不靠随机延时或手工重写调度函数。候选显示probe-directory且可见loader在两阻塞任务释放前开始。生产仅IconPreviewRepository.java三行增加/一行替换：构造预热Runnable交给既有indexPool.execute，任务入口保留pauseP2检查；新池在构造时刚创建、未对外发布且队列为空，此唯一提交不增加通用准入/重试系统。没有新增线程池/Manager、缓存、会话或永久任务。目录内容/构建内部顺序/源选择规则保持，异步完成时刻可能变化，不宣称所有并发加载的相对先后固定。

**生命周期与回归：** 构造提交是进程Owner，不绑定设置页会话；目录任务仍一次调用IconLibraryCatalog.load，沿用原异常日志。低内存pauseP2在开始前检查，已经运行的工作不强行中断，与原RenderTask一致。测试另同时占住目录和两个decoder，把预热排队后设置pauseP2，验证不执行目录；删除这行guard的负例准确失败。主机与API36 ART各167检查通过（同一167项跨两环境，不称334个独立场景），包括原有可见订阅合并/取消/边界竞争/队列有界/网络隔离/MAIN交付；构造实际提交和线程方法为实际源码，Bitmap/Drawable/cache/network/Catalog内容是夹具，受控阻塞不是全ROM真实UI卡顿复现。

**实际APK线程证据：** 正式包五次启动的ICON_CATALOG_READY日志tid与Perfetto thread交叉核对：旧五次全部icon-preview，新五次全部icon-directory；每进程各1条ready/5199项。旧目录耗时2340/1124/1194/1114/1114ms，新1195/1126/1088/1091/1081ms（中位1124/1091），目录工作本身仍约1.1秒，没有被跳过；rows一致不等同全部目录内容/语言/包变更矩阵的字节等值证明，Catalog代码/资源未改。具体tid、PID见catalog-owner-analysis.json；不从排他wall失真的旧ART采样推断收益。

**五启动与正式交付：** Pixel_6_Pro/API36/x86_64/4KiB/host RTX3060/read-only/no-snapshot，原1080×2400/480及数据保持；force-stop进程而保留OS/ART/磁盘缓存，每次Perfetto相同配置。旧PAGE_READY=3477/2146/2237/2077/2091ms，中位2146；新2030/2024/1899/2276/2095ms，中位2030；构建帧wall中位1432.454/1432.393ms几乎相同，CPU959.276/912.536ms，顺序/缓存/调度仍未隔离，不把116ms归因修复，整体冷启动仍未解决。build.bat、v1/v2/v3签名、zipalign-P16、v1.5.8/33通过；SHA256=935efbeecd8bd4ed047651f3b44e0f9b144e55295bcd8e0ddec1815279c5c149，相对be4cb7f…非签名成员仅classes2.dex变化，原版smali/资源/native保持。保数据安装拉回base.apk哈希一致，五轮桌面图标/桌面设置/BACK/底部上滑搜索/settings提交/结果图标与系统设置启动/BACK及显式前台返回通过，同PID5406/限定日志无fatal，五轮结果和稳定桌面截图人工核对。

**状态与下一项：** 本项目录/解码worker隔离已收口，不再循环采样同一占位条件；冷启动、长稳、真机/三星Share及完整多ROM/主题/分身矩阵未关闭。常用应用仍关闭，未声称Top5验收；测试0.6秒转场等待不进生产，不替代首触摸/全手势HOME验收。100暂存项patch哈希保持，无add/提交/推送，MEMORY.md未更新；本日志/性能/回归/问题清单/统一计划更新。临时手势工具删除、只读模拟器关闭，证据build/startup-directory-owner-20261021/。下一项检查目录失效与重建的并发发布，避免应用安装/更新期间旧预热结果覆盖新的失效状态；先建立可重复的中途失效负例，不擅改用户应用或权限。Folder继续暂停，A22不重测。

<a id="2026-10-21-冷启动第四批原版阴影重复alpha提取与成功路径临时图回收"></a>

#### 冷启动第四批：原版阴影重复Alpha提取与成功路径临时图回收

**根因与原版对照：** data/L.a(Bitmap,Canvas,int,int,float)在同一未变v9和同一Yq/BlurMaskFilter下连续extractAlpha两次，分别供v11/v13两次不同颜色叠加。二者在使用期间只有读取，没有任一方被Canvas设为写目标；不同半径的NORMAL/OUTER提取仍是必要工作。当前L、clean/raw原实现均有同段重复，maintained/HolographicOutlineHelper也保留相同模式；原APK归档仍缺，未宣称重新读取了原APK。外层a(Bitmap,Canvas,float,int)自己创建带边距Bitmap v1，只作内部输入；内层返回新ARGB结果、Canvas已脱离输入，外层成功返回前v1未显式回收。

**最小修复及所有权证明：** 生产只改launcher/smali/com/smartisanos/launcher/data/L.smali两个方法。两次颜色绘制继续保留，但v13/v12改为复用同次v11遮罩/v10偏移，末尾仅按唯一Owner回收一次v11；NORMAL/OUTER、半径、颜色、位置和层数均不变。外层Canvas.setBitmap(null)以后回收自己创建的padding v1，原图/返回图不回收。每次原版阴影生成extractAlpha4→3，Bitmap生产操作2个createBitmap+4个extractAlpha→2+3，少一个临时位图与一个int[2]；成功路径padding不再等待GC。没有全局/跨调用缓存、池、Manager或新阴影算法，也不改raster版本。仅改善成功路径，现有异常/OOM路径未新增finally资源协议，不宣称所有中断清理完成。

**实际原生位图验证：** 新tools/tests/icon_shadow/run_bitmap_tests.py直接组装修改前/后实际Smali，依赖当前APK的ua.b及Android原生Bitmap/Canvas/BlurMaskFilter，不替换为Java阴影模型。363组像素案例/6267检查（含微基准Canvas脱离检查），覆盖8×11/32/96/192、空透明/不透明/分级alpha/镂空/随机、0.5/1/3/9/16/24半径与三组双色，以及ALPHA8/RGB565/F16。公开单层入口及内部双色核心均逐像素、尺寸完全等值，输入像素/generation/存活和输出存活保持。另行组装仅暴露局部临时引用的跟踪副本，证实padding与输入/输出不同，候选成功已回收，所有3个alpha中间图均回收；原版4个alpha均回收但padding未回收。完整非采样追踪确认公开入口完成，extractAlpha4→3、createBitmap仍2次；不从采样栈推调用次数。旧源码负控准确失败padding release candidate=true，错误复用未模糊遮罩负控准确失败输出尺寸，测试确实约束回收和视觉。既有58选择/缓存/管线、24主题切换及44交接保护检查通过。

**局部耗时边界：** 首轮32×32/30次CPU基准有0及不足粒度值，保留bitmap-probe结果但不作性能结论。改128×128/每组300次，正反交替5组CPU旧288.111/286.071/329.719/281.617/320.015ms，新187.514/188.196/173.184/217.702/184.064ms，中位288.111→187.514ms，仅此暖态单色/半径9局部基准，不等于所有图标/整体启动速度或内存峰值收益。未将释放引用数转换成PSS/Graphics下降承诺。

**五样本、构建与实际回归：** 同一API36/x86_64/4KiB/host RTX3060/只读无snapshot模拟器，原1080×2400/480覆盖、数据/OS/ART/磁盘缓存保留，逐次force-stop并采Perfetto。旧包PAGE_READY=3121/2364/2148/2208/2119ms，中位2208；新包2014/1974/2249/2265/2172ms，中位2172；GL构建帧wall中位1514.953→1495.709ms、scheduled CPU909.450→895.211ms。差异小且顺序/调度/缓存未隔离，不认定36ms为稳定收益，整体冷启动仍未解决。build.bat、v1/v2/v3签名、zipalign-P16、v1.5.8/33通过。正式SHA256=be4cb7f019cfef1ac66ba9aa527b606999edab8634cf5fa02fc7385a5560199d，非签名成员仅classes.dex变化；引用表一致，26086方法的flags/registers/instructions仅上述两个L.a变化（排除移动的debug-info指针，未以此替代异常表完整验收）。安装拉回base.apk哈希一致；五轮图标/桌面设置/BACK/底部上滑搜索/settings提交/结果图标和系统设置启动/返回通过，PID5994保持，限定日志无fatal，截图人工核对。末尾等待转场稳定再拍桌面；测试等待不进生产、不是纯首触摸延迟或完整手势HOME验收。

**交付与剩余：** 100项暂存patch哈希保持，无add/提交/推送；MEMORY.md未更新，本日志/性能/回归/问题清单/统一计划更新。未改默认HOME、主题、布局、图标源、权限或刷新率。常用应用未开启，三星Share/真机/Android9完整光影/多ROM多主题长稳及异常路径仍待验。Folder继续暂停，A22不重测。临时手势工具移除，任务只读模拟器关闭；证据build/startup-shadow-20261021/。下一项核对首屏应用资源装载与后台预热是否重复加载同一应用资源，先建立包/组件/调用Owner和时序证据，再决定最小修复；不重复来源哈希、颜色分类、诊断扫描或本批已收口的重复遮罩采样。

<a id="2026-10-21-冷启动第三批复用同次未变图案的诊断边界扫描"></a>

#### 冷启动第三批：复用同次未变图案的诊断边界扫描

**根因与参考：** 继续上一批的原图绘制/边界扫描/阴影链核对。composeTexture先analyzeVisibleBounds(analysisSource)，再扫描physicalArtwork，随后reportSourceCanvasOnce又扫描normalizedArtwork；普通未加角标图案是同一个Bitmap且中间没有像素变化，因此第三次是纯诊断重复扫描。边界只进入日志/debugMetrics，不参与sourceScale、几何、圆框或阴影绘制。reportSourceRouteOnce仅有私有定义无调用，不能把它当本轮真实重复来源解析。原APK归档仍缺，clean/raw及maintained没有本移植Java诊断Owner；当前LauncherSettingBridge/原L.a只读输入并创建自有阴影中间图，IconIlluminationCompat准备读取alpha，未为诊断问题替换原版算法。既有ART sample中的扫描CPU约16ms只是定位线索，不是本批精确节省或全启动根因。

**最小修复与所有权：** 仅生产IconRasterDiagnostics.java，composeTexture将已经得到的visibleAfter、对应Bitmap引用、generationId作为当前调用局部参数交给原reportSourceCanvasOnce。原REPORTED判重后，只有对象身份相同且generationId相同才复用；空透明图的null边界也是已扫描结果。角标替换图案、原地变更或下游像素修改时仍执行原后置扫描。引用不出当前调用，不新增缓存/Manager，不改变回收和异常边界，不改任何绘制/阴影/圆框/布局/动画参数，不需递增raster版本。普通首次3次扫描→2次，变化图案保持3次，已报告重复合成仍2次。

**测试与负例：** 新tools/tests/icon_raster/run_bounds_tests.py从实际修改前/后源码提取整个composeTexture、scanner、VisibleBounds/StaticSource和report一次门禁/日志公式，使用Android原生Bitmap/Canvas运行1007场景8056检查。覆盖透明/不透明/alpha39与40阈值/随机与内边距，32/96/256输入、Drawable/Bitmap、resize、圆框已准备输入、角标新图/原地变更/null返回、projection/shadow阶段受控像素修改、阴影失败回退、重复报告、同身份下一次像素替换。输出像素/完整诊断文字/调用次数/输入像素与回收/Drawable bounds保持；projection/shadow/几何/profile是受控Owner，不称完整原版光影像素验收。旧源码负例准确失败old=3/now=3/expected=2；去掉identity/generation条件的负例准确发现透明图被修改后日志误报可见宽高0而应1，保护不是多余分支。初次负例main未打印未捕获异常，只见shell Killed；已在测试入口显式捕获打印/System.exit(1)，重新取得上述断言，未当Launcher崩溃。既有LocalCompose246+Uncached289通过。

**构建与五样本：** build.bat、v1/v2/v3签名、zipalign-P16、v1.5.8/33通过；SHA256=ca7c3c809767cfc0eba9c17d96b116d547472cad7e52254760c3b6c5a17ad266，相对上批a4b23942…非签名成员仅classes2.dex改变，原classes.dex/图标/资源/native保持。Pixel_6_Pro/API36/x86_64/4KiB、host RTX3060、read-only/no-snapshot，保留原1080×2400/480和数据，不更改HOME/主题/宫格/权限/刷新率。旧包PAGE_READY=3415/2368/1763/2521/2200ms，中位2368；新包2128/2288/2138/2131/2175ms，中位2138。构建帧wall中位1586.614→1491.678ms，scheduled CPU972.511→1019.287ms；缓存/调度/顺序影响未隔离，CPU未同步下降，不归因230ms差额、不宣布整体启动提速。未重复已证明存在顺序影响的上一批ABA来凑收益，冷启动仍未解决；不跨模拟器/真机比较。

**功能与恢复：** 正式保数据安装，拉回base.apk哈希一致。五轮桌面图标、设置进入/BACK、底部上滑搜索、settings提交和结果图标、启动系统设置、BACK/显式Launcher前台通过，PID5728保持；限定PID日志无AndroidRuntime fatal。最终脚本截图抓到系统设置转场中间帧，保留final-desktop.png，不作为稳定桌面图；补查焦点smt_launcher并在转场后复核final-desktop-settled.png正常。每轮测试原有0.6秒等待不进生产代码，不作为首次触摸延迟或全面手势HOME验收；常用应用关闭，不覆盖三星Share/Top5、真机/完整主题/分身/光影矩阵。100暂存项patch哈希保持，无add/提交/推送。MEMORY.md未更新；本日志/性能/回归/问题清单/统一计划更新。模拟器完成后关闭，临时手势工具移除；证据build/startup-bounds-20261021/。

**下一项：** 诊断重复扫描已收口，不再围绕它循环采样。继续细分原版阴影多层合成中的alpha提取、不同半径遮罩及临时Bitmap分配，确认哪些是原算法必要工作、哪些确有重复，再决定修改；不按函数次数直接删阴影层。Folder仍暂停、A22不重测、冷启动未关闭。

<a id="2026-10-21-冷启动第二批颜色分类批量读像素整体提速未证明"></a>

#### 冷启动第二批：颜色分类批量读像素，整体提速未证明

**根因与最小修改：** 继续首屏GL构建主线。既有ART样本的wall时间倒退仍不采用；按单线程单调CPU时钟重算，场景任务采样CPU合计706.404ms，其中nativeGetPixel约42.381ms，只是部分开销，不是完整首屏根因或精确调用次数。当前f.d与clean/raw均逐像素getPixel，maintained/IconColor也如此；原APK归档仍缺失。原c()先缩到64×64，原d()再逐列逐行分类。仅在原f.d对宽高均不超过64的图一次getPixels，保留x-major顺序、HUE/计数/平局/透明阈值和输出；较大直接d输入保留原路径。临时int[]至多4096项/16KiB，调用结束即可回收，不新增缓存/Manager、不改Bitmap所有权/动画/布局。生产只改launcher/smali/com/smartisanos/launcher/actions/sort/color/f.smali。

**等值与负控：** 新tools/tests/icon_color/run_device_tests.py直接组装实际修改前/后Smali，并在Android16原生Bitmap运行，APK只作现有依赖；303用例覆盖null、透明/半透明/纯色/随机/平局图案、非方图、1/63/64/65/256尺寸、RGB565/ALPHA8/F16、resize阈值、recycled/hardware异常与输入内容/所有权保持。每份完整非采样trace分别确认一次d退出，64×64基准getPixel=4096，候选getPixels=1。用旧源码作候选，负控明确在4096对4096处失败。初版合并追踪/复杂色追踪在ART事件上限截断，即使overflow=false也不完整，保留失败文件，不用971/3360等部分计数作结论；最终分开采集并检查完整退出。暖态单色分类100次CPU五组中位152.740→32.340ms，只是局部微基准，不等于启动收益。

**五样本与反向复核：** 同一Pixel_6_Pro/API36/x86_64/host RTX3060/4KiB、原1080×2400/480配置，read-only/no-snapshot，保留数据/OS/ART/磁盘缓存，每次force-stop重启并采Perfetto。旧包PAGE_READY=2971/2228/2528/2450/2255ms，中位2450；新包1761/2119/1729/1935/1647ms，中位1761；差值大于局部调用能解释的程度，故额外装回旧包复核1652/1749/1521/1734/1873ms，中位1734。构建帧GL CPU三组中位1080.928/800.362/828.345ms。反向旧包同样变快，缓存/调度/执行顺序影响未隔离，不能把初始689ms差额归因修复，也不宣称整体冷启动提速；冷启动仍未解决。每组首屏decodeBitmap仍25次，不改变取样条件或删慢样本。详情five-analysis.json与三组原始trace。

**构建与交付：** build.bat通过；v1/v2/v3签名、zipalign-P16、v1.5.8/33通过。正式SHA256=a4b23942db8647478a6e1bf87161ee8c03f6dd5515a372772532ae8057203711。除签名外仅classes.dex变化；常量引用表相等，26086方法的flags/registers/instructions对比仅f.d改变（比较排除移动后的debug-info指针，未以此替代异常表全面验证）。最终恢复新包安装，拉回base.apk哈希一致。五轮正常桌面图标/桌面设置BACK/底部上滑搜索/提交settings/结果图标与启动系统设置/返回通过，PID6899保持；截图人工核对，限定PID日志无AndroidRuntime fatal。回归有0.6秒转场等待，是测试节奏，不是生产延时或首触摸延迟测量。常用应用开关保持关闭，未验Top5/三星Share，也非全面手势HOME/真机/主题矩阵验收。81手势合同+4工具兼容场景通过。100项暂存patch哈希逐字保持，无add/提交/推送，MEMORY.md未更新。证据build/startup-gl-cpu-20261021/。

**下一项与边界：** 色彩逐像素JNI局部开销已收口，不再围绕它重复采样。接下来核对首屏原图绘制、可见边界扫描和原版阴影合成之间有无可省略的重复工作；优先使用现有Owner，只对确认重复做最小修改。Folder性能继续暂停，A22不重测，原生16KiB/HOME系统交接及真机缺口保留。

<a id="2026-10-21-android16硬件模拟器冷启动显示链核对与手势回归工具兼容修复"></a>

#### Android16硬件模拟器：冷启动显示链核对与手势回归工具兼容修复

**范围：** 用户要求继续冷启动剩余路径；真机不在，明确改用Android16模拟器。Pixel_6_Pro/API36/x86_64，-read-only/-no-snapshot启动，host GPU实际为RTX3060；4KiB页，保留原有1080x2400/480覆盖配置，未改默认HOME/主题/布局/宫格/权限/刷新率。正式343fd257…/v1.5.8/33保留数据装入只读运行副本。原APK仍缺失；clean/raw原J消息完成→requestRender/窗口属性主线程投递链及现有Java延后任务Owner核对，maintained没有本项目的新增诊断/目录预热Owner可直接替换。没有恢复Folder性能测试或A22试验。

**五样本新证据：** 进程重启但保留OS/磁盘/ART缓存，有Perfetto采集开销，不能与历史真机/SwiftShader对比收益。PAGE_READY为3190/2254/2465/2668/2352ms，中位2465ms；包含scene构建的onDrawFrame为2334.538/1607.347/1821.226/1958.919/1728.330ms，中位1821.226ms，scheduled CPU中位1141.666ms。该帧decodeBitmap各25次、合计约101–122ms，剩余不能直接归为图片解码或“重复纹理”。通过同GL线程acquireNextBufferLocked frame编号→同一SurfaceView的SF latch→commit token→显示FrameTimeline，得到首个构建帧缓冲相对PAGE_READY锁存差+7.540/+6.939/+2.381/-3.119/-39.058ms。负值表示回调可能晚于缓冲，不是时间倒流；日志只有毫秒精度。此证据确认没有回调后数秒的锁存等待，不是录屏像素识别的首个桌面内容，更不是物理屏幕呈现验收；显示帧仍有SF CPU Deadline Missed/Prediction Error，未称全程无掉帧。

**就绪后负载：** 主线程OPTIONAL_PAGE_TASKS仅1/3/3/5/4ms，中位3ms。部分样本就绪后三秒icon-preview消耗约868–1049ms CPU，icon-online约418–673ms；目录加载栈指向IconPreviewRepository构造时P2预热→IconLibraryCatalog.load→已安装标签/ICU拼音，后者peek也被自动图标别名解析、候选版本/变体使用。仅凭后台耗时不能删除预热或拆出并行目录缓存；没有发现可安全删减的新重复调用，本轮生产代码/APK净修改为零，整体冷启动仍未解决。ART启动采样成功产生trace，但本次数据20处同线程时间戳倒退，旧顺序分析器得出超过阶段长度的排他wall排名，故整份wall排名不作优化依据；Perfetto时间线和scheduled CPU独立分析，未用失真排名确定根因。

**首次交互边界：** 最初采集脚本沿用旧分辨率点720/2760，超出当前2400高度，五组仅保留启动/显示链，不计交互。按截图校准540/2160后另做5组单次真实Dock点按，均打开桌面设置；其中第2组即时窗口断言过早而中断trace，无响应耗时结论，保留后来设置截图；第3组错误从dumpsys window windows子命令读取不存在的全局mCurrentFocus字段，脚本超时但UI实际已打开，改为完整dumpsys window。第1/3/4/5组trace可见设置performCreate，距离PAGE_READY约478/427/582/544ms，包括ADB/轮询与Activity创建，不能当纯输入响应延迟或不丢首次触摸的全矩阵证明。失败样本保留，不删除慢样本或用补测冒充优化前后五样本。

**回归工具根因与最小修复：** tools/tests/search_gesture/TouchInput.java在API36反射InputManager.getInstance抛NoSuchMethodException，shell工具PID6940随后异常退出137；不是Launcher崩溃。仅当旧访问器不存在时改取InputManagerGlobal.getInstance，其余反射/权限异常照常抛出，不大范围catch、不改downTime或输入业务。实际API36完整DOWN→MOVE→UP注入返回0，并打开原搜索Activity。既有run_tests.py增加实际工具源码的旧API形状、新API形状、访问器抛SecurityException不应fallback、两访问器皆缺失四场景；同时验证swipe/CANCEL完整事件、恒定downTime/单调eventTime/触屏source/同步注入。81生产手势合同检查及4工具兼容场景通过；旧工具实际源码负例在新API形状准确失败NoSuchMethodException。旧API是主机夹具控制，不称本轮Android9真机验证。修复没有打入APK，不为工具问题改搜索业务。

**最终功能及交付：** 标准adb swipe有未打开样本，随后修正工具后用稳定downTime输入。早期稳态回归紧接BACK/显式前台立即点按有未打开记录，最终稳态组明确等待0.6秒界面转场（仅测试节奏，不改生产或作为首次交互数据），五轮桌面设置→BACK→底部上滑→settings输入并空格提交Gboard拼音组合→结果图标/启动系统设置→BACK/显式Launcher前台通过，同PID6279；搜索结果截图逐一复核，限定PID日志无fatal。原AVD常用应用未开启，未改权限/开关，不能称Top5/三星Share回归。只修改工具和其既有测试，未构建新主APK；实际工具javac/d8构建、API36注入、正式APK安装/哈希、启动/搜索/设置已验证。正式与已安装APK仍343fd257…，启动Owner字节及100项暂存binary patch不变，无add/提交/推送。MEMORY.md未更新。证据build/startup-visible-api36-20261021/verification.json、visible-analysis.json、interaction-analysis.json、functional-five.json及各失败输出；模拟器只读运行在证据保存后关闭。

**结论与风险：** 本轮关闭“PAGE_READY之后是否仍等待数秒显示”和回归工具兼容误判这两个排查点，没有解决整体冷启动、首次物理可交互、目录预热依赖拆分、长期内存或多ROM。后续优化必须有具体重复/无效工作与来源失效证据，不能再次把已关闭的来源/hash/ID微优化当新任务；Folder继续暂停。

### 2026-10-20

<a id="2026-10-20-连续验收收口真实saf导出回读取消授权失效统一剩余入口"></a>

#### 连续验收收口：真实SAF导出/回读/取消/授权失效，统一剩余入口

**执行方式与范围：** 用户要求“一次性执行完”，改为关联链连续执行、统一汇报；不再每个微项停等“下一项”。统一当前入口为LAUNCHER_FIX_AND_OPTIMIZATION_PLAN.md顶部表，旧10/20“最新”标题改标“历史批次”，历史证据保留。没有确认新的生产根因，本轮生产代码净变更为零；不因测试数量增加宣称冷启动或Folder解决，Folder按此前要求暂停，A22不再作为当前故障反复测。原版APK仍缺失，不冒称重新反编译原包。

**真实SAF：** 用户明确允许Documents/SmartisanAudit-20261020专用目录及新增授权、测后恢复。V2458A/API36，临时同签名诊断包只加debuggable标记，不加组件/权限/业务代码。保存原备份偏好及journal存在性、记录既有rollback_latest归档SHA256；不读账号凭据、不恢复用户桌面。首个诊断清单因属性顺序未获系统DEBUGGABLE认可，未取得有效快照/未写备份；调整属性排序后run-as与JDWP确认可用，原二进制Manifest和根目录正式APK均逐字恢复。诊断包由既有build.bat构建签名，不能当新增发布版本。

**实际路线与结果：** 原备份位置“尚未选择”、上次备份“暂无”。中途用户手动选择/backups，先保留并询问；用户后续明确要求测后恢复尚未选择，最终已按此恢复。专用空目录授权后，立即备份→预览返回取消，目录无输出；再次预览→保存成功，产生2026-10-20 20-42.slauncherbackup，3048126字节，日志COMPLETE、元信息指向真实文档。拉回ZIP共74成员CRC全通过。通过系统文件选择器选中该新归档进入恢复预览，9页/2文件夹/70应用与导出预览一致，然后返回；没有点击“开始恢复”，不能记为整库恢复验收。两次同名保存提示要求改名，测试前后归档SHA256一致，没有替换文件。

**取消与失败样本：** 首次用jdb默认全线程断点准备取消，暂停引发Input dispatching timed out（PID19407，20:46:24，FocusEvent等待5000ms），随后系统记录user request after error结束进程；该诊断诱发ANR不能当正式包ANR，也不能记取消PASS。重启后本次候选已清、journal回IDLE、旧归档与撤销快照保持。改用本地JDI辅助仅SUSPEND_EVENT_THREAD，在实际copyToUriAndVerify入口（partial文档已创建并记账）立即调用生产cancelRunningBackup并自动resume/dispose，无全局暂停：返回true、同PID22424、journal CANCELLED/BACKUP_CANCELLED、partial不存在，唯一已成功归档哈希保持。断点在复制入口，未写入首个chunk；这不是大文件传输中段取消或云盘断流验收。辅助app_process状态程序因Looper准备错误/厂商进程限制未取得有效结果，未作为通过依据；最终URI恢复使用受控JDI且仅操作本次新增权限。

**真实撤权与清理门：** 撤销专用测试树后，新备份因取消日志仍追踪已删文档且无法查询而报告BACKUP_CLEANUP_PENDING，保留证据；这是既有保护生效，不能越过它报普通授权失效。该场景日志留证后，确认无活动操作、候选不存在、原用户journal本来不存在，仅移除明确属于本次测试token的日志以隔离下一个测试，不称此为生产自动恢复。无未清理任务时再次备份，真实弹出“备份位置不可用/备份目录授权已失效/重新选择目录”，点击后打开原系统树选择器，BACK取消，不自动grant/重开预览。传输中SecurityException分类仍由夹具验证，本次实际验证的是撤权后的预检和错误UI。

**统一回归：** 21组最终套件通过，regression-final.json汇总每组证据。备份导出636/104场景、错误UI8、撤销85、worker122、checkpoint144、preview52、偏好25；搜索图标/索引、图标队列161、缓存Android真实SharedPreferences及PNG44、图标包失效18、Android资源ID80、圆框回退334、图标库页面14、延后来源、阴影/主题/解锁合同通过。光影Android隔离生命周期788、线程交接23011、恢复绑定2418通过，边界仍是受控scene/传感输入，不能代替手持可见输出。首次批量运行4个套件缺必要参数，属于调度错误，补齐后实际重跑通过，初次结果保留在regression-results.json；不能把其exit2当生产失败或隐藏。

**正式包与功能：** 正式v1.5.8/33、SHA256 343fd257b9b13abb989ff9d09bcb67ab61cb7d242152260e6755abb7ec937bea保留数据恢复安装、拉回哈希一致，v1/v2/v3及zipalign-P16通过，DEBUGGABLE已撤除。正式五轮底部上滑搜索五个常用图标、输入settings→实际启动com.android.settings.Settings、BACK并显式回Launcher、桌面设置打开/BACK，同PID25008；每轮截图逐一复核无空图标，限定错误日志无fatal。这是BACK/显式前台回归，不是系统HOME全面屏手势交接验收，不以此关闭A05或整体启动性能。

**恢复与交付：** 专用目录经精确文件名/哈希确认后仅删除本次归档并rmdir空目录，撤销仅本次测试URI。用户明确确认后，临时/backups授权也撤销，JDI持久授权最终为空，备份偏好恢复原值、原journal恢复缺失；原撤销快照SHA256不变。最后再次保数据恢复正式包并核对备份页“尚未选择/上次备份暂无/撤销2026-10-19 16:47”。偏好文件复核曾被adb shell换行转换误判，改exec-out确认原始字节，未作为生产故障。未更改布局/图标来源/主题/导航/刷新率/默认桌面或清数据。100项index binary patch不变，无add/提交/推送。更新本日志、功能报告、问题清单和专项计划；MEMORY.md未更新。全部证据build/consolidated-acceptance-20261020/verification.json及各场景日志/截图。

**仍未完成：** 冷启动总体/物理首帧首交互、暂停的Folder卡顿、长期PSS/Graphics与GPU/慢网压力、三星S25U Share现场和完整ROM/显示矩阵、严格16KiB原生库、系统HOME交接与手持光影、哈希旧档迁移、隔离环境完整恢复与多provider/大档/中途撤权/断电。当前安全同名替换未实现，继续保护旧文件并要求换名。不能把本机本地provider闭环或21组合同检查换算成全部优化完成。

<a id="2026-10-20-a07目录授权失效saf异常分类阻止误回退及复用目录重选入口"></a>

#### A07目录授权失效：SAF异常分类、阻止误回退及复用目录重选入口

**根因与负例：** SAF查询/创建/复制等操作的SecurityException原先落入两保存入口通用BACKUP_EXPORT_FAILED/BACKUP_COPY_FAILED；rename捕获所有Exception当不支持重命名，权限拒绝也继续fallback创建第二目标。旧源码隔离负例准确失败SAF permission denial must report lost directory access scenario=permission-query。原失败弹窗只有说明，没有直接目录重选动作。

**最小修复：** DesktopBackupController.writeToTree将初始目录查询和partial创建并入原URI拥有/异常清理范围，在这个SAF导出边界检查异常及cause链SecurityException，清理本次候选后转BACKUP_LOCATION_PERMISSION_LOST并保留原cause。rename遇直接或包裹权限异常重新抛出，禁止继续fallback创建；普通rename失败仍保留原兼容回退。不对全局/local snapshot/database异常做统一权限分类，普通IO和本地快照SecurityException保持原错误。删除被拒绝仍由原pending清理/日志机制保留URI，权限模拟恢复后只删本次候选，不动旧备份或上次记录。

**设置入口与复用：** MaintainedLauncherSettingsHost用小型showBackupFailureDialog共享两处已有错误展示（保存Listener和预览Listener），只对LOCATION_PERMISSION_LOST显示原风格choice，用户点击“重新选择目录”才调用已有openBackupTree(activity,false)，取消不调用；复用原SDK分流/存储权限/系统ACTION_OPEN_DOCUMENT_TREE/持久授权/ActivityResult入口，不创建新Picker或Manager，不自动grant、不恢复失败预览。只读、普通复制、坏日志、元信息pending继续各自信息提示。原版APK仍缺失，clean/raw/maintained此前无此移植SAF导出Owner，沿当前链路修复，不改原版桌面核心。

**隔离验证：** 原81场景保留，新23场景，两条实际保存方法分别覆盖查询、创建、打开、回读、rename直接/包裹SecurityException、fallback第二目标创建/打开/回读权限失效；断言不提前发布元信息、rename拒绝不创建第二目标。再覆盖复制中模拟撤销后清理仍被拒绝、日志URI保留、模拟恢复访问后清本次候选且旧文件/元信息保持；普通IOException及本地快照SecurityException负控不误分权限。636检查/104场景通过。新UI夹具提取实际showBackupFailureDialog/backupResultMessage，8检查验证不自动开picker、明确重选、取消无动作、正向回调使用原picker且continuePreview=false、其他错误不误弹授权选择。撤销保护85、worker122通过，共851项。文件/FD/日志/锁和保存方法是真实JVM执行，provider/Android JSON/AtomicFile/本地快照/UI是受控夹具，不称Android真实撤权验收。

**构建与真机：** build.bat、签名v1/v2/v3、zipalign-P16、v1.5.8/33通过，SHA256 343fd257b9b13abb989ff9d09bcb67ab61cb7d242152260e6755abb7ec937bea；相对35c6cf仅classes2.dex非签名成员变化。V2458A/API36保数据安装，拉回APK哈希一致；正常HOME/图标、设置/备份页/底部上滑搜索常用图标基础回归，同PID及限定日志无fatal/Journal异常。从现有“备份位置”实际打开com.android.documentsui/.picker.PickActivity，BACK先回根目录、再BACK取消回备份页，位置仍“尚未选择”。未点“使用此文件夹”、未创建目录/授予新URI权限/改系统权限，未实际备份恢复。真机验证的是共用picker的打开取消，不是新权限错误弹窗或真实撤权故障；两者严格区分。

**修改与交付：** 生产仅DesktopBackupController.java、MaintainedLauncherSettingsHost.java，测试tools/tests/backup_export/run_tests.py。100项暂存binary patch逐字保留，无add/提交/推送；MEMORY.md未更新，本日志/功能报告/问题清单/专项计划更新。证据build/backup-permission-loss-20261020/verification.json、device-verification.json、before/after-final/build/install/签名、picker route和取消截图。未切图标来源/主题/布局/默认HOME/导航/刷新率，Folder性能继续暂停。

**下一项与边界：** 下一项补齐专用SAF测试目录的端到端导出、回读和取消验收，先明确测试目录/文件及恢复清单；新增SAF目录授权需用户明确允许并选择，不自动改用用户已有备份。实际撤权/云盘断流/外置卡/进程退出/断电矩阵、安全同名替换仍未完成；当前同名保存仍保护旧文件并要求换名。本批不把851项夹具或只读页面回归当作全部备份恢复验收。原FileNotFoundException兼容映射保持，未扩称已区分所有文件缺失原因。

<a id="2026-10-20-a07上次备份元信息以complete为提交依据保留已完成文件并补写记录"></a>

#### A07上次备份元信息：以COMPLETE为提交依据，保留已完成文件并补写记录

**根因与负例：** execute和copyPreparedArchive都先提交上次备份时间/名称/URI，再写COMPLETE；后者失败，外层捕获删除新文件，但偏好仍指向它。SharedPreferences.commit返回false也可能已更新内存，不能假定元信息未变化。新旧源码负例准确失败failed completion must preserve previous backup metadata scenario=complete，原先的有效上次记录被覆盖。

**最小协议与Owner：** 复用现有Controller/Journal/操作锁。两保存路径统一调用小型completeBackup/publishCompletedBackupMetadata helper（原实现重复且无共享发布入口，需抽取这段交接；未新增Manager/Service）。最后一个取消检查后进入finalizing：先写并确认COMPLETE，再更新元信息，时间取已确认entry.updatedAt，URI用实际partialUri、名称为本次文件名，统一清last_backup_incomplete。Journal增加可选completedFileName，保存恢复所需名称，旧记录缺字段仍兼容，不改变备份归档格式。

**失败和恢复边界：** 尝试COMPLETE以后不在外层删除文件或重写FAILED，避免“已发布但回读失败”的COMPLETE被降级并删除实际完成文件。日志仍COPYING时，后续原cleanup只删本次未提交候选，旧元信息不动；实际已COMPLETE时，后续cleanup/新备份准入只补写元信息，不删文件或改变完成时间。偏好commit失败提示BACKUP_METADATA_PENDING/“备份文件已保存，但完成记录尚未更新”；新操作在补写仍失败时释放瞬时锁并阻止覆盖旧journal。只在原启动/主动备份入口尝试一次，不循环重试。旧COMPLETE缺新字段继续原行为，不猜URI对应文件名。新偏好即使已在内存生效，也指向保留的有效文件；不承诺commit=false一定保留旧内存值。原版APK仍缺失，clean/raw/maintained此前无本移植SAF交接Owner，按当前结构修复。

**修改与验证：** DesktopBackupController.java、BackupOperationJournal.java、MaintainedLauncherSettingsHost.java、tools/tests/backup_export/run_tests.py。测试新增提取实际execute，与原实际copyPreparedArchive各跑完成写失败/静默失败/同步失败/已发布但回读失败、偏好提交失败、fallback偏好失败和成功；种下真实临时旧备份及旧元信息，验证旧文件字节保持、不提前发布记录、日志主导保留/清候选、pending阻止新操作并释放锁、重读日志从新Context重建元信息、重复补写保持完成时间、旧COMPLETE无新字段兼容。原64场景保留；其中COMPLETE/prefs失败从“立即删新文件”调整为显式验证提交阶段保留、受journal追踪与后续恢复，不把预提交取消/写入/回读/校验/fallback失败的清理断言移除。491检查/81场景、撤销85、worker122，共698项通过。

**验证边界：** 生产方法/Journal/Lock/FileUtils与文件/FD为实际JVM执行，归档/数据库快照/Android JSON/AtomicFile/provider/偏好为受控夹具。新Context模拟重建，不是实际结束Android进程或断电；偏好夹具保留commit失败可更新内存的行为，未做真实SharedPreferences磁盘故障。没有在手机执行备份/恢复或调整目录授权。未覆盖外部用户主动删除已完成备份后的显示一致性，也不以本批解决provider非事务URI间隙。

**构建与真机：** build.bat、签名v1/v2/v3、zipalign-P16、v1.5.8/33通过，SHA256 35c6cf9daa6cb47d93d9cf45b73d0c28da55888b9e9634bbaecb9052d6ee7a2e；相对e2231f仅classes2.dex非签名成员变化，100项暂存binary patch逐字保持，无add/提交/推送。V2458A/API36保数据安装，拉回APK哈希一致，正常HOME/图标、设置与只读备份页返回、底部上滑搜索常用图标基础回归，同PID及限定错误日志无fatal/Journal错误；没有诱发元信息失败，不称真实SAF完整验收。未改主题/布局/导航/刷新率/图标来源/默认桌面/权限，Folder性能暂停。

**交付及下一项：** 本日志/功能报告/问题清单/专项计划更新，MEMORY.md未更新。证据build/backup-metadata-publication-20261020/verification.json、device-verification.json及before/after-final/build/install/签名/截图。下一项检查导出过程中目录授权失效：SecurityException目前可能落入通用复制/导出失败，而非目录授权失效提示，先用受控权限异常复现并核对重新选择目录入口，再最小修复，不擅改手机权限。真实provider/外置卡/云盘断流、进程终止和断电矩阵、安全同名替换仍未完成。

<a id="2026-10-20-a07备份日志写入确认fd同步与逐字节回读失败不发布内存状态"></a>

#### A07备份日志写入确认：FD同步与逐字节回读，失败不发布内存状态

**根因与负例：** BackupOperationJournal.write只调用finishWrite便返回true，未同步FD或回读，还在实际写前改变Entry状态/时间/错误码。参照当前RestoreOperationJournal可知AtomicFile.finishWrite可能只记录发布失败而不抛异常。新负例对旧实际源码准确失败unpublished or unsynced checkpoint must not report success scenario=silent-finish：未发布候选却返回成功。

**最小实现：** 生产仅BackupOperationJournal.java修改。复用现有Restore日志策略：先保持原有read预检，构造候选JSON及局部状态/时间/错误码，结构验证后转字节；候选超过既有128KiB读取上限时在startWrite前拒绝，防止发布不可回读的文件。write后FD.sync→finishWrite→原readBytes逐字节Arrays.equals校验，全部通过才更新Entry并返回true。finishWrite后清空output，不因回读失败再对已发布文件执行failWrite；仍持有输出的失败路径尽力failWrite，回退自身异常附加到首个异常并记BACKUP_JOURNAL_WRITE_FAILED，返回false。没有复制Restore类或新增Manager/日志/归档结构，不修改UI或备份/恢复流程。原版APK仍缺失，clean/raw/maintained此前无本移植日志Owner，复用当前项目Restore实现优先。

**验证：** 原54场景全部保留，新增10场景，356项/64场景导出检查通过：finish不发布、同步阶段关闭FD模拟sync失败、发布后读失败、合法JSON多一空格造成字节不一致、failWrite自身异常、过大候选、COMPLETE静默失败不报成功并清新目标、IDLE静默失败阻止新操作/重试、PREVIEW_READY静默失败不发布预览、首次写未发布保留.new并阻止不安全reset。验证写失败时Entry状态/时间/错误码不先行改变，旧检查点仍在时可确认重试；发布已发生但回读失败时只保证返回false和内存不发布，不冒称文件一定回到旧版本。85撤销保护、122恢复worker回归通过，共563项。实际生产方法/Journal/Lock/FileUtils及真实JVM文件/流/FD.sync，AtomicFile/JSON/provider/归档/UI为受控夹具；sync失败是关闭FD注入，静默发布/回读异常由夹具模拟，不是Android真实磁盘故障或硬断电验收。

**构建及真机：** build.bat、签名v1/v2/v3、zipalign-P16、v1.5.8/33通过；SHA256 e2231f7af98254a0d2c37c6f5bb211531d5335239a430459b3a434e3b8c63500，相对67b4e9仅classes2.dex非签名成员变化，100项暂存binary patch逐字保持。V2458A/API36保数据安装、APK拉回哈希一致；正常启动/图标、设置与只读备份页进入返回、底部上滑搜索常用图标基础回归通过，同PID且限定错误日志无fatal/备份日志错误。未在真机造写入故障、实际备份恢复或调整目录权限；不称真实SAF/损坏恢复/长稳全矩阵完成。未切默认桌面/导航/刷新率/图标来源/主题/布局；Folder性能仍暂停。

**交付与后续：** 修改日志类、tools/tests/backup_export/run_tests.py及本日志/功能报告/问题清单/专项计划，MEMORY.md未更新，无add/提交/推送。证据build/backup-journal-durability-20261020/verification.json、device-verification.json和before/after-final/build/install/签名/截图。下一项核对“上次备份”元信息发布顺序：当前时间/名称/URI偏好在COMPLETE日志之前提交，日志失败后原捕获分支会删新文件，界面可能还指向已删的文件；先建立元信息保持负例，再最小修复。实际provider非事务URI窗口、断电/云盘/外置卡矩阵、安全同名替换仍未完成；sync和回读确认不等于物理介质绝对持久化保证。

<a id="2026-10-20-a07备份日志损坏或读失败停止备份并保留证据预览只在checkpoint成功后发布"></a>

#### A07备份日志：损坏或读失败停止备份并保留证据，预览只在checkpoint成功后发布

**根因与负例：** BackupOperationJournal.read捕获所有Throwable后new Entry/IDLE；Entry.fromJson以optString默认关键字段，缺state会当IDLE、未知state当FAILED。空文件、截断/缺字段JSON或读取失败可能绕过旧操作保护，后续write/reset覆盖记录。旧实际源码负例准确失败corrupt backup journal must not appear idle。原测试首次新增JSON字面量转义有误导致夹具编译失败，已改用JSONObject构造后再取得上述真实负例，没有当生产失败样本。

**读取与覆盖保护：** 参照现有RestoreOperationJournal的hasJournalFiles/readBytes/缺失判断，检查base/.bak/.new，只有可读可访问父目录内确认无日志文件且openRead报不存在才返回IDLE。其余IO/运行时读取问题抛BACKUP_JOURNAL_READ_FAILED；解析失败、缺token/state/stagingPath/partialUri、未知state或IDLE仍带资源，抛BACKUP_JOURNAL_CORRUPT。destinationUri仍是可选，旧有效日志兼容。Backup沿用boolean写接口，read以带errorCode的运行时JournalException区分两类，避免大改原调用签名；write在startWrite前预读旧日志并验证待写结构，损坏/读失败时返回false，reset也不得覆盖原证据。不是增加另一套日志或自动删除损坏文件。原版APK仍缺失，clean/raw/maintained此前无本移植日志Owner，优先复用当前项目已验证的Restore日志读取模式，不更改原版Launcher核心。

**调用链最小收口：** 新备份准入捕获JournalException后释放瞬时owner/清running，以明确损坏或读失败文案回调；启动异步cleanup原RuntimeException边界继续兜住，不让Launcher启动崩溃。预览后保存若首次read失败，错误处理里再次read也可能失败，现单独捕获保留旧文件，仍交付完成回调并finally释放锁。state和PREVIEW_READY检查write返回；预览对象移到成功checkpoint之后赋值，避免失败却持有无效预览。SettingsHost补齐两错误提示，不引导用户清应用数据，不自动reset坏日志。

**修改与验证：** BackupOperationJournal.java、DesktopBackupController.java、MaintainedLauncherSettingsHost.java、tools/tests/backup_export/run_tests.py。原39场景保持，新15场景覆盖空/截断/缺字段/未知state/IDLE含资源、坏日志write/reset字节保持及阻止新备份/不删文档/正确回调与锁释放、读取IO异常、预览保存读失败且错误记账也失败、真正缺失、仅.new、.bak恢复、128KiB超限、预览两个checkpoint失败与正常确认。314导出检查/54场景、85撤销保护、122恢复worker，共521项通过。实际生产方法/Journal/Lock/FileUtils+真实JVM IO，Android JSON/AtomicFile/provider/归档/界面为受控夹具；没有把JVM注入称作Android真机损坏日志验收。

**构建与设备：** 复核时调整预览发布顺序后重新完整build.bat，最终包签名v1/v2/v3、zipalign-P16及v1.5.8/33通过，SHA256 67b4e922fcf406a446306072cdcfb96cfa3fb9467d9c161544b04c5563a68b3a；相对950d2d仅classes2.dex非签名成员变化。V2458A/API36保数据安装，系统安装页确认后Success，拉回APK哈希一致；正常HOME/图标、桌面设置、只读打开桌面备份与恢复页并返回、底部上滑搜索五个常用图标显示完成，同PID且限定本PID BackupJournal/AndroidRuntime/DEBUG/libc日志无读失败/损坏/fatal。备份位置仍未选择，没有选目录/实际备份/恢复、没有写入或损坏手机日志；只证明正常入口基础回归，不证明真实故障或全SAF验收。未改布局/图标来源/主题/导航/刷新率/默认桌面/权限，未恢复Folder性能采样。

**交付与下一项：** 100项暂存binary patch逐字不变，无add/提交/推送。MEMORY.md未更新，本日志/功能回归/问题清单/专项计划更新。证据build/backup-journal-guard-20261020/verification.json、device-verification.json及before/after-final/build-final/install/签名/截图。下一项检查BackupOperationJournal.write在AtomicFile.finishWrite仅记录错误但不抛异常时仍返回true：沿现有Restore日志的FD.sync及写后字节回读校验建立负例和最小修复。该静默持久化边界本批未关闭；非事务provider URI间隙/真实云盘与外置卡/断电矩阵、安全同名替换仍待办。损坏日志保持阻断和原证据，不承诺自动修复未知内容。

<a id="2026-10-20-a07-saf回退复制确认partial删除后才交接最终uriandroid16真机基础回归"></a>

#### A07 SAF回退复制：确认partial删除后才交接最终URI，Android16真机基础回归

**根因与负例：** rename不支持时复制到final并校验成功后，writeToTree调用deleteDocumentQuietly(partial)，无论删除是否成功都把entry.partialUri换成finalUri并清空destinationUri，随后可写COMPLETE，丢失残留partial的追踪。旧源码负例准确失败fallback cannot complete with unremoved partial scenario=fallback-delete-denied，final和partial都在却已报告成功。

**最小修改：** 只改DesktopBackupController.writeToTree这一交接点：复用上批deletePendingDocument，只有delete成功或成功空查询确认不存在，才把日志交给finalUri。拒绝/异常/查询null或异常则抛BACKUP_CLEANUP_PENDING，保留已持久化的partial和destination两URI，由原异常分支尝试清理本次输出、原调用者记FAILED，再由已修启动清理/新备份准入处理。若新目标也删不掉，两者都仍有记录；不提前发布成功元信息，不把未清理文件标COMPLETE。只是本次导出失败，未访问/删除任何旧用户备份。不新建Manager/重试/日志结构，继续保留正常rename/fallback和原格式。原版APK归档仍缺失，clean/raw/maintained没有此移植SAF Owner可搬用，沿现有代码修复。

**修改文件与隔离验证：** 生产仅DesktopBackupController.java，测试tools/tests/backup_export/run_tests.py。原32场景断言保留，新增7场景：partial删除false/抛错、删除拒绝且查询null/异常、两个目标均拒绝删除、partial删除后交接checkpoint失败、delete返回false但成功空查询确认不存在。验证失败不发布元信息、保留两URI/FAILED、下一次清理仍保留被拒绝目标、权限模拟恢复后清理/IDLE、正常完成不误拦。实际方法体+真实JVM文件/FD/流/Journal/Lock，provider/UI/归档验证是夹具；247项/39场景通过，撤销保护85和worker122通过，共454项。

**构建与真机：** build.bat、v1/v2/v3签名、zipalign-P16、v1.5.8/33通过，SHA256 950d2d82072097bc76a1e6e0d46d75a5bc80f03b1e5297d85277e2fbcb77e968；相对50b43d仅classes2.dex非签名成员变化，100项暂存binary patch逐字保持。期间检测到V2458A/API36真机重连，沿用此前保数据安装与回归授权；系统外部来源确认后install -r成功，拉回base.apk哈希一致。图标截图、既有文件夹打开/外部点击关闭、底部上滑搜索五个常用图标、settings查询匹配并打开com.android.settings/.Settings、BACK回Launcher、桌面设置打开/BACK回桌面完成。BACK从系统设置回的是原文件夹界面，没有称其返回搜索页。桌面PID前后保持，限定本PID AndroidRuntime/DEBUG/libc日志未见FATAL EXCEPTION/Fatal signal；不等于完整ANR/长稳验收。

**测试工具与设备状态：** 旧TouchInput shell进程两次被系统结束（137/Killed），失败留证，未当成Launcher崩溃；改用设备平台input touchscreen swipe后实际打开搜索。临时DEX按本地SHA256确认身份后删除。最终回到原先第二桌面页；没有切默认HOME、导航/刷新率、图标来源/圆框/主题/布局或权限，没有在真机执行备份/恢复。功能查询可能按既有逻辑产生使用记录，不宣称应用数据逐字不变。未测试真实SAF拒绝删除路径，不以UI回归替代provider故障验收。Folder只做基础开关，不恢复已暂停的性能采样。

**状态与下一项：** 已更新本日志/功能报告/问题清单/专项计划，MEMORY.md未更新；无add/提交/推送。证据build/saf-fallback-cleanup-20261020/verification.json、device-verification.json、before/after-final/build/install日志及截图。下一项优先处理BackupOperationJournal.read对损坏/读取失败一律返回IDLE：先用截断JSON/读取异常负例验证会否覆盖旧记录，再参照既有RestoreOperationJournal的失败关闭规则最小修复。静默持久化失败、非事务URI创建/rename窗口、真实云盘/外置卡/断电矩阵和安全同名替换仍未完成。

<a id="2026-10-20-a07-saf启动清理删除失败保留记录新备份不覆盖待清理日志"></a>

#### A07 SAF启动清理：删除失败保留记录，新备份不覆盖待清理日志

**修前证据与根因：** cleanupInterruptedBackupNow调用deleteDocumentQuietly吞掉false/异常后仍reset。受控provider拒绝删除时文件尚在，旧源码负例准确失败denied cleanup preserves journal URI and state scenario=delete-denied。仅保留journal仍不够：新备份原先直接写入新操作，可能覆盖待清理URI。

**最小修复：** 继续由DesktopBackupController和原BackupOperationJournal/操作锁拥有清理。逐项删除成功才清空对应URI，两个相同URI仅处理一次，未清理staging也保留路径；有剩余或偏好提交失败时保持原非终态和剩余资源，记录BACKUP_CLEANUP_PENDING，不reset。只有资源处理成功后才写新IDLE，检查write返回值。删除返回false/抛异常后，只认成功且空的文档查询为已不存在；null/查询异常一律保留。这样即便上轮删除成功后checkpoint/reset失败，下次也能确认旧URI已不存在并继续。新预览/直接导出worker持已有操作锁先调用同一清理入口；未完成则释放本次瞬时owner、清running并提示pending，不写入新journal。没有循环、定时重试、目录扫描或新Manager；每次启动/主动备份仅一次清理。COMPLETE仍直接返回，不把成功备份当垃圾删除。SettingsHost补齐明确pending结果文案。

**修改与参考：** DesktopBackupController.java、MaintainedLauncherSettingsHost.java、tools/tests/backup_export/run_tests.py。原版APK仍缺失；此前clean/raw/maintained未找到本移植SAF Owner，本批沿当前实现修复，没有替换原版核心或改归档格式。同名保存仍拒绝覆盖，保留换名提示及旧圆框/撤销快照修复。

**验证：** 184项/32场景SAF实际方法体隔离检查通过，增加拒绝/抛错、下一轮恢复、阻止新操作且释放锁/保留旧journal、两目标仅一个可删、进度checkpoint失败、reset失败后空查询重试、null/异常查询不证明不存在、COMPLETE不删文件。保留原导出取消/复制/校验/URI变化/fallback/偏好/日志失败断言；85项撤销保护、122项恢复worker通过，共391项。provider/UI/归档验证是受控夹具，文件/FD/流/Journal/Lock是真实JVM IO；首轮编译发现Log夹具缺少平台已存在的两参w重载，补齐夹具后通过，非生产API错误。未执行真实provider进程退出/硬断电或权限恢复矩阵。

**交付：** build.bat、v1/v2/v3签名、zipalign-P16、v1.5.8/33通过；SHA256 50b43d9ee4c0318c0cea142800de24434fda9b61575f8fba645e8b60fc77950e，相对a79e13仅classes2.dex非签名成员变。100项暂存binary patch逐字不变，无add/提交/推送。ADB无设备，未启动模拟器、未安装或操作用户备份。MEMORY.md未更新；本日志/功能回归/问题清单/专项计划更新。证据build/saf-cleanup-retry-20261020/verification.json及before/after-final/undo/worker/build/signature/align日志。

**边界与下一项：** 本批修复已记录未完成导出的启动清理和新备份准入；不是全部SAF失败恢复验收。journal损坏被read当IDLE/静默持久化失败、非事务URI窗口、并发目录改动、真实云盘/外置卡/权限撤销未关闭。另审查发现fallback成功路径仍以deleteDocumentQuietly删除partial后即丢弃其追踪，拒绝删除可能遗留临时文件；下一批先对此建立负例并修复成功路径的清理确认/记录交接，不动用户备份。Folder性能继续暂停，完整安全同名覆盖仍未实现。

<a id="2026-10-20-a07-saf同名备份封住先删旧文件入口目录查询失败停止写入"></a>

#### A07 SAF同名备份：封住先删旧文件入口，目录查询失败停止写入

**根因与修前证据：** writeToTree在新partial创建前deleteDocument(existing)，同名覆盖后取消会丢旧备份。追加真实方法隔离负例，旧源码准确失败same-name attempt preserves old document scenario=cancel documents={}。仅把删除移到partial校验之后仍无法保护后续rename、复制、偏好或COMPLETE失败，不能声称安全覆盖已实现。

**本批范围与行为变化：** SAF缺少统一原子替换能力，本批采用保守保护而非完整替换协议：Controller遇到同名目标一律BACKUP_NAME_EXISTS，即使旧调用者传overwrite=true也不删除/写入旧文档；用户需换名保存。SettingsHost移除原“覆盖”确认路径，提示“已保留同名备份，请更换名称后保存”，预览页不丢弃，可编辑名称后重新保存。后台仍重新检查冲突；复用现有目录枚举，拆出findTreeBackupChecked供实际写入使用，query返回null或抛异常时中止，不能把查询失败当作不存在。公共UI查询入口继续记录失败并返回null，后台会严格复查。两处结果提示补齐NAME_EXISTS/TREE_LIST_FAILED，不再显示泛化复制错误。不新增Manager/缓存/归档格式；原版APK归档缺失，clean/raw/maintained未找到这套SAF导出Owner，不冒称原版有原子覆盖方案。

**修改文件：** DesktopBackupController.java、MaintainedLauncherSettingsHost.java及tools/tests/backup_export/run_tests.py。保留旧图标圆框、撤销快照、导出清理修复。原overwrite参数保留兼容旧调用签名，当前明确不执行覆盖；不是将覆盖功能标记完成。

**验证：** SAF夹具160项/24场景、撤销快照85项/12场景、恢复worker122项通过，共367项。新增断言覆盖overwrite=true时旧文档URI/字节保持且不创建目标、overwrite=false冲突、目录null/异常时零创建；保留原20场景的写入/回读/校验/取消/rename/fallback/日志/偏好失败、两目标启动清理和旧journal兼容断言。采用实际生产方法体、实际Journal/Lock/FileUtils及真实JVM文件/描述符，provider/界面/归档验证是夹具，未把同名短路后的故障注入说成执行了写入或取消。UI仅编译检查，未实际操作预览换名。

**交付：** build.bat、签名v1/v2/v3、zipalign-P16、v1.5.8/33通过。SHA256 a79e13dd8937a0ab163778694d95b0657b0469288cc12c741c3ffde9f3fd9ab6；相对8bb7d2仅classes2.dex非签名成员变化。100项暂存binary patch逐字保留，无add/提交/推送。ADB无连接设备，未启动模拟器、未安装、未操作任何用户备份。MEMORY.md未更新；开发日志/功能回归/问题清单/专项计划已更新。证据build/saf-overwrite-20261020/verification.json及before/after-final/undo/worker/build/signature/align日志。

**未完成与下一项：** 本批只消除已识别同名目标的破坏性覆盖入口；完整同名安全替换协议仍未实现。目录被其他进程并发改动、provider非事务create/rename、进程在URI回传与日志记录之间退出、日志损坏/静默持久化失败、真实云盘/外置卡/权限撤销仍未验。下一批先修现有启动清理中deleteDocument失败被吞掉、journal仍被reset的证据丢失问题：拒绝删除负例→保留未清理URI及状态→下次清理恢复；不扫描用户目录、不无限重试。Folder性能继续暂停。

<a id="2026-10-20-a07-saf导出补齐失败清理及实际uri追踪取消不再误报复制失败"></a>

#### A07 SAF导出：补齐失败清理及实际URI追踪，取消不再误报复制失败

**修前证据与根因：** writeToTree创建.partial后即写入/回读，调用者的partial只在整个方法返回后赋值；中途取消/复制或校验失败，外层捕获到的URI仍为null，遗留.partial。新隔离负例准确失败failed/cancelled export leaves no new documents scenario=cancel，残留doc://1=backup.slauncherbackup.partial。重命名可能返回不同URI，旧entry.partialUri未更新；元信息提交失败后清理旧URI会漏掉已重命名文件。rename不支持时二次复制同时存在两份文件，旧journal仅记.partial，进程中断后不知道新目标。另外预览后保存路径把BackupCancelledException映射为BACKUP_COPY_FAILED。

**最小修复：** 继续由现有DesktopBackupController.writeToTree拥有本次创建的文件，方法内异常清理原partial和新目标，再原样抛回调用者；调用者在成功返回后直接持有实际finalUri。重命名成功及时记录实际URI；回退复制期间在BackupOperationJournal增加可选destinationUri记录第二目标，旧journal缺字段仍按空值读取，不改备份归档格式。创建/转换目标后检查COPYING日志写入结果，失败不继续写，COMPLETE记录失败也不提示成功；原启动cleanup处理两个URI，重复URI只删除一次。预览保存取消写CANCELLED并返回BACKUP_CANCELLED/已取消。正常开关/布局/图标/动画无变化，不创建新Manager或存储体系。clean/raw/maintained无这套移植SAF Owner可直接替换；原APK归档仍缺失，未冒称新反编译。

**验证：** tools/tests/backup_export/run_tests.py提取实际writeToTree/copyToUriAndVerify/copyPreparedArchive/cleanup及取消、错误、回调方法，编译实际BackupOperationJournal/Lock/FileUtils/Result。文件、JVM FileDescriptor、流、checkpoint、锁和staging是真实临时IO，DocumentsContract/ContentResolver/UI/归档验证为受控夹具，未访问用户目录。20场景133项通过：取消、写入/回读/长度/校验失败、不可写/创建失败、fallback第二目标失败/取消、重命名URI改变或保持、rename不支持/抛错、偏好或COPYING/COMPLETE写入失败、两目标启动清理、旧journal缺字段读取；保留原文件清理/锁释放/状态断言。旧撤销保护85、异步恢复worker122回归通过，共340项。本批未使用真实SAF provider，也未实际终止导出进程，不把fixture模拟两目标恢复写成真实重启验收。

**交付与保护：** build.bat/签名v1-v3/zipalign-P16/v1.5.8/33通过，SHA256 8bb7d2b0df9dac5745ee4057e474353e3c44041a700673bb88936b531e667e1b，相对8b782仅classes2.dex非签名成员变化；既有圆框和旧撤销快照修复保留。100项暂存binary patch逐字保持，无add/提交/推送。ADB当前无连接设备，未启动模拟器、未安装或操作用户备份。本轮只改Controller/导出日志及新增测试；MEMORY.md未更新，更新开发日志/功能报告/问题清单/专项计划。

**剩余与下一项：** 明确未关闭覆盖同名备份的安全边界：existing在新partial写入/校验前就被deleteDocument删除，取消仍可能丢旧备份，下一批优先做保留旧文件的替换协议。provider拒绝删除、返回后尚未来得及记录URI即进程退出、日志损坏读取/静默持久化失败、真实云盘/外置卡/SAF长断流及权限撤销矩阵仍需验，不称完整SAF取消安全。Provider清理仍是best effort；没有增加未经证据的重试或扫用户目录。Folder性能继续暂停。证据build/saf-export-cleanup-20261020/verification.json及before/after-final/undo/worker/build日志。

### 2026-10-19

<a id="2026-10-19-a07取消安全保留旧撤销快照修复按字符串引用释放操作锁"></a>

#### A07取消安全：保留旧撤销快照，修复按字符串引用释放操作锁

**两项修前证据：** 现有createRollbackAndTransition在CREATING_ROLLBACK后先删rollback_latest，导出新快照时取消仍会丢旧撤销包；新隔离负例准确失败old undo bytes retained scenario=cancel-export。另BackupOperationLock.release以AtomicReference.compareAndSet(token,null)按引用比较，日志反序列化得到的等值新String虽然owns=true却无法释放；独立负例equal decoded token releases operation失败。上批将组合测试残留owner暂列夹具问题，现在已确认它对应真实release缺陷，修正此前结论。

**实现与Owner：** 继续使用现有Controller/Journal/Guard/Lock，不新增Manager/日志格式/表。新快照放rollback_latest/preparing_TOKEN，开始创建前把候选路径持久化，取消/构建失败/交接失败仅删本次候选和staging，旧archive不动。正常恢复COMMITTED后，原后台首帧cleanup或启动Guard在既有跨进程writer lease下，复制候选到publish.tmp→FD.sync→SHA256校验→同文件系统Os.rename原子替换正式archive。候选在CLEANING/IDLE持久化前保留，发布失败保留COMMITTED和文件，启动可重试；ROLLED_BACK保留原旧撤销包，仅清候选。旧journal直接指向rollback_latest的路径继续兼容。Lock先取当前owner、按token内容核对，再CAS同一个owner对象，等值token可释放、旧token不释放新owner。此前clean/raw/maintained无本移植JSON快照Owner可搬用，修当前链路；原APK归档缺失未冒称新反编译。

**被撤回方案与失败留证：** 初版候选发布曾用AtomicFile，Android9真机EACCES验证发现旧实现备份rename失败后仍可能打开既有目标写入，不能满足此处的旧撤销文件保护，已经撤回并改为上述临时文件+Os.rename，最终生产没有AtomicFile快照发布。第一轮设备新模式误用旧case目录中刻意损坏的journal，报CORRUPT；给新模式独立子目录后重测。两项失败均保留日志，不算用户Launcher崩溃或通过样本。

**回归：** 新run_undo_preservation_tests.py编译实际Controller/Guard/Lock/Journal/文件工具，85检查/12场景通过，覆盖导出/归档/校验失败、两个取消点、交接失败、checkpoint失败、成功发布、恢复回滚保留旧包、发布rename/源缺失失败与重试、reset失败后CLEANING恢复及等值/过期锁token。checkpoint144和异步worker122通过；旧guard的终态reset失败预期改为保留新增的耐久CLEANING状态，未删除原文件保留断言。主题回退31先前回归通过，本批不计入上述351项最终JVM总数。

**真机隔离：** X21A/API28实际Android AtomicFile/JSON/OS权限/文件重命名及测试进程SIGKILL/新进程重试：平台57、worker7、cleanup13、两组restart各6、torn journal4、新快照16、快照restart3，共112检查通过。新快照EACCES旧文件字节保持，撤销快照临时文件写半后结束的是独立probe，新进程读到完整旧包并发布正确候选。用户Launcher PID7133前后不变，无APK安装/用户布局恢复；三处本批临时工作区按summary或DEX哈希精确识别后清理。边界仍是Android+归档/DB/主题夹具，不称完整真实SAF备份恢复、硬断电或所有ROM验收。

**交付及后续：** build.bat、v1/v2/v3签名、zipalign-P16、v1.5.8/33通过，最终SHA256 8b782490cdaf6d615cb4e1a3b8f3e7f80da9b317ac981ba114502ea80b83a36e，相对45859仅classes2.dex非签名成员变更，图标圆框修复保留。本批未安装，手机仍是上批已验证圆框包。100项暂存binary patch逐字保留，无add/提交/推送。MEMORY.md未更新；本日志/功能报告/问题清单/计划已更新。下一项检查备份导出到SAF时写入中断/取消与未完成文件清理边界，不恢复用户桌面；真实全恢复/空间极限/多ROM长稳仍未完成，Folder性能继续暂停。证据build/restore-undo-preserve-20261019/verification.json、before-undo/before-lock、after-final及device-rename。

<a id="2026-10-19-图标未命中圆框按实际来源判定保留选择并查恢复清理边界"></a>

#### 图标未命中圆框：按实际来源判定，保留选择；并查恢复清理边界

**用户确认现象：** 改进版/其他来源回退为应用原图时没有圆形框，不是已匹配图案消失。本批不把它误归为选择被自动重置或下载文件消失。历史10/12规则为透明模块图标按用户所选来源禁止回退圆框；本次用户明确希望未匹配原图使用圆框，按最新指令调整。

**根因与最小修改：** Raster已把未命中managed来源归为DEFAULT，但Host.desktopDefaultCircleEnabled再读持久化选择，IMPROVED/PACK/CUSTOM/RESOURCE选择会否决圆框。现Host保留单参入口，新增接收本次effectiveType的重载；准备/已准备复用/合成/纹理key四处传既有已解析类型，不额外查询图片或选项。原Renderer谓词仍仅DEFAULT可加框，更新说明为实际来源。无匹配时画原图圆框，命中时保留managed图案及原全画布，不改持久化来源、PNG、阴影、几何、ActiveIcon/Folder特殊边界。原DEFAULT defaultShape键由follow_app变circle，开关关闭及managed命中仍有各自键，已有版本字段/来源失效机制保留，不另加缓存或批量删除文件。原APK归档缺失，clean/raw/maintained无本Host policy可直接替换；复用当前四层Owner。

**验证：** 新run_fallback_policy_tests.py提取实际Host函数、实际Raster准备函数和实际defaultShape key表达式，搭配真实Android9 Canvas/Bitmap/Renderer；来源/PM/偏好为夹具。旧Host快照负例准确失败global=IMPROVED，修后334检查覆盖全局/单项选择、回退、开关开关、命中保持、来源到达/再次失效和key一致性。原Renderer59、实际准备/合成及所有权289检查通过；三个已有夹具只补新重载以继续编译，不改旧断言语义。没有以隔离图像测试冒称所有真实图标包/多用户/ROM完整矩阵。

**恢复清理审计：** discard READY在reset持久化成功后删本次staging、释放token；abortPreparation遇journal持久化失败保留文件/检查点，只释放瞬时owner，后续由现有恢复门处理；首帧cleanup在writer lease下重读token/状态，正常完成保留撤销包、撤销完成才清撤销包。checkpoint144、worker122回归通过，本批备份生产0修改。补试READY discard锁断言时发现原组合夹具继承前一个异步undo的UUID owner，不能作为生产锁泄漏证据；尝试已撤回，WorkerTest源码逐字恢复，失败日志保留。**尚未关闭：** createRollbackAndTransition在CREATING_ROLLBACK后先删除旧rollback_latest，再建新快照；取消/失败可能使旧撤销快照不可用。这是下一批优先故障注入和最小修复边界，不把现有回归写成完整取消安全验收。

**交付：** build.bat、v1/v2/v3签名、zipalign-P16、v1.5.8/33通过；SHA256 45859fbfc475cc53b0ef7b3ede348a64964ee13e165da3ce28d007cdcf11e056，相对82e244仅classes2.dex非签名成员变化，原Folder classes.dex保留。vivo X21A/API28保数据安装成功，安装拉回hash一致；正式一次Folder开关/图标、底部上滑搜索、实际settings查询/系统设置启动/BACK、桌面设置/BACK通过，同PID7133，截图另行人工核对。未切换图标来源/圆框设置/主题/布局/默认HOME/权限/导航；测试触摸DEX移除并回首屏。100项暂存binary patch不变，无add/提交/推送。

**边界与下一项：** 本次关闭用户明确的回退原图无圆框逻辑；成功下载后被删除/全图标包矩阵、Android16/高刷/多ROM长稳未验，不宣称Folder或冷启动提速。下一批处理“创建恢复前快照时替换旧撤销包”的取消与失败边界，先保留证据再窄改，仍不恢复真机用户布局。MEMORY.md未更新；更新开发日志/功能报告/问题清单/专项计划/图标合同。证据build/icon-fallback-circle-20261019/verification.json、before/after、renderer、compose及formal-ui。

<a id="2026-10-19-a07结构校验预览提前拒绝孤儿引用补齐文件夹环检查"></a>

#### A07结构校验：预览提前拒绝孤儿引用，补齐文件夹环检查

**根因和范围：** 归档预览经BackupValidator→LayoutSnapshotExporter.validate只做数量/字段/ID检查，未调用已有FolderTopologyValidator，孤儿子项可进入预览，到Importer调用同一拓扑Owner才拒绝；原Importer该项已在任何数据库写入前检查，不能称修前孤儿引用已破坏数据库。另一方面拓扑Owner只检查父Folder是否存在，自引用/互相循环引用的父ID都存在，缺少环检查，可能通过原导入前后两道校验。原版clean/raw及maintained沿FolderInfo/itemType=2、子项folderIndex引用父ID结构作对照；本轮原APK归档仍缺失，不冒称重新反编译。未无证据禁止所有历史嵌套或特殊页重复索引。

**最小修复：** LayoutSnapshotExporter.validate尾部接已有Topology校验，预览/导出/导入复用同一Owner；保留Importer原有显式前置/事务后置保护。FolderTopologyValidator把现有Folder映射记录为父ID图，源布局和数据库校验共用迭代查环；completed集合避免共享长链重复遍历、不递归，不新建Manager/格式/表。无环旧关系仍沿原规则通过。只修确定的引用与环边界，不把重复位置/所有特殊页面语义宣布全部覆盖。

**验证：** 扩展既有RestorePageProbe。修前Android9独立进程负例在archive structural validation rejects case 0断言失败，日志确认引用不存在Folder的预览漏检；shell退出137是该测试进程断言，非用户Launcher崩溃。修后143真实Android SQLite/JSON/AtomicFile检查通过（含原120回归）：正常父子、孤儿、自引用、双向环、重复ID均验证；异常导入前后原表行/页面和pending哨兵保持；DB校验一致；12000节点环拒绝且无栈溢出、长无环链和共享父路径通过。另checkpoint144通过，共287检查。此为隔离DB，包/Profile/图标边界夹具，未执行真实用户SAF恢复或断电。

**交付及保护：** build.bat/签名v1-v3/zipalign-P16/v1.5.8/33通过，SHA256 82e244dac24e2e698b49d8d8345593f6ef20b71cf1f0873e83f4a56a7b8ca7ff，相对上批55eb仅classes2.dex非签名成员变化。未安装、未动用户桌面库，真机X21A/API28的Launcher PID5750前后不变。两个成功目录按summary定位，失败目录按本批DEX SHA256精确匹配，三处临时/data/local/tmp工作区校验绝对前缀后清理，不删其他目录。100项暂存binary patch保持，无add/提交/推送。证据build/restore-structure-20261019/verification.json、before-assertion.log及final/device.log。

**风险与下一项：** 已有损坏的有环数据现在会明确拒绝导出/恢复，不静默改用户图标关系。A07真实归档/SAF/进程中断/分身多ROM和完整页面位置语义仍开放。下一项检查恢复取消与失败后的临时归档、旧撤销快照和操作锁是否被正确保留或释放，先做隔离故障注入。Folder性能继续按用户要求暂停。MEMORY.md未更新；本日志、功能报告、问题清单及计划更新。

<a id="2026-10-19-a07页面预览修复纯文件夹页面漏计隔离sqlite布局回归通过"></a>

#### A07页面预览：修复纯文件夹页面漏计，隔离SQLite布局回归通过

**明确根因：** BackupArchiveReader.ValidatedBackup.pageCount以folderIndex>=0排除子项，但原版itemType=2的根文件夹通常folderIndex=0，导致只有文件夹的桌面页也被排除。例如页面3只有一个空文件夹，预览原显示0页；同一布局导入器却按根文件夹占用该页。唯一用户端调用在MaintainedLauncherSettingsHost的preview_page_count。clean/raw FolderInfo和maintained FolderInfo均用itemType=2，当前Importer/Pending既有占位规则也将Folder纳入桌面页，直接复用该判定；本轮原APK归档缺失未冒称新反编译。

**最小修复：** 仅BackupArchiveReader.java把排除条件限定为非Folder且folderIndex>=0。保留集合去重、负页/负格排除和旧档folderIndex缺省-1，不修改备份格式/持久化数据/Importer/页面分配/动画或UI布局。未加入新的计数Owner。

**验证：** tools/tests/restore_pages/run_preview_tests.py编译实际Reader，JSON使用既有偏好测试夹具；修前准确失败pages expected=1 actual=0，修后52检查覆盖仅文件夹/空文件夹、多页/同页去重、子项内部页不计、特殊负页/负格、旧根表示与缺省字段、shortcut和0/1/999页及格位0/1/11/19。旧档偏好25回归通过。另用既有restore_profiles --pages在vivo X21A/API28的独立app_process运行实际Exporter/Importer/Pending/Topology及真实Android SQLite/JSON/AtomicFile，120检查通过，含12/20宫格、1000槽复用/容量耗尽事务回滚、特殊页保护、根文件夹占位、导出再导入。包/Profile/图标边界是夹具，非完整真实归档/SAF恢复。合计197检查，不重复性能采样。

**构建与设备边界：** build.bat、v1/v2/v3签名、zipalign-P16及v1.5.8/33通过，SHA256 55eb69082e01dc88ab86b7336e0449b6f6bb9589258004325fb39d3265e647c9。原Folder classes.dex与1bb4逐字相同；上批缺主题commit检查保留。未安装APK、不恢复真机用户布局，独立SQLite目录限定/data/local/tmp/smartisan-restore-pages-f02-UUID且完成后仅删除该目录；Launcher PID前后均5750。100项暂存binary patch保持，无add/提交/推送。

**旧档审计和下一项：** Validator仍接受format1/2；shortcuts、portable sources、wallpaper的缺省入口保持既有规则，本批仅代码核对，未以此宣称历史真实归档全通过。A07完整旧档/SAF/中断/分身/多ROM仍开放；下一项核对异常归档的页面/文件夹结构校验能否在写数据库之前拦截，使用受控畸形布局及隔离数据库验证，确认实际缺陷再窄改。Folder性能继续暂停。MEMORY.md未更新；更新本日志、功能报告、问题清单及专项计划。证据build/restore-page-preview-20261019/verification.json、before/after日志及sqlite/summary.json。

<a id="2026-10-19-转备份恢复修复缺失主题包回退写入失败仍报成功"></a>

#### 转备份恢复：修复缺失主题包回退写入失败仍报成功

用户要求先做其他项目，Folder性能采样暂停，保留此前已验修复，CPU停顿仍未解决。本批转A07，审查预验证、阶段journal、应用/自动回滚/启动恢复和旧档可选数据入口，不操作设备布局。

**明确根因及最小修复：** DesktopRestoreController.applyArchive在主题包缺失时将launcher_theme退回恢复前值，但忽略SharedPreferences.Editor.commit返回false，继续进入APPLYING_ICONS、壁纸和VERIFYING，可能最终COMMITTED。PreferenceBackupCodec自身已检查commit，壁纸源Owner也已有关键写入检查，唯独这处分支遗漏。现只检查该写入，失败抛IOException，复用现有失败检查点、回滚、重试及状态提示；不新建恢复Owner、重试循环或改变格式/数据库/原动画。正常缺主题仍保留旧主题，主题可用分支不受影响。原APK归档仍缺失，clean/raw及maintained目录未发现本自建JSON/journal恢复Owner，不冒称从原APK复制；直接修当前已有实现。

**可复现与回归：** 新增tools/tests/restore_journal/run_theme_fallback_tests.py，复用原checkpoint夹具编译实际Controller/Journal/Guard/Lock/FileUtils；仅Android/DB/归档/Codec边界受控，不用真机用户档案。修前准确失败：failed fallback must not commit incoming restore，事件仍为DB/PREF/ICONS/PORTABLE/RECONCILE/WALLPAPER/VERIFY，证明漏检。修后31检查/5场景：成功回退、单次失败自动回滚、双次失败保留检查点后重试、撤销失败后重试、主题可用旁路。同时checkpoint144、worker122、偏好25通过，共322检查；此前旧档省略字段保留当前值/权限相关设置不迁移规则保留。没有以这些隔离测试证明完整真实SQLite/SAF恢复或断电持久性。

**构建与保护：** build.bat成功，v1/v2/v3签名及zipalign-P16通过，版本v1.5.8/33未改。SHA256 ed227fe97533c1d30d5aebea74310fbeb5e5485333aebf82539487386d6b9ecb，相对上批1bb4仅classes2.dex非签名成员改变，原Folder classes.dex保持。100项暂存binary patch逐字不变，已有改动保留，无add/提交/推送。未安装本包、未发ADB恢复/调整设备命令，设备仍保留此前已装包；构建不等于真机验收。证据build/restore-theme-fallback-20261019/verification.json及各测试/构建日志。

**边界与下一项：** 关闭的是主题包缺失回退的写入失败漏检；A07整库/旧档/SAF/真实进程中断/分身及多ROM验收仍开放，不能将注入commit(false)解释为已复现用户设备故障。下一批核对旧格式备份的缺省字段与页面/文件夹布局导入兼容，使用临时归档和隔离数据库，确认具体问题再修，不恢复真机现有桌面。MEMORY.md未更新；本条及功能报告/问题清单/专项计划更新。

<a id="2026-10-19-folder首次动画步长修复输入当帧漏门打开前cpu停顿仍开放"></a>

#### Folder首次动画步长：修复输入当帧漏门，打开前CPU停顿仍开放

**真实根因：** Eb.update在输入处理前判断当前Folder是否正在动画；Folder实际在同帧Ra.T的InputManager.update中创建，随后AnimationManager.update错误使用桌面空闲后累积的delta。API28 X21A原两应用Folder诊断五次创建当帧为108/72/66/63.6/91.2引擎单位，后续约20；录像第一展开帧大小不一致。clean/raw原版Eb.update原本传固定fx，未出现移植elapsed时钟的这条漏门。原APK归档本轮缺失，未冒称重新反编译；maintained elapsed仅参考，未整块替换原逻辑。

**最小修改：** Ra.T在输入前记住当前Folder身份，动画管理器更新前仅对本帧新建且正在打开的Folder调用既有folderAnimationFrameDelta。Eb增加读取原fx的小入口，复用原刷新率归一化，不改曲线/时长/已有过渡门/held-pointer门；输入、事件、物理和post回调继续收到原delta。同一动画管理器的伴随动画共用该首次归一化，和既有Folder活动门一致，不引入随机延迟或新缓存。生产仅Ra.smali/Eb.smali，shell TouchInput仅增加单调时间日志以对齐UP，不进入APK。新增测试执行实际Smali分支346检查通过，既有数学64检查通过；修前快照负对照准确失败。

**链路证据：** 同次UP→同步准备→GL queue→录屏首次展开已对齐。诊断五次准备73.662–81.838ms、最重GL89.922–99.279ms，录屏首次展开在UP后106.164–127.643ms，queue到录屏展开11.311–26.971ms；嵌套段不可累加。依据Android9 screenrecord源码以overlay单调时间校准视频PTS，时基残差不超过5.2us。它是录屏虚拟显示的合成像素，并非物理面板/光子或唯一Launcher buffer ID；录屏和插桩增加负载，不用其宣称无录屏速度收益。

候选五次保留输入delta79.2/69.6/84/82.799995/75.6，实际动画管理器首步全部19.999998。人工逐一查看前一帧/第一展开帧/后一帧，候选有效帧号5/5/6/5/7，首次展开尺寸一致、随后逐渐放大。最初两个图像差异阈值分别漏掉小幅动画/误选静态压缩变化，旧输出保留但无效，不作为首次运动时间证据；正确索引candidate-corrected-first-index.json及review图。没有给候选新增未经时钟校准的UP到物理显示收益。

**正式无录屏五样本：** 同机/同文件夹/100ms原地短按/各两次预热，baseline-formal-pair最大GL墙钟75.988/82.393/84.944/91.163/77.700ms、scheduled CPU71.424/72.751/76.105/82.903/70.584ms；candidate-formal-pair最大GL74.015/84.039/81.565/71.948/76.117ms、CPU67.985/76.284/74.678/65.095/69.192ms。未锁DVFS/温控且A后B，不能把差异归为本次CPU提速；72–84ms长帧仍在。五对非状态栏打开静态画面逐像素相同。本次关闭的是首次动画跳步，不是完整Folder卡顿或冷启动。

**几何澄清及下一项：** Constants.updatePageCellCenterPoints只是选取pageCellAllCenterPoints中已有数组，基础九格坐标没有每次从屏幕重算。原版关闭销毁打开场景，重新创建时fa.ir仍调用移植FolderCellPositionAdapter，复制/修正位置并做反射几何查询；此前只复用了同一次适配内的计算，没有跨次复用。用户指出固定布局应复用是正确方向。下一项核对既有几何结果所有者、变化输入和失效链，限定尺寸/方向/布局/主题资源/图标文字尺寸等实际输入改变才重算，先证重复及成本；不直接缓存共享可变Point数组/完整场景/Bitmap，也不把全部长帧归因坐标。停止重复已关闭的PM/hash/ID微优化。

**构建与边界：** build.bat完成，v1/v2/v3签名及zipalign-P16检查通过，正式1bb4ce8cf2c1cd8a949c743fe8b8121fab03aa2141eb11a3b29c948b3f717f22，版本沿用1.5.8/33；相对4b1仅classes.dex变更。临时诊断源码/正式产物已恢复、helper已删，DEX无FDIAG/FVIS delta/FCPU_PROBE。100项暂存binary patch逐字不变，无add/提交/推送。一次旧正式包安装确认超时-200，之后重试成功；早期rawframes探针退出后生成文件已精确移除，不修改系统策略。Android16/高刷/TNT/动态图/九个实际应用/多ROM/长稳及物理显示未验，整体冷启动仍开放。MEMORY.md未更新。证据build/folder-visible-motion-20261019/verification.json、timeline-summary.json、first-tick-summary.json、candidate-tick-summary.json及formal-ui；正式功能回归结果以本条补充为准。

**正式功能回归补充：** Android9 X21A正式1bb4五轮同PID1252完成原两应用Folder打开/关闭、图标检查、Dock底部上滑搜索（250/450/700/350/900ms）、实际settings查询及系统设置结果启动、BACK、桌面设置/BACK；已人工查看五组Folder/查询/结果/桌面设置截图。采集窗口无FATAL/Launcher ANR标记。最终回桌面首屏，测试touch DEX移除；未调整默认HOME/布局/主题/权限/导航/刷新率。安装拉回hash一致、临时源码恢复、100暂存binary patch保护通过。此项不覆盖动态图/多页应用/Android16高刷/多ROM长稳；Folder CPU等待仍开放。

<a id="2026-10-19-folder绑定细查没有重复创建证据不新增生产修改"></a>

#### Folder绑定细查：没有重复创建证据，不新增生产修改

**范围与结论：** 沿上批cell-create→folder-content-create→g.Ba进行逐节点分段，而非重复坐标/hash/ID优化。正式4b1基线先同Folder两次预热，再五次同100ms原地短按；最大GL墙钟[75.482,69.272,89.549,77.868,85.881]ms，对应scheduled CPU[72.280,63.657,80.908,61.356,77.846]ms。它是当前会话基线，不与上批不同会话比较收益，整体卡顿仍在。

**有效诊断五次：** 原Game Centre/Jovi两应用Folder，每次2项应用纹理入口/2次键解析、19次Ba节点绑定。create入口18次，但首9次完成构建，另9次经既有iH已创建保护立即返回，后者合计仅0.044–0.054ms，不能据18次入口认定重复创建。原版clean/raw也保留create保护和同步绑定；gn虚调用及其嵌套调用不等于直接重复构建。保持9格/空位/原顺序，不通过删空位或提前动画掩盖CPU阻塞。

| 诊断分段 | 五次含子调用墙钟范围(ms) | 判断 |
|---|---|---|
| Ba全部节点 | 30.626–33.630 | 19次；包含纹理与文字，不和子段累加 |
| 两项应用纹理入口 | 22.865–26.743 | 每应用1次，未见同一Cell重复纹理解析 |
| 其中两次键解析 | 21.432–25.565 | 既有必要来源校验，不新增无失效证明的键缓存 |
| 动态同步＋阴影检查 | 0.407–0.672 | 两入口各8次，绝大部分早退，不足以解释主长帧 |
| 文字构造 | 1.832–3.523 | 3个文字节点，不是主要长帧Owner |
| Cell后置 | 0.880–1.105 | 9次，没有足够收益证据支持改原流程 |

只在当前2个静态应用上得出这些结果，不覆盖Folder含天气/日历的动态路径。诊断带额外section开销，不与正式基线作速度比较；18个入口的父子关系和早退由sections/create-entry-summary留证。原APK归档本轮仍缺失，已对照clean/raw及已有原机APK证据，未冒称重新反编译缺失APK；maintained FolderPageView同步create仅作参考，未整块搬入。

**本批生产改动为0：** 没有新的可复现错误或冗余工作证据，不删除原iH保护、节点创建、动态图标/阴影兼容入口，不绕过来源有效性检查，不加入新缓存或改动画。临时诊断复用上批setAppTracingAllowed自身进程Owner，新增Ba/同步/阴影分段，build.bat成功后所有源码/四份正式产物恢复，临时helper删除。临时诊断APK的构建不等于新正式修复。

**恢复与回归：** 4b1cd41624c30e2f6d24ab834729b2e0f4a021bdfead5f168ce1409cad0c1435正式包已保数据恢复，拉回与本批基线/当前build哈希一致，DEX无FDIAG/FCPU_PROBE。正式包五轮Folder/图标/底部上滑搜索、实际settings查询/设置结果启动/BACK、桌面设置/BACK通过，同PID27301；已查看五组截图，UI捕获窗口无FATAL/Launcher ANR标记。默认HOME/布局/主题/来源/导航/刷新率/权限未调，最终回首屏，临时touch DEX已移除。本轮基线100项暂存binary patch逐字保持，无add/提交/推送。生产源码逐字恢复并与诊断前快照一致，不重复构建未改的正式包。

**下一项：** 绑定细查收束，不继续以亚毫秒早退制造微优化。串联同一次触摸UP→folder-open→GL/EGL提交→首个实际运动buffer，确认剩余等待发生在同步准备、首轮绘制还是提交显示；回到用户可见停顿的完成门，未证明重复/无效调用前不改生产。Folder卡顿/整体冷启动、Android16本轮、高刷/动态图/九实际应用/多ROM/长稳仍开放。MEMORY.md未更新；开发日志、性能/功能/问题报告及专项计划更新。证据build/folder-cell-bind-20261019/verification.json、binding-summary.json、create-entry-summary.json及formal-ui。

<a id="2026-10-19-folder初始cpu复用一次适配内的几何计算长帧仍未关闭"></a>

#### Folder初始CPU：复用一次适配内的几何计算，长帧仍未关闭

**定位：** 当前5d2ac17e/API28 vivo X21A，同Game Centre/Jovi两应用Folder、100ms原地短按，正式初组五次最大GL墙钟[100.698,86.201,90.018,81.517,93.454]ms，scheduled CPU[92.033,80.190,79.396,72.519,83.903]ms，确认CPU同步工作仍重。临时逐调用诊断最终有效组：folder-open约72–91ms，page/grid约60–74ms；每次9个格位adjustY约14.9–18.0ms、一次adaptPositions约6.9–14.1ms，均为含子调用的诊断墙钟，不能相加所有父子section或视为无插桩速度。2个实际应用仍需原版9格场景/空位，不删除空位或提前启动动画。

**对照与根因：** 当前compat Adapter在已验证Folder LayoutProperty后，调用公开Geometry函数逐格重新验证同一身份，adaptPositions还逐格计算相同的居中修正和行距。此前M.fn已复用一次坐标数组，本轮不是重做该修复，而是减少数组适配内部/adjustY的重复验证与数值计算。clean/raw的fn保持同步造格、原坐标读取，没有这套Java兼容Owner；maintained FolderPageView也同步create，无同名兼容Owner可直接替换。原版APK归档本轮缺失，未冒称重新反编译原APK；沿用上批原机APK静态证据，未操作DT1902A。保留原版流程和资源。

**最小生产仅两Java：** FolderVisualGeometry公开rowGap/contentGroupCenterCorrectionY继续验证及原fallback，新增同类package-private已验证入口复用原公式；FolderCellPositionAdapter仅在原身份检查通过后调用它们，adaptPositions在本次调用内各计算一次，再用于各点。adjustY仍实时查当前布局/中排锚点并保留回退；没有跳过整个二次坐标适配、没有跨调用/跨帧几何或Bitmap缓存、没有改变坐标公式/运算顺序/主题/动画/SMEngine所有权。

**可复现边界：** 新增tools/tests/folder_timing/run_geometry_tests.py，编译两份实际生产Owner与修前快照，对不同尺寸、文字高度、0/3/6/9/12点、空点、短数组、布局对象替换、非Folder/无布局、负索引、复制失败/非数组以及公开入口fallback做对照。839项通过，float bit逐位相同；受控mode查询2700→1548。64项时钟、12项Surface通过；图标审计errors=0（保留既有INVALID_NAME警告）。这些是隔离边界，不能替代横屏/多ROM实机验收。

**正式紧邻对照：** 为避免把旧热进程与新安装首开混比，初组/诊断/新包首组全部保留另存；随后旧5d2与新4b1均保数据安装、先同Folder打开两次预热，再各五次同100ms短按、同桌面/布局/主题/来源、不录屏。下表每项为一次打开捕获窗口的最重GL帧，不等于输入延迟或首个物理运动帧。

| 指标(ms) | 修前五次 | 修后五次 |
|---|---|---|
| GL墙钟 | 94.179,91.849,79.019,89.142,97.083 | 94.379,83.090,92.162,75.987,73.020 |
| 该帧scheduled CPU | 88.349,85.196,72.209,79.613,86.094 | 88.093,76.594,84.882,69.960,69.089 |

CPU中位85.196→76.594ms，墙钟中位91.849→83.090ms；五对完整非状态栏静态画面逐像素相同。没有锁DVFS/温控或反转A/B顺序；最坏仍94ms，不能将这组下降推广为稳定整体提速、首个运动buffer闭环或Folder已不卡。下一项沿有效时间线核对剩余cell-create→folder-content-create→g.Ba同步绑定/空格位工作，不重复已关闭PM/hash/坐标数组/资源ID微优化；整体冷启动继续开放。

**功能与交付：** 最终build.bat、v1/v2/v3签名、zipalign-P16、v1.5.8/33通过；最终SHA256 4b1cd41624c30e2f6d24ab834729b2e0f4a021bdfead5f168ce1409cad0c1435，相对5d2仅classes2.dex非签名成员变化，无FDIAG/FCPU_PROBE，保数据安装拉回一致。正式五轮Folder图标/开关、底部上滑搜索、实际settings查询/设置结果启动/BACK、桌面设置/BACK同PID21272通过，截图人工核对；UI窗口无FATAL/Launcher ANR标记。默认HOME/导航/刷新率/权限/主题/圆框/来源/布局未调整，最终回原首屏，临时touch DEX和空profile文件移除。本轮开始已有97项暂存，binary patch逐字保留；历史53是旧批快照，不能套用当前计数。无add/提交/推送。

**诊断失败留证：** 首次近16寄存器方法插桩使p0超过4bit指令限制，构建失败后finally完整恢复；改为低寄存器alias后构建成功。普通Trace分段在该非debuggable API28未输出，ART命令先不支持clock-type、再被Process not debuggable拒绝，均不计有效采样；没有修改debuggable或系统策略。临时helper仅在诊断进程反射setAppTracingAllowed开启自身标记后取得上述分段；所有临时源码逐字恢复、helper删除、正式产物无标记。安装确认无焦点一次因安装已成功而停止点击，未调整策略。失败、初组和有效组目录分开保留。

Android16本轮不在、未启模拟器；九真实应用/动态图、TNT、低内存、跨ROM、高刷/长稳仍未验。MEMORY.md未更新；开发日志、功能/性能/问题报告与专项计划更新。证据build/folder-first-motion-20261019/verification.json、baseline-warm/final-warm及geometry-tests-final。

<a id="2026-10-19-android9搜索入口修正adb输入误判正式包五轮通过"></a>

#### Android9搜索入口：修正ADB输入误判，正式包五轮通过

**结论修正：** 上两批“Dock上滑未打开”记录是真实失败的自动化样本，但本轮证明其输入流不符合正常触摸合同，不能据此认定Launcher搜索入口有业务故障。vivo X21A/API28上临时诊断三次stock adb input swipe：DOWN/UP的downTime分别4072662/4073115、4074800/4075114、4076783/4076998；移动及起点有效，识别器uk=true/rk=false/sk=false/tk=true，但downTime不一致令现有保护判invalid。Android9 AOSP input.sendSwipe逐事件以当前when调用injectMotionEvent，而该函数MotionEvent.obtain(when,when,...)，与实机证据一致： https://raw.githubusercontent.com/aosp-mirror/platform_frameworks_base/android-9.0.0_r1/cmds/input/src/com/android/commands/input/Input.java 。这不是圆框或来源失效修复引入的证据。

**最小修复仅回归工具：** 新增tools/tests/search_gesture/TouchInput.java及prepare_touch_input.py，复用shell既有注入权限和Android InputManager，每条DOWN/MOVE/UP或CANCEL共用一个downTime，eventTime实时递增，注入失败抛错、事件回收。没有新增App/权限/设置、Manager或缓存。对照当前识别器、clean/raw原版finish gates及maintained FlingUpGesture后保留原行为，不删除异常事件保护，不移植参考项目的整个手势实现。临时SEARCH_PROBE源码已逐字恢复；正式生产手势源码和本批开始时字节一致。

**验证：** 原手势隔离检查81项通过。恢复正式5d2ac17e799d203798cc73f2cd3ec5672fbdbdd75e6d9da7ff461fc980b0da8f后，在X21A完成五轮：原Game Centre/Jovi两应用Folder打开/封面关闭、底部(540,2100)向上到(540,1000)打开搜索、实际输入settings/显示设置结果/启动系统设置、BACK到桌面、桌面设置/BACK。滑动时长250/450/700/350/900ms，全部同PID16664；已人工查看五组Folder/查询结果/桌面设置截图，不能只凭脚本字段判定。另验证ACTION_CANCEL、30px短滑和stock malformed swipe均不打开，随后有效流仍打开，证明清理及保护保留。UI捕获窗口无FATAL EXCEPTION/Launcher ANR标记，不等于长稳验收。

**正式包与状态：** 诊断build.bat完成后四份正式产物均恢复；本轮未修改生产代码，无需另建发布包。保留数据恢复正式APK，设备拉回SHA与基线/当前build一致、无SEARCH_PROBE；上批圆框v8效果保留。默认HOME与本轮基线均Smartisan，未发设置命令；返回功能用BACK，不混写成系统手势HOME。主题/圆框偏好/来源/布局/权限/导航/刷新率未调，最终返回原首屏；临时shell touch DEX已移除，原版DT1902A未操作，原53暂存binary patch逐字一致，无提交推送。

**剩余与下一项：** 这是测试输入修复和当前Android9搜索路径验收，未验证实体手指全部中断/多指/反向拖拽、全ROM/分身/三星Share现场或Android16本轮。Folder初始CPU长帧和冷启动整体仍开放；下一项回到Folder输入→首个运动buffer之间的阻塞，只改有调用证据的重复或无效工作，不重复已关闭PM/hash/坐标/ID微优化。证据build/search-entry-20261019/verification.json、formal-ui/summary.json及review-sheet.jpg；历史失败保留，不覆盖旧样本。MEMORY.md未更新，本轮更新开发日志、功能报告、问题清单和专项计划。

<a id="2026-10-19-默认圆框实心方底边缘延展保留完整图案"></a>

#### 默认圆框：实心方底边缘延展，保留完整图案

**用户可见问题：** 圆框模式下天气/相册/电话等像方块贴在白圆上。根因是DefaultIconCircleRenderer v7为保护全部可见像素（含方底四角）按外接半径缩小整张PNG，再画到浅色圆内；不是缺图或资源加载失败。真机ResolveInfo.loadIcon取到11个实际应用：天气、相册、便签、安全、信息、计算器、钱包、主题、视频、电话均为BitmapDrawable，只有抖音是独立Vector背景/前景的AdaptiveIconDrawable。因此不能凭空拆出这10张PNG的语义前景，也不能只改自适应图层。

**方案与原版边界：** 用户优先处理圆框后，其他搜索/Folder任务保留。圆框是现有Java兼容功能，clean/raw和原机SMEngine没有可直接替换的同名Owner；沿用当前Renderer/完整图案矩阵，未替换原版图标/几何/阴影。Android自适应图标仍使用原背景/前景分层，不改其图案；官方图层合同参考https://developer.android.com/reference/android/graphics/drawable/AdaptiveIconDrawable 。没有引入AI分割、包名特例、重绘资源、Manager或新缓存。

**最小生产仅DefaultIconCircleRenderer.java：** v8检测占源画布至少60%宽高、宽高比至少95%、opaque core中至少99.5%像素alpha≥250的近方形实心底。复用原完整图案矩阵，把opaque core的BitmapShader按CLAMP延展至原圆包络，再在上面画原完整图案，保留四角内容和视频底部文字。不是放大整图裁掉四角，也不是推断/删除背景色；复杂边缘可能被延展成色带，透明/不规则/细长/很小的图案继续原中性底保守路径。只作用于DEFAULT圆框；managed fallback、IMPROVED/PACK/CUSTOM/RESOURCE及跟随应用入口的选择条件保留。VERSION升为v8进入既有纹理身份，旧圆框不继续命中。临时core Bitmap用后释放，并防createBitmap返回同一对象时提前回收source；无新增跨帧Bitmap缓存。

**抗锯齿与测试：** legacy只画一次圆包络，避免中性底和延展底重复叠加alpha；自适应路径原样。新增default_icon_circle/run_device_tests.py，扩展DefaultCircleProbe：Android9真实Canvas共59项通过，含DEFAULT选择门、四角标记完整、横竖图、原留白不放大、透明回退、128/256/384输出、主体/源所有权/Drawable bounds、整画布alias及圆边alpha。修前受控负例明确失败于“实心底未延展”。初次probe未输出堆栈即Killed的记录保留，补main Looper和受控异常输出后定位到负例；不是Launcher崩溃。shader/color路径8bit舍入差异最多1，测试允许2，不把它误写成逐像素相等。

实际11源修前/修后对照，抖音完整RGBA相同；其他10源中央128区域最大通道差异1、圆mask alpha最大差异1。天气/相册/电话/视频对照见build/default-circle-smart-20261019/comparison.png；最终桌面截图确认方块白框消除，文字完整。使用手机真实图案生成对照，没有AI改图或替换在线图标。

**构建/真机回归：** build.bat、v1/v2/v3签名、zipalign-P16、v1.5.8/33通过（不等于严格16KiB库验收）。最终APK SHA256 5d2ac17e799d203798cc73f2cd3ec5672fbdbdd75e6d9da7ff461fc980b0da8f保数据安装vivo X21A/API28；相对上一批5297只变classes2.dex非签名成员，无诊断注入。五轮Folder图标/开关、桌面设置/BACK返回同PID14877通过；保留用户现有圆框/来源/主题/布局/默认HOME，不切换配置或清数据，原53暂存未改，无提交/推送。

**边界与后续：** 当前效果已在截图同机确认，不推广为所有图案语义识别；复杂照片/边缘花纹延展、其他ROM/密度、动态图/分身运行矩阵未验。没有冷启动或Folder提速结论。此前Android9搜索入口未通过，查询启动未验；此次未重开该路径，也不称全功能通过。本批末尾HOME解析为Smartisan，与上批vivo结果不同；本批开始未单独采HOME基线，没有发过默认HOME切换命令，不能套用上批值强行恢复或据此归因。下一项回到搜索入口同基线定位，然后继续Folder初始阻塞。MEMORY.md未更新，更新开发日志/功能报告/专项计划；证据build/default-circle-smart-20261019/verification.json。

<a id="2026-10-19-来源失效核对图标包两处局部修复android9搜索回归未通过"></a>

#### 来源失效核对：图标包两处局部修复，Android9搜索回归未通过

**范围：** 完成上批约定的来源变更通知审计，修复图标包Owner的两处遗漏。没有新增键/Bitmap缓存，没有改Folder动画、几何、资源或纹理所有权。本批不是Folder卡顿/冷启动提速的完成证明，停止重复已关闭的hash/PM/label/坐标/资源ID微优化。

**原版和Owner：** clean_launcher、raw及上批DT1902A APK反编译的Cell.cb(I)均以ItemInfo.Ne先查Ea.bb；移植版还先解析来源身份。原版Aa.c要求逗号分隔extra_packagename，随后r→e进原更新队列。maintained的IconManager使用JSON协议，不能直接搬入本项目。当前Java notifyIconUpdate缺extra，但源码/Smali没有调用者，作为不可达候选留证，未修改，不归因为当前卡顿。

| 变化 | 既有更新Owner与审计结果 |
|---|---|
| 自定义、单项/全局选择 | forceUpdateIcon/applyIconChanges或applyIconChange→dispatchIconUpdate→原Aa队列；预览失效不等于SMEngine纹理失效 |
| 包安装/替换/卸载、预载完成 | SmartisanInstallManager→invalidateIconPackPackage/onIconPackOverridesChanged及预载完成回调；本批补全局跟随者遗漏 |
| 在线下载及恢复 | promoteDownloadedImprovedIcon→scheduleSmartisanIconRefresh→合并包更新；恢复事务另由RestoreIconSourceReconciler管理，保留 |
| 外部文件晚到/删除/同名变化、临时来源不可用 | 尚无覆盖全部入口的单一有效revision；即时检查和就绪回调不足以证明统一纹理失效屏障，继续保留来源校验 |

**根因与最小修改，仅两生产文件：** IconPackManager.resetCache清映射/递增generation但漏清sCandidateCache，getCandidateMetadata仍能直接返回旧候选；补一行evictAll，复用原锁与generation。MaintainedLauncherSettingsHost.onIconPackOverridesChanged只通知显式MODE_PACK，漏全局AUTO/无redirect记录及更新后消失的appfilter映射；事件入口快照原持久所选包（避免稍后卸载fallback/选择切换抹掉关联），匹配时在既有worker用allLauncherPackages合并包集合，再走原applyIconChanges。非所选包仍只通知显式用户，空集合不发、集合去重、不改来源选择；所选包事件会额外重绑非跟随者一次以覆盖无记录者，不在每次Folder打开扩大工作。并保留applicationContext不可用时的传入Context。

**边界验证：** 新增tools/tests/icon_preview/run_pack_invalidation_tests.py提取实际方法并控制worker/main调度。修前两组分别失败于“全局AUTO/无记录漏通知”和“旧候选未清”，修后13+5=18项通过，包含非所选包/普通应用事件、空集合、选择不变、事件后切换、Context及generation。这是JVM隔离逻辑，不是实机真实包广播验收。既有Folder时钟64项、Surface12项通过；图标库errors=0，保留既有INVALID_NAME警告。

**交付：** build.bat、v1/v2/v3签名、zipalign-P16、v1.5.8/33通过，P16不等于严格16KiB库验收。APK SHA256 5297d96f0e3f9548c8718293fbfdaee690dd8c350ac907ce435bb5fbfd0c3b24已保数据安装vivo X21A/API28并拉回一致；相对db14只有classes2.dex非签名成员变化，无FOPEN/FDIAG/固定120测试代码。Android16本轮不在，未启动模拟器、未操作原版锤子。

**五样本/局部功能：** 手机原装fb6506与上批db14不同，最初五次仅保留现状；另安装并核对db14，和5297各采5次同机原Game Centre/Jovi两应用Folder、100ms原地短按、顺序热打开。修前最大GL墙钟[124.893,98.204,122.040,103.605,78.657]ms，修后[113.180,85.682,58.169,101.562,90.704]ms。不是scheduled CPU或物理呈现，没有锁DVFS/温控/缓存，不能归因整体提速，长帧仍在。五对非状态栏完整静态画面逐像素相同；另5轮图标/Folder开关/桌面设置/BACK返回同PID11755通过，捕获窗口无FATAL/Launcher ANR标记。

**未通过及失败记录：** 搜索手势设置画面确认为开启，但多条Dock向上输入未打开搜索，查询/结果启动未执行，不计回归通过。默认HOME是vivo原生桌面且未改，有效返回用BACK，不把直接启动Launcher当HOME验证。最初误开便签/进入原生桌面的路线样本排除，未同意便签权限；atrace最初按TGID漏计(-----)线程，改按B|PID及线程栈归属，失败原始记录保留。候选首次安装-200、UIAutomation多次null root，普通安装按钮重试成功，未改USB/安全策略。既有app_icon_candidates总套件修前即因ManagedIconSource提取签名过期失败，未冒充通过；额外目录shell隔离probe被Settings provider权限拒绝阻止SQLite初始化，不是Launcher崩溃，亦不计通过。搜索Activity直接ADB启动因未导出被拒，未绕过。

**下一项与边界：** 优先用同基线实际手势定位Android9搜索入口失败，区分设备/采样/既有行为与回归，再回到Folder输入→首个运动buffer的CPU阻塞。来源失效审计已完成，但不允许据此跳过来源校验。真实图标包替换/移除/选择矩阵、本轮API36、多用户/分身、多ROM、长稳耗电未验。默认HOME/主题/布局/来源选择/权限/导航/刷新率未改，53原暂存不变，无提交推送。MEMORY.md未更新；证据build/folder-source-invalidation-20261019/verification.json。本批更新现有五份记录。

### 2026-10-18

<a id="2026-10-18-folder原版差异审计推进节拍与surface高刷修复打开前停顿仍开放"></a>

#### Folder原版差异审计：推进节拍与Surface高刷修复，打开前停顿仍开放

**用户现象与范围：** 用户确认“点击后停一下才放大”和“放大途中顿一下”均存在，并要求120Hz像桌面一样增加中间帧而非动画倍速。扩大原版静态对照到9个关键文件、71个差异方法，区分绑定、绘制和统一计时；这不是71个BUG。继续使用上批从DT1902A提取的8.0.4 APK及clean/raw，maintained的MainView真实delta仅参考，不整块替换。原版控制器j/动画_r仍保留；原版Eb.update每次Ra.T传固定fx，当前移植版则以真实GL回调时间折算，引入了与显示节拍不一致的推进量。

**实机定位：** V2458A/API36，c034c864基线、现有三应用九格Folder、同一蓝色壁纸、实体光影开启。临时clock Trace 5次瞬时tap及5次100ms短按：没有复现长按旧问题的120引擎毫秒首步，不能套用长按补丁；实际创建当帧约16.8–25.2。明确SurfaceView buffer→SF latch→commit token→display FrameTimeline后，同样约16.6ms的呈现间隔却连续对应27.599、7.2或27.599、6.0的引擎推进量，存在非均匀推进。原版固定fx临时对照在60Hz均匀，但90Hz录屏变快，只作诊断，不交付全局固定步长。关闭光影仍先查文件是另一路代码问题；当前实机光影实际开启，文件ready检查500ms累计约1.6–1.9ms，不以此解释当前卡顿，未修改该路径。

**高刷直接证据：** 系统菜单/面板120Hz、应用高刷开关原本开启时，旧Launcher Surface仍约60fps，应用读取的当前模式也可被ROM覆盖为60。仅设置peak/min或照当前模式请求的候选仍是60，保留失败数据，不算120Hz通过。临时向原GL Surface声明120fps后，实际显示间隔变为约8.3ms，动画后续更新从17次增加到32–35次。由此补齐现代Android Surface帧率协商，不能把系统菜单值当应用实际帧率。

**最终生产仅3文件：** LauncherSettingBridge新增两项兼容处理；SMGLSurfaceView只在既有surfaceChanged及窗口重新可见时调用Surface投票（5行）；Eb.update仅在原Folder正在打开Zr或关闭Yr时归一化步长（16行）。Surface从当前分辨率的supportedModes取得能力上限，API30使用setFrameRate两参数，API31+仅允许无缝切换；不写系统设置、不设置preferredDisplayModeId、不改变分辨率，由ROM/用户/温控政策裁决实际帧率。最终无新增DisplayListener、轮询、Manager、线程或缓存；中间候选的监听器未保留，因为能力投票不需要跟随每次模式回调重发，原生命周期足够。Frame delta用应用当前实际报告的refreshRate连续归一化原fx：fx×60/rate，60Hz约20、120Hz约10，保留原fx速度及原曲线，未知显示退回既有elapsed；恢复基准0 delta、100ms上限及held-pointer保护保留。没有回退全局真实时钟，Folder以外动画保持原路径；Folder同时运行的伴随时间线仍共享原Ra.T。

**60/120对照：** 最终数学逻辑诊断各5次，均原有Folder/100ms短按；首个创建tick仍沿用原路径，表中计数为后续active ticks，不等同全部物理帧。移除诊断后，最终db14d579正式包另做标准/高模式各5次Perfetto，录屏另采，不混入无录屏时序。

| 项目 | 标准60Hz | 高120Hz |
|---|---|---|
| 正式5样本显示间隔中位(ms) | 16.646,16.646,16.642,16.648,16.644 | 8.323,8.324,8.323,8.323,8.323 |
| 诊断后续推进值(引擎单位) | 20 | 约10(浮点Trace截断9.999) |
| active后续tick次数 | 17,17,17,17,17 | 35,35,34,34,35 |
| 末次active tick距控制器入口(ms) | 279.876,287.134,282.107,287.589,283.182 | 300.853,294.244,282.166,278.174,293.649 |

这是增加中间帧而非120Hz倍速的证据，不是严格相同物理动画首尾时长证明。FrameTimeline仍没有Launcher SurfaceView应用帧，用明确buffer映射；全窗口末尾标准有0–1、高刷有1–2个未完成present，已核实位置在trace尾部，不把它们算成动画丢帧，也不称完整零丢帧。高刷仍有约16.7ms显示长间隔。正式录像以ROI变化阈值分段：60Hz五段约250–269ms/15个变化帧，120Hz约275–374ms/28–29个变化帧；高刷第5段374ms异常原样保留，没有同时trace，不能擅自归为编码误差或宣称全程已流畅。录屏阈值首尾与引擎active首尾不同，不能据此作精确总时长比。

**仍未解决：** 正式标准模式第1次最大GL55.365ms、scheduled CPU50.873ms，其他4次CPU约16.457–18.427ms；高刷5次最大CPU约12.493–19.829ms。不能只看中位或宣布打开前停顿/冷启动提速。创建当帧及纹理查询前的兼容来源/完整key解析仍会阻塞，首个真正运动内容的buffer身份与这段绑定成本还需进一步闭环。下一项仅核对图标来源变更的既有失效通知（安装替换、自定义、图标包、在线下载/文件到达），验证能否安全恢复原版“先查已有纹理”的热路径；不重新采已关闭的PM/label/hash/资源ID微优化，也不直接添加无失效证明的key/Bitmap缓存。

**回归与交付：** 64项提取生产时钟方法边界、12项Surface API/同分辨率能力/合成60模式/Surface替换边界通过；API29/30/31为隔离fixture分支，并非这些版本的实机验收。正式包5轮Folder三图标/开关、系统设置/HOME、Dock底部上滑搜索、实际settings查询并启动结果、桌面设置/HOME，同PID27461通过；另5轮桌面左翻/右返截图确认实际换页并回到原页，同PID通过。捕获UI窗口无FATAL/Launcher ANR匹配，不覆盖全时段长稳。原版DT1902A未安装任何包；本轮原机录屏有未打开/打开其他Folder的路线问题，排除数值比较，只沿用上一批confirmed-route与APK证据。

5对同会话clock-before与交付标准模式截图，书架/图标/文字位置目视一致；非状态栏每通道平均差异小于0.00034、最大2/255，未声称逐像素相同。最初误用前一批不同壁纸截图的比较作废，不据此判定主题被改。原版资源/几何/动态图标所有权未动，未新增图像缓存。90/144Hz实机、其他ROM、外接/TNT显示、九实际应用/动态图、严重掉帧/温控/耗电/长稳及系统HOME闪壁纸仍未验；若ROM报告帧率与实际渲染不一致，或GPU严重掉帧，逐帧推进仍可能延长动画，不能推广为全设备已解决。

用户明确授权临时调整刷新率，测试后系统UI恢复“智能适配”，应用高刷开关原本开启且未改；peak_refresh_rate=120.0、min_refresh_rate不存在恢复校验一致，自动锁屏60000ms未改。导航过程中误开自动锁屏选择框已取消，未选新值。诊断产物一次因Windows映射锁恢复失败，已补恢复；XML证据声明utf8的解析问题改以显式UTF-8解码验证，设备状态实际已恢复。最终build.bat、v1/v2/v3签名、zipalign-P16、v1.5.8/33通过（不是严格16KiB库验收）。SHA256 db14d5792fc9d9b0dc3387a2af7dbbdfb240190acdd948b091407888eff96113，安装拉回相同；相对c034c864仅classes.dex/classes2.dex非签名成员变化，正式DEX无FOPEN/FDIAG及固定120测试方法。原53暂存binary patch一致，无提交/推送，MEMORY.md未更新。完整证据build/folder-open-chain-20261018/verification.json、原始trace、两档录像、失败候选与静态差异；本批更新现有五份记录。

<a id="2026-10-18-folder资源表重复查询修复补充原版dt1902a对照"></a>

#### Folder资源表重复查询修复，补充原版DT1902A对照

**本批结论：** 原有Folder卡顿仍未整体验收。本批只关闭图标兼容链重复资源ID查询，不改原版动画、节点、几何、来源到达重查或Bitmap所有权。前一批M.fn本次坐标副本修复保留。不能把下面局部收益或五轮功能通过写成“文件夹已不卡”或“冷启动已解决”。

**原版证据：** 用户接入DT1902A，Android10/API29，原生Launcher8.0.4/code3。只读提取系统APK，SHA256 e5bdc075c230cdf0685268752f43731ed0d67ee6f8735f8097b3cb381a878e2e，保存在build/folder-resource-match-20261018/original-device/LauncherSmartisanNew.apk；original_apks归档路径仍缺失，没有擅自替换。REA/JADX提供者不可用，采用本地apktool反编译，不能声称REA成功。控制器j、页面init/_r/bind/工厂、坐标ir、M.fn和Cell.cb共8方法与clean/raw全部一致；当前控制器/动画入口/工厂仍一致，差异集中于既有几何适配、坐标副本和兼容图标键/activeicon同步。原版也先同步new/init/bind页面，再调用_r启动动画，没有据此新增预热或异步页面系统；maintained不是同一SMEngine链，未搬运其Folder实现。

原版原有中间两应用文件夹，5轮实际打开/关闭、截图人工核实，同PID22175。瞬时tap未触发打开，改用原地100ms短按成功；早前黑屏和仍在桌面的样本作废，只有confirmed-route计入。legacy atrace无进程名，按采样PID关联，不能用process.name空结果误判无onDrawFrame。五轮最大GL墙钟[20.457,19.802,24.815,25.903,20.293]ms，最大scheduled CPU[6.950,6.639,5.830,6.870,7.213]ms；不是与V2458A同硬件/相同应用/同数据/同输入时长，不计算跨设备提速率，也不能把GL墙钟当物理呈现。未安装移植包/改布局或系统设置，保留用户原版手机环境。

**定位与最小修复：** 临时细分发现候选可用性检查每开22次、资源图标查找13次，其中既有settings资源名查找14次，重复进入Resources.getIdentifier。无用settingsContext总计仅0.128–0.520ms，不作为本批修复。生产仅IconPreviewRepository和MaintainedLauncherSettingsHost两Java文件：复用已有Repository保存资源表整数ID（含同表的0），最多4个Resources、各256项；按资源对象身份/AssetManager/Configuration区分，配置回调及RUNNING_LOW以上trim清理；framework查询不持元数据锁，clear/config竞态不能回填旧表。保留设置包与应用包、规范化与原始名称的搜索次序。文件、在线目录、variants、自定义来源与实际Drawable仍即时检查，不缓存“应用永远没有图标”的结论，不缓存Bitmap，不新建Manager。新增元数据内存有上限，但未做长期争用/PSS或动态ResourcesLoader/ROM overlay矩阵，不能宣称内存占用下降。

三组相同细分热路径每开49次ID请求，桌面已预热后原生查询均0，49次合计首开[0.095,0.116,0.139]ms、再开[0.199,0.265,0.206]ms。候选检查累计首开[0.712,0.965,1.115]→[0.509,0.650,0.561]ms、再开[1.556,2.180,3.193]→[1.052,1.516,1.130]ms；资源图标累计首开[0.787,1.048,1.032]→[0.120,0.151,0.182]ms、再开[1.838,2.234,2.876]→[0.261,0.360,0.314]ms。嵌套区段不相加，诊断开销不与正式时间比较；不是冷缓存查询为0的承诺。

**正式同机五组：** V2458A/API36原有三应用九格Folder，62e887e1→c034c864，先旧后新各5次重启后首开及再开，统一等待6秒；不清数据/OS缓存，不锁DVFS或改自适应刷新。这里是Folder首开，不是五次整体冷启动验收。

| 指标 | 首开修前→修后ms | 再开修前→修后ms |
|---|---|---|
| 最大GL墙钟五样本 | [32.319,21.644,24.241,26.042,20.593]→[23.808,19.921,22.806,25.998,36.629] | [23.620,19.062,21.253,20.549,26.406]→[19.920,18.000,25.844,19.348,20.153] |
| 最大scheduled CPU五样本 | [11.214,14.687,13.981,13.454,16.959]→[13.029,9.808,13.144,13.803,16.343] | [15.382,17.807,12.758,16.127,15.072]→[17.086,14.150,14.453,10.413,16.615] |
| 最大GL中位 | 24.241→23.808 | 21.253→19.920 |
| 最大CPU中位 | 13.981→13.144 | 15.382→14.453 |
| 映射显示间隔最大值中位 | 16.750→16.713 | 16.753→16.682 |

FrameTimeline仍没有Launcher SurfaceView应用帧，用明确layer latch→SF commit token→display FrameTimeline，所有映射present均非空；原生显示时间线不是应用全部帧统计。修前一次首开起始间隔33.291ms，修后五组第一间隔约16.64–16.66ms，但顺序采样及调频混杂，不能归因于本补丁或宣称稳定整体提速。修后最坏36.629ms帧中scheduled2.284ms、dequeue34.431ms，缓冲等待与CPU仍分开；另一最大CPU帧16.343ms，不能把整个长回调当图标计算。首次内容运动及松手到运动延迟尚未闭环。

**回归与交付：** Android实机80项资源ID边界通过：正/零ID、包和Resources隔离、配置/回调/低内存、容量、异常、查询锁外及失效竞态；晚到/删除文件、在线目录和variants仍生效。删除失效清理的负例明确失败于configuration callback（app_process退出属于负例，不是Launcher崩溃）；首个负例只返回Killed，增加断言输出后重跑，未掩盖。480组合/1665项纹理键与来源对照通过。修前后十对完整非状态栏场景逐像素一致。最终正式包5轮Folder三图标/开关、系统设置返回、Dock底部上滑搜索、实际settings查询并启动设置结果、桌面设置返回，同PID4403通过，所捕获UI窗口无FATAL/Launcher ANR匹配。

build.bat成功，v1/v2/v3签名、zipalign-P16、v1.5.8/33通过（不等于严格16KiB库验收）。最终SHA256 c034c864c5b8fa34bcb29653cdb3550aa02c9561e23156bd0ca3385df06f4b87，安装拉回相同，相对62e887e1仅classes2.dex非签名成员变化。全部临时源码/产物已恢复，正式DEX无FDIAG；原53暂存binary patch逐字节不变，未提交/推送。两生产Java文件及一个边界测试外未改本批其他代码，更新现有五份记录，MEMORY.md未更新。完整证据build/folder-resource-match-20261018/verification.json及原始trace/截图/差异/失败记录。

**下一项仍是Folder整体故障：** 用原版及移植版分别对齐松手→首个真正运动内容buffer→SF显示，检查打开前停顿与动画中间等待的边界；静态截图/GL结束不能替代运动验收。停止重复已关闭的PM/label/hash/坐标复制/资源ID查询微优化。九个实际应用/动态图/长稳/多ROM/系统HWC内部原因与冷启动仍开放，不能先宣布Folder完成并转下一功能。

<a id="2026-10-18-folder逐格重复坐标复制最小修复并完成真机回归"></a>

#### Folder逐格重复坐标复制：最小修复并完成真机回归

**定位与原版对照：** 按上一项继续细分page-create的节点、材质和文字，未重做PM/label/hash优化。临时逐调用Trace及14个方法clean/raw对照：页面工厂/构造/create/gn/bn、Cell内容创建/状态更新、Mc文字构造保持原版结构；已有差异是安全区/书架高度及Startup诊断，不撤掉兼容适配。四处文字构建累计约0.359–1.308ms，三格材质获取约0.012–0.040ms，没有据此改绘制或文字缓存。实际残余发现于M.fn逐格布局：原版每个格子调用fa.ir取得全组坐标，当前兼容层ir新增adaptPositions，会复制整组9点，九格循环因此复制81点。三组首开/再开均ir9、adapt9、copyPoint81，ir累计首开[0.915,1.061,0.861]ms、再开[1.441,2.077,1.195]ms。原版APK归档仍缺失；clean/raw为原实现证据，maintained使用不同的FolderCell/RectNode组织，仅参考未搬运。

**最小修复：** 生产仅launcher/smali/com/smartisanos/launcher/view/b/M.smali的protected fn()V，24行新增/1行替换。新增一个方法局部寄存器，只对实际FolderPage实例复用本次首次取得的坐标副本；取得位置仍在第一个格子创建之后，空循环不新增ir调用，每次fn入口重新置null。普通桌面分支仍逐格调用ir，不增加字段/持久缓存/跨打开状态。ir自身仍由原Owner更新Constants并通过既有Adapter复制，继续保留每格adjustY；几何公式/原始全局坐标/动态图标/Bitmap生命周期/动画均未修改。调用链核对：Cell创建链无updatePageCellCenterPoints写入，Page布局只读取副本x/y后传入setTranslate，未把这些点交给子节点保存；不把方法局部副本提升为全局缓存。

**次数与局部耗时验证：** 修后三组首开及同进程再开均ir1、adapt1、copyPoint9，adjustY仍9。ir累计首开[0.112,0.143,0.151]ms、再开[0.356,0.266,0.452]ms；仅说明重复复制减少，不把嵌套诊断耗时或不同运行状态当整体提速。三枚图标纹理仍命中，PM仍5、内容hash仍1，未顺手改变已关闭路径。临时逐调用标记覆盖有开销，正式五组另采；为避免候选fn增加局部寄存器后p0超过普通invoke编码范围，修后诊断不再给fn额外加寄存器，而在其调用者/ir/Adapter内标记。正式源码无诊断。

**正式五组：** V2458A/API36原有三应用Folder、布局/主题/用户数据/系统设置不改，25d0ab51→62e887e1，先旧后新，不清OS/ART缓存、不锁DVFS或自适应刷新。

| 最大onDrawFrame | 修前五组ms | 修后五组ms | 中位修前→修后ms |
|---|---|---|---|
| 首开 | 24.283,13.945,24.554,32.445,38.184 | 13.931,15.849,17.576,20.704,21.281 | 24.554→17.576 |
| 再开 | 21.460,20.817,23.948,26.882,22.288 | 22.654,20.774,25.330,33.279,18.363 | 22.288→22.654 |

回调cadence有约11/16ms组间变化，再开中位未改善，最坏仍33.279ms，不能宣布稳定整体提速/Folder已顺滑。修后第3组再开25.330ms中scheduled23.470ms、dequeue0.227ms；第4组再开33.279ms中scheduled2.328ms、dequeue31.294ms。CPU与缓冲等待继续分开，不能把后者当图标计算。十对首开/再开截图的书架及非状态栏场景逐像素一致；这不是运动或物理present验收。

**失败与验证边界：** 修后第4次进程启动，脚本等待当前PID的PAGE_READY日志超时；该PID日志导出为0字节，截图实际桌面正常，原因未确认，没有进入工程模式或改日志设置。失败目录final-formal/failed-readiness-4保留。已通过的前三组不覆盖；第4/5组重新进程启动，同样等待5秒，另以文件夹缩略图区域和基线逐像素一致作就绪门，再采首开/再开。该日志门差异单列，不称完整同条件冷启动验收，不据此强报性能收益。首次功能回归在设置入口前电脑ADB服务连接中断，记录ui保留；连接恢复后完整重跑五轮于ui-retry，不能把失败首轮算通过。

**交付回归：** 正式包最终五轮Folder开关/三枚图标→系统设置/HOME→Dock底部上滑搜索→实际settings输入并启动设置结果→桌面设置/HOME，均同PID11664通过，未打开Folder内联系人数据。build.bat、v1/v2/v3签名与zipalign-P16、v1.5.8/33通过；P16检查不等于严格16KiB native验收。SHA256 62e887e18f9133c23027710b9b4bcecebe80c36c80334eeaf10b0db65d5af0ed，安装拉回一致，相对25d0ab51仅classes.dex非签名成员变化。全部Java/Smali哈希检查只M.smali变化，所有临时源码与正式产物已恢复，正式DEX无FDIAG，原53暂存binary patch一致，MEMORY.md未更新。UI窗口无FATAL/Launcher ANR匹配，但前述进程日志缺口限制覆盖，不推广为全时段无崩溃。手机保留新正式包，用户布局/默认HOME/导航/权限/日志/刷新设置未改。

本批关闭“逐格重复复制整组坐标”局部问题；节点/材质/文字未发现其他可安全删减工作，不重新设计或预热。**下一项：细分修后仍达23.470ms CPU的起始帧，聚焦尚占主要时间的资源匹配调用内部（资源名/可用性查找），不重做已关闭PM次数/无用label/像素hash优化。** 系统HWC延迟内部原因、Folder总体顺滑/九个实际应用/动态图/多ROM/物理呈现、整体冷启动仍未闭环。完整证据build/folder-scene-bind-20261018，包括对照、三组细分、前后次数、正式五组、失败、截图、调度核算及verification.json。

<a id="2026-10-18-folder缓冲等待旧长帧为显示侧背压起始cpu间隔仍开放"></a>

#### Folder缓冲等待：旧长帧为显示侧背压，起始CPU间隔仍开放

本批只推进producer→缓冲释放→SF latch/present，不重复已关闭的PM/label/hash微优化。V2458A/API36原有三应用Folder、正式25d0ab51、数据/布局/主题/系统设置不改。原34.709ms样本GL的32.973ms dequeue等待期间，SF在136105.611025记录wouldBackpressure=1，随后PrevFramePending=1、PrevHwcFrameMissed=1、PrevGpuFrameMissed=0及onCommitNotComposited；桌面buffer9在136105.593652锁存，buffer10到136105.628666才锁存，frame7在136105.634663释放，内层dequeue于136105.635204返回。可确认该次等待伴随上一HWC帧未完成与合成跳过，不能归为34ms图标CPU；不能据此断言厂商驱动内部根因或整个Folder问题已解决。原trace内SF绝对时钟与ftrace存在偏移，不跨时钟直接相减。

**正式五组系统trace：** 每组进程重启后首开/封面关闭/再开，Perfetto4.5秒窗口，不清系统/ART/用户缓存，不锁DVFS或自适应刷新，无并行录像。首开最大GL回调[23.636,27.988,25.576,16.711,25.136]ms，再开[18.473,20.734,21.296,23.801,15.573]ms；本批无生产变化，不作为优化A/B。Android16该机FrameTimeline仅有SF显示帧及状态栏，缺少Launcher SurfaceView应用帧；用明确桌面layer的latchBuffer编号→所在SF commit token→display FrameTimeline交叉映射。263次锁存，262次有对应显示token，1次末尾锁存无对应token保留缺口。前3组桌面更新间隔约16.6ms，后2组约11.1ms，自适应cadence变化，未改手机刷新设置。115次大于10ms的dequeue均在返回前看到本layer释放，释放开始至返回0.215–1.322ms。多数等待与正常持续呈现并存，不能仅按dequeue阈值认定卡顿；SF显示帧也不等于物理屏幕拍摄。

**未解决的起始CPU间隔：** 第4/5组再开头两个桌面buffer对应显示结束间隔22.203/22.024ms，后续约11.1ms。第4组对应onDrawFrame23.801ms、scheduled21.864ms、dequeue0.172ms；第5组相应早期帧12.922ms、scheduled12.111ms。二者不能继续归为dequeue长等待。三组独立临时细分Trace只作定位：folder-open首开[8.300,7.047,9.398]ms、再开[16.052,16.397,19.842]ms，纹理键累计首开约3.686–4.774ms、再开10.450–13.978ms，动画启动0.454–0.674ms；嵌套耗时不相加、诊断开销不与正式样本比较。纹理仍命中、内容hash仍1次、PM仍5次；没有找到新的安全删减点，不猜改缓冲数量、swap interval、动画或兼容来源到达重查。控制器j/页面init/_r原版clean/raw一致的既有对照保持，原APK归档缺失，未做原版同机运行对照。

**回归与交付状态：** 正式包五轮Folder开关/三枚图标、桌面系统设置返回、Dock底部上滑搜索、实际settings查询并启动结果、桌面设置返回通过，同PID24725；诊断卸回正式包后另1轮同PID28021通过。捕获UI窗口无FATAL/Launcher ANR匹配，不扩展为全时段长稳结论。临时诊断构建成功，7个临时改动文件与4个正式APK产物恢复；本批生产源码/正式APK均未改变，无需为调查另构建正式版本。安装拉回SHA256仍25d0ab51437931a3caf6595c0864361c36fc2f63abb92c1851e7a7914acfece4，正式DEX无FDIAG，原53项暂存binary patch逐字节一致。图标/书架截图已留存，用户布局和系统状态未改。首次Perfetto配置放local/tmp被服务权限拒绝，改用系统提供的perfetto-configs目录成功，失败日志保留；没有改设备权限。

证据build/folder-buffer-wait-20261018：原始trace、previous-fence-evidence.txt、buffer-summary.json、initial-gap-frame.json、三组诊断、UI及verification.json。本批更新开发日志/性能/功能/稳定性报告和计划，MEMORY.md未更新。**下一项仍是Folder：针对已出现22ms起始显示间隔的场景绑定CPU区段，细分原版page-create中texture-key以外的节点/材质/文字绑定，核对与关键调用的重叠；不再把系统背压当图标CPU，也不重做已关闭hash/PM计数。** 缓冲等待的直接链路局部说明完成，厂商HWC延迟原因、Folder整体顺滑/九应用/动态图/多ROM、冷启动仍未验收，不转快捷桌面。

<a id="2026-10-18-folder单次组件解析复用完成剩余长帧定位到缓冲获取等待"></a>

#### Folder单次组件解析复用完成，剩余长帧定位到缓冲获取等待

**本批目标与依据：** 继续上一批之后的PM/标签/重查，而非重做来源hash。V2458A/API36原有三应用Folder、原布局/主题/设置，基线c7ae5701。三组首开/同进程再开细分Trace，每次resolveLauncherActivity为7次、iconOverrideDrawable的未使用标签读取2次；PM方法累计首开[1.216,1.772,1.307]ms、再开[4.077,2.843,2.875]ms，标签仅0.004–0.012ms，不能把标签当主要卡顿。三枚纹理仍命中、受管内容hash仍1次；资源来源重查继续保留。

**最小修复：** 生产只MaintainedLauncherSettingsHost.java。loadIconForComponentSource增加可选的本次prepared ResolveInfo；仅desktopSourceForTextureKey已确认主用户/准确组件的IMPROVED缺失分支传入，复用本次组件解析，loadIconSource的第二次override查询照常执行。普通公开加载API传null，每次仍通过PM重新解析，不存跨调用状态、无新缓存。另删除iconOverrideDrawable中的info.loadLabel调用；selectedIconDrawable私有实现根本未读取label参数，保留其签名、实际来源选择及其他必要标签读取。原版控制器/动画、资源、图标内容/几何、阴影/Bitmap所有权不变。clean/raw/maintained无此新增Java兼容Owner，原控制/动画逐方法对照沿用同日调查；原APK归档仍缺失。

**验证：** 扩展既有tools/tests/icon_metadata/run_key_source_device_tests.py，提取真实iconOverrideDrawable/selectedIconDrawable及解析Owner，PM/来源夹具、真实Android Bitmap/ART。以当前c7ae5701源码为基线，480组合逐一完整key相等，总计1670检查通过；单缺失来源PM 3→2、该无用label 1→0。覆盖两次键调用各自重新解析、回退期间图标可用、元数据/安装变化、分身/组件旁路、标签异常及普通Drawable API。旧Host新负例明确在“复用一次已解析组件”断言失败。三组真机相同诊断确认每开PM 7→5、该label 2→0，redirect完整读取仍9次、IMPROVED解析仍7次、内容hash仍1次；不把必须保留的源到达重查称为已删除。

**正式五组：** 先基线后最终、各5次进程重启+首开/封面关闭/再开，不清用户数据/OS/ART缓存，CPU/DVFS/自适应刷新未锁定。最大GL回调首开修前[27.086,16.921,24.153,17.305,27.733]ms，中位24.153；修后[14.562,21.399,16.914,34.709,21.547]ms，中位21.399。再开修前[19.616,23.378,25.431,20.739,24.197]ms，中位23.378；修后[16.292,26.108,16.798,25.029,24.816]ms，中位24.816。所有样本保留，首开最坏变高、再开中位未改善，不能宣布整体稳定提速/卡顿已解决。回调cadence也有变化，见verification.json，不混用不同批次五组制造收益。

**34.709ms长帧核对：** final-formal/pair-4-first，GL tid19372：sched_switch核算约1.920ms处于scheduled、32.789ms休眠离CPU；同线程嵌套SurfaceView BLAST的dequeueBuffer外层32.973ms、内层32.865ms。该帧起点在ACTION_UP派发开始后约27.223ms，不把它武断称为动画首个运动帧。当前可确认是缓冲获取等待，不是34ms持续的图标CPU计算；缓冲未释放的具体原因、fence/消费者/系统合成归因及物理呈现仍待证明，不修改buffer数量或动画来猜测规避。GC标记只按同进程/该帧时间筛选，其他进程HeapTaskDaemon事件不作Launcher归因。scheduling.json和long-frame-sections.json保存核算及原始区段。

五对书架和非状态栏场景像素一致；正式五轮Folder开关→桌面系统设置→HOME→Dock底部上滑→实际settings输入/结果启动→HOME→桌面设置→HOME同PID19549，捕获窗口无Launcher FATAL/ANR匹配，不包含Folder内打开联系人。修前/后各6秒录像保留。build.bat、v1/v2/v3签名、zipalign-P16、v1.5.8/33通过；正式SHA256 25d0ab51437931a3caf6595c0864361c36fc2f63abb92c1851e7a7914acfece4，拉回安装包一致，相对c7ae5701仅classes2.dex非签名成员变化。诊断后源码/正式产物恢复，正式DEX无FDIAG；Raster与RedirectDB本批字节不变，原53项暂存binary patch一致。真机留最终正式包，布局、默认桌面、日志及其他系统设置未改，MEMORY.md未更新。

**下一项：Folder打开期间SurfaceView dequeueBuffer等待。** 本批重复组件解析/无用标签读取局部收口；不再重复PM/label/hash计数。下一步对齐输入/动画、producer申请缓冲、releaseBuffer/fence、SF latch/present，确认等待发生在哪一帧及哪一侧延后；只有明确重复/无效工作或兼容异常才窄改。Folder总体、冷启动、九应用/动态图/跨ROM/长稳及物理显示仍开放。证据build/folder-source-resolution-20261018包含前态、负例、1670测试、诊断三组、正式五组、原始trace、截图、录像、构建/签名及verification.json。

<a id="2026-10-18-folder打开卡顿修复improved未命中后的apk回退键加载"></a>

#### Folder打开卡顿：修复IMPROVED未命中后的APK回退键加载

**真机根因：** 在V2458A/API36原有翻译机、对讲机、联系人Folder上，用临时android.os.Trace标记分开输入、GL场景初始化/绑定、键构造、纹理查询/合成、原版动画_r、eglSwapBuffers。三次进程首开及同进程再开，三枚纹理均命中、无重新合成；键构造却仍先解析/加载来源和扫描像素。翻译机/对讲机的日志明确为DEFAULT，联系人为IMPROVED。此前指纹仅覆盖显式原图/AUTO全局DEFAULT，漏了AUTO全局IMPROVED但资源未命中的最终APK回退。修前每开三次内容hash，累计首开5.558–6.162ms、再开7.534–9.795ms；动态图标检查/同步及安全区很小，不能以它们替代真实热点。

**最终最小修复：** 生产只改MaintainedLauncherSettingsHost.java。在原loadIcon中抽出同Owner的loadIconSource，保留强制原图、第二次override查询和最终APK回退顺序；普通loadIcon/loadIconForComponent仍返回真实Drawable。只有主用户/准确组件、AUTO全局IMPROVED未命中，第二次override也未取得图片时，允许现有defaultDesktopSourceFingerprint供纹理键使用。缺少安装/Activity元数据仍真实加载；回退期间图标才可用时仍返回实际Drawable，原类型/身份重查继续执行。未新增Manager/Bitmap缓存/线程/预热，不改动画、尺寸、阴影、资源或Loading；Raster本批与fb6506d5基线逐字节一致。原版j/init/_r对照结论保持，修复针对兼容来源链而非原版动画。

**诊断因果对照：** 同样标记的三组修前→修后，内容hash每次3→1，剩余联系人的真实受管图片；修后hash累计0.056–0.083ms首开、0.112–0.224ms再开。open至_r开始：首开[19.704,21.334,24.645]→[12.042,7.438,7.019]ms；再开[25.349,32.686,34.024]→[19.161,20.153,17.107]ms。这些是诊断CPU边界，输入ACTION_UP到动画/随后swap也已记录；swap不是SF present/物理可见帧。未用诊断值冒充正式性能。

**正式五组与功能：** 同机、同三应用/布局/主题，先fb6506d5后c7ae5701，保留数据/OS及ART缓存，顺序A/B非随机。首开最大onDrawFrame修前[25.372,28.655,28.273,35.740,30.909]ms，中位28.655；修后[16.922,20.213,16.675,13.266,17.404]ms，中位16.922。再开修前[36.739,30.369,30.460,39.111,39.073]ms，中位36.739；修后[13.161,26.313,22.211,23.334,25.161]ms，中位23.334。保留所有样本；本场景明确减轻，但再开仍超一帧，未宣布全部Folder/冷启动流畅。五对书架和非状态栏场景逐像素相同。正式五轮Folder开关→桌面系统设置→HOME→Dock底部上滑→实际settings查询/结果启动→HOME→桌面设置→HOME同PID3936；不包含Folder内启动联系人/翻译机，不扩写为全矩阵。修前/修后各留6秒开关录像。

**验证/边界：** 扩展既有tools/tests/icon_metadata/run_key_source_device_tests.py，480组合/1185检查在本Android16真机通过；新增IMPROVED回退0像素加载、来源在第二次解析期间到达、缺安装元数据回退、APK替换及DB补写、普通Drawable API不变。旧Host负例在新增IMPROVED缺失组合明确失败。使用提取生产方法、真实Bitmap/ART与夹具PM/来源，不冒充实际换包/网络现场。build.bat、v1/v2/v3、zipalign-P16通过，v1.5.8/33，SHA256 c7ae5701ac47ddd8d0f43607b28c11356ac2d58c35eaf289ae4d0c586b56a63d；相对fb6506d5仅classes2.dex非签名成员变化，拉回包一致。53项暂存binary patch一致；正式DEX无FDIAG标记和SourceHash候选类。临时源码/正式产物均快照恢复，真机留最终正式包，布局及系统配置未变，MEMORY.md未更新。

**失败与撤回：** 首次诊断安装被手机拒绝，随后无标记采集作废保留；安装确认后才产生有效trace。批量像素读取候选虽保持hash且微基准略降，未采用。弱键/世代号hash元数据候选在隔离相同Bitmap上有效（1445检查），实际Folder仍花相近时间且未消除回退来源重扫，已完整撤回，不保留新缓存；候选APK/trace存档。该测试初次编译变量重名/缺Map，以及错误假定32bit哈希随每次像素变化必不同的断言均保留，修正后用像素世代变化、重新扫描与旧hash等价验证，不以测试错误掩盖生产失败。最终1185测试不含撤回方案。原APK归档仍缺失，依据clean/raw一致参考及实际日志；证据统一build/folder-open-timeline-20261018。

**接下来：** 此处“IMPROVED未命中→最终APK回退”的像素加载已关闭，不再重测同一来源哈希制造进度。Folder总体仍开放；剩余首要边界是再开时来源解析/PackageManager/label/重查耗时与真实呈现，下一步细分这些调用，仅在确认同次解析重复时窄改；九应用/动态图标/其他ROM及长稳另列未验，暂不跳快捷桌面。

<a id="2026-10-18-用户纠正folder可感知打开卡顿未解决补齐原版逐方法对照"></a>

#### 用户纠正：Folder可感知打开卡顿未解决，补齐原版逐方法对照

用户再次指出文件夹打开仍卡一下；上一条局部来源键修复和GL回调中位下降不能替代“点击后开始动起来”的实际验收。本次重新提取clean_launcher、clean_launcher_raw和当前launcher的方法正文，忽略空行/调试行比较；七个选定方法的clean/raw正文一致。当前FolderController.j、关闭清理eh、FolderPageView.init和开启动画_r均与原参考一致。原版j每次new FolderPageView→init→a(FolderInfo)同步绑定/创建→挂入根场景/updateGeometricState→通知监听→_r开动画；关闭eh会onClose/removeFromParent/clear并清空Av/Bv。原版也每次建页面，并非永久保留完整打开场景；不能据此新增常驻场景缓存或缩短动画。

明确差异：原版Cell.cb直接ItemInfo.Ne→Ea.bb查询既有纹理，未命中才走e/s合成；当前在Ea.bb前加入applicationCellTextureCacheKey的来源/几何计算，未命中增加场景纹理分流，绑定后增加动态图标几何及阴影Owner同步。FolderPageView.a的新增部分是FolderSceneMetrics安全区根变换/裁剪；原版动画_r本体未改。ItemInfo.Ne仅建立条目标识，当前该方法也与原版一致，新增来源链在其调用后，不能称为原版必需。上批已移除明确DEFAULT的APK Drawable读取，但剩余键生成/节点创建/兼容调用各自耗时和点击至首个运动帧的分段仍未在此真机定位，静态差异不是卡顿因果证明。原版完整j/init/_r未改也不等于原版所有下游都未改。

证据build/folder-device-api36-20261018/original-comparison包含每方法三份正文、差异和methods.json；比较脚本compare_original.py保留。maintained的FolderPageView使用不同PageView/RectNode组织，仅作参考，不替换当前SMEngine链。original_apks/com.smartisanos.launcher-3.apk当前不存在，本次依据两个一致的本地反编译参考，不声称已重新反编译原APK或完成原版同机运行对照。仅更新调查/报告，无生产源码或APK变化，无新增性能收益；无需重复构建安装或重复已有五组。当前目标仍是修复用户可见卡顿：以原版一致的控制/动画为边界，定位输入派发→GL执行→绑定/缓存→_r→首个可见运动帧，保留系统profile拒绝与可移除诊断需求，不先转其他任务。MEMORY.md未更新。

<a id="2026-10-18-folder来源键已最小修复转android16真机验收"></a>

#### Folder来源键已最小修复，转Android16真机验收

**修复与根因：** Cell.cb在Ea.bb纹理缓存查询前生成来源键，DEFAULT路径也加载APK Drawable并哈希。仅在现有Host确认主用户、组件匹配、显式原图或AUTO全局DEFAULT时，复用ManagedIconSource携带安装时间、APK路径、UID、图标资源ID和Resources Configuration组成的指纹；缺少有效安装信息仍走原完整路径。Raster优先使用该指纹；CUSTOM/RESOURCE/IMPROVED/PACK及受管未命中时来源到达重查保持。生产只改MaintainedLauncherSettingsHost.java和IconRasterDiagnostics.java，不新增缓存、线程、预热，不改原版几何、阴影、动画和Loading。clean/raw及maintained对照沿用上一条调查；原APK归档缺失的限制仍在。

**已完成验证：** 扩展现有tools/tests/icon_metadata/run_key_source_device_tests.py，Android9/16各480组合、1168检查通过，涵盖安装替换、资源配置、APK路径、单应用来源切换、图标包回退期间到达、用户及旁路。完整ART再开窗口修前2次键生成伴随2次loadIconForComponent，修后2次指纹、0次该加载；修前首开窗口仅1条，不能当完整次数。第一次候选误将延后DB原图补写的raw hash加入键，首开最大回调中位恶化至92.066ms，已撤除该错误字段并保留失败证据，不安装该候选。

正式fb6506d5ad907c4d2317b0774cbc7f8428501fa9b5b483160dda5591ae9a7ce6，v1.5.8/33，build.bat、v1/v2/v3签名、zipalign-P16通过；相对紧邻88bab291基线仅classes2.dex非签名成员变化。API36/host GPU同场景五组首开最大onDrawFrame中位51.829→43.639ms，再开16.988→16.316ms；五对非状态栏场景/书架像素相同，五轮Folder应用启动、实际settings查询/结果启动、桌面设置返回逐轮同PID通过。先后执行且缓存受前序运行影响，不认定稳定整体收益；修后首开仍有长帧，Folder与整体冷启动未关闭。ART异常空trace对应独立进程自行SIG9，原因未定，不计有效样本；后续带PID/落盘校验的trace有效。

证据build/folder-source-key-fix-20261017。旧vivo Android9仅修前五组有效（首开/再开中位110.682/110.338ms）；profile使用不支持的clock参数失败，修后五组及搜索回归未完成，不能写成真机通过。用户确认手动创建的文件夹保留。10/18用户改用新接Android16真机V2458A/API36、1260×2800/560dpi/4KiB；已确认ADB授权，留存设备原安装包5d42e937…与桌面，直接使用已有翻译机/对讲机/联系人三应用文件夹，不启动虚拟机。

**Android16真机结果：** 紧邻基线88bab291与正式fb6506d5保留数据安装，同机同布局各五组独立进程首开/封面关闭/同进程再开。首开最大onDrawFrame修前[29.210,29.736,31.244,22.148,29.106]ms、中位29.210；修后[21.159,30.065,26.070,23.528,32.628]ms、中位26.070。再开修前[30.191,41.164,28.943,35.959,33.344]ms、中位33.344；修后[27.429,35.134,38.218,34.696,31.801]ms、中位34.696。保留全部样本，未清OS/ART缓存，顺序A/B非随机；首开中位降低但最坏值略增、再开中位未改善，不能宣布整体流畅度或冷启动已解决。五对完整书架及非状态栏场景逐像素相同。

真机提取生产方法480组合/1168检查通过，静态图标合同通过。五轮Folder打开/封面关闭→桌面系统设置启动→HOME→Dock底部上滑搜索→实际settings查询→设置结果启动→HOME→桌面设置→HOME全部完成，同PID14346，窗口内无Launcher FATAL/ANR匹配。此组没有从文件夹内启动应用，不扩大验收范围。最初中央Dock上滑后未确认搜索Activity，换左侧Dock并等待Activity确认后成功，早期XML是SystemUI、不得记查询成功。当前正式包拉回hash与构建产物一致；53项暂存binary patch逐字节不变。安装前5d42e937不是本次修前紧邻源码基线，未将其混入性能收益比较。

补充ART采样被真机SecurityException明确拒绝：正式进程not debuggable / not profileable by shell；去掉clock参数仍拒绝，不属于Launcher崩溃。未改系统日志/开发者选项或主APK Manifest绕过，未取得真机剩余Java子调用排名，不沿用模拟器排名继续盲改。性能及功能原始证据、失败和verification.json统一在build/folder-device-api36-20261018。正式包留在真机、用户文件夹及布局保留。MEMORY.md未更新。当前DEFAULT缓存键来源加载这一局部修复已通过来源/视觉/功能验收；Folder总体仍开放，下一项是利用可移除诊断包定位同机再开长帧的具体调用，诊断包与正式五样本分开，结束恢复正式包；之后才评估快捷桌面。

### 2026-10-17

<a id="2026-10-17-folder首开定位到缓存键前的系统来源加载尚未修复"></a>

#### Folder首开：定位到缓存键前的系统来源加载，尚未修复

当前正式88bab291…/v1.5.8/33在Pixel_6_Pro/API36/4KiB只读副本、host NVIDIA RTX3060、1080×2400/480dpi、12宫格黑主题/默认圆框、动态关闭。通过原版交互创建Maps与设置两个应用的固定文件夹，仅在临时副本改布局，真机未操作。5组独立进程首开→点击上方封面关闭→同进程再开：最大onDrawFrame首开[48.723,42.313,49.257,48.428,59.134]ms，中位48.723；再开[17.820,17.515,17.003,23.012,13.268]ms，中位17.515。各对PID不变，书架/两图标区域(80,650)–(1000,1750)逐像素相同。它们是GL CPU回调wall时长，不能替代GPU完成、SF present或物理可见帧，也不是修前后提速对照。

两次独立1ms ART采样都在FolderController.j→FolderPageView.a→Cell.cb→applicationCellTextureCacheKey→buildTextureCacheKey→desktopSourceForTextureKey→loadIconForComponent/ResolveInfo.loadIcon链采到阻塞：第一次ApkAssets.nativeLoad约50.037ms CPU，第二次ImageDecoder.nDecodeBitmap约52.049ms CPU；采样带开销，不能与上述正常帧时长相加，也不能推出精确读取次数/具体应用。Cell.cb先构造完整键，再查询Ea.bb，所以已有纹理仍可能先付出来源读取。当前DEFAULT回退参与resolvedSourceHash与类型/身份判定；直接跳过或长期记忆会改变换图有效性，尚无安全删除候选。本批不改生产代码、不增加缓存/预热/线程、不改尺寸、动画或Loading，Folder性能仍未验收。

对照clean/raw的FolderController.j、FolderPageView.init与a(FolderInfo)及maintained FolderPageView：原创建/同步事件链保留，当前场景安全区几何适配不据此回退；maintained不同引擎组织不能整块替换。原APK归档当前缺失，未伪称已反编译复核。静态图标合同PASS；现有正式包保留数据安装、拉回hash一致。5轮文件夹内设置启动→HOME→封面关闭→Dock底部上滑搜索/关闭→桌面设置→HOME完成，同PID7006；仅验证搜索入口/关闭，未验证查询结果。UI捕获流无FATAL EXCEPTION。未改源码故未重复构建；原53项暂存binary patch不变，MEMORY.md未更新。

失败记录：早期原始pair-*误以为BACK已关闭文件夹，实际再次点击标题进入命名弹窗，整组不计再开数据；修正为上方封面点击后的valid/五组，保留开关截图。最初解析器不识别E|pid，失败留档后修正工具。试建文件夹期间的相机启动/重排及fixture-open.atrace也不是有效Folder验收。有效证据统一在build/folder-first-open-20261017/valid、confirmation、ui及verification.json；其他初步数据不得选用冒充回归。

下一项：限定这条Folder缓存键链，先核对DEFAULT来源指纹在安装替换、单应用换图/在线图到达、分身/用户、主题及宫格变化时的现有失效Owner，再取得同条目/同版本的精确调用对照；只有能保留内容身份与失效语义才最小复用。发生新代码后再做同条件五组及来源/图标/搜索/设置回归；不重复本轮既有采样制造新进度。之后转快捷桌面真实打开缓冲峰值/GC。冷启动整体、原真机9图标长帧、可见帧及全ROM仍开放；A01–A25统计不变，不新增已完成项。

<a id="2026-10-17-a25_icon_cache_payload_and_mirror_boundary_fixed"></a>

#### A25_ICON_CACHE_PAYLOAD_AND_MIRROR_BOUNDARY_FIXED

**根因：** A25：下载校验只验证各PNG分块CRC，缺少图像数据、空IDAT、重复IHDR等仍能被写入缓存并阻止备用镜像；CRC正确而压缩流无效也会被发布。单镜像读入超过512KiB或响应期限时直接return false，跳过备用镜像。原始用例8断言失败，补充压缩流用例又确认2项实际失败。初始测试认为Android一定拒绝坏Deflate，实测9/16均可能返回部分Bitmap；该测试假设已纠正并保留原输出，不把native非空当有效性证明。

**修复：** 只修改现有IconPreviewRepository：沿用原CRC/尺寸/字节上限和写盘Owner，补充首个唯一13字节IHDR、实际IDAT数据及IEND边界检查；同Owner的hasValidPngData使用标准Inflater流式验证共享IDAT压缩流，8KiB缓冲、解压输出上限9MiB（涵盖现有1024边长RGBA16与Adam7），finally释放Inflater，不分配像素、不另建PNG像素解码器/缓存/线程。超限只终止当前镜像响应并进入既有备用链；取消仍立即返回且不尝试备用下载。像素文件不重编码，镜像顺序、超时数值、online_icon_cache_v4及负缓存一小时策略不改，原A24修复保留。

**验证：** JVM新37项、Android9/16各44项通过：合法RGBA/16位/Adam7、零长分块后有效数据、跨IDAT的zlib头、CRC/结构/截断/损坏压缩流/解压上限、HTML及超限响应回退、404与临时失败区分、读取返回时取消不发布/不负缓存、有效同名替换及坏更新保留旧图/无临时文件残留。HTTP为受控连接，不冒充真实镜像线路。seed/verify在不同进程；Android使用拥有的临时目录内平台SharedPreferencesImpl并等待QueuedWork落盘，新进程确认替换字节、真实解码颜色/Alpha及404标记。JVM偏好为代理夹具。首次平台prefs测试因后台线程存活而超时，未计通过；只修测试进程flush后退出，最终两设备完整通过，超时记录保留。队列161项和提取实际pause/resume/retry的14项共享回归通过。

正式包API36/host GPU中，分类页与全部图标网格各5轮外部设置暂停→BACK恢复，均同PID4483；实际日志确认旧ICON_LIBRARY会话取消及新会话打开，网格截图正常。取消记录pending/extra为0，表示未取得真实socket在途或未完成预览被暂停的样本；不能以此声称慢网在途UI取消也通过，该路径仅受控响应和既有队列测试覆盖。初次网格工具假定设置返回根页，实际正确恢复了库页，工具失败留档后按当前页面进入全部网格重测。未选择或应用任何新图标。

build.bat、v1/v2/v3签名、zipalign-P16、v1.5.8/33通过，正式SHA256 88bab291d7d58fcb5d7dbac81f9821438ae4d78688b11520259744b2b1fa81c8，模拟器保留数据安装拉回一致；对15923f86…仅classes2.dex变化，原53项暂存binary patch不变，无测试连接/探针进入主DEX，无本次Launcher crash/ANR。生产仅IconPreviewRepository.java；新增tools/tests/icon_preview/run_cache_tests.py是因为旧网络fixture替代fetch本体、不能验证真实字节/CRC/发布与跨进程存储；扩展既有tools/tests/icon_library/run_page_state_tests.py覆盖实际pause方法，未复制生产Owner。

**边界/下一项：** 同名更新验收仅限显式成功发布后的文件替换和新进程可见性；不新增远端自动刷新，发布同名资源仍遵守原缓存版本机制。本批不批量删除/重验历史缓存，不宣称完整PNG语义验证或全部线上坏包已关闭。原APK归档仍缺失，clean/raw/maintained无同名Java Owner，备用镜像行为按当前规则及PNG规范核对（https://www.w3.org/TR/png-3/）。真实镜像慢网/复杂坏包、旧缓存迁移、跨ROM、三星S25U Share现场及长稳仍未验收；冷启动整体未解决，清后台已恢复的返回现象不再复测。下一项转文件夹首开长帧：先确认实际可见卡顿与调用，不重复本轮缓存采样。 证据build/icon-cache-boundary-20261017保留原暂存/源码快照、负例/错误假设/超时、中间APK、最终探针/原始日志、跨进程summary、两组UI截图/XML/会话事件和verification.json；只读AVD退出不保存快照，真机仅隔离shell探针、未安装主APK或操作UI/日志/工程状态。更新六份现有报告，MEMORY.md未更新。

<a id="2026-10-17-a24_visible_preview_queue_eviction_fixed"></a>

#### A24_VISIBLE_PREVIEW_QUEUE_EVICTION_FIXED

**根因：** A24：预览低优先级任务排队期间，可见P0订阅加入相同pending批次，会话96阈值裁剪仍依据原P1/P2任务挑选，给可见行回调null；设置适配器会将该图标清空。另全局淘汰在检查消费者之后、队列移除/批次detach之前释放pending锁，允许P0订阅加入即将被丢弃的批次。前者修前新增用例6断言失败；第一次局部修后再加可控并发门，后者修前仍1断言失败；原始负例/中间APK和首轮UI均保留。

**最小修复：** 仅修改现有IconPreviewRepository：PendingCallback携带本次订阅Priority，保留旧双参构造；会话裁剪跳过有有效P0回调的共享批次。会话选择/移除/完成detach和全局检查/淘汰或拒绝/detach在同一pending临界区内完成，避免可见订阅在中间加入旧批次。全局继续renderAdmission→pending顺序，没有解码、网络、等待栅栏或同步UI回调进入锁内，没有增加Manager/队列/线程；既有512全局上限及8槽metadata预留不变，96原本就是低优先级裁剪触发阈值，不把它称为全P0硬上限。P0超出全局容量仍明确回调null，不宣称无限负载全成功。原有7行schedulePersistence保留，未覆盖用户暂存。

**验证：** 既有61项扩展到161项，桌面JVM及Android9真机/API36均通过；覆盖同/跨会话P1共享后可见订阅、取消单订阅后可淘汰、800个P0请求突发及8槽metadata、取消40/80会话后无旧回调/旧任务执行、32轮已完成待主线程投递时取消、会话与全局淘汰窗口中并发加入以及锁顺序终止。Android隔离使用提取的生产方法和真实ART执行器/MAIN Looper，主线程投递用栅栏控制，Bitmap/Drawable/cache/网络为夹具，不等于完整原生图片/GPU。测试门只注入提取副本，正式DEX无evictionGate。初次Android9隔离打印153通过但Killed退出，未算有效完成；只修测试进程退出方式后重新完成，失败日志留档。

最终build.bat、签名v1/v2/v3、zipalign-P16、v1.5.8/33和保留数据安装拉回哈希通过，SHA256 15923f869ab42ebd13b569426fc93cfdf9c99f0046884321848ae13655a77cf6；对b09ead0c…仅classes2.dex变化，53项暂存binary patch不变。API36/host GPU最终五轮Dock底部上滑搜索入口→桌面设置→应用图标页→三组快速上下滚动→HOME完成，每轮中途XML确认可见行变化，起止同PID5555，最终Launcher crash/ANR事件0条，截图/XML保留并人工复核。查询/结果启动未覆盖，不重复冷启动五样本冒充本次队列验收；真机仅读取SDK/锁屏与隔离shell进程，未安装最终主APK或操作UI、未改日志/工程配置。

**参考/范围：** 原APK归档仍缺失；clean/raw与maintained无同名兼容Java Owner可直接复用，适配器现有P1预取/P0绑定和generation防错位链已对照，本批不修改原版引擎/UI/图标内容、阴影、动画或内存策略。证据build/preview-queue-pressure-20261017含源码/暂存快照、负例、中间和最终测试、构建、安装包、签名及五轮UI；只读AVD结束退出不保存快照。本批证明并修复设置图标队列的受控可达丢回调路径，不能认定是三星S25U常用Share缺图的同一根因；三星现场、完整图片/全GPU压力、长期锁争用/峰值PSS、真实后台压力、全ROM、完整恢复及严格16KiB仍未验收。冷启动整体仍未解决；用户确认清理后台恢复的返回现象不再单列复测。下一项转图标库坏包隔离、暂停后取消、同名图片替换及跨进程缓存有效性；不重复本批已通过用例制造新进度。 更新六份现有报告，MEMORY.md未更新。

<a id="2026-10-17-gpu_backend_contrast_stage_closed"></a>

#### GPU_BACKEND_CONTRAST_STAGE_CLOSED

同一诊断APK、同一Pixel_6_Pro/API36/4KiB只读AVD、1080×2400/12宫格黑主题/默认圆框，host确认NVIDIA RTX3060、software确认SwiftShader。两后端各五次进程冷启，保留用户数据与系统/ART/磁盘缓存；先host后software，非随机交错。绑定后36次glGenTextures内部wall：host [74.439, 45.548, 50.193, 70.472, 42.894]ms，中位50.193；software [1519.419, 1449.889, 1123.302, 1119.243, 1110.335]ms，中位1123.302。两组均34个不同材质纹理未命中、4个不同Shader构建，无同名重复。

诊断PAGE_READY：host [4211, 3699, 4223, 2777, 2419]ms（中位3699）；software [23425, 9425, 10604, 5666, 4930]ms（中位9425）。保留全部慢样本，不以重采抹掉首轮波动。诊断日志/后端/冷暖均影响数值，本次是后端对照，不是生产代码优化A/B，也不是物理可见帧。

结论：之前SwiftShader约1秒的纹理分配等待明显受软件后端影响，不能据此认定正式APK存在同名重复纹理/Shader创建，不能外推真机；后端内部排队/同步根因未证明。本项阶段排查收束，无正式修复，不继续围绕同一来源/首轮纹理路径循环采样；整体冷启动仍未验收。

复用上批诊断APK，无源码插桩或重新构建；正式APK保持b09ead0c…，原53项暂存保持。每个后端随后保留数据恢复正式包，拉回哈希一致，各一次冷启PAGE_READY 1421/4305ms，仅恢复烟测。底部上滑搜索入口/桌面设置入口烟测通过。软件后端初次desktop.png中相机/文件/信息/通讯录等部分前景缺失，较晚desktop-late.png已恢复；没有定出首次完整可见时刻或直接根因，不能称首次视觉验收通过，前后截图保留。host两次查询脚本未通过：截图中settings停留IME候选区、编辑框仍为空；原日志、截图/XML留档，不认定查询结果/启动回归通过，不为本次GPU对照扩展搜索逻辑修复。未重复完整五轮功能，不称全功能验收。

用户再次明确：清理手机后台后返回桌面已恢复。A22撤下当前独立复测/修复，不再要求解锁，历史日志保留；仅将内存压力观察并入A18长稳边界，不把用户恢复现象当已证代码根因。下一项转图标P0可见任务队列峰值、取消与旧回调边界；既有production preview 61项通过，只补缺失压力/真实Android边界。主登记13局部完成、2部分、6开放、1历史现象合并、1候选撤回；不计算总体完成百分比。

证据build/gpu-backend-contrast-20261017，含后端身份、十个原始诊断样本及installed.apk、正式包恢复烟测、失败查询、入口截图、comparison.json、index-before.patch。只读AVD退出不保存快照；真机未安装或操作UI，未改工程/日志状态。MEMORY.md未更新。

<a id="2026-10-17-用户纠正返回加载现象已恢复撤下独立复测"></a>

#### 用户纠正：返回加载现象已恢复，撤下独立复测

用户此前已说明清理后台应用后返回桌面正常，本次再次明确不需要重复测试该现象。A22历史Create/SIG9证据保留，不继续作为当前独立故障排查，不要求用户解锁或开启日志。未证实的内存压力阈值/长期行为仅并入A18长稳边界，不把恢复现象写成已证代码根因。主登记改为13局部完成、2部分、6开放、1历史现象合并观察、1候选撤回，不计算总完成百分比。GPU对照收束后转图标可见任务队列压力/取消与旧回调边界；旧章节中的“下一项A22”均被本记录覆盖。MEMORY.md未更新。

<a id="2026-10-17-post_bind_render_profile_no_production_change"></a>

#### POST_BIND_RENDER_PROFILE_NO_PRODUCTION_CHANGE

**本项结论：** 临时诊断五轮均为绑定后34次材质纹理未命中且名称各异（21个asset名、13个文字纹理名），4次不同Shader程序构建，没有同名重复；P.glGenTextures绑定后到PAGE_READY共36次，内部wall累计1038.583/1235.445/1031.022/1094.064/1138.800ms，单次最大182–225ms。36次不等于34个miss的逐一对应，不把差额解释成冗余。21张基线APK资产逐像素哈希无重复，仅证明APK资源，不等于运行时所有主题来源相同。

**采样：** 两份SCENE_BIND_END后附加的1ms ART采样，完整未溢出。GL绑定后到完成派发前，glGenTextures叶CPU驻留约268/529ms、nativeDecodeAsset约240/100ms、glCreateShader约87/15ms；均为采样辅助且有附加开销，不能当调用次数/正式启动时延。GL wall记录各倒退1/2次，CPU无倒退，放弃wall排名。

**根因边界与参考：** Ea已按名复用纹理，ta已按名复用Shader，sa.create有mProgram>0返回门，Da.bind有现存纹理ID复用门。raw原版参考的sa.create/Da.bind与本轮修前归一化一致；clean_launcher该部分缺失，改查clean_launcher_raw；原APK仍缺失。maintained有同类缓存和程序门，仅参考。当前证据是首次真实创建/后端调用占用，没有成立的安全删除候选，不新增Owner/缓存/线程，不提前派发完成、不隐藏加载。glGenTextures耗时可能包含后端同步/排队，尚不能定位驱动内根因或外推真机。

**恢复与回归：** 正式包仍b09ead0c…/v1.5.8/33，临时P/sa/mymaterial.f计数源码及APK/idsig均恢复原字节，原53项暂存binary patch保持。诊断build.bat通过，恢复后签名v1/v2/v3、zipalign-P16及安装拉回哈希一致。API36/4KiB/SwiftShader、1080×2400/12宫格黑主题/默认圆框，同包五次PAGE_READY为6868/6066/5546/5789/5210ms，中位5789；绑定到PAGE_READY为2365/2137/2098/2022/1823ms。只为同包回归，非新优化前后比较，不等同物理首帧。

五轮Dock底部上滑300/500/800/650/900ms→搜索settings→结果启动设置→HOME→桌面设置→图标查询→HOME完成，逐轮起止同PID5600；最终Launcher am_crash/am_anr事件为空。有效两页截图与上批同哈希包在[0,110,1080,2300]对照：page0变化像素448；page1变化像素448。差异均仅在页码指示器[x517..562,y2006..2021]：当前隐藏、参考可见，原图及局部放大留档，不称整页零差异；独立图标宫格[0,115,1080,1970]两页均零差异。搜索、图标查询及桌面截图人工复核。

**证据/后续：** build/bind-render-profile-20261017内保留两份trace、计数五轮、诊断APK、源码/产物快照、reference-check/asset-check、正式五样本、有效两页及UI截图/XML、verification.json。真机本轮仅读取SDK确认API28，未安装或改变配置/日志/工程状态；只读AVD不保存快照。下一项先做Android16硬件GPU后端与当前SwiftShader的同路径对照，或在可用真机采同一GL阶段，分开资源解码、纹理分配/上传及驱动等待，确认可移除工作再最小修复。冷启动整体、可见帧、真机UI/三星Share现场、全ROM/长稳及严格16KiB仍开放；A11/A19部分、A22等开放的登记不变。 MEMORY.md未更新。

<a id="2026-10-17-post_ready_persistence_profile_no_production_change"></a>

#### POST_READY_PERSISTENCE_PROFILE_NO_PRODUCTION_CHANGE

**本项结论：** 对补写原生成/PNG/数据库链完成定点采样和分支计数，未据此删改正式逻辑。五轮每轮21条任务：原图PNG/MD5校验21次，MD5命中20次；com.google.android.calendar走强制重建1次，另编码dark/light/transparent三套缓存3次，总PNG24次，原写库接口1次且返回true。21条DONE不等于21次写库，也没有每个条目重复生成三套缓存。现有LauncherSettingBridge.shouldForceDynamicIconDatabaseWrite保留动态/普通模式交接的MD5旁路；这次观察到动态关闭时日历仍走该分支，但尚未建立可取代交接保护的模式/来源有效性证明，不删除该保护、不改MD5协议或缓存格式。重复编码消除没有成立的安全候选；不为产生修改而改动原版链。

**采样与限制：** 正式b09ead0c…APK通过am profile在SCENE_BIND_END后附加1ms/dual-clock采样，两份完整、未溢出trace覆盖icon-online。CPU记录无倒退；nativeCompress叶CPU采样约110/173ms，解码约128/20ms，资源冷暖明显，不能当稳定收益。两份wall记录分别出现3/2次倒退，旧analyze_profile产物的inclusive wall排名不采信；sampling-summary.json只作CPU驻留辅助，不把采样entries当精确调用数。初始全启动trace停得过早，首次聚焦采集遇到PID尚未创建，非采样输出0字节，均留档，不纳入有效计数。

**精确计数办法：** 仅诊断APK在Aa/e.s现有PNG、MD5分支和写库调用加无用户数据的日志，不改变分支条件和返回值；连续5轮按实际DONE线程TID过滤，确认21/20/1/24/1计数一致。原APK归档仍缺失；clean_launcher中Aa/h与原三套缓存链已对照，maintained对应LauncherModel/ShortcutIconHelper仅参考，未搬运其写库实现。诊断构建通过后，Aa/e.s及全部build APK/idsig恢复修前字节；正式生产源码、签名APK仍b09ead0c382ddab1119a26c0ed867a3298b6d3c1727ff95d7b0de00f7b6e69f8，无采样/计数入口遗留，原53项暂存未动。没有新增Owner/缓存/线程或正式修复文件。

**正式包回归：** 恢复b09ead0c…保留数据安装到同一API36/4KiB/SwiftShader只读AVD，5次PAGE_READY 4912/5940/4913/4534/4610ms，中位4912；只是同包恢复后回归，无修前/修后收益含义，标记不是物理首帧。两页formal-visual截图复核仍处加载阶段，已作废，未完成本批像素对照；Dock上滑搜索→设置结果启动→HOME→桌面设置→应用图标查询→HOME五轮记录见本批功能报告。原正式签名/zipalign-P16再验证；本批未安装或操作真机，未调整日志/工程设置。当前只读AVD已退出，ADB仅余真机；退出后末次crash/ANR事件无法补取，不声称该项验收通过。

**证据/下一项：** build/source-persist-profile-20261017含原始trace/失败采集、临时APK、诊断五轮计数、源码和APK修前快照、正式五样本及功能截图/XML/恢复核验。后台补写已定位，暂保留其内容有效性检查和交接保护。下一项回到冷启动关键路径，重采SCENE_BIND_END→PAGE_READY的首轮绘制/纹理上传/Shader创建，确认真实阻塞或重复工作后才最小修复。日历模式切换、真实GPU/可见帧/PSS长稳/全ROM仍为待验专项；冷启动整体未解决。MEMORY.md未更新。

<a id="2026-10-17-uncached_static_source_composition_and_post_ready_load"></a>

#### UNCACHED_STATIC_SOURCE_COMPOSITION_AND_POST_READY_LOAD

**根因/最小修改：** 无原图缓存的普通静态纹理缺失，原prepareUncachedStaticSource先准备分类图、Smali合成又重新解析来源。复用现有StaticSource、同一准备/分类/合成链及PENDING_SOURCE_WRITES：public旧API保留，内部重载支持同步合成，Smali先尝试composeUncachedStaticApplicationIconTexture。非圆框正式Drawable请求2→1，五类来源的type/identity查询各2→1（含DEFAULT圆框；其Drawable本来1次仍1次）。以上是提取生产方法的Android隔离计数，不等于磁盘解码次数。缺源、APK_DEFAULT兼容回退仍进入原准备/恢复路径；非空原图字节（含损坏字节）继续上批解码/恢复门。队列512上限、条目合并、页面就绪后调度和拒绝重试不变，队列只存条目、不存Bitmap。合成在退出补写锁后进行，共用独占临时图finally释放/别名转交；没有新增Owner/缓存/线程或跨调用来源状态。

**原版与范围：** 原APK归档仍缺失，clean/maintained无该兼容Java方法。生产仅IconRasterDiagnostics.java与e/s.smali；原完整合成体、scheduleSourceWrites和persistSource与修前逐字对照不变，原分类/阴影/几何/GL完成/HOME链未改。两个既有测试脚本扩展当前来源与无缓存对照，无测试夹具进入主APK。

**验证：** 修前288项无缓存对照，修后Android9/16各289项无缓存检查及246项上批同步入口检查；覆盖五类来源、同identity替换、空/坏缓存、APK_DEFAULT回退、恢复、队列上限、异常和别名所有权。记录合成夹具非完整GPU；原resolver481+生命周期289、补写暂停/单批合并/队列拒绝重试/过期身份、58+24阴影/Smali及图标合同通过。标准build.bat、v1/v2/v3、zipalign-P16及v1.5.8/33通过，最终SHA256 b09ead0c382ddab1119a26c0ed867a3298b6d3c1727ff95d7b0de00f7b6e69f8；相对f2d0af9b…仅classes.dex/classes2.dex变化，原53项暂存未动。

**同条件五样本：** API36/4KiB/SwiftShader只读AVD、1080×2400/12宫格黑主题/默认圆框，保留用户数据及OS/ART/磁盘缓存。基线PAGE_READY 5121/5581/4565/4667/4633ms（中位4667），最终4334/4716/4427/4787/4436ms（中位4436）；scene中位2337→2282ms，绑定后1796→1592ms。前后组未随机化、范围重叠，不认定整体稳定提速或物理首帧改善。两页桌面裁剪区域像素零差异。五轮Dock底部上滑300/500/800/650/900ms→搜索设置结果→系统设置→HOME→桌面设置→应用图标查询→HOME均同PID6637，无本次Launcher crash/ANR。

**PAGE_READY后负载：** 常规五次均释放21条任务、各完成21个唯一条目，无FAILED/MISSING/DEFERRED；最后完成距PAGE_READY基线1236/1289/1087/1087/1047ms，最终1076/1000/1031/1080/1099ms，中位1087→1076ms。DONE仅说明原生成调用返回有效字节，不能据此声称21次SQLite/磁盘写入。另各5次独立后台观察，不混入上述主计时：首次post-ready shell采样到约3s后，整进程CPU增量中位970→900ms，对应实际DONE线程的icon-online增量250→220ms；后段约1–3s该线程CPU增量均0。10ms粒度且漏掉首次采样前工作，整进程含GL/动画/GC，不作稳定负载下降结论。窗口首末RSS中位分别271736→223276KiB、304704→220312KiB，不是峰值/PSS或泄漏证明；修后首采样RSS更高，不能宣称内存降低。shell读取进程IO被拒，未填0冒充实测。

**立即搜索边界：** 额外冷启动PAGE_READY后228ms开始Dock上滑，当时仅完成1/21条补写；搜索打开并显示设置图标、返回同PID6637。末条补写在2283ms，查询输入完成3303ms，因此只覆盖补写期间发起入口，不冒充“补写未完时查询结果”验收。原AM提示HOME自动启动实例收到Intent，不是崩溃；日志保留。

**证据/下一项：** build/uncached-source-compose-20261017保存源码/暂存/APK修前快照、原始20次启动（主计时前后各5、后台观察各5）、逐轮日志/截图/XML与验证JSON。真机仅隔离检查，未安装本批包验真机UI/五样本，未调整工程模式/日志；只读AVD结束关闭不保存快照。下一项对21条补写的Aa.a→原生成/PNG编码/数据库链做定点采样，区分必要补写与重复工作，再最小修复。冷启动整体、PSS/Graphics长稳、首次重建A22、全ROM/严格16KiB继续开放。MEMORY.md未更新。

<a id="2026-10-17-call_local_static_source_composition"></a>

#### CALL_LOCAL_STATIC_SOURCE_COMPOSITION

**根因/范围：** 已有有效原图缓存的普通静态纹理缺失时，Smali先解码原图，prepareStaticSource解析正式Drawable并生成独占分类图，composeTexture又解析一次。非圆框分支重复正式来源请求；DEFAULT圆框原有复用已是一次。不能凭相同identity或预览generation跨调用保留来源，同identity可以替换像素。

**最小修改：** 复用现有StaticSource、准备实现和唯一合成器。e/s只在原iconRawSource成功解码且高分辨率静态分支中，调用同类内同步入口，一次解析紧接准备/原分类器/原合成；调用结束不保存来源，下次纹理重建重新解析。源缺失、APK_DEFAULT兼容回退、无/坏原图缓存均回原分支，保留512条补写门及持久化Owner。没有新增Manager、线程、版本门或常驻Bitmap缓存。准备独占副本在finally释放，合成返回该副本时转交；API不回收借用输入。Smali仅成功后回收iconRawSource本次新解码的输入，失败分支仍持有输入给原恢复流程。原合成体、分类算法、几何、阴影、投影、GL完成和HOME交接未改。

**验证：** Android9/16各246项本地同步链检查，覆盖五类来源、同identity换像素/类型、来源恢复、空/损坏字节真实解码、异常释放、别名转交和借用图存活。最终合成在该探针中为记录夹具，不能冒充完整GPU测试。既有resolver481+生命周期289在9/16通过；键来源480组/1093项、搜索11项Android图像用例、补写队列及58+24阴影/Smali、图标合同通过。原APK归档仍缺失，clean/maintained无该Java兼容链；原版分类及原合成体对照保留。标准build.bat、v1/v2/v3及zipalign-P16通过，v1.5.8/33最终APK f2d0af9bba21af878065daa3f86394117a87a989fa082fdae8d8b3f5961eba76；相对0e4c466c…仅classes.dex/classes2.dex变化，原53项暂存不变。

**五样本：** 同一只读API36/SwiftShader/4KiB/1080×2400/12宫格，保留用户数据及系统/ART/磁盘缓存，基线PAGE_READY为4466/4318/5601/4053/4161ms（中位4318），最终4171/4642/4252/4259/3770ms（中位4252）。scene中位1885→1899ms，绑定后1839→1638ms；范围重叠，不宣称整体稳定提速，FIRST_FRAME回调不是物理可见帧。两页桌面裁剪区域像素零差异。五轮Dock上滑搜索→设置结果启动→HOME→桌面设置→应用图标查询→HOME逐轮同PID5357，通过，未见本次Launcher crash/ANR。

**证据/边界：** build/local-source-compose-20261017。初始探针直接比较未预乘颜色的断言失败留档，改比Android实际像素后通过；首次构建的宽字节入口未安装，收紧至成功解码入口后重新构建和验收。first-edit-snapshot文件是在第一次编辑后抓取，不冒充原始源码快照，原合成体对照用上批来源及已核实的日志参数修复；计时基线APK独立保存并核对安装哈希。真机仅隔离用例，未安装本批包做真机UI/五样本；未改真机工程模式/日志状态。只读AVD结束关闭且不保存快照。

**下一项：** 无原图缓存的首建/延后补写仍保留原两段链，先量化其重复解析与PAGE_READY后负载，再验证能否在原有补写Owner内局部复用。冷启动整体、真实首交互/内存长稳、A22首次重建、跨ROM仍开放。MEMORY.md未更新。

<a id="2026-10-17-prepared_source_lifecycle_and_decoration_metadata"></a>

#### PREPARED_SOURCE_LIFECYCLE_AND_DECORATION_METADATA

**本轮任务/进度：** 继续准备→合成阶段重复来源和Bitmap生命周期核对；总体进度及剩余任务集中更新到LAUNCHER_FIX_AND_OPTIMIZATION_PLAN顶部、问题清单口径同步。A01–A23主问题去重为13项局部修复/维护并回归、2项部分完成、7项未闭环、1项不可达生产候选撤回；父子项不能折算成整项目完成百分比。结构/重点链审计和五份报告已完成，完整冷启动、返回、跨ROM、恢复/长稳验收仍未收口。

**量化/所有权：** 既有prepared_icon_source增加--audit-lifecycle，提取生产准备、Bitmap转换、合成Resolver和分类入口。五类非圆框来源准备1次+合成边界1次正式请求；不等同两次磁盘解码。准备副本用于本次颜色/resize分类，不能用旧ItemInfo.color替代；copy像素/Alpha不变、回收副本不损坏共享图源，缺图则可能返回借用cachedSource，不能统一回收所有输入。同类型/身份仍能换像素，candidateRevision未证明覆盖全部实际图源，跨阶段复用须另建立局部传递和失效/所有权门。Aa.g→e.s.c([B)为从Model字节新解码位图，不是直接返回共享Bitmap；该恢复分支释放责任另查，不误并入借用规则。未证明永久泄漏，不强制GC或改变缓存容量。

**本轮安全最小修复：** 合成器已有resolved.type，decorateProfileIcon只为日志又执行一次完整desktopIconSourceType。仅IconRasterDiagnostics四行生产改动：私有方法接收当前类型、一个调用点传入、两处日志复用。像素/徽标逻辑和回收顺序不变，无新Owner、缓存或Bitmap跨阶段持有，Host/Smali逐字节未变。80组提取生产装饰方法，类型查询1→0、像素和返回对象归属不变；修前方法与前一正式包源码完全相同。Android9/16原481项及新增289项检查通过，分类器/徽标外围为夹具，不称完整GPU或真实分身验收；阴影58/主题24及图标合同通过。

**最终构建/对照：** build.bat、v1/v2/v3签名、zipalign-P16、v1.5.8/33通过。APK SHA256 0e4c466c24139eacf4cc11927467e311d1a06860f67bafebad003799318c0d1c，对上一0d9794b8…非签名成员仅classes2.dex变化，原53项暂存不变。API36/4KiB/SwiftShader只读副本、12宫格黑主题、默认圆框，保留用户数据/OS/ART/磁盘缓存。修前五次PAGE_READY4621/4016/4166/5107/4739，中位4621ms；最终4657/3813/3827/4307/4295，中位4295ms。范围重叠，A后B未随机化，不以326ms观测差认定整体稳定提速；完成标记不是物理首帧。两页[0,110,1080,2300]区域像素完全一致。

**采集失败/功能：** 候选安装后的首次logcat一次性探针握手失败，0个有效样本，流和错误保留candidate-handshake-failed；工具在10s握手截止前重复确认探针，计时样本开始前完成，不放宽生产Loading/手势或拿安装自启动当冷样本。重新采集最终五次成功。最终5轮Dock上滑300/500/800/650/900ms→settings搜索图标/启动系统设置→HOME→桌面设置→应用图标查询→HOME均同PID5343，截图/XML保留并核对。真机只执行隔离，不覆盖安装新APK/操作工程设置或日志；本轮按用户允许使用Android16，测试后只读AVD关闭且不保存快照。

**文件/下一项：** IconRasterDiagnostics.java、现有run_device_tests.py和六份主文档；证据build/prepared-chain-audit-20261017。准备/合成间的第二次来源请求仍保留；下一项验证局部传递解析结果和独占/借用标记、来源变化失效，确认后再窄改和五样本/功能回归。随后继续首次返回重建/内存压力、Folder首开/锁屏及队列压力等；全恢复/分身、HOME光影、全ROM/严格16KiB/长稳仍待验。MEMORY.md未更新。

<a id="2026-10-17-texture_key_source_reuse_implemented"></a>

#### TEXTURE_KEY_SOURCE_REUSE_IMPLEMENTED

**根因/最小修改：** 来源hash先完整加载图像，type有效性检查再次解析正式来源，identity又读取CUSTOM完整数据。复用Host既有ManagedIconSource，在单次纹理键调用内携带Drawable/type/identity；正式resolver和identity新增接收已读redirect的内部重载，原public入口保留。IconRasterDiagnostics只在普通userId=0、包名/组件精确一致、非动态/设置/快捷的键上使用该结果，hash算法和键格式不变；没有新增来源Owner、长期缓存、线程、几何/阴影或生命周期变更。

**回退边界：** 检查发现图标包非阻塞未命中可能在回退中变为可用，最终包只在正式受管来源命中时复用metadata；未命中返回的metadata为null，仍走原type/identity重查，不固定DEFAULT。专门用例验证此变化。分身/异组件保留原链；异组件可能多一次资格查询，未证明全ROM无耗时退化。原APK归档缺失、clean_launcher/maintained无同名兼容链，对照沿用前批已核对结果，不替换原版核心。

**同图读取对照：** 新tools/tests/icon_metadata/run_key_source_device_tests.py提取修前/后生产纹理键、hash及来源方法，真实Android PNG、不同原图/受管图案、Context/PM/图标包外围夹具，API28/36均480组/1093项通过。有效CUSTOM同图文件解码和PNG重编码4→1；IMPROVED来源请求及夹具PM请求2→1。完整键、缺失/损坏、内容/资源身份替换、PACK晚到、用户/组件/非Bitmap旁路与Bitmap借用生命周期检查通过；只证明隔离链，不冒充完整APK现场次数。旧身份720组/3690项、Android来源481项、搜索11项、补写队列拒绝重提、阴影58/主题24及图标合同通过。

**交付/五样本：** 标准build.bat、v1/v2/v3签名、zipalign-P16通过；最终v1.5.8/33，SHA256 0d9794b88a0d1224b8c99091453c81cbcdf02bd9e714b42d4ef4e44b39a3ab67，相对e3d84deb…仅classes2.dex变化，无临时自采样入口，原53项暂存binary patch不变。按用户选择在API36/4KiB/SwiftShader只读副本上保留数据，紧邻基线和最终包各5次并拉回hash一致；PAGE_READY基线4752/5536/5495/9104/5389、最终4397/4388/5010/4898/4710ms，中位5495→4710ms。初始基线中位4390ms，明显波动、9104ms样本保留，不认定整体稳定提速。更早非最终候选的五样本亦完整保留，不混为最终验收；两页区域零像素差。

**功能/收口：** 最终包5轮底部上滑300/500/800/650/900ms→搜索settings与结果图标→启动系统设置→HOME→桌面设置→应用图标查询→HOME，全程PID7279，截图/XML保留并人工查看搜索及图标查询。非最终工具第二轮将保留的查询追加为settingssettings导致失败，原记录保留，修工具先清空输入后重跑最终5轮；不是删除产品保留查询功能。未见该最终回归期间Launcher am_crash/am_anr，主动force-stop的冷样本退出不算故障。本批真机只做隔离用例，未安装新包进行真机UI/五样本；未调整工程设置，日志仍no。用户后续偏好为日志再次开启后保持开启，本批改用Android16，不冒充已重新开启真机日志。只读AVD测试结束关闭、不保存快照。

**文件/下一项：** 两个生产文件、上述新增用例、run_source_identity_tests.py重载提取夹具及性能/功能/问题/计划/维护文档；证据build/source-key-reuse-20261017。下一项量化prepareStaticSource→composeTexture剩余来源请求与生命周期，不能跨阶段直接保存可能已加圆框的Bitmap。A22首次返回重建、全ROM/压力/长稳及冷启动整体仍开放。MEMORY.md未更新。

<a id="2026-10-17-source_hash_validation_draw_read_audit"></a>

#### SOURCE_HASH_VALIDATION_DRAW_READ_AUDIT

按用户要求只读核对来源哈希、有效性检查及正式绘制。确认Cell在Ea.bb缓存查找前先生成含resolvedSourceHash的键，hash加载正式Drawable并扫描Bitmap像素；type的hasEffectiveManagedDesktopSource另加载受管Drawable仅判非空，prepareStaticSource/composeTexture亦重复请求来源。IMPROVED在线磁盘命中后放入已有sSmartisanIconCache，后续同源通常复用Bitmap，不能把重复请求写成重复解码。CUSTOM的完整redirect读取则每次decodeFile并compress PNG；类型/身份和正式加载均使用该接口，存在明确重复工作。资源/APK解码次数受Android资源缓存影响，未冒充精确次数。

重解析上批两份修后trace，resolvedSourceHash inclusive456/454ms，磁盘decode叶路径38/37ms，getPixels叶路径34/26ms；有效性检查inclusive377/359ms，PM Binder叶路径83/86ms。采样有开销、inclusive重叠，无条目参数，非本日重采样或正式五样本，不能据此计算收益/同图精确次数。详细链路、缓存差异及最小复用范围写入PERFORMANCE_BASELINE_AND_OPTIMIZATION顶部，证据build/source-read-audit-20261017。原APK归档缺失，clean_launcher/maintained无该兼容链；不动原核心。

未修改生产代码/APK或设备配置，未重建/安装，不重复功能与五样本冒充新修复验收；原53项暂存binary patch仍一致。下一批在现有ManagedIconSource中验证同次解析结果供hash/type/identity消费，先取得同条目/来源次数负对照，再窄改与五样本、像素、图标/搜索/设置/返回回归；不新增常驻图像缓存，不用旧iconRawData或文件存在替代真实有效性。A22首次重建风险仍开放。MEMORY.md未更新。

### 2026-10-16

<a id="2026-10-16-source_identity_reuse_after_profile"></a>

#### SOURCE_IDENTITY_REUSE_AFTER_PROFILE

**收尾补充：** API36另5次系统设置返回全部同PID4642；底部上滑搜索settings、结果图标/启动系统设置及桌面设置往返完成，同PID4642。手机日志采集已通过系统UI停止，计时归零、persist.sys.log.ctrl=no，回到桌面；本批只读AVD已关闭且不保存快照。功能及问题清单同步更新，首次重建失败保留为A22，未作全部启动/返回问题解决声明。

**重新采样/根因：** 按用户要求回到修后剩余启动路径。vivo X21A/API28两次1ms自采样均确认desktopIconSourceIdentity重新进入刚执行过的desktopIconSourceType→hasEffectiveManagedDesktopSource，重复PackageManager查询和正式图标来源检查。identity的GL inclusive采样驻留298/289ms；分类c/d为嵌套调用，c约107/114ms，未证明冗余，不改分类或原阴影。Eb.oh的纹理预载已先查Ea.bb缓存，没有取得重复上传的充分证据，不改SMEngine或预载顺序。采样有开销、inclusive重叠，不能作为正式耗时或精确调用次数。

**最小修改/文件：** MaintainedLauncherSettingsHost.desktopIconSourceIdentity新增包内重载接收紧邻调用已解析的effectiveType，原单参入口保留；IconRasterDiagnostics的resolveStaticSource/buildTextureCacheKey两处传入该值。无缓存/Manager/线程池/选源规则/栅格几何/资源或生命周期变动。tools/tests/icon_metadata/run_source_identity_tests.py提取修前/修后生产方法比较720组/3690项，包含缺图回退、DEFAULT/自定义/资源/图标包、全局选源、空上下文/条目及旧入口；负对照证明paired类型解析2→1、输出一致。prepared_icon_source原Android夹具只补重载桩，481项通过；必要补写并发/拒绝重提、阴影58/主题24、搜索真实PNG/Looper11及静态图标合同通过。clean_launcher原分类f与现行字节相同；原APK归档缺失、maintained没有本兼容Host入口，不替换原版核心。

**采样复核：** 修后两份trace的identity驻留约52/50ms，未再出现identity→type子路径；没有宣称消除所有重复来源读取。临时profile源码已逐字恢复、正式DEX无TEMPORARY_PROFILE/launcher_startup_profile标记。正式build.bat、v1/v2/v3签名、zipalign-P16和版本v1.5.8/33通过；APK SHA256 e3d84deb8fc8157ce2cf5a93945bda5693dee084155e729a4accc512c6d57fe3。相对基线5e1b3d1b…非签名成员仅classes2.dex变化，核心DEX/资源/Manifest/native库未变，原53项暂存binary patch对照一致。

**同机五样本：** 当前20宫格/网格主题/动态图标关闭、保留数据和OS/ART/磁盘缓存。诊断安装前首个基线5次PAGE_READY3021/3037/3055/2994/3021ms保留；诊断取样/回装后紧邻正式基线3038/3111/3032/3048/3080ms，候选2921/2857/2827/2809/2771ms。中位PAGE_READY3048→2827ms（约-7.3%），scene task→bind2271→2030ms，DB211→208ms、bind→ready237→244ms；FIRST_FRAME388→387ms，候选首轮451ms保留。前两页SOURCE_IDENTITY中位126.684→18.099ms。A后B未随机化，不能外推首装、低内存、总功耗或全部ROM。两页区域[0,110,1080,2220]逐像素零差异，人工核对图标/阴影/布局。

**真机功能/异常留证：** 采样前5次桌面点击系统设置→HOME均PID25173。正式包最初五轮搜索/设置/图标查询中，首轮2957在Launcher重新Create/MAIN_VIEW_INIT后自行SIG9→3629，与旧J.b(Activity)重复初始化保护相符；未抓到直接调用栈，Activity重建触发条件仍未闭环，不能归为ABE或本次identity改动。旧UI工具把每轮PID与初始PID比较，后续4轮虽保持3629也显示false，原输出保留不改；补充工具逐轮记录pidBefore，再5轮Dock 300/500/800/650/900ms→搜索settings图标/结果启动系统设置→HOME→桌面设置→图标包名查询→HOME，5/5始终PID3629，截图对原模板通过。首轮失败不因补测成功被抹去，冷启动整体及重建风险未关闭。

**Android16/下一项：** 同一正式包在API36/4KiB/SwiftShader只读AVD保留数据安装、拉回hash一致；首次logcat握手失败未产生样本，原目录保留，重试5次PAGE_READY4316/5249/5722/5099/4151ms，中位5099ms，仅兼容回归，无同会话A/B收益结论。证据build/startup-remaining-20261016；后续继续检查resolvedSourceHash、正式来源有效性检查和实际绘制是否重复读取同图，须具体调用/次数证据后才窄改，再五样本及功能回归。MEMORY.md未更新。

<a id="2026-10-16-android9_external_return_blocker"></a>

#### ANDROID9_EXTERNAL_RETURN_BLOCKER

**最新用户恢复反馈：** 用户清理手机后台后报告外部应用返回已正常。随后仅作只读内存快照：MemTotal=5839880KiB，MemAvailable=3568516KiB（约3.40GiB），Launcher PID25173 TOTAL PSS=209654KiB（约204.7MiB），其中Graphics=114116KiB（约111.4MiB）、Java Heap=28432KiB、Native Heap=44616KiB。当前可用内存充足；清理前/触发瞬间无同步内存压力证据，不能由恢复反馈直接确认Launcher泄漏、LMK回收或ABE具体策略阈值。历史退出执行者ABE已证实；内存压力/后台负载为优先待验证条件。未再次操作应用往返或调整设备状态，不把用户恢复反馈冒充新的5轮同PID验收；本次仅更新文档，MEMORY.md未更新。

**20:45后授权对照与交接实验复核：** 用户允许临时开启自启动并恢复。实际UI确认关闭→开启→5次系统设置返回→仍全部换PID；UI确认开关在5次后仍开启，再恢复关闭→5次返回仍全部换PID。不能将自启动关闭认定为本次根因，系统日志保持no、未改电池/默认HOME/导航/关联启动。随后按用户要求检查交接实验前版本：build/home-return-audit-20261011/baseline.apk（SHA256 50a8befb8e8d2bd0843905776a364721b00a245bb2f7a88f24b2cbd03b88ab11，v1.5.8/33）反编译确认LauncherHomeCompat尚无HOME生命周期/PixelCopy/Surface交接实验；保留数据安装该包，同一路径5次仍全部换PID。它比上一轮4944…旧包更早，未将含交接实验的近版当作实验前版本。

**旧返回实现与现行差异：** 10/11实验前APK与当前J.onPause、J.onResume、Eb.onResume去行号后的Smali逐字相同；普通Resume走原J/Eb恢复场景/动画时钟并请求渲染，HOME Intent仍经FROM_HOME_KEY或MAIN+HOME进入J.a(Intent)，没有把普通热恢复改为主动冷启动。Launcher层新增关闭为默认的诊断钩子；当前LauncherHomeCompat与10/14动画交接实验前、10/13背景同步实验前备份SHA均为fe89c832…，10/13绘制同步前仅少了回调日志包装。当前三项HOME全局开关均null、log.tag.SmartisanHome为空；附着Surface实验要求API34+，独立模块HomeMergeVisibility要求API36，在本API28机不适用。废弃PixelCopy/Texture原型未恢复。实验前包在当前设备状态也复现，不支持直接归因交接动画，但仍不能解释用户此前正常状态何时变化。

**补充限制：** 只读看到系统ABE更新版5.17.0.0/target35、内置版4.6.0.12，不据版本差异推断兼容故障。REA Android入口缺少调用方JADX MCP JAR，未更改配置或安装工具；改用已有apktool仅反编译Launcher历史包并比较本地源码。当前强停触发条件仍未查清，生产逻辑未修改；最新5e1b3d1b…包已恢复安装，后续以最新包真实返回复测为准。证据新增autostart-on-routes、autostart-restored-routes、pre-experiment-1011-routes及home-method-comparison.json，MEMORY.md未更新。

**正式标签核验/最终复测：** 用户提出直接安装旧1.5.8对照后，从仓库v1.5.8标签（指向5d138863，2026-10-09）只读提取当时已跟踪的build/launcher-signed.apk，SHA256与上述50a8befb…实验前归档完全相同。因此已完成的旧包5轮就是仓库标签版的实装对照，不仅是同版本号；未校验远程Release下载资产，也不能代指用户另一份更早同号包。最新5e1b3d1b…恢复后拉回hash一致，再5轮返回仍全部换PID，阻塞未解决。恢复后的额外搜索截图中设置图标可见，但结果点击后等待系统设置焦点失败、落回桌面，停止该UI脚本并保留原截图，不能记本轮完整搜索/设置回归PASS。原53项暂存统计对照一致；仅补证据/文档，未构建或修改生产代码。

**用户反馈/优先级纠正：** Android9从其他应用返回桌面出现加载动画。暂停后续冷启动热点优化，将外部应用返回同进程、无冷加载作为当前阻塞验收项；此前虽记录外部返回失败，仍继续推进性能批次，不能据此认定完整功能回归完成。

**当前实测：** vivo X21A/API28，以桌面真实点击系统设置图标→HOME，不使用force-stop。正式5e1b3d1b…包5次均换PID；保留数据换回本轮优化前4944e939…旧包，同一路径5次也均换PID。恢复最新5e1b3d1b…包后，离开桌面约1秒进程已消失，包stopped从false变true，返回才冷启动。两包Manifest仅assets configChanges标志不同，当前证据不能归因最近两项图标性能改动，也不能解释用户此前正常状态何时变化。

**实时日志：** 开始时persist.sys.log.ctrl=no，注入探针不进入logcat，下午旧日志不用于判断本次退出。用户明确授权临时开启并恢复日志；ADB属性写入和直接启动受保护界面被系统拒绝，随后经手机自带Log信息采集界面开启，探针在19:51:51可见。19:52:07和追加5次19:55–19:56均记录am_kill reason=stop by com.vivo.abe，当前退出为系统ABE强制停止；未通过修改Loading、原HOME路由或保活掩盖。系统省电模式OFF、默认HOME仍为当前Launcher。自启动页锤子桌面开关关闭，仅观察，不等同已确认杀进程触发原因；临时对照另行请求授权，尚未调整后台/电池策略。

**范围/证据：** 本次未改生产源码、未重新构建、未动原53项暂存。build/android9-home-regression-20261016保留旧/新APK、各5次样本、实时强停记录与界面截图。19:58已在原日志界面停止采集，计时归零、persist.sys.log.ctrl恢复no，未上传日志；最新APK已恢复安装并回到桌面。问题仍未解决，下一步是获授权后对已观察的后台设置做可恢复单变量对照，再据因果证据确定处理；必须完成5次真实外部返回和图标/搜索/设置回归才解除阻塞。MEMORY.md未更新。

<a id="2026-10-16-vivo_static_managed_source_defer"></a>

#### VIVO_STATIC_MANAGED_SOURCE_DEFER

**根因：** 两次vivo X21A/Android9采样中，GL nativeCompress驻留约1270/1204ms，经e.s.a(ItemInfo,Z)→Aa.a生成旧PNG/三套缓存/投影。原prepareUncachedStaticSource仅允许DEFAULT，缺少旧字节的IMPROVED等受管静态图标即使正式来源可用，也先在GL内编码再正式合成。未得到真机纹理/Shader重复创建证据，不照搬模拟器结论改引擎。

**最小改动/文件：** launcher/tools/java/com/smartisanos/launcher/theme/IconRasterDiagnostics.java删除该方法一行DEFAULT限制、更新注释；tools/tests/deferred_icon_source/run_tests.py补五类来源/已有缓存/缺图/非静态/设置/512限额并支持修前负例。复用原正式来源/最终合成器、原PENDING_SOURCE_WRITES、页面就绪释放和有界IO，不新建缓存/线程池、不扩大DB阶段DEFAULT延后门、不改MD5/SQL/三套格式/原阴影/SMEngine。同步性能、回归、问题、简化报告及专项计划。

**诊断安全与对照：** 系统拒绝非debuggable正式包外部采样后，临时构建仅由明确Intent extra触发自采样、PAGE_READY停止，未开启debuggable或更改设备策略。采样后LauncherStartupDiagnostics恢复任务前原字节，正式classes2.dex无临时profile标记。当前、clean_launcher/clean_launcher_raw及maintained参考均检查；原APK归档缺失边界沿用此前记录。采样trace有开销，未计入性能组。第一次冷启动基线因ADB日志daemon重连没有时间线而判采集失败，保留INVALID记录并增加logcat握手后重采，未以慢为由剔除样本。

**验证/产物：** 标准build.bat、v1/v2/v3签名、zipalign-P16通过；正式v1.5.8/33 SHA256 5e1b3d1b8aff120f5e3a9ae2e6413e7501ceb3ec915d0a99e979f3e50108bbd5，真机与API36保留数据安装并拉回hash一致。新负例修前在IMPROVED失败，修后补写来源门/批次/拒绝重提/替换身份通过；Android Bitmap resolver481、搜索真实PNG/Looper11、图标合同、阴影58/Smali主题24、图标库恢复重试6项通过。搜索探针首次因安装后Launcher未运行、pidof为空未执行，启动后重跑通过，不当生产故障。

**五样本：** 同机同布局/主题/选源、无并行构建/录屏/隔离测试，基线4979fc9b…页面就绪6024/6327/6238/6377/6315ms，候选4541/4616/4553/4591/4525ms，中位6315→4553ms；scene task到bind5377→3646ms，DB257→266ms、bind到ready342→341ms。保留OS/ART缓存、A后B未随机化和补写带来缓存变化的限制，不宣称首装/物理呈现/总CPU功耗收益。末轮29项补写29 DONE、0失败/缺失。两页截图最大通道差2/255、平均绝对差约0.016–0.017，未见视觉几何变化，不记完全像素相同。

**功能/剩余：** 真机五轮Dock上滑、搜索settings、结果启动系统设置、HOME、桌面设置、图标包名查询及HOME完成；外部返回仍被com.vivo.abe杀后台，不记热恢复PASS。额外冷启动在就绪观测时补写DONE=0即上滑搜索成功、结果图标可见、同PID，不把1.75s含ADB/手势墙钟当显示延迟。API36/4KiB同包五次5025/5256/5028/5272/4885ms，12宫格/黑主题/SwiftShader，仅作兼容回归；启动前SystemUI无响应通过实际XML“等待”恢复，未记Launcher ANR，搜索/系统设置/桌面设置往返通过。临时权限/选源/主题/布局/导航未改。

**下一项与完成门：** 对修后约4.5s重新采样，重点MainView.oh纹理预载/解码和颜色分类的具体重复或无效工作；取得调用证据再最小修复，同机5样本和来源/视觉/搜索/设置回归。后台帧率、首交互帧、长稳、三星Share及完整恢复/ROM矩阵未关闭；之后进入文件夹首开。证据build/startup-gpu-vivo-20261016；MEMORY.md未更新。

<a id="2026-10-16-startup_prepared_circle_source_reuse"></a>

#### STARTUP_PREPARED_CIRCLE_SOURCE_REUSE

**根因/修改：** DEFAULT圆框来源Bitmap已经准备好，IconRasterDiagnostics.composeTexture仍经resolveStaticSource加载Drawable后置空弃用。复用现有resolver增一个内部参数，只对有效DEFAULT圆框输入免第二次加载；来源准备、缺图/回收、非圆框、受管源和桌面设置保留原路径。StartupPageSceneDiagnostics只在既有前两普通页聚合来源/栅格/原阴影/投影的嵌套耗时和次数；d.1新增原完成事件入队标记，不改原事件顺序/Loading/SMEngine/阴影/几何。原实现对照clean_launcher及clean_launcher_raw；原APK文件本机缺失，未能重新校验归档字节身份，未改参考目录。

**文件：** launcher/tools/java/com/smartisanos/launcher/theme/IconRasterDiagnostics.java；launcher/tools/java/com/smartisanos/launcher/diagnostics/StartupPageSceneDiagnostics.java；launcher/smali/com/smartisanos/launcher/d.1.smali；tools/tests/prepared_icon_source/run_device_tests.py，以及四份审计报告和专项计划/本日志。无新Manager/缓存/线程池。

**验证：** build.bat、v1/v2/v3签名、zipalign-P16、版本v1.5.8/33通过，最终SHA256 4979fc9bd143a424b32fdbbffdad9df7717e9d58ff3cc38c6253cd6e9294a852。Android resolver隔离481项、图标合同静态审计、原阴影58项/Smali主题24项、补写并发/拒绝重提、搜索真实Android11项、图标库恢复重试6项通过。API36/4KiB只读副本与vivo/Android9均完成同诊断基线及候选5次进程冷启动；API36前两页21图标Drawable加载每轮42→21，局部加载中位283→142ms，桌面区域像素一致。API36整体PAGE_READY基线续组5378/候选5881ms，未证明整体提速/不退化；vivo未命中分支复用0、同诊断基线6392/最终候选6283ms不当收益。完整原始数据、开机负载组及失败样本均在build/startup-owner-20261016。

**真机回归：** 正常安装页“继续安装”后pm Success，拉回APK hash一致；首次ADB -200和安装返回前错误启动的采样明确判无效并留证。最终包5轮真实Dock上滑、搜索settings、结果启动系统设置、HOME、桌面设置、应用图标包名查询和HOME完成；图标可见、与此前截图模板一致。外部返回每轮仍被com.vivo.abe杀进程，不记热恢复PASS；诊断基线在完成5次冷样本后的系统设置am start -W曾25s超时，保留，不伪装通过。Usage Access仍default，其余用户配置未改。

**剩余/下一项：** 入队标记证明bind后0–2ms已投递原完成事件；API36额外1ms ART采样的后段约1.92s在RenderManager.r/SceneNode.render，glGenTextures约1.27s及Shader创建/链接为重点，采样开销/软件GPU不能外推实体机。下一批在真实GPU确认重复创建/无效资源后才改，再同机同数据5次及像素/来源/搜索/设置回归，之后文件夹首开；不提前结束Loading或关闭阴影。冷启动整体仍未解决，MEMORY.md未更新。

<a id="2026-10-16-android16_startup_baseline"></a>

#### ANDROID16_STARTUP_BASELINE

按用户补测要求，以Pixel_6_Pro只读临时副本确认Android16/API36、4KiB，保留数据安装并拉回校验2b8d3fad…正式包。12宫格黑主题、SwiftShader，连续日志5次进程冷启动PAGE_READY中位5221ms（5033–5433），DB256ms、scene task到bind2413ms、bind到page ready1950ms；另5次系统设置返回同PID，最终桌面截图可见，正式捕获流无FATAL EXCEPTION。前置SystemUI无响应及脚本未识别smt_launcher的两轮失败保留，不作速度筛选或Launcher崩溃结论。未改生产代码/重新构建/用户策略，测试后停止临时副本；证据build/startup-api36-20261016，细项和缓存/软件GPU限制见性能报告。下一项A19细分图标来源/阴影与绑定后完成区段，证据确认后最小修复，同设备五样本及图标/搜索/设置回归完成才关闭该批。MEMORY.md未更新。

#### VIVO_STARTUP_BASELINE_AND_NEXT_OWNER

用户要求继续方案，并明确每批结束要给出下一项及完成条件。本批复用现有LauncherStartupDiagnostics/StartupPageSceneDiagnostics，不改生产代码、不装诊断包，保持2b8d3fad…正式包和vivo X21A原20宫格/普通网格主题/关闭动态设置。最初轮询5次日志只剩后段，保留原始数据但不作为完整时间线；随后启动前持续抓日志的5次完整样本PAGE_READY中位5509ms、FIRST_FRAME回调中位362ms，DB区段177ms、GL场景构建4747ms，前两页来源解析1992ms/阴影993ms。前两页统计不是全部页面；callback不等于完整桌面/SF/物理呈现，详见性能报告。

两次ADB设置返回出现PID变化，events确认stop by com.vivo.abe。另从桌面真实点击系统设置5轮也全部由系统结束旧进程，不能把约7秒焦点返回当作热恢复；桌面设置ThemeChooserActivity内部往返5/5保持PID20828。未更改用户电池/后台策略，未添加保活/固定延时/重复HOME或恢复旧实验。证据build/startup-vivo-20261016/captured、warm-touch、warm-in-app、analysis.json及系统kill events。原53项暂存内容保留，MEMORY未更新；本轮无生产修改无需重建。

下一项明确为A19：从e.s.a→IconRasterDiagnostics及原阴影Owner细分静态来源/资源读取/解码和重复判断；得到可重复的具体耗时/次数或负例后才做最小修复。完成门是同真机同数据5样本、图标四层合同及来源/搜索/设置回归通过；之后处理文件夹首开长帧。A18 vivo后台策略是独立兼容边界，不与GL优化混作同一个根因。

#### ICON_METADATA_READS_WITHOUT_PNG_WORK

继续全项目方案的实际重复计算项A11；当前IconManager.getLableForPackage及Host.displayNameForDesktopItem/isOriginalIconForced/hasManualIconOverride不消费iconData，却会调用getRedirectIconInfo并在CUSTOM时完整解码/PNG压缩。复用已有getRedirectIconMetadata，四行替换、无新增生产接口/缓存/线程。原版clean没有当前Java偏好存储实现；maintained使用自身表模型，仅参考其名称与图片消费分离，未移植其核心。桌面来源解析、图片读取、规范化/损坏回退、备份、圆框及几何均不改。

修前真实Android负例在名称读取发现图片文件访问；修后42项通过，覆盖五种模式、身份、名称回退、图片消费者的尺寸/像素及损坏图回退。探针初次未捕获断言，Android Runtime结束测试进程并把断言写入crash buffer；已在夹具捕获并输出预期负例，不是Launcher进程异常。vivo X21A相同512×512随机PNG、两种名称各12次、交替5轮，独立采样wall中位2314.076→0.773ms，图片文件访问24→0。详细数值、CPU原值和不能外推为整体启动/耗电收益的边界见PERFORMANCE_BASELINE_AND_OPTIMIZATION。

29组共享主机回归、图标合同静态审计、build.bat、签名、zipalign通过。v1.5.8/33最终SHA256 `2b8d3fad0f0cf36a1a45ed2b77c1c0ccdeba67d812e0e5a8cdd4aa354b042b99`，vivo保留数据安装成功，拉取base.apk字节身份一致；与上一批ca263178…载荷仅classes2.dex改变。截图确认桌面名称、应用图标列表、图标库weixin八项和返回；未应用任何新图标。原53项index逐条比对一致；未提交/推送，MEMORY.md未更新。证据build/icon-metadata-20261016。

另以-read-only/-no-snapshot启动既有API37临时副本，实际PAGE_SIZE=16384、x86_64、pageSizeCompat=4；同一正式包原GL桌面和12→20重载可见，单次PAGE_READY14904ms不能作启动提速结论。按用户“用真机测试”已停止该副本、丢弃本轮写入。未关闭系统兼容模式、未改native库，A04仍未原生合规验收。后续回归以vivo真机为主，三星/严格16KiB/全主题/真实恢复等原边界保留。

随后vivo正式包连续5轮Dock上滑300/500/800/650/900ms→settings查询→设置结果启动系统设置→HOME→桌面设置/应用图标→com.android.settings查询→HOME均完成，PID12016保持；截图确认名称与原图/改进版图标可见，未应用新图标。uiautomator旧文件误读/导出失败属于测试工具问题，失败轮次未计PASS；最终采用实际焦点/页面截图/结果Activity确认，不改生产行为迎合工具。完整记录及限制见FULL_FUNCTION_REGRESSION_REPORT本批节。

#### ICON_LIBRARY_CANCELLED_QUERY_RESUME_AND_RETRY_VISIBILITY

继续前批图标审计，先核对当前页面Owner、原版/clean/maintained无对应的新图标库页面，以及旧Owner负例。`IconLibrarySearchPage.scheduleFilter()`在120ms防抖或后台查询期间可能被`pause()`取消；旧`resume()`仅`bindVisible()`，使页面继续显示旧结果和当前新输入。目录读取失败时，`showDirectoryError()`设置重试文字，但`loading.message`此前为GONE，用户看不到重试提示。只在现有页面类增加一个待发布查询标志：排队时置位、发布结果或退出分类时清除；恢复时仅重发被取消的查询，已完成结果仍只重绑。失败提示明确显示，不改搜索索引、预览队列、图标资源或UI样式。

新`tools/tests/icon_library/run_page_state_tests.py`提取生产恢复/失败处理方法执行；修前“取消的查询应在恢复后重发”负例失败，修后6项通过。图标库源数据10项、预览队列61项通过；图标源审计5199 PNG/4720应用/0错误，保留既有`com.miui. delock.theme`无效名称警告。`build.bat`、签名、v1.5.8/33通过；最终SHA256 `ca2631786eacbb18cdd97d86f1cd686de25ff0cd77be57faa4e50852962c81b6`，相对前批f9e…仅`classes2.dex`改变。vivo X21A/Android9保留数据安装后从设备拉取`base.apk`，SHA完全一致；该ROM安装器曾令ADB返回`-200`，安装界面显示完成，最终以拉取APK核验。真机实际进入“应用图标→主题→替换图标→搜索更多图标”，`weixin`返回8项且可见图标，未应用任何图标。HOME后系统最近任务回到了另一个既有设置任务，未形成本页待查询时暂停/恢复或故障注入的真机证明；这两项仍限于源方法负例与回归。设备未清数据、未改主题/宫格/壁纸，原53项暂存内容未触碰。MEMORY.md未更新。

#### SEARCH_ICON_CACHE_REFILL_AND_DOCK_ENTRY

延续10月15日方案；先只读重现，再按用户“继续执行”实施。原53项暂存blob保持不变，不暂存/提交/推送。代码基线APK为669d1cc2…，真机原装包另行拉取保存在build/search-icon-fix-20261016/before/phone.apk，未清数据。只读负例在build/search-icon-logic-audit-20261016，修复/回归在build/search-icon-fix-20261016。

根因及最小修复：

- A12：SearchIconBackend的有界encoded LRU可在全量hydration时淘汰排序靠前的图标；warmTop5只读LRU，requestDecoded在miss时直接返回null，既不排队也不回调。Oe旧PNG被启动优化延后时同样没有恢复分支。现在在原单worker/合并请求内补载：hydration只保留身份→模型ID元数据；miss按ID查当前模型、clone并核对包/Activity/user，不逐行扫描全模型；旧PNG缺失/解码失败才复用IconRasterDiagnostics原最终合成器，包含来源/圆框/阴影，未直出RAW、未新增图标管理器或网络抓取。Top5预热沿同一加载方法，失效批次不得吞掉新请求或回写旧缓存。
- A13：已有暂存启动优化把必要PNG补写送入可暂停/丢弃的P2预览任务；被丢弃后pending仍在，pageReady/added门导致不能重新提交。复用IconPreviewRepository有界IO池，新增一个明确返回接纳状态的进程级持久任务入口；一个批次只占一个队列槽，重复页面事件合并。满队列保留pending并清调度状态，在后续真实page/source事件重新提交；没有定时器、无限重试或新线程池。写入仍由原e.s.a负责，并保留删除/替换身份检查；空结果不再记DONE。
- A14：设置明确提示从Dock向上滑，但正常方向的起点条件startY < height - 96dp排除了Dock。X21A实际应用高2201、density3、Dock起点2100，旧门槛1913；修后仅放开应用表面内的Dock起点，上方280dp门、方向、单指、距离、1000ms完成窗及去重保留。临时诊断证明2100→1000事件startValid=true/sawMove=true/invalid=false，正式包已移除SEARCH_INPUT_PROBE。

验证分批进行：28组离线全部通过；新增Dock负例对修改前Owner确实失败，最终手势81项、搜索缓存/取消/身份和补写队列检查再次通过。真机隔离执行真实Bitmap/Looper搜索图标11项（48×262948字节PNG压力、LRU淘汰、Top5/可见补载、无逐行全模型扫描、旧PNG缺失调用最终合成边界）；该测试的模型和合成器为受控替身，不能冒充整套桌面合成像素验收。其他Android隔离组为journal/重进/撕裂写、启动清理112、SQLite身份83、安装worker39、QD99、向量23011、壁纸归档56。安装worker初次因两个过期夹具方法缺失无法编译，补齐接口后39项通过，未改生产安装逻辑。

正式包v1.5.8/33，SHA256 `f9e30adc3a79100560ffa9e2dc295749f5fa956e653ccec92e212c429d57b88a`；标准build.bat、签名、zipalign通过，vivo保留数据安装后拉取hash一致。与669d…逐载荷比较仅classes2.dex改变，Manifest/资源/native/原Smali载荷未变。生产源码涉及SearchIconBackend.java、IconRasterDiagnostics.java、IconPreviewRepository.java、VerticalGestureDirectionConfig.java。前轮备份/Smali修复继续保留。

真机X21A/Android9：正式包300/500/800/500/650ms Dock上滑5/5，五个常用图标每轮均有实际像素，PID6653稳定；1100ms拒绝，第三页Dock进入、T9键盘Back后再次Back回桌面、HOME、英文settings及743944→设置图标/结果、无匹配、结果启动系统设置、搜索历史和设置往返、三页横向翻页已测。屏幕转场未结束的早帧截图不作最终验收。Android9自带input swipe按每次事件重置downTime，不满足当前手势身份门；最终用固定downTime、按目标时间注入的shell夹具测试，没有弱化生产事件校验。首次进入时还观察到状态栏窗口占满触摸区；随后焦点恢复smt_launcher，此独立现场未通过假设补丁处理。

用户明确允许临时Usage Access测试；原GET_USAGE_STATS为default、常用应用关闭。测后精确恢复default，设置截图config-restored.png确认开关关闭；联系人/快捷桌面/动态天气仍保持关闭，未改主题、壁纸、默认桌面、导航模式、布局或备份。最终采集目标进程未见FATAL/ANR/图标加载异常；已有LauncherEvent obtain event null和memtrack平台噪声保留，不能声称全日志零错误。详见FULL_FUNCTION_REGRESSION_REPORT的本日矩阵。S25 Ultra未连接，Share包对应实际数据未获验证；全主题、真实整库SAF恢复、分身、手持光影、锁屏/长稳和跨ROM未关闭，不称全功能完整验收或启动提速。MEMORY.md未更新。

### 2026-10-15

#### FULL_PROJECT_AUDIT_AND_MINIMAL_FIXES

基线为本目录main/5d138863及53项已有暂存修改。任务前已分别保存staged/unstaged patch、工作区、5256个关键文件SHA及原APK128da7b5…；本轮不暂存/提交/推送，原有暂存blob身份保留。实际137 Java/3712 Smali，完成目录/入口盘点和重点执行链深读，不称全部Smali/native逐指令已证明安全。模块真实路径为独立home-root-module/modules/home-route，未改模块或启停框架。

第一批修复过期测试夹具：ThemeBackupCodec/portable源新签名，以及Model的SQLiteTransactionListener边界。journal144、restore worker122、Model188检查通过；不将夹具编译失败当生产恢复崩溃。

第二批复用IconBackupCodec收敛BackupValidator/RestoreIconSourceReconciler的图片验证。原校验先完整解码再判尺寸，多处不释放临时Bitmap；现先读bounds，portable越界在分配前拒绝，custom仅为验证采样，finally释放。归档仍写原始字节，不降低实际图标画质，不更改布局/阴影/圆框。旧分配负例失败，新184项和API36真实图像/归档56项通过，标准构建/签名/ZIP对齐及保留数据安装通过。

搜索索引API组合的DIRTY停滞候选虽能在公开方法负例复现，当前生产调用可达性未证，改动已完整撤回；SearchIndexRepository与任务前一致。正常状态6项通过，可选--probe-deferred-api负例保留在报告，不计已修BUG。

第三批实际输入定位搜索入口：1800→1100/300ms可进入，1800→800/250ms和1700→900/650ms被拒。FlingUp私有a方法将终点p5误用于起点区域谓词，高density终点被要求>840px；且保留500ms门，偏离当前1000ms搜索合同。对照clean原向下终点>=H/4，现于既有VerticalGestureDirectionConfig恢复镜像终点，Smali恢复1000ms并改用终点谓词。起点/单指/方向/距离/去重门保留。76项边界/接线、最终250/650/900ms进入及1100ms拒绝通过，Chrome提交后显示正确结果。反转方向/实体触摸未全面验收。

最终27组离线检查通过；Android隔离journal、SQLite pending、QD捕获99/代际9、Sensor向量23011及注册111检查通过，受控边界见专项报告，不当整库SAF或实体光影验收。API36最终包Back/HOME键/原生上滑各3次共9次聚焦桌面且PID保持；三个静态图标ROI与任务前RGB零差异。采集窗口无AndroidRuntime FATAL，不据此保证全场景零崩溃。

标准build.bat、v1/v2/v3签名、ZIP 16KiB检查通过；最终v1.5.8/33 SHA256 669D1CC29F1458C44DB47809DDAB60DA9F82548212B67F13070C9984E46BC48C。Manifest/版本/DB schema/原资源/native不改；有效载荷仅classes.dex的两处手势接线及classes2.dex。当前版本文档已对齐badging，历史示例不批量替换。

初轮五个进程冷启动PAGE_READY任务前中位2119ms、最终2426ms；进一步同现有数据交替安装/预热、各5次，A中位2780ms/B中位2536ms，最坏2879/3538ms。中位方向反转而尾部仍波动，缓存/系统负载未逐字节控制，不把差值解释为补丁因果，未证明提速或启动尾部非退化，详见性能报告。没有SF物理呈现/完整帧预算/功耗/长稳数据。x86_64库LOAD仍4KiB，ZIP对齐不证明16KiB运行；OPPO HOME合成、实体光影、完整恢复和多ROM矩阵仍未关闭。未改手机/主题/壁纸/导航/默认HOME，未清数据。MEMORY.md未更新。

五份审计报告入口见docs/INDEX.md；原始证据在build/full-project-audit-20261015。

#### MANAGED_ICON_FALLBACK_NO_DEFAULT_FRAME

用户指出Smartisan模块在改进版下不应带默认圆框。根因为模块0.6自身加白底，且桌面desktopIconSourceType将改进版缺图回退归为DEFAULT，错误沿用全局默认圆框开关。模块在独立root-module分支0.7恢复原透明PNG；主桌面复用DefaultIconCircleRenderer/现有RedirectIconDB元数据及IconSourceManager，在MaintainedLauncherSettingsHost集中按用户选择判定圆框。显式单应用original和全局DEFAULT保留默认形状设置；改进版/包/自定义/资源回退原图不被当成主动DEFAULT。只读override元数据，不为判定解码自定义PNG。IconRasterDiagnostics的source准备、纹理compose、日志和defaultShape缓存键统一此判定；有效来源仍如实为DEFAULT，不伪装IMPROVED，不改阴影/几何/SMEngine/动画。

47项实际Android圆框像素/选择规则、58阴影缓存、24主题转换及合同审计通过。标准构建、v1/v2/v3签名及Smartisan_API37_Test保留数据安装通过；全局improved现场模块日志SOURCE_FULL_BOUNDS/FULL_CANVAS，原透明图标已显示无白底。截图build/startup-circle-audit/module-icon07-page2.png。桌面APK SHA256 128DA7B5C91AE8C51983CA9A6410D1AA97661DC76D2BC49FB79F1A33FA138DC3，模块962EA990…；实体机未操作，完整图标包/自定义回退、各主题和备份恢复本次未全面新增实测。模块手势Hook未改，moto16尚未验证，QuickSwitch/Recents深度集成未实施。MEMORY.md未更新；未暂存/提交/推送。


#### STARTUP_FRAME_CPU_GAP_AUDIT

继续拆分首次加载，未动原SMEngine/动画/Loading门。现有LauncherStartupDiagnostics+vc增加最多12个启动场景帧wall/线程CPU/前帧间隔日志，page-ready后停止。恢复AVD后旧A35包空目录已达3849ms，故不能把之前9–12s当固定代码等待，也不能归功于新代码。新诊断包01164144…三轮页面3039/3174/3437ms，DB1811–2214ms，场景帧wall1210–1220/CPU837–844ms，绑定到原完成事件179–256ms、完成到主线程2–14ms；未复现旧秒级交接空档。旧Perfetto含699ms交换缓冲；21次64px颜色微基准CPU103ms，仅定位不改算法。构建、签名、保留数据安装与日志通过；原用户0目录/亮屏设置恢复，实体机未操作，完整首装/物理呈现/全主题仍未验收。只有诊断变化，不宣称新提速补丁；前轮数据库批量提交等实际修复继续保留。MEMORY.md未更新。详见ANDROID17_STARTUP_AND_ICON_AUDIT_20261014.md顶部10月15日节。

### 2026-10-14

#### STARTUP_PLACEMENT_BATCH_AND_TIMELINE

继续审计首次加载：两轮空目录基线页面16104/12218ms；细分发现初始应用放置逐项落盘1834+17ms，图标缓存/颜色1737ms，随后还有原GL页面构建及完成事件交接。复用DatabaseHandler原H/G，仅在启动批次外包事务并确认最外层提交；空批次不入事务，不跨图标线程池等待持锁。原嵌套事务可能吞异常，现有LauncherModelRepository内增加提交监听，拒绝把回滚误认为成功；失败仍走原启动保护。不改ID/排位/Schema/耐久级别。默认圆框Alpha半径计算改每行端点等价求解，40组逐像素一致。A/d/c/Eb/Page增加一次性阶段诊断，不改SMEngine或Loading关闭时机。

最终APK A35D5B5E…标准构建/签名/模拟器保留数据安装通过。API37同一空目录条件5轮页面8776/8867/9325/10374/12144ms，中位9325ms，最坏仍12144ms；放置批次41–397ms。五轮22条数据库ID/身份/排位全部与基线相同，integrity_check=ok；生产提交监听正常/嵌套回滚/外层回滚9检查通过；58阴影/缓存、24主题转换及合同审计通过。剩余数据准备4.0–6.4s、场景绑定2.6–3.4s、下一原GL完成事件1.56–2.57s仍存在，未证明物理呈现时刻或整体稳定提速比例。原用户0目录及亮屏设置恢复，截图检查正常；实体机、完整主题/图标包/恢复矩阵未新增验收。模块未改、未提交推送、MEMORY.md未更新。细节见docs/compatibility/ANDROID17_STARTUP_AND_ICON_AUDIT_20261014.md顶部后续节。


#### DEFAULT_CIRCLE_PADDING_AND_STARTUP_PRIORITY

用户要求所有默认圆形图标完整留白及减少首次加载等待。原opaque-cover会截断SIM卡/不规则图案；现在唯一DefaultIconCircleRenderer按实际Alpha半径完整fit，保留4%径向空隙及原有内边距、只缩小不放大，外部几何/阴影和managed来源不变，token v7。31项Android像素检查通过。

主动SIGQUIT发现DatabaseHandler等待8任务图标PNG/阴影批次，颜色批次又经Oe触发旧缓存往返。只将启动DEFAULT普通应用的旧缓存持久化延后到原page-ready边界，复用现有P2队列和Aa/Utils/IconDB，验证条目身份；静态首绑直接用现有来源/Composer，颜色分析复用原64px缩略方法。搜索预热/资源、图标revision迁移及首次系统壁纸PNG后移；API29+无缓存时先读系统刘海，保留校准回退。未改SMEngine、动画时长或提前隐藏Loading。902状态栏、58阴影/缓存、24主题转换、49壁纸Owner门控及图标合同检查通过，常规构建/签名/模拟器安装通过。空数据无追踪样本页面12178ms，21项缓存后台补写完成/失败0；带完整追踪样本仍32120ms，图形开销和当前页准备仍存在，不能称首次加载完全解决。交付APK SHA256 10EA06CE…，最终截图确认完整SIM/齿轮与原有图标留白；重启现有框架后boot17设置→手势HOME同PID1698，HOME_SENT/BRIDGE_HOME_SENT恢复。原模拟器用户0目录恢复；实体手机及完整备份/managed来源运行矩阵未新增验收，MEMORY.md未更新。详见docs/compatibility/ANDROID17_STARTUP_AND_ICON_AUDIT_20261014.md。


#### DESKTOP_SETTINGS_SHORTCUT_LOCALE_FIX

用户英文桌面截图中Dock设置仍为中文。Aa.k构造内置设置入口时硬编码中文，旧布局数据库又保存该默认中文标签，导致只修改新入口后旧布局仍显示中文。复用MaintainedLauncherSettingsHost.localizedDesktopSettingsLabel及现有launcher_setting_name英文/中文资源，不新增翻译体系；Aa.k调用已有方法，ItemInfo读取普通布局/指定列布局时只对精确设置组件及已知默认标签进行语言更新，保留用户自定义名称和其他应用/文件夹。新helper放在既有设置宿主中，因为原标签方法不包含组件/旧标题检查。

常规build.bat、v1/v2/v3签名、Android17保留数据安装通过；未清除布局，截图build/api37-label-final06.png确认原Dock中文已变Desktop Settings。对应模块0.6图标安全留白在独立模块工作区修复，主桌面圆形图标渲染规则未改。本次只检查Android17英文现场，其他语言及所有布局恢复路径未全面实测；原版SMEngine/返回动画不变。MEMORY.md未更新。


#### ANDROID17_STATUS_BAR_CALIBRATION_RELOAD_FIX

Android17模拟器启动加载慢审计确认：同一cutoutBottom145、gap5，实时statusBarTop63/145使原上限把effective150截成145再恢复150，触发两次STATUS_BAR_COMPAT_CHANGE冷重载。日志能对应旧PID结束与一次重载超时，不归因“动画时长太长”。现仅修改既有StatusBarHeightCompat.calculate的upper至少容纳base，保留真正配置变更的重载、手动偏移与SMEngine。新增902项生产纯计算回归，正常build.bat及签名通过，主分支原有未提交改动保留。APK DCED4A60…已保留数据安装到Android17，安装后GL首帧日志889ms、模型/页面6160ms；后续桌面设置返回PID6349保持，无同类自动重启。不同APK基线/缓存负载及切出桌面时间不一致，不将前后数字作为纯前台性能因果或屏幕呈现指标。补充受控前台冷启动GL首帧9276ms、页面9456ms，无自动重载；首帧8123.710ms，三次栈命中PNG压缩、图标栅格化及模拟器纹理交互，这部分尚未消除。实体vivo/其他ROM未此次回归，MEMORY.md未更新。详见docs/compatibility/ANDROID17_STARTUP_AND_ICON_AUDIT_20261014.md。


#### ROOT_HOME_KEY_ROUTE_AUDIT_AND_TNT_BRANCH_REMOVAL

按用户要求先审计，不新建ROOT分支、不安装或启动模拟器。ColorHomeFix反编译确认系统桌面手势入口Hook→HOME识别→Instrumentation注入KEYCODE_HOME，并有SystemUI动画及system_server配套Hook；仅授予锤子APK的su权限不足以实现。模拟器当前离线，本地Google APIs镜像也不含Oplus入口，不能冒充ColorOS验证。后续优先独立ROM模块、限定Smartisan默认HOME，不改SMEngine。详见[ROOT路线审计](../../compatibility/HOME_RETURN_COMPATIBILITY_AND_REFACTOR.md)。用户要求的横屏分支feature/tnt-tablet-launcher无独有提交，13个已暂存文件已逐文件备份校验至E:/FANG/smartisan/branch-archives/tnt-tablet-20261014-134053；原目录同HEAD detached后删除分支名，前后暂存／工作状态不变。main及设备未改动，MEMORY未更新。


#### VIVO_NORMAL_HOME_HANDOFF_LIVE_AUDIT

用户连接vivo X21A / Android9后，指定b2a4da1c复核现装4944E9…APK，无安装／主题／导航变更。三次上滑回HOME均同PID、Context及scene，Surface每次重建。后两次录像明确显示完整图标与Dock在设置窗口缩小／淡出期间已参与过渡；第一次唤醒准备后的返回有黑底阶段，不能标三次全部正常。热返回首GL完成77.630／48.150ms，系统AppTransitionReady147.682／98.546ms（均Resume起算）；这些不是实际present fence，也不单独证明系统等待条件。尚无可移植的ColorOS补丁。诊断开关已恢复，其他设备未操作，MEMORY未更新。完整证据及限制见[现场报告](../../compatibility/HOME_RETURN_COMPATIBILITY_AND_REFACTOR.md)。

**NOVA_WALLPAPER_ZOOM_AB_NO_RELIABLE_GAIN**

- 按用户授权实施Nova壁纸zoom最小实验：默认关闭，API26–29跳过，API30+仅请求自己HOME窗口zoom=1，关闭恢复0。直接反射版被API36拦截，未生效样本排除；实际Binder版由ADB夹具解析本机编号，不硬编码跨版本事务、不改hiddenapi策略。系统WindowState确认0→1→0，未写壁纸/改引擎/改Surface或加遮罩。
- 同APK4AA4982A…BEF9B6、PID9131、手势mode2，关闭→开启→回关，每组5次；有效5/3/3，4次最终留Settings排除。视频空档中位数611/537/472ms；两关闭组合并553ms、开启537ms约差16ms，SF中位数关闭539ms、开启550ms，未见方向一致的改善。GL完成和SF采样不等同物理呈现，没有把单次变快当收益。
- 候选源码/APK/trace/录像归档，生产代码恢复任务开始快照，虚拟机恢复43A8F180…6F0F2E，实验键/zoom恢复缺省；正式主包未引入该策略。详见兼容报告第19节和HOME_NOVA_ZOOM_EXPERIMENT_20261014.json。Android8–16目标保持，实体OPPO/vivo未操作；该项尚不能作为修复，MEMORY.md未更新。

**NOVA_APK_HOME_HANDOFF_AUDIT_ANDROID8_TO_16**

- 直接审计同机Nova8.0.18 APK（262535B9…E630B）的真实smali，并重新解码资源/Manifest；11个关键方法证据见build/nova-handoff-audit-20261014/code-evidence.json。不是只引用Launcher3开源实现，未采集/安装或改生产源码。
- 新追到Oplus框架检测后默认关闭wallpaper_zoom_effects的链路，以及wallpaper_scrolling_force控制的主Window内壁纸绘制/格式切换；后者默认false，不能视作录像时生效或确定防闪回原因。确认完整图标Surface/finish协议差异，仍不能覆盖合同到达前曝光。主Window/Surface角色、已有resumeWhilePausing及恢复异步消息均核对，未猜测属性修复。
- 用户明确兼容范围Android8–16；按API26–29、30–33、34–36分清能力门，保留vivo9/16基准。NovaAPK最低API27不改变本项目Android8.0支持。没有加入隐藏Binder硬编码、固定等待或全局不透明策略，完整原生手势闪回仍未修复。详细差异及借鉴限制见兼容报告第18节；MEMORY.md未更新。

**ROOTLESS_HOME_ACTION_SOURCE_RESEARCH（源码可实施性，不是设备修复验收）**

- 联网核对Lawnchair、Neo、OpenSmartisanOS具体实现：目标图标Surface合同不提供提前显示整个HOME的入口；系统侧FallbackSwipeHandler掌握HOME目标显示/alpha。没有把代码移植能力等同普通APK的系统权限。
- 找到与用户“手势走虚拟键路线”相符的新候选：替代边缘手势调用公开无障碍GLOBAL_ACTION_HOME。HyperGesture已有实现；Android12的SystemUI及默认动作执行端实际发送KEYCODE_HOME。需切三键避免原生手势竞争、用户开启无障碍，返回效果为HOME动作对应动画，不承诺原生跟手动画或自动隐藏按键栏。
- 来源固定版本、实施位置、许可及导航误触边界见兼容报告第17节。OPPO12尚未验证此路线；没有重复采样、构建/安装或改Launcher/SMEngine/Manifest。主包SHA256仍C0BEDCEEA1B8181D08810833486C39CFD9BA5448FCAF27E98A853E485F369A00。当前只有方案研究完成，原生手势闪回未解决；MEMORY.md未更新。

**HOME_GESTURE_HANDOFF_EVIDENCE_ONLY_NO_BEHAVIOR_FIX**

- 用户要求完整桌面在APP缩小时参与过渡。已有同包双导航证据足以确认路线差异，本轮新增四帧场景可见性诊断未产生行为修复；按用户纠正停止重复采集，撤回临时诊断源码，虚拟机恢复本轮前功能包，实体手机未操作。
- 同诊断包/PID4380，手势与ADB HOME键各3次有效HOME；前者GL结束72–125ms，SF有效GL层可见330–461ms，后者35–75ms/221–295ms。两组均有已到buffer被HOME窗口/Activity父层隐藏的阶段，录像的退出动画与露底方式不同；不能仅凭有buffer断言完整图标已呈现。节点可见/scale=1、场景/Context复用；错误的材质alpha乘积已作废，未用于补丁。
- 具体时间线、证据及限制见 `docs/compatibility/HOME_RETURN_COMPATIBILITY_AND_REFACTOR.md` 第16节。完整手势交接仍未解决；没有新增HOME重发、固定等待、遮罩、全速后台渲染或SMEngine修改。未更新MEMORY.md。

**WALLPAPER_BACKUP_AND_REFERENCED_ICON_SOURCE_EXPORT**

- V2458A/API36的backups目录读取3份归档：2,855,663/28,840,143/29,840,614字节，icons/sources分别61/508/518张，三档均无壁纸文件。整目录导出图标缓存纳入未引用库原图是增长原因，不能根据“带阴影”文件名推断阴影纹理进入归档。
- 新导出复用稳定布局、保存图标记录、现有自动候选及OEM别名；保持历史哈希PNG保守保护，不删手机缓存。自定义图标原字节与图标包选择原链路不变，图标包APK仍需恢复设备安装。生产ZIP代码隔离重打包28.84MB样本为2,882,631字节；实际新备份可增加当前候选及壁纸，不强制承诺固定大小。
- ThemeBackupCodec可选wallpaper字段记录default/selected及底层主题，自选只保存一份原图，恢复重建私有URI；系统/高斯/默认/缩略图缓存不打包。现有恢复回滚归档也保存壁纸；旧档无字段保留当前来源。文件/图片验证在数据库写入前，恢复过程中不写旧活动主题的系统壁纸，等原协调器初始化目标主题再同步。
- Android16隔离43项、PreferenceBackupCodec25项、主题同步47项通过；包含自定义图片字节、改进版原图逐文件恢复、全局/单应用图标包选择、旧档校验与回滚。布局/快捷方式和实际源别名解析在隔离测试有受控边界，不把此称为完整真机恢复验收。构建签名、16KiB对齐与虚拟机安装HOME启动通过。
- APK SHA256 43A8F180580944B7DF447ADC166941304C737CEA3707940A030729C9206F0F2E。源码文件及命令/范围见BACKUP_WALLPAPER_AND_SOURCE_SIZE.md，原始统计/测试见build/backup-wallpaper-20261014/report.json。真机只读，未安装或恢复；未更新MEMORY.md。

### 2026-10-13

**THEME_SYSTEM_WALLPAPER_SOURCE_SYNC_AND_PICK_PUBLISH_FIRST（用户新授权，虚拟机局部验证）**

- 用户明确要求普通主题、透明/毛玻璃自选或默认及四指切换同步系统壁纸，更新此前不写系统壁纸的范围。复用现有宿主/执行器/URI和原主题回调，普通返回不重复写壁纸。透明alpha覆盖不能当默认壁纸，改读已保存底层主题资源。
- 旧选图先PNG重编码和缩略图后刷新，改先提交原图并排场景刷新，系统写入锁与选择锁分离。最终透明/Aero源提交176/167ms，刷新请求191/182ms；系统写入仍约3.7秒，录像新背景先可见，不能把刷新日志等同呈现或保证大图零卡顿。
- API36第一次同步触发 `wm_relaunch_resume_activity ... 80000000`，原版onDestroy SIG9冷启动；仅向有效HOME Activity的0x00003fff加入CONFIG_ASSETS_PATHS至0x80003fff，并同步文本Manifest。最终Black/Blue/Aero切换、选图、恢复默认保持PID；未改SMEngine和原M壁纸接收器。
- 最终APK SHA256 6C8E357488FCF9DEADDA1481C6BB563F6356521D0D3A83BFFEC7C271B69AEE44。47项断言、build.bat、签名、16KiB对齐和最终AXML通过。前一候选Black手势3/3、交付包两次有效HOME无旧蓝色壁纸，交付组第一轮Settings排除；完整图标仍晚出现；Aero三次输入只有两次到HOME，排除另一轮。OPPO/vivo最终包、实际四指、锁屏/最近任务/快捷桌面和帧率资源矩阵未验收。
- 源码：MaintainedLauncherSettingsHost.java、LauncherSettingBridge.java、文本/二进制Manifest；工具patch_launcher_assets_config.py与tools/tests/theme_wallpaper_sync。完整矩阵、前后SF采样、无效样本与参考边界见docs/compatibility/HOME_RETURN_COMPATIBILITY_AND_REFACTOR.md第15节和HOME_BACKGROUND_SYNC_20261013.json。未更新MEMORY.md，保留未验收边界。


**窗口绘制交接专项：两种候选已实施并测，无闪回目标未达成，行为改动已撤回**

- 按用户“第一条”授权，只修改现有LauncherHomeCompat／SMGLSurfaceView进行默认关闭A/B。H1把平台重绘通知移到本次EGL swap尝试后；H2把同一个super.surfaceChanged交给GL队列，以避免主线程同步等一帧后再请求重绘。原SMEngine、主题、格式、背景、动画和输入不变。150项离线回调／取消／世代与尺寸队列检查通过，候选构建、签名及虚拟机保留数据安装通过。
- H1同APK／PID10772前后各3轮，H2同APK／PID13251前后各3轮严格APP→HOME，均仍露系统壁纸。H1确实完成交换后通知，H2尺寸callback到REDRAW_REQUEST间隔由约96–127ms变为约0.5–2ms，但首桌面图层可见仍约0.35–0.47s，不能把取消主线程等待当作闪回已经修复。没有新Context／scene创建。两个未回HOME的手势和一轮带overview控件的返回单列，不冒充严格APP返回结果。
- 两行为候选及150项测试归档到build/home-draw-sync-20261013/candidate-source，正式源码只保留默认关闭的重绘请求／平台回调开始结束时序，原回调原线程原时机转发。虚拟机恢复4944E9…测试前APK、手势mode2和原属性；实体OPPO／vivo未操作。正式诊断包构建／v1-v3签名／16KiB对齐通过，F8FCA1…，未安装；DEX确认两实验tag已移除。采集工具新增测量隔离时间与手势时长参数，产品恢复没有固定等待。
- 另逐帧检查已保存Nova录像：第1次返回的4.242–4.441s只有森林背景与缩小APP，4.523s可见其余桌面图标，背景连续是该正常样本的明确差异；不能据此把Nova标为用户可见闪回或认定这是它正常的唯一原因。完整证据、实验APK和OPPO／主题／解锁／高刷新率未验边界见兼容报告第14节及HOME_RETURN_EMULATOR_20261013.json。当前未交付闪回修复，MEMORY未更新。

**最终实测：Android16虚拟机候选无改善，已撤回；有buffer但HOME祖先仍隐藏**

- 后续离线复核同机保存的Nova8.0.18／Smartisan三轮手势SF：Nova的Wallpaper可见且HOME主窗口不可见采样为330–420／280–320及380–430／190–240及310–380ms；Smartisan为270–380／260–320及390–440／220–260及330–380ms。两组HOME首可见采样分别约450–550ms与470–530ms。多数采样仍有RecentsActivity可见，不能称纯壁纸显示时长；Nova的用户视觉正常结论保留。结合OpenSmartisanOS的FallbackSwipeHandler，图标合同回复只改变后段收拢目标，不能回溯其到达前Wallpaper与HOME窗口的早段交接；因此没有为闪回强行移植新图标Surface或重绘原版图标。详见兼容报告第13节。本项没有改运行源码、安装APK或操作实体设备／虚拟机。
- 继续核对原版与当前 `LauncherActivityTheme` 的 Wallpaper 父主题和 `windowDisablePreview=true`；AOSP ActivityRecord 对 HOME 快照启动窗口限定为直接解锁使用，不能以改一个 preview flag 推断 ColorOS 原生手势会提前合成完整桌面。结合已失败的主窗口Texture实验，本轮不改主题属性或原版渲染链。平台实现仅为参考，未取得 ColorOS 12 私有源码或新设备前后实测；详见兼容报告第13节。

- 用户后续授权使用虚拟机测试，操作仅限 emulator-5554 / Pixel_6_Pro / Android16 API36，全面屏手势mode=2、默认Smartisan、Black主题。备份原安装4944E9…包，保留数据分别安装修改前B40FA5…和候选B86FC4…；各3次Settings→手势HOME，组内PID稳定且三轮确实回HOME。实体vivo没有ADB操作或安装。
- 两组3/3录屏仍露系统壁纸，APP缩小动画存在。首桌面buffer图层可见相对Resume：修改前403.702／494.665／501.581ms，候选492.410／453.382／538.629ms；没有稳定改善，不能将延后刷新当作闪回修复。FrameTimeline事件结束、GL回调、窗口commit均不是面板呈现。
- 候选第一轮347.123ms的SF祖先链：BLAST桌面buffer为1080×2400，但hidden by parent；主窗口、HOME Activity和根Task仍flag is hidden。这确认该阶段有系统合成显隐阻挡，不单独认定具体ROM策略／窗口同步根因，也不证明最早buffer全部内容正确。
- 归档候选源码、APK与177项测试runner到 `build/home-resume-handoff-20261013/retired-candidate/`，只撤回本次候选的4个运行文件改动；三个before副本逐字节一致，vc恢复原warm hook，其他既有dirty状态保留。回退标准构建／v1-v3签名／16KiB对齐通过，APK SHA256 `ABA68CE1D1CC4064019C46593FB8F5EAD2FA0B50B242F34713C6D5C29CAD7F96`；与B40FA5…ZIP所有条目内容相同，包括两个DEX。
- 虚拟机恢复测试前4944E9…APK，已核对hash、默认HOME和mode=2；诊断设置已由采集脚本恢复。没有覆盖正常vivo链路，也没有正式发布新修复。新增机器证据 `docs/compatibility/HOME_RETURN_EMULATOR_20261013.json`，详见专项文档第10节；MEMORY未更新。

**实施阶段记录：普通恢复刷新任务绘制交接候选（已由上方实测撤回）**

- 可确认的应用侧问题：旧 `vc.onDrawFrame` 内直接向 MAIN 投递恢复刷新任务；GL 交换、窗口提交及 Surface 重绘完成不属于其释放条件。10/12 日志中刷新早于 `finish draw` 标记，但该差值不等于任务造成的延迟，也不是全部壁纸闪现的根因证明。
- 实现：复用 `LauncherHomeCompat` 管理现有刷新任务的释放，原刷新内容仍在 `MaintainedLauncherSettingsHost`。API29+ 有效硬件窗口等待 GL 当前交换尝试结束、根窗口帧提交和已登记的 Surface redraw 回调；原框架 callback 原时机转发。API28 及以下／软件窗口／失效 Observer 保留原 GL 更新边界。Pause／Stop／Destroy／冷准备／恢复替换取消旧任务。没有延迟等待、轮询、额外渲染线程或持续绘制。
- 修改源码：`LauncherHomeCompat.java`、`MaintainedLauncherSettingsHost.java`、`SMGLSurfaceView.smali`、`vc.smali`；新增 `tools/tests/home_return/run_tests.py`。原 J／Eb／SMEngine、动画时钟、主题与窗口 flags 未修改。冷启动／冷重载首帧协议继续走原入口。
- 验证：真实 helper 编译后的 177 项确定性回调／取消断言通过；标准 build.bat、v1/v2/v3 签名及16KiB对齐通过。与本轮前 B40FA5… 包比较，仅 classes.dex、classes2.dex 与签名 ZIP 项改变，Manifest／resources／res／assets／native 共1,954项字节相同；SMEngine 源码没有新增 diff。暂存区仍为空，其他既有改动保留。
- 候选 APK：`build/launcher-signed.apk`，SHA256 `B86FC41F3A28624C0750BEF9604A65D127F5B993CF06741CB4057BEC0AD8527A`。修改前 APK、源码、定向 diff、测试和构建记录位于 `build/home-resume-handoff-20261013/`。
- 限制：未安装／未追加 ADB 采样，不能提供修改后设备帧时间线。窗口 frame commit／GL swap 尝试／Surface redraw 都不代表面板呈现；本补丁减少任务过早介入的风险，不直接改变 ColorOS 在 HOME 隐藏时的前段 Wallpaper 选择。OPPO 手势消除闪回、vivo9/16非退化、解锁／快捷桌面／主题与耗电均未验收。完整渲染宿主重构仍是待证据支持的后续方案。详见专项文档第9节；MEMORY 未更新。

**HOME 壁纸闪现：历史设备矩阵与重构边界收口，尚未修复 OPPO 手势**

- 专项文档：[HOME_RETURN_COMPATIBILITY_AND_REFACTOR.md](../../compatibility/HOME_RETURN_COMPATIBILITY_AND_REFACTOR.md)。覆盖正常 vivo9/16、异常 OPPO PDCM00/ColorOS12 手势、同机同包实际三键正常、Nova 正常参照、模拟器及未验收 ROM／场景；ADB HOME key 不冒充虚拟键点按，安装后首轮进程更替不混入热恢复。
- 10/12 OPPO 后续主分支诊断确认有效手势协议，位置回复实验三轮发送但无系统接收确认，仍露壁纸。没有实现完整 Nova 图标 Surface／finish 回调，不能将这个子集实验标为“Nova 方案无效”。
- EGLWindowSurfaceFactory 转接 TextureView 的同 APK（B8CBE0…）开关组各 3 次、组内 PID 稳定。画面与设置图标点按可运行，排除状态栏／时钟后的静态截图 ROI 通道均值／p99 误差均为 0；主核心 DEX、资源、Manifest、native 库 hash 相同。三轮仍见 Wallpaper，没有验收收益。该原型保留 SurfaceView 壳，仍可能参与窗口／Surface 同步；这点是设计局限，不是已证明的唯一根因，也不代表完整 TextureView 宿主无效。
- 原型源码／APK／hash 已归档到 `build/home-coloros-audit-20261012/retired-texture-factory/`，解除 LauncherHomeCompat 对 HomeTextureHost 的接入并移除本任务新增的原型类。保留默认关闭的日志 tag 诊断入口与 HOME 协议存在性标记，未保留位置回复、截图或新渲染线程。10/11 热恢复改动和其他工作树修改保留。
- 对照 OpenSmartisanOS Launcher3（9222aa7…）、本地 maintained 与 SmartisanWeather-Revived（f6b21ec…）。修正过宽表述：maintained 主桌面仍是 SMGLSurfaceView；天气是 Compose 重写，不能作为 HOME 呈现修复证据。具体原接口合同、线程／窗口同步、完整宿主与协议阶段见专项文档 R0–R4；这些是设计，不标实现／验收通过。
- 本地标准 build.bat 通过，v1/v2/v3 签名与16KiB对齐验证通过，文档本地链接／JSON及git diff --check通过。解除实验后的APK SHA256为 `B40FA56821D3F797D13C869EC9455878B24DE19934727748F3721EA65D802951`；与10/11主包对比，原核心classes.dex、资源、Manifest和native库均逐项相同，classes2.dex不再包含HomeTextureHost。未安装此包，不能称作真机修复。
- 10/13 用户明确不再要求连接手机，本轮不再做 ADB 操作、安装、主题／导航／默认桌面切换。不能将本地构建当作修复后真机验收。OPPO 壁纸问题仍未完成；项目与全局 MEMORY.md 均未更新。

### 2026-10-11

**APP → HOME 统一恢复策略：保留热场景，窗口级闪回仍为部分解决**

- **施工范围**：main 位于 `E:\FANG\smartisan\home-main`。原工作目录的平板适配和暂存内容未改动。未提交、暂存、推送或修改默认 HOME。原未提交 HOME 原型已完整保存在 `build/home-unified-20261011/before/source/` 和 `before/worktree.patch`，两台 vivo 安装前 APK 也已拉取归档；本节替代当天早先的截图接力说明。
- **【已废弃】截图／遮盖原型**：撤掉 HomeFrame、离场 PixelCopy、Decor 整屏 BitmapDrawable、HOME 隐藏 Surface 到 Focus、连续前三帧 glReadPixels 与 PNG 写盘。旧原型没有消除系统缩窗阶段壁纸，且引入截图、延后 Surface 显示和后台 PNG 任务，不作为统一恢复策略保留。没有删除快捷桌面自身需要的截图链。

**根因与证据边界**

| 状态 | 审计结论 |
|---|---|
| CONFIRMED | 当前 Launcher 和原版 APK 的 LauncherActivityTheme 继承 Wallpaper.NoTitleBar，禁用 starting preview；窗口允许系统壁纸露底。当前／clean_launcher 均保留 EGL Context、透明格式、原版 z-order。maintained 的普通 View／窗口背景不能替换原版 GL 场景。 |
| CONFIRMED | 正常 vivo Android 9/16 普通 APP 返回也会销毁／新建 Surface；最终稳定样本 Context generation 始终为 1、Eb scene identity 不变。因此 Surface 重建并不是异常 ROM 的充分根因。vivo 无闪回体验不能归结为它从不重建 Surface。 |
| CONFIRMED | J.onResume 复用原 Eb，Eb.onResume 重置动画时钟、置恢复位并 requestRender；vc.onSurfaceChanged 仅尺寸改变时 create，onSurfaceCreated 才重新接入资源上下文。没有在本补丁中新增冷启动、解锁准备或纹理重建入口。J 的当前普通生命周期并不直接调用 SMGLSurfaceView.onPause/onResume；其包装方法存在不等于已经接入 Activity。J 设置的是 RENDERMODE_WHEN_DIRTY，原版 SMEngine 保持原路径。 |
| CONFIRMED | 旧 scheduleLauncherPostFirstFrameTasks 每次热 Resume 都重置 cold gate，导致搜索 warmup、raster revision、图标包 preload、恢复／Loading 完成等整组初始化重新排队。本次只删除这个无条件重开，保留壁纸 pending、角标 dirty 和天气 TTL 恢复检查。它是确认的重复工作，不宣称它独占全部闪回时间。 |
| CONFIRMED | GL 绘制和交换之后仍有合成可见性空档。最终 vivo16 首帧 GL 完成约 21–24ms，SF SurfaceFrame 事件结束约 26–29ms，但带有效 buffer 的桌面 layer 首次被 SF 标为可见约 74–89ms；模拟器相应可见时间更晚。onDrawFrame 返回、queueEvent 和 buffer 可读均不能冒充 FIRST_PRESENT。 |
| SUSPECTED / NOT TESTED | 一加、小米、OPPO 的具体现场 ROM／导航窗口、Recents 和 GPU 首帧是否具有相同原因，尚无同一操作的现场呈现证据。模拟器时序不能证明全部厂商原因，也不证明完全解决所有 ROM。 |

**最终最小补丁**

1. 继续由 J/Eb/vc 和系统 Surface 生命周期恢复桌面：保留同一场景和有效上下文，不主动隐藏／重新布局／切换格式，不修改 SMEngine、动画、shader、图标、主题资源、Manifest、版本或权限。真正 Surface／Context 失效仍交给原版与框架原入口处理，没有第二个重建 Owner。
2. 在既有 LauncherHomeCompat 内增加关闭为默认的时序诊断。记录 Create/Pause/Stop/Resume、Focus、窗口可见性、Surface Attach/Detach/Create/Destroy/Size、EGL Context 创建、场景 create、前四次 renderer 完成及下一 GL loop；记录 elapsedRealtimeNanos、monotonic 时钟、PID、Resume/Surface/Context 世代及对象身份。GL 标记明确 `presented=unknown`，没有每帧截图、无限日志、固定恢复延时或轮询。
3. cold／受控 reload 使用原首帧任务门；热返回只在下一 GL 更新后消费既有 pending/dirty/TTL 三项。必要的壁纸变化、角标和天气刷新保持，不删除功能调度。
4. 两个独立诊断实验均默认关闭且须同时启用诊断：API34+ attachment lifecycle 与普通不透明主题关闭 SHOW_WALLPAPER。API34 API 隔离在内部类，Android9 已实际运行。attachment 实验在 Stop 调用既有 GLSurfaceView.pause，Resume 对应恢复，以免有效 Surface 驱动后台更新。透明覆盖／aero／trans 不允许套用不透明窗口实验。诊断关闭后恢复捕获的原 flag 与默认 lifecycle。

**前后时间线（ms，统一以 Activity Resume 开始为 0）**

| 样本 | Surface 创建 | 首次 GL 绘制／完成 | 首个 SF SurfaceFrame 事件结束 | 首次有效 buffer layer 可见 |
|---|---:|---:|---:|---:|
| vivo16 安装前，保留的有效 trace 1轮 | 旧包无诊断 | 开始 11.066，结束 18.654 | 21.985 | 71.969 |
| vivo16 最终包，3轮手势 | 10.0–13.8 | 完成 20.9–24.2 | 25.5–28.6 | 73.8–88.6 |
| vivo9 最终包，同 PID 3轮 HOME | 34.0–42.5 | 完成 46.1–51.1 | API28 无 FrameTimeline；该次首呈现未完整对齐 | 仅取得 atrace／窗口／video，不能填造 SF 首呈现 |
| 模拟器安装前，保留的有效 trace 1轮 | 旧包无诊断 | 开始 727.2、结束 1687.8 | 1761.0 | 1775.0 |
| 模拟器最终包，3轮 HOME key | 58.6–105.7 | 完成 90.7–164.4 | 139.9–228.0 | 322.1–435.9 |

SF 事件结束与 layer 可见分别报告，前者可能发生在隐藏层，不能直接叫首次用户可见画面。video 是 screenrecord 的合成采样，不是面板高帧率摄像。安装前／后包、采样数量和模拟器负载不同，上表只提供真实时序，不据此计算性能改善百分比。最早锁屏挡住 HOME、尺寸不匹配的手势以及未回到 Launcher 的操作不纳入有效配对。

**独立实验结果**

- attachment：vivo16 和模拟器各3次返回依然每次重建 Surface，Context 和 scene 未重建，没有降低 Surface 重建次数。因此已退回原默认策略，不正式开启该选项。vivo16 同 PID 样本 GL mtrack 为 42660 KiB，PSS 随进程缓存波动（实验样本334654 KiB），不能归因于实验；可对齐的两个 GL_PAUSE→GL_RESUME 后台区间均无 onDrawFrame。没有完成长期 GPU/内存压力／后台电池对照，不能标耗电通过。
- SHOW_WALLPAPER：模拟器普通 Classic Black 确认窗口 flags 由81910300变81810300；手势缩窗仍露系统壁纸，3轮中一轮未真正回到 Launcher，另两轮 SF layer 可见约501／680ms，没有稳定收益。flag 已恢复，正式行为保持原版。实体机当前壁纸主题、透明／毛玻璃完整 A/B 尚未验收，不能推广为主题通用修复。

**验证与风险**

- 标准 build.bat、v1/v2/v3 签名、16KiB zipalign、badging 和 git diff --check 通过；v1.5.8/code33。最终 APK SHA256 `4944E939ADBE8E75C78C0A3CDDA06DDF325F852722BAFF01309ABDDDFEEA53EA`。vivo9/16 保留数据安装后拉取 APK 的 SHA256 与本地产物一致；未清数据、改系统壁纸或默认 HOME。
- 候选包：vivo9 HOME 3轮、Back 2轮、Recents→HOME 2轮；vivo16 HOME 3轮、手势3轮、Recents→HOME 2轮，前台和 PID 核对、录像／图像抽样及日志检查完成。最终包：vivo16手势3/3、vivo9稳定HOME3/3、模拟器HOME key3/3。最终稳定组没有 ACTIVITY_CREATE、EGL_CONTEXT_CREATE、SCENE_CREATE、COLD_DEFERRED_TASKS 或 UNLOCK_SESSION_ARMED／UNLOCK_PREPARE_BEGIN／UNLOCK_COMMIT_PLAY，未发现新增 Java/native fatal。只是这些具体路径的结果，不是全部动画／ROM PASS。
- **保留异常**：vivo9 最终覆盖安装后第一组出现 LauncherAlias 任务结束、新 Launcher Activity 创建、PID29882→30180；新进程执行 cold tasks。J.b(Activity) 原有同线程再次创建时 kill/relaunch 分支仍存在，本次没有修改；events证明任务／进程变化，但尚无完整退出调用栈，不能把它称作已解决。后续同PID30180的3轮热返回无cold。该首轮不能纳入热恢复或“全非退化”通过。
- 模拟器三键导航3次、原手势3次、Recents与两次sleep/wake恢复已测；最终手势另有2次仍停在Settings，不能计为成功，也不能据此归因Launcher。普通主题Blue切换后两次HOME已测，恢复Classic Black后已用UI层级核对Current标记。真实锁屏解锁／凭据、快捷桌面、透明／毛玻璃切换、实际异常ROM双导航、长稳／低内存和电池完整矩阵仍待对应设备验收。
- SMEngine、assets/res、resources.arsc、二进制Manifest和项目MEMORY在施工前后逐文件hash无变化。全局及项目 MEMORY.md 未更新。实验设置由采集器按原值（含不存在状态）恢复；模拟器导航恢复gestural。原平板目录保持原暂存状态。

**文件与复现入口**

修改：`LauncherHomeCompat.java`、`MaintainedLauncherSettingsHost.java`、`Launcher.smali`、`view/SMGLSurfaceView.smali`、`view/vc.smali` 和本日志；新增 `tools/capture_home_return.py`。诊断属于移植兼容边界，现有 startup one-shot 标记无法区分每次恢复与上下文世代，故复用现有 HOME helper扩展，没有新增 Manager/Service。产物位于 `build/launcher-signed.apk`。

```powershell
python tools/capture_home_return.py --serial <serial> --label rom-home --rounds 3 --diagnostics --method key
python tools/capture_home_return.py --serial <serial> --label rom-gesture --rounds 3 --diagnostics --method gesture
# 两项实验分开运行；未改善时保持关闭，不能拿keyevent替代真实三键或手势导航。
python tools/capture_home_return.py --serial <serial> --label rom-attachment --diagnostics --attachment
python tools/capture_home_return.py --serial <serial> --label rom-wallpaper --diagnostics --opaque-wallpaper-off
```

诊断输出在 `build/home-unified-20261011/<label>/`：同次 video、timing.log、Window/SurfaceFlinger状态、API29+ Perfetto／API28 atrace、samples.json。离线时序保存为 timeline.json，汇总为summary.json；工具的采样准备等待不参与Launcher恢复逻辑。没有SF层／帧数据时必须保留unknown。

### 2026-10-09

**主题状态、默认毛玻璃壁纸与文字同步：最终保留方案（用户确认当前正常）**

- **最终状态**：V2458A／Android16保留数据安装当前包后，用户最终反馈“现在正常了”。本次按用户要求停止代码和真机操作，只收口文档。APK为`build/launcher-signed.apk`，SHA256：`50A8BEFB8E8D2BD0843905776A364721B00A245BB2F7A88F24B2CBD03B88AB11`。此确认覆盖用户当前观察到的恢复效果，不延伸成全部设备、主题和壁纸矩阵通过。
- **状态栏根因证据**：四指后确实存在黑桌面文字／白状态栏。Launcher最终app_text_color为黑色，WindowManager已有LIGHT_STATUS_BARS，SystemUI也记录isLight=true，但失败现场的实际mDarkIntensity与mNextDarkIntensity仍为0.0（白色）。因此仅写入相同appearance或仅检查请求标记，不能证明SystemUI已按目标颜色重新绘制。最终刷新后取得mDarkIntensity=1.0的记录；过程中仍有白色截图，所以以随后用户“当前正常”的确认收口，不把字段变化单独当作视觉PASS。
- **状态栏最终修复**：颜色仍由桌面最终app_text_color唯一决定，保留原版e/s.d→e/g.run调度。Launcher窗口恢复在导航缓存早退之前同步legacy标记与Insets；最终颜色提交明确FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS、清FLAG_TRANSLUCENT_STATUS并保持透明底色。原颜色任务随后通过postOnAnimation跨真实帧边界清理旧appearance，再按最新app_text_color提交；递增世代淘汰旧帧任务，不缓存旧主题目标色。没有按状态栏单独判断一套黑白，也没有使用随机时间延迟或改变主题动画时长。跨帧刷新仍可能存在一帧中间外观，完整切换录屏与其他ROM需继续验收。
- **壁纸取色最终规则**：保留原0.6亮度阈值，通过原窗口、状态栏与Dock几何定位图标文字区域，48×48采样该区域亮度；暗色Dock不参与桌面图标区选择。默认毛玻璃素材在该区域应得到黑字，状态栏同步黑色；深色图标区选白字。窗口尺寸或LayoutProperty未就绪时保留原黑字预设，后续原主题初始化按有效几何重算。遮罩强度继续使用原全图算法，与文字区域取色分开；不改变感应光影、普通阴影、图标大小或宫格几何。
- **默认壁纸与黑边**：现场背景节点可见、1080×1920纹理存在，但sGaussianBackGray仍为初始化值1.0；无自选壁纸时未分析主题自带background.png，使外部背景被盖黑。现补取当前原版主题资源并初始化原遮罩系数。直接分析素材自身像素；本轮中间包发生的0×0位图崩溃来自Application阶段按未初始化窗口尺寸重采样，该路径已撤掉。总览间隙还使用Android系统壁纸层，故默认毛玻璃、无自选壁纸时复用WallpaperManager同步主题自带壁纸，仅FLAG_SYSTEM；自选壁纸或透明覆盖优先保留。后台执行，按来源／wallpaper id避免每次解锁重写；来源标记v2隔离ROM权限拦截时写入的旧成功标记，返回无有效id或实际id不符时不记录成功。此操作会更新系统桌面壁纸，锁屏不在调用范围；vivo权限批准与实际写入仍须单独验证，不能凭setStream返回或日志宣称完整通过。
- **主题设置状态**：currentTheme优先读取原版ThemeManager已选中的对象，未初始化时继续原存储回退。MAIN恢复只刷新主题预览、壁纸入口与缩略图；复用布局时显式恢复壁纸行VISIBLE，避免旧主题隐藏后的GONE残留。不重建设置页、不丢弃滚动位置。常规切换后的“当前”标记和毛玻璃壁纸行在V2458A已检查；魅族实际路由尚未ADB复测。
- **电话纹理**：普通路径按当前准备好的source计算resize，旧过渡／六参数回退按ItemInfo中保留的color.resize，存在不同内容框输入。两条合成入口统一调用原版分类器分析当前source，栅格缓存升到v30隔离旧结果；不改图标尺寸、Dock几何、立方体动画或PNG。魅族视频已见先变大再缩小，但该机真实分类值／纹理交接尚无ADB证据，不能称为该机唯一根因或单项验收通过。
- **修改文件**：`launcher/smali/com/smartisanos/launcher/data/Constants.smali`、`launcher/smali/com/smartisanos/launcher/e/g.smali`、`launcher/smali/com/smartisanos/launcher/e/s.smali`；`launcher/tools/java/com/smartisanos/launcher/theme/`内`MaintainedLauncherSettingsHost.java`、`LauncherSettingBridge.java`、`IconRasterDiagnostics.java`。Manifest、原图、shader、atlas、UV、mesh、12／20几何、普通阴影与解锁动画未改。临时文件写出及Window默认背景试验未保留，没有新增Manager／Service。
- **验证与边界**：标准构建成功，v1／v2／v3签名和zipalign已检；23项主题状态、33项设置会话、44项原smali纹理交接、图标合同审计通过。生产取色方法的5项隔离行为检查覆盖真实默认毛玻璃PNG、纯黑／纯白、冷启动零尺寸和缺失布局，默认素材选择黑字。真机已有保留数据安装、常规主题列表／壁纸行、冷进程、双指总览返回以及SystemUI字段／截图证据；用户最后确认当前正常。四指自动注入不能仅凭INJECTED当成功，仍需真实回调／前台核对；系统HOME有返回vivo桌面的既有行为，本轮未改默认桌面归属。完整自选浅／深壁纸、20宫格、透明覆盖、长期与跨ROM矩阵未验；ADB仅V2458A，魅族主题与电话放大未验。
- **文档与保护**：今天的倒序每日摘要和本详细记录同时更新，感应光影原有记录保留。MEMORY.md未更新；没有清用户数据、暂存、提交或推送。证据存于忽略目录`build/theme-route-audit-20261009/`。

**桌面图标感应光影：资源就绪、初始光照和暂停恢复同步**

- **确认的代码问题**：原J以20lux初始化跟踪值，首读数按10lux死区过滤，并从默认值开启过渡；初始值不代表实际传感器读数。Ra.q重新应用天气预设时直接写入Na.lU，覆盖已按lux调整的强度，后续相同读数可能被过滤。Oa在既有页面状态门提前退出后保留非零start，Ra.w持续拒绝更新；首个任务未执行前start=0又允许重复排队。材质读取派生投影失败时转到固定设置图标第八层资源，缓存会阻碍正确图案恢复；八层部分绑定也可进入绘制。IconIlluminationCompat.write与register共用类监视器，位图／文件工作会与恢复注册互相等待。这些路径有实际生产Smali探针对照证据，不把所有用户现场现象归为唯一原因。
- **最终修复**：H／r继续为原传感器Owner；用注册线程／世代拒绝旧回调和旧GL交付，保留合法缓存首读数。r合并最新lux到原n事件队列；首次有效读数直接初始化，恢复时复用已显示lux并保留10lux死区。Ra／Oa保存当前插值，暂停门退出后由原Qa有效更新接续；新值从当前显示值继续原过渡，不完成过时目标后再跳转。天气刷新按已有有效lux归一化，未取得光照传感器值时保留原天气预设。原2秒时长、Ma曲线、lux公式及0.5／0.7天气系数保持；不保留额外终点或零时长试改。
- **纹理与缓存**：仅派生应用／桌面设置投影禁止借用固定设置第八层；失败描述符不占据后续加载，MutiTex绘制需八层绑定均成功。新GL上下文由原Ea丢弃派生描述符，再由原材质加载，使用cb而非在新上下文删除旧ID。Settings投影移到现有Eb预载阶段预备。可见Cell缺失普通投影时经现有Source Resolver／Composer与有界Bitmap执行器恢复；写入进行中不重复排队，同世代失败不逐帧无限重试。Folder共享回退和ActiveIcon轮廓Owner保留。MASK_LOCK使生成／删除继续串行，并与传感器注册锁分开；缓存命中不重新生成八层。光照请求改为100000µs，实际回调仍由硬件决定，不能宣称原机实际500Hz或50倍节能。
- **修改文件**：IconIlluminationCompat、IconRasterDiagnostics、IconPreviewRepository；launcher/H、r、view/Eb、view/a/g.1、view/vc；smengine/Ra、Oa、Qa、Ea、mymaterial/f.1、h.1；既有传感器／生命周期／handoff探针和新增run_resume_probe.py。本轮没有新增Manager／Service，没有改Manifest、PNG资产、材质shader、atlas、UV、mesh、宫格／图标尺寸、普通阴影参数或解锁起播链路。
- **集中检查**：传感器111项、生产Smali恢复／绑定2418项、原向量handoff23011项、Android Bitmap缓存477项、删除／重启／缺层修复788项及持久缓存重启检查通过；预览61项无失败，图标合同审计通过。起点生产Smali探针复现冻结过渡和错误固定轮廓回退。纹理上传／场景门在探针中是显式受控边界，不等同桌面视觉验收。与起点索引比较J及材质公式文件不变，Cell除draw补资源检查外所有几何方法不变；设备旧包与新包1565个受保护Manifest／资源／Textures／native条目逐字节一致。
- **最终包**：标准build.bat、v1／v2／v3签名和16KiB zipalign通过，v1.5.8/code33，SHA256 `7586D222BE01938DA070768DBD57225CC0840A90E07547D228680802D019BBEF`，保留数据安装X21A/Android9。最终冷启日志首次255lux以phase=-1初始化在八层绑定前生效，未再从默认20lux渐变；14个投影绑定样本均ready=true。最终包4次连续解锁通过，PID22213保持存活，首次231lux恢复及时；该进程5次注册、5条冷启动生成记录，4次暖解锁没有新增PNG生成，采样无FATAL／VerifyError／失败绑定。开启→关闭→开启的恢复结果确认，调试属性已清空并重启回生产状态。截图／录像存于build/illumination-resume-20261009/，不把中间包12次解锁样本合并成最终包次数。
- **边界**：真实手持倾斜／遮挡光线未验，用户明确不在设备旁；现场三个偶发症状未取得同条件全量复现与统计，不能宣称所有场景绝无延迟／丢影。run-as被设备拒绝，未改debuggable或操作用户私有数据来造损坏；异常／上下文失效由隔离原代码探针覆盖。12／20完整切换、全部主题、动态天气／日历、Folder／Dock握持边界、长稳及其他ROM矩阵未全面覆盖。保留用户140%图标、+8文字、20宫格和原主题／布局；仅测试光影开关并恢复开启。MEMORY.md未更新；保留原有暂存与README等无关改动，未执行暂存、提交或推送。

### 2026-10-08

**主题列表奇数末行循环补图与动态边框重算（V2458A真机验证）**

- **根因**：当前 `ThemePreviewAdapter.getCount()` 只返回真实主题数；奇数末行缺少右侧 GridView 子项，左右两格的背景和底部圆角无法闭合。原版 `clean_launcher` 的 `B.smali` 会补出空格；用户进一步明确要求末格显示主题图案，滚动到顶部和底部都保持双格，因此在既有适配器中将末格映射回该区第一项。
- **修改**：奇数项时适配器仍返回偶数格，但末格展示并指向该区第一主题；首行仍展示前两项，末行展示最后一项和首项。点击重复项进入首项详情，不新增主题身份。背景数组按补齐后的格数生成，`applyState()` 处理本地／在线归属变化时重新计算首行、中间行和末行资源。真实主题顺序、下载、选择及详情逻辑不变。
- **验证**：`build.bat` 成功，v1／v2／v3签名及zipalign通过；保留数据覆盖安装到V2458A／Android16。真机本地主题为奇数时，末行“文艺黄｜经典黑”双格、左右底边和圆角闭合；点击重复的“经典黑”进入其已有详情，返回后滚至顶部仍为“经典黑｜蓝色”双格。当前在线主题为偶数，末行左右两格对称。所测页面和返回路径无Launcher crash记录。
- **边界**：本次未安装／卸载主题包来实际触发奇偶切换；代码已在既有状态刷新中重算，但该动态场景和其他ROM尚未真机覆盖。只有一个主题时，为满足双格会显示同一主题两次。

**替换图标重复默认入口删除与页面往返闪烁修复（V2458A最终包验证）**

- **最新要求**：删除替换页“还原默认图标”行。默认图标仍由应用图标列表左侧原有selectOriginal入口恢复；候选网格继续仅显示图标库／图标包，搜索更多／从相册选择保留。之前首轮优化保留独立还原行的布局由本条替代。
- **根因与最终实现**：返回列表时，只有应用枚举缓存被复用，分组rows仍从空状态异步构建；列表与顶部当前图预览键又包含导航session，暖返回无法命中旧图。重复全应用分组会解析大量图案并挤出可见Bitmap缓存。现在在同Activity且应用身份集合一致、已发布代际有效时复用既有分组／名称／版本／来源／搜索索引；恢复筛选与位置，有效暖返回不再重新扫描。数据过期或来源变更仍走已有后台刷新；待完成的来源更新禁止复用旧选中快照。预览键以现有Repository候选revision失效，图标变更通过既有invalidateIconData更新revision；session继续负责请求取消与旧回调拒绝，不再作为图像内容身份。候选身份／选中／包版本／标签未变时不替换原卡片。
- **修改文件**：MaintainedLauncherSettingsHost.java、IconPreviewRepository.java、既有app_icon_candidates探针与run_tests.py、icons/README.md及本日志。复用现有Adapter／Repository／缓存与180ms转场；无新增Manager、无图标资源重绘。工作区原有dimens.xml等改动及暂存状态保留，本轮未执行暂存、提交或推送，项目与全局MEMORY均未更新。
- **集中检查**：标准build.bat成功；v1／v2／v3签名、zipalign通过。201项候选／分组生产检查、18项UI接线和按键快照检查通过，预览61项无失败。新增检查覆盖连续返回复用、不同Activity／应用集合拒绝、待完成来源变更拒绝、候选选中／身份变化；javap确认构造器不提前扫描、预览键不再使用session；APK内classes2.dex与构建dex一致。
- **最终包身份**：v1.5.8/code33，SHA-256 `a2f44a00893ecd82e3a6394ccfa76809ee59dfbe543f46ba0e9fc8966d97d913`；V2458A/Android16保留数据覆盖安装，提取已安装base.apk校验一致。
- **真机范围**：最终包应用图标／替换页10次往返通过；3轮往返录屏抽帧确认暖返回图案持续显示，未再出现基线的候选或列表先空白再补图画面；截图／XML确认还原行删除，顶部和选中来源正常。搜索筛选、图标库与返回层级单独验证，过程日志保存在build/icon-page-polish/。不以录屏采样宣称所有单帧或所有ROM均无闪烁；冷缓存、内存压力、过期刷新、真实中文IME及改图写入／备份恢复完整矩阵仍未覆盖。

**设置页首个分组标题顶部距离统一（V2458A真机验证）**

- **根因**：主题页列表和应用分身、隐私密码页共同读取 `settings_section_content_top=18dp`；状态栏设置页首组使用原设置项 20dp 上边距和 `SettingItemTitleStyle`。两种标题容器的高度、内部 padding 不同，导致前者的实际文字约低 12dp。此前 2026-07-18 的 18dp 只统一了主题、分身、隐私密码三页，并未对齐状态栏页。
- **修改**：仅将共用 `settings_section_content_top` 从 18dp 改为 6dp。主题、分身、隐私密码的首组一起上移；不改标题栏、字号、卡片、主题预览或其他已使用原设置间距的页面。对照 `clean_launcher` 原主题布局和 maintained 主题布局，保留当前移植结构。
- **验证**：标准 `build.bat` 成功，v1/v2/v3 签名有效，zipalign 检查通过；保留数据覆盖安装到 V2458A（Android 16、1260×2800、560dpi）。真机打开主题、分身、状态栏三页并返回，主题和分身的首组控件 bounds 均为 `y=347..494`，状态栏标题栏底边 `y=326`，三页截图中首组文字视觉上对齐。Crash buffer 中未见 Launcher 崩溃；两条当晚 `AndroidRuntime` 属于 `uiautomator dump` 的自动化服务重复注册。验收 APK 单独保存在 `build/launcher-settings-spacing.apk`，原有同名构建产物恢复。
- **边界**：隐私密码页与另两页共用该尺寸，但未在本次设备上单独进入拍照；其他 ROM、字体缩放与横屏未覆盖。

**图标库、替换候选与搜索目录优化（实现完成，V2458A集中验证通过；完整兼容矩阵未覆盖）**

- **最新要求**：用户明确要求替换图标页不再显示默认图片候选；因此当前推荐网格只接收TYPE_LIBRARY／TYPE_PACKED，默认恢复和相册选择复用原设置行独立显示，MODE_ORIGINAL／MODE_CUSTOM及旧配置仍可读取。顶部继续显示实际生效图案，手选的跨应用RESOURCE和具体PACK图案仍保留。旧记录“默认图标始终作为可恢复候选”仅代表旧版布局，不能据此恢复网格默认项。
- **页面与任务**：保持原设置180ms转场、分类标题、标题／系统BACK层级、18sp分类行和原搜索资源。有限State只保存三组元数据快照和滚动状态，不持有Activity／View／Bitmap；目录revision变化清旧快照。同revision暖进出无需Catalog重解析或全包准备。在线索引先可用，图标包索引后台补齐，未齐时只报告已找到数量。查询使用已就绪不可变Catalog，不在按键时读取assets／PackageManager。现有Repository内增加有界查询／目录工作通道，取消会话会清掉排队任务；现有解码入口另有512个全局排队上限，优先让可见工作替换无界面消费者的低优先预取，压力拒绝会清掉pending，保留点击重新确认。HTTP与Bitmap缓存及v4磁盘路径保持。
- **包内目录**：派生缓存升级icon_pack_search_v2.db，原始声明stamp只依赖包版本／格式；Catalog和设备Label变化只比较并更新实际变化的名称／词项，不重解析未升级包XML。targets保留原始大小写和完整组件，单drawable的全部明确应用关联仍可搜索；主显示名称确定排序。COUNT／稳定排序分页代替全量命中ID数组，快照以包世代／数据库epoch验证。在线与PACK按同一相关度分段合并。单个坏包隔离并报告，覆盖DB及备份结构不迁移；v1仅派生缓存，在v2准备后移除。
- **名称与分类**：保留5199个PNG和全部sourceId、4720个应用身份／4625个包名路由；source与geometry保持分离，不以搜索别名自动换图。按精确包名核对Google Play、应用宝公开数据与本地F-Droid快照，名称及分类附来源证据、核对状态，未知不伪造；英文店名与原有中文名并存。已确认名称／别名的预生成全拼、分词、首字母及名称级覆写进入typed groups和兼容terms，APK词表也供已有IconPinyin使用。保留17个分类ID，补可信类别和搜索标签，不机械按包名前缀分类。当前1767个名称有来源证据，635个英文名称字段、2795个条目仍为标识符，“其他”1976个，详细清单由既有工具report输出。
- **参考核对**：指定原版主APK和clean目录未包含当前同名apps_category.json；当前与maintained存在这些分类JSON，因此本轮只称既有精确分类资料，不再将其笼统归为指定原版主APK资产。原版核心、PNG、阴影／感应、动态天气／日历、宫格几何、主题、解锁／Folder／快捷桌面与Manifest均非本轮修改范围。MT名称另由官网链接APK的包名／中英label核对，参考APK不安装到用户设备。
- **集中构建与自动检查**：全部生产代码和数据完成后统一执行标准build.bat，v1.5.8/code33，v1／v2／v3签名、zipalign与图标合同审计通过。最终签名APK SHA-256为`4f7e56010fa045c15ffdc6d23a0ee40aace739c2410554d73a352d2cab8cc018`，真机安装包提取后hash一致。候选189项、UI接线16项及按键查询快照检查、预览调度61项、目录维护10项通过。5199个PNG、4720个应用身份及包／组件／primary路由逐项与基线一致；1566个受保护APK条目（原版classes.dex、Manifest、资源、native库与Textures等）一致。既有1条非法文件名警告、18组同内容图片保留，不自动去重。
- **最终包真机验证**：V2458A、Android16/API36，保留数据覆盖安装；未改用户图标覆盖、主题或宫格设置。设置替换页截图确认蓝色系统默认齿轮已从候选网格消失，顶部仍显示实际生效图案；还原默认／相册为独立行。分类全部进入／返回30次通过；其他分类滚动10次，返回恢复原行位置及替换页／应用列表层级。weixin、wx、qq、qqyy、xiaohongshu、zfb和DeepSeek搜索命中对应应用。真机Android SQLite目录探针170项通过，0／1／5／20包覆盖至10万条；设备现有Smartisan OS包1922条，冷准备499ms、内存暖复用0ms、磁盘暖复用1ms。桌面12宫格、文件夹打开／点外部关闭、翻页及返回截图正常，保持原蓝色主题和布局。采样进程日志未见FATAL／VerifyError／ANR／页面打开或查询失败。证据保存在`build/icon-library-implementation/physical/`。
- **性能与验收边界**：旧包5轮386帧、jank1.55%、p95=13ms；最终包30轮2426帧、jank1.69%、p95=13ms。循环次数与swap状态不同，不据此宣称总体性能或内存改善；最终包实际查询样本5–10ms，其他分类3ms。2795个标识符名称与30项分类冲突继续待资料核对。未覆盖真实中文IME候选组合、真机跨应用改图／默认恢复写入／相册导入／备份恢复、20宫格及其他ROM完整矩阵；未改用户配置以制造这些测试。Delta真实包模拟器测试超时，不计通过。构建与上述实测不代表全部兼容性验收完成。
- **文件**：IconLibraryCatalog／IconLibrarySearchIndex／IconLibrarySearchPage／IconPackManager／IconPreviewRepository／IconPinyin、MaintainedLauncherSettingsHost、SmartisanInstallManager的重复图标失效调用、catalog与派生assets、tools/icon_library.py及既有候选／预览／目录检查、icons README、BUILD_GUIDE与本日志。SourceId、自动包／组件路由、RedirectIconDB格式不变。项目与全局MEMORY未更新；未暂存、提交或推送。

**应用图标来源、中文／拼音搜索、分类与滚动预览**

- **问题与根因**：X21A截图和现机旧包复现指南针在应用列表／桌面为银色改进版，进入替换图标却由硬编码 DEFAULT 标记且顶部取系统原图；单应用选择身份与实际 RAW 来源分别计算。图标库的 GridView 甩动时主动释放绑定并暂停加载，导致停下才看到图片；应用列表滚动绑定还重复读 DB／PNG、包版本和应用名称。旧目录4720个应用／5199张PNG，4458个应用名称与sourceId相同；原版 `launcher/assets/apps_category.json`／`category_name_list_json.json` 中已有较细类别，但此前只映射至8个粗类别，未归类应用无法按中文名检索。系统“设置”目标是手机系统应用，其可选图中两个同名齿轮有不同sourceId；不得按显示名称合并。
- **修复**：沿用当前 `RedirectIconDB`、`IconPreviewRepository`、现有桌面 RAW 查找与维护设置宿主；将生效Drawable和候选key在同一次 `resolveManagedIconSource` 中确定，替换页顶部显示实际生效图案，默认图标始终作为可恢复候选，单应用资源／图标包／自定义及全局改进版各保留精确身份。显式原图选择不再被后台图片下载升为 AUTO，自定义图替换后失效相关预览。选择后返回应用列表时使旧快照过期，后台重新核对有效来源。列表版本／标签／生效状态在后台快照中计算；滚动一帧合并可见请求，图库滚动不清空图片，前后相邻两行只预取本地资源且不占可见请求槽。维持既有网络双线程、有界图片缓存、取消令牌与原资源／布局／动画。
- **目录与搜索**：保留全部PNG和sourceId；复用原版精确包名到类别的表，将新闻资讯、生活实用、交通出行、商务办公、学习教育、金融理财、铃声壁纸、儿童母婴、书刊阅读单列。结合已审核常用包名及F-Droid精确包名记录补中文／英文名称，给中文名及别名写入全拼／首字母关键词；图标库与应用图标列表共用 `IconPinyin`，本机已安装应用标签在各自后台索引中追加全拼／首字母，输入时不运行ICU。最终2621个应用仍归“其他”，其中大量只有包名，不能保证未知应用的中文检索；不按包名片段臆测身份／分类。分类影响手动搜索，自动换图仍只按明确包／组件身份。
- **验证与限制**：源与派生索引审计5199源／4720应用／4625包名、0错误，1条历史非法文件名警告；图标候选189项、UI接线13项、预览48项、目录7项及图标合同审计通过。标准 `build.bat` 成功，最终v1.5.8/code33，v1／v2／v3签名与zipalign通过；签名APK SHA-256 为 `E7A6ED3D22F492971E1517D70E51280C3C49B48FB4E9C7FD408061B120920CC7`。Android16模拟器上同数据安装旧／新APK对照：旧包替换页顶部仍是蓝色系统原图而勾选齿轮，新包顶部／勾选／应用列表一致；选择另一齿轮后2秒内列表更新，返回替换页仍一致。图标库 `weixin` 命中微信中文名，甩动过程截图可见图标，最终APK冷启及应用图标页打开无AndroidRuntime崩溃。模拟器相同8次甩动新包两轮jank分别38/188和62/168，旧包51/175，波动大，不能推出稳定帧率改善。上一轮旧包X21A图标列表8次甩动113/337帧jank、p95=26ms，系统图库109/343、p95=23ms；2026-10-08 X21A未连接，最终APK在该机的滚动流畅度、中文IME拼音输入、桌面图标／冷重启跨ROM一致性仍待同机测试。Android目录探针编译／推送后被设备app_process杀死，未取得本轮SQLite运行结论。其他ROM／图标包异常和未知目录条目仍待实测。
- **文件与保留**：`MaintainedLauncherSettingsHost.java`、`IconPreviewRepository.java`、`IconLibrarySearchPage.java`、`IconLibraryCatalog.java`、`IconPinyin.java`、`AppIconSearchIndex.java`、`icons/catalog.json`及派生索引、`tools/icon_library.py`与对应受控检查／本日志和icons README。原版APK／clean_launcher已核对设置包身份及原资源；maintained仅参考设置页，不替换原版Launcher核心。已有暂存／未暂存改动保留，未暂存、提交或推送本轮文件；项目与全局MEMORY.md未更新。

### 2026-10-07

**冷重载后快捷桌面首次进入缺少过渡动画**

- **现场与根因**：V2458A／Android16用户多次备份恢复后的ADB记录中，19:50:46完成BACKUP_RESTORE新Launcher首帧；19:50:53首次右滑在53.368松手并开始吸附，GL截图请求53.369、背景应用53.417、PopupWindow显示53.430，窗口显示时吸附已运行；同一进程再次右滑在19:50:58.336请求截图、58.366应用、58.372显示窗口，58.396才松手并开始吸附。首次可见画面因窗口晚到而跳至接近终点。原版clean_launcher的MagicFlow入口在原版系统环境中调度，maintained没有当前移植的GL截图＋PopupWindow宿主，故仅修当前QuickDesktopController的交接。
- **修复**：若松手决定打开而背景尚未就绪，保留打开目标，把宿主保持在几乎关闭的位置；截图应用且PopupWindow确实显示后，再复用原settleTo动画。普通背景及时就绪的连续跟手、关闭／取消、触摸归属、200ms曲线与原版手势门控不改。新DOWN／HOME／宿主清理会丢弃未显示的旧打开目标，避免迟到截图重开。
- **验证**：QuickDesktopCaptureGateProbe 99项及RootView截图顺序静态检查通过；标准build.bat成功，v1.5.8/code33，v1／v2／v3签名有效，保留数据安装到V2458A成功。冷启动稳定后的首次右滑录屏逐帧显示桌面→快捷桌面局部揭露→完整打开，左滑连续关闭；截图与视频在build/qd-first-open-stable-20261007.mp4和对应sheet。安装后第二次打开截图显示完整内容页、窗口存在。未重做真实备份恢复，以免改动用户桌面数据；本机冷启动录屏证明该路径的可见动画，不能宣称备份恢复全链再次验收。设备persist.sys.log.ctrl=no导致新进程QuickDesktopHost日志不再输出，修复后晚到分支的实际命中未由logcat确认；旧包现场日志是根因证据。当前进程未见新的崩溃退出记录，日志屏蔽限制仍在。
- **文件与风险**：仅QuickDesktopController.java、既有QuickDesktopCaptureGateProbe.java及本日志。若GL截图始终失败或窗口不能显示，原有下次DOWN清理规则保持，仍需实机检查极端失败路径、慢拖中途截图晚到、真实备份恢复与其他ROM。MEMORY.md未更新；既有暂存／无关改动保留，未暂存、提交或推送。

**透明／毛玻璃主题取消桌面左右边距：新授权的布局修复**

- **问题与证据**：用户撤回此前光影试改后，提供同机1260×2800普通／透明主题同布局对照。图标内部细节匹配确认相机／设置／文件夹主体尺寸基本不变，但四列横向位移约+16／+5／-5／-16px，Dock横向未移动；核心是透明主题额外左右页边距使图标区收窄。用户明确要求“取消透明主题，毛玻璃主题的左右边距”，本轮是随后独立授权的布局改动，不恢复已撤回的光影方案。
- **实现**：复用LayoutPropertyParser/P.smali现有加载入口，仅在竖屏普通12／20宫格资源（含20宫格历史键兼容）解析结束、LayoutPropertyAdapter适配和原formatCell/createCellPoints之前，将透明后缀或毛玻璃标志下的page_view_margin_left/right设为0。普通主题、横屏、Folder后缀、其他概览模式仍走原字段；上下边距／行高、Dock、颜色／阴影／图标尺寸／字体、资源PNG及原版渲染链不改。既有代码由新有效宽度重建Cell中心、Camera、atlas和壁纸取样，不追加缓存留白／边缘mesh、不改shader、不替换Page渲染Owner。
- **代码验证**：tools/tests/transparent_layout/run_tests.py执行生产Smali键选择和边距归零方法，遍历实际layout.xml及透明／毛玻璃／普通／Folder、横竖屏、各资源模式，检查只有两个字段在限定条件下变为0、重复执行幂等、其他字段保持、720／1080／1260／1368／1440的格式化有效宽度；23700项通过，修前Parser副本在目标边距检查失败。图标合同静态审计通过；毛玻璃标志在原Theme初始化／prepareToChangeTheme中建立，未新增运行时扫描或逐帧补偿。
- **构建／安装**：标准build.bat最终成功，v1／v2／v3签名与16KiB zipalign通过。v1.5.8/code33，SHA256 `66DCB486A93B3C405A77E3E8509E1164D896DFFCA185E1362AA86353E503AF58`。相对安装前撤回包，ZIP条目仅classes.dex和签名改变，classes2.dex、resources、native、Manifest及图片相同。一次构建在签名阶段遇到APK临时文件占用，释放后标准重建成功；一次安装确认被中断，最终按真实vivo安装页完成确认后保留数据安装成功，设备base.apk hash一致。未把失败尝试记成成功。
- **真机对照**：V2458A／Android16／1260×2800、原透明主题和同一壁纸／布局。最终透明页面相对用户普通主题图片的相机／设置横移0px、文件夹-1px，首列信息绿色标记中心157.5对157.0px，Dock设置横移0；原约16px左右内缩消失，图案大小未增加。透明主题原有纵向差异仍保留，未承诺全部Y坐标与普通主题相同。壁纸图片资源不变，但页面宽度重建会改变合成取样，未宣称背景像素逐点零差异。
- **操作／边界**：负一屏进入及BACK返回已操作；Folder点击进入／BACK返回已操作，保存画面处于打开动画中，不能算完整静态Folder视觉验收。当前只有一个可见桌面页，左滑未翻到其他页，未把该动作报成多页切换通过。未修改用户开关、图标大小、文字大小、布局或保存主题／壁纸；最后回到Launcher。毛玻璃完整真机、12宫格实际切换、其他ROM／屏宽、全部倍率／握持姿态和概览／拖动尚未全覆盖，不把横向对齐结果外推成全部光影问题通过。
- **文件／记录**：生产仅P.smali；测试在tools/tests/transparent_layout/。证据与修改前Parser／设备APK／暂存索引快照在build/trans-layout-unify-20261007/，此前截图测量在build/trans-layout-audit-20261007/。MEMORY.md未更新，保留原有暂存内容，未暂存、提交或推送。

**今天光影改动已撤销：恢复当天开始前的实现**

- **用户决定与当前状态**：用户要求“撤销今天光影的修复”，停止修复／诊断试改。用户最新普通／透明主题对比显示普通主题光影正常，透明主题出现投影残片与背景分割；只关闭感应光影后残片消失。该透明链路问题未解决，不保留之前候选的验收成功说法。
- **撤回范围**：按本轮开始前保存的逐文件副本，恢复smengine/D.smali、view/b/ka.smali、view/a/g.1.smali；取消今天加入的atlas水平扩容、边缘网格／UV延伸、投影视口源取值变更。移除PageAtlasMetrics、TransparentProjectionProbe以及vc.smali的临时采样钩子和今天投影测试，已撤下的纹理wrap试改不恢复。PageNoRenderTarget直接分支试验曾导致所有正文节点集中在屏幕中心，已立即撤下；fa.smali仍为试验前原页面选择，没有保留该分支。
- **明确保留**：Dock光影10月3—4日的ca.smali深度遮挡修复、10月5日前已存在的页面光影实现／动态mask兼容；20宫格文字放大与GRID_12／GRID_20／LEGACY_ENGINE_KEY_GRID_20命名兼容继续保留。没有全仓回滚、改数据库／布局、删图标PNG或撤回图标库／预览等无关修改。保留相关文字回归测试。
- **验证边界**：恢复文件与10月7日开始前备份逐字节比较；旧光影边界问题可能仍在，这次只是撤回试改。标准build.bat成功，v1／v2／v3签名与16KiB zipalign通过；保留的文字测试73项和图标合同静态审计通过。撤回包v1.5.8/code33，SHA256 `64BA9479A7D13E11CAD8016B742D6908E7F78E994A25C003586BEF72C7D58388`，最终classes.dex／classes2.dex确认没有PageAtlasMetrics或TransparentProjectionProbe。当前V2458A保留数据安装成功，设备base.apk hash一致，Launcher进程PID25859存活。校验过程中手机已由用户进入相册，获取的是相册画面，不能算作撤回桌面视觉验收；不再打断用户操作，未修改主题／开关／布局，不把撤回当成透明主题问题已修复。
- **设备范围**：直接绘制试验安装在X21A后立即保留数据恢复试验前包。撤回时ADB连接已变为V2458A／Android16，X21A及魅族不在线；只对当前授权连接设备执行保留数据安装，不声称不在线设备已安装今天撤回包。
- **记录与保留**：本轮撤回前源文件／探针与暂存索引快照保存在build/light-rollback-20261007/，未删除原APK参考。MEMORY.md未更新，未暂存、提交或推送。

### 2026-10-05

**放大桌面图标的感应投影遮挡与动态天气／日历开关残影**

- **当前状态**：现行修复保留原合成顺序并调整投影的缓存视口，已构建、保留数据安装；截图中感应投影重新可见。手持左右倾斜、页面外边缘及完整主题／宫格矩阵仍待验收，不标全场景通过。用户指出首轮切边仍在、后续直接绘制候选失去感应效果；两种失败方案均已撤下，不再把初轮截图当作通过证据。
- **确认的根因**：桌面与 Dock 绘制目标不同。真实 GL 诊断显示桌面 mode9（20宫格）使用 1216×2180 整页 atlas，投影被限制到 304×436 的格子 viewport，投影横向角点为 -63.992～367.992，即宽431.984，超出两侧各约64像素；Dock target/viewport为空，直接绘制。原深度修正不能解除格子 viewport 裁切。直接将投影移到主屏幕则遇到正文／背景缓存的绘制分类与覆盖，不作为最终方案。
- **最终实现边界**：仅 iew/a/g.1.smali 中 sc[27] 的 page-batch 绘制，按真实格子／完整 atlas viewport 比例和现有 Cell Camera 计算 scale/translate，将同一投影映射到现有整页缓存；屏幕投影位置、尺寸、UV、天气／握持向量和 shader 保持原合同，不使用固定放大系数。标量复制 viewport，避免 SceneNode 的 Ga 引用 setter 与 RenderTarget 共用可变对象；每次从 Ra 原参数重建，避免累计缩放。退出 page-batch 时复用原 forceUpdateShadowMap 一次恢复直接几何；保留 Folder owner 的深度遮挡。正文／背景格子 viewport、Page blend、层级和原 CellOnPage 均已恢复原实现，ga.smali 无本轮净修改。
- **动态开关残影**：关闭时普通来源写入 Pe() 对应八层 PNG，重新开启 ActiveIcon 原来没有提交当前轮廓。LauncherSettingBridge.composeActiveIconToBaseBounds() 在原版动态正文回收、接触阴影合成前，经 qP/Rj/Pe() 复用 IconIlluminationCompat.prepare 更新八层 Alpha。原缓存签名／同Alpha复用保持，不删除数据库或所有缓存，不把合成后的接触阴影当作 mask。两份原版 APK 对应 clean_launcher／clean_launcher_raw 的 Cell、Camera、PageWithRenderTarget、ActiveIcon 已对照；maintained 仅用于状态 API 参考。
- **验证及限制**：标准构建、图标合同静态审计、现有58项阴影选择／缓存、24项主题转换及真实Android的477项投影缓存检查通过。现行启动日志图标合同83 events/matrix=6通过；这些不替代手持验收。当前透明覆盖、140%和20宫格的真实截图，文件管理／相册／企业微信三个正文ROI相对修改前RGB最大差异均为0。微信原 x325/326 切边的所测最大RGB跳变由9降到2，平均由3.341降到0.435；文件管理外侧所测最大由2降到1，仅作为这一姿态的局部证据。Folder打开／返回、桌面长按垃圾桶／Dock收拢及取消截图已检查。最终包再次关闭／开启动态功能成功，真实天气／日历Pe键八层mask更新，恢复后79 events/matrix=6检查通过；重新开启后的日历和第五页天气截图保留。20:58后的crash buffer为空。
- **最终产物**：v1.5.8/code33，标准build.bat、v1/v2/v3签名、16KiB对齐通过。保留数据安装vivo V2458A/Android16，手机拉取base.apk与最终APK SHA256一致：`4F124E9D7D616D1CB18720B19BE992DBDE5B9A4FB7AC055C07595D46640ED444`。最终classes2.dex确认没有临时诊断类；相对本轮初始手机包只变classes.dex、classes2.dex及签名条目。新截图为final-atlas-home/longpress/folder和final-reenabled-home/weather；没有用安装成功或静态截图补报手机左右倾斜的验收。
- **文件与风险**：生产净修改为 g.1.smali、LauncherSettingBridge.java，另更新本日志；临时诊断源码已移除。Dock ca、IconRasterDiagnostics、IconVisualMetrics、八层算法、shader、资源、PNG及原动画均未改。整页投影会增加相对格子裁切的片元面积，性能预算未测；非page-batch、其他主题／倍率／ROM、页面外边缘、拖动迁移及12宫格仍未完整覆盖。保留所有既有及并行工作变更。未更新项目／全局MEMORY.md，未暂存、提交或推送；本地证据在 build/page-illumination-fix-20261005/。

**图标搜索界面与锁屏／解锁：停止时的当前状态（未全场景验收）**

- **用户最终要求**：先停在当前版本，只更新文档。此后不继续改生产代码、测试代码、PNG、构建脚本，不重新构建／安装／操作手机。后续恢复排查前先看本条，不能把上一次局部通过当作最终结果。
- **图标搜索界面**：搜索框和“搜索更多图标”入口复用应用图标页宽度／原圆角资源；入口与类别行复用18sp锤子标签。计数原本与标题都设置14sp，但分别创建控件；现直接从“搜索结果”继承实际字号、Typeface、颜色、字距、文字缩放和字体Padding。类别点击通过原设置宿主打开下一页，复用180ms转场并显示类别标题；返回先恢复类别首页及列表位置，再回替换图标。搜索结果右侧“共 N 个”取已有在线列表与包内快照之和，不新增图片加载／扫描。
- **分类与中文搜索**：目录来自APK assets，类别少／中文查不到的原因是旧条目只有包名与other类别，不是未推Gitee。当前源库5199个PNG、4720个应用记录、4625个包名；补充常见名称后仍有4470个记录未可靠分类，不能称为全库中文完成。后台目录初始化会补充本机已安装应用真实标签／声明类别；输入及Cell绑定不访问PackageManager。自动匹配仍只用明确包名／组件身份，中文模糊检索只用于手选。未同步镜像可能影响新PNG下载，不影响APK内的分类文本。
- **搜索已验证范围**：vivo V2458A／Android16上类别下一页标题与返回、全部7121／包内1922／系统111／社交75／影音101／浏览器25已检查；Edge查询7、无结果0及类别首页隐藏计数已检查。真实Android目录128项覆盖53个已装包标签、中文微信4／日历3／浏览器15条在线匹配、0／1／5／20合成包最多10万条及分页／取消。中文索引是生产搜索方法的Android检查；shell文本注入探针被ROM终止，不将其称为真实中文键盘UI验收。未知应用名称、真实跨应用保存／恢复／进程重启、20个真实安装包、长期滚动及跨ROM仍待验。
- **微信误播根因证据**：旧诊断进程2425的session4在USER_PRESENT到达时resumed=false／focus=false，仍保留pending；约1294ms后普通返回桌面获焦点才COMMIT_PLAY。系统设置单次录屏未复现不能证明微信路径通过，仅提前onPause清理或应用启动取消也未覆盖完整后台交接。后续用后台写入最近128条事件的临时文件绕过ROM日志屏蔽，诊断文件不是正式功能。
- **当前保留的会话保护**：在已有LauncherBelowKeyguardCompat和startActivityForUser中处理，成功启动外部应用后清旧资格；当桌面未resumed且收到实际解锁信号时，公开ActivityManager.getMyMemoryState只读自身进程importance，明确高于FOREGROUND才取消待播会话。未知状态保留原规则；前台但onResume晚到仍允许交接。已消费会话拒绝迟到GL prepare。没有加入其他应用扫描／黑名单、UsageStats、无障碍、权限或新Manager。接口说明见[Android公开API](https://developer.android.com/reference/android/app/ActivityManager#getMyMemoryState(android.app.ActivityManager.RunningAppProcessInfo))。
- **误播的有限通过证据**：63DA诊断样本中后台importance=125，取消后未等返回桌面再COMMIT；正常桌面交接importance=100，兼容开启的session9–12仍播放。用户当时确认“微信返回正常，正常解锁动画也正常”。这只确认该包与该路径，不能外推到后续准备流程调整后的最终包、长期或所有ROM；当前最终包的完整误播回归仍待补足。
- **仍存在的问题**：用户随后明确表示“桌面先静止一下，动画才开始”，且在恢复／再调整准备流程后再次反馈锁屏仍会卡一下。准备链在锁屏过渡中改变场景、关屏广播晚到、首次可见帧与渲染准备交接等是待核对的方向，尚未获得足够证据确定所有卡顿的唯一Owner。当前状态必须写为**锁屏卡顿与解锁前静止未解决／性能未验收**，不能写“锁屏、解锁已经流畅”或承诺零回归。
- **起播时机冻结与当前代码**：用户要求“不要改变之前的解锁时机，包括解锁兼容的时机”。当前tryCommitUnlockAnimation和scheduleV157ResumePreRoll保留任务开始前实现，普通焦点门、兼容有效dismiss不等焦点、原120ms预滚不改；XML／目标时长／几何／材质未改。准备入口曾全量恢复，随后又恢复了关屏确认／锁屏唤醒覆盖下准备的分支，因此**不能声称整个准备流程与旧版一致，也不能由播放方法一致推出实际可见起播没有延迟**。restored-normal-timing.txt是一次中间版本比对，只能作为历史证据；后续必须重新比对当前源码／对应包。
- **停止时的产物与证据**：最新本地产物为v1.5.8／code33，SHA256 `5D1B7A127AFB5C828B806649EF3AFFC27C564BD01AF5BA117BECAA1D04D53520`，对应build-lock-working-chain-restored.log。该构建有标准构建与保留数据安装成功记录，但用户最新反馈仍是锁屏卡顿；停止后未再次读取手机hash或做新的签名／性能验收。临时文件诊断已从源码移除，任务生成的手机诊断文件已在归档后清理，未恢复。全部验证材料保留本地 `build/icon-library-validation/`，图片／应用数据没有重置。
- **帧采样限制**：已保存unlock-audit/unlock-frame.perfetto-trace，但第一次查询未返回Launcher进程／相关切片；尚未完成采样有效性、动作时间轴及首次静止帧归属检查。不能因为存在trace文件，就宣称已经测得Launcher长帧或已定位／优化解锁延迟。没有新的可信全项目流畅度改善结论。
- **后续核对顺序**：先以同一包、同一兼容开关／主题／宫格匹配正常锁屏与微信返回的实际路径；确认trace确实包含Launcher及相关窗口／帧，再对齐真实关屏、locked-resume、首次可见画面、prepare和PLAY。仅凭未复现、构建成功或方法文本相同不得继续扩大结论。不得凭感觉增加随机延迟、改变起播门控或扩大回退准备链，先确认第一个真实异常。
- **本次文档范围**：仅更新本日状态、专项计划及图标库说明；项目／全局MEMORY.md未更新。保留已有Git暂存／未暂存内容，不执行暂存、提交或推送。架构与此前快捷桌面修复的已测记录保留，最新否定反馈优先于较早局部通过。

**图标库架构与基础验证（最新界面／停止状态以上一条为准）**

- **复用与新增原因**：复用当前 `AppIconCandidate`、`IconPreviewRepository`、`IconPackManager`、`RedirectIconDB`、原版搜索控件、加载资源和应用图标页行布局。现有替换页 ScrollView + GridLayout 不适合全库，因此仅新增 Settings 宿主内的可回收 GridView 控制器及轻量目录；未新增 Activity / Manager / Service。原版与 clean_launcher / maintained 设置资源作为布局、字号及Cell参考，未替换原版桌面核心。
- **数据保护**：PNG文件名与sourceId不变，catalog登记身份／别名／分类，variants兼容；构建改为源Audit → Generate → 生成结果Audit。用户确认的PNG删除／替换全部保留，并显式清理失效引用；生成器不能先吞掉错误。当前5199个PNG、4720个应用记录、4625个包名；初版4697条、补充后4470条分类尚未人工完善，18组重复内容及一个历史带空格文件名保留为审计提示，不擅自清理。
- **线程与加载**：发现候选只读元数据；文字搜索120ms debounce，旧generation不能反写；图标仅在可见Cell绑定。原下载链保留Gitee→GitHub和cache_v4，2条有界IO线程（队列24）与原2条预览线程分离。退出取消本页排队任务，Cell复用按session/renderKey丢弃旧回调。图片缓存6–16MiB，在线RAW磁盘上限64MiB。
- **图标包全库**：用户明确允许扫描包内全部声明图案并跨应用替换。目录由现有IconPackManager后台复用appfilter及picker XML，SQLite持久缓存64MiB，按包版本／catalog revision失效，安装更新卸载通知刷新；内存最多4×60条分页描述。首次进入显示“正在加载所有图标”，完成后开放输入／分类。旧pack:package保持目标匹配；新pack:package#drawable保存具体图案，数据库key仍是当前目标应用，不改分身主键。提交前重新验证图案可读，旧来源和恢复字段保持兼容。
- **界面结果**：宽度／原圆角资源、18sp入口与类别行、计数与标题字体继承、分类真分页及返回层级，均以上方最新状态为准；不要恢复早期privacyRow的22sp黑字或仅在同页切换GridView的结构。选图成功仍直接回替换页，计数只使用已筛选元数据。
- **隔离检查**：候选182项＋10项接线、预览队列43项、catalog 6项均通过；图标渲染静态合同通过。实际Android SQLite目录probe 71项通过，覆盖0／1／5／20个合成包、最多10万条元数据、取消及分页；真实已装包1922条，probe首次2232ms，内存／磁盘复用0ms。曾发现Android PRAGMA max_page_count返回行不能用execSQL，已改rawQuery读取并关闭；该早期崩溃属于shell probe，不能算Launcher崩溃。
- **真机目录及导航**：vivo V2458A／Android16，实际全库7121条（在线5199＋包内1922）；目录准备日志133ms、复开6／16ms，所测搜索2–6ms，预览cacheLimit8388608。图标包、全部、浏览器结果标题BACK均先回分类首页，再以系统BACK回替换页。最新数量包再次保留数据安装后截图确认右侧全部7121／图标包1922／Edge查询7／无结果0；分类首页隐藏数量，标题和系统BACK顺序均通过。新进程15599目录复用5ms、所测筛选4–8ms，无新增AndroidRuntime错误；不是完整性能矩阵。框宽与前页一致。验证资料本地 `build/icon-library-validation/`。这些耗时为所测路径，不保证任何设备／网络均无卡顿。
- **构建与边界**：标准build.bat、v1/v2/v3签名、保留数据安装通过，版本仍v1.5.8/code33，当时数量功能验收包SHA256 `7FDB7401744C8AB7FDB674587CD92A672003CA13469C37F529152806275D6E72`，手机安装包hash一致。真实跨应用改图未写入用户Edge配置，具体图案读写身份由隔离测试覆盖；实际备份恢复／进程重启、20个真实安装包、长期滚动及其他ROM待验。桌面GL不出HWUI帧时不能以0帧推断流畅；旧设置样本754帧／2.12%与新功能样本路径不同，不宣称整体性能提升百分比。未修改阴影、几何、动态图标或原版手势链，本次不代表此前全项目性能方案全部完成。项目／全局MEMORY未更新，未暂存／提交／推送。

**快捷桌面首页入口及截图前触摸取消：原版对照后的回归修复**

- **原版核对**：直接从 `original_apks/com.smartisanos.launcher-3.apk` 的 classes.dex 提取 RootView、Eb、fa、e/e、e/b 和 InputManager，避免 Windows 大小写文件名碰撞丢失 `v` 的参考；RootView.a／i、Eb.Dh、fa.Am／vm／sr、e.ng 共7个方法与 clean_launcher 去除行号后的正文一致。`Eb.Dh()` 在 `sr()==0` 且文件夹关闭的条件下分别处理单页 `Am()` 的首页动画进度与多页 `vm()` 第一组的位置，并继续检查拖动／切换等原状态。原 `e.ng()` 通过后台 `ContentResolver.call(MAGIC_FLOW_URI, "request_show")` 请求系统 MagicFlow，短暂 `uu` 状态下 RootView.i 向 InputManager 派发 CANCEL；InputManager 在 UP／CANCEL 清理 ME／LE，rh 则补偿上一触摸周期缺失终止事件。不能把系统接口的短状态门直接移植为全局禁用触摸。
- **两个回归根因**：10月4日把概览13／10一律拒绝，错误改变了原版多页首页入口；原有接管后在释放时才取消引擎触摸，使申请背景截图时图标按下仍可能存在。仅修改截图触发不够：原 GL update 与请求发布并发时，在 update 后领取请求还可能读到取消事件处理前的一帧。窗口失败后若继续更新打开进度，也可能留下未呈现宿主状态。10月4日捕获到的不可见可触摸窗口仍是有效现场，但不能以禁止多页功能代替治理它。
- **最小修复**：沿用 RootView 的原方向／单指／J.Ta／首页允许分支及现有 Controller／Capture／Host。候选允许12／9／13／10的首页，非首页和图标编辑仍排除；确认接管时，复制当前事件为 CANCEL，经原 j 派发后才 requestShow。已取消目标不再收到后续 MOVE；终止事件沿原 RootView 状态清理，但不重复派发 CANCEL／UP 到目标。GL 在 Eb.update 前领取截图世代，再 update 和读回，保证已排队的 CANCEL 在捕获帧被处理。窗口显示失败立即关闭；显示过程中被取消后不再重开进度；新 DOWN 清理截图／窗口未呈现的旧打开状态。未新增 Manager／Service，未改动画、阈值、主题、光影或全局输入开关。
- **修改文件**：`launcher/smali/com/smartisanos/launcher/view/RootView.smali`、`view/vc.smali`、`launcher/tools/java/com/smartisanos/launcher/quickdesktop/QuickDesktopController.java`；扩展既有 `tools/tests/quickdesktop/QuickDesktopCaptureGateProbe.java` 和 `run_capture_gate_probe.py`。没有改原版 InputManager 或 Cell；原版提取、现场、窗口、截图、控制实验与安装证据保留本地 `build/quickdesktop-gesture-20261005/`。
- **隔离验证**：97项真实 Android MotionEvent／VelocityTracker 配合受控宿主的检查覆盖首页模式、非首页／编辑排除、已取消 MOVE／UP、未呈现旧宿主、窗口显示期间取消和重新进入；9项截图 generation 检查通过。3项 Smali 静态顺序检查分别核对取消先于请求、终止不重复派发、领取世代先于 update／读回。这些不替代实际 Launcher 窗口或 GL 验证。
- **真机验证**：vivo V2458A／Android16、普通灰色主题12宫格。单页从相机／时钟／日历起手右滑10次，多页第一组相机起手10次，均实际显示快捷桌面，未离开 Launcher，BACK后对应全屏 PopupWindow 已移除。多页反向、ACTION_CANCEL、第二指打断各3次，之后可以重新打开；非首页右滑先返回第一组且无快捷桌面窗口，再右滑才打开。单页连续10组翻页、Folder打开／外部关闭、桌面设置点击及返回、快捷桌面左滑关闭、HOME关闭及重新进入均已检查。单页相机100ms按下后右滑与空白起手截图，所测相机背景 RGB 通道最大差异1、平均绝对差异0.000422，未见按下残留；不宣称所有动画帧像素完全一致。
- **日志与最终复验**：旧包日志确认为 request→background→释放取消的次序。首个安装进程7444没有MAIN应用日志；手机 `persist.sys.log.ctrl=no` 且shell无法更改，具体限制Owner未确认。临时设置现有 QuickDesktopHost 日志tag，最终安装进程14023可输出该tag，9次实际截图请求均有前置取消标记，记录为取消→请求→背景→窗口；未用旧进程日志证明新顺序。日志tag已恢复原空值。最终包单／多页各3次图标起手、反向取消及重新进入、Folder和设置返回，共18个实际窗口状态检查通过；首次安装后一个早期手势仅形成候选、未得到RootView揭露资格，不计为成功打开样本，桌面稳定后的验证另存 `final/`。所测进程持续存活，AndroidRuntime未见新错误，系统退出记录最近仅为 PACKAGE UPDATED，无新崩溃／ANR退出；不代表完整长期日志验收。
- **构建与安装**：标准 build.bat、签名v1／v2／v3、16KiB zipalign及保留数据安装通过；v1.5.8／code33，最终SHA256 `083CD9C8E1E149EB92C5F87D51C11A8F1620D9936ED7C2CD2B61F8E151031393`，手机拉取包hash一致。前述单／多页各10次以及完整取消／非首页／HOME／左滑验证用首个构建FA0A42…包，最终只补显示时取消后不复活的保护，并以上述3＋3及窗口／日志复验覆盖；两个构建证据分开保存，不混称全矩阵最终包通过。
- **范围与风险**：实际20宫格、透明／毛玻璃、长时间随机手势、四指主题、系统面板／锁屏／生命周期与跨ROM完整矩阵仍待验；故障窗口的系统异常条件仅受控检查，未在真机强制制造。未以本次修复承诺全项目流畅度或所有历史冻结已根治。项目与全局 MEMORY.md 未更新，未暂存／提交／推送。

### 2026-10-04

**应用图标页搜索固定顶部与锤子圆角资源复用**

- **现象与根因**：搜索框原先追加在 ListView 页头设置项后方，随内容滚动；过滤只改变 adapter rows，设置卡片仍占据搜索结果上方空间。设置专用样式将原 QuickSearch 胶囊 NinePatch 拉伸，同时叠加 outline 裁切和系统 elevation，形状与阴影不协调。对照原 APK 的 clean_launcher 搜索布局和 maintained 的 app_icon_settings_layout，确认此应用图标页由现有兼容宿主拥有，保留原版桌面搜索入口及资源。
- **最终实现**：用户最终选择锤子圆角矩形，复用 maintained 设置资源 `sub_item_back_ground_single.9.png` 的现有圆角、边缘和阴影，取消额外系统投影，不增加或改绘 PNG。只在 APP_ICON_LIST 的现有 RelativeLayout 中增加标题下方的固定搜索容器，ListView 排在其下；共享 XML 与替换图标页保持。继续复用 OriginalSearchBarCompat、现有查询索引、虚拟列表、会话和预览链路。保留一个 header slot 的位置契约；有有效关键词时收起设置 header，查询/聚焦将结果滚到可见位置，空关键词只滚过设置 header 而不隐藏它，清空后可向上滚回设置。原清空保持焦点与键盘的操作保留；未增加全局键盘、系统栏监听或定时器。
- **验证**：标准 build.bat、apksigner verify、16KiB zipalign、aapt2 badging 通过，保留数据安装成功；v1.5.8/code33。最终安装 APK 拉取 SHA256 与本地产物一致：`853A1E8BDC3938FBD18A7F8D7FC7C5E88BC25E14569E41483370C30C8C8D5074`。vivo Android16 真机截图与 UI dump 确认滚动前后搜索编辑区坐标均为 `[196,402][1218,473]`，高于图标样式；Edge 搜索结果完整显示在键盘上方，无结果提示、清空、收起键盘后滚回顶部恢复设置、替换图标页及标题返回已检查。现有候选/查询生产受控平台回归344项、UI接线静态10项通过，未将这些静态检查当作真机证明。当前 Launcher PID6537日志未见FATAL、ANR、VerifyError或Fatal signal；全设备 crash buffer 中旧 media.swcodec 崩溃不当作 Launcher 新崩溃。
- **文件与边界**：生产修改仅 MaintainedLauncherSettingsHost.java、OriginalSearchBarCompat.java，前者改固定布局/搜索滚动，后者改设置专用背景；既有48dp高度和裁切改动保留。未改变任何图标选择、主题、光影、宫格或用户设置值；未实际提交替换图标选择。跨ROM、横屏和更大字体/显示缩放仍未覆盖，不声称全项目流畅度得到新的测量收益。源码/已安装基线、构建日志、最终 APK 和截图保存在本地 `build/icon-search-pinned-20261004/`；未暂存、提交、推送，未更新项目或全局 MEMORY.md。

**后续流畅度建议可行性复核（审计，未实施）**

- **用户约束与范围**：用户要求仔细核对优化是否有效，同时保护稳定性。本轮只复核当前代码、原APK对应clean_launcher截图路径、maintained资源／渲染参考、正式APK资源与已有trace，复跑候选回归；未修改生产代码、构建或操作／安装手机。以下区分已测收益、代码可行性与未验证效果，不能把建议写成已完成优化。
- **已实施S2收益重查**：原始settings-analysis与四个Perfetto样本重新读取。10轮正式设置样本健康检查及最后动作覆盖均通过；BACK峰值仍为7.783–12.063ms，对照基线29.171ms；inflate记录190→108（第10轮113）。S2a单独一轮BACK峰值反而32.886ms，不能把后续收益归给全部资源／异步化措施；没有单项配对实验，最终收益限定S2组合与所测设置往返。四段trace未查到MaintainedSet前缀线程记录，不据此认定迁移线程从未运行或无耗时。

| 后续项 | 复核证据与实际能改变的事 | 稳定性边界与决策 |
|---|---|---|
| 初始化迁移去重 | show(MAIN)每次安排15秒后线程；三个迁移各有持久完成标记，完成后迅速返回。去重能减少重复排队／线程，尚无帧尖峰归因证据 | 可做小范围单飞；不能永久用进程boolean替代持久标记，不能漏首次／恢复后再次需要的迁移，不能将首次磁盘读取挪到MAIN。降为后台整理，不承诺明显改善滑动 |
| 图标候选批量任务 | 已有两线程优先级池、6–16MiB按字节缓存、96项会话队列治理、request/session/generation与目标尺寸解码。一个P0 discovery仍串行load所有库候选／图标包，栅格化后完整一次发布；候选version每项还会查包信息 | 优先测真实ICON_CHOICE的排队／load／发布，考虑已有队列内分段及一次请求内元数据去重。完整列表、选中优先、稳定来源顺序、下载失败过滤、下载促进已有图标刷新、分身身份和离页取消保持。不能改成按完成顺序陆续出现，也不能删掉drawable有效性检查；减少阻塞其他任务不等于首个候选一定更早 |
| 快捷桌面读回缓冲 | vc.b每次allocateDirect(width*height*4)，GL随后copy到独立Bitmap，worker只消费Bitmap。1260×2800单缓冲约13.46MiB，加Bitmap约26.92MiB；原版也是分配后glReadPixels，已删掉旧零填充数组 | 有条件复用GL独占缓冲；不影响原版另一截图调用。只能减少分配频率，readPixels／Bitmap创建仍在，峰值与揭露收益未证明；保留缓冲会增加闲时内存，引用释放不等于原生内存立即回收。尺寸／Surface／压力失效及像素、generation必须验证，暂不引入Bitmap池 |
| 主题详情缩小原图 | 正式APK内70张delta_L/trident_L：68张626×1356、2张556×1204；手机框PNG714×1604，实际资源缩放另由density决定。详情已有后台解码及8MiB结果缓存 | 撤回笼统“大预览普遍降采样”建议；这些源图不是之前观测的1919²大图，普遍二分采样可能损失清晰度。只在实际源／目标与内存证据支持时采样，不改正文纹理、mask或图标Alpha |
| 首次主题状态、启动／Loading | 主题首扫仍MAIN以保持完整正确首屏；后台刷新复用两线程主题预览池。首帧后搜索预热也复用已有池，资源create/isPrepared同步且miss内含copy／fsync | 先测首次打开／升级／资源提取并发与队列等待。MAIN遇到资源预热的锁可能等待（代码可达，未复现长等／死锁），不能笼统说全部准备已离开MAIN；主题刷新被预览队列延后也待测。恢复DB前安全门、锁、fsync、Loading token／真实首帧／10秒失败流程保留，无证据不改等待预算 |

- **回归与验收条件**：既有候选生产方法受控平台／XML回归344项、UI接线静态检查10项通过，仅证明现有基线行为，不能证明尚未实施方案稳定或提速。候选新改动必须保持完整单次发布、排序／回退／下载副作用、应用切换／退出／包更新回调身份；截图须验证取消／Surface／内存压力／真实画面；首开预热须验证同资源竞争、HOME／锁屏与Loading前后。每项独立与相同冷热条件旧包配对，分别量排队、MAIN／GL、内存／分配与实际呈现；没有可重复收益则不保留复杂化补丁。窗口残留、触摸失灵、数据变化、错图／模糊、崩溃／ANR或持久增长任一新回归即停止该项，保留数据恢复已验证基线。多ROM零影响无法由单机／fixture保证。
- **当前结论与文件**：下一步应先补真实候选路径与资源预热竞争的时序证据，迁移去重仅做有限后台整理，缓冲复用后置，主题详情普遍降采样不采纳；稳定性集中回归与性能测量配套进行。更新本条和专项计划审核说明；项目／全局MEMORY.md未更新，无暂存／提交／推送，既有staged修改保持。

**流畅度S2后续：设置返回、主题状态与原搜索资源复用**

- **范围与根因**：接续已授权的流畅度方案，保留S1/S3与触摸归属修复。应用图标页和原搜索共用的资源入口每次新建AssetManager／Resources并查询自身包信息；主题两组adapter分别扫描安装状态，首次poll再次扫描，格子绑定还可能查询DownloadManager；设置Activity返回MAIN则反复inflate。已核对当前Owner、原APK的clean_launcher资源／ThemeChooser、maintained参考，沿用现有资源Owner、SettingsHost、OverlayHost和预览队列，不更换原动画或页面结构。
- **S2a修改**：OriginalQuickSearchResources只缓存一项资源数据，每次仍创建当前Context包装与独立Theme；自身APK路径／长度／时间、完整Configuration／DisplayMetrics及提取文件状态均参与失效。资源升级提取在临时文件完成copy／fsync后rename发布，失败不发布缓存。真实桌面首帧之后借已有IconPreviewRepository队列预热，未绕过恢复守卫或Loading首帧token。主题首次准确状态只扫描一次并共享给两组adapter；后续poll借已有主题executor查询，MAIN绑定，保留1000ms轮询周期；离页取消排队任务，已运行的迟到结果经owner／Handler／Runnable身份门丢弃。首次主题扫描仍在MAIN以保留完整正确首屏，未宣称已经完全异步化。
- **S2b修改**：扩展已有MAIN缓存到同一个ThemeChooserActivity已离场页面，返回重绑设置值；当前页面仍附着的快速返回沿原重建路径，完整配置／密度变化则失效，销毁按匹配owner清理。Launcher overlay原有“新会话且pages为空”的条件保持。只复用MAIN，不缓存图标、权限、密码、备份等状态敏感页；原scroll／back／session及180ms子页、260/220ms主入口动画不变。复用新增配置快照是原缓存缺少失效条件所需，没有新增Manager／Service。
- **正式设备对照**：vivo V2458A／Android16、经典蓝普通主题12宫格，同样20秒协议，每轮两组主题→MAIN、应用图标→MAIN、翻页动画→MAIN。实际基线APK8D877A…（保留同期赞助页更新）、S2a包280D28…与最终S2a+S2b包分别采样；基线与S2a各一轮，最终包10轮，共每个目标页20次打开及返回。页面截图核对正确标题／当前主题／图标列表，动作Activity身份与时间线完整，无data_loss／overrun。错误起始页或手机被操作打断的试采不计入结果。

| 正式样本 | MAIN doFrame最大ms | BACK分发最大ms | inflate记录数 | 含App Deadline Missed的ThemeChooser帧 |
|---|---:|---:|---:|---:|
| 保存的实际安装基线 | 35.366 | 29.171 | 190 | 14 |
| 只实施S2a | 22.839 | 32.886 | 186 | 11 |
| S2a+S2b第1–5轮 | 28.214／28.305／23.556／27.371／17.359 | 11.426／8.291／8.701／9.013／8.556 | 各108 | 6／4／2／6／6 |
| S2a+S2b第6–10轮 | 21.333／27.509／23.027／18.174／21.705 | 12.063／8.134／9.516／7.783／9.120 | 108／108／108／108／113 | 7／4／5／6／4 |

- **结果解释**：复用后BACK处理峰值7.783–12.063ms，基线29.171ms；inflate记录明显减少。doFrame仍波动，Buffer Stuffing、Display HAL、Prediction Error与App Deadline Missed分开统计，不用混合计数宣称全项目FPS或零卡顿。基线只一轮，不能将最终10轮包装成10组基线配对。目标页所测收益支持保留补丁，其他路径不能据此验收。
- **功能与隔离验证**：生产资源Owner在Android app_process隔离目录下完成434项资源共享／独立Theme／语言字体方向夜间与密度／升级／提取失败／文件丢失／并发检查；直接提取生产方法的受控JVM主题状态23项、MAIN owner／附着／快速返回／配置失效／销毁67项通过，fixture不代替真实平台完整矩阵。真机另核对隐私密码验证页（未输入密码）、强迫症、状态栏、搜索手势、快捷桌面设置打开／返回，五次MAIN滚动位置bounds一致；快捷桌面实际打开→原搜索输入edge显示Edge结果→清空→退出，Folder打开时桌面／Dock／投影全隐藏、外部关闭恢复均有实际画面。未修改用户主题、宫格、开关、密码或布局。
- **产物与文件**：标准build.bat、apksigner verify、16KiB zipalign、aapt2 badging、保留数据安装及安装APK拉取hash一致；v1.5.8/code33，SHA256 `DB2C5CF79F051C5CDEDC3DDC88F7E88A4FC5C43DC76001977D3C0CA7C009BE99`。所测Launcher PID11261 crash buffer为空，进程日志未见FATAL／ANR／VerifyError；全设备旧media.swcodec崩溃未当作Launcher新崩溃，也不声称全设备crash buffer为空。生产文件为OriginalQuickSearchResources.java、MaintainedLauncherSettingsHost.java、LauncherSettingsOverlayHost.java；新增tools/tests/settings_resources下四个probe／入口文件，本条及专项计划已更新。基线、源码备份、trace、脚本、截图和安装APK保留在本地build/fluency-s2-20261004/。未更新项目／全局MEMORY.md，未暂存／提交／推送，同期赞助页及其他既有改动保持。
- **未验边界**：主题下载安装／卸载恢复、真实配置变化与内存压力、开关改值重进、所有设置子页／权限系统页、overlay完整动画矩阵、五次冷进程／真实重载Loading、20宫格／更多主题／跨ROM仍未完整验收。S1b缓冲、S4候选预览、S5其余启动Loading项尚未实施；本轮不扩大页面缓存，不用固定等待或缩短动画补偿，保留专项计划后续阶段。

**快捷桌面与单页／多页触摸归属修复**

> 本条“一律排除概览13／10”的模式限制已于2026-10-05撤回并纠正：原版多页首页本来允许进入快捷桌面。以下现场与历史测试记录保留，不作为当前入口行为；现行实现及验证见10月5日记录。

- **用户现象与现场**：用户明确该问题在此前版本已出现，普通单页和多页都可能发生，锁屏再解锁恢复；不能直接归因于本轮优化。现场进程29432仍存活，未见FATAL／ANR，InputDispatcher为enabled且未冻结；截图显示多页概览，窗口与输入dump却存在1260×2800的可触摸快捷桌面PopupWindow。其最后日志为一次打开释放后target=1，后续点击不再进入RootView。这是本次捕获的触摸窗口冲突，不能推断所有历史单页失灵均为同一原因。原onLauncherStopped清理窗口，与锁屏可恢复的现象吻合；未把锁屏当作修复手段。
- **先恢复基线**：保存现场截图、进程／窗口／输入和故障APK，再保留数据安装已保存的0598DD…基线，截图确认桌面及Folder可用后才继续。基线同样允许在概览右滑触发快捷桌面，证明模式资格缺口早已存在；基线未复现相同不可见窗口卡死，不据此归因。最初两组测试结束在主题设置页，后续排除；不能把注入成功或安装成功当功能PASS。
- **原版Owner核对**：对照原APK的clean_launcher RootView、J、Eb和view/b/fa；J.Ta只返回Activity可交互标志ng，并非页面模式资格。Eb.isEditMode仅表示图标编辑，概览时也可能false；当前px.Dl读取显示模式hH，普通十二／二十对应12／9，概览对应13／10。原RootView的j(MotionEvent)继续拥有SMEngine触摸派发，maintained参考不替换该链。
- **最小修复**：复用QuickDesktopController，在候选DOWN、原RootView请求前、背景就绪及窗口显示前检查当前显示模式，仅普通12／9且非图标编辑可揭露；模式变化后旧截图不能覆盖概览。RootView不合资格时继续原页面派发。快捷桌面实际接管一次拖动后，其UP统一沿已有RootView取消路径向原引擎发送CANCEL，避免同一UP又完成原桌面翻页／按下状态；宿主本身仍按原进度和速度决定打开或关闭。原阈值、动画时长、曲线、图标／光影和主题资源不变，无新增Manager或随机延迟。
- **真机有效采样**：用户暂停手动操作后，正式包进程20096完成普通单页20组快速左右滑动；截图确认仍为桌面，后续能继续切页。随后10组逐组回首页的快捷桌面打开及动画中连续反向滑动，日志为10次实际request／10次背景应用／10次引擎释放取消，各组最终close-release target=0；最终输入窗口列表无全屏PopupWindow，保留的input channel不算活动窗口。文件夹实际点开、外部关闭正常。多页概览20组边缘反向滑动，20次模式13拒绝、0request／0capture／0window；另一次完整左滑截图确认换到下一概览组，双指退出回普通单页正常。主题预览→HOME→快捷桌面→关闭→Folder亦有实际截图，未应用新主题，最终返回普通桌面。这些路径未用锁屏或重启来恢复，不能等同长期零复现。
- **隔离与产物验证**：production Controller的83项资格、普通12／9、概览13／10、Folder8、图标编辑、模式中途变化、UP归属及迟到背景检查通过；production Capture的9项generation检查复跑通过。标准build.bat、apksigner verify、16KiB zipalign、aapt2 badging、保留数据安装及安装APK拉取hash一致；v1.5.8/code33，SHA256 `84F06AADC57E99F3D6DD23E71759E1EB63B222706BDE6ED843F047AFDA57FF7A`。所测正式进程crash buffer为空，未见FATAL／ANR／native fatal／VerifyError／模式读取失败；git diff --check通过。
- **文件与证据**：本次追加生产修改为`RootView.smali`与`QuickDesktopController.java`；扩展`tools/tests/quickdesktop/QuickDesktopCaptureGateProbe.java`及fixture入口`run_capture_gate_probe.py`，沿用现有generation probe。现场、恢复、有效／无效采样和安装校验产物留在本地`build/swipe-freeze-20261004/`。本条及专项计划更新，项目／全局MEMORY.md未更新，既有staged文件保持，未暂存／提交／推送。
- **风险边界**：实际20宫格、透明／毛玻璃、图标编辑拖放、长时间随机触摸、系统面板打断、锁屏与跨ROM完整矩阵仍待补足；用户历史单页冻结未在本轮捕获同样完整的故障链，保留此不确定性。此前S1/S3性能样本仍按其原范围有效，不能用本次触摸修复宣称全项目流畅度方案完成。

**流畅度优化首批实施：快捷桌面截图触发与多页比例校正**

- **范围与产物**：用户授权开始执行并允许操作手机；在既有 dirty 工作区上保留全部 staged 修改，未暂存／提交／推送。本地基线 APK `0598DD95FDD8DF48EE52AF497AE47A38E597E176E7F0DA688DED0AB2022CBF2E` 与相关源码已保存到 `build/fluency-s1-20261004/baseline/`。最终正式 APK SHA256 为 `3BF81D29ECD21E033874232949C1E512FE2EC90D2BAE75DA3316AB83FA1CA827`，v1.5.8 / code33；已保留数据安装 vivo V2458A / Android16，拉取已安装 APK 后 hash 一致。临时 `OVERVIEW_ICON_ASPECT` Trace 包装已移除，再走标准构建并验证正式包，手机最终停留原桌面。
- **S1a 根因与修改**：ACTION_DOWN 提前刷新内容并申请整屏读回，普通点击／Folder／多页操作即使不打开快捷桌面也付出分配与截图成本。DOWN 现在只记录候选；复用原版 RootView 单指、方向、J.Ta()、sLeftScreenEnabled 允许分支的 requestShow，确认后只准备一次。onProgress 回调移入原允许链且依赖已取得的截图资格；不改变原手势阈值、Ad、派发和动画参数。背景处理完成后才揭露宿主窗口，避免空背景先出现再替换；后台模糊分辨率、锐利层和原参数保持。
- **S1a 竞态保护**：在 GPU 读回前领取具体 generation，onGlFrame 携带同一编号；取消、第二指、HOME／detach 后旧读回只丢弃自身结果，不能领取新手势的 pendingHost。新增短状态锁仅保护请求发布／领取／取消，GPU／worker 不在锁内。沿用现有 Controller／Capture／Host，无新增 Manager／Service。
- **S1a 实测**：正式包 Folder 连续20次正确打开／点击外部关闭，另一次截图检查，均无 capture 请求；3次快捷桌面打开为3请求、3背景应用。多页20次双向切换无请求；快速打开、ACTION_CANCEL、反向取消、揭露后第二指的真实注入路径及截图已检查。录屏抽帧检查背景交接，Folder 打开时桌面、Dock 和投影均隐藏，退出恢复，当前日历／时钟位置正确。主题／应用图标／翻页设置前进返回、HOME、重新打开快捷桌面、点击其搜索栏进入 OriginalQuickSearchActivity 及返回，共13个窗口状态检查通过；这不等于所有设置子页或竖滑搜索入口均验收。
- **S3 新证据**：只消除误截图后，多页 GL CPU 尖峰仍有45.77–58.53 ms，不能将其算作 S1 的帧率收益。临时区段定位到 preserveOverviewIconAspect：四次切换687次调用共158.492 ms，四个长帧内该方法分别占33.994／44.670／35.997／43.345 ms；重复枚举继承方法与字段是实际热点。对照原版 SceneNode、Constants、clean_launcher 几何合同及 maintained 参考，继续使用现有兼容 Bridge。
- **S3 修改**：复用 PIXEL_GRID_METHODS，以已确认的引擎签名按需取得 Method，缓存类的字段元数据；不再枚举数百个继承方法。比例校正复用此缓存，但每次仍读取当前 page_width／height 和节点 scale，原计算、sc[0]/sc[7]、弱引用校正记录及 ActiveIcon 重绑判断保持。只缓存 Class／Method／Field，不持有 Activity／View，不缓存最终比例、位置或一次场景结果。优化后同类诊断样本684次调用共3.916 ms，最大单次0.087 ms；诊断数据与正式性能数据分开。

| 20秒正式 Perfetto 样本（同设备、蓝色普通主题、12宫格、相同双指动作） | 完整 GL 帧 | GL CPU 最大值 ms | CPU >33.33ms 帧数 | 误截图请求 |
|---|---:|---:|---:|---:|
| 已保存基线，2组进入／退出 | 1239 | 52.999 | 4 | 4 |
| 正式优化包，第1轮2组 | 1218 | 28.011 | 0 | 0 |
| 正式优化包，第2轮2组 | 1198 | 15.161 | 0 | 0 |
| 正式优化包，第3轮2组 | 1198 | 13.751 | 0 | 0 |
| 正式优化包，第4轮2组 | 1198 | 13.963 | 0 | 0 |
| 正式优化包，第5轮2组 | 1198 | 14.897 | 0 | 0 |

- **性能解释**：正式包5轮共10组／20次切换、6010个完整 GL 帧；切换尖峰下降且所测 >33.33ms CPU 长帧消失。统计按 sched 与 onDrawFrame 的重叠计算实际 GL CPU，不是呈现 FPS／GPU 时间。普通帧 p95 为5.311–5.971 ms，基线5.552 ms；p99 为6.803–7.439 ms，基线6.470 ms，不宣称全局 p95／p99 改善。采样无 data_loss／overrun；最后输入及其后帧均落在完整 trace 窗口。基线只有一轮正式对照，不将5轮优化复测包装为5轮基线配对。
- **平台／构建检查**：production Controller 在真实 Android MotionEvent／VelocityTracker 下、受控 Host／Capture 的16项触发／释放／HOME／关闭检查通过；production Capture 的9项世代领取、读回期间取消与新请求保护检查通过。直接运行构建生成的 production Bridge dex，71项十二／二十引擎模式、继承字段、精确 overload、重复不累积、ActiveIcon 重绑及尺寸变化检查通过；fixture 不替代实际20宫格迁移验收。新增回归入口在 `tools/tests/quickdesktop/run_capture_gate_probe.py` 和 `tools/tests/geometry/run_overview_probe.py`。
- **最终验证**：build.bat、apksigner verify、zipalign -c -P16、aapt2 badging、保留数据安装、安装 hash 校验及 git diff --check 通过。正式进程29432的 crash buffer 无记录，所测日志无 FATAL／ANR／native fatal／VerifyError／OVERVIEW_ICON_ASPECT_FAILED／STATIC_ICON_PIXEL_GRID_FAILED。实际截图与记录保留在本地 `build/fluency-s1-20261004/`，采错场景的 earlier samples 不计入结果。
- **文件及边界**：生产改动为 RootView.smali、vc.smali、QuickDesktopController.java、QuickDesktopBackgroundCapture.java、LauncherSettingBridge.java，另补回归脚本／fixture及本计划文档。F01–F15、光影参数／向量、主题资源、图标来源和原版动画不变。S1b缓冲复用、S2设置／搜索资源与转场、S4候选／预览、S5启动／Loading尚未实施；S1a/S3完整矩阵也未全部验收。实际20宫格、透明／毛玻璃、不同倍率、拖动归类／垃圾桶、冷启动多轮、50次内存往返及跨ROM仍待验。本轮收益限定已测路径，不宣称整个项目已优化完成。项目及全局 MEMORY.md 未更新。

**流畅度优化完整方案（方案阶段，未实施）**

- 用户要求制定完整方案并保持正常功能。本轮复核当前代码、原版RootView／clean_launcher、maintained主题设置参考及既有审计证据，将完整S0–S6顺序、Owner／文件范围、功能保护、性能目标、回归矩阵和回退流程写入 `LAUNCHER_FIX_AND_OPTIMIZATION_PLAN.md` 顶部2026-10-04章节；与旧启动阶段／F01–F15编号分开，不重复已完成修复。
- 新确认的施工限制：现有RootView.onProgress兼容回调位于原版单指／J.Ta()允许门之前，不能直接将DOWN截图搬到onProgress就算解决。第一项必须同时做到非快捷桌面零读回、原版手势归属保持、真实揭露前背景连续；不能用固定延迟、模糊／光影降级、缩短动画或移除稳定性门换帧率。
- 只更新计划、开发记录及索引说明；无生产代码／资源／Manifest修改，无构建／安装或手机操作。本地正式APK hash复核仍为0598DD…；既有dirty改动保留。方案尚未实施，冷启动／Loading／搜索／20宫格／跨ROM的未验范围不转为PASS，项目及全局MEMORY未更新。

**全项目流畅度复审（仅审计，未修改生产代码）**

- **基线与范围**：在 HEAD `912fd89a38d185444935bc146d6c52032b309d58` 的现有 staged／unstaged 工作区上复审，保留全部已有改动。当前本地正式 APK 与 vivo V2458A / Android 16 已安装 APK 的 SHA256 均为 `0598DD95FDD8DF48EE52AF497AE47A38E597E176E7F0DA688DED0AB2022CBF2E`。全量风险检索覆盖 131 个 Java、3712 个 Smali，另清点 233 个原版资源 XML（`launcher/unknown/res`）及 435 个设置资源 XML；检索命中数量不是 BUG 数量，也不代表每个文件完成语义／真机验收。
- **深读范围**：启动／HOME／解锁、12/20 与多页模式、PageWithRenderTarget／SMEngine、Folder／Dock、设置共用转场、主题／壁纸、应用图标／候选／缓存、搜索／IME／索引／历史、快捷桌面／媒体／背景、天气／日历／感应投影、安装／分身／角标、备份／恢复／Loading。对照 original APK 对应 clean_launcher 及 maintained 的设置／主题加载参考；原版动画、图标资源、主题参数、投影向量和 F01–F15 保护保持。
- **真机采样**：得到完整 20 秒的两次双指收拢／展开（单页↔四页）Perfetto 样本，1195 个完整 `onDrawFrame`；四个切换窗口分别出现约 48.7／49.1／47.6／52.8 ms 的 GL 长帧。相应 GL 实际 CPU 运行约 48.2／48.6／47.6／52.3 ms，单个长帧内 dequeueBuffer 只有约 0.2 ms，故这些尖峰不能用常规 VSync 等待解释；尚缺 Java／native 方法栈，不能直接指定唯一 Owner。普通稳定帧的 GL CPU 多为约 3–5 ms，`onDrawFrame` wall time 包含 buffer 等待，不是 GPU 工作时间或最终显示 FPS。
- **设置采样**：真实 `MAIN→THEME_LIST→MAIN→ICON_LIST→MAIN→PAGE_FLIP→MAIN`，对应 ThemeChooserActivity 的 84 个 FrameTimeline surface frame 中，9 个 `App Deadline Missed`、12 个 `Buffer Stuffing`、4 个 `Display HAL`、59 个 None；各类含义分别保留，不合并为应用 CPU 卡顿率。主线程最重 `Choreographer#doFrame` 32.65 ms、布局 23.42 ms、单次 inflate 28.55 ms；一次 1919×1919 位图解码 45.54 ms 在 `pool-9-thread-1`，48.07 ms GC 在 HeapTaskDaemon，均非主线程暂停时长。此样本验证设置 Activity 路径，不宣称 overlay／所有子页均已实测。
- **Folder／翻页采样**：打开／关闭文件夹、左右翻页及普通桌面空白点击，观察到约 28–36 ms 的 GL wall time 尖峰；只统计 Launcher foreground 对应的 GL 区间。末尾搜索动作没有进入搜索 Activity，剔除该段，搜索入口／IME仍未完成本轮动态验收。

| 优先级 | 证据与问题 | 最小优化方向及保护边界 |
|---|---|---|
| P1 | `QuickDesktopController.onTouch` 在符合桌面区域的 ACTION_DOWN 即执行 `schedule(root,host,0)`；普通点击、Folder 开关、翻页乃至双指刚按下都有 `QD_BACKGROUND_GL_CAPTURE_REQUEST`。普通点击已得到 `QD_BACKGROUND_APPLIED sharp=1260x2800 blur=240x533`，即快捷桌面没揭露也完成整屏截图与模糊。 | 优先收口已有手势 Owner 与截图触发条件，排除普通点击／反向翻页／Folder／多指；保留快捷桌面揭露前画面、坐标、generation／取消门及原版手势归属。不能简单延迟截图造成揭露时背景跳帧。 |
| P1 | `vc.b` 每次 GL 截图均新建全屏 DirectByteBuffer 和 ARGB_8888 Bitmap；1260×2800 下仅两者约 26.9 MiB，另外有 worker 缩小／模糊工作。多指取消发生在 MAIN，GL 已开始读回时仍会支付分配和 readPixels 成本。 | 先消除误触发，再审计现有 capture Owner 的缓冲复用和生命周期；不创建第二截图 Manager，不任意改成低清锐利背景。四个多页长帧与该链时间相关，但唯一方法根因仍待短时方法栈／分段标记验证。 |
| P1 | 设置往返仍重复 inflate／构造／首次 measure/layout。共用 `setSettingsContentView` 对新旧整页启用硬件层，下一帧启动 180 ms 动画；布局／图标回调可能落在同一动画帧。已有主页面缓存只覆盖 Launcher overlay 新会话，不能覆盖本次 Activity 往返。 | 先缩减首帧绑定与重复布局；评估单会话复用已有页面或快照，重绑设置值并保持 owner／session／back／scroll／attach 门。评估整页硬件层建立成本，保留原版转场外观／时序，禁止直接缩短动画掩盖卡顿。 |
| P2 | `alignStaticIconPixelGrid` 在 Cell.draw 中逐帧运行，仍读取反射字段、遍历父链、做 native corner 投影及分配 float[12]／varargs；`preserveOverviewIconAspect` 在模式绑定中重复枚举方法／读取相同模式几何。 | 在已有 helper 内缓存 Method／Field 与线程内 scratch，按主题／模式／尺寸／Surface／动画变化正确失效；保持静止 1:1 像素对齐、动态几何与多页圆形比例。未证明它独占四个长帧。 |
| P2 | `OriginalQuickSearchResources.create` 每次建立 AssetManager／Resources／Theme，并查询自身包更新时间；升级后首次提取还在调用线程 copy／fsync。应用图标页搜索栏与搜索 Activity 共用该入口。 | 复用现有资源 Owner，按 APK 更新时间／Configuration／density 缓存和预热；只包装当前 Context，不能静态缓存 Activity。设置资源已有 `scheduleSettingsResourcesWarm`，不得重复新增预热 Manager；也不能声称每次打开都复制 APK。 |
| P2 | 主题两个 adapter 构造分别 `themeEntriesFor` 查询安装状态，紧随的 polling 又查询状态并对两个 adapter notify；有下载记录时 getView 仍可能查 DownloadManager。现有 getView 资源 ID／安装缓存和后台预览解码已经保留。 | 同次页面会话共用安装／下载状态快照，安装广播／下载变化按相关条目失效，保持回调身份和实际数据新鲜度；不恢复旧的逐格 PM 查询。 |
| P2 | 图标候选和可见预览共用现有两线程优先级池；候选任务一次扫描图标包并产生所有预览后才发布。后台仍可能加载远大于目标的源图（本次观测1919²）。缓存／取消门已存在。 | 测量候选队列等待和源图内存预算，优先可见条目并复用已有元数据与预览缓存；不把已有后台解码误报为 MAIN 解码，不替换图标来源／Alpha／尺寸契约。 |
| 安全门，先测量 | 启动前 `RestoreRecoveryGuard` 仍同步等待恢复 writer 文件锁／读取 durable journal，异常恢复可含 rollback／清理。Loading 依赖 UI 调度和实际首帧交接；weather geocoder join 在搜索 worker 内，搜索历史 commit 在 diskExecutor，不能据关键字认定阻塞 MAIN。 | 单独测量 IDLE 冷启动、恢复竞争与真实恢复路径。必须保持数据库初始化前事务安全、首帧 token、GU 向量原子交接、UNKNOWN保留；禁止统一把 commit 换 apply、移除锁、缩短 Loading 超时或删原版 mipmap。 |

- **证据文件**：`build/performance-audit-20261004/source-inventory.json`、`overview-complete.pftrace`／动作时间表、`settings-complete.pftrace`／动作时间表、`folder-search-complete.pftrace`／动作时间表、`trace-analysis.json`。早期动作误入其他 Activity／长按单图标及 buffer 太小导致动作前半段丢失的样本不计入结论。当前 APK 非 debuggable／profileable，shell 方法采样被 Android 拒绝；没有为审计改 Manifest 或安装诊断包。
- **验证／风险**：采样后 Launcher PID 保持20189，按该 PID 过滤 crash buffer 未见 AndroidRuntime／native crash。本轮仅新增审计产物和本记录，未修改生产代码／资源、未构建或覆盖安装、未改变主题／宫格／快捷桌面偏好；无性能改善或全项目验收声明。冷启动／Loading／解锁、真实搜索和完整快捷桌面进入、20宫格、更多主题、低内存、后台竞争及跨 ROM 仍待性能验收。项目 `MEMORY.md` 与全局 memory 未更新。

**关于我们 Power by 赞助卡片**

- **原因与范围**：用户要求将“使用小技巧”替换为赞助名单，并删除其后所有技巧分组。页面由 MaintainedLauncherSettingsHost.showAboutPage 加载 setting_about_us → setting_tips_view；原 APK 对应 clean_launcher 没有该新增技巧布局，maintained 的关于页只有 logo／关注我们。沿用当前页面和现有单卡片背景，不新增 Java owner 或改桌面逻辑。
- **修改文件与效果**：launcher/tools/maintained_settings_res/res/layout/setting_tips_view.xml，以及 values/strings.xml、values-zh-rCN/strings.xml；新增 launcher/tools/java/com/smartisanos/home/settings/SponsorNoteTextView.java。当前没有随TextView自然换行绘制记事本横线的控件，因此仅新增局部TextView子类，以实际Layout基线和字体高度绘制浅灰横线及空白行，不新增页面／Manager。标题严格使用“Power by”；名单为“@夏尔美、@星辰、@幸福的街角、@287266982”，便签卡片下方独立灰字为“感谢以上锤友赞助支持，排名不分先后”。名单连续排列并自动换行，复用上方蓝色文字的 more_item_right_color_bg／setting_item_text_copyright_size（13.5dp），与外部分组标题16dp区分；记事本横线随实际文字行绘制，仅在名单后保留两行空白；取消固定最小高度与弹性留白，后续增加姓名仍可扩高；原技巧的所有 include 和后续分组标题从此页面移除。上方 logo／关注我们保留。
- **验证**：标准 build.bat 成功，v1.5.8／33；v1／v2／v3签名、16KiB zipalign检查通过。保留数据覆盖安装 vivo V2458A／Android16 成功，最终真实关于页截图及UI树确认蓝色小字号的连续四位姓名、一条文字横线加两条空白横线、卡片外下方的新感谢文案及完整圆角，未显示旧技巧分组；本轮读取的AndroidRuntime日志为空。证据为 build/power-by-build.log、power-by-about.png、power-by-nav.xml。未提交／推送，保留既有暂存和工作区改动。
- **风险与文档**：当前屏幕与中文字号已实测；更多姓名自动换行、超大系统字体和其他ROM尚未真机验证。仅更新本日志，MEMORY.md未更新。

**应用图标搜索与单应用多图标包候选**

- **修改文件**：MaintainedLauncherSettingsHost.java、IconPackManager.java、IconPreviewRepository.java、RedirectIconDB.java、SmartisanInstallManager.java、OriginalQuickSearchActivity.java、OriginalSearchBarCompat.java；新增 AppIconCandidate.java、AppIconSearchIndex.java、OriginalQuickSearchResources.java、tools/tests/app_icon_candidates/AppIconProbe.java 与 run_tests.py。所有 Java 均在 launcher/tools/java 现有包下；本记录更新于 DEVELOPMENT_LOG.md。没有修改桌面 Smali／渲染资源。
- **真实入口与原因**：审计 main 的 ThemeChooserActivity.smali → MaintainedLauncherSettingsHost.show → item_id_icons → showIconPage → AppIconAdapter，以及原 APK／clean_launcher 设置行、现有 QuickSearch 资源和 maintained 参考后修改。原替换候选只包含当前全局图标包且加载／轮询混在 Adapter；搜索没有页面内索引。现有 DEFAULT／IMPROVED／PACK／CUSTOM／RESOURCE owner、动态图标及最终桌面几何不变。
- **搜索**：复用 OriginalSearchBarCompat／OriginalSearchEditTextCompat／qs_original_search_bar.xml，将已有资源 APK 加载代码抽为 OriginalQuickSearchResources 共用，不复制 drawable、颜色或尺寸。页面可管理应用来自现有 IconManager／RedirectIconInfo 集合，后台分组时一次构建 AppIconSearchIndex；按 displayName／packageName／componentName trim＋Locale.ROOT 不区分大小写过滤，输入不触发 PackageManager 扫描。空查询恢复分组；非空只显示搜索结果与原列表 Item，点击仍进入原替换页，无结果灰字提示。未新增拼音算法。
- **最终视觉**：以本日“应用图标页搜索固定顶部与锤子圆角资源复用”为准：搜索固定在标题下方，复用 `sub_item_back_ground_single.9.png`，不叠加系统投影；有效关键词收起设置 header，清空后可滚回设置。原先随列表滚动的胶囊背景与淡投影方案已被取代，不作为当前实现。第三方包名10sp灰字，单行 END 省略，不撑大格子。
- **候选链**：新增不可变 AppIconCandidate 元数据，来源包括既有 component／system alias／本地图标／variants／在线镜像和所有 getIconPackPackages 检出的包。IconPreviewRepository 既有 worker／session 执行 collect → stableKey去重 → 当前候选优先／包名稳定排序 → 一次提交；IconPackManager 既有 appfilter XML／assets解析和显式 getPackedIcon 验证有真实对应 Drawable 才加入。Adapter 只绑定候选／预览与既有点击操作。Pack 写入仍为 RedirectIconDB.updatePackIcon → forceUpdateIcon → applyIconChanges／Launcher AppIconUpdate／分身刷新，不改 IconSourceManager 全局选项。
- **线程与缓存**：新增 getRedirectIconMetadata 避免获取模式时解码自定义图；大图预览在原仓库执行器栅格化并复用字节限额缓存。候选元数据最多8页且总权重256；图标包映射继续保留全局当前包＋最多2个额外包。解析移出全局锁，主线程缓存访问不会等待后台 appfilter；generation／session／请求票据丢弃旧结果，取消页面移除刷新闭包。安装／卸载仅淘汰对应包映射，后台刷新有效页面和引用该包的覆盖，普通应用安装不会清空全局已加载映射。
- **回退**：保存的 pack:<package> 已卸载时，单应用来源、桌面 source type／identity、设置预览均回到当前全局来源；全局包本身失效时继续走既有原图回退，不写新全局值。CUSTOM／RESOURCE／动态天气日历／系统 alias／分身／在线缓存／阴影材质／感应光影／倍率与12／20宫格的所有权未迁移。原全局样式切换主动重置非 CUSTOM 覆盖的规则保持原样，测试组合是在选定全局后再设置单应用 Pack。
- **构建与自动检查**：标准 build.bat 成功，v1.5.8／33；签名 v1／v2／v3 与16KiB zipalign 检查通过。tools/tests/app_icon_candidates 的受控 Android 边界执行实际生产解析／候选／搜索／回退／数据库逻辑：344项生产检查、10项静态 UI 接线通过，覆盖0／1／3＋／20包、重复 action、assets／XML、失效映射、持久化重开、缓存容量、解析竞争及 session取消；这些不等于 Android UI／帧率验收。audit_icon_contract.py 通过，既有 settings_session 33项及生命周期检查通过。
- **真机证据与边界**：vivo V2458A Android16／1260×2800安装成功。Edge搜索仅Edge并进入正确页、QQ搜索显示QQ／QQ音乐、包名搜索／无结果／清空回分组已检查；真实 Smartisan OS＋两个临时测试包同时出现，重复THEME action无重复候选，长包名省略。全局DEFAULT／IMPROVED／Pack A后设置Edge Pack B均显示对应预览；冷进程／覆盖安装后Pack B仍置顶勾选。全局Pack A＋QQ Pack C桌面立即变为测试图标，卸载C后同一桌面恢复A图标且无空白，未重启Launcher；测试包B/C已卸载，全局恢复IMPROVED。性能日志候选收集为pool线程。长时间滚动帧率／堆增长、完整50／100／150％和12／20宫格、天气日历／小程序全矩阵未做真机量化，不能标为全部通过。本轮不更新 MEMORY.md，保留任务开始前已有暂存／工作区改动，未提交或推送。

**Dock 感应投影透明矩形深度遮挡（2026-10-03—04）**

- **根因与原版对照**：原版 CellOnDock.draw 调用 db(false) 为 sc[27] 恢复含深度测试的投影状态；MutiTexMaterial 的全透明片元也未 discard。相邻投影矩形在当前 Dock 中重叠，同深度 GL_LESS 会使前一矩形的透明区域挡住后一阴影。10 月 3 日在独立 Mali GLES／24bit depth 探针复现，透明前矩形使后投影 Alpha 总量减少约67%；仅关闭投影深度测试后与单独绘制参照逐像素一致。这是隔离证据，正式路径由本轮同机前后截图继续验证。当前 Dock 绘制／投影初始化方法已对照 clean_launcher、clean_launcher_raw 和 maintained；前两者原方法一致，maintained 仅作状态 API 参考。原版天气预设定义、选择与 opacity getter 保持相同，21组 blur Alpha 完全一致、九姿态 GPU Alpha 最大差异1/255；没有把偏淡未经测量归因为移植时调低参数。
- **最小修复**：生产文件仅 launcher/smali/com/smartisanos/launcher/view/a/ca.smali，在既有 db(false) 之后、d(Camera) 之前为非空 sc[27] 调用 setIsEnableDepthTest(false)。每帧继续先走原版状态初始化；其他 Scene 重绑定仍走原 f/db 初始化，不新增 Manager、shader、缓存或尺寸逻辑。静态 Dark／Light／Transparent 阴影、mask Alpha、天气／光照／握持算法、图标大小、层级和动画资源均不改，尚未额外增加投影透明度。
- **构建与设备**：标准 build.bat、ICON_CONTRACT_STATIC_AUDIT、v1/v2/v3 签名、16KiB 对齐通过，版本仍 v1.5.8/33。保留数据安装 Android16／vivo V2458A 成功，最终 APK SHA256 5BF81C96433D1B485D6FBA62D11BB0EE1DE9B9D325CD54B5231474AEE7F1D8BF 与手机 base.apk 相同。相对已安装基线，APK zip条目仅 classes.dex 与签名文件改变；classes2.dex、资源、native、Manifest 相同。用户已有暂存／工作区改动均保留，未暂存、提交或推送。
- **真机效果与基本回归**：蓝色主题1260×2800前后截图确认企业微信左下竖直截断消失，原 x372/373 切边在 y2660 RGB 跳变量由(-9,-14,-24)降至(0,0,-1)，y2670／2680同样消除明显台阶。企业微信和便签正文、空白背景的所列 ROI RGB 零差异；其他含透明边缘的 ROI 仍有感应投影差异，不宣称全屏零差异。桌面设置 Activity 进入／返回通过；真实保持 Dock 电话长按期间截图看到原垃圾桶与 Dock 收拢，松手取消／BACK 后位置恢复，PID13662持续存活。最新 exit-info 为本次 PACKAGE UPDATED，没有新增 crash 退出；crash buffer 保留历史异常，安装后时间范围未见新 AndroidRuntime／FATAL，旧记录不算本轮新异常。
- **证据与风险**：build/dock-illumination-fix-20261004/ 保存构建／签名／对齐、前后／长按截图、APK条目差异及像素结果；前期原版／GPU审计在 build/dock-illumination-audit-20261003/。本轮验收限定当前蓝色主题、当前布局和姿态；橙色／透明／毛玻璃主题、12/20 切换、Dock与桌面拖动迁移、手持多姿态、其他倍率与ROM仍待实际回归，不能把本次完整显示称为与原版全场景强度一致。更新本日志，未更新 MEMORY.md。

### 2026-10-03

**专项编号与进度纠正／F05跨进程补充验收（未修改生产代码）**

- **施工进度**：本次专项以 FULL_REGRESSION_STABILITY_AUDIT 的 F01–F15 为准。F09–F15 已在前面的集中处理轮实现／审计；F10 是快捷桌面 draw 快照消费，不能与旧启动计划“阶段10：安装、卸载、角标和分身”混用。后续F05两项清理及writer补验应记为补充验收，不作为倒退阶段或重新编号的下一阶段。专项文档增加当前状态表，已实现、已验证范围和待统一回归项分别列明；不重复修改F10，不将全部实现处理完成当作完整设备矩阵完成。
- **本轮已完成证据**：新增 RestoreLeaseProbe.java、run_lease_probe.py，run_device_tests.py增加隔离编译入口。Android16使用真实OS锁／AtomicFile／JSON／MAIN，导入和偏好为受控边界。11种情形、111项宿主和69项原生检查通过：writer正常完成后守卫重读终态不重复导入；7种未完成状态下隔离writer退出后回滚一次；COMMITTED／CLEANING退出不重复导入。持锁期间不推进守卫、日志及归档保持，释放后MAIN继续且锁可再获取。仅终止已校验身份的隔离夹具进程；Launcher PID16638前后相同，未触碰真实桌面数据。
- **保护与风险**：本轮生产代码未改、未重新构建／安装／截图，设备与本地APK仍为0DB246…，五个视觉保护文件哈希不变。人工持锁约一秒的时间不代表真实恢复／最坏HOME预算；完整SAF恢复／撤销、生产故障点、OEM／跨ROM和持续帧预算仍待统一验收。证据在 build/f05-restore-lease-20261003/。更新本日志和专项审计；MEMORY.md未更新，未暂存／提交／推送。

**F05 后续：启动旧备份清理移出 MAIN（实现、Android 16 隔离与正式包基本路径通过）**

- **根因与原链**：`ja.1.onCreate` 在原 DatabaseProvider 初始化前调用 RestoreRecoveryGuard；Guard 先同步执行 DesktopBackupController.cleanupInterruptedBackup，再进入必要的恢复 writer／日志安全门。旧备份清理包含 staging 递归删除、SAF 提供器删除 partial document、偏好 commit 与备份日志 reset。用保存的实际旧方法摘录和真实 Android MAIN／AtomicFile 复现提供器删除发生在 MAIN；提供器边界为受控替身，不冒称真实云端卡顿或实测帧耗时。原版 APK 对应 clean_launcher_raw、clean_launcher 和 maintained 中无等价移植备份事务清理入口；继续复用当前 Controller／OperationLock，不新增 Manager／Service，不改原版初始化顺序。
- **唯一生产文件与行为**：仅 `launcher/tools/java/com/smartisanos/launcher/backup/DesktopBackupController.java`。现有公开清理入口预留原 BackupOperationLock，后台 `DesktopBackupCleanup` 执行原清理主体，完成／异常后释放；其他操作已有 Owner 时不清理其正在生成的备份，重复入口不会派发第二个在途任务。使用 application Context，未置入 running／prepared 状态或改变取消／预览 UI。IDLE／COMPLETE 保留、PREVIEW_READY 不提示失败、其余未完成状态写 last_backup_incomplete、SAF 失去权限时的原静默删除策略及 reset 顺序全部保留；源码对照确认原清理主体及其余 Controller 方法完全相同，仅入口派发变化。
- **安全与验收**：RestoreRecoveryGuard、恢复 journal、OS writer、原 DatabaseProvider 接点完全未改；真实恢复／回滚仍在原数据库初始化之前串行完成，不能为了响应速度绕过它。旧备份清理仅操作自身 staging／partial document／备份日志与提示偏好，不导入桌面数据库／主题／图标。新增 `tools/tests/restore_worker/BackupStartupCleanupProbe.java` 和 `run_backup_cleanup_probe.py`，实际摘录当前及任务前方法，生产 BackupOperationJournal／BackupOperationLock／BackupFileUtils 配合真实 Android 16 Looper、JSON、AtomicFile 和文件执行；提供器和偏好为受控边界。新版112项检查覆盖全部备份状态、受控提供器阻塞期间 MAIN heartbeat、新操作互斥、重复入口、活动备份不被删除、权限撤回、原提示规则和完成释放；Launcher PID12784在隔离检查前后不变。既有122项恢复线程／进程锁、144项恢复日志故障检查继续通过，但这些检查中旧备份 Controller 为替身，不将其称为完整真实备份→恢复证明。本轮只有 Android 16 连接，未补报 Android 9 新清理路径实测。
- **构建、安装与保护**：标准 build.bat、v1／v2／v3签名、16KiB对齐、v1.5.8／33及diff检查通过。保留数据安装 V2458A／API36，设备 APK与本地产物SHA256一致：`0DB246F07097C3B9E46B05235C76CE2394AD090E4DF0007DCE7C7AB43F4F8DD2`。启动、桌面设置进入／返回原首页完成；PID16638错误日志未见 FATAL／VerifyError／ANR／SecurityException／native Fatal signal／新增清理失败日志，但有限日志不等于全生命周期验收。相对上一阶段998968…包，仅classes2.dex与签名条目变化；资源、Manifest、classes.dex、native未变，今天五个视觉保护文件哈希不变，电话／系统设置／桌面设置三个静态采样区域RGB最大及平均差异均0。未重新完整切主题／宫格矩阵，未改变其代码与参数。
- **风险与证据**：启动前恢复守卫仍可能等待正在写库的另一进程，最坏 HOME／启动耗时、真实完整SAF恢复／撤销、断电、存储满和跨ROM仍未闭环。提供器长期不响应时，桌面 MAIN 不等这次清理，但备份／恢复操作门仍等待其结束，未添加任意超时／强行并发删除；last_backup_incomplete在后台完成后持久化。原备份日志失败处理及 reset-before／after-delete规则没有在本项重新设计，不将后台迁移称为故障原子性修复。证据保留 `build/f05-startup-backup-cleanup-20261003/`：任务前源码／APK、baseline／native、构建／签名／保留验证、安装包／运行日志与 static-pixels.json。已更新本日志和专项审计，MEMORY.md未更新；未暂存、提交、推送或清理用户文件，原暂存／工作区保持。

**F05 后续：恢复首帧收尾移出 MAIN（实现、Android 9／16 隔离验证及 Android 16 基本路径通过）**

- **根因与范围**：冷重载 Coordinator 在 Choreographer 的 MAIN 首帧回调中调用 `DesktopRestoreController.onLauncherFirstFrame`；旧方法同步执行 journal 读取、CLEANING／IDLE 的 fsync＋回读、staging／apply／撤销包递归删除，然后显示成功。保存任务前实际 Controller，并用生产方法夹具复现：方法返回前日志已重置、staging 已删除。这证明主线程同步收尾，不是实际帧耗时测量。检索原版 APK 对应 clean_launcher_raw、clean_launcher 和 maintained，未发现等价移植恢复事务入口；沿用现有 Controller／OperationLock／首帧通知，不替换原版初始化、Loading、数据库或主题链。
- **最小修改**：本阶段唯一生产文件 `launcher/tools/java/com/smartisanos/launcher/backup/DesktopRestoreController.java`。首帧只提交一个 `DesktopRestoreCleanup` 后台任务；同 token 重复首帧不重复派发。任务预留现有 BackupOperationLock 操作门，避免收尾期间新撤销重用 `rollback_latest`，并持已有 OS writer lease 后重读 token／终态。仍先持久化 CLEANING 和 IDLE，再删除临时文件；普通恢复保留撤销包，撤销完成才删除它。成功／具体日志失败／写锁失败经原 MAIN Handler 显示原 toast，仅成功普通恢复启动既有图标补源。使用 application Context，不持有设置 Activity；其他恢复、数据库、线程 Owner 与非恢复重载路径不改。
- **故障与并发验证**：扩展现有 restore_worker／restore_journal 测试，共五份测试源码／脚本；新增占用 writer 时 MAIN heartbeat、新撤销被挡、重复首帧、CLEANING／IDLE 失败不删源／撤销包、不提前成功、stale token、等待锁期间 journal 被替换、非终态与另一操作 Owner、回滚结果和 MAIN toast 检查。122 项生产线程／进程锁检查、144 项事务故障检查、13,131 项设置读取／恢复监听器回归通过。真实 Android 9 X21A 与 Android 16 V2458A 各通过 57 项平台 IO／权限、7 项导入 worker、13 项新首帧收尾、6＋6 项 checkpoint SIGKILL 重进及4 项未完成 AtomicFile 写入重进，共各93项；真实 Looper 响应、writer 等待、重复结果、权限错误保留和 MAIN 回调通过。archive／布局转换／UI／偏好仍为受控边界，这些检查不等于完整真实桌面恢复；SIGKILL 仅作用于独立探针。
- **正式包与真机**：标准 build.bat、签名 v1／v2／v3、16KiB 对齐、v1.5.8／33 和 diff 检查通过；SHA256 `998968DC94CD05C51863AEAD4412420BFC79FA72ADB97E9972875F31D19A1C35`。X21A 在 install-r 期间断开，停止其等待中的安装命令，未将该尝试记为安装通过；新连接 V2458A 经核对为 API36、已装本项目 v1.5.8，保存旧包后保留数据安装成功，设备 APK 与本地产物 SHA 一致。Android 16 启动、设置进入／返回、快捷桌面揭露／关闭并返回原首页已完成；最终经典蓝／12 宫格，原已开启的快捷桌面开关保持。PID12784 错误日志未见 FATAL／VerifyError／ANR／SecurityException／native Fatal signal，但不能据有限日志声称全生命周期无问题；本轮未重新完整切主题矩阵，也不把连续横滑命令记成已逐页验证的完整翻页性能。
- **视觉保护与证据**：今天 Bridge／Raster／Cell／Eb／光照材质五个保护文件哈希与 F09 开始快照相同；本轮 APK 对比上一轮 F5F329… 包，仅 classes2.dex 与签名条目变化，资源、Manifest、classes.dex、native 不变。Android 16 安装前／设置与快捷桌面返回后的系统设置、电话、桌面设置三个静态采样区域 RGB 最大／平均差异均0；未改图标大小、Alpha、纹理过滤、主题参数、垃圾桶／Dock 或 GL。证据保留于 `build/f05-first-frame-cleanup-20261003/`，含任务前 Controller／APK、native／native-16、签名、设备安装包、关键终态与 static-pixels.json。
- **未关闭项与文档**：启动前恢复守卫仍同步等待 writer／执行必要回滚，最坏 HOME／启动阻塞和 ANR 风险尚未量化，不能异步绕过数据库安全门；主线程旧备份清理也未在本阶段迁移。真实完整 SAF 备份→恢复→撤销、生产故障点断电、存储满、用户 UID 与 OEM 分身、持续帧预算仍未验收。保留原 reset 后删除的顺序，删除中进程退出可能遗留临时文件，未新增清理事务或宣称所有磁盘故障原子完成。已更新本日志和专项审计后续状态；MEMORY.md 未更新，未暂存、提交或推送，用户已有改动／暂存保持。

**F09–F15：剩余审计项集中处理与统一回归（已测范围通过，不等于全 ROM／完整恢复／帧性能验收）**

- **F09 根因与最小修复**：原 Sensor 经 H→Ra.k 写 GU 的三个分量，GL 的 Qa.run 经原 a/c.b→a/j.x 逐分量复制方向；事件队列的发布锁不保护随后发生的 GU 改写。Android 隔离屏障以原生产方法复现混合姿态 `(1,-5,6)`，既不是旧输入也不是新输入。Ra.k 写 GU 和 Qa 复制 GU 共用该向量 monitor，异常释放锁；入队、球面投影、Scene 更新、材质和原 Y 取反均留在原路径，锁外执行。原版 APK 对应 clean_launcher_raw 的 Ra.k 与修改前一致，Qa 与干净参考一致；clean_launcher 不含对应 Ra 文件，不能声称已比较不存在的文件。maintained 没有等价原版渲染链。新增实际摘录／组装 Smali 探针在 Android 9／10 通过 23,011 项，含确定性交接、20,000 次并发压力和异常释放。这里只确认并修复共享向量问题；注册／Scene 世代、真实队列积压、手持倾斜和完整动画性能仍未验收，不给 pooled n 贸然加任务名或改原队列。
- **F10／F11**：QuickDesktopHostView 延后创建现有 ContentView，关闭／从未揭露时不再解码固定图片；第一次原横滑揭露前同步创建完整内容，原资源、比例、RootView 手势和背景交接不变。ContentView 的 onDraw 消费卡片开关、天气／日期／签名、支付图标和媒体快照，不再查询媒体服务／偏好／PackageManager。音乐查询由可见期间的单一 HandlerThread 执行，至多一个查询在途，MAIN 按 generation 接收；关闭／detach 停止定时刷新、退出线程，旧结果不写回。80／180ms 控制后刷新和 1s 可见刷新保留，media-key 临时状态增加 volatile 可见性。平台媒体查询 RuntimeException 明确日志并使用无歌曲信息的快照。首次揭露解码和低频配置读取仍在 MAIN，没有宣称第一帧／Binder 耗时达标。探针曾发现首次打开重复启停导致两次查询，已修正后重跑；12 项实际 Android View／Looper／Bitmap 检查通过，80 次绘制不触发媒体／偏好读取，关闭停止轮询、旧结果拒绝及禁用音乐卡不查询通过。受控媒体／天气／动作边界不算真实 MediaSession 全矩阵；相同受控内容的原／新版 RGBA 所有像素 0 差异。
- **F12／F13／F14**：恢复 READY 回调增加 `prepared == ready` 身份门；Host 的恢复监听器只弱持有 Activity，复用 attach／detach，销毁时脱离，旧监听器、新选择和非备份／恢复页面均不能更新全局进度或打开预览，页面归属消费已有 SettingsBackEntry。模型 snapshot 异常／null／非 Map 返回 UNKNOWN，首次安装门保留已有项，包级删除停止；正常空 Map、主用户／分身／特殊项保持原语义。Host 相同四来源 boolean 读取委托既有 LauncherSettingBridge.readBool，未改 Bridge 或 int／string 规则。新增／扩展生产方法测试：布尔来源冲突／非法类型／异常与恢复回调 13,131 项、Model 188 项、恢复线程／旧 READY 替换 74 项通过。恢复验证中离开页面、销毁和重新选择有隔离检查；未将真实完整恢复 UI／SAF／桌面重建补报为 PASS。
- **F15 判定**：源码／Smali、Manifest／资源、构建入口检索未发现 openFromDesktop 的正式调用，旧覆盖层仍有 Launcher／Host 的生命周期、返回和窗口辅助引用，全部 Java 继续参与构建。动态外部反射不能由文本检索排除。保留 DEAD_CODE_SUSPECTED，本轮安全删除 0 行；未恢复废弃覆盖层，也未为“全部优化”强删兼容代码。
- **集中回归与设备范围**：`build/final-regression-20261003/` 保存 19 组本地脚本与 10 组 Android 隔离批次结果，均通过；最后增加页面归属门后只重跑受影响的 13,131 项监听器／boolean 与 74 项恢复线程检查。覆盖卸载身份／取消原动画、查询未知保留、下载失败、备份偏好、搜索缓存、设置会话／底部手势、解锁状态机、主题阴影／透明交接、恢复日志失败、SQLite 页面槽／分身／pending 重试、安装调度、Sensor 交接与投影缓存。Android 隔离重跑分别含 83 项 Profile、120 项页面、17 项 pending＋3 项重进、39 项安装 worker、43 项 Intent、477 项缓存、788 项生命周期和 23,011 项感应交接；夹具 SIGKILL 不作用于用户 Launcher。原版 Smartisan 仅用于隔离比较，未替换原版桌面。
- **正式包与真机结果**：标准 build.bat、签名 v1／v2／v3、16KiB 对齐、badging v1.5.8／33 和 diff 检查通过。保留数据安装 vivo，最终设备 APK SHA256 与本地一致：`F5F3295077335F446A6A01A4179966E026D913B3A8E5DA18035177E2FB6EA298`。16EE6B… 的集中真机路径包括经典蓝→经典黑→毛玻璃→经典蓝、快捷桌面首揭露／关闭／音乐控制视图、快捷桌面进入搜索并以 `dian` 匹配电话等应用、设置返回；F09 正式包另已完成透明开关、12→20→12、感应开启下主题切换并恢复关闭。最终 F5F329… 包只补 Host 的恢复页面归属门，重新安装后启动与设置返回通过，最终经典蓝／12 宫格／感应关闭，临时开启的快捷桌面恢复初始关闭。未将中断前尚在确认框的最终宫格重切当作额外完成。按正式 PID 的错误日志未见 FATAL／VerifyError／ANR／SecurityException；信息级日志有限，不能据此证明无所有生命周期问题。测试探针的早期断言不算 Launcher 崩溃。
- **视觉、文件与边界**：相对 F09 开始快照仅变更 Ra.smali、Qa.smali、DesktopRestoreController.java、LauncherModelRepository.java、QuickDesktopContentView.java、QuickDesktopHostView.java、QuickDesktopMediaBridge.java、MaintainedLauncherSettingsHost.java。今天图标清晰度／完整 Alpha／编辑等比／垃圾桶时间步长的五个保护文件 SHA 全部不变；最终 APK 相对 F09 已安装包只有 classes2.dex 和签名条目改变，资源、native、Manifest、classes.dex 相同。所测静态电话／设置区域未再次软化，缓存八层仍遵守前期零差异证据。还未覆盖：完整真实恢复／撤销与断电、OEM 分身卸载补恢复、授权 MediaSession／微信支付来源、持续四指／手持光影／完整性能与其他 ROM／倍率。F05 启动守卫和首帧清理预算也仍有验收边界；本轮处理完成不代表所有审计风险永久关闭。新增相应隔离探针，更新本日志与专项审计；未更新 MEMORY.md，未暂存、提交或推送。

**F08：投影缓存失效、版本校验与内存容量收口（实现／隔离 Android 检查与 vivo 基本回归通过）**

- **根因与范围**：F07只补了提前命中的八文件存在／非空门；原 Aa.b(ItemInfo)／E(String) 删除PNG时不清 MASKS，非零损坏文件仍可命中，VERSION未验证磁盘结果，进程Map也无上限。另以当前及原版APK对应 clean_launcher_raw／clean_launcher 确认：Aa.F(String) 从文件取绝对路径后 startsWith(packageName)，普通包名实际匹配不到；Android旧生产方法负例已复现。maintained的 HolographicOutlineHelper 没有可直接复用的原版八层缓存适配器。本轮复用 IconIlluminationCompat 与 Aa 四个现有清理入口，不改数据库、Package/Profile路由、Composer、材质、传感器或GL。
- **生产文件与清理 Owner**：仅 `launcher/tools/java/com/smartisanos/launcher/theme/IconIlluminationCompat.java`、`launcher/smali/com/smartisanos/launcher/Aa.smali`。原 C（下载占位）、E（精确key）、F（包级）、b(ItemInfo) 的重复文件循环委托给现有投影 Owner；b继续使用原Pe，主用户／分身／组件身份不重写，C由统一入口添加layer分隔符，最终文件名与原版一致。生成和清理共用既有类monitor，关闭功能时也清理缓存。精确key只删该key；包级使用 packageName＋下划线边界，仅处理八层PNG／临时PNG和新增索引／临时索引，保护相似包名与其他文件。包级清理包括同包派生缓存，不删除应用、数据库或源图。任务前四个原清理方法与raw原版完全一致；其余Aa方法文本在任务前后完全一致，包括原生成／模型业务链。
- **容量与磁盘复用**：同一个 MASKS 改为最多256条的访问序LinkedHashMap，仍用弱Bitmap引用；淘汰只移除内存记录，不删原GL可能仍在使用的PNG。原shadow目录每key保存一个约200字节 `.projection` 索引，记录格式magic、现有VERSION、源图尺寸／density／hasAlpha／premultiplied、完整Alpha SHA-256及八层长度／CRC32。新进程或内存淘汰后只有源签名、版本、元数据与八层CRC全部一致才复用；无索引、旧版本、截断／尾随数据、缺层和损坏都重建。PNG名称、256px、140px正文、全Alpha、SIGMA及读取路径不变，没有第二个缓存目录或Manager。
- **提交与故障边界**：重建前移除旧内存条目及旧索引，索引失效失败就停止后续重写；八层PNG全部写完且源revision稳定后才用临时索引rename提交，部分PNG失败不留成功索引。不支持读取Alpha或源在生成期间变化时不记录可复用索引。八层已完成而可选索引写入失败时保留PNG、明确日志、不记录内存命中，下次保守重建；Linux文件名上限夹具已验证此路径。索引不是用户数据事务日志，没有新增fsync承诺：进程中断／不完整数据由下次校验再生成处理。热命中检查长度／mtime；mtime变化只触发CRC复核，不据mtime证明同图。新进程／淘汰重入必验CRC；相同长度且mtime也被保留的进程内外部改写不在热门的完整覆盖范围，不能声称持续逐帧校验PNG。
- **Android隔离检查与旧版负例**：新增 `tools/tests/icon_illumination/ProjectionLifecycleProbe.java`、`run_lifecycle_probe.py`。使用完整生产缓存／Blur、实际摘录组装的四个Aa方法及原ItemInfo.Pe，Android Bitmap／Canvas／PNG／File／CRC／monitor真实执行，Application／偏好为独立夹具。旧F07生产Owner＋旧Aa复现清理后留内存条目、包级路径不匹配、非零坏PNG误命中与Map超过256条。新版788项通过：主／分身／组件、禁用状态清理、下载占位key、相似包名与无关文件保护、冷源Alpha变化、同尺寸同时间戳损坏文件的冷CRC拒绝、热损坏／非零截断PNG、截断／未知版本／尾随索引、临时提交、权限式失效阻断及修复、索引可选失败、300个真实write入缓存、访问提升／淘汰不删PNG、淘汰后复用、实际Aa清理与写入monitor串行。新进程复用、只改VERSION的独立dex拒绝旧索引、夹具删除索引／制造未完成PNG后SIGKILL及重进修复通过；该SIGKILL是中断派生缓存夹具，不是声称在生产compress指令某一点断电。Launcher PID20181在隔离检查前后不变，没有操作用户桌面缓存。
- **像素／相关回归／性能边界**：F07既有477项真实Android缓存／像素检查仍通过；当前Owner实测192px来源的八层PNG与旧F07完整生产Owner输出逐字节相同、RGBA0差异。58项生产主题／缓存、24项Smali三态切换与ICON_CONTRACT_STATIC_AUDIT通过。F07探针本轮热write中位同revision0.206ms、新Bitmap同Alpha0.871ms，含新增文件有效性门；不是Launcher帧耗时、分配量或冷启动收益。本轮没有重跑／补报原版手持倾角验收；原21组native／九GPU姿态证据仍属于F07记录。冷CRC／大量包清理IO预算、整桌面compose频率与最大等待未测。
- **今天修复与正式包**：五个视觉生产文件（Bridge／Raster／Cell／Eb／光照材质）前后SHA256全部不变；APK相对任务前仅classes.dex和classes2.dex变化，资源、Manifest及native库不变，正式dex无IconPixelAudit／EditGeometryAudit／两个缓存探针。标准build.bat、v1/v2/v3签名、16KiB对齐、v1.5.8／33及git diff --check通过。保存旧安装APK后保留数据install -r成功，新设备base.apk与产物SHA256均为 `8C8AD016E9C45B75D9C93B64BC8A3EE3F8DCC187FA7A266E83B199E638E2A90C`。启动、12宫格编辑／退出、进入设置／Back、左右翻页并回原页已截图验证；原页面／主题／12宫格／默认桌面保留。电话仍192px正文：安装前RAW采样MSE0.000463／Y半像素模型33.9573（top1959），安装后及返回RAW0.000532／Y半像素模型33.9697（top1958）；只有当天已记录的1px整数相位边界，未发现重新插值软化。编辑圆形仍90×90px，系统设置返回与安装后逐像素一致。PID21749持续存活，按该PID日志未见FATAL／VerifyError／ANR／SecurityException／投影失败；设备仅保留有限错误级平台JDWP／BackgroundFallback／memtrack记录，不能据此称全生命周期无问题。
- **风险与后续**：实现及所列隔离／基本路径完成；真实系统卸载重装后原模型／GL纹理重绑、手持投影、跨ROM／Android16、20宫格重切与其他倍率、完整垃圾桶／拖动动画、磁盘满和生产故障点断电尚未闭环。内存容量已有硬上限，PNG／索引磁盘仍沿正式key／包清理保留，不新增盲目清理正在使用文件的磁盘配额。失效后首次重建仍有原同步生成成本；CRC为派生文件完整性校验，不是恶意修改防护。下一阶段F09 Sensor／GL线程与生命周期专项，原传感器链保持不动；原15项审计统计继续作为第一轮快照。证据在 `build/f08-projection-lifecycle-20261003/`，新增两份探针、更新本日志和专项审计；未更新MEMORY.md。本轮未操作暂存、提交或推送；工作期间观察到前序改动已有暂存，保持原样，F08新增／增量仍留工作区。

**F07：投影缓存命中前移（实现、隔离像素检查及 vivo 基本回归通过）**

- **根因与最小范围**：旧 IconIlluminationCompat.write 在查询缓存前已经 extractAlpha、绘制 256×256 mask 并分配 int[65536]＋byte[65536]，数组本身至少320KiB；命中只省掉八次模糊和PNG。本阶段仅修改该现有 Owner，原版 APK 对应 clean_launcher／clean_launcher_raw 的 Aa 全 Alpha、140px正文投影到256px、八层SIGMA契约保持。maintained没有可直接复用的同链适配器；没有新增第二个阴影缓存、Composer、线程或Manager。
- **修改行为**：同一个 MASKS 条目记录弱 Bitmap 引用、generation及尺寸／density／hasAlpha／premultiplied／输出目录；修订和元数据相同时在 raster 前命中。不同 Bitmap 先逐行读取完整源Alpha做SHA-256，用 width 级数组替代命中前的256² mask与数组，签名／元数据一致才复用；RGB变化不改投影，Alpha变化仍重建。getPixels不受支持时保守进入原有raster路径，不据包名／文件mtime猜同图。force始终重建，重建前移除旧成功条目，来源修订变化时不记录成功缓存。命中前检查八个文件存在且非空，避免缺层、零长文件和部分重写失败后误报完成；这只处理本次提前命中必需的有效性门，F08的版本、正式失效通知、条目上限／跨进程索引仍待下一阶段。
- **今天修复的保留证据**：用户明确不得影响 STATIC_ICON_PIXEL_GRID_AND_ORIGINAL_ALPHA／OVERVIEW_ICON_ASPECT_AND_TRASH_ENTRY。记录并复核 LauncherSettingBridge.java、IconRasterDiagnostics.java、Cell view/a/g.1.smali、Eb.smali、光照材质 g.1.smali 的任务内前后SHA256，五个文件均完全一致。以安装前F06正式APK对照新包，签名之外仅 classes2.dex 变化；classes.dex、图标／主题资源、Manifest、原SMEngine和native库全部逐条目不变。IconPixelAudit／EditGeometryAudit／ProjectionCacheProbe 未进入正式dex。静态正文无缩放过滤、1:1叶节点相位、电话192→192→246→屏幕192px、完整静态Alpha、编辑比例补偿和 held 时间步长限制都保留。
- **隔离 Android 检查**：新增 tools/tests/icon_illumination/ProjectionCacheProbe.java 和 run_cache_probe.py，完整生产缓存 Owner／Blur，真实 Android Bitmap／Canvas／PNG／文件，Context与偏好为隔离夹具；vivo X21A／API28通过477项检查，涵盖140／192／256源图、任意Alpha／透明边缘、新Bitmap同Alpha、RGB变化、Alpha变化、force、缺层／空文件、density／hasAlpha元数据、回收、弱引用、换输出根及部分IO失败后修复；与强制生成的八层输出逐像素一致。原版锤子 DT1902A 与vivo的既有native／GPU探针重跑：21组原版模糊Alpha零差异；九姿态GPU Alpha最大差异≤1级、平均<0.03。58项生产主题／缓存、24项Smali主题三态切换、ICON_CONTRACT_STATIC_AUDIT通过。
- **性能证据边界**：同机隔离write循环预热60次，五组各40次取耗时中位数；旧版同Bitmap修订命中10.266ms、新版0.131ms，新Bitmap同Alpha旧版10.204ms、新版0.792ms。后者交替使用两个已预先创建的Bitmap，排除Composer／源图构建成本。只证明本探针热命中减少raster工作，不代表桌面帧耗时或冷启动改善；一次完整冷生成旧219ms／新251ms不能作性能结论。早期ART全局bytes-allocated读数不能反映本例大数组的可靠逐调用分配量，已从最终探针移除，不引用为“实测减少多少字节”；320KiB来自实际旧数组尺寸和新版提前返回分支。未测真实compose频次／各调用线程预算。
- **正式包与真机路径**：标准 build.bat（自动选择SDK37工具）、v1/v2/v3签名、16KiB对齐、v1.5.8／33和git diff --check通过。保存已安装APK后 adb install -r 成功；设备与产物SHA256均为 F5AB925054AD8253C155084866EBB50D893A0F0F9A769C10A190A49B3D4DCAED。启动、十二宫格编辑／退出、设置进入／返回、左右翻页并回原页完成；PID20181持续存活；当前截图的电话完整192×192正文区域、系统设置和桌面设置192×192区域相对安装前RGB差异0，十二宫格编辑圆形正文仍90×90px。编辑退出／返回后电话与当天已有记录相同出现1px整数Y位移，不能继续按固定裁切坐标写成RGB零差异；按实际位移对齐后中心120×120区域相对安装前MSE0.000255，全192px区域MSE0.1723（最大RGB差4级），与未插值源图的中心MSE0.000463，纵向半像素平均模型MSE33.9573，未支持再次软化；已另存返回路径证据，未据此改节点／过滤。保留数据／默认桌面／宫格与主题，没有执行恢复或卸载；按新PID20181采集日志未见FATAL／VerifyError／ANR／SecurityException，但仅有错误级平台JDWP／BackgroundFallback／memtrack日志，不能据此证明全生命周期安全。
- **文件与剩余风险**：生产代码仅 IconIlluminationCompat.java；新增两份上述隔离探针，更新本日志与全项目专项审计的后续状态。证据在 build/f07-projection-hit-20261003/。弱引用不持有Bitmap像素，但条目较旧Integer增大，key累积上限仍属F08；非零损坏PNG、版本变更、缓存清理正式通知／磁盘空间和并发来源改图仍需继续审计。F09 Sensor／GL交接未改；本轮未做手持倾斜可见光影验收、20宫格重切／其他倍率与ROM、完整垃圾桶／拖动动画性能，不能用隔离像素PASS补报。今天已有20宫格与动画证据仍保留原边界。未更新 MEMORY.md，未暂存、提交或推送。

**F06：待安装补恢复复用串行安装线程与失败重试去重（实现／隔离运行及桌面基本回归通过）**

- **根因与复现**：SmartisanInstallManager 已有 HandlerThread，但 attemptOriginalPackageAdd 将 pending JSON／PM／DB／AtomicFile 操作放进 MAIN Runnable。完整旧生产 InstallManager 在 Android 9 独立 app_process 中复现 MAIN 补恢复。PendingItemRestoreHandler 在 DB 提交后再更新 JSON，后者 EACCES 时保留旧 pending；基线生产代码重试得到两份同身份数据库行，负例 `BASELINE_PENDING_DUPLICATE_REPRODUCED rows=2`。另一个中断窗口是派发标记被持久化，重启继续当作已派发，从而跳过后台处理中断的事件。
- **最小修改与文件**：本阶段生产改动仅 `launcher/tools/java/com/smartisanos/launcher/install/SmartisanInstallManager.java`、`backup/PendingItemRestoreHandler.java`、`backup/RestoreMergePlanner.java`（后两者位于同一 Java 包根）。两个 attempt 调用者仍为已有 worker 任务，firstInstall 判断与 Package／Profile／Model 门不改，补恢复在发 MAIN 通知前同步完成于 worker；原 Aa.c 通知、非首次安装／替换保留行为、下载图标清理仍在 MAIN。重载已持久化安装事件时仅重置上一进程的 dispatched，再走原判断，不盲目重发 ADD。Pending 在同一 DB 事务内读取该包现有行，以既有 RestoreMergePlanner.stableKey 按 user／组件／类型／shortcut id 判断，已经提交和批内重复身份计为已解决，不重新插入／占格；DB 成功后才消费 JSON。仅将现有 cursorRow 开放包内复用，没有新增身份转换器、Manager、状态 enum、数据库 schema 或线程。
- **原版与参考边界**：对照原始 APK 对应 clean_launcher 的 Aa.c → DatabaseUpdater Action.aaa 及当前相同入口；通知仍沿原数据库／模型派发，不复制原私有系统逻辑。maintained 未提供当前 pending helper 或可直接替换的原版安装兼容链，因此直接复用当前 InstallManager 的串行调度；保留最近静态图标／编辑态比例／垃圾桶时间步长等工作区改动，没有触碰图标、动画、主题或 Smali。
- **隔离设备验证**：新增 `tools/tests/pending_worker/`，完整生产 InstallManager 配合受控包／Profile／Model／补恢复边界，真实 Android HandlerThread／MAIN 上39 项通过：阻塞 worker 时 MAIN 心跳、补恢复完成前不通知、交替用户的10 个 burst 事件、重复回调、替换／changed／已有模型不重加、旧派发重判与已表示条目重放不 ADD。扩展现有 RestorePageProbe／restore_profiles runner，实际生产 Pending／Exporter／Importer／Planner、Android SQLite／AtomicFile／JSON 上17 项通过，覆盖 JSON EACCES 后 DB 已提交、持续失败不重复、修复后消费、位置保留、批内重复、同包不同用户／组件／类型、shortcut id 与 bridge 迁移、quiet Profile、DB trigger 故障及修复；probe SIGKILL 后新进程重试另3 项通过。120 项页面槽测试中两处原样重写相同身份的“新批次”改为不同组件，仍检查原容量和连续批次边界；120 项页面、83 项恢复身份、141 项事务、70 项恢复 worker、95 项卸载目标回归通过。设备为 vivo X21A／API 28；隔离阶段 Launcher PID 17281，安装后重跑 Pending 的 PID 19088，均前后保持。
- **正式包与基本真机回归**：用户本轮明确授权必要真机测试；保存已安装 APK 到 `build/f06-pending-worker-20261003/before-install.apk` 后 adb install -r 成功，未清数据／改默认桌面／安装测试 App／强杀用户桌面。标准 build.bat、v1/v2/v3、16KiB 对齐、badging v1.5.8／33 和 git diff --check 通过；最终设备 base.apk 与本地 APK SHA256 均为 `A1DF0802CD953D38059956AF5C250B91D2A620135A15ABCE302F0697C17435EF`。启动成功，进入桌面设置 ThemeChooser、Back 返回、左右翻页并回原页的截图可见完成，所见页面位置与安装前一致，运行 PID 19088 未变化。UI dump 在设置第一次返回 null，截图与 Activity 栈作该路径证据；不把这次 dump 当成功。按新 PID 采集的日志未见 FATAL／VerifyError／ANR／SecurityException，只有平台 BackgroundFallback／memtrack 等错误，日志信息级别有限，不能据此证明全部生命周期／性能安全。旧 crash 缓冲中 RestorePageProbe 的断言是前期测试夹具原样批次触发，已按真实不同身份修正并重跑通过；非正式 Launcher 崩溃。
- **风险与未验证项**：真实补恢复＋原 Aa／数据库任务的联动、实际 OEM 分身、PackageManager 广播风暴、磁盘满、快捷方式可启动性、Android 16 和其他 ROM 未做完整验收；隔离测试的 Package/Profile/Model 状态为替身。DB 与 JSON 仍不是单一事务，本项证明正向身份重试可幂等处理，没有增加自动重试策略；已被原模型表示、未经过 firstInstall 门的残余 pending 清理仍不扩展。F05 启动守卫及首帧清理预算、整份恢复数据一致性也未在本轮关闭。证据在 `build/f06-pending-worker-20261003/`。未更新 MEMORY.md，未暂存、提交或推送。

**OVERVIEW_ICON_ASPECT_AND_TRASH_ENTRY：多页面编辑图标压扁与长按垃圾桶进入跳帧修复，vivo 真机通过所列路径**

- **范围与原版依据**：用户明确“压扁，不是感应光影”。本轮对照原版APK对应的 `clean_launcher_raw/`、`clean_launcher/` 和 maintained，复用既有 Cell 模式切换、PageWithRenderTarget、长按共享时间线。当前 `animations/lb.smali`（TrashAnimation）／`animations/U.smali`（DockViewAnimation）与两份原版参考逐字节一致，普通页面 `view/v.1.smali::Sg()` 和Dock `view/l.1.smali::Sg()` 长按方法与原版一致；页面文件另有既存文件夹回位兼容hook，不能称整个文件完全相同。maintained `CellStatusForPage.handleLongPress()` 也将 TRASH_APPEAR、RELAYOUT_BY_LONG_PRESSED、CELL_NARROWED 加入同一条时间线后start。垃圾桶原版沿Y轴移动 `trash_display_height`，时长0.2f、曲线编号14，没有新增或重绘动画资源。
- **压扁根因与修改**：vivo十二宫格普通页面1080×1768，编辑页519.875×808，实际最终父节点scaleX=0.48136574、scaleY=0.45701358，Y/X=0.9494099；离屏texture中的正方形正文被最终页面纵向压缩约5.06%。叶节点JNI角点属于离屏页面，必须再乘最终PageWithRenderTarget比例，不能只据离屏246×246判断没有压扁。原版与maintained按页面宽高分别缩放，现有Cell.Mm()/resetCellScale只处理悬浮页且相应格子比例抵消成1，未补偿当前实际视口。仅在 `Cell.Ya(I)` 模式切换后调用既有Bridge新增的 `preserveOverviewIconAspect()`：页面内静态sc[0]／ActiveIcon根sc[7]按scaleX/scaleY补偿Y，X/Z和页面、格子、位置不动；退出恢复自己的基准，弱引用记录防止反复进入累积，并识别ActiveIcon重新绑定覆盖scale。排除Dock和文件夹内容；20宫格设置值20对应引擎普通mode9、编辑mode10，12宫格为12→13，不能用mode20读20宫格几何。没有修改图标Bitmap、阴影、1.20、IconVisualMetrics、LayoutPropertyAdapter或感应光照算法。
- **进入动画根因与修改**：原版 `MainView.update()` 每次向Ra.T传固定fx，移植版为兼容既有动画速度／解锁使用真实帧间隔并归一化。Ra.T先处理InputManager与EventManager，长按在其中创建并start时间线，随后同帧AnimationManager使用已计算delta；vivo旧日志第一帧delta=120ms，垃圾桶Y从-380.84375直接到-244.12926，约94%位移，下一次即到-234.78125。缓存图标热路径反射后仍复现，不能把反射优化单独当成修复。仅在Launcher `Eb.update()` 中用原InputManager.hk()指针保持标志，实际delta超过2×fx时改为单次fx；较小间隔保留，松手／CANCEL后仍走原计时。没有重写TrashAnimation、DockViewAnimation、SMEngine或取消／成功链，没有随机延时或修改0.2f／曲线。临时节点诊断版本看到十次中间位置，正式无诊断包录像仍看到底部→部分露出→完全升起。
- **热路径开销收口**：此前清晰度修复的alignStaticIconPixelGrid每帧反复getMethods；本轮仅缓存该方法所用反射元数据，仍按原方法名／参数数选择首个匹配，像素对齐条件和结果保持不变。其他Bridge反射用户不改；缓存不是本次垃圾桶跳帧的独立解决方案。
- **正式包真机证据**：保留数据覆盖安装vivo X21A／Android9成功，真实设置十二→二十→十二切换；原像素白色圆形正文统一RGB>200探针，12宫格90×85→90×90，20宫格67×63→67×67，原宽度不变。12宫格五次进出和长按轻拖CANCEL后再次进出未见累积，最终90×90；松手／CANCEL后Dock回位、图标布局未改变。切回12后的电话120×120内部RGB与此前清晰度正式截图逐像素一致、MSE0；后续编辑退出一次产生1个整数屏幕像素的Y位置变化，按该实际位置对齐后MSE0.000255，未见再次插值软化，不能写成所有固定裁切坐标始终RGBA0变化。未实际卸载应用，本轮取消／成功系统卸载仍以此前记录为准，不能借本次进入录像补报通过。
- **文件、产物与验证**：本轮生产代码仅 `launcher/tools/java/com/smartisanos/launcher/theme/LauncherSettingBridge.java`、`launcher/smali/com/smartisanos/launcher/view/a/g.1.smali`、`launcher/smali/com/smartisanos/launcher/view/Eb.smali`。标准build.bat、v1/v2/v3签名、16KiB对齐、ICON_CONTRACT_STATIC_AUDIT、git diff --check通过。正式APK仍为v1.5.8／33，SHA256 `74B59F866ACD253C52D17503F2A8A8ED2AE7B5AF39B552C8F51546358E04F783`，已安装APK哈希相同，PID17281未见AndroidRuntime／LauncherIconShadow错误。临时EditGeometryAudit与Host诊断hook已移除，Host内容与任务开始备份相同，classes2.dex无诊断类。锤子系统Launcher只读对照／录像，未替换APK，未安装maintained。
- **证据、风险和边界**：`build/edit-trash-20261003/` 保存任务前备份、task-only.patch、original-animation-comparison.json、诊断节点日志、final-visual-evidence.json、正式截图和三个垃圾桶原像素裁切录像／GIF；只裁切物理像素，没有空间放大或锐化，VFR按时间戳重采样，不能以平均录制FPS当原始帧间隔。held指针异常delta限制也会作用于长帧中的拖动／捏合，vivo本次长按松手、轻拖CANCEL和进出模式已验，其他ROM／高刷新率／快速拖动和完整解锁动画矩阵仍待验；动态节点所有绑定时机、文件夹整体预览、全主题和50／150%编辑几何未完成专项验收。正式手机恢复12宫格；没有清数据、删应用、改在线图标／缓存版本或改主题阴影。既有其他工作区改动保留；未更新MEMORY.md，未暂存、提交或推送。

**STATIC_ICON_PIXEL_GRID_AND_ORIGINAL_ALPHA：普通静态图标两次插值及阴影 Alpha 损失修复，vivo 当前12宫格通过**

- **FIRST_BLUR_OWNER**：`LauncherSettingBridge.composeStaticIconTextureWithOriginalShadow()` 将192px正文放入246px texture，位置仍为 `(27,13.5)`；原来正文与阴影共用过滤 Paint，无尺寸变化也发生线性插值。对照原版 `data/L.a(Bitmap,IZ)` 与 maintained `HolographicOutlineHelper`，正文使用独立、明确关闭过滤的 Paint。三个受控192px输入的 source→artwork 0变化；无阴影正文探针在texture `(27,14)` 提取也0变化，真实GPU上传电话的不透明正文0变化。CPU单点修复后用户仍看出偏虚，后续诊断证实第二 Owner，不能恢复旧的“只修CPU即可”结论。
- **SECOND_BLUR_OWNER（直接测量）**：vivo X21A 的Dock实际高度409px，父节点 `view.V` 坐标 `(0,-935.5,0)`，使1:1 texture落在屏幕半像素位置。诊断包在GL线程读取实际上传texture和JNI投影角点：电话Cell坐标 `(270,0,0)`，正文叶节点原 `nodeX=0,nodeY=8,nodeWidth=nodeHeight=246.00002`，`textureWidth=textureHeight=246`；viewport为1080×2280。屏幕坐标（左上原点）`left=687,top=1944.5,right=933,bottom=2190.5`，不是GPU再次放大，而是GL_LINEAR在半像素位置再次插值。主相机为原版透视Camera（parallel=false），该叶节点实测比例1:1；不是仅按逻辑尺寸推算。
- **第二处最小修复**：`view/a/g.1.smali` 的Cell.draw在实际绘制前调用Bridge现有兼容层新增的 `alignStaticIconPixelGrid()`。只放行普通应用、无ActiveIcon、非mode8、无RenderTarget、父链静止且无XY缩放、投影尺寸与真实texture尺寸相同的叶节点；动画、文件夹、动态和非1:1路径不对齐。仅补偿不足一像素的位置相位，未改节点大小、Dock高度、LayoutProperty、Camera、TextureManager、SMEngine或GL过滤。修复后 `nodeY=8.499977`，屏幕矩形约为 `(687,1944,933,2190)`，正文边界 `(714,1958,906,2150)`，电话仍为 **192源图→192artwork→246texture→最终192px正文**。不属于源图不足，也没有电话192→256→230的生产链。
- **真机正文证据**：单独修Node相位后同源电话内部120×120区域相对未插值源图MSE从34.017917降到0.000532；修复前相对“纵向半像素平均”模型仅0.060498，修复后该模型误差33.969687。原版同区域相对未插值源图MSE为0.001088。恢复阴影、移除诊断后的正式包仍为0.000532，证明正文已接近原版采样。最终真实桌面的96×96内部区域同样不支持半像素平均模型：系统设置MSE0.004593、桌面设置0.001447、短信0.003617，均相对各自实际artwork。短信和系统设置的实际源图为256px、正常缩至192px；这些素材与原版／maintained不保证同源，不能用不同素材要求全图RGB一致。
- **阴影偏淡根因与修复**：静态compositor原来调用 `createStaticShadowSilhouette()` 删除Alpha1～127，电话／短信／桌面设置受控素材分别删除328／371／1127个非零像素；该处理来自2026-08-01的6818fce3，为避免素材自带阴影二次生成，但不等同原版。原版及maintained使用完整Alpha，阴影拷贝Paint不启用Bitmap过滤、横向居中使用整数除法。现仅静态compositor恢复上述行为，原阴影生成器和模糊不变。共享silhouette helper及动态LiveShadow调用保持原样；静态texture缓存增加专属版本后缀 `full-alpha-unfiltered-v1`，动态缓存键不变。
- **主题职责保留**：普通主题仍按 `icon_light_shadow` 选择Dark／Light，aero／trans／glime使用Transparent，半径／颜色／透明主题额外偏移和特殊覆盖均不变。原版xxhdpi Dark两层Alpha33／41、Light18／18、Transparent11／15；maintained Dark为47／63，不能照搬其更深参数。此前记录的感应投影晴天0.5／非晴天0.7和设备倾角是另一条材质链，本轮不修改，也不把它混成静态贴地阴影。
- **原版与阴影像素验证**：归档原版APK与连接锤子系统Launcher APK SHA256完全相同。隔离app_process加载原版、maintained及当前真实APK，统一输入／参数后底层生成器九组Alpha0差异；原版vendor HIGH_QUALITY与Android NORMAL测试蒙版也0差异，排除模糊算法替代为本次根因。实际新生产compositor在电话／短信／桌面设置 × Dark／Light／Transparent九组最终texture Alpha全部与原版0差异，九组不透明正文0差异；在同一Android 9上全部RGBA0差异。跨Android 9／原版Android 10仅4～20个半透明边缘RGB像素相差1级，Alpha不变，是舍入边界，不声称跨系统全部RGBA完全相同。
- **文件、构建与安装**：生产修改仅 `LauncherSettingBridge.java`、`IconRasterDiagnostics.java`、`view/a/g.1.smali`。临时 `IconPixelAudit.java` 及Host首帧hook已删除；Host内容与任务开始备份完全一致，最终classes2.dex中无诊断类。标准build.bat、v1/v2/v3签名、16KiB对齐、git diff --check通过；58项主题／缓存、24项生产smali三态切换及ICON_CONTRACT_STATIC_AUDIT通过。正式 `build/launcher-signed.apk` 仍为v1.5.8／33，SHA256 `35DE408751F721579496CE42F2348D6D857017E62727E2776BF0FF3E60C67CEC`；保留数据覆盖安装vivo成功，启动和第1／2页往返截图正常，PID11468未出现AndroidRuntime或LauncherIconShadow警告。未替换锤子系统APK、未安装maintained桌面。
- **证据与未验证边界**：证据保存在 `build/icon-clarity-20261003/`，包括实际APK隔离阴影探针、`shadow-pixel-audit.json`，以及 `node-audit/` 的上传纹理／实际节点、最终截图、`phone-final-before-original-native.png`、`final-icon-screen-fit.json`。截图只按原始物理像素裁切，没有放大／锐化；三列阴影背景和设备感应条件不同，不能仅靠截图灰度认定阴影强度。当前12宫格静态同源电话正文和受控静态阴影问题已验证；20宫格、50／150%及跨ROM、全主题实际切换、完整动画与新增反射调用帧耗时未完成验收。1.20、IconVisualMetrics、LayoutPropertyAdapter、天气／日历、文件夹及光照材质均未修改。MEMORY.md未更新，未暂存、提交或推送，其他工作区修改保持原样。

**F05：恢复／撤销主体离开主线程（实现与隔离检查完成，性能／完整恢复待验）**

- **根因与范围**：设置页 MAIN 同步 beginUndo 解包；:reload 的 MAIN 在旧 PID 退出后同步执行 archive／SQLite／偏好／图标导入和验证，会阻塞 Loading。沿用现有 DesktopRestoreController、BackupOperationLock、冷重载 Coordinator 和 Activity，不替换原版数据库、动画或任务链，不改变 F02／F03 导入算法、F04 状态枚举与持久化阶段。原版初始化接点仍为 ja.onCreate 在 DatabaseProvider 前调用恢复守卫，不能把这个前置安全门直接异步放行。
- **修改文件与行为**：本阶段生产文件为 `backup/BackupOperationLock.java`、`backup/DesktopRestoreController.java`、`backup/RestoreRecoveryGuard.java`、`reload/LauncherColdReloadCoordinator.java`、`reload/ReloadTransitionActivity.java`（均位于 `launcher/tools/java/com/smartisanos/launcher/`）。撤销接受请求后后台解包／准备，既有 Listener 返回准备结果，MAIN 交接重载；beginUndo 的 true 表示已接受，非恢复成功。重载旧 PID 确认退出后才提交单个后台导入，完成结果返回 MAIN；首次与重试共用退出门，generation／弱引用／销毁检查阻止旧回调启动桌面。普通宫格、主题和图标尺寸重载仍走既有启动路径。执行导入时暂停首帧超时，完成后重新开始原首帧等待，不把导入用时算成首帧失败，不新增 UI、状态 enum 或 Manager。
- **事务与并发保护**：现有 BackupOperationLock 增加进程内互斥和 `files/backup_restore/restore_writer.lock` 的 OS 文件锁，重载写库和启动守卫串行；锁文件不删除，避免不同进程锁住不同 inode。守卫获取锁后重新读 journal；内部恢复调用复用已持锁入口，避免重复获取 OS 锁。写锁失败停止导入、保留源／回滚文件并提示；存储修复后成功重试会替换旧失败提示。F04 检查点仍决定能否进入下一写入阶段；页面关闭仅废弃启动回调，已经开始的事务继续安全完成。没有给正在写入的任务开放并行重试。
- **验证与产物**：新增 `tools/tests/restore_worker/`，生产 Controller／Guard／Lock／Coordinator 配合受控 archive／DB／Activity／queued MAIN：旧生产 Coordinator 复现 MAIN 导入；新版 70 项检查涵盖阻塞导入时 MAIN 响应、首次／重试 PID 门、重复提交、撤销解包、失败重试选回滚、销毁／结束／取消后的旧回调、启动失败、非恢复重载和启动守卫竞争；Windows 子进程真实 OS 锁正常退出／强杀后释放通过。141 项事务故障检查、95 项卸载目标检查再次通过。扩展 F04 Android 探针，vivo X21A／API 28 通过 46 项平台 IO／权限、7 项真实 Handler／Looper 后台回调、6+6 项 checkpoint SIGKILL 重进及4 项未完成 AtomicFile 写入重进，共69 项；锁文件创建 EACCES 与 journal 写入 EACCES 分开验证。Archive／SQLite 转换／UI／偏好仍为替身，非整份桌面恢复验收。Launcher PID 前后13985，未安装 APK、未强停桌面、未读取用户桌面。标准 build.bat、v1/v2/v3 签名、16KiB 对齐及 git diff --check 通过；v1.5.8／33，APK SHA256 `BD538D359528EA17217F084A1711CA584FD0C72DD95B6CC5A73950CEEECF12B8`，证据位于 `build/f05-restore-worker-20261003/`。
- **未关闭项**：启动恢复守卫仍同步执行，HOME 在后台恢复期间启动主进程会等待文件锁，真实最坏启动耗时／ANR 风险未量化；首帧后的既有 journal 清理和文件删除仍同步，尚未证明其帧预算。异常恢复、首帧交接／清理、进程中途退出、完整备份一致性、Loading 录像和 Android 16／跨 ROM／应用 UID 权限仍需隔离设备验收；不能将本项或全项目标记性能／生命周期闭环。未更新 MEMORY.md，未暂存、提交或推送。

**F01：系统卸载入口保留用户身份与阻止跨用户误卸载（安全门实现，实际 UI 待验）**

- **根因与范围**：普通应用经 na／ia → requestUninstallItem 保留了条目，但 UninstallCompat 发出的 ACTION_UNINSTALL_PACKAGE 与 ACTION_DELETE 仅含包名，既有返回确认／模型删除门不能阻止系统先对错误用户执行卸载。另一个 data/A.p 条目入口先按旧 user10 规则扫描同包分身，再请求包名卸载，可能丢失原选择身份或对 user999 抛错。本轮只修请求目标与此普通应用旁路，保留 F02–F04 工作区修改、快捷方式／特殊条目旧路径和现有模型冻结架构，不进入 Component Phase 3。
- **最小修改与取舍**：生产文件仅 `launcher/tools/java/com/smartisanos/launcher/compat/UninstallCompat.java`、`launcher/smali/com/smartisanos/launcher/data/A.smali`。使用现有 ProfileRepository 映射 userId／serial；目标句柄非空、serial 已知且与 Repository 的当前用户句柄相同才放行，两份 Intent 均携带 EXTRA_USER。没有以相同 serial、固定 user10／999 或仅包名推断跨用户目标；无法安全确认时不发 Intent、不设置 pending、不查询／删除模型，明确提示“无法安全卸载此用户的应用，请到系统设置中操作”，主线程显示提示，复用既有 cancelSystemUninstall → 原 Y(1)／W／V，异常仍用原 GL 清理。已等待确认时的后续顺序请求直接返回，避免覆盖 pending 或清理正在等待的场景。包名式主题等入口仍仅表示当前用户；普通 Item 在 A.p 读取 user／扫描关联包前转交原 requestUninstallItem，特殊 Item 保留原分支。
- **原版／参考依据**：对照原始 APK 的 clean_launcher_raw、clean_launcher ia／A 卸载链及 maintained UninstallApp 单项确认链，原版使用私有 ApplicationManager 和原数据库／动画派发，不能直接照搬到普通 Android 或恢复其提前删除。继续使用当前已验证的取消／成功动画、PackageStateRepository → ProfileRepository → RemovalGateway → LauncherModelRepository → item-level 执行器，没有新增 Manager、Service、状态 enum 或第二套用户转换器。原版 APK 归档保留；本地 decompiled_theme_check 对应缓存只有部分目录，未假称其中存在本次所需的 Launcher 类。
- **平台证据边界**：[Android EXTRA_USER 文档](https://developer.android.com/reference/android/content/Intent#EXTRA_USER)确认用户字段公开可用，[AOSP UninstallerActivity](https://android.googlesource.com/platform/frameworks/base/+/ad6383d7f91d332d63d8453ac59ab982fe16478d/packages/PackageInstaller/src/com/android/packageinstaller/UninstallerActivity.java)读取该字段并检查目标 profile，但这不能证明 OEM 卸载器会按该字段卸载分身。项目尚无已验证的跨用户卸载通道，所以当前方案保守拦截所有非当前用户请求，属于明确的兼容功能限制；不得将“已添 extra”称为跨 ROM 精确卸载通过。以后开放必须先验证真实系统目标和包安装状态，失败不能退回当前用户包名卸载。
- **隔离负例与检查**：扩展现有 `tools/tests/stability/test_uninstall_bridge.py` 的 Intent／Profile 边界，新增 `test_uninstall_target.py`；执行 HEAD 的真实旧桥接代码，确认 user999 发出了无 EXTRA_USER 的卸载请求。新版 95 项检查覆盖 0／10／999／128／负数、用户字段缺失／非 Number、句柄或 serial 未知、进程用户非 0、当前用户正常／备用入口、等待中第二请求、取消一次性回位、确认删除、非应用排除与当前用户包名式入口。原模型 169 项继续验证同包用户／component／条目、快捷方式、查询不确定与重复广播；108 组合移除策略、8 组取消、4 组系统等待、原两阶段队列及 Smali 行删除检查通过。A.p 新入口只做静态接线检查，没有将其称为真实 DatabaseUpdater 事件运行通过。
- **Android 与恢复回归**：新增 `UninstallTargetProbe.java`、`run_device_uninstall_target.py`，vivo X21A／API 28 app_process 执行真实生产 UninstallCompat，真实 Android Intent／Parcel／UserHandle；启动被 Capture Context 截获，Package/Profile／Model、GL 派发为受控替身，提示队列未渲染。旧代码同样复现跨用户目标丢失，新版 43 项检查通过，含真实 Intent 序列化后 EXTRA_USER、两动作目标一致、跨用户拦截、非 0 当前用户与等待保护。未打开系统卸载界面，未卸载应用／安装 APK／访问用户桌面数据，Launcher PID 前后 13985。F02 120 项实际 Android SQLite 页面、F03 83 项恢复身份及 F04 141 项事务故障／重载静态门检查再次通过。
- **产物与剩余风险**：标准 build.bat、v1/v2/v3 签名、16KiB 对齐与 git diff --check 通过；APK v1.5.8／versionCode 33，SHA256 `F0C31E9ECB3399A08547A5CAF305A6AC7E748B2F076F8E03781E5263F5643326`，证据在 `build/f01-uninstall-target-20261003/`。当前产物包含 F01–F04 既有修复，不能据上述检查宣称全项目无回归。新的拦截提示／回位、正常主用户实际卸载、系统取消与成功动画需安装后验证；F01 本轮未重新做真实 PackageManager 卸载事实检查，10 月 2 日用户已确认的动画仅是此前版本证据。分身必须到系统设置卸载，Android 16／其他 ROM、完整真实恢复与进程／跨文件故障窗口仍待验证。未更新 MEMORY.md，未暂存、提交或推送。

**F02：待安装恢复复用页面槽与事务容量保护（2026-10-02—03，隔离 SQLite 通过）**

- **范围与回归要求**：用户要求继续下一阶段并强调不要修复后再破坏其他功能。本轮仅处理 F02 页面分配旁路，保留 F03/F04 的既有修改并运行对应回归。没有以代码行数减少或构建成功代替数据安全／运行验收，也没有把隔离检查称为全项目无回归。
- **根因与负例**：PendingItemRestoreHandler 直接以页表 `MAX(_id)+1` 新建页面，不消费预置 `pageIndex=-1` 空槽且无 1000 行保护；它还以页表最大索引作为桌面末页，可能受空的正索引预分配页影响。执行基线生产 Pending 方法、受控安装事实与真实 Android SQLite：末页 12 格已满、页表 1000 行时，补入一条后得到 `pageRows=1001 unused=999`，复现旁路破坏既有不变量。此证据来自独立 fixture，未对用户桌面做丢失／恢复实验。
- **修改文件与复用**：仅本阶段修改 `launcher/tools/java/com/smartisanos/launcher/backup/PendingItemRestoreHandler.java`、`LayoutSnapshotImporter.java`、`LayoutSnapshotExporter.java`。从 Importer 的既有实现提取包内 `nextRestorePageId`，主恢复两处分配与 Pending 共用；既有 defaultPage／persistPage 开放包内复用。Exporter 的同一页表读取封装为 readPageRows，字段／排序与导出保持一致，isUnusedPageSlot 规则未变。没有新页面 Manager、状态 enum、数据库 schema 或第二套可复用槽定义。
- **行为与事务**：优先取最小可复用槽 `_id`，仅真正没有槽且页表不足 1000 行时允许增加记录，新桌面索引限定 0–999；有状态、标题、containment 或扩展数据的特殊行保持原样。已有目标页直接使用，避免重复页行，Pending 新页继续原默认值，主恢复继续原模板克隆。Pending 的 ID、末页、末格、页表快照均放入既有数据库事务；根级 FolderInfo 也占用格子，不被排除。Importer 对保留条目采用相同根级 FolderInfo 边界，防止满格文件夹后的追加覆盖原格。容量不足或后半批分配失败时，整个数据库批次回滚，pending 不消费，不新增重试调度。
- **对照与测试**：原版 clean_launcher 的 data/a/m、页表字段及 maintained PageInfo 只作原结构对照；此移植 pending/helper 无可直接搬用的原版或 maintained 恢复链。新增 `tools/tests/restore_pages/RestorePageProbe.java`，扩展现有 `tools/tests/restore_profiles/run_device_tests.py --pages`，复用原 app_process 构建／隔离方式。vivo X21A／API 28 实际执行生产 Pending、Importer、Exporter、FolderTopologyValidator 与文件工具，使用真实 SQLite 事务、JSON、Intent、AtomicFile；Package/Profile／图标边界为受控替身。120 项检查通过，涵盖 12/20、末页满／余一格／空桌面／零页表、1000 预置槽、无预置槽追加、特殊页保护、无可用槽、批次中途容量耗尽后的全回滚、全分配页、索引上限、最后允许的新记录、连续批次、成功消费后重复事件、已有目标页、根级文件夹末格，以及真实 Exporter 导出后由生产 Importer 再恢复。
- **验证与产物**：F03 的 83 项恢复身份检查、F04 的 141 项事务故障检查及两处重载接线检查仍通过；标准 build.bat、v1/v2/v3 签名、16KiB 对齐、git diff --check 通过。最终 APK v1.5.8 / versionCode 33，SHA256 `5E28AC32D4B1D481E8FB310BEF169C6B1653957ED5F08C67EB5B8B52988661C1`。基线负例、新版 120 项、83 项回归、事务检查与构建证据在 `build/f02-restore-pages-20261003/`。Launcher PID 前后均为 13985，未安装 APK，探针仅访问唯一 `/data/local/tmp/smartisan-restore-pages-f02-*` 和独立 profile 回归目录，不操作用户桌面数据。
- **风险与未验范围**：真实安装事件／模型通知／渲染、Launcher 应用 UID、完整备份恢复／撤销、Android 16 与其他 ROM 仍待验；既有安装主 Handler 同步调用 Pending，本轮未迁移线程，未测新页表读取的实际帧耗时，不宣称流畅度改善。数据库事务与 pending 文件消费仍是两步，跨两步的强杀／文件写入失败、并发回调幂等性不在本次页面槽证明范围；“成功消费后重复事件”不等于上述故障窗口闭环。历史已超 1000 行的数据库未在本轮直接清理，快照继续沿用现有 normalizeReservedPages。空间耗尽保留 pending，但不会凭空承诺释放空间后自动再补入，仍受原安装事件入口约束。
- **文档与仓库**：已更新本日志和专项审计后续状态；项目及全局 MEMORY.md 未更新，未暂存、提交、推送，保留此前 F03/F04、构建产物及其他工作区改动。

### 2026-10-02

**F03：恢复保留条目接入 Package/Profile 事实源（隔离 SQLite 验证通过，真实分身待验）**

- **阶段判断**：用户确认继续进入下一阶段，按恢复数据安全顺序处理 F03；F04 已有实现、失败注入和 Android 9 隔离平台验证，可继续处理独立根因，但完整恢复／撤销与断电验收没有被标记完成。本轮不做代码精简，不扩展 component lifecycle Phase 3，不处理 F01/F02/F05 等其他审计项。
- **根因与负例**：旧 RestoreMergePlanner 对所有条目使用当前主用户 PackageManager，未消费条目的目标 user／serial，异常最终 false；Importer 只有该布尔值为 true 才保留备份外条目，随后整表重建。主用户无包、分身当前行存在、旧备份无该行的受控 fixture，执行基线生产 Planner／Importer 的真实 Android SQLite 流程，得到 `preview=0 preserved=0 finalRows=0`。这是隔离条件复现，不是用户桌面曾丢数据的证据。原去重键还直接使用源备份身份，源 user 与目标 user 不同时可能漏保留或重复插入。
- **修改**：仅修改 `launcher/tools/java/com/smartisanos/launcher/backup/RestoreMergePlanner.java` 和 `LayoutSnapshotImporter.java`。条目安装事实改为复用现有 `ProfileRepository → LauncherItemKey → PackageStateRepository`，现有 PackageState enum 不变；只按目标 user 转换运行时 serial，不使用备份源 serial 查询当前设备。当前条目和已 remap 的备份条目，仅 `REMOVED_CONFIRMED` 进入丢弃／pending 分支；UNKNOWN、REPLACING、锁定／静默／暂不可用等状态保留行，不能因查询不确定清表丢失。pending 消费者继续调用原 isInstalled，但仅 PRESENT／DISABLED 为正向安装事实；UNKNOWN 不主动补入，主用户安装事实不代替分身事实。
- **身份与边界**：预览复用已有 remapIdentity，Importer 在清表前执行同一映射，并复用这份目标条目集合做去重和插入，不二次猜测源／目标身份。当前 DB 行不做备份源 profile remap；原源 JSON 保持不变。pending JSON 额外保留已有目标 serial 字段，serial 不匹配时返回 UNKNOWN，避免按复用的数字 user id 激活旧 pending。FolderInfo 仍为结构行，快捷方式保持 package／shortcutId／目标 serial 身份；不改数据库 schema、原版页面／宫格、图标来源、动画或 Launcher 生命周期，不新增 Manager／Profile 解析方案。图标包可用性继续作为资源判断，未冒充桌面删除许可。原版／clean_launcher 无该移植恢复辅助链；maintained 的 ProfileAppsSettingsActivity 按 UserHandle／serial 枚举仅作对照，正式修改仍使用本项目冻结的事实源。
- **测试**：新增 `tools/tests/restore_profiles/run_device_tests.py`、`RestoreProfileProbe.java`，复用已有 app_process 隔离方法。实际生产 Planner、Importer、PendingItemRestoreHandler、FolderTopologyValidator 和文件工具运行于 vivo X21A／API 28，使用真实 SQLite 清表／重建、事务、JSON、Intent 和 AtomicFile。83 项检查通过：九种 PackageState、目标 user／serial、不同源 serial 映射、源 user id 碰撞、同包不同组件、当前 pinned shortcut、目标快捷方式去重、未知 serial、源 profile 未解析、FolderInfo 父子结构、未知备份条目保留、明确缺失 pending、主用户存在／分身 quiet、UNKNOWN 不补入、正向事实补入及旧 serial 拒绝。Package/Profile 事实、目标 profile 映射和图标编解码是受控替身，未以此声称真实跨 ROM Binder／分身权限通过。
- **构建与证据**：F04 生产事务控制流 141 项及两处重载接线检查仍通过；标准 build.bat、v1/v2/v3 签名、16KiB 对齐、git diff --check 通过。最终 APK v1.5.8 / versionCode 33，SHA256 `40979907932ED2CDBB4D980B02522B3F840C5E36D5256FBF155ACBC337D1EE91`。基线负例、新版设备输出、摘要和构建证据在 `build/f03-restore-profiles-20261002/`；未安装 APK，Launcher PID 前后均为 13985，探针只访问唯一 `/data/local/tmp/smartisan-restore-profiles-f03-*` 目录，不操作用户桌面。
- **剩余风险与文档**：真实分身用户可见性、Binder 异常、锁定／quiet 切换、安装替换并发、快捷方式实际图标与点击、真实完整恢复／撤销及 Android 16 仍待设备验收。保留 UNKNOWN 行意味着暂不可解析的旧条目也可能留下，这是防止不确定查询造成数据丢失的明确取舍。F02 待安装补入仍存在页面槽旁路，将作为下一项独立处理；不得将本轮 pending 用户身份检查称为页面分配已修复。已更新本日志和原始专项审计的后续状态；项目／全局 MEMORY.md 未更新，未暂存、提交或推送，保留此前 F04 和构建产物改动。

**F04：恢复事务日志失败门与证据保留（故障注入及 Android 9 隔离运行通过，完整恢复待验）**

- **范围与根因**：按用户要求优先处理全项目审计 F04，未做代码精简或其他审计项修复。原 `RestoreOperationJournal.read()` 将读取／解析异常当成 IDLE，`write()` 返回失败却被调用方忽略，导致日志未可靠保存时仍可继续数据库、偏好和图标写入；重载也忽略恢复返回值，清理可能先删恢复来源再尝试重置日志。备份偏好测试通过不能证明这条事务链安全。
- **实现**：复用既有 Journal、DesktopRestoreController、RestoreRecoveryGuard 和冷重载 Owner，无新 Manager、Service 或事务状态。日志读取区分真正不存在、读取失败和损坏，检查必需身份／路径字段；写入改为必须处理的 checked exception，先同步文件描述符，再提交 AtomicFile 并回读比对，仅确认成功后推进内存状态。日志不可读／损坏时禁止覆盖或重置，不伪造 IDLE。每阶段检查点失败停止下一阶段；普通恢复错误继续使用已有回滚链，但回滚也必须先保存检查点。已完成状态重试不重复导入，部分导入后的重试使用已有回滚来源。
- **收尾与用户反馈**：准备失败、启动恢复和首帧清理均先确认日志重置成功，再删除临时来源；失败保留最后检查点及回滚文件，不提示恢复成功。首次重载与“重试”都检查恢复结果，失败复用原失败／重试界面；设置页复用明确的日志错误提示。损坏日志阻止新的恢复与自动恢复写入，Launcher 普通启动仍可继续；本轮没有自动重建或删除损坏日志。成功恢复后替换先前的日志失败通知，避免恢复成功仍显示旧错误。
- **修改文件**：`launcher/tools/java/com/smartisanos/launcher/backup/{RestoreOperationJournal,DesktopRestoreController,RestoreRecoveryGuard}.java`、`launcher/tools/java/com/smartisanos/launcher/reload/{LauncherColdReloadCoordinator,ReloadTransitionActivity}.java`、`launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java`；新增隔离测试 `tools/tests/restore_journal/{run_tests.py,run_device_tests.py,DeviceCheckpointProbe.java}`。原版／clean_launcher／maintained 无同名移植事务 helper，继续修复当前实现，不替换原版桌面核心。新增 JournalException 仅用于强制调用方处理持久化失败；设备探针复用已有 app_process 方式，不加入正式 APK，不新增生产故障注入开关。
- **验证**：编译并执行实际生产 Journal、Controller、RecoveryGuard 的 141 项检查通过，覆盖不存在／损坏／读失败、写入／同步／静默提交失败、各导入阶段与回滚检查点、重试、清理失败和证据保留；初次／重试重载门做静态接线检查。既有备份偏好 21 项、设置会话 33 项及生命周期／外部结果／备份锁／轮询接线检查通过。最终标准 `build.bat`、v1/v2/v3 签名、16KiB 对齐、`git diff --check` 通过，badging 仍为 v1.5.8 / versionCode 33（minSdk 23、targetSdk 28）；最终 APK SHA256 `D504D48F01F2E8FB367F34DF47333005DC0A501AF93608A25BE46848D78C9D43`。测试／构建证据保留在 `build/f04-restore-journal-20261002/`。
- **Android 9 隔离运行**：vivo X21A（API 28）执行未改写的生产 Journal、Controller、RecoveryGuard、锁和文件工具；使用真实 Android AtomicFile、JSONObject、文件描述符同步与 EACCES，归档／数据库／设置通知使用隔离替身。41 项平台检查、保存检查点后 SIGKILL 重进 6 项、SIGKILL 后启动守卫恢复 6 项、真实 AtomicFile 未完成写入后 SIGKILL 重进 4 项，共 57 项通过。覆盖读权限失败、写权限失败不推进状态、不执行后续 importer、不误报成功、保留恢复来源、权限恢复后重试、损坏日志保留、旧 `.bak` 恢复及中途写入读回上一检查点。三次 SIGKILL 只杀探针自身；AtomicFile 中途写入场景由探针直接打开平台写入，未在生产 `write()` 中植入暂停／强杀钩子。探针仅访问唯一 `/data/local/tmp/smartisan-restore-journal-f04-*` 目录，Launcher PID 前后均为 13985，未安装 APK、未访问用户桌面数据；摘要、编译／运行输出见 `build/f04-restore-journal-20261002/device-android9/`。
- **边界与风险**：本机故障注入与 Android 9 探针证明事务控制流、真实平台日志 IO 和失败门，不证明实际 SQLite、图标、主题转换或整份备份一致性；探针为 shell UID，未覆盖 Launcher 应用 UID／SELinux 的全部行为。同步和回读、SIGKILL 重进均不等于真实断电验证；Android 16 当前无在线设备，磁盘满、生产进程中途强杀、真实恢复／撤销和重试界面仍需隔离设备验收，未替换用户设备 Launcher、未操作用户桌面数据。无法读取的日志仍可能需要先保存文件和日志证据再人工处理，不能自动假定安全清空。F04 本身未覆盖 F02/F03；后续 F03 修复见本日独立事项，F02 仍未修复。
- **文档与仓库**：本节记录最终方案和验证边界；专项审计保留原始基线统计并增加 F04 后续处理说明。未更新项目或全局 MEMORY.md，未暂存、提交或推送；构建产物继续保存在本地，保留此前工作区改动。

**卸载取消、成功动画与桌面下载稳定性**

- **历史根因与本次更正**：普通 Android 公共系统卸载框不创建原版私有 `oa.jk`，空弹窗判断和运行中短路会使取消后跳过 GL 场景复位。**【已废弃】把 `fd → T → hd` 强制清理当作正常卸载返回流程**：它虽能解除锁死，却跳过动画，等待系统确认期间调用还会提前清掉回收站场景。该调用只保留为异常兜底，正常取消／成功均使用下述原版动画。保留防卡死修复，只在系统框等待时阻止 J.onPause 的清理，移除 Launcher.onPause 的重复调用；返回后按取消／确认移除分别交给原版动画，不重建 Activity、不在生命周期线程操作 GL、不新增 Manager/Service。
- **原版动画与兼容接线**：原版取消通过 `oa.Y(1) → W → V` 播放 0.3 秒回位与场景时间线；现在公共卸载返回未确认移除时复用该 GL 事件，完成回调释放输入和卸载标志，快速返回与进入动画重叠时保留 GL 强制清理兜底。成功时保留 Sc.SO，继续由现有 `Aa.a(ItemInfo) → DatabaseUpdater → Sc.b` 播放图标落入垃圾桶、垃圾桶收回及桌面回位两段 0.3 秒动画，不先强制回位。对照 clean_launcher 和 maintained 的 TrashView / DatabaseHandler，确认动画资源与完成回调已存在，无需重写。有效原版录像 `original-ready.mp4` 的 45.4–45.6 秒为取消，76.4–77.0 秒为成功；旧当前录像 `success-current.mp4` 实际只捕捉到取消，真实成功发生在录屏结束后，不能用它声称成功动画已对照。熄屏录像无效，变帧率录像按 ffmpeg 时间戳重采样核对。
- **真实卸载与分身／快捷方式边界**：普通应用仍只启动公共系统卸载界面，不提前私有 deletePackage 或删除数据库。系统返回补查本次 item，复用 PackageStateRepository/ProfileRepository → RemovalGateway → LauncherModelRepository；只有包确认移除且配置可用才允许单条目执行，广播已提交时不重复提交。修正执行器底层 `A.q` 仍按整包／用户扩展删除且追加 user10 的旧行为：普通应用只删除已确认的具体行，并将该行原样交给既有 GL 任务，避免后续空列表再按包扫描场景。Sc 回收站匹配和 data/w 任务优先级使用数据库条目 ID，避免同组件分身误匹配或同包另一入口抢占。模型拆成逐条目派发后，旧 data/z 队列仍会连续 forceFinish 前一动画；现在遇到 ON_CELL_UNINSTALL_ANIMATION 暂停后续任务，由原 Qc/Pc 完成回调清除标志、时间线后继续原队列，保留两段动画，无随机延迟或新队列。na 的公共分流仅 itemType=0，快捷方式、小程序和其他特殊类型保留原路径。查询异常、配置锁定／静默、升级／替换都不按卸载删除；取消保留应用和布局。
- **修改文件**：既有 `Launcher.smali`、`a/oa.smali`、`a/T.smali`、`a/W.smali`、`a/na.smali`、`view/Sc.smali`、`view/Pc.smali`、`view/Qc.smali`、`data/A.smali`、`data/w.smali`、`data/z.smali`、`UninstallCompat.java`、`LauncherModelRepository.java`；测试在 `tools/tests/stability/`。保持现代模型冻结架构，不进入 Phase 3，不修改应用分身发现／启动、快捷方式创建、图标 PNG、动态天气／日历、阴影或主题动画。
- **下载修复**：更新 APK 写入私有目录，不再要求 Android 6–10 共享存储授权；仅 DownloadManager 未成功入队时复用已有后台直连，已入队不重复写文件。直连拒绝空包和长度不完整包并删除残片。更新／主题下载任务丢失、查询失败时结束 UI 轮询并提示重试；主题公共 Downloads 授权规则不变。仅修改既有 MaintainedLauncherSettingsHost.java，不改下载源。
- **验证与当前边界**：取消 8 状态、系统框等待 4 状态、移除策略 108 组合、生产卸载桥接和生产模型 169 项检查通过，新增执行生产 Smali 的底层行删除隔离测试及两阶段队列保护检查通过，覆盖用户／组件／条目隔离、快捷方式排除、查询不确定保留与重复事件；下载 5 场景、设置会话 33、预览 32 项此前通过。标准 build.bat、v1/v2/v3 签名、16KiB 对齐、git diff --check 通过；新版 SHA256 `C5960800116EA8DAD00A9F1D494DB68BC77EFBFDDC8819CA27E5D4228DE2C215`，保留数据安装到 vivo X21A／Android 9 成功。取消动画已获用户确认正常；成功修复包安装后用户卸载独立 Fixture 测试应用并明确回复“正常了”。PackageManager 确认测试包已不存在，桌面 PID 保持 13985，回收站退出、Dock 恢复。新录像 uninstall-success-v2.mp4 开始时已是卸载后的桌面，未捕捉动画本身；成功动画验收依据为用户现场确认，不将该录像称为动画逐帧对照证据。原版设备未安装修改包。Android 16、分身／小程序真机和其他 ROM、实际网络下载仍未完整复测。设备日志关闭，空日志不算崩溃检查通过。此前重新应用改进版图标已获用户确认正常；本轮未修改 PNG、未暂存／提交／推送。未更新 MEMORY.md。

**在线图标库索引、候选与缓存同步**

- **用户资源改动**：暂存图片共 1008 张替换、141 张新增、191 张删除；库现有 5263 张 PNG。新增／替换图共 1149 张，尺寸为 512×512（1069）、384×384（78）、192×192（1）、288×288（1），均满足文件大小／边长限制并带透明通道；本轮不修改图片，不以通道存在代替背景和视觉质量验收。
- **同步**：执行现有 `tools/generate_icon_index.py` 更新文件清单、大小和 SHA256；候选表移除 181 个已删文件引用，并按已有包名后缀规则登记 12 张新增 `_2` 等候选，同步 `launcher/assets/icons/variants.json`。新 `icon_数字.png` 和 `ic_folder_bg.png` 未声明应用归属，保留在索引，不猜测映射、不改应用识别规则；这些文件不能仅靠名称成为对应应用的自动图标。
- **缓存**：同名替换不会自动绕过原 v3 持久缓存，下载／miss、预览／磁盘裁剪、备份恢复原始图标缓存统一递增为 `online_icon_cache_v4`；修改现有 `MaintainedLauncherSettingsHost`、`IconPreviewRepository`、`RestoreIconSourceReconciler` 和 `icons/README.md`，不新增缓存管理器，不删除旧缓存；缓存身份加入现有 `ICON_RASTER_REVISION`，通过既有一次性 `ensureIconRasterRevision → applyIconChange` 刷新持久合成图，避免仅换下载目录后桌面仍读取旧 iconData。不改动态图标、阴影、视觉比例或图标包／自定义选择。旧备份的原始图片仍可还原到当前缓存，保持备份自包含语义。
- **发布边界**：在线 PNG 不打包进主 APK，发布前须先同步 GitHub／Gitee 镜像，再发布使用 v4 的 APK；否则新缓存仍可能从镜像下载旧图。切换版本后需重新下载，弱网／离线可能暂时回退应用原图；持久合成图通过既有刷新流程更新，网络下载完成后沿用原刷新派发。未提交或推送镜像。
- **文档整理**：感应实现、齿轮、静态阴影、白线、设置会话和光影备份统一保留一条合并记录；独立 handoff 文档只保留记录入口、旧实验撤下说明与探针用法。预览调度／内存审计保留独立范围和未完成边界，未把验收风险删除。
- **验证**：5263 个索引文件、大小和 SHA256 一致，4536 个包的 5063 条候选全部指向存在图片，APK 候选资产与源文件字节一致；三个缓存消费者均使用 v4。预览调度 32 项及页面接线、备份编码器 21 项通过；标准构建、v1/v2/v3 签名、16KiB 对齐和 `git diff --check` 通过，最终 APK SHA256 `DB303C8A6DBB13ED61D9301526B1902D4ECC9DA954AD01DC06DFA3081960D39A`。用户 PNG 与暂存区一致，本轮没有修改图片；镜像未发布，未安装本轮缓存版本包或做真机下载／升级往返。未更新 MEMORY.md，未提交或推送。

**图标感应光影、阴影统一与备份（合并记录）（2026-10-01—02）**

- **主题交接与白线根因**：ThemeCubeCells 原先按旧 TH 和 target 前缀交接，与包含阴影身份的 Composer 缓存不一致；`pa.getStaticTargetTextureName()` 读取目标 sc[0] 的实际纹理，`ga.Li()` 在销毁目标面前同步真实桌面 TH/sc[0]，仅普通静态应用生效，ActiveIcon、文件夹及旧纹理回退保留。毛玻璃退出时 `l.onComplete()` 又提前将 Renderer.AF 恢复为 1（白 RGB、Alpha 0），正式背景尚未接管，cover 淡出后露出一帧白线；Android 9 原状态栏止于第 84 行，Launcher 白线位于第 102 行，逐 draw 探针确认其出现在背景 cover 交接阶段，改变状态栏文字及诊断颜色不能消除。仅把清屏恢复移到 `theme/k.1.smali` 的 `r()` 正式背景交接之后，保留大屏保护、最终值和动画时长。所有颜色／像素探针已移除，未将缺失纹理或文字颜色误认成白线原因。
- **主题交接验证**：44 项生产 smali 交接与保护检查、58 项阴影选择和 24 项三态切换检查通过；Android 9 毛玻璃→格子、格子→经典黑录像与第 102 行检测未见末尾白线，用户确认正常，日历仍显示 2 日。正式白线修复包 SHA256 `AFD5F8087B598D0E65F645BB5BE85C35FD6DED8868F30B8CE949A1455CF4470A`，证据 `build/shadow-transition-audit-20261002/`。此前录像捕捉的轻微图标收尾边缘变化仍保留为未完全验收项；Android 16、透明覆盖开关及其他 GPU/ROM 尚未独立复测。系统日志禁用，空 logcat 不算崩溃验证。
- **实现与入口**：复用原版 `H/r → Ra → Qa → Cell.sc[27] → MutiTexMaterial`，适配普通 Android 缺失的 OEM blur、传感器注册 Looper 和跨 GPU 计算；不新增 Manager/Service，不改图标与文件夹几何、解锁或状态栏。入口位于“应用图标 → 桌面文字调整”下面，复用 SettingItemSwitch/SwitchEx，只有右侧滑块可点击或滑动切换；新安装默认关闭，保留已有偏好，沿用冷重载与备份。图标感应光影和快捷桌面增加性能开销提示。按用户要求更新光影说明为“开启后，桌面图标的投影会跟随当前环境的天气、光照情况以及手机握持视角动态变化。开启此功能会增加桌面耗电”，同步中文资源、英文资源及中文回退；使用自然换行，不插入硬换行，仅修改文案，不改环境输入或感应算法。文案包标准构建、签名和 16KiB 对齐通过，保留数据覆盖安装 vivo／Android 16 成功；最终文字的真机排版尚未截图验收。
- **贴图与 GPU**：IconProjectionBlur 复现 Android 10 Skia sigma、三级 box 窗口和逐轴整数舍入，三尺寸、七 sigma 共 21 组原版真机 Alpha 对照完全一致。原 shader 同贴图侧向位移在 Adreno 640 约 29.25px、Mali-G925 约 0.15px；兼容式显式复现实测约 256 的距离分母并避免溢出，九组固定光源 Alpha 最大误差 1/255、平均误差小于 0.023/255。仅取消 MutiTexMaterial 被优化掉的死 uniform uShadowRadius 的强制上传，保留其他材质检查。探针入口 `tools/tests/icon_illumination/run_probes.py`，不替换原版 Launcher。
- **输入与阴影职责**：原 H 姿态矩阵、Ra 时间/天气光源不重写；J 既有监听器使用 HandlerThread，成功注册后才设 mRegistered，原 fb() 注销并退出线程。姿态传感器优先 11，其次 20、15；无可用姿态源或注册失败则保留静态阴影，缺光线传感器沿用天气预设。57 项宿主检查覆盖缺失服务、优先级、注册失败、异常和线程清理。普通 Composer 在静态合成前取完整 Alpha，按原版 58..198/256 几何生成八 PNG；静态贴地阴影和 Weather/Calendar LiveShadow 保留自身职责，sc[27] 只显示移动投影，不裁切原版材质。
- **桌面设置齿轮**：底栏带文字的齿轮是应用 Cell，不能与独立编辑按钮 Ec/SettingButton 混同。ThemeChooserActivity 入口现使用固定原版 icon_setting 素材进入唯一静态 Composer；投影仍由 Cell.rl() 在创建材质前调用 prepareSettingsIconProjection() 补齐，以原版素材复用八层生成，精确匹配完整组件，不增加节点，不改点击行为。只在本轮统一其静态生成和缓存，不重画齿轮或改感应贴图算法。修改 IconRasterDiagnostics.java，保留已有 view/a/g.1.smali 接线。
- **静态阴影统一（10 月 2 日补齐）**：原版按主题 icon_light_shadow 选择 Dark/Light，aero/trans/glime 使用 Transparent，三种颜色共用两组半径。Bridge 现直接读取同一 ICON_TYPE，不再用透明开关和壁纸明暗后缀推断；缓存键加入类型、半径、颜色并递增阴影版本。另修复原 setIconType 将“非 Light”等同 Dark 的三态遗漏：当前为 Transparent 时重新选择普通类型，再保留原特殊主题覆盖，避免退出毛玻璃后普通主题继续使用浅阴影。桌面设置完整 ThemeChooserActivity 组件以固定原版 icon_setting 素材进入现有 Static Application Composer，缺素材返回旧 DB 读取，不将已合成 DB 当 RAW；不受图标包、在线图标和默认圆框替换。保留物理尺寸、轮廓低 Alpha 过滤、动态 LiveShadow/CachedFrame 生成方法和既有感应投影路径，不重画素材、不新建节点。生产选择与缓存 58 项、原 smali 状态切换 24 项和图标契约检查通过；修改 Constants.smali、LauncherSettingBridge.java、IconRasterDiagnostics.java，新增 tools/tests/icon_shadow/run_tests.py。
- **关联设置优化**：短暂 HOME 返回保留子页；仅在设置已暂停、真实返回未锁定桌面、随后熄屏时结束设置会话。前台锁屏、外部 Activity/权限和备份恢复期间不清理；后台暂停主题页 UI 轮询，销毁时清理回调、页位置和预览缓存，不取消真实下载。复用 SettingsHost、ThemeChooser 生命周期和 SCREEN_OFF 入口，修改 SettingsHost、ThemeChooserActivity、Launcher、ia.1 及中英文设置 strings；生产 SettingsSession 33 项及接线检查通过。
- **感应与设置已有验证**：标准 build.bat、v1/v2/v3 签名、16KiB 对齐、git diff --check 和静态图标契约通过。vivo V2458A/Android 16 保留数据安装成功，v1.5.8/33，该轮 APK SHA256 `B7DF2F997A3CEEAEE64C96E04D1DA3F30C5D49DAACB746CE8F08A5946B7FD322`，最新静态修复产物见下项。用户确认普通图标投影移动；齿轮倾斜录屏确认外部阴影变化、本体及文字稳定，真实点击打开设置通过。开关标签不触发、右侧点击关闭和滑动开启通过；关闭时 H/r 连接退出、开启时重新注册。短 HOME 保留子页、桌面返回后熄屏清理、前台锁屏保留子页通过；12/20 宫格和文件夹已有可见投影检查。证据位于 `build/icon-illumination-contract-final/`、`build/setting-illumination-20261001/`、`build/settings-session-validation-20261001/`。当轮 PID 9705 持续存活；设备关闭系统日志，本轮不把空 logcat 当作崩溃检查通过。
- **静态修复真机验证（10 月 2 日）**：标准构建、v1/v2/v3 签名、16KiB 对齐通过，保留数据安装至 vivo，最终 APK SHA256 `151D92C0B0125B7FA8E1829374733B7F3ABB5F4EC105A9725621032AE1E6CBEB`。原版锤子蓝色主题 global icon_illumination=0；vivo 无感应线程，纯静态截图已对照。用户保持动态天气/日历开启并完成毛玻璃→蓝色切换；系统设置、桌面设置及日历三个 ROI 与蓝色冷启动截图逐像素一致（max/mean error=0），日历正常显示 2 日，天气页显示云和 16°、外部阴影可见，天气整体及其阴影 ROI 在热切换与冷启动后同样逐像素一致，结果记录于 regression-pixels.json。动态生成/缓存、LiveShadow 尺寸方法、Weather/Calendar smali、IconVisualMetrics 和感应生成器与本轮前暂存版本逐段相同，仅共享类型读取修正。最新 exit-info 为安装更新和主动冷启动，无新增 crash 记录；系统日志仍禁用，空 logcat 不计通过。证据位于 build/static-shadow-fix-20261001/。原版与移植素材/密度及低 Alpha 处理仍有区别，不能宣称全部图标、全部主题或 ROM 已逐像素一致。
- **验收边界**：同蓝色主题对照仍有偏浅现象，两机倾角未锁定；移植版晴天预设基数 0.5、原版当时日志为非晴天基数 0.7，是已找到的参数差异，不能据此解释全部色差，未提高不透明度强行补偿。深浅全主题一致、晴/非晴及高 lux、动态 live/cached 交接、50/150% 和全部来源、透明覆盖、解锁、其他 ROM/GPU、后台下载返回轮询仍待验证；首次生成性能未量化。外部文件选择器 HOME 后熄屏保留会话及后续取消已观察，完整恢复流程未重测。仅构建和探针通过不代表上述视觉验收完成。未更新 MEMORY.md，未提交、未推送。

- **问题与根因**：感应光影偏好键已有可迁移白名单，但新安装默认关闭时未必写入 SharedPreferences，备份可能遗漏默认值，恢复到已开启的设备后无法还原关闭状态；共用预览页也未展示该开关。权限功能行固定显示“需要重新授权的功能”和 6 项，未区分备份／恢复，也不能查看具体清单；恢复确认文字含显式换行，形成逐句排版。
- **修复结果**：备份补齐 `launcher_icon_illumination_enabled=false` 的隐式默认值，保留显式开启／关闭，备份和恢复预览均显示“图标感应光影”状态。旧备份缺失该字段时显示“此备份未记录”，恢复保留当前值。备份页改为可点击的“无法备份的开关”，恢复页显示可点击的“需要重新授权的功能”；复用现有信息弹窗列出天气自动定位、动态天气和日历、应用通知角标、滑动清除角标、联系人搜索、下滑打开系统面板，恢复提示手动开启并按提示授权。归档新增 `excludedSwitches` 名称清单，不记录这些开关值或系统授权；旧归档没有清单时使用当前六项规则。恢复确认改成一段连续提醒，随屏宽自然换行；按用户截图反馈进一步用逗号、分号连接相关内容，统一中英文资源与中文回退文案，保留替换范围、末尾保留、自动保存、可撤销和壁纸不变的全部说明，不改弹窗行为。
- **修改范围**：`PreferenceBackupCodec.java`、`MaintainedLauncherSettingsHost.java`、`setting_backup_restore_preview.xml`、中英文 `strings.xml`，新增 `tools/tests/backup_preferences/run_tests.py`。沿用现有归档、SAF、预览和恢复入口，不新增管理器，不改桌面布局恢复、撤销、壁纸、动态天气／日历渲染或感应光影算法。
- **验证与验收**：生产编码器 21 项受控检查通过，覆盖默认关闭、开启／关闭往返、旧档缺字段、权限值排除和清单过滤。标准 `build.bat` 构建、v1/v2/v3 签名、16KiB 对齐通过，v1.5.8/33，APK SHA256 `284109956EE0FB6D09E36E03B3A24AA4030C291E061B2E74C2BE4FB6C52B3CAB`；vivo X21A／Android 9 保留数据安装成功。备份预览截图确认光影“关闭”和“无法备份的开关”；设备实际生成的 12:11 归档 `settings.json` 确认包含 boolean false 和六项排除名称。用户确认“可以了”。证据集中在 `build/backup-preview-20261002/`。
- **文案补充验证**：逗号／分号排版调整后再次标准构建、v1/v2/v3 签名和 16KiB 对齐通过，保留数据安装 X21A 成功；最新 APK SHA256 `5FE61C310AB0B5BBECE17D85660CC5F33912ED734F68AAECC023005E1C109CE7`，构建日志 `build/backup-preview-20261002/build-copy-layout.log`。只调整文字资源和中文回退，最终标点版本尚未重新截图验收。
- **边界**：本轮未执行覆盖当前桌面的真机恢复；编码器往返测试不替代全桌面端到端恢复。Android 16／其他 ROM 尚未独立验证本轮界面；系统权限仍须用户授权，不能随备份迁移。未更新 `MEMORY.md`，未暂存、提交或推送。

**图标预览调度与设置内存稳定性审计**

- **本轮范围**：在现有版本上检查桌面生命周期、图标／预览缓存、后台任务和渲染开销；优先功能稳定，只修复有代码或设备证据的问题，不改动态天气／日历、主题选择、宫格和感应投影的视觉契约。
- **确认的问题与修复**：`IconPreviewRepository` 将无 UI 回调的预加载当成无消费者而跳过；`RenderTask` 只在有图标 key 时执行 loader，导致无 key 的后台准备任务没有执行；低优先级队列裁剪只移除任务却留下 pending 回调；正在运行的旧任务按 key 完成，会在取消后同 key 重入时写回缓存、误取新请求回调。现保留无回调预加载的消费者标记，执行 metadata loader，裁剪时立即分离旧批次并完成其回调，以原回调列表身份检查任务归属，取消后的未发布 Bitmap 仅由任务自己回收。P2 已排队工作在内存压力下停止生成，可见请求仍可恢复。沿用现有两线程、缓存字节上限、优先队列和 RequestSession，不新增 Manager、线程池或渲染层。
- **页面生命周期**：`AppIconAdapter` 创建时固定自己的 RequestSession，普通／有效图标预加载和后台准备都绑定该会话；退出页面取消排队任务，销毁设置宿主补齐会话清理。用弱引用确认页面 owner，旧 Activity 销毁不取消新 Activity 的会话；保留短 HOME 返回页面、实际图标下载和备份恢复的既有规则。修改 `IconPreviewRepository.java`、`MaintainedLauncherSettingsHost.java`，新增 `tools/tests/icon_preview/run_tests.py`。该预览调度是移植兼容层，原版／clean_launcher 无此 helper；maintained 的 `Utils$GenerateShadowIconTask` 属于桌面生成链，未替换或搬入本轮调度。
- **审计保留项**：主题小／大预览已有 2／8 MiB 上限及内存压力回收，图标预览缓存已有 6–16 MiB 上限；View 仍引用的缓存 Bitmap 不强制 recycle。原感应监听在 J.onPause()/fb() 注销并退出 HandlerThread，快捷桌面已有 stop／destroy 的截图请求取消与宿主释放入口，天气定时刷新已有开关检查和小时级 TTL。本轮未发现需要替换这些 owner 的证据；未改静态阴影、LiveShadow、天气／日历动画、纹理清屏交接、图标尺寸或系统栏规则。
- **验证**：旧生产调度方法在受控 worker barrier 测试中复现 7 个失败检查；修复后 32 项检查及页面 owner 接线检查通过，覆盖无回调预加载、无 key 工作、裁剪／可见重试、取消／重入、共享消费者和内存压力。现有设置会话 33、传感器回退 57、阴影选择 58／三态切换 24、主题交接 44、搜索图标和图标契约检查通过。标准 build.bat、v1/v2/v3 签名、16KiB 对齐通过，最终 v1.5.8/33，SHA256 `AF69DFD17B459B366A6DC7E17C75E88275F873166E117AA69F5F31372DC93B3D`；vivo X21A／Android 9 保留数据安装成功，设备 APK 哈希一致。真机图标页滚动、返回／重开和普通图标显示已截图／录屏核对，桌面日历仍显示 2 日。
- **内存与未完成边界**：首次采样在设置主页，PSS 253535 KiB、Graphics 154032 KiB，不是纯桌面基线。旧包和新包的设置→HOME 路径都观察到进程重建，日志关闭，原因尚未确认；不把不同 PID 的下降算作回收或优化收益，也未据猜测修改 HOME／重载逻辑。新包返回键退出设置的同一 PID 29708，Views 223→12、Activities 2→1；自然静置后 PSS 270040→264652 KiB，Graphics 159460 KiB 未下降，此短时样本不证明长期无泄漏。`gfxinfo` 仅覆盖 Android View，不能代替 SMEngine GL 帧率。Android 16／其他 ROM、透明开关、长时间 Native／GPU 内存趋势和帧时间改善尚未验证；不宣称全桌面无 BUG 或性能已经完美。证据集中在 `build/stability-audit-20261002/`。未更新 MEMORY.md，未暂存、提交或推送本轮修改。


**主题详情底部列表拖动不跟手**

- **根因与对照**：原版 APK 的干净参考和 maintained 主题页没有当前兼容层的 HOME 触摸拦截。`ThemeChooserActivity` 接入 `blockSettingsHomeGestureScroll()` 后，底部 48dp 内的触摸只要向上偏移超过 4dp 就向窗口发送 CANCEL，没有判断横向位移。vivo V2458A／Android 16 同样横向拖动 500px，轻微向上的轨迹仅移动约 54px 就停住，纯水平轨迹可继续滑动；采样 View 帧无超时，确认本次不跟手来自触摸取消，未将其归因为渲染性能。
- **最小修复**：`MaintainedLauncherSettingsHost.java` 记录触摸起点 X，横向位移占优后锁定本次手势归属并放行后续拖动；只有向上位移占优才沿用原 HOME 防护。保留取消、结束与 Activity 隔离逻辑，不改主题资源、预览调度、桌面主题应用、图标阴影或天气／日历。
- **验证与边界**：新增 `tools/tests/settings_session/test_bottom_gesture.py`，直接检查生产方法，71 项检查通过，覆盖不同密度、横向偏移／反向、纵向取消和状态清理；已有设置会话 33 项及接线检查通过。标准构建、签名与 16KiB 对齐通过，保留数据安装 Android 16 成功；安装后复测相同斜向轨迹，列表可持续移动，用户确认“可以了，正常了”。证据位于 `build/theme-scroll-audit-20261002/`。其他 Android 版本／ROM 尚未独立真机回归，自动检查不替代系统 HOME 手势完整设备矩阵。未更新 `MEMORY.md`，未暂存、提交或推送。

### 2026-10-01

**主题状态栏、切换加载与图标修复**

- **状态栏**：所有版本以最终 `Constants.app_text_color` 为唯一颜色来源，普通主题固定、毛玻璃/透明沿用原版壁纸分类。后续审计确认四指加载窗口也会保存 Launcher 切换前的明暗，退出时用 `WindowInsetsController` 恢复旧值；framework 对新接口控制过的状态栏位不再转换旧 `LIGHT_STATUS_BAR`，导致应用文字正确但状态栏可能停留旧色。现 Launcher 不再参与加载快照恢复，独立设置页保留；原 `e/g` 统一提交原版装饰、旧 flags 和 API 30+ appearance，仅修改状态栏位，获得焦点时复用同一提交入口。按用户要求撤去 vivo/API 36 零调暗特殊策略，不新增取色规则或延时重试。最新包的毛玻璃、连续四指及壁纸明暗切换交由用户真机验收；旧 X21A 截图不能证明本轮修正已通过视觉验收。
- **主题切换**：透明/毛玻璃退出时的 GLThread 崩溃由生成图标纹理丢失引起，恢复链已覆盖静态图标和 `ORIGINAL_ACTIVE_ICON` 动态键；用户确认毛玻璃切回普通主题不再崩溃。缺失源图时的 1px 临时纹理仅用于避免崩溃，动态图标交接帧仍待回归。加载窗口首帧黑带源于 `theme_changing` Dialog 的 `FULLSCREEN` 隐藏状态栏；仅该窗口清除该标志，保留透明状态栏及 `LAYOUT_FULLSCREEN`/`SHORT_EDGES`，让原版灰色遮罩覆盖顶部。X21A 前后录屏 `build/theme-loading-before.mp4`、`build/theme-loading-after2.mp4` 显示黑带消失；其他系统版本未验证。
- **跟随应用图标**：12/20 宫格缺少可选 `icon_size_origin_resize`，0 被钳为 1px，导致 aShell You 等只剩名称；缺省时改用当前宫格 `icon_size_origin`，纹理键升至 `raster:v29-follow-app-content-box`。X21A 实际绘制恢复为 12 宫格 192×192、20 宫格 142×142；圆形路径不变。
- **解锁兼容模式**：对照 Git 标签 `v1.5.7`（`6df1c64d`），开启原有开关后复用旧版起播策略：真实 GL 准备完成后，有效解锁信号可不等待窗口焦点；已观察到锁屏交接 Resume 且设备可交互时，沿用旧版 120ms pre-roll。关闭时保留当前已解锁且获焦点才起播的策略。保留新会话 ID、旧 GL 事件隔离、重复信号抑制和应用覆盖取消；不回退全局计时或 XML，12/20 宫格继续共用 1.32 秒目标时长。修改 `LauncherBelowKeyguardCompat.java`、设置说明和现有解锁测试；状态测试覆盖默认门控、兼容无焦点起播、真实准备后调度、重复/取消回调及应用覆盖。魅族录屏显示起播衔接停顿，但缺少该设备日志，修正效果待用户安装后验收。完整 `build.bat`、签名 v1/v2/v3、16KiB 对齐和 `git diff --check` 通过，版本保持 `v1.5.8/33`；未安装魅族，状态测试不能证明真机无卡顿。新包 SHA256：`4E215796ED8A30F60B32AE881DFCB2DF98F1A80685BD1D30A7D9B18FA5CAF83F`。
- **修改与验证**：涉及 `Constants.smali`、`J.smali`、`e/g.smali`、`theme/t.1.smali`、`Material.smali`、`IconRasterDiagnostics.java`、`LauncherSettingBridge.java`、`SmartisanProgressDialog.smali`、`OriginalLoadingContentFactory.java`、`MaintainedLauncherSettingsHost.java` 等现有实现。最新包标准 `build.bat`、v1/v2/v3 签名、16KiB zipalign 和 `git diff --check` 通过，保留数据安装 X21A 成功并提交 Launcher 启动；用户要求自行测试，本轮未继续切主题或宣称视觉通过。APK SHA256 为 `F43F98B884F5616E7492804AFF1314A7EBC5FBF4D1715C3EBCA23178CB14C950`。Android 16 系统自动反色在撤去特殊策略后的表现、连续四指、透明覆盖及壁纸明暗切换仍待验收。未更新 `MEMORY.md`。

### 2026-09-30

**四指切主题状态栏修复与搜索、预览内存优化**

- **四指热切换根因与修复**：V2458A / OriginOS 16 故障现场中，经典蓝桌面标签为白色，WMS 与 SystemUI AppearanceRegion 均为 `isLight=false`，但 `StatusBarTransitionsController.mDarkIntensity=1.0`，实际状态栏仍为深色；没有 pending/deferring/tint 动画。打开设置再返回，同一主题恢复 `mDarkIntensity=0.0`。读取设备实际 SystemUI、framework、vivo-services 和 services 代码，确认 `DarkIconCheckControllerImpl` 会在第三方窗口上采样背景并覆盖主题图标明暗，重复提交原版颜色不能解决。`DisplayPolicy` 对 `FLAG_DIM_BEHIND` 窗口禁止自动反色采样；现仅在 vivo / API 36 的 Launcher 原版 `e/g.run()` 颜色提交点声明该标志并设 `dimAmount=0`，沿用原版主题及透明主题壁纸分区取色，不增加调暗、不改导航栏行为。复用 `LauncherSettingBridge`，未新建 Manager 或改四指动画。新包安装后用户连续四指左右切换并明确确认“现在颜色能跟随”；随后采样为 `isLight=false`、`mDarkIntensity=0.0`。这是本次四指热切换验证，不能用设置页切主题替代。9 月 24 日记录中的“未修复”是当时状态，现由此项验证更新。
- **微信分身搜索图标**：关闭桌面设置中的分身显示时，旧代码按包名清掉主用户和分身用户的全部搜索图标；模型默认用户 `-1` 与索引主用户身份不一致，同一快照重复 hydration 又会取消界面回调。现按包名加用户身份清理，统一默认主用户，合并同快照刷新回调；失效任务不再回填缓存或消费新请求。`OriginalQuickSearchActivity` 同时按源版本和快照版本刷新图标。用户已确认开启再关闭微信分身后正常；最终包再次搜索 `weixin`，微信结果与图标可见。
- **搜索与窗口引用**：搜索匹配在开始、逐条处理和排序前检查查询版本，中止过期工作，保留原有排序和最终界面发布门控。`StatusBarHeightCompat` 的静态弱键表旧监听器反向强持有 Activity/DecorView，现使用弱 Activity 引用，并在 Launcher `onDestroy()` 显式解绑；不改变状态栏高度计算。没有以自然 GC 导致的 PSS 下降宣称泄漏或流畅度已量化改善。
- **主题预览**：大图解码和逐像素手机屏幕遮罩转到现有后台线程池，弱引用与请求 token 保证只回填当前页面；大图缓存限制 8 MiB，小图限制 2 MiB，并在内存紧张和配置变化时清缓存。缓存淘汰不回收 View 仍在使用的 Bitmap。缩略图加载完成只更新仍绑定该主题的 ImageView，移除逐图延后整页 `notifyDataSetChanged()`，避免重绑、占位图和缓存反复淘汰。最终包真机本地主题五个缩略图完整显示；详情连续预览蓝色、格子、经典蓝、蓝色后，最终勾选与蓝色大图一致，未点击“设定”更改用户主题。
- **安装包审计**：最终签名 APK 为 57,039,610 字节（54.40 MiB），相对设备基线 57,035,514 字节增加 4 KiB，未声称瘦身。主要体积来自原版 Textures（约 23.2 MiB）、theme_preview（约 9.0 MiB）及嵌入设置资源 APK（压缩后约 5.6 MiB）。未发现大于 100 KiB 的完全重复资源组；已压缩图片进一步无损 ZIP 压缩收益有限。保留原版主题、设备布局和兼容资源，不为了减包压缩主 dex、resources.arsc 或移除资源；这些改变可能影响加载性能或原版效果。
- **验证与边界**：标准 `build.bat` 完成，最终版本为工作区已有 `v1.5.8/33`，v1/v2/v3 签名与 16 KiB 对齐通过；V2458A 保留数据安装成功，受控 Launcher 启动后 AndroidRuntime 未见异常。真实 SearchIconBackend 回归脚本通过主/分身隔离、整包失效、默认用户和同快照双回调测试；现有解锁脚本通过生命周期及 XML 时间换算测试（非真机帧时间证明）。状态栏策略只启用于已核对 ROM 的 vivo Android 16；其他 ROM、透明壁纸多明暗场景、20 宫格及文件夹/解锁高帧率视觉仍未覆盖，本轮未修改其原版几何或动画。证据保存在 `build/performance-search-20260930/`。保留已有无关工作区改动，未提交或推送；本轮未更新 `MEMORY.md`。

**备份恢复问题与翻页动画字段**

- Android 16 / V2458A 真机复现：恢复旧备份后“立即备份”报 `Layout limits exceeded: pages=1001 items=62`，备份与恢复均无法继续。检查设备旧归档及 `clean_launcher`、当前原版 `data/A.smali`：原版固定预置 1000 条 `table_pageinfos`，其中大量 `pageIndex=-1` 空槽。恢复导入器追加当前新安装应用时，直接插入新页面，生成第 1001 条；后续恢复前快照和备份均被 1000 页上限拒绝，回滚也随之失败。此前对 `:reload` 进程识别的推测没有获得日志支持，相关试验改动已撤除。
- 导入器现优先复用最小编号的原版空槽；空槽耗尽时才在 1000 页上限内插入新记录。对设备已存在的第 1001 条，导出器仅在可明确识别空槽并一一映射全部溢出有效页面时生成 1000 页快照，保留条目和页面；不满足条件仍报错，避免静默丢数据。设备现有第 6 个板块从 `_id=1001` 映射到预留 `_id=6`。
- `launcher_page_animation` 原已列入便携设置白名单，但偏好未写入时不会进入归档。备份现沿用原版读取顺序，以 Launcher 偏好优先、`Settings.Global` 回退，显式记录有效值（默认 `0`）；备份和恢复预览增加“桌面翻页动画”，按原版存储值 `0/3/4/6` 显示四种动画，旧备份缺失该字段时显示“此备份未记录”。
- 真机保留数据安装验证包后，“立即备份”进入预览并保存 `2026-09-30 18-31.slauncherbackup`；回拉检查为 1000 页、62 条目，实际板块 6 个，第 6 板块 `_id=6`，且 `settings.json` 含 `launcher_page_animation=0`。用此备份恢复完成 `RESTORE_VERIFY_COMPLETE itemCount=62`，撤销入口出现，再次进入备份预览成功且无需溢出映射。随后实际恢复 9 月 28 日旧备份，日志 `RESTORE_PAGE_SLOT_REUSED id=6 pageIndex=5`、`RESTORE_VERIFY_COMPLETE itemCount=60 preservedNewItemCount=4`；最终恢复 18:31 的当前状态备份，校验为 62 条目。未清除应用数据。
- 撤掉无证据的恢复保护进程识别改动后，最终源码再经 `build.bat` 构建、v1/v2/v3 签名校验，包另存 `build/launcher-android16-backup-restore-fixed.apk`，原工作区构建产物已恢复。V2458A 保留数据安装最终包，备份预览显示 6 个板块、62 个应用及“桌面翻页动画：默认动画”；同一当前状态备份再次恢复后，撤销入口时间更新为 18:45，桌面正常显示，再次进入备份预览仍为 6/62 且无溢出映射。该次最终包的恢复日志只留有 `RECOVERY_JOURNAL_FOUND state=COMMITTED`，故以 UI、撤销记录和再次备份作为应用完成证据；Android 9 此次未重测。

**最终状态（2026-09-29—30）**

- **设置任务与动画**：桌面设置仍由 `ThemeChooserActivity` 承载。Android 9 沿用 Launcher 同任务入口，Android 14+ 的桌面设置入口使用 `NEW_TASK`，交由系统处理 HOME 与边缘返回。二、三级页在设置任务仍存活时保留。Android 16 独立任务的 HOME 系统缩窗已在 V2458A 上验证；普通主题切换仍可能先缩小设置任务，再播放原版桌面主题动画，尚未解决。期间尝试的 Launcher 内覆盖层、自绘缩小、主题专用退出动画和跨任务交接试验均未作为当前方案保留。
- **加载与导航栏**：冷重载使用原有加载动画窗口，Launcher 初始化弹窗不再显示“正在初始化”等文案；所有 `SmartisanProgressDialog` 共用加载动画的文字区域现统一隐藏，仅显示动画。主题切换的共用进度窗口不再被误改为冷重载黑色全屏窗口。“隐藏虚拟键”偏好覆盖 Launcher 自有设置与加载窗口；具体 ROM 的系统窗口仍需实测。加载文字最后一项修改已完成标准构建，尚未逐个触发场景做真机视觉验收。
- **备份与预览**：点击“立即备份”直接进入“备份桌面”二级预览页，准备期间只在页面内显示占位值，不叠加加载弹窗；“开始备份”才保存已校验的暂存归档。备份和恢复共用预览，图标包、图标大小、默认应用图标框、桌面文字大小、状态栏高度和 Dock 高度连续排列；“桌面文字大小”与“状态栏高度设置”位于同一卡片。图标大小读取主偏好，旧备份仅在缺少主值时迁移旧副本；旧归档缺少的新设置显示“此备份未记录”。
- **图标归档根因**：在线图标源缓存实际使用应用包名作为 PNG 文件名，旧备份筛选仅接受十六进制文件名，导致源图标被跳过。现接受安全的包名式 PNG 文件名并沿用旧文件名兼容；校验和恢复使用同一规则。单个损坏或缺失的自定义图标会回退应用原图，不再使整份备份/旧档读取失败。图标包本体仍由设备已安装应用提供，备份保存选择信息，不打包第三方图标包 APK。
- **备份真机证据**：vivo X21A / Android 9 保留数据安装后，实际点击“立即备份”进入预览并完成保存；新文件 `2026-09-30 14-49.slauncherbackup` 为 1,111,654 字节，归档含 27 张在线图标源 PNG，原始图标数据合计 1,099,885 字节。设备上的 2026-08-17 / v1.5.6 旧备份（7,298 字节）通过文件选择、归档校验并正常显示恢复预览。未点击“开始恢复”覆盖当前桌面，因此旧备份的实际应用阶段仍未实测。备份文件大小取决于当时已缓存的图标和自定义图标数量，不能只按固定 MB 数判定成功。
- **其他保留修改**：设置返回的图标阴影清理复用原版 GL 事件；快捷桌面在缺少已保存开关值时默认关闭；翻页动画预览的手机屏幕区域对齐主题预览。后两项及 Android 14+ 跨 ROM 效果未完成最终真机验收。
- **验证范围**：最终源码通过项目标准 `build.bat` 构建，`build/launcher-signed.apk` 为 `v1.5.7/32`，v1/v2/v3 签名验证通过，并在 X21A 保留数据安装成功；备份保存和旧档预览已在同机验证。构建与安装不能代替 Android 16 主题切换、所有加载场景和旧档实际覆盖恢复的真机验证。`MEMORY.md` 未因这组反复试验更新。

### 2026-09-28

**【已废弃】设置主页 HOME 覆盖层可行性原型（仅测试入口，未迁移设置功能）**

原型只验证 Launcher 覆盖层可移除，未完成设置功能迁移且源码已删除；不得恢复为正式设置架构。当前任务归属以 2026-09-30 的最终状态为准：Android 9 同任务，Android 14+ 使用 NEW_TASK。

**备份预览与恢复清单统一（Java/资源编译通过，真机待验）**

- **问题**：备份流程原本在命名弹窗后直接生成归档，没有内容预览；恢复页虽已有布局统计，但图标包、尺寸类设置未展示，“需要重新授权的功能”只有空值行。
- **实现**：备份先在缓存暂存并校验最终归档，再用该归档展示预览；用户命名并点“开始备份”后只将同一文件复制到 SAF 目录，避免预览与保存重新采样产生差异。备份和恢复共用预览页；顶行展示备份名称，恢复名称从所选文档读取。增加图标包、图标大小、状态栏适配/微调、Dock 高度和设置范围说明，并列出 6 个换机后需检查/重新开启的权限功能。原有文件名冲突覆盖确认和归档格式保持不变。
- **设置文案**：移除“隐藏虚拟键”开关下方“部分系统可能不生效”说明，开关本身及行为不变。
- **范围说明**：权限依赖的开关状态仍不写入归档；新设备需手动检查动态天气/自动定位、联系人搜索、角标提醒/滑动清除和系统面板手势。壁纸、应用安装包与应用数据、系统授权仍不备份。旧归档缺少字段时显示“此备份未记录”。
- **验证**：全量 `launcher/tools/java` 在 Android 36 bootclasspath 与现有 unsigned APK classpath 下 Java 8 编译通过；maintained 设置资源 `aapt2 compile` 通过；`git diff --check` 通过。未运行完整 `build.bat`，因为它会覆盖当前工作区已暂存的 APK 产物；未安装或进行真机备份/恢复往返。
- **风险**：实际 SAF 目录授权、名称冲突覆盖、预览取消清理、跨设备缺失图标包/主题包及权限重新开启提示仍需真机验收。未更新 `MEMORY.md`，未提交或推送。

**解锁时间单位与 GL 会话交接修正（构建/状态测试通过，真机待验）**

- **根因**：`Eb.update()` 默认以 `fx=20 × 0.06=1.2` 推进全局动画，XML 的 `totalDuration=1.32` 原样送入引擎时，标称时长被压到约 1.10 秒；这是时间单位问题，不是 120Hz 固有倍速。原版 XML 各单元有自己的分段和错峰，标称时间不能代替整场动画或首帧可见时长的实测。
- **计时修复**：`animations/c/k.updateUnlockTiming()` 在创建解锁曲线前读取 `Eb.getAnimationTimeScale()`，统一换算解锁的 duration/delay，毛玻璃背景也先读取同一换算结果。默认 1.32 秒转换为 1.584 引擎秒，再由 1.2 倍时钟推进，恢复 1.32 秒墙钟时间基准。没有改 XML、插值器、几何和全局 `Eb.update()`，翻页/文件夹等动画保持原计时；100ms 掉帧上限仍保留，严重卡顿会影响实际总耗时，不宣称严格逐次 1320ms。
- **起播条件**：现有单一 `LauncherBelowKeyguardCompat` 消费有效 dismiss 前检查 Resume、interactive、Keyguard unlocked 和 Window Focus；无广播的原有 locked-resume 兜底保留。GL 帧回调只在已有有效会话及解锁证据时补一次条件检查，处理焦点回调与 Keyguard 状态更新先后的差异，不新增固定延迟、Handler 轮询或第二套 Coordinator。Focus/GL 回调不等于 SurfaceFlinger 已经展示画面，起播与可见首帧仍须录像验收。
- **GL 完成与取消**：移除接收器中入队即 `PREPARE_READY/FORCE_FINISH_COMPLETE` 的假完成；`ea` 在真实 `wr()` 后检查 `Kd()`，`da` 在真实 `Fd()` 后确认结束，`ca` 在 GL 初始化后才登记播放派发。原有三类事件在构造时保存 Session ID，拒绝已取消/旧会话的初始化和播放；Timeline 回调保存 GL Session ID，旧 FINISH 不会清除新会话。旧清理事件若发现更新的 GL 会话已准备，直接忽略，避免清掉新画面。连续可见桌面再次锁屏不再被已消费会话的重复信号规则吞掉。
- **修改文件**：`LauncherBelowKeyguardCompat.java`、`ia/ea/ca/da.1.smali`、`animations/c/b.smali`、`animations/c/k.smali`、`view/Eb.smali`、`view/vc.smali`；新增 `tools/tests/unlock/run_tests.py`。未新增 Manager/Service，未改 Manifest、数据库、原版 XML 或全局动画倍率。
- **验证**：宿主状态测试直接编译当前 Java Owner，以 Android/Receiver stub 检验真实准备回执、未获焦点/仍锁定的门控、重复广播、连续锁屏、旧事件/回调、晚到清理、应用覆盖返回、非桌面锁屏和兼容偏好快照；另检查 60/90/120/144Hz 下 XML 标称时间换算。测试不代表实际 Smali/GL 调度或视觉验收。完整 `build.bat` 通过；最终 APK 为 v1.5.7/32，v1/v2/v3 签名与 16K zipalign 检查通过，Smali 新回调描述符与本轮编译的 Java 方法签名一致，`git diff --check` 无空白错误。
- **风险与验收**：ADB 无在线设备，未安装本轮包。必须实测 12/20、兼容开/关、普通/透明/毛玻璃主题、指纹/人脸/密码、连续锁屏及动画中打开应用；重点观察焦点晚到造成的等待、首次毛玻璃解锁、首帧丢失及触摸恢复。未更新 `MEMORY.md`，未提交或推送。

**解锁板块锁图标与标题间距微调（构建通过，真机待验）**

- 当前黑色验证页使用原版 `lock_icon_0016.png`；图片本身 126×102 像素，可见 Alpha 仅位于 x=41..83、y=25..79，图标容器内的透明下缘叠加原版 18dp 图文间距，使锁的可见部分离“解锁板块”较远。只将该验证页图标画面下移 8dp，不移动标题、圆点和键盘，也不改原版图片及设置密码页。
- `build.bat` 完整构建通过；ADB 无在线设备，图标与文字的最终可见间距仍待真机截图确认。

**Dock 手势设置归位及密码提示原版几何对齐（构建通过，真机待验）**

- “反转 Dock 栏手势方向”及其说明从“强迫症选项”移至“搜索与桌面手势”，位于“交换搜索与系统面板手势”下方；原 `dock_slide_reverse_enabled` 偏好键、默认值与 `SLIDE_DOCK_ACTION_TYPE` 应用逻辑不变。
- 对照原版 `security_control_unlocker.xml`、`unlocker_hint.xml` 和 `unlocker.text.main`：原版提示区位于键盘上方剩余区域中央，图标、提示文字、六点依次排列；字号取 `unlocker_txt_main`，图标尺寸、图标到文字、文字到圆点间距及圆点尺寸/间距均来自原版资源。此前兼容页“解锁板块”为 24sp、“输入密码”为 19sp，错误提示单独切到原版字号，造成输入正常态与错误态的字号和位置跳变。
- 黑色板块解锁页现按原版提示区层级和尺寸资源排列；白色设置验证页保持其白色键盘和标题栏，输入/错误提示共用原版字号、圆点间距及同一位置。错误文字从原版 `unlocker_invalid_password` 资源读取，黑色页圆点继续使用原版空心/实心/红色素材，白色页因背景不同保留可见的正常圆点配色并复用原版红点。未改密码摘要、校验、重试、键盘触摸和动画时长。
- `build.bat` 完整构建通过；ADB 无在线设备，尚未确认不同屏宽/密度下黑白页正常态、错误态的实际文字基线与圆点像素位置，也未确认 Dock 开关迁移后的页面点击和切换效果。

**桌面设置名称与说明文案梳理（构建通过，真机排版待验）**

- 对照实际开关语义和当前设置页命名，将搜索入口改为“搜索与桌面手势”，搜索开关改为“启用桌面搜索手势”，方向开关改为“交换搜索与系统面板手势”，Dock 方向开关改为“反转 Dock 栏手势方向”；“状态栏设置”和“快捷桌面”沿用已确认名称。搜索开关只控制桌面手势入口，未关闭其他搜索入口；Dock 方向受原版 `launcher_switching_orientation` 影响，因此说明不再写死默认左右方向。
- 主设置页为搜索入口补现有 `TipsView` 样式说明，同时更新状态栏、快捷桌面、搜索及方向开关下方的中英文说明。快捷桌面说明明确首屏右滑和开启后左侧进入设置；搜索及系统面板说明继续随方向开关切换。未修改偏好键、开关默认值、手势分发、设置导航或左侧标签与右侧开关的触摸归属。
- 追加“隐藏虚拟键”说明：主设置页及“强迫症选项”中同名开关下方均使用已有 `TipsView` 样式，说明覆盖 Launcher 自有界面并提示部分系统可能限制效果；开关行为不变。
- `build.bat` 完整构建通过，最终 APK v1.5.7/32，v1/v2/v3 签名通过，`git diff --check` 无空白错误。ADB 无在线设备，主设置页新增说明行的换行与间距、两种手势方向文案切换及中英文实际显示仍待真机验收。

**隐私密码错误反馈对照原版（构建通过，真机视觉待验）**

- 原版 `UnlockerHintView.ka()` 在错误时显示 `unlocker_invalid_password`，将六个 `SecurityPinImageView` 切换到 `pin_dot_red`，对点容器按 0/10/26/42/58/74/90/100% 的关键帧以 0/-25/+25/-25/+25/-25/+25/0 px 摇动 400ms；原版 APK 包含空心、实心、红色点资源，错误文字色为 `unlocker_tips_wrong`。当前兼容页此前只 Toast、立即清空点，无法呈现原版反馈。
- 现有 `MaintainedLauncherSettingsHost` 的黑色板块解锁页和白色设置验证页共用错误提示方法：错误文字、原版红点、400ms 摇动和现有错误震动后恢复输入。黑色页正常状态改用原版空心/实心点，点大小、间距及错误文字大小读取原版 dimen；保留各自黑白键盘与密码验证逻辑。设置页二次设置密码不一致的提示仍走原有流程。
- `build.bat` 构建、Java 编译、签名完成；ADB 无在线设备，未验证两种页面的可见帧、实际震感及不同 ROM 资源缩放。真机需分别输入错误的六位密码，检查提示文字、红点、摇动、震动、400ms 后清空与再次输入。

**隐藏虚拟键恢复 Launcher 内页面生效（构建通过，真机待验）**

- 历史核对：仓库最早可追到的开关实现是 `7c99b57c`（2026-06-03），当时 `launcher_hide_navigation_bar` 只在 `Launcher.smali` 的创建、恢复、焦点回调调用；更早的 `c3134ad8` 把设置项隐藏，`maintained` 当前文案也限定桌面主界面。用户明确记得首次实现时所有页面均隐藏；现有入库代码无法还原该体验来源，不能把旧文档的“只在桌面”当作对用户实测的否定。
- 本轮首次尝试的全局 `ActivityLifecycleCallbacks` 在 V2458A/Android 16 启动时触发 `NoClassDefFoundError: android.app.Application$ActivityLifecycleCallbacks$-CC`，导致桌面闪退；该尝试已完整撤除，随后恢复版覆盖安装后 Launcher 能进入前台。最终方案只复用已有 `MaintainedLauncherSettingsHost.applyLauncherNavigationBarSetting()`：Launcher 主窗口保持原逻辑，设置、主题、搜索、密码确认页的现有入口按偏好隐藏导航栏；加载窗口沿用先前独立于偏好的无系统栏策略；开关点击立即作用于当前设置窗口。未新增 Manager、Service 或全局回调。
- 本轮最终 `build.bat` 通过，APK badging 为 `v1.5.7/32`，`git diff --check` 无空白错误。构建后 `adb devices -l` 没有在线设备，故最终包尚未覆盖安装和实测各页面的虚拟键显示；三键导航、手势导航、短暂过渡窗口和不同 ROM 仍须真机检查。不要把构建通过记为视觉通过。
- 追加根因修正：`NativeLauncherSettingsHost` 与 `MaintainedLauncherSettingsHost` 的重启加载 fallback 都会调用 `setSystemUiVisibility(0)`，主动清除隐藏虚拟键；maintained 的原版进度 Dialog 显示前后也没有应用窗口隐藏策略。现统一复用已有 `LoadingUiWindowCompat`，并为快捷方式确认 Activity/Dialog 补齐隐藏偏好。完整 `build.bat` 再次通过；最终包仍待设备重新连接后的安装、三键导航截图及页面往返验证。
- 全 Launcher 窗口续修：设置页 `tuneWindow()` 原来只写 `LIGHT_STATUS_BAR`，会覆盖隐藏导航标志；现在同一主线程紧接着应用开关。现有设置宿主的 12 个 Dialog 展示入口与 Smartisan 进度 Dialog 在显示前后复用同一导航栏策略，搜索菜单 Dialog 与快捷桌面 PopupWindow 也在自己的窗口/内容根上按偏好设置 `HIDE_NAVIGATION` 和 `IMMERSIVE_STICKY`。这是系统栏隐藏调用，不是黑底遮挡。完整构建通过；未连接手机，首次重载过渡窗口的可见首帧、三键/手势导航以及 ROM 是否临时重置系统栏仍待真机录像验证。
- 首次重载交接补口：`LauncherColdReloadCoordinator.beginReload()` 在成功启动 `:reload` 后，立即对旧 Activity 窗口仅隐藏导航栏；`ReloadTransitionActivity` 在 `onCreate` 内容前以及 Resume/Focus 继续使用现有加载窗口策略，且覆盖页首帧后才结束旧进程、新桌面首帧后才撤覆盖页。加载窗口不依赖开关，开关开启时其他 Launcher 自有窗口按同一偏好隐藏。普通应用不能凭 Manifest 中声明的 `WRITE_SECURE_SETTINGS` 就修改全系统导航策略；当前不写系统级 `policy_control`。构建通过，具体 ROM 的系统启动窗口是否在交接前显示一帧仍待设备录像。

### 2026-09-27

**原版图标 MD5 命中误重试导致冷启动耗时（同机真机改善，交互回归待续）**

- V2458A/Android 16 受控冷启动及宫格重载确认，Activity/GL 首帧约 0.12–0.15 秒，完整 `Model/Page ready` 修复前约 4.4–5.78 秒。前两页约 1.3–1.8 秒用于图标来源，纹理 cache miss 为 10/12；`:reload` 过渡页交接约 0.4–0.6 秒，并非完整桌面内容就绪点。对照 maintained 的持久化 `ItemInfo.iconData`，当前继续保留原版 `Aa/e/s` 生成和主题/动态图标/分身语义。
- 根因是原版 `Aa.a(...)` 在图标 MD5 与数据库相同返回 `null` 表示无需写库，而当前静态图标 `e/s.a(ItemInfo,true)` 把它当作无图最多重做 4 次。临时计时证实普通图标来源选择重复 4 次；PackageManager 精确解析通常低于 1ms。`Aa.smali` 仅在 MD5 命中分支通过已有 `ItemInfo.Oe()` 取已存字节并交给 `iconRawData`，`e/s.smali` 在 `ContentValues=null` 时使用这份已存数据；真正变化仍走原版生成与写库，读取失败仍保留原重试/默认图标兜底。未引入新缓存表和失效策略。
- 同机修复后 12 宫格受控冷启动 PID 22829 的 `Model/Page ready=2398/2399ms`、前两页 546/493ms，图标来源 205/275ms；最终包补齐可空 `ItemInfo` 保护并重装后 PID 3492 的 `Model ready=2852ms`。20→12 宫格新进程 PID 24735 的 `Model ready=2983ms`，前两页 810/753ms，之前同机回 12 的新进程为 5783ms。20 宫格首页及 12 宫格修复前后图标截图已看，动态时钟/日历、文件夹、微信、相册位置可见正常；12→20 新进程缺少完整 Startup 标记，不能声称它的最终内容耗时。两次先行尝试的 PM 小优化及临时分段日志无实测收益，已撤除。
- 完整 `build.bat`、APK 覆盖安装、真机冷启动和宫格往返、`git diff --check` 通过。未取得跨机/多轮统计、图标包/分身/手动图标选择的完整回归，也未取得解锁动画可见帧录像。用户另报首页与负一屏往返偶发整屏触摸失效、锁屏再解锁恢复；ADB 从首页完成一次有效打开/关闭，关闭后无残留 Quick Desktop PopupWindow，快速连续注入未形成可靠的多轮打开，仍须在真正卡住当刻抓焦点/输入窗口及日志。

**加载动画去文字与启动/解锁对照（构建和受控启动通过，动画视觉待验收）**

- 对照原版 `widget/c.q` 只设置 `loading_progress` 的行为，当前正常初始化、`:reload` 过渡页和设置触发的桌面重载均隐藏加载文字，继续使用已有动画。主题切换内部传入的消息仍供状态栏调暗语义判断；备份进度、失败提示和重试按钮继续显示。修改 `widget/c.smali`、`ReloadTransitionActivity.java`、`MaintainedLauncherSettingsHost.java`。
- 普通初始化和主题切换的原版 `widget.c` Loading Dialog 过去未统一应用 `LoadingUiWindowCompat`，只有带冷重载 token 的初始化以及 `:reload` 过渡页会主动隐藏系统栏；现所有原版 Loading Dialog 在 `show()` 前后调用同一窗口策略，独立于“隐藏桌面虚拟键”设置。只影响加载窗口，不修改桌面虚拟键偏好和动画资源。构建、安装通过，三键导航与不同 ROM 的实际隐藏效果尚待截图验收。
- V2458A 上先回拉已安装旧包作 QA 基线，再保留数据安装本次 APK。受控启动 PID 10773 的 GL 首帧 124ms，Model/Page ready 4432/4433ms；前两页分别 1033/1038ms，图标来源解析 598/737ms，纹理缓存命中均为 0。这些只定位阶段，当时尚未改动图标缓存或原版模型链，也没有取得宫格切换专属耗时或 maintained 同机 A/B；后续实际修复及计时见本文件顶部记录。
- `build.bat` 完整成功，`git diff --check` 无空白错误，最终 APK `v1.5.7/32` 的 v1/v2/v3 签名与 16K 对齐通过。APK 安装成功且 Launcher 顶层 Activity、普通桌面截图正常。加载动画瞬间截图、12↔20 宫格切换、真实锁屏解锁及微信往返当时尚未视觉验收；后续验证见顶部“解锁动画当前结论”。本项目用户可选布局只有 12 和 20 宫格。

**感知阴影续做文档与桌面手势、解锁残留收口（构建通过，待真机交互验收）**

- **【已废弃】早期感知阴影兼容实验**：该实验已删除，不能按当时“尚未恢复”的结论判断当前功能；正式感应光影实现、GPU 出图与验证见 2026-10-02 合并记录。`ICON_ILLUMINATION_HANDOFF.md` 仅保留历史入口，不恢复旧实验。
- 解锁 Session 的现行触发、微信返回误播根因与本轮修正统一见下方“解锁动画当前结论”；此处不再维护重复的临时结论。
- 快捷桌面候选手势加入第二根手指时撤销捕获与开启候选，把后续多指事件交还原版手势识别器；去掉宿主 attach 后 700ms 与 HOME 后 300ms 的预先 GL 截图，正常单指右滑仍于手势 `DOWN` 请求当前桌面截图。减少非打开操作的全屏读回与后台模糊工作。
- `build.bat` 完整成功，APK v1.5.7/32，v1/v2/v3 签名与 16K 对齐通过，`git diff --check` 无空白错误。新包已在 V2458A 保留数据安装成功，系统包信息与 Launcher 顶层 Activity 均确认正常；受控 `am start` 因 Launcher 已在前台仅交付给现有实例。ADB 单指注入未产生可确认的快捷桌面日志，尚未完成微信往返、锁屏解锁、四指/单指混合触摸录像；因此不把用户现象或总体流畅度标为真机 PASS。旧包同设备日志曾显示约 4.8 秒才 Model/Page ready，但此次新包未取得相同条件的结构化新样本，不能用其证明改动后的初始化速度。图标缓存命中及快捷桌面手势截图延迟仍需同设备计时归因，不提前修改原版模型或缓存链。

**解锁动画当前结论（合并 9 月 24–25 日未推送试验）**

- **现行实现**：本项目只向用户提供 **12 和 20 宫格**，由原版 `fa.wr()/fa.Lr()` 与 `UnlockAnimationXML` 负责画面；仓库内的 `unlock9/16.xml` 只是原版/maintained 对照资源，不能称为本项目的可选布局。当前 12/20 解锁 XML 标称 `totalDuration=1.32` 秒，并已移除移植版额外的 `navigationbar` 动画。`Eb.update()` 与 maintained `MainView.update()` 均按 uptime 帧差、100ms 上限及 `fx × 0.06` 推进。没有保留刷新率分档或 120ms 锁屏预滚。
- **触发与兼容**：在桌面确实可见时建立锁屏 Session；有效 `USER_PRESENT/action_keyguard_to_dismiss` 只允许消费一次，无广播的 ROM 以 locked Resume、解锁及 Focus 兜底。兼容开关沿用设置键 `launcher_unlock_wait_for_focus`，当前仅在播放时发现原版场景未初始化的分支补发 init，**并不改变已有场景的起播时点或动画时长**。**【已废弃】照搬 maintained 的 `isUnLockAnimationRunning()` 到 `r.Jd()` 的判断**：把预初始化 Timeline 误判为正在播放，导致兼容模式停在准备画面；该判断已删除，不得恢复。
- **微信返回误播的真机根因**：V2458A / Android 16 记录中，微信前台时 Launcher 在 `1790522015.104` Stop（屏幕亮、Keyguard 已解锁、Session 仍 active），`1790522015.393` 才收到 `USER_PRESENT`；旧条件要求 Stop 时已经 pending，因此未取消，广播在 Launcher 停止时仍 `COMMIT_PLAY`，回桌面 Resume 后 614ms 才 START。现 Stop 只要已解锁且 Session 未消费即取消，并禁止已停止的 Launcher 在 dismiss 分支立即播放；已消费但动画未结束的 Stop 继续 force-finish。这个问题属于错误资格判断，不能靠缩短/延长 XML 遮掩。
- **快慢与丝滑度边界**：同机一次有效直接回桌面 Session 中，`USER_PRESENT→START≈9ms`，Start 时 Focus=false，约 37ms 后获 Focus，`START→FINISH≈1094ms`。12/20 XML 的 1.32 秒在当前和 maintained 共用的默认 `20×0.06=1.2` 推进倍率下对应约 1.10 秒墙钟时间；这与实测相符，不是单独把本项目调快。XML 中部分单元的各段时长之和仅 70/130 帧；maintained 的可选布局与本项目不同，可能改变主观节奏，但尚无同机 A/B 可见帧录像证明具体视觉差异。现行兼容开关只补未初始化场景，不能延长时间或推迟直接 dismiss 的起播。
- **验证状态**：本轮最新代码完整 `build.bat` 通过并保留数据安装到 V2458A。新一次微信路径在 Stop 时 `UNLOCK_CANCEL_NOT_DIRECT_HOME`，其后 USER_PRESENT 为 `UNLOCK_SKIP_NO_SESSION`，返回桌面无新的 `COMMIT_PLAY`；用户肉眼确认这次返回没有看到残段。GL 在 Resume 后曾报一次 stale start 并立即 force-finish，仍需高帧率录像排除单帧闪现。普通直接回桌面的 Session 仍 START/FINISH 各一次。兼容开/关与加载窗口虚拟键视觉尚未验收。**【已废弃】早期“兼容模式等待 Focus”“强制刷新率档位”“误用 `r.Jd()`”方案**均已被现行实现取代，此处只记录失败机制，不再逐次列构建流水。

### 2026-09-24

**搜索 T9 输入选项与主题状态栏图标颜色交接**

- 四指切主题状态栏不同步 ADB 复核（未修复）：V2458A/OriginOS 16 在蓝色主题四指热切换后，桌面标签白色而状态栏深色；安装的 `lightblue` 主题 APK 中 `status_bar_icon_color=#ffffffff`。临时诊断包日志确认原版颜色链在文字主题更新附近已向窗口提交白色 `ffffffff`，WMS AppearanceRegion 与 SystemUI LightBarController 均报告 `isLight=false`（期望浅色图标），但 StatusBarTransitionsController 的 `mDarkIntensity` 仍为 `1.0`（深色）；设置页选主题经 Activity 返回/窗口交接则显示正常。尝试在文字更新点追加普通主题提交、显式 `WindowInsetsController` 外观设置以及跨帧外观切换，用户真机四指复测均仍异常；这些无效代码和临时日志已撤销，不把构建/提交状态视为视觉 PASS。后续需收集同主题设置页成功与四指失败的 Window/SystemUI 状态差分，定位 OriginOS 着色状态未刷新或原版热切换的窗口交接缺口；不得通过全局强制白色、无条件冷重载或随机延时掩盖透明主题的壁纸分区取色。
- 【已废弃】解锁动画 9 月 24 日旧方案：已由 2026-09-27“解锁动画当前结论”统一替代；本节其余记录仅涉及当日搜索、主题和设置项。
- T9 设置文案归位：原布局将“开启后，从 DOCK 栏向上滑动……”的搜索入口说明放在新增 T9 开关之后，视觉上误作 T9 描述。将搜索入口说明移回搜索总开关下，T9 下独立显示“开启后，使用原版T9键盘，关闭后使用系统键盘”；同时补英文资源，不改开关行为。
- 快捷桌面“音乐与快捷支付”左侧详情入口：页面原本已有启用后进入 `showMedia()` 的回调，但共用 `SettingItemSwitch` 默认拦截开关外的触摸，该行没有开启标签导航，导致左侧无响应。只为此行启用 `setLabelNavigationEnabled(true)`；右侧仍只负责开关，关闭时左侧不进入详情，其他卡片行仍保持纯开关。完整构建、v1/v2/v3 签名、vivo X21A 覆盖安装通过；在原本开启状态下真机点击左侧进入含三项设置的详情页，AndroidRuntime 无崩溃。关闭态左侧不进入详情由现有 `isCardEnabled()` 门控，未另行切换用户开关实测。
- 三键盘反馈补齐：搜索 T9 原版按下态已有 `btn_pressed.9.png`，本次为每次 `ACTION_DOWN` 补一次 `KEYBOARD_TAP` 系统触感反馈，点击/松开继续由 View 常规状态处理。解锁板块与验证隐私密码共用 `addPasswordKeypad()`，原代码已在 DOWN 调用一次 `KEYBOARD_TAP`，但触摸事件全部消费且从不设置 pressed，状态 drawable 也只有常态；现用原版 `btn_pressed.9.png` 构建 pressed 覆盖层，DOWN/UP/CANCEL 显式置位和清除 pressed，纯色 fallback 也补按下态。沿用系统触感设置，不强制绕过用户关闭的震动设置；错误密码额外提示震动仍保持原逻辑。完整构建、T9/maintained 资源包按下图检查、v1/v2/v3 签名、vivo X21A 覆盖安装及 Launcher 启动无崩溃通过；三场景真机触摸、消失/取消与实际震感尚待验收，未创建或更改用户密码。
- 主题状态栏同步补修：原版主题对象切换后延后 500ms 跑 `W.run()`，桌面文字资源则在 `t.r(theme)` 的 `Constants.initByTheme()` 中更新；两者不是同一次提交，主题动画完成后可能残留旧 Window 的状态栏明暗。现在 `t.Tf()` 完成回调里再执行原版 `W.run()`，用当前主题和壁纸顶部/底部区域采样结果更新状态栏/导航栏；保留原版延后任务兜底壁纸稍晚可读的情形。透明主题仍按不同壁纸区域分别取色，不强制状态栏与桌面文字同 RGB。完整构建、v1/v2/v3 签名、vivo X21A 覆盖安装与受控 Launcher 启动通过，清空日志后未见 AndroidRuntime；连续四指切换、透明主题不同明暗壁纸仍待真机回归。
- 搜索：`搜索与上下滑手势` 增加默认关闭的 `T9 键盘输入` 开关，保存在 `launcher_settings/search_t9_enabled` 并进入现有偏好备份白名单。开启时 `OriginalQuickSearchActivity` 禁止系统 IME 因焦点弹出，在原有搜索页面底部显示十二键面板；按钮图来自原厂 QuickSearch 3.0.0/101 的 `btn_*_classic_normal.9.png`，数字直接写入原搜索框，继续走已存在的 T9 拼音首字母索引与异步结果链。关闭后仍用系统输入法。收起键恢复结果区高度，点击搜索框可重新打开面板。
- T9 回归修正：首版将原始 360×201 的按键素材塞入固定 52dp 行高，360dp 宽屏时纵向被压缩；改为按素材宽高比和当前搜索内容区实测宽高等比计算四行，空间不足时同步收窄整块键盘并居中，结果区底边随高度差更新。原数字索引把应用名、包名、完整拼音和首字母拼成一个连续串后做 `indexOf`，`39` 可命中包名或中段且跨字段误命中；纯数字查询现在只取应用标签数字前缀、标签拼音首字母前缀或完整拼音前缀，非数字文本检索不变。
- 联系人/按键反馈追修：联系人在异步结果线程中临时取得共用匹配模型，但首次评分前没有等待拼音准备，故“抖音”联系人输入 `39` 漏检；现于同一结果线程评分前完成模型准备，保留原有联系人开关、权限和电话号码前缀命中。原版 `DialButtonView` 按下时在普通按键上方绘制 `btn_pressed.9.png`，移植版此前漏带该资源；现用原始按下素材叠加到每键的 pressed 状态，抬起恢复常态。
- 状态栏：`e/g.run()` 中原先先写 DecorView 的 `LIGHT_STATUS_BAR` 标志，再用旧 Window attributes 更新主题颜色，可能覆盖即时图标明暗；现同一原版颜色解析链先更新 Window attributes，再设置 DecorView 标志。不改变主题选择、透明主题及颜色资源。
- 四指切主题追修：原版主题切换排队执行 `W.run()`，再把状态栏颜色执行体 `g.run()` 投递到主线程；快速连续切换时，旧主题颜色任务可能晚于新主题 UI 执行。`g.run()` 执行前对比其主题对象与当前 ThemeManager 对象，过期任务直接退出，不改动当前主题资源与文字链。初版误调用仅限同包访问的 `X.access$000()`，真机报 `IllegalAccessError`；已改用公开的 `X.eg()` 当前主题入口。最终包真机重装后 `am start` 进入 Launcher，清空日志后的 AndroidRuntime 无崩溃。尚需实际四指连续切换验证是否完全覆盖用户现象。
- 验证：完整 `build.bat`、资源 APK 中 T9 drawable 检查、最终 APK v1/v2/v3 签名通过，`git diff --check` 通过；真机设置页显示 T9 开关。最终修正包在 vivo X21A 经原生“继续安装”确认后 `adb install -r` 返回 `Success`，桌面可启动。用户澄清实际搜索入口是桌面上滑；改用上滑后 ADB 注入手势仍未成功进入搜索页，故数字 `39` 实际结果、键盘真机视觉、系统 IME 切换、四指主题切换后的状态栏即时颜色仍待真机验收。其他分辨率仅按可用内容区等比布局设计，未做多机实测；不能把构建或单机安装视为跨设备功能 PASS。

### 2026-09-16

**图标框冷重载、双入口设置行与显示设置备份**

- 图标框：名称改为“默认应用图标框”。原确认回调仅发 per-package 图标刷新，没有启动冷重载；现同步保存成功后复用 LauncherColdReloadCoordinator 的进程交接，失败提示并尝试恢复原值，不修改 Geometry 或其他图标来源。
- 双入口设置行：此前 SettingItemSwitch 一律拒绝开关外的 DOWN，误拦截了原有二级菜单。仅为“动态天气和日历”“快捷桌面”显式开放标签导航，仍由原有 enabled 判断控制是否进入；右侧独立切换，其他标签保持不能切换。
- 备份：状态栏自动适配/高度、Dock 高度、图标大小、文字大小已有白名单；补入 com.smartisanos.launcher_prefs/launcher_default_icon_shape_v1。同时将这些设置的隐式默认值写入新备份，避免默认备份恢复时无法覆盖后续修改。恢复继续走原有类型化 commit 与冷重载；不迁移设备安全区缓存。
- 验证：最终 build.bat 成功，git diff --check 通过，APK badging 为 com.smartisanos.launcher / v1.5.7 / 32，v1/v2/v3 签名通过。当前 adb devices 无设备，尚未验证真机点击、确认后的进程切换及备份恢复往返。旧备份缺失的图标框设置不能追溯补出，需重新备份。未更新 MEMORY.md。

### 2026-09-15

**自适应 DEFAULT 圆形四端平边修正**

- 根因：Adaptive 分支先把图层画入带 inset 的 circleBounds，再把整个含透明边的画布映射至 circleBounds，重复缩进使圆周四端缺少底图覆盖。此前把中间位图平边归因于偏好异步保存的判断没有证据，应撤回该根因结论。
- 修改：DefaultIconCircleRenderer v6 将自适应图层画到完整源画布，按不透明外轮廓确定内接裁切区域，再通过抗锯齿 oval 映射到既有圆形包络。最终 Geometry 与原版尺寸分类沿用现有实现。
- 验证：build.bat 成功，ADB 覆盖安装成功；build/circle-v6-install.png 真机截图中微信、aShell、抖音四端平边消失。git diff --check 通过。按比例计算，不含设备分辨率常量；其他分辨率真机尚未验证。
- 同轮设置项修改：图标、文字与状态栏高度调整的零值在行尾及选择项显示“默认”；数值存储保留原语义。负一屏反向手势修复尚待专项真机验收。

#### DEFAULT 系统原图放大圆形裁切

- **根因**：旧 `DEFAULT_VISIBLE_FIT` 在最终 Composer 内按透明可见边做 98% 对齐，却绕过了原版 `IconColor.ColorInfo.resize -> icon_size_origin_resize` 内容框；第一版圆形实验又新增浅色底板并把原图缩到 75%，造成用户截图中的底色不一致。随后仅把整张透明画布放大仍会保留圆角矩形/八边形透明角，视觉继续小于真正圆形图标。
- **修改**：仅在有效来源确定为 `DEFAULT` 后生成 256×256 canonical source。传统位图从原 Drawable 自身 Alpha 外轮廓求可覆盖中心的内切裁切框，放大并直接裁成圆形，不生成或猜测额外底色；AdaptiveIcon 分别绘制原 background/foreground。圆形外径采用 5 个现有完整圆形 IMPROVED 资源 Alpha 外径中位数 `0.9791667`。Smali 保留原版 `IconColor.resize` 分类并把结果交给统一 Composer，Composer 仍从当前 `LayoutProperty.icon_size_origin` / `icon_size_origin_resize`、现有 rasterScale 和用户倍率得到最终内容框；未改 `IconVisualMetrics`、Cell、Scene、Folder、Dock、QuickLaunch、ActiveIcon、文字或动画。
- **设置与缓存**：应用图标页新增“默认应用图标样式：跟随应用/圆形”，默认圆形。切换时只解析并刷新当前有效来源为 DEFAULT 的普通应用，动态日历/时钟和受管来源不进入该集合。缓存键加入 shape、renderer version、source canvas version、IconColor 内容框类型、组件/用户/source identity；最终版本为 `raster:v24-default-inscribed-circle`。
- **测量**：5 个基准 IMPROVED 圆形资源的 Alpha 外径比例为 Chrome `250/256`、Spotify `190/192`、Telegram `248/256`、Edge `188/192`、Phone `188/192`，中位数 `0.9791667`。vivo X21A 的 1080px 截图中，十二宫格 100% 下 `vivo 官网`、`录音机`、`aShell You` 的水平可见外径均为 `188px`，单格宽 `360px`，即 `52.2%`。
- **验证**：`audit_icon_contract.py`、`git diff --check`、完整 `build.bat`、`aapt2 dump badging` 与 v1/v2/v3 签名检查通过；APK 为 `v1.5.7/32`、SHA256 `C9AA4127775F15BA8DB3598422E200FD899616CBBA68094AAF1AB2160B73ED34`。保留数据安装到 vivo X21A/Android 9，系统安装器完成时间为 `2026-09-15 15:09:05`；最终截图确认默认原图底色直接铺满圆面。十二宫格与二十宫格的 100%/150% 均完成截图复核，跟随应用/圆形 A/B 可切换并已恢复十二宫格、100%、圆形。30 次交替翻页前后 PSS 为 `232853 -> 236271 KB`，Graphics 均为 `144620 KB`，未见 Launcher FATAL/VerifyError/OOM/ANR。
- **边界与风险**：当前设置页可选图标范围实际为 80%–150%，因此没有伪造 50% 结果；80% 本轮也未单独截图。只验证 vivo X21A/1080×2280/Android 9，尚未覆盖 1220/1260/1440、Android 12–16、多 ROM、全部 AdaptiveIcon/传统位图、Folder 开合和 ActiveIcon 全矩阵。30 次翻页 PSS 的约 3.4 MB 差值是单次过程样本，不能据此证明长期内存完全无增长。覆盖安装命令返回厂商错误 `-200`，但手动点击系统安装器后 `lastUpdateTime` 与最终包版本已更新，Launcher 正常启动且 ART 未报验证错误。

### 2026-09-14

#### QuickDesktop 性能 Gate 验证（未修改产品代码）

- 原始完整指标保存在 `build/quickdesktop_gate_metrics.csv`，单位沿用 dumpsys 的 KB；此前记录把 KB/1000 的近似值写作 MiB 不严谨，本次以原始值为准。冷启动采样仍含启动异步任务，不能作为稳定空闲基线。
- 累计 1/5/10/20/30 次完整开关日志确认 30 次打开、30 次关闭，无 Launcher ANR/崩溃。PSS 为 318612（冷启动）、424477、446815、457931、517717、518457 KB；30 次后约 +30/+60/+180 秒分别回落到 368709/368493/368217 KB。Graphics 静置保持 247310 KB，Bitmap 39605 KB，ViewRootImpl 回到 1，线程数稳定 48。支持本轮未观察到持续累积，不能归因 Graphics 常驻差额，也不能由总线程数证明某个 Executor 的归属。
- 临时 shell 注入器通过 InputManagerGlobal 使用连续 downTime 完成约 20/40/70% 屏宽位移后反向，独立三组均返回关闭且无窗口残留。随后交替 30 次循环出现部分有 DOWN/UP 但无展开进度的样本；存在页面位置/同时人工操作干扰，尚未完成隔离复现，不标记反向 Gate 全通过。展开与关闭自动动画中立即反向尚待验证。
- 用户配合完成关闭、完全打开、半开、展开自动动画中、关闭自动动画中五组锁屏/解锁。日志确认 CANCEL/Stop 清理，无 Launcher PopupWindow 残留，最后可再次完整打开关闭。解锁 Timeline 视觉是否不变仍需用户确认，未修改解锁代码。
- 旧 UiAutomator runner 因 Android 16 缺少 RepetitiveTest 失败；首版临时注入器因 InputManager 初始化失败崩溃，均为测试工具故障而非 Launcher 崩溃。产品源码与 APK 本轮未改，MEMORY.md 未更新。结论：内存回收 Gate 通过本轮样本，完整交互 Gate 待收口，暂不宣称冻结。

#### 快捷桌面触摸窗口清理与截图瞬时内存收口

- **根因与范围**：快捷桌面展开后使用全屏 `PopupWindow` 并切换为 `touchable=true`，但普通 `Launcher.onStop()` 在没有快捷动作待处理时直接返回，`QuickDesktopHostView.onDetachedFromWindow()` 也没有通知 Controller 解除窗口与静态 Host；异常动画/生命周期边界存在透明窗口继续拦截桌面触摸的风险。GL 捕获同时分配全屏 `byte[]`、DirectByteBuffer、原始 Bitmap，后台又创建第二张全尺寸翻转 Bitmap；1260×2800 单份约 13.46 MiB，重复捕获还会各自创建线程并到主线程应用阶段才淘汰旧结果。本次只修改 QuickDesktop 宿主、捕获与 Launcher 销毁入口，未动 RootView 原版手势门控、动画参数、卡片布局、图标、文件夹、解锁动画或 12/20 宫格。
- **修改**：Controller 新增单一幂等 `cleanup(reason, releaseHost)`，统一取消 pending capture、先将 PopupWindow 设为不可触摸、再 dismiss、重置 gesture/action 状态，并在完整 detach 时清除 Root/Host 与截图引用。重新 attach、Launcher Destroy、普通 Stop、Host 非预期 detach 和正常关闭均复用该入口；预期的 PopupWindow dismiss 通过窄状态标记避免 detach 回调递归销毁可复用 Host。`vc.b()` 删除仅用于零填充 DirectByteBuffer 的全屏 `byte[]`；捕获结果直接作为 sharp Bitmap，sharp/blur 两个 ImageView 在显示层做 Y 翻转，取消第二张全尺寸翻转 Bitmap。后台处理改为单线程 Executor，并在缩放、模糊和主线程应用前分别检查 generation；关闭/detach 会主动使旧任务失效。
- **验证**：`git diff --check` 与完整 `build.bat` 通过，最终 APK 保持 `v1.5.7 / 32`，v1/v2/v3 签名有效，已保留数据覆盖安装到当前 vivo 1260×2800 设备。真机首次展开背景方向正确，窗口按 `touchable=false -> true` 交接；连续 10 次完整展开/关闭均命中 `QD_CLEANUP reason=host-closed`，关闭后 WindowManager 不再存在 Launcher PopupWindow。快捷桌面打开时切到系统设置，日志命中 `reason=launcher-stopped` 且窗口消失，返回后仍可再次完整展开/关闭；快捷桌面打开时按 Home 也立即清理，随后桌面继续响应手势。未见 `FATAL EXCEPTION` 或 ANR。
- **内存边界**：打开时一次样本约 `PSS 459 MiB / Graphics 296 MiB / Bitmap 46 MiB`；关闭基线约 `369/231/46 MiB`。连续 10 次后立即采样因 GC 延迟升至约 `525/292/82 MiB`，静置约 60 秒后回落到约 `377/247/40 MiB`，Views/ViewRootImpl 从 `22/6` 回到 `12/1`。说明本轮没有观察到逐次永久累积或窗口残留，但 Graphics 仍比关闭基线高约 16 MiB，SMEngine/OpenGL 长期纹理占用尚未归因，不能宣称整体 195 MiB Graphics 已解决。
- **风险**：当前仅验证一台 vivo、12 宫格和 10 次循环；ImageView 显示层翻转、Stop 强制关闭与 Latest-Wins 捕获仍需其他 ROM、锁屏/解锁、快速半程反向手势和 30 次循环验证。没有引入截图有效性复用，也没有改主题缓存或拆分 `MaintainedLauncherSettingsHost`，避免扩大优化范围。未更新 `MEMORY.md`，未提交或推送。

#### 状态栏与桌面图标/文字调整设置收口

- **界面修改**：主设置项改名为“状态栏设置”，说明“可以自定义状态栏高度”按快捷桌面同款 `TipsView` 放在卡片外；详情页“顶部留白微调”改为“状态栏高度调整”。高度弹窗改成选择后点“确定”才保存并冷重载，底部保留“取消/确定”，删除页面内“恢复默认”和“应用并重启桌面”。应用图标页将两项改名为“桌面图标调整/桌面文字调整”，右侧均显示相对默认值：默认为 `0`；图标档位为 `-20/-10/0/+10/+20/+30/+40/+50`，文字档位为 `0/+2/+4/+6/+8/+10`。
- **文字不生效根因与修复**：首次实现只修改 `LayoutProperty.text_font_size`，但普通桌面标签最终由 `DesktopLabelMetrics.resolveDesktopTextSize()` 按分辨率重新计算固定字号，前面的值会被覆盖。调整量现由该最终字号 Owner 叠加，并只同步 12/20 宫格的标签几何后备字段，不遍历 Folder 或其他模式；已有奇数试验值规范到最近偶数档。偏好加入现有备份白名单，变更继续复用冷重载协调器。
- **验证**：`git diff --check` 与完整 `build.bat` 通过，最终 APK 保持 `v1.5.7 / 32`，已保留数据覆盖安装到当前 vivo 设备。ADB UI hierarchy 确认主设置说明位于卡片外，状态栏页无“恢复默认/应用并重启桌面”，高度弹窗含“取消/确定”；应用图标页显示“桌面图标调整 0”“桌面文字调整 +6”，文字弹窗完整显示六档。真实选择 `+10` 与恢复 `+6` 均完成冷重载，日志分别命中 `DESKTOP_TEXT_SIZE_APPLIED extra=10 modes=2` 与 `extra=6 modes=2`，真机截图可见桌面文字放大，未见 `FATAL EXCEPTION`。
- **风险**：当前仅验证 12 宫格和当前 vivo；20 宫格已接同一最终 Owner 但尚未切换宫格逐档截图，其他 ROM 也未验证。设备最终保留用户原试验值就近对应的 `+6`。未更新 `MEMORY.md`，未提交或推送。

- **设置页顶部留白色带**：新增 padding 未绘制背景，露出 Window 默认底色。公共设置内容容器改用与状态栏一致的 `0xfff7f7f7` 背景。完整构建与覆盖安装成功，当前 vivo 真机截图确认新增顶部留白的异色色带消失；其他 ROM 尚未验证。

- **状态栏高度同步设置页**：设置 Activity 仍由系统预留顶部空间，未使用桌面手动增量。`StatusBarHeightCompat.settingsTopSpacing()` 读取已保存配置，`MaintainedLauncherSettingsHost.setSettingsContentView()` 在公共内容容器设置额外顶部留白，覆盖使用该入口的主设置与二级页；草稿不触发实时布局。保留系统安全区，不将设置标题推入系统状态栏。
- **验证与限制**：完整构建、覆盖安装通过；当前设备 UI hierarchy 显示系统内容起点 y=147，设置标题起点 y=175，与 +8dp（560dpi 下 28px）一致。其他 ROM、负微调以及全部二级页切换未完成真机验证；此前桌面滑动无响应仍未确认根因，不宣称修复。

### 2026-09-13

#### 搜索结果与历史标签的图文视觉对齐及历史图标稳定性

- **原版对照与根因**：原版 QuickSearch 的 `empty_view.xml` 使用 `FlowLayoutEx`、`wrap_content` 标签、6dp 横间距和 10dp 行间距，按历史顺序与内容实际宽度自然换行，并不会拉伸标签或均分每一行；原版结果行则将 30dp `ImageView` 和文字容器分别放在 60dp 行的几何中心。因此当前 360dp 可用宽度下一行只有 3 个较长标签、右侧留下不足以容纳下一项的空间，本身符合原版算法。真正导致截图中同一批历史在 `3+3` 与 `4+2` 间跳动的是图标消失后标签测量宽度缩短：当前历史绑定只读取容量有限的已解码图标缓存，缓存未命中时没有主动请求解码；标签重新创建后便退化成纯文字。当前搜索复用 Launcher 图标位图，其透明画布的可见重心与现代系统字体字形重心不等同于 View 的几何中心，故即使布局属性与原版相同，结果行图标仍平均比文字高约 9px，历史图标高约 3–4px。
- **修改**：保留现有 `HistoryFlowLayoutCompat` 的原版顺序、自然换行、6dp/10dp 间距及原版标签背景，不新增均分、重排或固定四列。每个应用历史标签在已解码缓存未命中时通过现有 `SearchIconBackend` 主动请求图标，并用来源代次、标签条目键和父容器三重校验避免异步结果写到已回收标签；索引图标预热完成后也会重新绑定历史区。标签关闭字体额外上下留白并保持 `CENTER`；结果图标增加 2.5dp 向下视觉补偿，历史标签图标增加 1dp 向下视觉补偿。按用户要求将历史标签字体由 13.5sp 调整为 13sp、图标由 18dp 调整为 17dp、图文间距由 5dp 调整为 4dp，并在保留原版 9-patch 上下内边距的同时把左右内边距各减少 1.5dp。
- **验证**：`git diff --check` 通过，完整 `build.bat` 构建通过；最终 APK 为 `v1.5.7 / 32`，v1/v2/v3 签名有效，SHA-256 为 `960097DE1CB93A571C80FEBA114827B1BA06EC6386F6DD16F802A2D156A1196D`。已保留数据覆盖安装到 V2458A（1260×2800）；搜索结果 6 行的“文字可见重心减图标可见重心”由修复前平均 `8.91px` 收敛为 `-0.09px`，历史标签前三个稳定样本由 `2.57–4.06px` 收敛为 `0.06–1.50px`。ADB UI 边界确认历史容器宽 `1134px`，收窄后的前四项“淘宝 / QQ音乐 / 儿童乐园 / 天气”连同三个 6dp 间距共占 `1133px`，仅余 `1px`，8 条应用历史真机显示为 `4+4`；所有历史项均显示图标，Activity 可正常拉起，日志未见 `FATAL EXCEPTION` 崩溃。
- **风险**：本次验证的是当前 360dp 宽设备和当前前四项；仍保持原版按内容自然换行，若前四个应用名称更长，仍可能少于 4 项，短标签则可能多于 4 项。若要任何内容都严格固定四列，需要截断文字或改成网格，属于另一种非原版布局。图标缓存冷启动时可能短暂等待后台解码，但完成后会写回仍有效的标签；包卸载、主题或图标来源变化仍按现有失效策略刷新。未修改搜索结果列表、Dock、虚拟键、解锁动画兼容或其他设置逻辑。未更新 `MEMORY.md`，未提交或推送。

#### 搜索历史按搜索结果直接生成唯一记录

- **根因**：搜索框键盘“完成/回车”会写入 `TYPE_QUERY` 纯文字记录，随后点击应用结果会再写入 `TYPE_APPLICATION` 应用记录；历史仓库此前仅对“类型与内容都相同”的项去重，因此“微信”“抖音”分别同时显示带图标应用项和无图标文字项。
- **修改**：键盘提交前先在当前应用索引中按完整桌面名称匹配：匹配到应用时直接写入一条 `TYPE_APPLICATION` 记录，匹配不到才写入一条 `TYPE_QUERY` 文字记录，不再经过“先写文字、点击后再补应用”的正常流程。历史仓库以显示内容为唯一记录键，应用另按包名更新；历史展示也会按当前索引解析记录，能找到应用就显示图标并直接启动，找不到才保持纯文字查询。读取旧 `entries_v1` 时仍会一次性清理 1.5.7 已经产生的双记录，但这只属于旧数据迁移。
- **验证**：完整 `build.bat` 构建通过，最终 APK 为 `v1.5.7 / 32`，v1/v2/v3 签名有效，SHA-256 为 `34D8BA6C51CDEF099D89BE9C2C356F22B26E2CD78A01B5F80B15D8872A6A1F2A`。已覆盖安装到 V2458A（1260×2800），Launcher 与原版搜索页均可重新拉起，未见最终安装后的 `AndroidRuntime` 崩溃。旧数据迁移日志已确认删除原有 2 条重复项；ADB 的系统 `input text` 无法可靠输入中文，因此“中文精确匹配后直接记录应用”的最终交互仍需手动提交确认，不以构建结果代替真机行为验收。
- **风险**：完整桌面名称相同的两个应用在历史区共用一个显示记录，搜索结果列表本身仍会分别显示。应用改名或卸载后，历史项会按当前索引重新判断是否能显示图标和直接启动。未修改搜索索引、搜索结果排序、联系人、Dock、虚拟键或解锁动画兼容逻辑。未更新 `MEMORY.md`，未提交或推送。

#### Dock 恢复 v1.5.6 高度基准

- **根因**：1.5.7 的桌面布局适配把 `dock_height` 与 `cell_height_dock` 归入 Placement 字段，按真实屏幕高度除以所选资源 profile 高度缩放。在 1080×2280 设备匹配 1080×2340 profile 时比例约为 `0.974`，因此无论“隐藏桌面虚拟键”是否开启，Dock 都会比 1.5.6 略矮。
- **修改**：只从 Placement 特例中移除 `dock_height` 与 `cell_height_dock`，让两者重新走 1.5.6 原有的 `factorFor()` 全高缩放规则。透明桌面的页面高度与边距仍使用 Placement 比例；未修改虚拟键显示开关、图标尺寸、宫格、文件夹或解锁动画兼容逻辑。
- **验证**：确认 Git 标签 `v1.5.6` 中两个 Dock 字段均走通用高度缩放，并对照 1.5.7 引入 Placement 特例的提交定位回归；`git diff --check` 与完整 `build.bat` 构建通过。最终 APK 为 `v1.5.7 / 32`，v1/v2/v3 签名有效，SHA-256 为 `2CB06C0BD9360B906D4655A6988D4B515BDFEF4836E6234A4FF5F47D1B35D400`。ADB 当前仅连接 V2458A（1260×2800），不是问题截图对应的 1080×2280 设备，故未覆盖安装、未完成同机截图测量，不把视觉效果标记为真机通过。
- **风险**：修改仅影响竖屏桌面的 Dock 容器高度和 Dock 单元高度；不同分辨率 profile 下会回到 1.5.6 的比例语义。透明桌面的主体 Placement 仍保持 1.5.7 修复，需真机确认 Dock 与最后一行宫格间距没有新的视觉偏差。未更新 `MEMORY.md`，未提交或推送。

### 2026-09-12

#### 解锁动画兼容模式 — 默认预滚不变，可选等待桌面焦点

- **范围与原因**：用户放弃此前整批未提交优化后，只恢复解锁兼容功能。部分 ROM 上默认 120ms 预滚可能在锁屏遮挡期间已经推进，用户只能看到动画后半段；本次不修改原版动画资源、时长、倍率或播放事件，只增加下一次锁屏会话生效的可选门控。
- **修改**：强迫症选项增加“解锁动画兼容模式”，默认关闭。关闭继续沿用 `RESUME_PRE_ROLL`；开启后不排队预滚，必须等 Keyguard 已解锁且 Launcher 获得窗口焦点才允许唯一播放。偏好在会话 arm 时快照，切换开关不会打断当前动画，并纳入设置备份白名单。
- **验证**：独立 Session 测试覆盖两种模式、先 Focus/先解锁、无 USER_PRESENT、重复事件、连续锁屏、旧回调、中途切换设置、普通应用返回、解锁进入其他应用及关闭动画，均通过；`git diff --check`、完整 `build.bat` 与 v1/v2/v3 签名通过。最终 APK 为 `v1.5.7 / 32`，SHA-256 `4B696665DB39D41F1F1A231DE51DBE1D6094CF1A59BA463D744CF5B441F3BFED`，已在 vivo X21A 覆盖安装并回拉路径哈希核对一致；强迫症选项页实机显示新增开关且默认关闭。尚未替用户执行真实锁屏/解锁，视觉节奏仍待手动验收。
- **风险**：兼容模式会比默认模式晚到窗口获得焦点时起播，某些 ROM 可能感觉衔接略有停顿；Focus 也不等同于 Surface 首帧提交，因此不能仅凭状态测试宣称视觉完全通过。未更新 `MEMORY.md`，未提交或推送。

### 2026-09-09

#### 快捷桌面进入搜索后的返回闪现修复

- **根因**：快捷桌面点击搜索复用了普通外部应用的延迟关闭策略，只设置 `actionLaunchPending`，等待 Launcher `onStop()` 或返回时的 `onResume()` 再关闭宿主。但同 APK 的 `OriginalQuickSearchActivity` 使用透明窗口，Launcher 不一定进入 `onStop()`；搜索退出时透明窗口先露出下面仍打开的快捷桌面，随后 Launcher `onResume()` 才执行关闭，表现为先闪回快捷桌面再回首页。
- **修改**：搜索入口使用独立的 `searchLaunchPending` 两阶段交接：先保留快捷桌面并启动搜索，`OriginalQuickSearchActivity` 窗口首次获得焦点时调用 `onSearchSurfaceReady()`，再同步隐藏并释放底层 PopupWindow。若目标按普通不透明 Activity 流程令 Launcher 进入 `onStop()`，原有生命周期兜底仍会关闭宿主并清理标记。音乐、支付、设置和六个快捷工具继续沿用目标覆盖后关闭策略；未修改搜索退出动画、首页手势、快捷桌面滑动或桌面分页。
- **原版与参考边界**：当前正式搜索仍是同 APK 的 `OriginalQuickSearchActivity`，没有恢复独立 QuickSearch APK、截图、PixelCopy 或模糊背景。`clean_launcher` 的原版入口使用独立 QuickSearch Provider，与当前 Launcher 内透明 Activity 的生命周期不同；maintained 没有当前快捷桌面宿主，不能直接提供修复实现，因此本次只在两者交接边界做最小兼容修复。
- **验证**：`git diff --check` 通过，完整 `build.bat` 成功；最终 APK 为 `v1.5.7 / 32`，v1/v2/v3 签名有效，SHA-256 为 `6FF2BB1408161B310FB51F38AC62A4969371AD9CB3FF92796C205218D81A0883`。构建完成后 ADB 无在线设备，未执行覆盖安装和真机动画录制，因此当前状态为实现与构建通过，不标记视觉 PASS。
- **风险与回归**：该交接避免“先关快捷桌面再等搜索启动”可能产生的进入前桌面空档，也避免返回时仍保留快捷桌面；仍需在真机检查首次与重复进入搜索、系统 Back、搜索栏取消、输入法显示/隐藏、横条/三键导航及搜索启动失败回退。其他快捷桌面动作只增加搜索专用标记隔离，不改变目标覆盖策略。

### 2026-09-08

#### 快捷桌面固定快捷工具跨品牌解析

- **根因**：便签入口只尝试 Smartisan 的固定 Activity 和 `com.android.notes`，魅族便签等厂商包即使已经安装也无法命中，最终错误提示“未安装便签软件”。录音、计算器、日历和时钟虽已有部分 Android 标准 Intent 或少量厂商包兜底，但覆盖顺序和品牌范围不一致，同样可能在其他 ROM 上误报未安装。Android 本身没有统一的“打开便签”Intent，因此不能仅靠一个通用 Action 解决。
- **修改**：保持六个原版固定图标与点击热区不变，只扩展 `QuickDesktopActions` 的动作解析。便签依次尝试 Smartisan 原入口、Smartisan/魅族/小米/OPPO/vivo/华为/荣耀/三星等已知应用包，最后复用项目现有系统图标识别语义，按 Launcher Activity 的包名、类名和“便签/笔记/备忘录/Notes/Memo”桌面名称解析，并优先系统应用。日历、录音、计算器和时钟先走 Android 标准 Category/Action，再走厂商包和同类身份兜底；城市服务继续按用户选择的支付宝/微信快捷入口处理，不伪造不存在的 ROM 城市服务 API。
- **原版与参考边界**：`clean_launcher` 和 maintained 仅提供 Smartisan 固定组件或旧数组参考，不能覆盖现代厂商包；本次复用了当前 `IconManager` 已验证的 package/component/label 分类原则，没有创建新的 Manager/Service、没有修改原版手势、卡片布局或支付协议。
- **验证**：`git diff --check` 和完整 `build.bat` 通过，`v1.5.7 / 32` APK 已用 `adb install --no-incremental -r -d` 保留数据覆盖安装，v1/v2/v3 签名有效；本地产物与设备 `base.apk` SHA-256 均为 `FAACE84F78700522FBFFDA53F45FABB5C65B84C046D3D58B087EC99648FA0CA0`。V2458A/Android 16 的系统解析结果分别为日历 `com.bbk.calendar/.MainActivity`、录音 `com.android.bbksoundrecorder/...ReclistActivity`、计算器 `com.android.bbkcalculator/.Calculator`、时钟 `com.android.BBKClock/.alarmclock.HandleApiCalls`，便签包 `com.android.notes/.Notes` 也存在且可启动；安装后未见本轮 `FATAL EXCEPTION` / `AndroidRuntime` 崩溃。
- **风险与回归**：当前没有连接魅族设备，所以 `com.meizu.notepaper` 及其身份兜底属于实现和构建验证，不能写成魅族真机 PASS。各 ROM 若隐藏系统工具 Launcher Activity 且又不实现标准 Intent，仍需取得该机实际 package/component 后补精确候选；身份兜底只在标准入口和已知包均失败时启用，降低误开同名第三方应用的风险。

#### 快捷桌面快速切换与正常旧备份误报损坏修复

- **根因**：快捷桌面打开进度恰好达到 `100%` 时，`settleTo(1)` 的立即完成分支只更新位移便返回，没有调用 `onHostOpened()` 将 PopupWindow 切成可触摸状态；打开动画尚未结束时也要等最后一帧才接管触摸。快速反向滑动因此可能落到下层 `RootView`，既会造成快捷桌面看似卡住，也会让关闭手势继续驱动桌面分页而进入第二页。恢复问题并非归档损坏：恢复预览若被快捷桌面等其他设置路由直接替换，原 READY 状态的 `PreparedRestore` 和全局操作令牌不会经过预览返回回调释放；再次选择任何正常备份时，忙碌状态又被错误编码成 `RESTORE_INVALID_ARCHIVE`，界面遂显示“备份文件无效或已损坏”。
- **修改**：`QuickDesktopHostView` 在打开吸附开始时即调用 `onHostOpened()` 接管下一次触摸，并补齐进度已到终点的立即完成分支；一次触摸未结束时即使内容到达关闭边界也不提前销毁窗口，部分展开状态允许双向水平拖动以支持快速反转。`DesktopRestoreController.validateSelectedFile()` 在用户明确选择新文件时先安全丢弃尚未执行的旧预览，再获取新令牌；真实并发占用改用 `RESTORE_OPERATION_BUSY`，设置页显示“桌面正在执行其他设置，请稍后再试”，不再冒充文件损坏。
- **原版与参考边界**：Launcher 侧继续由原版 `RootView` 负责首页、方向锁和连续打开进度，替换宿主只修 PopupWindow 的触摸所有权交接；未新增第二套桌面分页或手势识别。原版 APK 与 `clean_launcher` 没有当前 `.slauncherbackup` 兼容层，备份修复仅处理当前移植版未执行预览的生命周期，不放宽 ZIP、路径、清单、JSON、校验和或 PNG 安全校验。
- **验证**：四份设备备份（`2026-08-22 10-01`、`2026-09-07 09-09`、`2026-09-08 20-03`、`备份快捷方式`）逐一通过 ZIP 完整性、必需条目、逐文件 SHA-256 和便携图标 SHA-256 核验，确认原提示属于状态误报。`git diff --check` 与完整 `build.bat` 通过，最终 APK 为 `v1.5.7 / 32`，使用 `adb install --no-incremental -r -d` 保留数据覆盖安装成功，设备 `dumpsys package` 确认版本一致。V2458A/Android 16 上已复现“恢复预览被快捷桌面设置替换”的原触发顺序并安装修复包，用户随后确认恢复和快捷桌面当前均正常。
- **风险与回归**：本次真机结论覆盖 V2458A/Android 16 当前手势节奏和上述四份 format v2 备份；Android 8–15、三键导航、不同触控采样率以及 format v1 归档仍未组成完整矩阵。真正截断、校验和不符或内容非法的备份仍会按原安全策略拒绝恢复。

#### 快捷桌面默认开关状态无法备份恢复

- **根因**：`SharedPreferences.getAll()` 只返回已经实际写入 XML 的键，而快捷桌面总开关和四类卡片开关默认均为开启。用户在默认状态创建备份时，未操作过的开关没有持久化键，`settings.json` 因而缺少这些状态；之后关闭开关再恢复，恢复器没有旧值可覆盖，表现为备份和恢复都没有效果。恢复本身已经使用同步 `commit()`，归档也始终包含 `settings.json`，问题不在异步落盘或 ZIP 漏文件。另一个边界是原版 `Constants.sLeftScreenEnabled` 属于进程内手势门控，恢复后的新 Launcher 实例此前没有主动从快捷桌面私有配置重新同步。
- **修改**：`PreferenceBackupCodec` 在编码 `quick_desktop_private` 时不再只复制物理键，而是通过 `QuickDesktopController` 读取总开关、四类卡片、个性签名、默认音乐应用和快捷支付提供方的完整逻辑值，默认状态也明确写入新备份；其他偏好文件的既有白名单策略不变。恢复仍只应用归档中实际存在的字段，因此旧备份缺少快捷桌面字段时不会臆测覆盖当前设置。`QuickDesktopController.attach()` 在每个 Launcher 新实例附着时把已恢复的总开关同步到原版 `sLeftScreenEnabled`，并增加每个偏好文件的字段计数日志用于备份/恢复核验。恢复预览新增“快捷桌面组件”一行，显示四类组件中的启用数量及快捷桌面总开关状态；旧备份缺少完整字段时明确显示“旧备份未包含”，不误报为 0。
- **原版与参考边界**：原版 APK / `clean_launcher` 没有当前移植版的现代 `.slauncherbackup` 与快捷桌面私有配置；maintained 参考项目也没有可直接复用的快捷桌面备份实现。本次只修当前兼容层，没有改原版数据库、手势进度、卡片布局或系统权限策略。
- **验证**：`git diff --check` 通过；两次完整 `build.bat` 均通过，最终 APK 为 v1.5.6/31，v1/v2/v3 签名有效，SHA256 为 `90AFF2CB5039B4B5A89486FF0B0E3BC4048F3A81A7371BE6F912D22A2C54DBB7`，X21A/Android 9 已安装 `base.apk` 与本地产物哈希一致。真机新建的 `2026-09-08 08-42.slauncherbackup` 中 `settings.json` 已确认 `quick_desktop_private` 包含总开关、四组件开关、个性签名、音乐应用和支付提供方共 8 个字段；用户随后执行一次恢复并确认设置重新生效，08:52 日志进入 `confirmStartRestore()` 且未出现 `FATAL EXCEPTION` / `AndroidRuntime`。最终恢复预览真机显示“快捷桌面组件 4 / 4 · 已开启”，Launcher 重建首帧后首页右滑可正常进入快捷桌面。
- **风险与回归**：只有使用本修复版本重新创建的备份才具备完整默认状态；旧备份没有快捷桌面字段时按兼容策略保持恢复前当前值，并在预览中标明未包含。当前已关闭默认全开归档的备份、恢复和预览可见性问题；“部分关闭备份→全部开启→恢复”的组合矩阵，以及 Android 8–16 跨 ROM 恢复仍需后续 Phase 3/5 Gate 覆盖。

### 2026-09-07

#### 快捷桌面 9 月 6–7 日阶段汇总（整体约完成一半）

- **已完成的原版主链**：沿用 Launcher 原 `RootView` 首页右滑入口和连续进度，快捷桌面不是数据库分页、Activity 覆盖层或系统悬浮窗；普通首页与多板块首页均使用本次手势起点的实时桌面截图，按“清晰截图→渐进模糊→暗层→完整内容页”固定层级渲染，整页跟手、悬停、松手吸附、反向退出、Back/HOME 和关闭总开关后的回弹已经收口。
- **已完成的固定内容**：按原 432 宽坐标恢复天气、搜索、音乐、扫码/付款、六个快捷工具和生活信息卡片，并完成跨宽高比等比缩放、整体下移、透明导航横条、搜索图文对齐、温度单位间距、城市显示、个性签名、快捷工具垂直居中及音乐长文本避让播放按钮。音乐接入标准 MediaSession 的曲名、歌手、封面、状态、播放/暂停、上一曲、下一曲与双界面；封面使用卡片同圆角，左上角音乐入口可跳转选定的已安装音乐应用。
- **已完成的设置与动作**：桌面设置主页面使用单一“快捷桌面”标签，右侧 Switch 启停，只有开启后点击左侧才进入设置；每个主设置标签的说明文字位于卡片下方。快捷桌面页的“音乐 & 快捷支付”同样使用一个标签和 Switch，左侧进入二级页，默认音乐应用、快捷支付应用和音乐信息权限均归入该二级页；音乐候选仅枚举已知系统/第三方播放器，不再混入浏览器、抖音、淘宝或微信。搜索、计算器、时钟、音乐及支付宝/微信快捷入口均走目标首帧覆盖与安装状态检查，未安装时给出提示；微信扫码/付款使用其已发布的 Launcher Shortcut 能力，支付角标随提供方切换。
- **已完成的数据边界**：总开关、四类固定卡片开关、个性签名、默认音乐应用和快捷支付提供方均使用快捷桌面私有配置；可移植配置已加入桌面备份白名单，通知使用权仍由 Android 系统管理且不写入备份。固定原版卡片保持固定布局，不进入第三方 Widget 的自由编辑模式。
- **当前完成度与未完成项**：Phase 0–2 已 PASS，Phase 3 的 V2458A 视觉与主要交互已通过，按完整方案（Phase 0–5）计约完成一半。仍需完成备份→清理/迁移→恢复实测、支付宝/微信扫码与付款四组合回归、固定卡片全部开关组合、关闭总开关回弹复测，然后才可将 Phase 3 标记 PASS；Phase 4 的标准 `AppWidgetHost` 选择/绑定/配置/持久化/恢复/删除/排序/尺寸/失效占位尚未开始，Phase 5 的 Android 8/11/12/14/16、宫格、分辨率、字体与导航模式矩阵也尚未开始。

#### Maintained 设置总宿主首轮职责拆分

- **根因**：`MaintainedLauncherSettingsHost.java` 已增长到 19,632 行、约 954 KB；快捷桌面页面绑定、音乐应用筛选、快捷支付选择和通知使用权入口集中混入主题、角标、备份等旧职责，继续在总类追加会放大回归与维护风险。
- **修改**：新增 `QuickDesktopSettingsHost.java`，整体接管快捷桌面设置主页、音乐与快捷支付二级页、个性签名、播放器候选、支付提供方及音乐信息权限绑定。总宿主只保留页面路由、共享 Smartisan 设置壳和卡片 Switch 的原有通用能力，并将必要通用方法由 `private` 收窄为同包可见；布局、Preference 键、点击条件、页面动画和持久化 Owner 均未改变。总宿主降至 19,307 行，本轮没有继续拆其他历史模块。
- **验证**：完整 `build.bat` 通过，APK v1/v2/v3 签名有效；最终 APK 与 V2458A 已安装 `base.apk` SHA256 均为 `B2BC356CADE39D44B4EFC4D130C2C75A9ECB2EF5E6575B46C0C1402663F4CCD5`。真机直接进入“快捷桌面设置”，页面、四个 Switch 与个性签名正常；点击已开启的“音乐 & 快捷支付”进入二级页后，默认音乐应用、快捷支付应用和音乐信息权限三项均正常显示。`git diff --check` 无空白错误。
- **风险**：这里只完成快捷桌面职责的第一轮机械拆分，没有借机重构 1.9 万行中的其他设置模块。后续拆分必须按主题、图标、角标、备份等独立边界逐个进行，并在每次拆分后重复页面导航、返回栈和真机构建 Gate，禁止一次性“大切文件”。

#### 快捷桌面支付徽标原版尺寸对齐（V2458A 真机视觉通过）

- **根因**：项目提供的 `wechat.png` 为 698×698 ARGB 图片，但绿色圆形主体只占约 514×512，四周各有约 13% 的透明留白。此前直接把整张图片画进 23 个设计单位的目标框，实际可见圆只有约 17 个设计单位，因此虽然方形底图和双层图标已经消除，视觉仍明显小于原支付宝徽标。
- **修改**：微信徽标作为 Launcher 运行时资产放入 `launcher/assets/quickdesktop_original/wechat_badge.png`；首次加载时按 Alpha 非透明边界裁去透明留白，再以原支付宝圆盘约 20 个设计单位的可见直径绘制。两个支付卡片继续共用原版锚点 `x=390.5` 及各自原 `centerY`，未增加包图标 fallback 叠层，也未改卡片主体和点击热区。
- **验证**：`build.bat` 完整通过并成功覆盖安装至 V2458A/Android 16；最终 APK SHA256 为 `888490BFC03CE7FBF45769EBFE4A4580C42D3BD0A2BC67E98249FA69972CB405`。HOME 后完整右滑进入快捷桌面的真机截图确认两个微信徽标位置一致、圆形边缘完整、无支付宝残留、无方形底图；用户确认“现在对了”。
- **Gate 边界**：本条只关闭支付徽标的视觉问题。Phase 3 的 V2458A 视觉与主要交互已经过多轮真机反馈，但备份→清理/迁移→恢复，以及支付宝/微信扫码和付款双入口的完整回归证据仍未齐；在这些 Gate 完成前不把 Phase 3 或跨 ROM 状态扩大为 PASS。

#### 负一屏原版固定卡片功能与跨分辨率布局补齐（待真机验收）

- **布局**：继续使用原版 432 宽坐标，不改变已验收的整页跟手层；内容整体从 22 调整到 42 个设计单位。绘制与点击统一使用 `min(windowWidth/432, windowHeight/768)`，短屏按高度缩放、宽屏水平居中。温度单位改为按温度文本实宽定位，搜索图标/文字以同一中心线对齐，快捷工具图标在卡片中垂直居中并删除非原版需求的页码圆点。
- **天气与自定义文字**：头部城市读取动态天气同源的自动/手动城市，不再写死“本机”；原“0步”由负一屏设置中的“顶部自定义文字”控制，空值回退“0步”，最长 12 字符。
- **音乐**：音乐卡读取标准 `MediaSessionManager` 的歌曲、歌手、播放状态和封面；播放按钮随状态切换，未授予通知使用权时仍以公开媒体键控制并即时回写按钮状态。点击唱片区域切换原版紧凑/中央控制两种界面，第二界面提供上一曲、播放/暂停、下一曲；左上角放大后的音乐图标单独进入系统可用音乐播放器。设置页新增“音乐信息权限”入口，说明封面和曲目信息依赖 Android 通知使用权。
- **备份恢复**：备份白名单加入 `quick_desktop_private`，覆盖总开关、四类固定卡片开关和顶部自定义文字；天气手动城市及坐标继续作为可移植配置保存。通知使用权属于 Android 系统授权，按既有安全策略不写入备份，恢复后需用户在新设备重新授权。
- **验证**：`git diff --check` 通过；`build.bat` 完整编译、资源打包与签名通过，APK 为 v1.5.6/31，v1/v2/v3 签名有效，SHA256 `EF1A7DC1D7ACBD647348DC2F60C1D4E7C84B3D4738F0CF5D01FD4D73A0A12AC2`。当前 X21A/Android 9 已安装基线仍为 `444055C9...`；普通 `adb install -r` 未完成覆盖，`adb push + pm install -r -d` 明确返回厂商 `Failure [-200]`。另一台 DT1902A 是不同版本/签名系统桌面，未做危险覆盖。因此本节只能标记实现与构建通过，视觉、点击、权限返回和备份恢复均待真机验证。
- **风险**：第三方播放器只有暴露标准 MediaSession 且用户授予通知使用权时才能提供曲名和封面；部分播放器可能不支持上一曲/下一曲。Android 8/11/12/14/16、不同宽高比和字体缩放矩阵仍未通过，不得将 Phase 3 标记 PASS。

### 2026-09-06

#### 负一屏 Phase 3 设置与固定入口接线（真机验收中）

- **设置结构**：桌面设置主页面仅保留一个“负一屏”开关项；右侧 Switch 直接启停原 `RootView` 入口，点击该项其他区域进入二级设置。二级页提供“音乐 & 快捷支付、快捷工具、日历提醒、生活信息”四个原版固定组件开关。Android 小组件管理区在标准 `AppWidgetHost` 的选择、绑定、配置、删除和恢复链完成前保持隐藏，避免出现无功能入口。
- **内容与动作**：固定卡片按开关动态收拢；天气头部读取桌面动态天气同源 `WeatherBridge` 数据。音乐优先 Smartisan Music，并按 ROM 精确包名回退到本机音乐；计算器、时钟、日历和录音依次使用原版精确组件与 Android 公共 Intent；支付宝扫码/付款保留原 Magic Flow URI。搜索及应用启动改为系统接受目标后延迟 220ms 关闭宿主，用目标首帧覆盖 Launcher，避免先露出一帧桌面。
- **视觉微调**：完整内容层统一向下移动 22 个原版设计单位，点击热区同步移动；Launcher 导航栏继续透明铺底并关闭 Android 10+ 的强制对比底色，目标是与桌面手势横条一致。
- **验证**：上一构建已在 V2458A 确认二级设置可进入，关闭“快捷工具”后负一屏卡片即时收拢且原手势仍能打开。包含天气、点击首帧覆盖、合并主开关、下移及导航底色修正的新 APK 已通过 `build.bat` 和 `git diff --check`，SHA256 为 `678B76A21CC80150AC32E3FF7913005CF6990288AAF581DE971FD5AE65142E2B`；构建后设备断开 ADB，尚未安装，不能标记 Phase 3 PASS。
- **风险与边界**：日历提醒仍遵循原版“无事件时容器为 GONE”的数据驱动语义；天气数据需要用户已开启动态天气并完成定位/城市设置。第三方 Widget、Android 8–16 跨 ROM 与完整分辨率矩阵仍未开始验收。

#### 负一屏 Phase 2 原版运动与背景链路

- **根因与原版证据**：原 `com.smartisanos.magicflow.apk` 已从 `original_apks/` 解包审计。其 `RootView` 将完整 `ContentView.translationX` 限制在 `-screenWidth..0`，背景 `BackgroundView` 不参与横移；背景由当前 Launcher 截图、模糊缩略图和暗层组成。此前内部宿主只有背景空壳，且二次累计位移、半透明截图交叉及旧首页缓存会分别造成无卡片、漂移重影和多页面模式显示旧首页。
- **修改**：保留 Launcher 原 `RootView` 手势门控，以其归一化 `Ad` 唯一映射 `openProgress=1-Ad`，只平移一个完整内容层；加入原版 432 宽度比例的头部、音乐/支付、快捷工具和生活信息首屏骨架并复用 Magic Flow 原图。背景改为清晰截图不透明托底、模糊层覆盖、暗层及内容层的固定顺序；每次有效右滑使用本次手势按下时的 GL 帧，不再复用进入编辑/多页面模式前的旧首页。
- **保持不变**：未加入 PageIndex 或桌面数据库，未修改 `fa.updateScroll()`，未创建 Activity/Service/系统悬浮窗，未申请私有权限；搜索、分页、Folder、HOME 与解锁主链保持原 Owner。
- **验证**：`build.bat`、覆盖安装及设备 APK SHA 一致性通过；V2458A/API 36 上完整打开、反向关闭、Back/HOME、分段拖动和中途悬停已运行。两张同一悬停位置截图像素一致的样本已取得；用户随后明确确认“现在完全正常了”。Phase 2 据此收口，后续视觉微调不得重新引入第二套位移累计或手势中途更换截图。
- **风险**：当前卡片数据与点击目标尚未全部接通，第三方 `AppWidgetHost` 尚未开始；Android 8/11/12/14 与其他 ROM、分辨率及编辑模式完整矩阵仍待后续 Gate。兼容模糊使用预渲染位图，参数与 Smartisan 原私有实时模糊实现不同，最终视觉继续以真机验收为准。

### 2026-09-05

#### v1.5.4 解锁 Resume 预滚语义恢复

- **根因与证据**：本轮安装前的 Focus 版真机样本为 `USER_PRESENT→COMMIT=117ms`，会在 Launcher 已可见后才播放；随后验证的 direct-dismiss 版虽为 `USER_PRESENT→COMMIT=2ms`、`COMMIT→START=11ms`，用户仍能感知晚。另一方面，首次 locked Resume 立即播放会比 USER_PRESENT 提前约 `367–418ms`，用户确认过早。`v1.5.4` 实际源码不是立即播放，而是 `onLauncherResumedForUnlock()` 在确认锁屏离场后通过主线程延后 `120ms` 派发原版锁屏/解锁链。
- **修改**：当前严格 Session 在同一 Session 已 Prepare、Launcher locked Resume、direct handoff 有效且尚未消费时，仅安排一次 v1.5.4 的 `120ms` Resume 预滚。到时仍由唯一 `tryCommitUnlockAnimation()` 授权并派发原版 `q(1)`；若 USER_PRESENT 已先到则立即消费，延后任务自动失效。Pause/Stop、非直接回桌面取消、重复广播及以后 HOME 不补播规则不变。
- **范围**：未改 Unlock XML、Timeline、duration、`Eb.update/Ra.T`、刷新率或 Window/Surface flags。这里的 `120ms` 不是新猜测参数，而是从 `v1.5.4` 对应源码恢复的已存在语义。
- **验证**：`git diff --check`、`build.bat`、v1/v2/v3 签名、覆盖安装、设备同源 SHA 与 ART verify 通过。V2458A 连续两次有效 Session 均命中 `V1_5_4_RESUME_PRE_ROLL`：Resume→Commit 约 `120/123ms`，Commit→Start `4/5ms`，Start 分别比 USER_PRESENT 提前 `236/223ms`、比 Focus 提前 `337/383ms`，每次仅 Commit/Start/Finish 一次；动画运行 `1313/988ms`。最终肉眼节奏仍以用户验收为准。

#### DEFAULT APK 图标可见主体统一

- **根因证据**：新缓存 v19 已实际重建，排除旧缓存混用。真机日志显示全部来源虽使用同一 `192px artwork / 246px texture`，但 DEFAULT 源图透明可见比例从约 `0.75` 到 `1.0` 不等；完整源画布等比塞入必然造成主体有大有小。此前 DEFAULT-only Launcher3 normalizer 只会缩小面积过大的图标、不会放大带透明留白的图标，因此既造成整体偏小，也无法解决本问题。
- **修改**：仅 DEFAULT APK 来源使用已有 alpha 可见边界，将最长可见边统一对齐到 IMPROVED 当前约 `98%` 的 artwork 可见范围并按可见中心定位；IMPROVED/PACK/CUSTOM/RESOURCE 继续保留设计画布，不参与归一化。缓存身份更新为 `raster:v20-default-visible-fit`，所有分辨率按相同比例计算，不含包名、机型或固定物理像素特判。
- **保持不变**：未改 `IconVisualMetrics`、用户 50/100/150% 比例、宫格、Cell、文字、阴影、Folder Preview、ActiveIcon 或动态图标。
- **验证**：Java 编译、完整 APK 构建、覆盖安装与 ART verify 通过；v20 重建日志中典型 DEFAULT 的最长可见边由此前 `144–192px` 收敛到 `188–192px`，正常桌面与编辑页截图均已取得。不同图形的宽高比和内部构图仍由应用原图决定，最终视觉一致性以用户验收为准。

#### 桌面编辑齿轮恢复 v1.5.4 白色资源

- **根因证据**：`Ec.smali` 当前与 v1.5.4 逐行一致，差异来自资源。maintained 的 gear 本体为深灰；`clean_launcher_raw` 是实心白齿轮；Git 标签 v1.5.4 的受控 `build/launcher-signed.apk` 则使用用户记忆中的白色描边齿轮，三组图片均不是同一文件。
- **修改**：从 Git 标签 v1.5.4 自身归档 APK 逐字节提取并恢复 `editBtn_bg/gear/inShadow`，不复制 dex/smali；继续由原版 `Ec` 分层绘制和旋转，不增加 tint 或第二套按钮实现。
- **验证**：恢复后的三张资源 SHA256 分别为 `6504CE57…`、`FDB74861…`、`0CED6D8E…`，与 v1.5.4 归档 APK 完全一致；最终 APK 内再次核对一致，覆盖安装后的编辑模式截图已显示白色描边齿轮。上一轮原始 APK 实心白资源在真机仍显示不符，已由本记录取代。

#### 初始化加载页恢复原版纵向面板

- **根因证据**：Launcher 的 `loading_progress.xml` 及 80 帧 PNG 原本即与 clean 原版一致；差异来自后加的 `OriginalLoadingContentFactory`，它按屏幕宽度生成横向胶囊。原版/maintained 保存的 `smartisan_progress_dialog.xml` 则为 246×160dp 纵向面板、48dp 进度、13sp 单行文案及 12dp 上间距。
- **修改**：加载页工厂恢复上述纵向结构并加载已有 maintained 资源包中的原版 `smartisan_progress_dialog_bg`，资源不可用时才使用同尺寸暗色圆角 fallback；原版进度动画帧不变。
- **验证与风险**：构建、签名、覆盖安装及 ART verify 通过，无新增动画帧或时长；本轮没有为了触发加载页而改主题/宫格，纵向面板的实际动画视觉及首次加载 maintained 资源包的 I/O 影响仍待自然触发时验证。已完成真机测试的 APK SHA256 为 `E9043B9A11B1CE8A29A1B0DFA9F778DC9810B60B38D2844C72E7AEBCD26662F9`，当时设备 base.apk 与本地完全一致。随后仅修正诊断文字及 `.gitignore` 精确资源放行并重建，最终待安装 APK 为 v1.5.6/31、SHA256 `1C74EF1A97A590112F926FCDF82AC9531559585CCB068ED6E5F4FFD4A1459615`；手机在最后一次覆盖前断开 ADB，运行行为与已验证包相同但最终字节尚未装机核对。

### 2026-09-04

#### 【已废弃，已被 2026-09-05 v1.5.4 Resume 120ms 预滚语义取代】解锁动画 App-only 边界：首次 locked Resume 立即预滚动

#### Launcher 铺满布局与导航横条解耦

- 根因：关闭隐藏虚拟键时错误清除 `LAYOUT_HIDE_NAVIGATION`；原版窗口初始化还会重写布局位。顶部布纹则是 `Lc → status_bar.png` 的实际贴图差异。
- 修复：保留上下系统栏布局，仅切换导航控件；隐藏默认 false；复用 maintained 默认主题状态栏资源，保留外部主题与状态图标明暗链。Unlock、Folder、图标几何不变。
- 资源：`launcher/assets/Textures/1080p/status_bar.png` 字节原样来自 maintained 同路径，SHA256 `971c34811d38673d3f839371eb19c9ea3325acec6c89e7d40083c6c50ca85416`；原工作区文件为 `be09aaee…`，原始 APK 对应文件为 `f700636b…`，三者不是同一文件。
- 验证：静态契约、构建、APK 内资源一致性、v1/v2/v3 签名及设备 ART verify 通过。V2458A/1260×2800 真机确认关闭开关时桌面铺满、横条保留、底部标签完整且默认主题顶部平滑；用户确认该效果正常。开启后隐藏横条的最终回切测试因设备被外部操作打断，不扩大为完整开关矩阵。历史“关闭隐藏同时清除底部布局标志”的方案由本记录取代。
- 范围：没有修改图标/文字几何、Folder 或 Unlock 动画。其他主题继续使用各自资源链，未逐主题截图；三键导航和其他 ROM 未验证。一次性专项文档与静态脚本在本轮收口删除，未提交、未推送，未更新 MEMORY.md。

### 2026-09-03

#### 有效 direct-handoff 的 USER_PRESENT 预滚动恢复

- **根因证据**：同一 V2458A 的既有 SurfaceFlinger A/B 中，v1.5.5 七个有效样本均在 USER_PRESENT 同步派发，ANIMATION_START 比 FIRST_PRESENT 早 `8.034–28.800ms`，FIRST_PRESENT 后 `9.254–60.669ms` 才获 Focus。CURRENT 唯一完整可解析样本则在 Layer visible 后约 `35ms` 才因 Focus 派发，形成静止 Buffer 暴露。v1.5.4 与 v1.5.5 的 `ia.1` 触发链和 `animations/c/k` 主体完全相同；v1.5.4“偶尔较短但不先停顿”符合锁屏后预滚动语义。分辨率可能放大设备差异，但不是本次已证明的动画主体计算根因。
- **修改**：仅在 `LauncherBelowKeyguardCompat.tryCommitUnlockAnimation()` 中区分真实 direct dismiss 与无 USER_PRESENT fallback。已有 `unlockDismissPending` 只会在 Session active、Launcher resumed 且 `resumeDuringKeyguardHandoff` 有效时建立；该信号存在时不再要求 WindowFocus，仍要求 Prepare、Resume、interactive、Keyguard unlocked、direct handoff 及未消费。无 dismiss 信号时继续要求 Focus，兼容不发 USER_PRESENT 的 ROM。Commit 前仍先设置 `unlockConsumed=true`，继续走唯一原版 `ACTION_INTERNAL_PLAY → ja.k().q(0)`。
- **保持不变**：未改 `ia.1`、`q(0)/q(1)`、unlock9/12/16/20、Timeline、duration、`Eb.update/Ra.T`、AnimationFrameRateController、Window/Surface flags、Folder、图标或天气；没有恢复 v1.5.4 的 120/250/1200/1500ms 生命周期时间猜测，也没有新增 Handler、Timer、Thread、ROM/分辨率判断。
- **构建与静态验证**：`git diff --check` 与 `build.bat` 通过；APK 为 `v1.5.6/31`，SHA256 `EB5E9FEF80DF710A093BF67D7C74D97B7F750FB819C9418EB556D3E21DBA7C4D`，v1/v2/v3 签名及设备 `cmd package compile -m verify -f` 通过，覆盖安装成功。
- **正常解锁真机验证**：V2458A/OriginOS 16 一轮记录 `USER_PRESENT → COMMIT=0ms`、`COMMIT → START=5ms`；Start 时 Focus=false，约 40ms 后 Focus 到达只记录 `UNLOCK_SKIP_CONSUMED`。本 Session 的 COMMIT/START/FINISH 均为 1，证明提前播放和 exactly-once 同时成立。trace 位于 `build/ab_unlock_evidence/current/run_11/`；该轮缺少分析器所需的完整 GL marker，不能声称已重新取得 FIRST_PRESENT，最终肉眼顺滑度待用户验收。
- **防误播真机验证**：明确打开 `com.android.settings/.homepage.SettingsHomepageActivity` 并确认其为 top 后锁屏解锁，Launcher 日志为 `UNLOCK_SESSION_NOT_ARMED_NOT_VISIBLE_HOME → USER_PRESENT/UNLOCK_SKIP_NO_SESSION`；随后 HOME 的 Resume/Focus 继续 `UNLOCK_SKIP_NO_SESSION`，`PLAY=0`。普通设置返回同样未触发 Unlock Play。
- **范围与风险**：当前只完成 V2458A 一轮正常解锁和一轮设置前台非直接解锁；还需用户肉眼确认停顿消失，并覆盖快速重复、通知/相机直达及不发 USER_PRESENT 的 ROM。未更新 MEMORY，未提交、未推送。

#### 高分辨率解锁延迟：只读复核与测量边界纠正

- **范围**：记录 Folder 实施后，只读检查当前源码、clean_launcher、maintained 的 UnlockAnimationXML 参考及设备已有日志；未改 Unlock Gate、q(0)/q(1)、动画 XML、Timeline、duration、刷新率、Window/Surface flags，未新建诊断 APK、构建或安装。跨设备“1080P 正常、高分辨率延迟”是用户反馈，尚缺同 APK/主题/宫格/刷新率的对应运行证据，不能直接判定分辨率根因。
- **设备与来源**：当前 V2458A 为 1260×2800；设备安装包 SHA256 与 Folder 候选 `A163744E84B82B31475C6C3F2756A21F9CBF7E2CD63D1EF1A7DA59BF09765EDE` 一致。读取的现存日志保存在 `build/unlock-resolution-audit/current-existing.log`，不是本轮受控解锁采集。

| 当日日志 Session | USER_PRESENT → COMMIT ms | COMMIT → ANIMATION_START ms | 最后条件 |
| --- | ---: | ---: | --- |
| 3，20:03:13 | 27 | 5 | WINDOW_FOCUS_TRUE |
| 4，20:03:17 | 42 | 4 | WINDOW_FOCUS_TRUE |
| 5，20:07:28 | 1525 | 2 | WINDOW_FOCUS_TRUE |

- **样本限制**：Session 5 是未标注用户操作的长焦点等待，不能当作高分辨率正常解锁的典型值；以上均没有同步 SurfaceFlinger 实际 present，因此不计算视觉延迟平均值，不证明高分辨率导致等待。USER_PRESENT 与实际检测 KEYGUARD_UNLOCKED 也不是同一测量点，不混用。
- **READY 的实际含义**：`ia.1.smali` 调用 `ja.hb().q(0)` 后，立即在接收回调中调用 `LauncherBelowKeyguardCompat.onPrepareReady()`。`smengine/n.1.q(F)` 委托 `p.1.a(n,F)`；零延迟分支只是把 Event 放入 `tE` 并请求引擎更新，之后才由 `p.update → ek → Event.run` 消费。`hb` 中的 `Eb.ai()` 清理旧 emergency event，不是 GPU 完成屏障。故 `prepareBegin==prepareReady` 只描述该兼容接线返回，不能证明原版 Scene 已完成 GL 准备、纹理上传或上屏。此处发现的是测量盲区，不是已经证明的卡顿 Owner。
- **原版/当前边界**：`ea.1.smali` 与 clean_launcher 文件一致；`animations/c/k.smali` 对照原版仅 `isPlaying()` 增加已结束检查，初始化/播放方法没有差异。maintained 的 `UnlockAnimationXML.init/start` 仍是独立的初始化与播放入口，不作为替换当前动画的依据。当前 `J` 的两处 Surface 初始化已经设置 `setPreserveEGLContextOnPause(true)`，不能把问题未经验证地归因于“没有保留 EGLContext”。
- **分辨率假设**：当前 `IconVisualMetrics.resolve()` 按真实 Surface 宽度与 logical width 比值确定 physical raster；当前样本 physicalScale=1，不表示各分辨率纹理像素数相同，因为 logical LayoutProperty 本身也已经适配。相同宽高比下，1260 宽相对 1080 宽约为 1.36 倍像素量，1440 宽约为 1.78 倍；这只是像素量计算，不是耗时预测，更不能排除 ROM/芯片/刷新率差异。
- **纠正旧结论**：9 月 1 日的 `onDrawFrame=1.793ms` 与 `eglSwapBuffers=0.256ms` 仅覆盖 CPU 同步区间。GPU/显示同步依赖 fence，不能以 CPU 返回替代 FIRST_PRESENT；撤销“已经排除 Launcher/GL 并确定 SystemUI Owner”的强结论。参考 [AOSP 图形同步说明](https://source.android.com/docs/core/graphics/sync)。当时 EARLY_PLAY 实验没有 FIRST_PRESENT 对齐，不能单凭 START 日志定性；后续同机 v1.5.5/CURRENT Surface A/B 已确认预滚动差异，并由本日更新的严格 Session 实现收口。
- **下一判决**：优先同一高分辨率设备使用系统原生分辨率设置做受控对照（需确认支持，当前未更改），核对实际 Surface/Buffer 尺寸，并固定同一 APK、主题、宫格、图标大小、刷新率、解锁方式；不把 wm size 的逻辑覆盖冒充面板/Buffer 真正降分辨率。对齐原版准备实际执行、CPU 帧、GPU ready fence、Launcher Layer visible、buffer frame number/present 与 Focus。只在证据确认纹理重建/上传或原版 Prepare Scene 被覆盖时修复对应 Owner；若 Buffer 已 ready 但系统延后显示，则不通过提前 q(1)、固定 delay 或改 Timeline 掩盖。若两版/分辨率的呈现与播放时间均相近，继续核对第一张可见 Buffer 内容。
- **状态更新**：本节是实施前证据边界；最新结论以同日上方“有效 direct-handoff 的 USER_PRESENT 预滚动恢复”为准。未将分辨率写成 ROOT_CAUSE。

#### Open Folder 共享纹理路径恢复候选与真机结果

- **原因与范围**：按用户要求停止历史 A/B 构建，仅撤销 Open Folder 普通应用独立 Mode8 final representation。方法级对照 37301 恢复 cache/调用入口语义，保留 CURRENT Folder dH 尺寸及两处 Desktop userScale 隔离。
- **修改**：`g.1.smali` 的 `cb/fb/md` 与 `IconRasterDiagnostics` 的 Cell key/普通 Folder 判断；共享 `e/s` 内部继续保留当前 Desktop static pipeline。并非完整 37301 源码回退，更不等于已证明恢复其性能。
- **冻结**：未改 Unlock、Timeline、duration、Eb.update/Ra.T、Folder 资源/文字、天气/日历 Owner、g.jl；已有 Issue #11、Unlock 与 Preview 差分均保留。
- **验证**：diff check、构建、签名、设备 ART verify、安装与冒烟通过。同一个九普通应用 Folder 的 50/100/150% 各一次冷启动首次/第二次打开已采外部 atrace；首次最大 onDrawFrame 为 83.162/87.735/77.642ms，第二次为 78.158/80.932/80.836ms。
- **结论**：共享路径已实施，但长帧仍在，不能写“文件夹卡顿已修好”。三档截图未见 Folder 跟随桌面缩放，精确像素一致性与用户顺滑手感验收仍未完成。本轮已复核三个临时测试应用回到原位及 Desktop 100%。
- **文档与仓库**：只记录已验证事实；未更新 MEMORY，未提交、未推送。

### 2026-09-02

#### Issue #11 Desktop 局部偏移 Owner 与真实 Layout Profile

- **证据**：反馈日志中 V2183A 的最终 Launcher Window/SurfaceView 为 1080x2400；适配器使用 1.25 纵向倍率，图标栅格却保持 230/295、physicalScale=1。原版四个高度 profile 的 MODE_12/20/64 局部偏移不随高度改变。
- **修复**：三个局部偏移明确按所选资源宽度缩放；P 保留实际 Resources/目录/mode，适配器复用原版 global.xml 的真实宽高，仅用于有原版差异证据的 Placement 字段。冻结其他视觉字段；不增加机型、分辨率特判，不改 Folder/Unlock。
- **审计纠正**：旧 factorFor 虽写了 name_off_set_y 的 scaleY，但整数字段筛选漏掉 off_set 名称，实际 MODE_64 为 -100/-9/-9，并非 -125/-9/-9。修复显式纳入该字段；1080 宽目标为 -100/-7/-7。
- **诊断**：gridToken 复用 Constants.cellCount；Surface Owner 用实际解析成功标志，数值计算不变。三类新验收日志由 APK 内专用 marker 控制，正常源码不保留 marker。
- **验证**：1944 组 JVM 实际适配器几何用例、374544 次非目标字段检查、72 组 Folder 全字段比较通过；925 个冻结 APK 资源/原生库条目与备份一致。首次诊断包有新增 Smali p1 异常分支类型冲突，已恢复备份后修正；增加 ART 类初始化验证，修正包构建与 v1/v2/v3 签名通过。完整 Android 视觉矩阵与 V2183A 远程对照尚未完成，不标记 ROOT_CAUSE CONFIRMED。
- **产物**：`build/issue11/launcher-issue11-acceptance.apk`，v1.5.6/31，SHA256 `B10033F07EA7F44513F8D7D156CC6FE609F2ACED4C52A8E719A37FEF00DA2817`。
- **真机边界**：最终验收包已覆盖安装 V2458A，桌面与文件夹冒烟可运行；中间诊断包确认本地实际 profile 为 2340x1080。前后截图 mode/图标位置不同，不计同条件视觉通过；最终日志读取为空，不计日志通过。已另构建不含 acceptance marker 的普通包，详见专项报告。
- **状态**：`FIX_IMPLEMENTED_PENDING_REMOTE_ACCEPTANCE`；字段表、资源链、验证边界及反馈者操作说明见 [专项记录](../ISSUE_11_LAYOUT_ACCEPTANCE.md)。MEMORY.md 未更新；未提交、未推送、未向 Issue 发布未经验证的结论。

### 2026-09-01

#### 解锁动画首个 CPU GL 帧外部取证（未取得实际上屏时间，未改代码）

- **用户可感知问题**：V2458A 解锁时肉眼明确看到桌面先静止一下，随后原版解锁动画才开始运动。本轮只追踪第一张真实 GL 动画帧，不重新调查 Unlock Trigger/Gate 或 `q(1)`。
- **同一 Session 边界**：肉眼确认卡顿的 `sessionId=5` 中，`WINDOW_FOCUS_TRUE=893008662`、`COMMIT_PLAY=893008663`、`ANIMATION_START=893008665`，即 `FOCUS -> COMMIT=1ms`、`COMMIT -> START=2ms`。
- **外部 trace 对齐**：未新增生产日志，使用 atrace `view/gfx/sched/freq/idle/am/wm/input` 抓取同一轮。trace clock sync 将 logcat `ANIMATION_START` 对齐到 `1612539.414704s`；回调后第一个新启动的 `GLThread onDrawFrame` 为 `1612539.417238s -> 1612539.419031s`，所以 `START_TO_FIRST_GL_FRAME=2.534ms`、`FIRST_GL_FRAME_DURATION=1.793ms`。
- **CPU 帧补充证据**：`ANIMATION_START` 实际已发生在前一个正在执行的 `onDrawFrame` 内；该帧为 `1612539.414053s -> 1612539.416964s`（`2.911ms`），紧接的 `eglSwapBuffers` 为 `1612539.416970s -> 1612539.417226s`（`0.256ms`）。该片段未见 start 后 CPU GL 长阻塞，但不是可见帧或 GPU 完成证据。
- **结论纠正（2026-09-03）**：上述数值保留；原先据此将 FIRST BAD 收敛至 Keyguard/SurfaceFlinger 的推断证据不足。未测 Launcher Buffer 实际 FIRST_PRESENT/GPU fence，不能排除首帧内容问题或确认系统交接 Owner，也不能声称已经取得 first visible frame。仍不允许通过修改 Gate/Timeline 猜测修复。
- **冻结与验证范围**：未修改 `LauncherBelowKeyguardCompat`、`ia.1`、`q(0)/q(1)`、`unlock9/12/16/20`、Timeline、动画时长、`Eb.update()` 或 `Ra.T()`；未构建、未安装、未提交、未推送。当前只有 V2458A / OriginOS 16 的一次肉眼卡顿样本，未细分 SurfaceFlinger 内部 latch/present owner，也不得扩写为多 ROM 结论。
- 未更新 `MEMORY.md`。

### 2026-08-31

#### Folder 天气新 Owner 首次数据回放与 Open Folder 图标小幅增大

- **根因**：Folder/Open Folder 创建天气 `H` 后，`Eb.a(H)` 会清理旧实例并把新实例设为唯一 Owner，但原路径只在 Launcher model complete 或拖放时调用 `H.zq()`。当持久天气 Bundle 仍然新鲜、不产生新广播时，新 Owner 的温度保持默认值，第一次静态合成只得到蓝色背景；移出再移入恰好触发拖放刷新，所以立即恢复。
- **最小修复**：在 `Eb.a(H)` 写入新 Owner 后调用现有静态入口 `H.zq()`。数据继续由 `WeatherBridge.getWeatherBundle()` 读取并经原天气协议更新 `H`，`H.uq()` 继续通知所属 Cell 的 `gj()` 重绘；没有更改动态图标分类、数据格式、WeatherView 或缓存身份。
- **视觉范围**：仅调整 Open Folder portrait MODE_9 的 `_folder` artwork/texture 基准，1080 profile 为 `148/190`，sw411dp profile 为 `197/253`，相对上一版约增大 4%；Desktop、Folder Preview、文字间距、书架、阴影和 landscape 不变。
- **验证**：完整构建、badging、v1/v2/v3 签名与 diff 检查通过；V2458A 三轮强停冷启动的预览及首次打开都显示 `25°`，Calendar/Clock 正常；连续开关 Folder 10 次 PID 不变且无 crash。冷态首次打开的关键 GL 帧仍为 `217.370ms`，既有首开同步 scene CPU 卡顿未在本轮修改。
- 未更新 `MEMORY.md`；未提交、未推送。

### 2026-08-30

#### 桌面与设置主页 Activity 转场修复

- **根因**：桌面“桌面设置”入口通过通用 `startActivityForUser()` 打开 `ThemeChooserActivity`，设置主 Activity 退出时也没有这条桌面往返边界的专用转场，因此缺少原预期的上入下出动效。
- **最小修复**：仅对 `com.smartisanos.launcher/.theme.ThemeChooserActivity` 精确调用 `overridePendingTransition(settings_enter, 0)`，`finish()` 后调用 `overridePendingTransition(0, settings_exit)`；新增 260ms 进入与 220ms 退出动画，通过受校验的资源表补丁写入稳定 anim ID。
- **冻结范围**：设置内部一级/二级仍使用原有横向 View 动画；未修改全局 window animation、SMEngine、Unlock、Folder、桌面布局、图标或天气链。
- **验证**：`build.bat`、资源反读、badging 和 v1/v2/v3 签名通过；V2458A 桌面→设置与设置→桌面各 20/20 次通过，逐帧无黑帧，设置内部导航保持原动画。未提交、未推送。

### 2026-08-29

#### 魅族 Flyme 官方天气包精确识别修复

- **根因**：`WeatherBridge.isWeatherPackage()` 的官方天气精确包名列表缺少 `com.meizu.flyme.weather`；`LauncherSettingBridge.isDynamicIconPackage()` 在该路径上又没有 component/title 兜底，导致 Flyme 天气被当成普通静态 Application。
- **最小修复**：仅新增精确包名 `com.meizu.flyme.weather`，不泛化为 `com.meizu.*`，不修改 Calendar、WeatherView、天气动画、geometry、192 坐标、阴影、Timeline、Folder、图标大小或天气数据源。
- **逻辑验证**：`tools/verify_weather_package_detection.py` 确认魅族天气与既有官方天气包保持 `true`，而 `com.meizu.flyme.launcher`、`com.meizu.media.camera`、`com.meizu.filemanager` 保持 `false`。
- **构建与风险**：`build.bat`、v1/v2/v3 签名及最终 dex 字符串检查通过；当时没有 Meizu/Flyme 真机，故只记为 `RUNTIME_MEIZU_VALIDATION_PENDING`，不得写 Meizu PASS。未提交、未推送。

### 2026-08-25

#### Folder Preview Cell Mode 缓存 Owner 修复

- **根因**：`FolderIcons(la).a(F, ItemInfo)` 用 `ItemInfo.Ne()` 绑定纹理名后仍调用不带 `pageMode` 的 `e/s` 旧重载，Static Composer 因而回退全局 `SINGLE_PAGE_MODE=1`，使 Folder Preview 内 Calendar/Clock 误用 `269/344, grid=1`，而不是 Folder Cell 真实的 `224/287, grid=12`。
- **最小修复**：使用 `Qj.fH` 重建 preview cache key，并让 Weather ActiveIcon、Calendar ActiveIcon 和普通静态应用三条分支统一调用显式 `pageMode` Composer；未修改 Preview viewport、Mode8、IconVisualMetrics、Desktop geometry 或分辨率倍率。
- **验证**：完整构建和覆盖安装通过，Android 16 无 `VerifyError/FATAL`；V2458A 冷启动 Calendar/Clock 均为 `224/287, grid=12`，12→20→12、Folder 开关与两个不同 Folder 截图均正常，最后恢复 12 宫格。未提交、未推送。

#### Unlock 单 Owner 生命周期 ARM 与立即 Commit Golden

- **根因**：旧实现只允许 `SCREEN_OFF -> armFromScreenOff()` 建 Session，厂商 ROM 上 `onPause` 已看到锁屏证据却无法 ARM；旧 fallback 又用 250/120ms 延迟伪造 prepare/dismiss，导致延迟、重复和普通返回误触发风险。
- **最终链路**：`SCREEN_OFF`、`onPause`、focus-lost 与 `onStop` 统一进入 `armAndPrepareIfNeeded(source)`，首次真实锁屏证据立即 ARM 并同步派发原版 `action_keyguard_on -> q(0)`；`USER_PRESENT/dismiss` 只置当前 Session pending，无广播时由 `resume while locked -> first focus + interactive + unlocked` 同步进入唯一 `tryCommitUnlockAnimation()`，再派发原版 `q(1)`。
- **删除的旧路径**：删除 1500ms dismiss delayed Runnable、300ms pause cancellation、2500ms play watchdog、Maintained unlock wrapper/note/skip helper 与 receiver 重复 prepare；1500ms 只保留为同步 stale guard。不依赖系统 default HOME resolver，不修改 `q(0)/q(1)`、unlock9/12/16/20、Timeline、`Eb.update/Ra.T` 或刷新率控制。
- **验证**：V2458A / OriginOS 16 在 Smartisan 非默认 HOME 时连续 20 轮 `ARM/PREPARE/READY/COMMIT/PLAY/START/FINISH=20/20/20/20/20/20/20`，重复 ARM 40 次均忽略，首次真实 focus 满足到 Start 约 2ms；Settings、Recents 和普通 APP 返回均不建立 Session。ColorOS/Flyme 及锁屏相机等边界仍待对应真机验证。未提交、未推送。

### 2026-08-24

#### Open Folder 冷重载尺寸隔离与 Desktop Label 宽度适配

- **冷重载根因**：`Constants.applyIconSizeToProperty()` 已正确排除 `PAGE_1_3X3_MODE_FOLDER`，但进程恢复时 `MaintainedLauncherSettingsHost.maybeApplyLauncherIconSize()` 仍会调用 `applyRuntimeIconSizePercent()` 遍历全部 `layoutPropertyMap`，随后由 `scaleLayoutProperty()` 原地改写共享 `LayoutProperty`。该入口没有 Folder owner 判断，因此刚移动入 Folder 时使用的 Folder Base 正常，切换宫格或图标大小触发冷重载后，MODE_9/multiPageMode=8 却重新带入 Desktop userScale。
- **分辨率差异根因**：当前低分辨率 MODE_9 资源曾把 `icon_size_origin_resize` 改为 192，同时 `icon_size_with_shadow_folder` 只有 184，形成 resized artwork 大于 Folder raster envelope 的非法关系；`P.smali` 加载 `_folder` property 时会把资源 `icon_size_with_shadow_folder` 映射回运行时字段 `icon_size_with_shadow`，所以 184 确实是 Open Folder child 的最终 node/texture 边长，不是未消费的旁路资源。1440 `sw411dp` profile 仍保持可容纳的 `222/286`，所以问题主要在部分低分辨率 profile 暴露。原版 `clean_launcher_raw` 的基准为 1080 `166/216`、1440 `222/286`，并由 Folder 自己的 width-based profile/adaptation 扩展，不依赖 Desktop 50/100/150。
- **最小修复**：`scaleLayoutProperty()` 在改写共享属性前使用现有 `FolderVisualGeometry.isFolderLayoutProperty()` 识别 Open Folder 并直接跳过，从源头阻断 Desktop userScale 污染；没有采用除以 1.5、机型判断或事后补偿。MODE_9 资源恢复原版 1080 `166/216`、1440 `222/286`、landscape `56dp`。1080 到 1260 的同一宽度规则静态结果约为 artwork `193.67`、Folder texture `252`；1440 使用原版 profile `222/286`。普通 Desktop 和关闭状态 Folder 仍走原有 Desktop scaler，Preview 内部字段未再乘一次 userScale。
- **Desktop 文字**：`Mc.hq()` 的创建路径和 `Mc.o()` 的主题刷新路径仍读取各自 Desktop `LayoutProperty`，仅在 Paint `setTextSize()` 前调用 `DesktopLabelMetrics.resolveDesktopTextSize()`。字号基准固定为原版 1080 的 12宫格 36、20宫格 30，再乘 `surfaceWidth/1080`；因此 1080/1260/1440 分别为 12宫格 `36/42/48`、20宫格 `30/35/40`。字号不随 Desktop 50/100/150 改变，现有 Desktop label gap 和 icon geometry 均未修改。
- **冻结范围与验证**：未修改 `IconVisualMetrics`、Static Composer、physical raster、normalization、source resolver、阴影/cache、Weather/Calendar、Folder Preview、Folder书架、row/column、动画或 `FolderCellVisualMetrics`。`build.bat` 成功；最终 APK badging 为 `versionCode=31 / versionName=v1.5.6`，v1/v2/v3 签名通过，`git diff --check` 通过。X21A（1080x2280/480dpi）在线且原 Launcher 已安装，但 `adb install -r`、`adb install -r -d` 和 `/data/local/tmp + pm install -r -d` 均被 vivo 返回 `Failure [-200]`；为避免丢失桌面数据库未卸载 Launcher。故真实 12/20宫格、50/100/150、移动前后与冷重载截图矩阵尚未标记 PASS。未提交、未推送。

### 2026-08-23

#### Folder GLThread 资源释放与 draw 状态门控修复

- **崩溃路径**：`ka` 的 Folder Cell 仍在 Scene draw 时调用 `FolderIcons.oa(Z)`；兼容层 `gj()` 的 Weather/Calendar ActiveIcon 更新先通过 `FolderInfo.O(package)` 找 owner。当 stale callback 找不到 owner 时，当前实现错误调用整个 `FolderIcons.clear()`，把 `hz/iz/kz/Qj` 等渲染资源置 null，却没有先把 draw 标记 `jz` 置 false。下一帧 `oa()` 看到 `jz=true` 后直接对 null `iz` 执行 `array-length`，对应日志 `FATAL EXCEPTION: GLThread / Attempt to get length of null array / la.oa`。
- **最小修复**：`clear()` 第一条状态操作改为 `jz=false`，再按原顺序释放 `hz/iz/kz` 和 ActiveIcon；`oa()` 增加最终防线，`jz=false` 直接返回，`iz/hz/kz` 任一为 null 时设置 `jz=false` 并返回，正常 draw/RenderTarget/动画代码保持原样。`gj()` 的 Weather/Calendar owner missing 分支分别只调用对应 ActiveIcon 的原有 `g(true,false)` 停止接口并清空对应字段，然后返回，不再调用整个 `FolderIcons.clear()`；真正 Folder 销毁仍由 `ka.clear()` 等原生命周期负责。
- **冻结范围**：仅修改 `launcher/smali/com/smartisanos/launcher/view/a/la.smali` 的 `clear()/gj()/oa()` 生命周期状态门控；未修改 Folder Preview、2x2/3x3 viewport、图标尺寸、行列、书架、root scale、材质、动画或任何资源。
- **验证**：`build.bat` 和 Smali 编译通过；`pm install -r` 覆盖安装成功，设备 `classes.dex` 与本地产物 SHA-256 一致。V2458A 分4批完成20次 `force-stop -> Launcher` 冷启动，完成30次 Folder 连续打开/关闭，并对已安装 aShell 原 APK执行同签名覆盖更新后返回 Launcher；三组均为 `FATAL=0 / GLThread FATAL=0 / la.oa NPE=0`。设备现有 Folder 不含 Weather/Calendar，未通过修改用户桌面布局制造动态 ActiveIcon Folder 样本；真实应用卸载也未执行，因此这两项仍是明确未完成的真机矩阵，不能扩写为全场景 PASS。未提交、未推送。

#### 解锁动画非默认 HOME 前台资格与同步 Commit 修复

- **回归根因**：`launcherActuallyVisibleLocked()`、`onLauncherPaused()` 的锁屏可见快照和 `tryCommitUnlockAnimation()` 正式播放前都把 `isDefaultHome()` 当成必要条件。因此 Smartisan Launcher 即使真实 `resumed + windowFocus`，只要系统默认 HOME 是其他 Launcher 就无法建立或消费 session。播放前还重复调用 `isLauncherRuntimeReady()`；该条件只是 `J.getInstance()+context`，而原版 prepare receiver 在 `q(0)` 前、正式 play receiver 在 `q(1)` 前均已有 `J.Ua()` 检查，不应在已 `prepareReady` 后由兼容层第三次阻塞/取消。
- **实现**：彻底移除 `isDefaultHome()` 资格方法及三处依赖；锁屏前资格收敛为 Smartisan Launcher 自身真实 resumed/focus 快照，`SCREEN_OFF` 后仍必须确认 Keyguard locked。正式 commit 固定要求同一 session 的 `prepareReady + dismissPending + launcherResumed + windowFocus + keyguardUnlocked`，并继续执行 `shouldSkipUnlockAnimation()`；已 prepare session 不再被兼容层 runtimeReady 重复等待，原版 receiver 的 `J.Ua()` 检查保持不变。没有新增 postDelayed、提前量或 50/100/200ms 延迟，既有 1500ms 只继续用于取消未完成的非直达交接。
- **诊断时间线**：同一 session 记录 `SCREEN_OFF / PREPARE_BEGIN / PREPARE_READY / USER_PRESENT / LAUNCHER_RESUME / WINDOW_FOCUS_TRUE / KEYGUARD_UNLOCKED / RUNTIME_READY / COMMIT_PLAY / ANIMATION_START` uptime，并输出 `USER_PRESENT->COMMIT`、`COMMIT->START` 和最后满足的 Gate。非默认 HOME 单次为 `20ms/16ms`，默认 HOME 单次为 `15ms/20ms`，两者最后 Gate 均为 `WINDOW_FOCUS_TRUE`；说明 prepare/runtime 已在锁屏阶段完成，首次真实 focus 后同步 commit，没有额外延时等待。
- **防误播验证**：默认 HOME 锁解一次与非默认但 Smartisan 前台锁解一次均只播放一次。设置、微信主实例、电话和相机分别前台锁屏解锁，随后手动打开 Smartisan，全部 `ARMED=0 / COMMIT=0 / START=0`，只记录 `NOT_VISIBLE_HOME / SKIP_NO_SESSION`。非默认 HOME 连续20次为 `ARMED/COMMIT/ORIGINAL_PLAY/START/FINISH=20/20/20/20/20`，`CANCEL=0`、`SKIP_NOT_PREPARED=0`；20轮 `USER_PRESENT->COMMIT` 为 `6..30ms`（平均 `13.7ms`），`COMMIT->START` 为 `2..21ms`（平均 `5.5ms`）。
- **冻结与验证**：只修改 `LauncherBelowKeyguardCompat.java` 的 Trigger/Session Gate 与诊断；原版 `q(0)/q(1)`、SMEngine 动画时长、`Eb.update/Ra.T`、图标动画参数及刷新率适配均未改。`build.bat`、`git diff --check`、v1/v2/v3 签名通过；因 vivo 首次增量安装未替换设备 APK，最终改用 `/data/local/tmp + pm install -r` 并在系统确认页继续安装，设备端 `classes2.dex` SHA-256 与本地产物一致。默认 HOME 已恢复为 `com.bbk.launcher2/.Launcher`。未提交、未推送。

#### Open Folder Label Gap 与 Anchor 收口

- **根因**：Open Folder label 的真实最终位置已确认由 `FolderCellVisualMetrics` 返回值直接进入 `g.1.smali` 的 `Mc.setTranslate()`。此前虽然把 Folder Gap 改为 Desktop 数值，但仍叠加了从 `+40` 哨兵反推的 `34.3@1080` Anchor correction，导致 1260 设备修正值为 `40.0167`，文字比目标位置更靠近图标。
- **最终实现**：Folder 继续使用自己的 artwork/text geometry；Gap 直接调用 `DesktopLabelMetrics.finalVisualGap()`，不再维护第二份 Folder Gap 基准。唯一 Folder Anchor correction 调整为 `BASE_FOLDER_LABEL_CORRECTION1080=28.43`，统一按 `surfaceWidth / 1080` 缩放：1080=`28.43`、1260=`33.1683`、1440=`37.9067`、2160=`56.86`。1260/20 宫格下最终 `Mc.setTranslate Y` 约为 `-71.9983`，回到原版 `name_off_set_y_folder=-72` anchor。
- **冻结范围**：未修改 Desktop、`DesktopLabelMetrics` 输出、普通/Folder icon geometry、166/216 图标基准、Folder Preview、书架、row/column、root scale、Constants 和 Desktop 50/100/150 隔离；已撤掉 bounds 反射、`Qj/Pj` runtime 取底边、临时日志和二阶段生命周期逻辑。
- **验证**：`build.bat` 成功；APK v1/v2/v3 签名验证通过；`adb install -r build/launcher-signed.apk` 成功；V2458A/1260×2800 真机截图确认翻译机、对讲机、闹钟时钟文字整体下移，图标和书架未变化；未发现 `FATAL EXCEPTION`、`VerifyError` 或 `NoClassDefFoundError`。1080/1440/2160 通过同一 width-based 公式静态审计，尚未取得对应设备截图。未提交、未推送。

### 2026-08-21

#### 桌面图标渲染管线尝试及统一性复审

- **当时定位**：源码追踪发现冷启动（Cold Bind）和异步热更新（Hot Update）存在不同的数据源入口：
  - Cold Bind 渲染管线 (`g.1.smali`): 在渲染时通过 `shouldUseManagedIcon` 前置拦截，直接在 Java 层取了 Drawable 画满 UI 单元格，完全绕过了数据库保存的 `iconRawData`。由于之前去除了 `InsetDrawable` 尺寸欺骗，导致直接将 256x256 生素材截断渲染而变大。
  - Hot Update 数据更新管线 (`Aa.smali`): 在线下载完成更新数据库时，原本存在的“官方 Static Application Composer”（内边距补齐与缩放逻辑）被早期的 `cc29dbca` 提交用硬编码的 `goto :cond_6` 完全跳过，导致生素材未被裁剪缩放直接转存 DB，同样变得巨大。
- **已暂存修改**：放弃在 Java 侧模拟 Padding 的路径，恢复原版 Smali Composer：
  - 在 `Aa.smali` 中，移除强制跳出指令，重写了跳转逻辑（`if-nez p2`, `if-nez v1`）：确保所有的第三方应用程序和下载的 Canonical 图标，都能无条件进入 Composer 处理区；保留原有对于系统应用根据 `ColorInfo.resize` 来判定是否缩放的克制设计，避免系统应用被双重缩小。
  - 在 `g.1.smali` 中，移除了导致数据分叉的 `shouldUseManagedIcon` 判断和对 `PackageManager.getApplicationIcon` 的依赖。现在桌面对于所有的 `itemType == 0`，都优先读取数据库的 `iconRawData`。如果 `iconRawData` 存在，则直接渲染，从而保证 Cold Bind 也能读到已被 Composer 正确处理的带内边距位图。
- **复审结论**：本地构建曾通过，但该修改没有消除所有尺寸 owner。`e/s + IconRasterDiagnostics` 仍负责最终 physical texture 合成；如果 managed source 重解析成功，会覆盖数据库位图，如果失败则可能继续使用已经由 `Aa` 加过边距的 `iconRawData`。后一条路径存在重复留白/缩小风险，不能再写成 Cold/Hot/Restore 已统一。状态为 `AUDIT_REOPENED / FIX_REQUIRED`，不得签署 Final Pass。

### 2026-08-20

#### Desktop Backup & Restore：文件夹拓扑、Schema兼容与非便携权限隔离

- **范围**：修复 FolderInfo 被当作安装包过滤、父文件夹未先写入导致子项散落、不同原版数据库缺少统计列时的越界写入，以及通知监听/定位等非便携权限跨设备恢复。
- **实现**：恢复采用 `RESTORE PHASE 0..9` 有序事务；页表后先分类并写入 Folder，再写普通项和子项，最后追加保留项、恢复快捷方式图标并执行前后 FolderTopology 校验。状态清零只处理快照实际存在的字段；`NON_PORTABLE_PERMISSION_KEYS` 在导出与导入双向剥离。
- **验证边界**：V2458A 样本完成 PHASE 0..9、54项写入和冷重载，状态仅为 `FOLDER_TOPOLOGY_AND_SCHEMA_RESTORE_V2458A_PASS`。QuickLaunch备份恢复仍为 `ROOT_CAUSE_REOPENED`；普通Application最终Raster仍受 Icon Rendering Contract门禁；Android 8–16与多ROM矩阵未完成。不得写成全部备份恢复、全部ROM或全部旧机型PASS。

### 2026-08-15

#### QuickLaunch 小程序最终渲染源隔离修复（V2458A 真机视觉 PASS）

- **最终根因**：微信/支付宝的小程序创建、provider artwork、`final_icon` 和数据库写入并不是本轮头像/圆环丢失的最终 owner。真正的第一处分叉发生在桌面最终渲染：`itemType=1` 的 `QuickLaunchItem` 曾被 `IconRasterDiagnostics` 当成普通 Application，再按 `packageName=com.tencent.mm` 进入 DEFAULT/IMPROVED 等普通应用 source resolver/cache，导致已经正确保存的小程序逐快捷方式位图被微信宿主应用图标覆盖；`ItemInfo.Oe()` 同时还会对 QuickLaunch 套用普通应用分身 badge。
- **正确生产链**：微信/支付宝继续使用 v1.5.5 最终兼容语义：`LauncherApps.getShortcutIconDrawable()` provider-first，只有不可用时才回退 wrapper source；provider artwork 视为 `source_already_decorated`，保留其小程序头像与圆环/外框，写入 `smartisan.shortcut.final_icon=true`，由 `QuickLaunchItem.z()` 直接序列化，**不调用 `e.s.a()` 二次重画**。原版 `A.smali / EVENT_INSTALL_OR_UPDATE_SHORTCUT` 数据库业务流不承担 provider 图标特殊逻辑。
- **渲染隔离**：`itemType=1` 明确退出 `useDesktopStaticPipeline()`、`useManagedDesktopPipeline()`、`shouldUseHighResolutionDesktopRaster()`、`prepareStaticSource()`、`loadCurrentDesktopDrawable()` 和普通 Application composer；`ItemInfo.Oe()` 对 QuickLaunch 直接返回自身 `iconData`，不追加普通应用分身 badge。QuickLaunch texture/source 使用独立 `quick-launch-final-source`，身份包含 `packageName + shortcutId + userId + userSerial + iconData/iconRawData hash`，不同小程序不得因同属 `com.tencent.mm` 共用宿主应用 texture。
- **真机验证**：V2458A / Android 16 在修复包上重新添加微信小程序后，用户截图确认“云销盒”已经显示自己的小程序头像与圆环/外框；同屏微信主应用仍保持微信主图标，证明 QuickLaunch 与宿主 Application 最终显示源已经隔离。该项记录为 `QUICKLAUNCH_RENDER_SOURCE_ISOLATION_PASS / V2458A_VISUAL_PASS`。
- **未覆盖边界**：本次只冻结“新建微信小程序的最终图像来源与渲染隔离”。冷重载多轮、应用分身开关、主/分身同 ID、支付宝、Backup/Restore、旧错误 QuickLaunchItem 一次性迁移和点击启动完整矩阵仍需继续测试，不能根据本截图扩写为持久性全链 PASS。
- **防回归硬规则**：以后排查 QuickLaunch 图标，必须先按 `provider/createItem → table_icons → ItemInfo.Oe() → render source/texture` 分层定位 first bad owner；不得再把 `packageName` 相同当作图标身份，不得让 `itemType=1` 进入普通 Application source pipeline，不得为了“补圆环”给微信/支付宝 provider bitmap 调用 `e.s.a()`，不得在 `A.smali` 新增 provider/final_icon 特判。普通 Application 的 DEFAULT 圆形、IMPROVED、图标包和分身 badge 均不得处理 QuickLaunch。

#### 【已废弃】QuickLaunch provider 圆环由 `e.s.a()` 生成、通过修改 `A.smali` 消除二次 compose 的判断

#### 【已废弃】仅恢复 provider-first / `final_icon` 即可解决桌面最终显示微信宿主图标的判断

### 2026-08-12

#### 【已废弃，历史实现已被 Icon Rendering Contract 取代】Icon & Folder Unified Geometry

- 根因：旧静态合成会按 alpha 外包络而非完整源画布缩放，且曾固定读取 12 宫格 `LayoutProperty`，使 20 宫格和打开文件夹不能取得自己的 icon box；`LayoutPropertyAdapter` 的上限曾禁止宽于 1080 profile 的 surface 向上适配。文件夹的原始三列 X 没有按书架内容可用矩形重新居中。此前把桌面“桌面设置”虚拟化为普通应用并参与替换链，也与用户确认的原版行为冲突；尝试在 scene root 追加文件夹缩放还造成开合闪动/卡顿风险。
- 修复：普通静态源统一按完整 source canvas 等比 fit 到场景固定 artwork/texture box，不再作 alpha/面积/轮廓 optical compensation。普通桌面只适配 `LayoutProperty` 中的 icon box，不改变原版 scene/dock 几何。打开文件夹则由 `_folder` 这一份 `LayoutProperty` 统一缩放书架、内容、文字、标题和分页相对几何，列中心仅从 `folder_bookcase_width` 与已有左右 margin 推导。`FolderSceneMetrics` 回到原版，未保留额外 root scale/translate。桌面“桌面设置”恢复独立 `Ec.wz()` SettingButton，物理纹理只来自 `editBtn_bg.png`、`editBtn_gear.png`、`editBtn_inShadow.png`，不再进入 DEFAULT/IMPROVED/PACK/CUSTOM 或图标替换页。
- 路径：普通桌面、打开文件夹和关闭文件夹预览中的静态应用继续经 `IconRasterDiagnostics.composeStaticApplicationIconTexture()`；动态 Weather/Calendar 保留原版 ActiveIcon 内部动画，只共享外部 geometry。编辑模式 SettingButton 与桌面“桌面设置”保持原版独立控制按钮路径，不是应用图标。
- 修改文件：`LayoutPropertyAdapter.java`、`FolderCellPositionAdapter.java`、`IconRasterDiagnostics.java`、`ActiveIconRasterSpec.java`、`Ec.smali`、`g.1.smali`、`IconManager.java`、`MaintainedLauncherSettingsHost.java`。
- 验证：最终 `build.bat` 成功；`git diff --check` 成功；badging 为 `v1.5.6/versionCode 31`；v1/v2/v3 签名均通过。APK 已保留数据覆盖安装到 vivo V2458A，设备版本为 `v1.5.6/31`，本地/设备 SHA256 均为 `5025E686F036C9C23BB82C21C1E52154A7B87EE8873593D0B3BBE319BD5AE448`。该机实际加载 `_folder` 的 width scale `1260 / 1080 = 1.1666666`，连续 3 轮文件夹开合未见 FATAL/ANR；普通桌面截图未见本轮适配引入的崩溃。
- 未验证：只完成 vivo V2458A 1260x2800/560dpi 的运行与视觉冒烟。当前状态降级为 `HISTORICAL_IMPLEMENTATION / VIVO_1260_RUNTIME_SMOKE_ONLY`；普通图标算法以 2026-08-21 Contract 为准。
- 防回归：不得恢复 alpha bounds/hull/fill ratio optical 倍率；不得把 `currentPageMode()`再次固定为 12 宫格；不得将桌面“桌面设置”重新纳入普通应用替换链；文件夹 X 只能从 `_folder` usable rect 派生；不得向文件夹 root scene 追加 scale/translate 干扰原版开合动画。

### 2026-08-11

#### QuickSearch Q12-B 真机联系人与图标水合验证

- 真机：vivo X21A（`b2a4da1c`）、Android 9/API 28、1080×2280；安装前后仅使用本项目 Launcher，不安装任何测试 APK。
- 联系人：`READ_CONTACTS=granted`、Contacts 开关已启用、Observer 已注册。首次索引完成前快照为 generation=0/count=0，完成后为 generation=1/count=414；脱敏单字符查询提交 `contactCount=4`。日志不包含联系人、号码、lookup key 或查询文字。
- 图标：从 Launcher 上滑进入 Original QuickSearch，Snapshot=32；`QS_ICON_HYDRATE_END` 为 `dbLoaded=32`、`misses=0`，随后 `QS_ICON_REHYDRATE_APPLIED`。未使用 PackageManager fallback 或重建 SearchIndex。
- 修复：`ContactSearchRepository` 以 `indexReady` 而不是 `EMPTY` 的对象身份决定是否应重建；`OriginalQuickSearchActivity` 在 icon source generation 改变时使用现有 Snapshot 水合，完成后只刷新已存在的 Top Apps/Adapter。`SearchIconBackend` 提供受 generation 约束的完成回调。
- 验收边界：真机未实际切换第三方图标包，因此“切换某一个特定图标包后每个图标的像素级外观”仍需用户视觉确认；缓存清空后的同一 Snapshot 水合、联系人结果、上滑进入和稳定性均已通过。

### 2026-08-10

#### QuickSearch Q8-D.6 Emulator Presentation Runtime Closure

- 入口与边界：只使用 `emulator-5554`，所有 ADB 命令均指定 serial；通过 exported `ThemeChooserActivity` preview extra 由应用内启动 non-exported Original Activity，记录 `ENTRY_MODE=EXPLICIT_ACTIVITY_FOR_PRESENTATION_TEST`。未触碰 vivo X21A、未安装测试 App/独立 QuickSearch、未改 Gesture/RootView/SMEngine/Search backend/History semantics。
- 缺陷根因：原版私有 `MenuDialogTitleBar` 的 48dp 测量行为未被 public host 继承，Android 16 把 `wrap_content` title bar 扩成整个窗口，content panel/Clear 被推到屏外。补入 pristine `smartisan_title_bar_height=48dp` 并在 `OriginalMenuDialogCompat` 对 title host 应用该约束；没有重画 Dialog。
- 验收：EMPTY Top Apps=5 和 Phone history；`phone` 命中 Phone、Application header 直接接 SearchBar、Query Surface 全白；`zzzzz` zero result 全白。Dialog 修复后 title/Clear 均 48dp，左右 18dp、top 18dp、bottom 24dp；X/Back 保留历史，Clear 清空，点击 Phone 后 history 正常重建。三轮重开均保持 Original Activity、Top Apps=5、history=Phone、空 query。
- 稳定性与产物：最终 log 中 FATAL/ANR/CME/ResourcesNotFound/Inflate/Class/VerifyError=0；证据为 `build/q8d_emulator_{empty,query,zero,dialog,cleared}.{png,xml}` 与 `build/q8d_emulator_final.log`。`build.bat`、badging v1.5.5/30、v1/v2/v3 签名通过，SHA256 `E19E6386BE087A52B55C18AA4E30BE85E55EF84F49705F69F6D2D14D5EA5CE07`。
- 结论：Q8-D=`EMULATOR_PASS / REAL_DEVICE_VISUAL_CONFIRM_PENDING`。模拟器不能替代 vivo X21A 最终视觉与桌面纵向手势验收；本轮停止，不进入 Q8-E/Q9，不提交、不推送。

### 2026-08-09

#### QuickSearch Q7 Original QuickSearch UI Binding + Formal Presentation Cutover

- 原版审计：pristine SearchBar clear 只 `setText(null)` 并保留 editor；cancel 直接 finish；非空 Back 清 query、空 Back 退出；application suggestion 启动目标后保留 SearchActivity；singleTask 的新请求清旧搜索状态后重新处理。Q7 按这些行为绑定，不照搬 Maintained 页面。
- 实现：正式 facade 的正常目标改为 non-exported/singleTask/portrait `OriginalQuickSearchActivity`，只有同步启动异常才进入 Maintained fallback。Original 只消费当前 `SearchSnapshot`、单一 `SharedSearchMatchModel` 和 `SearchIconBackend`；Top Apps 与 suggestion 共用 Q5 component/user/profile/shortcut 启动 bridge，异步图标校验 entryKey、adapter/bind generation 和 Backend source generation。RootView、FlingUpGesture 的 150px/500ms/方向/单指判断及 SMEngine 均未修改。
- Preview：空态与 5-slot Top Apps 正常；Top App 2/2 启动成功并可返回同一 Original Activity；`dianhua` 和 `dh` 均命中电话，suggestion 点击成功且返回保留 query；clear、0 result、cancel、非空 Back、重开空态全部 PASS。Profile/Shortcut 自然样本为 `UNAVAILABLE`，身份链静态 PASS；DEFERRED/REPLAY 为 `STATIC_VERIFIED / NOT_NATURALLY_TRIGGERED`。
- 正式 Gate：用户完成三次真实手指上滑，日志实际得到 session 6/7/8/9 共 4 个有效样本，Original target/bound=4/4，Maintained 页面=0，fallback=0；request→bound 为 256/247/268/261ms。session 8 的 `dianhua` 结果数 1、3ms，并成功启动 `com.android.dialer/.TwelveKeyDialer`；最后一次重新进入为空态，Back 回 Launcher。
- 硬 Gate：Launcher PID 29023 的正式窗口批量 DB/PM/decode/UsageStats/ICU/网络/legacy loader 均为 0。系统日志中 vivo Calendar/Clock 进程 PID 2598/6383 的 OEM 动态图标 `BitmapFactory` 缺文件噪声不属于 Launcher。ResourcesNotFound/FATAL/ANR/CME/VerifyError 均为 0。
- 构建与边界：`build.bat`、`git diff --check`、badging v1.5.5/30、v1/v2/v3、Manifest/Dex 静态审计 PASS；本地与设备 APK SHA256 均为 `856F0176A13709D6F6A39FF32BE4E0714109BF69B3F03F83A6B7B6EA0BCA1948`。Launcher 覆盖安装 1 次，测试 App/独立 QuickSearch APK=0；`MEMORY.md` 未更新。
- 结论：Q7=`PASS`。正式桌面上滑展示层已由 Maintained Search 切换为 `OriginalQuickSearchActivity`，Maintained Search 仅为同步启动失败 fallback/reference。下一阶段为 Q8 Original Search Semantics；本轮立即停止，不开始 Q8、transition、ContainerView、screenshot/blur，不提交、不推送。

#### QuickSearch Q6.2 Original UI Pinyin Consumer Parity + Scroll Gate

- 根因：Q6.1 只复用了 Q5 scorer，却为每个 Snapshot row 创建私有 Q5 `SearchEntry`，首个查询在 Q6 单线程串行准备 32 份 ICU token，且没有消费 Q5 token READY 或自动 replay；所以这是 consumer state/readiness 缺口，不是 Q5 拼音算法、UI、Theme、Snapshot 或 IconBackend 问题。
- 修复：Q5/Q6 统一到进程级 `SharedSearchMatchModel` 和同一生产 scorer；后台 token 准备完成后通过 weak listener 事件驱动重放仍为当前的 query/generation。Activity destroy 移除 listener、递增 generation、取消 icon request 并关闭 executor；不使用 delay、polling、主线程 ICU/DB/PM/UsageStats/网络。
- 构建：`build.bat`、`git diff --check`、badging `v1.5.5/30`、v1/v2/v3 和最终 Dex 静态调用链均通过；最终本地/设备拉回 APK SHA256 同为 `F7EA2D2434BB4CA2215E84610D7DFE3EABB6472BA611C2BCBF301452D75AC7C4`。
- 真机：vivo X21A 仅覆盖安装 Launcher 一次，测试 App/独立 QuickSearch APK=0。Repository 有效 Snapshot 为 32、duplicates=0；`dianhua` 与 `dh` 均返回“电话”。真实 scorer 自动选出的 `o` 返回 32 条，实际滚动 `firstBefore=0 -> firstAfter=8`、`recycledBindCount=8`；Back、重开绑定 32 条、再次 Back 正常。
- 稳定性：Launcher FATAL、ANR、CME、VerifyError、ResourcesNotFound 均为 0。有效 Preview 开始时 shared tokens 已 READY，因此真机未自然产生 `DEFERRED/REPLAY`；该未就绪分支完成源码/Dex 静态核查，没有通过清 token 或重复冷启造样本。正式上滑入口仍是 Q5 Maintained Search；Q6 未修改 UI/Theme/Insets/Snapshot/IconBackend/RootView/FlingUp/SMEngine。
- 结论：Q6=`PASS`，Original UI Skeleton 冻结。下一阶段为 Q7，但本轮不开始 Q7、不提交、不推送；`MEMORY.md` 未更新。

#### QuickSearch Q6.1 Original UI Final Preview Verification

- 安装：本地 SHA 与指定值一致后只执行一次 Launcher 覆盖安装，返回 Success；设备拉回 APK SHA256 同为 `7AA87ED146A61BE5DE5C931003668A472484DA5286802A22F0322A50FE8B5027`，v1.5.5/30，测试 App 和独立 QuickSearch APK 均为 0。
- Theme/lifecycle：首次和第二次 Preview 均正常，旧 `0x7f010000` Theme namespace 冲突未复现；第二次 inflate/bind 为 66/111ms，Snapshot entryCount=32，四类 Q6 生命周期日志完整；目标异常与 FATAL/ANR/CME/OOM 全部为 0。
- UI：空态、5 个真实 Top Apps、原版 SearchBar/9-patch/icon、首字母 `dh -> 电话`、Back/重开、状态栏/cutout/手势导航均通过。实际 SearchBar=`x0/y84/w1080/h144`，Top Apps=`l54/t300/r1026/b480`，Top icon=108×108px，suggestion row=1080×180px，result icon=90×90px；无设备硬编码。
- 未通过项：Q5 已验证拼音 `dianhua` 在 Original UI 观察窗口内没有显示“电话”；首字母结果只有一行，规定的上下滑动没有形成列表位移或 recycle 样本。不能用 Q5 matcher PASS 替代 Q6 presentation consumer PASS。
- 边界：Q6 未改正式 RootView/FlingUp/SMEngine 入口，仍指向 Q5 Maintained Search；本次单次 ADB 桌面上滑未触发搜索，不作为新的手势样本，既有用户真实手指 Q5 PASS 保持。PM 全量扫描、网络、第二 APK=0。
- 结论：Q6=`FAIL / UNVERIFIED`，不改代码、不重复安装、不进入 Q7、不提交、不推送。

#### QuickSearch Q6 Original QuickSearch UI Skeleton

- 审计：只使用 pristine `original_apks/quicksearch_phone_reference/base.apk`（SHA256 `EDF915A1CA745276F07538ABEDBBF43711B20426697E45A83A4C076ED0562D66`）及其 `decoded/`；完成 SearchActivity、私有 SearchBar、empty view、5-slot Top Apps、application suggestion、9-patch/selector/尺寸/颜色依赖清单。`quicksearch_decode/` 不作为视觉来源。
- 实现：新增 non-exported/portrait `OriginalQuickSearchActivity` 作为并行 Preview；原版可见资源编译为 Launcher asset 中的无代码资源 APK，运行时使用独立 AssetManager/Resources/Theme。数据只读 SearchSnapshot，图标只读 SearchIconBackend，匹配调用 Q5 matcher；不改 RootView/FlingUp/SMEngine，不新增 PM 扫描、Provider、网络或第二个安装包。
- 唯一真机样本：vivo X21A 覆盖安装一次成功，已安装构建 SHA256 `7A9153F3C9AF5187B4FFFF775F272BA7CB9A6C2677643C57FB3B3AD2FFC5A115`。Preview 首开 FATAL 定位为外部资源 `0x7f010000` 继承 Launcher 主 Theme 后被误解析成 `attr/layoutManager`；已给资源 Context 使用独立 framework theme，并让嵌套 SearchBar inflater clone 到同一 Context。
- 验证：修复后 `build.bat`、`git diff --check`、资源表、内嵌 asset、binary Manifest、badging `v1.5.5/30`、v1/v2/v3 均 PASS；最终 SHA256 `7AA87ED146A61BE5DE5C931003668A472484DA5286802A22F0322A50FE8B5027`。因一次安装额度已用完，修正版未重装，空态/查询/滚动/Back/重开/bounds 为 `UNVERIFIED`。
- 结论：Q6 为 `UNVERIFIED`，不进入 Q7；不再安装、不提交、不推送。

#### QuickSearch Q5.1 最终修正版最小真机闭环

- 真机：最终 APK 通过唯一一次覆盖安装运行于 vivo X21A；设备拉回 APK 与本地 SHA256 均为 `3B54D46B8635AF76F95E0C3B1FF217737F8C02E0BF052B15BAECB5C443A30C47`，没有安装测试 App。
- Backend/性能：两次 Cold-A 均为 Snapshot=32、duplicates=0、READY legacy loader=0、hydration misses=0、Top5 requested/decoded=5/5。UI mapping 为 14/15ms；Cold-A 页面/第一名称/第一图标/稳定/图标空白/IME median 为 176/106.5/108/112.5/0/338ms。5 次有效 Warm 相同指标 median/P95 为 135/150、83/90、84/91、86/93、0/0、304/307ms；旧 Cold 1434/1470ms 与 Warm 399/527ms 图标空白均降为 0。
- 正确性/资源：拼音 3/3、首字母 3/3、普通应用点击 3/3；中文输入、Profile、Shortcut 当前无可靠或自然样本，记为 UNAVAILABLE。主线程打开窗口批量 DB/PM/decode、UsageStats、ICU 和网络均为 0。PSS 218353→190967KB，Native 57680→30212KB，Dalvik 12629→14960KB，Graphics 128740→116012KB，无明显泄漏。
- 稳定性：Launcher 相关 FATAL/ANR/CME/OOM/VerifyError/IllegalStateException 均为 0；全 buffer 的 36 条 IllegalStateException 是历史 radio `SST pid 2661 Service not connected`，不属于 Launcher/Q5。
- 结论：Early Search 按限制只尝试一次，但在 `LAUNCH_MODEL_READY` 前注入的 ADB 上滑没有产生 `QS_SHOW_TRIGGER`，不能作为搜索样本，shell 即时显示、Snapshot 阻塞和 READY 后自动补数据均保持 UNVERIFIED。该项属于 Q5 必选门槛，因此 Q5 最终为 `UNVERIFIED`；不重试、不重新安装、不开始 Q6。

#### QuickSearch Q4 SearchIconBridge

- 审计：原版 QuickSearch `base.apk` 仍作为历史行为基线；Q4 明确是现代 Launcher 一体化性能优化，不恢复历史 `quicksearch_decode/LauncherIconBridge`。Launcher 当前由 `Aa` / `ItemInfo` 保存图标来源字节，经 `MaintainedLauncherSettingsHost` 的默认/改进版/图标包/自定义链和 `IconRasterDiagnostics` 合成临时最终纹理，再上传 SMEngine。
- 实现：新增 `SearchIconBridge`，只读 `Aa.nc()` 模型 clone 的 private `iconData`；按 component/user/profile identity 匹配，返回 HIT/MISS/INVALID 和短期 `IconHandle`。不持有 Bitmap cache，不调用 `ItemInfo.Oe()`，不触发磁盘、PackageManager、网络或动态 ActiveIcon。
- 诊断：`SearchIndexRepository` 在模型 READY 后旁路调用一次汇总命中率诊断；不改变正式搜索，仍不读取 `SearchSnapshot`。
- 验证：`build.bat` 通过；`aapt2 dump badging` 显示 `v1.5.5/30`、minSdk 23、targetSdk 28；`apksigner verify` 的 v1/v2/v3 均为 true；Q4.1 APK SHA256 `1E27877532314627882BD5FDF3935D6F901F096F71CEFA12D267C1D4289AFB93`。覆盖安装成功一次；一冷启动、三暖态拉起未出现新的 `QS_ICON_BRIDGE`/decode 行。内存采样：TOTAL PSS 228894→228780 KB，Native Heap 64664→64296 KB，Dalvik Heap 14676→14688 KB；未建立 Graphics/Java 全量对比。
- 结论：Q4/Q4.1 当前为 `UNVERIFIED`，不能据此选择 Q5 方案；缺口是运行时诊断日志未出现，而非继续安装测试 APK。Q3 保持 `UNVERIFIED / NON_BLOCKING`，Q5 不启动、不提交、不推送。

#### QuickSearch Q2 SearchIndexRepository 基础架构

- 根因：Q1-A 证明当前搜索页面首帧和顶部 View 绑定很快，主要延迟来自打开搜索后才同步准备全部应用 label/icon；原版 `ApplicationsProvider` 则在后台预建进程内索引。当前 Launcher 已有 `LauncherModel/Aa.nc()` 克隆快照和 ItemInfo 的 title/package/component/user 字段，无需另跑全量 PackageManager 扫描。
- 实现：新增 bitmap-free `SearchEntry`、不可变 `SearchSnapshot`、进程级 `SearchIndexRepository` 与阶段 logger。Repository 使用单个后台线程，预计算 normalized label、profile serial 与字符串 iconKey；读取主 DEX Smali 模型使用后台反射桥，缺 label 时才按单组件补齐。任何异常进入 FAILED 并保留空/旧 Snapshot，不影响现有搜索。
- 时序修正：仅依赖首帧时，真机出现模型仍为空而 READY(0) 的失败样本；最终同时等待现有首帧 deferred hook 与原版 `J.MESSAGE_COMPLETE/LAUNCH_MODEL_READY`，不使用固定延迟或轮询。Q3 包增量、Q4 图标桥和 Q5 正式接入均未提前实现。
- 验证：`build.bat`、v1/v2/v3 签名和 vivo X21A 覆盖安装通过，设备/本地 APK SHA256 均为 `6D1B7E7E96B384C11C0749EDC1D5BE814A7F255AB9C4AE321F0FD8A5E0DCA29B`。五次进程冷启动索引 build 为 16/28/23/19/25ms，min/max/average/median/P95 为 16/28/22.2/23/28ms，5/5 均为 32 entries、duplicates=0。系统可启动 Activity 也是 32。当前搜索仍记录旧 `QS_LOAD_ENTRIES_BEGIN/END total=32`，未接 Repository。
- 风险：Q2 前后各 5 次首帧中位数为 241/253ms、P95 为 248/265ms，差值约一个 60Hz 帧；索引在约 2.3s 的模型完成后才开始，时间线无首帧阻塞关系，但小样本跨安装波动仍需后续扩大矩阵。当前设备没有多 profile 和同包多 Activity 真机样本，且 shell 无签名数据库读取权限，逐 identity 集合差分未完成。

#### 编辑模式顶部标题按刘海、挖孔和圆角安全区自适应

- 根因：截图中的“已选择 [0/12] 个应用程序”来自 `com.smartisanos.launcher.view.Lc.a(g,float,int)` 创建的 SMEngine `Mc`/`status_bar_text` 节点。原版和 `clean_launcher` 都只在 `sa.ub()` 命中特定 Smartisan 设备且非大屏模式时使用 `Constants.getStatusBarTextLeftMargin()`；移植到 vivo X21A 后该分支不成立，标题固定在 `window_width/2`，与中心刘海重叠。之前检查普通 Android View 层不会命中真实显示链。
- 修复：保留原版标题内容、字体、Y 坐标、淡入动画和 SMEngine 节点，只替换 X 中心计算。API 28+ 从 DecorView 的实时 `WindowInsets.getDisplayCutout()` 获取全部 bounding rect，按 Decor/scene 比例转换坐标并与标题真实纹理宽高检测相交；无相交保持居中，相交后按左安全段、右安全段、最大安全段选择。多开孔先排序合并，系统左右 Insets 参与内容边界；宽刘海使完整标题无法装入任何一侧时，使用真实 `safeInsetTop` 保护圆角边缘，避免贴屏幕 0 点。布局/Insets 变化会重新计算，并把节点更新排回 GLThread；不修改标题 Y、字号、文案或桌面其他状态栏节点。
- 原版对照：`launcher/smali/com/smartisanos/launcher/view/Lc.smali` 与 `clean_launcher` 的原始实现一致；本次没有复制 maintained UI，也没有恢复原版机型固定边距。原版截图左侧有视觉安全留白，当前宽刘海回退用系统 safe inset 得到同类布局，但数值来自本机窗口几何。
- 验证：`build.bat` 完整成功，最终 APK 覆盖安装到 vivo X21A Android 9，包版本 `v1.5.5/30`。ADB 读取该机 1080×2280、中心刘海边界 `Rect(358,0-722,79)`；通过 `/dev/input/event1` 注入真实双指捏合进入编辑多选界面，截图确认标题左边缘约 79px，不再位于刘海中心，也不再贴左侧圆角。安装后 Launcher PID 存活，未见本次兼容层引起的 `FATAL EXCEPTION`/`AndroidRuntime`。
- 兼容边界：无刘海和标题未碰到左/右开孔时仍保持原版居中；中心水滴/药丸孔、左右开孔、多开孔以及不同标题计数宽度均由同一几何算法处理。当前仅 vivo 中心宽刘海完成真机可见验收，其他异形屏属于实现与场景矩阵覆盖，不能写成全部机型真机通过。

#### QuickSearch 历史补录（原记录日期：2026-08-09）

#### QuickSearch Q8-C Original Search Semantics & Ranking

审计与修复：

- 以 `original_apks/quicksearch_phone_reference/base.apk`（SHA256 `EDF915A1CA745276F07538ABEDBBF43711B20426697E45A83A4C076ED0562D66`）及其 `decoded/` 为唯一 pristine 证据，确认 `applications` / `searchkey` schema、LIKE/INTERSECT 查询、HanziToPinyin 前缀 trie、profile/shortcut 边界和独立 History 关系。
- 新增 `docs/development/QUICK_SEARCH_Q8C_SEARCH_SEMANTICS.md`，记录已确认行为与 `UNCONFIRMED_PRISTINE_BEHAVIOR` 边界。
- 在既有 `SharedSearchMatchModel` 内补充后台完整拼音/词首 token form，并按空格分词逐 token 前缀匹配；未新增 Provider、SQLite、第二 matcher、T9 链路或 UI/IME/手势改动。
- `last_resume_time` 写入来源、`token_index` 完整表/视图及 Top Apps 最终排序在 pristine 证据中仍未完全确认，Q8-C 不据此虚报 PASS。

验证：

- `build.bat` 成功，`build/launcher-signed.apk` SHA256：`BADED65C2688E537EFD0B8F829B832010B0DED7F9C15FA30D0884AFB10A18573`。
- APK 签名：v1/v2/v3 `true`；aapt2 badging：`com.smartisanos.launcher`，versionCode `30`，versionName `v1.5.5`。
- 按 Q8-C 限制仅覆盖安装一次 Launcher APK，未安装测试 App、未清除数据、未重新全量扫描。启动日志出现 `QS_INDEX_READY generation=1`、32 条唯一 entry、无 FATAL/ANR/ConcurrentModificationException；设备当前前台仍为 vivo 原桌面，无法完成完整手势/输入语义矩阵。

结论：`Q8-C PARTIAL / UNVERIFIED`，不得启动 Q9；保留后续对 pristine 未确认字段的静态核查。

#### QuickSearch Q8-C.1 Original Search Semantics Evidence Closure

- 以 pristine `original_apks/quicksearch_phone_reference/base.apk`（SHA256 `EDF915A1CA745276F07538ABEDBBF43711B20426697E45A83A4C076ED0562D66`）及 `decoded/` 完成补充静态闭环：`token_index` 仅存在于未接入实际 query 的 `MIN(token_index)` 死字符串，schema 没有该列或来源；`last_resume_time` 的字段、投影和过滤读取已确认，但 QuickSearch APK 内没有写入调用，外部写入保持 `UNCONFIRMED_PRISTINE_BEHAVIOR`。
- 确认原版 Top Apps 五槽位来自 `Settings.Global.maybe_launch_pkg_from_predict_result` 的最多五个包名，由 PackageManager 取得 label/icon；History 和 hot-word 是独立列表。预测源生成方及最终稳定排序未由 pristine APK 证明，仍为 `UNCONFIRMED_PRISTINE_BEHAVIOR`。
- 确认 `FuzzyTonesHelper` 使用后台 HandlerThread 加载 provider-backed `fuzzytones.db`，`fuzzy_tones_enabled` 默认关闭；当前设备是否启用未确认。pristine `alias` 存在并参与 LIKE，但当前 `SearchEntry` 尚未接入 alias，保持 `UNCONFIRMED`。
- 更新 `docs/development/QUICK_SEARCH_Q8C_SEARCH_SEMANTICS.md` 的“PRISTINE EVIDENCE CLOSURE”章节。本轮代码修改 `0`、构建 `0`、安装 `0`，没有新增测试 App，也没有重新扫描应用。
- 已通过显式 Manifest HOME 组件 `com.smartisanos.launcher/.Launcher` 将当前已安装 APK 拉到前台，未修改默认桌面；随后清空 logcat 等待用户真实手指语义操作。当前尚无新的 `dianhua/dh` UI 证据，运行时语义和 Top Apps 五身份暂记 `UNCONFIRMED`，Q9 不启动。

结论：`Q8-C.1 STATIC_EVIDENCE_CLOSED / RUNTIME_PENDING`；不得安装、构建或推送以补齐未知项。

#### QuickSearch Q8-D.1 Final Runtime Visual Verification

- 本轮按用户授权仅对 vivo X21A 执行一次 `adb install -r -d build/launcher-signed.apk`，本地 SHA256 已核对为 `E09A29F2EF4404EEEAB123FCF48144F8F3EACE24749150977BD58A8DA55329D7`；命令超时，未重试。
- 超时后按规定检查设备：`lastUpdateTime=2026-08-09 22:06:16`，设备实际 APK SHA256 仍为 `BADED65C2688E537EFD0B8F829B832010B0DED7F9C15FA30D0884AFB10A18573`，前台为 `com.android.packageinstaller/.PackageInstallerActivity`，未达到目标 APK 一致性，立即停止。
- 未进行真实手指视觉验收，未清 Launcher 数据、未安装测试 App。Q8-D.1=`UNVERIFIED / INSTALL_TIMEOUT`；Q8-D 不得改为 PASS，Q9 不启动。

#### QuickSearch Q8-D.1 真机回放发现与修正

- 目标 APK 后续在 vivo X21A 设备一致；真实进入 Original Search、IME、Top Apps=5、History=4 成功，`微信`/`电话` query 各命中 1 条。
- 点击 History 清除 X 触发 Launcher `FATAL/InflateException`。根因是嵌入 QuickSearch 资源包 Drawable ID 被直接传给宿主 `View.setBackgroundResource()`，宿主资源表将 `0x7f030002` 解为 `layout/abc_action_menu_item_layout`。
- 已将 Dialog panel/button 改为 `uiResources.getDrawable(id)` + `setBackground(Drawable)`；未再次安装。修正版构建 APK SHA256=`77DD92989E3AF1884735809D05C2921876A9C5B60C2C33449DA55BC63E6ED39C`，v1/v2/v3 通过。
- 结果区层级截图已确认 header、白色 row、divider 与淡蓝灰区域仍需修正版重新验收；Q8-D.1=`FAIL / RUNTIME_UNVERIFIED`，Q9 不启动。

#### QuickSearch Q8-D Original Search Result + Dialog Fidelity

- pristine 审计确认应用结果 header 来自 `header.xml` / `StickyListHeaderStyle`，标题源为 `application_desc`（中文“应用程序”），14sp bold、12dp 左内边距、`#f5f5f5` 背景；应用 row 继续使用 60dp / 30dp icon / 16sp bold 的 `list_item_nophoto_bg`，divider 为 `list_divider_drawable` 的 `#14000000`、2px。
- pristine `SearchActivityView.L()` 创建 `i/p/a` `MenuDialog`（普通 Dialog，底部对齐、透明 Window、dim、右上关闭、红色大按钮），不是 Android AlertDialog。当前 OriginalQuickSearch 已接入结果 header、divider、literal query `ForegroundColorSpan(#d44d44)` 和专用底部清空 Dialog；无结果时不显示 header，空态淡蓝灰背景保持不变。
- 新增 `docs/development/QUICK_SEARCH_Q8D_RESULT_PRESENTATION.md`。本轮 `build.bat`、`git diff --check` 通过；未安装 Launcher、未安装测试 App。状态：`CODE_COMPLETE / RUNTIME_UNVERIFIED`，不得启动 Q9。

### 2026-08-08

#### 图标系统文档冻结与旧专项审计清理

- 2026-08-21 复审更正：本节只能保留为当时的架构目标，不能作为当前验收结论。普通静态来源仍可能在 managed 生素材与数据库预合成回退之间分叉，ActiveIcon world-bounds 校正也没有现有真机样本的运行时命中证据；当前只确认普通 Cell 的最终 physical geometry、阴影、用户百分比和缓存规格原则共享。“统一”不指所有形状具有完全相同的可见宽高，也不代表所有来源、动态状态和分辨率已经验证。
- 防回归：冻结架构、合成顺序、缓存键字段、禁止倍率和剩余验证矩阵已同步写入项目 `MEMORY.md` 与 `LAUNCHER_FIX_AND_OPTIMIZATION_PLAN.md`。删除已被当前实现取代且包含 DEFAULT-only、旧 `raster:v8` 和“optical normalization 尚未完成”等错误状态的 `ICON_PROFILE_RASTER_AUDIT_2026-08-07.md`；`LAUNCHER_FIX_AND_OPTIMIZATION_PLAN.md`、`LAUNCHER_STARTUP_BASELINE.md`、`ORIGINAL_BEHAVIOR_REFERENCE.md` 分别承担总体计划、启动实测和原版链路职责，继续保留。
- 生产清理：关闭 `DEBUG_RASTER_DUMP`，诊断字段和按需导出代码保留，正式构建不再持续写入 `DEBUG_ARTWORK/DEBUG_TEXTURE/metrics.tsv`；需要专项验收时才临时启用，验收后必须恢复关闭。
- 验证：`build.bat` 完整成功；最终 APK 为 `v1.5.5/30`，v1/v2/v3 签名验证通过。vivo X21A 保留数据覆盖安装返回 `Success`，HOME 冷启动 `Status: ok`，Launcher PID 存活，启动日志未见 `AndroidRuntime` fatal。本次未清 Launcher 数据、未移动桌面 Item。
- 验收边界：vivo X21A 1080/12 宫格/当前 100% 是已完成真机基线；50/150、1080 20 宫格、1440/2K 12/20 宫格、720 或 1220/1260 中间分辨率、完整来源切换、冷启动和设备重启保持仍未全部完成。当前只能写“架构与算法统一”，不能写“所有手机均已验证”或 `ICON_SYSTEM_VALIDATION_FROZEN=true`。

#### 【已废弃】当前 1080 与原版截图的图标尺度复核（基于面积补偿方案）

#### 【已废弃】Weather/Calendar 静态 fallback 与动态外轮廓统一（基于面积补偿方案）

#### 【已废弃】图标统一几何、静态合成与最终缓存收敛（面积补偿方案）

### 2026-08-03

#### 搜索页常用应用的使用情况访问门控

- “显示搜索页常用应用”现在独立复用角标提醒的权限门控逻辑：绑定设置项时先检查 `AppOpsManager.OPSTR_GET_USAGE_STATS`，没有使用情况访问权限时强制保持关闭，不提前写入开启值。
- 用户点击开启且未授权时只显示锤子风格提示，并提供前往系统设置；取消、返回未授权或之后撤销权限都会保持/同步为关闭。只有从系统设置返回并确认权限已授予后，才写入开启值、更新开关状态并应用搜索页设置。
- 搜索页本身不依赖该权限，未授权时仍可正常打开；权限仅用于按实际使用频率显示固定的 5 个常用应用。中英文提示资源已复用现有 `search_usage_access_*` 字符串。
- `build.bat` 与 `git diff --check` 已通过；当前无在线 ADB，尚未完成 Android 8–16 真机权限授予、取消、撤销和返回场景矩阵。

#### 备份恢复与小程序快捷方式图标隔离

- 根因收敛：恢复会重建 `table_iteminfos/table_icons`，而旧备份或缺失的 `shortcuts.json` 没有逐快捷方式位图；随后桌面重新加载时只能从来源应用回退，表现为微信头像/失去圆环。普通改进版图标刷新本身只查询 `itemType=0`，但恢复前没有保留旧快捷方式缓存，导致兼容边界不完整。
- 修复：恢复事务删除数据库前按“来源包名 + shortcutId + userSerial”暂存当前 `QuickLaunchItem(itemType=1)` 的 `table_icons` BLOB；恢复优先使用备份中的逐快捷方式记录，旧备份或记录缺失时按稳定身份回填当前原始位图。改进版图标恢复后仅对已有本地资源主动刷新普通应用，快捷方式仍由原版最终位图链路消费。
- 验证：`build.bat` 完整构建、重打包、对齐和签名成功；`git diff --check` 通过。当前 ADB 无在线设备，尚未完成真机备份/恢复与动态图标切换截图回归。

#### 【备份目录双路径已被 SAF-only 方案取代】备份目录选择器与设置项默认值

- 历史版本曾提供“手机系统目录/应用专用目录”双选项；2026-08-15 起应用专用目录及选择弹窗已删除，当前只保留 SAF 手机系统目录。本段不得作为当前入口说明。
- 新安装或缺少历史键时，“显示搜索页常用应用”和“解锁动画”均默认关闭；已有用户显式保存的开关值不被覆盖。中英文资源均已补齐。
- `build.bat` 和 `git diff --check` 已通过；当前无在线 ADB 设备，未完成真机对话框截图和 Android 8–16 矩阵验证。
- 选项行改为独立的圆点控件与文字横向布局，增加与正文一致的左侧内边距，避免圆点贴近弹窗边缘；备份行为和默认值不变。
- 目录选择弹窗已拆到 `MaintainedBackupStorageDialog.java`，宿主仅保留入口和备份/恢复回调；选择圆点改为固定颜色和线宽的轻量自绘控件，避免不同 ROM 的原生 RadioButton 样式漂移。宿主减少约 77 行，完整构建通过。
- 复测发现上一版将 66dp 误用于左侧内缩，导致高密度设备圆点偏右；现改为 11dp 行内边距 + 30dp 圆点容器，使圆点中心与正文 26dp 起始线一致。

### 2026-08-02

#### PIN 小程序图标、恢复去重与冷重载白闪

- **跨 Launcher 残留 pin 边界（OPPO Android 12 真机）**：用户复测出现“新小程序可以弹窗并显示、以前添加过但当前桌面已无图标的小程序不再弹窗”。`dumpsys shortcut` 确认当前默认桌面及 shortcut access 均为 `com.smartisanos.launcher`；新成功的小程序 ID 归 Smartisan Launcher，而两个旧 ID 仍归 `com.android.launcher`。Android 只允许当前 Launcher 查询和维护属于自己的 pinned IDs，`LauncherApps.getShortcuts(FLAG_MATCH_PINNED)` 因此只返回新成功的 1 项；旧系统桌面残留的两个 ID 不会进入 Smartisan 的确认 Activity、回调或对账链。不得把这种跨 Launcher 所有权残留误判为 `QuickLaunchItem`、圆环合成或数据库补建失败，也不得通过清空微信全部 shortcuts、清除系统桌面数据等破坏性方式静默修复。安全恢复需要旧 Launcher 主动解除对应 pin，或由用户明确授权清理系统 ShortcutService 中微信的旧 shortcut 状态。
- **搜索页常用应用与使用情况访问**：恢复原版搜索栏与“搜索历史”之间的应用入口，但不恢复旧版一次创建最多 20 项、滚动吸附和延迟 Runnable 的实现。继续复用既有后台 `loadSearchEntries()` 与 `searchShortcut()`；数据到达后在固定单行只生成 5 个不同包名的普通应用，优先读取系统过去 30 天的前台使用时长，不使用搜索历史排序。强迫症选项中“上滑打开搜索页”下新增独立的“显示搜索页常用应用”开关；关闭后不创建该行。APK 已有 `PACKAGE_USAGE_STATS` 声明但没有可自动授予的运行时权限：当用户打开搜索页或常用应用开关、且常用应用已启用而 Usage Access 未授予时，显示现有锤子样式确认框；只有用户点“去设置”才启动系统 `ACTION_USAGE_ACCESS_SETTINGS`，取消不会阻断搜索。ROM 未向 Launcher 授予 UsageStats 时仍安全回退为稳定名称顺序；不联网、不在主线程扫描/解码。
- **【已废弃】删除 v1.5.5 `final_icon` 直通、强制所有 PIN 快捷方式重新经过原版合成的试验方案。**
- **当前修复**：用户复测确认该试验会让新添加快捷方式完全不显示，而 v1.5.5 可以添加并显示圆环。现恢复 v1.5.5 的位图归一化、微信/支付宝提供方装饰识别和 `final_icon` 序列化路径；保留后来增加的请求确认、profile 身份、数据库落库确认与失败回滚，不回退其他 PIN 兼容修复。
- **恢复去重**：`RestoreMergePlanner` 以前只认识 `shortcut_id/shortcutId`，遗漏了当前兼容 Intent 的 `smartisan.shortcut.id`，并对完整 Intent 做哈希；因此同一个小程序被当作“当前新增条目”保留后，又从备份恢复一次。现在解析兼容 Intent，按 `来源包名 + shortcutId + userSerial` 生成稳定键；普通应用仍按既有组件键处理。备份中已有的普通应用/同一小程序不会再把当前同一项附加回去。
- **逐帧证据与白闪修复**：用户提供的 720×1600、约 46fps、1.834s 视频共抽取 84 帧；第 34 帧（约 0.72s）左侧 `0–63px` 出现约 99% 高亮的系统启动窗口残片，下一帧已进入黑色加载面。根因是私有 `:reload` Activity 的系统预览仍为白色 `Theme.NoTitleBar.Fullscreen`，而 Java 仅在 `onCreate()` 后设黑。文本 Manifest 和实际注入的二进制 Manifest 均改为 Android 公共 `Theme.Black.NoTitleBar.Fullscreen`（`@0x0103000a`），与现有黑色 Loading 根一致；未改变 token、旧 PID、首帧握手、Loading 布局或任一动画时长。
- **验证与风险**：`build.bat` 完整通过；最终 `build\\launcher-signed.apk` 为 `v1.5.5/30`，`aapt2 dump xmltree` 确认 `ReloadTransitionActivity` 的二进制 theme 为 `@0x0103000a`，`apksigner` v1/v2/v3 验证通过。尚未在已连接设备执行实际恢复（会改写用户当前桌面），因此小程序圆环、同一小程序恢复不重复和白闪消失仍需在该 APK 上完成一次真实恢复验收。

### 2026-08-01

#### 关于页：移除操作日志并新增使用小技巧

- **根因与范围**：操作日志是 About 页面独占的临时诊断功能，包含持久化状态、`operation_logs` 私有目录、logcat 子线程、文件扫描、预览、合并和发送；它既不属于普通崩溃诊断，也不为其他设置功能服务。
- **修复**：删除 About 宿主对该区域的绑定，以及这条专用录制/扫描/分享链和相关状态字段。保留现有 `android.util.Log`、崩溃诊断、更新安装和其他设置逻辑。About 仍使用原有 `ScrollView`，在“关注我们”之后加入静态 `setting_tips_view`：四个分组均复用 `setting_follow_view.xml` 的分组标题、颜色、边距及三段圆角列表 drawable；每项采用主标题和可换行副说明，不增加按钮、弹窗、线程或跳转。
- **本地化与验证**：27 个 `usage_tips_*` 键成对写入默认英文与 `values-zh-rCN`。`build.bat` 完整通过，最终 APK 为 `v1.5.5/30` 且 v1/v2/v3 签名验证通过；Android 17 `1440×3120` 模拟器覆盖安装后，About 可打开、返回，英文四组全部可见并可滚动至最后一项，底部保留导航栏安全空间，UIAutomator 未见操作日志文本。Android 8/12/14/16、小屏/异形屏的真实设备矩阵尚未连接，不能声称已完成全机型真机验收。

#### 桌面备份与恢复：原版页表兼容、页面统一与真实备份修复

- **根因**：首版把 `table_pageinfos.pageIndex` 错当成唯一且非负的业务主键。原版页表实际可含负值的特殊页、预分配空页及重复页索引，导致 Android 9/12 的现有布局在导出校验阶段报 `Invalid pageIndex` 或 `Duplicate page index`，备份无法创建。
- **修复**：页表改为以原版 SQLite 主键 `_id` 做唯一性校验，保留原始 `pageIndex/status/containment`；恢复校验同样只验证 `_id`，新增保留应用时按实际已使用的根级页追加，并为真正新增页分配新的 `_id`。布局快照继续按原版列白名单读写 `table_pageinfos.pageTitle` 和 `table_iteminfos.title`，所以页面分组标题、文件夹标题、文件夹内容及位置会一起轮转。预览的“桌面板块数量”改为实际含根级内容的页面数，不再显示页表预分配容量。
- **界面**：首页入口移到“设置默认桌面”下、“关于我们”上；管理页去除手工 `>`，统一使用 `setting_next`，标题和右侧值采用一级设置的字号/颜色，右侧值与箭头留出固定但紧凑的间距，标题会自动让位。已选择的 SAF 目录显示其 document-id 路径（如 `/Download/LauncherBackup`），而不是泛化的“已选择目录”；这不是假定存在可访问的真实文件系统路径。恢复预览页同步使用相同的行高、字重、颜色和卡片宽度。说明明确列出会备份的页面/文件夹/位置/设置/主题/名称/图标，以及不会备份的壁纸、应用数据、账户、权限、默认桌面、密码、天气缓存和定位信息。
- **进度与恢复**：备份、校验和恢复均继续复用 `SmartisanProgressDialog` 显示阶段状态；恢复确认后仍走既有 `:reload` 冷重载，桌面首帧后再结束过渡，备份本身不重载桌面。
- **恢复结果与图标（schema v3 更正）**：提示与冷重载时序继续有效。旧归档不保存在线改进版 RAW，只能后台补齐；2026-08-21 起新归档通过 `icons/sources.json` 保存可移植改进版 RAW source。最终 raster 仍是可丢弃缓存，不进入普通应用备份真相。
- **验证边界**：用户提供的 vivo X21A Android 9 截图已显示 2026-08-01 的成功备份、恢复预览和可撤销状态；本地 `build.bat` 和 Android 17 模拟器覆盖安装通过。Android 12 及 Android 8/10/11/13–16 的真实 SAF Provider、恢复、撤销、杀进程恢复仍需逐机复测，不能用单机成功代替全机型承诺。

#### 移除 Shizuku 默认桌面通道

- **原因**：vivo X21A Android 9 实测 `cmd package set-home-activity` 可短暂返回成功，但用户按 Home 后系统会触发 `vivo.action.HOMERECOVERY` 并恢复 `com.bbk.launcher2`；该通道不能保证默认桌面真实持久生效。
- **处理**：移除设置页 Shizuku 选择/弹窗/文案、桥接和 UserService、离线 Shizuku JAR、文本与二进制 Manifest 的 Provider/权限/元数据以及构建期 AXML 修补器。原“设置默认桌面”入口恢复为只走既有 Android Role / 系统默认应用设置。
- **验证**：`build.bat` 重新构建成功；最终 APK 的 AXML 未发现 `ShizukuProvider`、`API_V23` 或 `V3_SUPPORT`，APK ZIP 与源码运行链均未发现 Shizuku/Rikka 类。

### 2026-07-31

#### 【已废弃】桌面备份与恢复（早期实现与构建级验证）

#### 【已废弃】Shizuku 可选默认桌面授权通道

#### Android 9窗口动画私有framework资源导致壁纸空白（修复、vivo真机验证完成）

- **现象与根因**：vivo X21A Android 9 安装后首次打开或从其他界面返回锤子桌面时，偶发只剩系统壁纸；退出再进入后恢复。ADB确认 Launcher进程、前台Activity和`smt_launcher` Surface均存在，没有Launcher侧`FATAL EXCEPTION`。实际异常来自系统WindowManager在`AppTransition.loadAnimation()`阶段反复抛出`Resources$NotFoundException: Resource ID #0x10a0177`。最终APK及原版APK的`LauncherActivityTheme -> @style/Animation`均保留了Smartisan framework私有的`0x010a0177/0x010a0178`，而该vivo framework的动画资源只到`0x010a00bd`，窗口布局因此可能在过渡期间中断。
- **修复**：仅把`style/Animation`中9个仍指向私有资源的task open/close、wallpaper open和wallpaper intra open/close值改为`@null`，与该样式其余空过渡项保持一致。新增`tools/patch_launcher_window_animation_resources.py`，按属性ID、旧资源ID和唯一出现次数校验后二进制修补`launcher/resources.arsc`；意外资源表会直接失败，不会宽泛替换。未修改Launcher内部翻页、文件夹、主题、解锁、Cell回弹、Timeline、duration或Surface生命周期。
- **最终包检查**：`build.bat`成功；`aapt2 dump resources`确认`style/Animation`的25项全部为`@null`，最终APK中`0x010a0177/0x010a0178`命中数为0；badging为`v1.5.5/30`，v1/v2/v3签名验证通过。最终APK的101个framework资源引用与vivo Android 9、SDK30、SDK34、SDK36资源表比对均无缺失；Manifest的41个framework引用在vivo Android 9上也无缺失；Smali/Java未发现硬编码`0x01xxxxxx` framework资源ID。
- **真机验证**：vivo安装器覆盖安装且保留数据后，执行5次`force-stop -> LauncherAlias`冷启动，全部`Status: ok`且前台为`smt_launcher`；执行8次`系统设置 -> Back`返回，全部回到同一Launcher窗口。`cmd package compile -m verify -f`成功，最终截图确认12宫格实际可见。完整测试日志未出现`FATAL EXCEPTION`、`AndroidRuntime`、`NullPointerException`、`VerifyError`、`Resources$NotFoundException`、`NoSuchMethodError`、`ClassNotFoundException`、`UnsatisfiedLinkError`、native fatal或Launcher ANR。
- **风险边界**：本次已清除当前APK中同类“引用不存在的Android framework资源”问题，但静态审计不能证明所有厂商ROM和所有业务入口都不会崩溃。Android 6/8、三星/小米/华为/一加等真实设备未在本轮连接验证；动态天气、主题切换、宫格重载和低内存进程恢复仍按各专项矩阵验收，不能用本次启动通过替代。

#### 【已废弃】动态天气/日历阴影复用静态原版生成器（v4/v5）

### 2026-07-30

#### 【已废弃】受管静态图标独立复用原版主题阴影（v6）

#### 设置页截图范围英文本地化补齐（构建、英文1440×3120模拟器关键页面验证完成）

- **根因**：`values/strings.xml` 已有大量英文基线，但 maintained 兼容宿主仍直接写入中文。英文系统因此会在强迫症角标、授权弹窗、主题卡片、图标设置弹窗、应用分身、隐私密码、宫格切换和检查更新弹窗中混入中文；图标页还用中文标题字符串判断行类型，直接翻译会使箭头和副标题标签逻辑失效。
- **修复**：为上述页面新增成对的默认英文与 `values-zh-rCN` 中文资源，Java 统一通过 maintained `Resources` 获取；主题卡片按 `ThemeEntry.id + "_name"` 映射显示名，文艺系列补齐稳定资源键；图标页以 `rowType` 判断“图标样式/桌面图标大小”，不再依赖显示语言；更新弹窗的无版本、最新版本、新版本、无 APK、失败和下载状态均改为格式化资源。
- **边界**：未修改设置页布局尺寸、功能开关语义、主题 id/包名、图标来源存储、隐私密码数据、宫格迁移与 Launcher 重载逻辑；未提交、未推送。
- **验证**：`build.bat` 完整构建成功，APK `versionName=v1.5.5 / versionCode=30`，v1/v2/v3 签名通过。只覆盖安装到 `emulator-5556`（`1440×3120`、`en-US`），未操作 1080P 真机；UIAutomator/截图确认主页宫格、OCD 角标、通知授权弹窗、应用分身空态、隐私密码输入、图标设置列表、图标来源弹窗和图标大小弹窗均显示英文。主题名称由已编译资源和稳定 id 映射验证，主题页未完成本次可见触发；检查更新网络各分支未逐项触发。

#### 普通桌面高分辨率图标与一次性高清纹理基线（构建、1440×3120模拟器当前20宫格验证完成）

- **根因**：用户提供的两张截图分别为 `1440×3120` 与 `1080×2400`。当前 `values-sw411dp` 使用 `dock_width=1440`，但 12/20 宫格图标内容和阴影尺寸曾被统一降为与 1080 资源相同的 `160/205`、`118/152`；`LayoutPropertyAdapter` 为避免普通桌面再次被放大污染，整体适配倍率最大为 `1.0`，因此 1440 Cell 变宽后图标不会补偿放大。对照 `clean_launcher_raw` 确认原版 1440 基线应为 12 宫格 `192/246`、20 宫格 `138/178`。
- **修复**：只恢复 `launcher/assets/layout/portrait/values-sw411dp/MODE_12` 与 `MODE_20` 的原版高分辨率内容组输入：图标 `192/246`、名称偏移 `-131`、设置按钮 `134`；图标 `138/178`、名称偏移 `-100`、设置按钮 `134`。2160×1080、2242×1080、2340×1080、`values-xhdpi` 和 `values-xxhdpi` 等 1080 坐标系资源保持不变。中间宽度设备仍由现有适配器按 `实际宽度/1440` 向下等比适配，超过原版 1440 手机基线时不无限放大。
- **高清链**：未增加 SceneNode 局部 scale。默认 APK 图标继续由原版 `e.s.a(Drawable)` 按适配后的 `icon_size_origin` 直接绘制目标 Bitmap，再由原版阴影链生成对应 `icon_size_with_shadow` 纹理；没有先生成固定 1080 小图。改进版、图标包、在线 PNG 和自定义源由 `IconRasterDiagnostics.resolveNormalIconRasterSpec()` 读取同一最终尺寸并结合 Surface 像素倍率，`composeStaticIconTexture()` 从保留的源图一次采样到最终物理纹理。桌面设置按钮使用相同 `rasterScale`。因此 1440 的 12 宫格目标为内容 `192`、纹理 `246`，存在额外物理 Surface 倍率时继续生成更高物理像素纹理，而不是把旧 `160` SceneNode 放大。源 APK 自身只提供低分辨率位图时仍受源素材上限约束；受管源会记录 `ICON_LOW_RES_SOURCE_LIMITED`。
- **边界**：没有修改普通桌面 Cell 中心、行列数、文字字号、Dock 高度、打开文件夹、文件夹 Timeline、动画 duration、`Eb.update()`、`Ra.T()` 或用户 50%～150% 图标比例；关闭文件夹预览只随普通桌面外框使用同一最终尺寸，不增加独立二次倍率。
- **验证与风险**：资源矩阵静态检查确认只有 `values-sw411dp` 的 12/20 宫格基线变化，1080 系列保持原值；`git diff --check`、`build.bat`、最终 APK 资源反读、`aapt2 dump badging` 和 v1/v2/v3 签名检查通过。`1440×3120/560dpi` 的 `emulator-5556` 覆盖安装成功，保留原有20宫格配置回到桌面；图标及文字完整、设置按钮日志为 `logicalSettingButton=134/finalTexture=134×134`，截图未见小纹理放大模糊，日志无 `AndroidRuntime/FATAL EXCEPTION/VerifyError`。未改动已连接的 1080 vivo。仍需在 1220/1260/1440 真机、12宫格、默认/改进版/图标包/自定义源、50%/100%/150%、动态天气日历和关闭文件夹预览中做可见验收。

#### 【已废弃】普通桌面静态纹理真实 Cell 尺寸与缓存隔离（v5）

### 2026-07-29

#### SMEngine稳定固定步长与刷新率识别（构建、60Hz OPPO真机验证完成）

- **根因与修复**：真实长帧差值一次性送入 `Ra.T()` 会使文件夹、解锁、翻页、主题和Cell回弹突然追赶；按屏幕宣称刷新率选步长又无法处理120Hz屏幕实际只渲染60fps。新增 `AnimationFrameRateController`：默认60fps，使用无分配EMA，忽略首帧、后台/Surface恢复帧和大于25ms的异常长帧；候选档连续稳定24帧并通过迟滞后才切换60/90/120/144档。`Eb.update()` 每帧只将 `20×60/effectiveRenderFps` 送入原版 `Ra.T()`，不追赶长帧；暂停、恢复和Surface重建时重置采样。
- **边界**：未修改文件夹Timeline、duration、scale、alpha、interpolator或局部速度倍率。
- **验证与风险**：确定性测试得到60/90/120/144fps分别为 `20/13.333333/10/8.333333`，偶发40ms长帧不改变120档。`build.bat`、v1/v2/v3签名和OPPO PDCM00覆盖安装成功；当前OPPO只提供60Hz实际渲染，90/120/144Hz墙钟时长仍需对应真机。

#### 打开文件夹内容组、标题和分页节点自适应（12/20宫格OPPO真机验证完成）

- **原版对应关系**：普通12宫格为3×4，图标内容/阴影尺寸为 `160/205`；普通20宫格为4×5，对应 `118/152`。两者打开文件夹后都进入独立模式8和固定3×3布局。本机文件夹值为内容 `192`、阴影 `184`，没有按外部12/20宫格缩放；本轮不缩小文件夹图标。
- **原版资源恢复**：临时写入 `2242x1080`、`2340x1080` 的 `-82/350/1840` 固定像素方案已撤销；两个 `layout.xml` 均恢复原版 `nameOffset/titleY/dotY=-72/253/1757`。
- **内容组与行中心**：`FolderCellPositionAdapter` 精确门控真实 `t` 容器与模式8，按 `358×folderBookcaseWidth/1080` 计算行距。`FolderVisualGeometry` 从图标阴影尺寸扣除原版可见底边内缩，再以独立 `appLabelGap=20×scale` 计算文字中心；图标、阴影和文字的完整内容组中心用于修正每层Cell，而不是单独强推 `name_off_set_y`。
- **标题与分页节点**：标题以书架可见顶部 `y=129/1356` 为锚点，`titleGap=300×scale`。原纹理实心外框最后一行是 `y=1224`，其下为长投影；分页点现以实心外框下沿为锚点并使用 `indicatorGap=44×scale`，OPPO节点中心Y为 `1746+44=1790`。`Z`节点实际位置和 `FolderSceneMetrics` 安全区边界消费同一结果。
- **隔离**：没有修改共享 `LayoutProperty`、`Constants.mode()` 返回对象、普通桌面资源、关闭预览或动画。`FolderSceneMetrics` 必须同时命中精确 `FolderPageView(t)` 与模式8；OPPO日志为 `scale=1.0 translateX=0.0 translateY=0.0 clip=0,96-1080,2310`。
- **验证**：纯计算覆盖720×1600、1080×1920、1080×2400、1440×2560、1440×3200。`build.bat`、v1/v2/v3签名和OPPO覆盖安装通过；12/20宫格普通桌面及打开文件夹无 `FATAL EXCEPTION/VerifyError`，设备最终恢复12宫格。
- **风险**：当前文件夹只有一页，分页节点不会绘制，最终44px间距只完成纹理边界、纯计算和节点接入验证，仍需多页文件夹可见验收。其他尺寸/ROM、隐藏/加密文件夹、其他主题尚无真机矩阵。

#### 普通桌面与文件夹派生布局隔离（构建、OPPO 真机验证完成）

- **根因**：`fa.ir()` 是普通桌面 Page 与打开文件夹容器共用的坐标入口。本轮文件夹综合自适应把原有 `FolderCellPositionAdapter.adaptPositions(owner, points)` 改成无 owner 参数的 `FolderLayoutMetrics.adaptPositions(points)`，导致普通 12/20 宫格也收到固定三列文件夹行坐标；同时 `FolderLayoutMetrics` 通过反射把书架、标题、分页点等派生值写回传入的 `LayoutProperty`。
- **修复**：`fa.ir()` 恢复 owner 门控，只有类层级确认为 `com.smartisanos.launcher.view.b.t` 的打开文件夹容器才复制并调整坐标；普通 `fa` Page 原样返回 `Constants.pageCellCenterPoints`。共用 `M.smali` 中本轮文件夹坐标调用保持移除。`LayoutPropertyAdapter` 遇到 `_folder` 时提前返回，不再对传入对象做文件夹专用缩放；实验性的 `FolderLayoutMetrics` 随后已完整删除。该阶段未修改 MODE_9/12/20 资源、数据库、Timeline、`Eb.update()`、`Ra.T()`、刷新率检测或动画 duration；后续阶段的变化以同日更靠上的记录为准。
- **真机验证**：`build.bat` 成功；最终 APK 为 `v1.5.5 / versionCode 30`，v1/v2/v3 签名通过。OPPO PDCM00 (`Android 12`) 使用 `adb install -r` 覆盖安装且不清数据；冷启动 HOME 成功。12 宫格显示 3×4 原布局，20 宫格显示 4×5 原布局，图标/文字随宫格模式恢复各自尺寸，桌面设置入口位于底部，关闭文件夹预览正常，普通 Page 无文件夹书架。打开文件夹时书架只出现在文件夹页；日志无 `AndroidRuntime`/`VerifyError`。验证后已将设备从临时 20 宫格恢复到原 12 宫格。
- **剩余风险**：本轮仅完成普通桌面恢复和单个打开文件夹的观察性检查；第二桌面页、Dock 的复杂内容、隐藏/加密板块、文件夹多页、不同分辨率/ROM 尚未形成完整真机矩阵。文件夹完整几何与高刷新率动画必须继续作为两个独立任务，不得在本修复中混做。

### 2026-07-28

#### Android O+ PIN 快捷方式请求与桌面数据一致性（构建、安装完成；真机矩阵待验证）

- **真机根因**：OPPO PDCM00 (`Android 12`，`PZXO8PHMONGYVSOZ`) 的实时 `logcat` 与 `dumpsys shortcut` 显示，微信分身运行在 `u999`；新添加的小程序已处于该用户的 pinned 集合，但 `cmd package resolve-activity --user 999` 无法解析 `com.smartisanos.launcher/.PinShortcutConfirmActivity`。因此没有确认弹窗时，系统会保留 pinned 状态而 Launcher 不会收到可落库的 `PinItemRequest`，表现为“有时没有弹窗，添加后桌面没有图标”。这与主用户可解析确认 Activity 的成功路径不同，并非随机。
- **对照与修复**：对比 maintained `6798dd765e478026c5207c3ed1b5b9a357405cba` 后，当前确认页取消 `singleTop`、`queuedIntents`、`onNewIntent()` 和多请求循环；Manifest 保留 `exported=true`、`Theme.Translucent.NoTitleBar`，新增 `stateNotNeeded=true`。每个 Activity 只读取自己的 `getIntent()`、展示一次确认并在取消/关闭后结束。调用当前原版 `F.b()` 时恢复第二项 Activity/Context 参数，仍使用当前 `EVENT_INSTALL_OR_UPDATE_SHORTCUT`，不覆盖 `F.smali`。
- **提交语义**：`ShortcutCompatBridge.dispatchInstall()` 的反射不再被当作落库成功。确认后记录 `PIN_ACCEPT_*` 与 `PIN_DATABASE_DISPATCH_*`，再以最终 `ShortcutLaunchActivity` Intent 查询原版快捷方式表；只有找到行才记录 `PIN_DATABASE_ROW_FOUND`、`PIN_COMMIT_SUCCESS`。失败会只移除本次 shortcut ID 的 pin，记录 `PIN_COMMIT_FAILED` 与 `PIN_ROLLBACK_UNPIN_SUCCESS`，不会清空同包其他小程序。原版当前 Action 已按完整 Intent 做 upsert，Intent 包含 `shortcutId + userSerial`，所以同一小程序重复请求更新、不同微信小程序及主/分身独立存在。
- **一致性修复**：在 `SmartisanInstallManager.onLauncherModelReady()` 后的后台线程查询 `FLAG_MATCH_PINNED`；`LauncherApps.Callback.onShortcutsChanged()` 也在模型就绪后补查。系统 pinned 存在而 Launcher 数据库缺失时复用同一原版转换/入库路径补建；不在首帧、每帧或 PIN 请求队列中执行该扫描。
- **验证状态**：`build.bat` 成功完成 maintained 资源、Smali、Java compatibility host、二进制 Manifest 注入、zipalign 和签名；`adb install -r -d build\\launcher-signed.apk` 已成功安装至 OPPO PDCM00，并强制重启 Launcher。完整 PIN 真机矩阵尚未完成：同一/不同小程序重复、取消后重试、确认后切桌面/杀 Launcher/重启、删除后重加、主微信/分身微信及支付宝均待以 `PIN_*` 日志和桌面 Cell/启动结果验收。本条不得解读为功能已完全验证。

#### 应用图标有效来源与分组口径收敛（构建完成，真机待验收）

- **问题**：桌面、应用图标列表右侧预览、单应用页顶部预览和“已重绘/未重绘”分组此前各自使用候选缓存、系统原图或数据库状态，导致同一应用在三个位置显示不一致；同包多 Activity 的拨号/联系人还可能因标签或包名兜底而串图。
- **收敛状态**：保留全局 `DEFAULT` / `IMPROVED` / `PACK:<package>` 单选和单应用手动覆盖优先级，统一由当前有效来源解析桌面、列表与单应用顶部预览；分组改按实际可解析的当前图标判断。系统图标映射改为组件优先，并只对系统应用应用标签别名，避免第三方同名应用或同包双 Activity 被错误套图。**【待修复】**普通 DEFAULT 尚未完成基于 `alphaVisibleBounds` 的 optical normalization；此前“不再推导几何”的结论已被最新 1080P 真机截图否定，本轮只记录，不改实现。
- **动态状态**：天气、日历、时钟在动态开关开启时由原版 ActiveIcon 链显示，分组不再把它们误判为缺少静态候选。此前针对 ActiveIcon 的比例、alpha 阈值、阴影参数和 PNG 尺寸试验均已撤回；当前没有把动态天气/日历视觉一致性标记为完成。
- **验证与风险**：`build.bat`、Java 宿主编译、Smali 回编译、签名和 `git diff --check` 通过。OPPO PDCM00 未连接，仍需在默认/改进版/图标包切换、拨号/联系人、12/20 宫格与三个主题下，由用户核对桌面、列表及单应用页的实际一致性。

#### 上滑搜索纳入已固定的小程序快捷方式（构建完成，真机待验证）

- **根因**：搜索页只查询 `ACTION_MAIN + CATEGORY_LAUNCHER` 的 Activity；固定小程序快捷方式的身份是 `packageName + shortcutId + user`，既不会出现在该查询中，也不能由普通 `startMainActivity()` 正确启动。
- **修复**：仅通过 `LauncherApps.ShortcutQuery.FLAG_MATCH_PINNED` 读取当前 Launcher 已固定的快捷方式，不混入未固定的动态/推荐快捷方式。`SearchEntry` 为快捷方式保留独立 `shortcutId` 和用户身份，搜索历史不再与来源应用 Activity 冲突；点击结果使用 `LauncherApps.startShortcut()`。若快捷方式位于已锁页面，仍先经过现有密码确认，再交给已有 `ShortcutLaunchActivity` 处理。
- **验证与风险**：`build.bat` 成功，最终 APK 仍为 `com.smartisanos.launcher v1.5.5 / 30`；当前无 ADB 设备，未完成“应用请求固定 → 桌面出现 → 上滑搜索名称 → 点击启动”的主用户、分身用户及删除后消失验证。

### 2026-07-27

#### 解锁触发链恢复至 v1.5.3，保留高刷新率真实时间推进（构建完成，真机待验证）

- **基线**：Git 标签 `V1.5.3` 指向 `25d20c4c`（`release v1.5.3`，Manifest 为 `v1.5.3 / 28`），不是按日期推断。
- **根因**：后续 `UnlockAnimationCoordinator` 在广播入口提前过滤/认领事件，并以独立 generation、播放权和动画回调决定是否允许播放；该状态与后续 Activity、页面或场景检查不同步时会留下已认领但未播放的周期，破坏 v1.5.3 已验证的原始触发顺序。
- **恢复**：`ia.1.smali` 删除 Coordinator 广播前置过滤并恢复 v1.5.3 的 `noteOriginalUnlockBroadcast()`；`animations/c/b.smali` 删除 generation 获取和 `onAnimationStarted/onAnimationFinished` 拦截，保留原版场景 cleanup 及低频 timing diagnostics；`ja.1.smali` 删除进程启动 reset；`MaintainedLauncherSettingsHost` 恢复 v1.5.3 的熄屏确认、1200/1500ms 时间戳去重与原始双事件 fallback；删除 `UnlockAnimationCoordinator.java`。
- **保留**：`Eb.smali` 没有回退固定每帧 20 的原版行为，仍以 `uptimeMillis` 帧间隔折算统一 SMEngine delta；`mStartTime==0` 时只建立时间基准，恢复后不会把长暂停直接推进到 Timeline。
- **验证**：`build.bat` 成功，maintained 设置资源、Smali、classes2.dex、二进制 Manifest 注入、zipalign 均完成；`apksigner` v1/v2/v3 均验证通过。`PZXO8PHMONGYVSOZ` 未出现在 ADB 列表，未安装、未产生锁屏日志或截图，未将任何锁屏次数、动画时长、刷新率兼容性或 ROM 兼容性标为已验证。
- **风险**：待在 OPPO PDCM00 Android 12/ColorOS 上完成正常及快速锁屏解锁；60/90/120/144Hz、主题/文件夹、进程回收和其他 ROM 均待真机验证。

### 2026-07-24

#### 图标性能优化阶段 8.2 同进程最终长稳复测与数据修正（真机验证）

- **测试环境**：OPPO PDCM00 (Android 12, API 31, 序号 `PZXO8PHMONGYVSOZ`)
- **同进程 30 分钟桌面静置与交互复测 (PID=11704 保持 100% 一致)**：
  - 00min: PID 11704 | PSS 149.6 MB | Native 42.4 MB | Graphics 59.7 MB | Act 1 | Views 6 (冷启动稳定后)
  - 10min: PID 11704 | PSS 199.5 MB | Native 79.0 MB | Graphics 67.2 MB | Act 2 | Views 195 (交互后)
  - 20min: PID 11704 | PSS 202.7 MB | Native 81.5 MB | Graphics 68.0 MB | Act 2 | Views 195 (+3.2 MB)
  - 30min: PID **11704** | PSS **203.2 MB** | Native **81.9 MB** | Graphics **68.0 MB** | Act **2** | Views **195** (+0.5 MB)
  - **同进程判定**：从 00min 至 30min 采样 PID 100% 保持为 `11704`，未发生进程死亡或重启 (`am_proc_died=0`, `lmkd=0`)；内存完全进入 **~203 MB 稳定平台**，无单向递增泄露。
- **同进程 10 轮图标页高压进出与快速滑动测试 (PID=11704)**：
  - 第 1 轮: PSS 250.5 MB | Native 83.3 MB | Graphics 111.9 MB
  - 第 5 轮: PSS 283.0 MB | Native 109.1 MB | Graphics 116.9 MB
  - 第 10 轮: PSS 276.1 MB | Native 100.2 MB | Graphics 119.9 MB
  - 10 轮退出 60s 后: PSS 回落至 **223.1 MB** (Native Heap 回落至 **61.7 MB**)
  - **结论**：高压进出后动态 Session 取消与位图 GC 正常生效，`knownKeys` ($\le 512$) 与 `PackMap` ($\le 2$) 强约束生效，退出 60 秒后 Native Heap 显著回落。
- **进程死亡与异常日志审计**：`am_proc_died` `0` / `lmkd` `0` / FATAL EXCEPTION `0` / ANR `0` / OOM `0`。

#### 图标性能优化与初始化分阶段收敛（阶段 0 至 8 完成，已通过真机 3 轮验证）

- **背景与目标**：原版本中进入“应用图标”设置页时，主线程同步构建大列表、扫描安装包、解析 `appfilter.xml` 并同步加载全部位图，引发明显主线程阻塞；同时无界的 Key Map、PackMap 和无 Session 状态导致退出页面后任务继续运行且内存高企。
- **核心修复与架构**：
  1. **模型构建移出主线程**（阶段 2）：应用图标页框架立即显示，后台异步构建分类与模型快照；通过 `RequestSession` 与 `bindGeneration` 过滤旧页面回调，避免列表跳变与错位。
  2. **目标尺寸采样解码**（阶段 3）：按 View 逻辑尺寸与屏幕 `density` 采样解码缓存位图，替换原始大图直接加载。
  3. **Session 动态取消**（阶段 4）：页面退出或重新进入时立即 invalidate 旧 Session，优先清理 `P2_IDLE` 等非可见任务，设置页面队列上限 96，防止旧无消费者任务积压。
  4. **静态缓存有界化**（阶段 5）：`knownKeys` 绑定为 `LruCache<String, IconRenderKey>(512)`；`sPackMapCache` 限制最大 2 项，并强保当前已选中图标包不被淘汰；XML 解析移出 `synchronized` 锁。
  5. **包变化缓存失效**（阶段 6）：在 `SmartisanInstallManager` 收到 `PACKAGE_*` 广播时触发 `IconPackManager.invalidateIconPackList()`，确保图标包包名列表在应用安装/卸载/覆盖更新后准确刷新。
  6. **冷启动任务审计与分阶段**（阶段 7）：首帧前仅保留 `C0_CRITICAL` 核心启动；图标解码按 `P0_VISIBLE` (当前页) -> `P1_ADJACENT` (相邻页) -> `P2_IDLE` 调度；非关键任务在 `LAUNCH_FIRST_FRAME` 握手后延迟执行。
- **真机验证 (OPPO PDCM00, Android 12)**：
  - **首帧渲染时间**：冷启动 `LAUNCH_FIRST_FRAME` 稳定在 **162–171 ms** (中位数 168 ms)。
  - **内存表现**：冷启动 60s TOTAL PSS **~176.2 MB** (Native Heap ~38.3 MB)；进入图标页多次滑动并退出 60s PSS 稳定在 **~228.5 MB**。
  - **稳定性**：30 分钟桌面静置与 10 轮图标页压力测试无 Crash/ANR，主线程违规为 0。

#### 版本号升级与文档同步（v1.5.5 / versionCode 30）

- **变更**：使用 `tools/set_launcher_version.py v1.5.5 30` 自动同步三大版本控制入口：`launcher/AndroidManifest.xml`、`launcher/original/AndroidManifest.xml` 与 `launcher/tools/maintained_settings_res/res/values/strings.xml`。
- **文档同步**：同步更新 `README.md`（含 v1.5.5 更新摘要）、`docs/architecture/APK_STRUCTURE.md` 及 `docs/development/LAUNCHER_STARTUP_BASELINE.md` 中的版本号。
- **验证**：运行 `python tools/set_launcher_version.py v1.5.5 30` 执行通过，二进制 Manifest 校验成功。

#### 下滑系统面板与上滑搜索状态残留修复（构建完成，已增加低频日志）

- **根因**：用户在桌面下滑打开通知栏/控制中心时，`FlingUpGesture.b(MotionEvent)` 在向下滑动阶段将静态标志 `sk` 设为 `true`。当系统面板在 `ACTION_MOVE` 阶段取得焦点后，Launcher 收不到后续 `ACTION_UP`/`ACTION_CANCEL`，跳过了 `FlingUpGesture.c()` 中的 `ew()` 清理，导致 `sk=true` 遗留至下一次手势；下一次上滑时 `!sk = false` 拦截了上滑搜索，直到该次上滑结束才由 `ew()` 清除状态，造成“必须第二次上滑才能打开搜索”的现象。
- **修复**：
  1. 在 `launcher/smali/com/smartisanos/launcher/a/a/a.smali` 中增加 `resetAfterSystemPanelGestureMoveConsumed()` 和 `resetAfterSystemPanelGesture()`，仅调用内部私有 `ew()`，不增加重复状态字段。
  2. 在 `launcher/smali/com/smartisanos/smengine/v.1.smali` 的 `ACTION_MOVE` 系统面板已消费分支（`isSystemPanelGestureConsumed() == true` 且 `onOriginalTargetCancelled()` 执行后）立即调用 `resetAfterSystemPanelGestureMoveConsumed()`。
  3. 保留 `ACTION_UP`/`ACTION_CANCEL` 消费分支中的 `resetAfterSystemPanelGesture()` 作为兜底。
  4. 在 `MaintainedLauncherSettingsHost.java` 中增加低频日志 `logFlingUpReset`，输出 `FLING_UP_STATE_RESET reason=SYSTEM_PANEL_MOVE_CONSUMED/SYSTEM_PANEL_UP_CANCEL beforeRk=... beforeSk=... beforeTk=... afterRk=false afterSk=false afterTk=false`。
- **验证**：执行 `build.bat` 构建成功，签名及二进制 Manifest 检查通过。

#### 自定义上传图标保存目录与列表刷新修复（构建完成）

- **根因**：
  1. 路径不一致：`saveCustomIcon()` 将相册裁切图片保存至 `getFilesDir()/custom_icons/`，而 `RedirectIconDB.readCustomBytes()` 从 `getFilesDir()/redirect_icons/` 读取，导致数据源永远返回 `null`。
  2. 列表视图未刷新：`AppIconAdapter.getView()` 与 `rebuildRows()` 直接使用 initial load 时创建的 `RedirectIconInfo` 对象，`info.drawableName` 留在 `"auto"`，未能读取数据库中已更新的 `MODE_CUSTOM` 状态与位图。
  3. 缓存空值：`iconDrawableForChoice` 在 `TYPE_CUSTOM` 缺失 `iconData` 时返回了 `plusIcon(resources)`，导致 `IconPreviewRepository` 线程池将其作为合法位图写入 LRU 缓存，阻碍了新图片的渲染。
- **修复**：
  1. `saveCustomIcon()` 写入目录统一为 `redirect_icons/`，并在 `RedirectIconDB.customFile()` 中增加遗留 `custom_icons/` 自动迁移。
  2. `AppIconAdapter.getView()` 与 `rebuildRows()` 在绑定和分组时实时调用 `RedirectIconDB.getRedirectIconInfo(...)` 获取最新记录。
  3. `iconDrawableForChoice` 缺失 `iconData` 时返回 `null`，避免将 `+` 号位图写入 `IconPreviewRepository`；`iconSourceId` 针对 `MODE_CUSTOM` 增加数据长度后缀 `custom_<length>` 驱动缓存 Key 更新。
- **验证**：`build.bat` 打包与签名成功，`aapt2` 校验通过。

### 2026-07-23

#### 应用图标全局来源统一与真实预览（构建完成，真机未完成）

- **问题**：旧实现的 `launcher_improved_icon_enabled` 与 `prefs_key_selected_icon_pack` 相互独立，改进版和图标包可同时开启；桌面、列表右侧候选图标与设置选择不能保证使用同一来源，全局切换还会遍历并重写部分 `RedirectIconDB` 记录，存在覆盖单应用设置的风险。
- **修改**：新增 `IconSourceManager` 管理互斥 `default`、`improved`、`pack:<package>` 状态，并在首次读取迁移旧配置；保存新状态时同步旧字段，保证原版 Smali/旧 Java 兼容。应用图标页顶部由三行改为“图标样式 + 桌面图标大小”，保留原有两行背景和箭头，不修改既有“已重绘/未重绘”列表、行布局或单应用候选页。
- **解析与预览**：桌面 `iconOverrideDrawable`、列表右侧图标和全局选择弹窗共用“手动 MODE_CUSTOM / MODE_RESOURCE / MODE_PACK / MODE_ORIGINAL 优先；MODE_AUTO/无记录跟随全局；任何来源缺图回退 PackageManager 原图”的解析。弹窗只维护临时选择，取消不写偏好；图标包扫描及 appfilter 预载在后台执行，预览优先跳过已有手动覆盖的普通应用。应用时不修改 `RedirectIconDB`，只清理/预载图标包缓存、刷新现有适配器并走已有逐包 `update_icon` 链。
- **弹窗视觉收口**：来源列表不使用任何 Android/Material 单选控件；每项为 54dp 锤子式整行，右侧仅复用 `preview_picture_selected` 小对号。首/中/末行分别复用 maintained 圆角背景；分割线改为每行内部的底部细线并左右缩进 24dp，避免穿出右侧圆角。列表独立限高 280dp，标题、预览和底部按钮固定；对号使用 22dp `CENTER_INSIDE`、右侧 24dp 间距且行容器不裁剪子视图。
- **验证**：基线和修改后均执行 `build.bat`；最终 launcher、maintained 设置资源、Java helper/classes2.dex、二进制 Manifest 注入、zipalign 与 v1/v2/v3 签名均成功。真机覆盖安装仍需先解决设备返回的 `Failure [-200]`，因此未把临时预览一致性、列表滚动位置、单应用覆盖和重启矩阵标记为已验收。

#### Android 8+ PIN 快捷方式的分身用户、原版数据库动作与图标框修复（构建完成，真机未完成）

- **删除分流与去重图标修复（2026-07-23）**：`na.run()` 的普通 Android `UninstallCompat.requestUninstall(packageName)` 快速路径此前只判断单项删除和包名，错误拦截了 `itemType=1` 的 `QuickLaunchItem`，所以拖入微信/支付宝小程序会打开来源应用卸载器。现先检查 `itemType`：只有普通应用（`0`）仍走系统卸载；快捷方式回到原版确认与 `ia -> DatabaseUpdater.Action.naa -> F.b()` 链。快捷方式确认文案改为“删除快捷方式 / 是否删除“名称”？ / 删除”，普通应用既有文案和系统卸载入口未改。
- **原版删除与 unpin**：`ia` 原有 `naa`（`EVENT_UNINSTALL_SHORTCUT`）分发完成后才调用桥接日志/unpin helper；helper 从当前项目 Intent 读取 package、shortcut ID、user serial，以 `UserManager.getUserForSerialNumber()` 恢复真实 profile（仅 item userId 与进程主用户相同才允许主用户 fallback），读取 pinned 列表、仅移除当前 ID，再写回剩余 IDs。unpin 失败只记录 `SHORTCUT_UNPIN_FAILED`，不回滚已完成的本地删除，也不会触发来源应用卸载。
- **【已废弃】快捷方式图标的来源已装饰、`final_icon` 直通与跳过原版合成方案。**
- **验证**：`build.bat` 成功完成 Smali、Java compatibility host、二进制 Manifest 注入、zipalign 和签名；`apksigner verify --verbose` 确认 v1/v2/v3。vivo X21A 在线，但安全的 `adb install -r build\\launcher-signed.apk` 仍返回 `Failure [-200]`；未卸载、未清数据，故未获得删除、unpin、主/分身隔离、普通应用卸载回归及微信/支付宝单框的真机证据。

- **确认页生命周期崩溃修复（2026-07-23）**：真机日志已确认崩溃发生在 `PIN_SHORTCUT_DIALOG_SHOWN` 之后、任何 `accept()`、用户解析、图标合成和数据库调用之前：`PinShortcutConfirmActivity did not call finish() prior to onResume() completing`。根因是 `tools/patch_pin_shortcut_manifest.py` 只把原版 no-display `PinShortcutActivity` 改名，却保留其不可显示窗口属性；新的确认页需要承载 `AlertDialog`。补丁脚本现在读取/覆盖已有 `android:theme`，或在缺失时追加 typed reference `0x01/0x01030010`（`@android:style/Theme.Translucent.NoTitleBar`）。未修改 `ShortcutCompatBridge`、`DatabaseUpdater`、`QuickLaunchItem`、分身身份/图标框或 `ShortcutLaunchActivity`。
- **验证**：重新执行 `build.bat` 成功；`aapt2 dump xmltree --file AndroidManifest.xml build\\launcher-signed.apk` 的确认页记录为 `theme=@0x01030010`、`exported=true`、`excludeFromRecents=true`、`launchMode=1 (singleTop)`，并包含 `CONFIRM_PIN_SHORTCUT` 与 `DEFAULT`。完整 dump 存放于 `build\\final_manifest_dump.txt`。真机覆盖安装仍受 `Failure [-200]` 阻塞，尚不能验证是否继续输出 `SHORTCUT_ACTION_RESOLVED`，更不能据此宣称快捷方式写入成功。

- **根因**：兼容桥接层此前将原版 `DatabaseUpdater.Action.maa` 当作枚举名传给 `Enum.valueOf()`；而 `maa` 实际为静态字段，指向 `EVENT_INSTALL_OR_UPDATE_SHORTCUT`，因此确认页 `accept()` 即使成功，桌面数据库派发仍会失败。原版 `d.j.c()` 转换快捷方式时还会把 `ItemInfo.userId` 重置为 `-1`，会破坏分身身份；原图为空时也没有完整复用原版快捷方式图标框路径。
- **修复**：`ShortcutCompatBridge` 反射读取 `maa` 字段并校验其枚举名/ordinal 后，继续调用原版 `F.b(action, null, items)`，不重建 Model、PageView 或数据库写入。转换完成后从 `ShortcutInfo.getUserHandle()` 读取 identifier，写回 `ItemInfo.userId`，并记录 `SHORTCUT_USER_RESOLVED`。原版 `QuickLaunchItem` 插入前去重原本只按 Intent，因此仅在该快捷方式入口将查询收紧为 `intent + user`，并保持普通应用的通用去重不变；数据库保存链同时持久化 `user` 与 `shortcutId`。`ShortcutLaunchActivity` 保持以 `UserManager.getUserForSerialNumber(userSerial)` 恢复句柄，分身记录不允许退回 `Process.myUserHandle()`。
- **【已废弃】快捷方式图标归一化后由桥接层提前合成的方案。**
- **验证**：`build.bat` 已通过 apktool、Java 宿主编译、二进制 Manifest 注入及 v1/v2/v3 签名；`aapt2 dump badging` 确认产物为 `com.smartisanos.launcher`、versionCode `29`、versionName `v1.5.4`，最终 Manifest 含导出的 `PinShortcutConfirmActivity`、`CONFIRM_PIN_SHORTCUT` 过滤器和非导出的 `ShortcutLaunchActivity`。`git diff --check` 通过。
- **真机状态与风险**：ADB 可见 vivo X21A、主用户 `0` 和分身用户 `999`，且已安装 `com.tencent.mm`；对新 `build\\launcher-signed.apk` 执行覆盖安装被系统拒绝，返回 `Failure [-200]`。因此未在新代码上验证主/分身同一小程序可同时存在、各自启动、重启保留、独立删除/更新，也未验证支付宝图标框。不得把本项宣布为真机完成。

#### 设置页系统返回统一为左上角返回（构建完成，真机待验收）

- 本工作树先恢复到 GitHub `origin/main` 的 `36f934d3`，随后仅按顺序合并 `84d97605`（小程序快捷方式恢复）和 `8116c122`（设置图标高清修复）；未带入此前资源同步、资源补齐、主题或宫格试验。
- `ThemeChooserActivity.onBackPressed()` 统一调用 `MaintainedLauncherSettingsHost` 当前页面已注册的原有返回回调。系统返回键、三键/全面屏边缘返回和标题左上角因此进入同一路径；首页没有回调时才交给原 Activity 退出。
- 各二、三级 maintained 设置画面在显示时注册其既有父页面回调；不创建新的 Activity、页面栈、资源动画或 AndroidX 返回分发器。`onDestroy()` 清理当前 Activity 所属回调，避免旧页面持有。
- 验证：导航源文件与已审计实现逐字节一致；`build.bat` 通过 apktool、二进制 Manifest 注入、Host Java / `classes2.dex`、zipalign 和签名。未宣称真机返回行为已完成，需在成功安装后覆盖标题、系统返回键和边缘返回三种入口。

### 2026-07-21

#### 桌面设置“桌面设置”齿轮按钮高清物理纹理合成修复（构建与签名验证完成）

- **根因**：桌面静止时显示的不是 `setting_button/` 路径下的原始资源，而是 `Ec.wz()` 在运行时合成并注册的两个内存纹理 `***settingbuttonup***` 和 `***settingbuttondown***`。而原版的 `Ec.wz()` 使用了背景 PNG 原始尺寸生成这两个合成纹理，然后由 SMEngine 放大显示，从而绕过了普通图标的物理 RasterSpec，造成明显的缩放发虚和模糊。
- **修复**：
  1. 在 `IconRasterDiagnostics.java` 中增加高清合成方法 `composeSettingButtonTexture`，结合当前 `LayoutProperty.setting_button` 逻辑大小与普通图标的物理 `rasterScale` 计算出目标物理纹理像素大小。
  2. 实现单次采样物理纹理缩放绘制，并保留原版按下状态下 60 度齿轮旋转和内阴影的多图层顺序。
  3. 修改 `Ec.smali`，在 `Ec.wz()` 中先动态读取当前页面模式 and 逻辑 `setting_button` 大小，然后分别调用 `composeSettingButtonTexture` 生成抬起和按下状态的位图并注册，若 helper 失败则通过 `:cond_fallback` 安全回退到原版旧低清合成流程。
- **文件**：
  - `launcher/tools/java/com/smartisanos/launcher/theme/IconRasterDiagnostics.java`
  - `launcher/smali/com/smartisanos/launcher/view/Ec.smali`
- **验证**：执行 `build.bat` 成功重新编译 Java 兼容层及 smali 代码，重新打包并使用 v1/v2/v3 成功签名。通过 `aapt2 dump badging` 验证包信息为 `com.smartisanos.launcher` (versionCode=29, versionName=v1.5.4) 且完全无安装和解析异常。
- **风险**：主题资源异常或反射/冷启动状态不可达时，会捕获异常并返回 null，安全走 fallback 回退机制，不影响主 Launcher 的正常启动。

### 2026-07-19

#### 【已废弃】桌面设置、动态天气和日历接入普通图标 RasterSpec（尺寸与阴影视觉方案错误）

### 2026-07-18

#### 应用图标预览框收紧与关闭改进版图标时保持分组（真机验证完成）

- **根因**：共用轻描边背景曾直接铺满原版 `icon_frame_background` 的 `86dp × 96dp` 透明画布，导致可见框接近整行高度；关闭“改进版图标”又会让 `AppIconAdapter` 同步重算所有应用的已重绘/未重绘分组，列表在批量回退时发生可见卡顿。
- **修复**：应用图标页继续保留原 `86dp × 96dp` 点击 Host 和 `48dp` 图标上限，只将独立可见框从 `76dp` 收紧为 `72dp`；`24dp` 红勾继续独立覆盖在右上，随框同步改为左 `60dp`、上 `7.666667dp`。关闭全局改进版图标时，Adapter 仅刷新行内选择状态，使红勾回到左侧原图，不调用 `rebuildRows()`，因此现有“已重绘/未重绘”顺序与分组保持不变；单应用选择及开启全局改进版仍保留原有重分组逻辑。
- **验证**：真机 1080×2304 覆盖安装后，“应用图标”页两侧框不再上下相连，红勾在右侧框外缘；打开“替换图标”页确认候选宫格尺寸与排列未变。构建、v1/v2/v3 签名、APK badging 和 ADB 覆盖安装通过；关闭开关后红勾逐行回到左侧原图，首个“已重绘”标题以及 58同城、Edge、Keep、OPPO 商城等现有顺序保持不变。

#### 设置页首个分组标题的垂直基准统一（真机验证完成）

- **根因**：隐私密码、应用分身已通过 maintained 宿主的页面级 `18dp` 顶部留白定位首个分组标题；原版 `theme_preview_gridview` 的列表容器没有这层留白，导致“本地主题”相对标题栏上移一档。标题字号、颜色和左边距相同，但页面级锚点不同。
- **修复**：只在主题页列表容器补 `18dp` 顶部留白，复用隐私密码/应用分身已有的页面级节奏；没有改动分组标题自身的 `15sp`、`#80000000`、30dp 左边距、11dp/1dp 内部上下 padding，也没有移动应用图标、替换图标的前置内容或卡片内部布局。
- **验证**：真机 1080×2304 上“本地主题”最终 bounds 为 `y=303..400`，与应用分身和隐私密码的首个分组标题 `y=303..400` 一致；下一内容容器均从 `y=400` 接续。`build.bat`、v1/v2/v3 签名、ADB 覆盖安装和主题页冷启动通过，crash buffer 无 Launcher 崩溃。

#### 应用图标与替换图标预览框共用视觉背景（最终结构已由同日后续记录覆盖）

- **根因**：替换图标候选框在 `AppIconAdapter.choiceIconBackground()` 中单独创建透明填充、`5dp` 圆角与 `1px #18000000` 描边；应用图标列表仍使用旧的 `icon_frame_background.png`，因此两处框的视觉材质不一致。
- **修复**：新增无尺寸、无 padding、无 inset 的 `icon_preview_frame_visual.xml`：透明底、5dp 圆角、1px `#12000000` 轻描边。候选页按资源名取得并 `mutate()` 独立实例。应用图标页最终将该视觉背景放进独立的小框容器；外层仍保持原 `86dp × 96dp` 点击区域，红勾为独立 `24dp` 覆盖层，具体尺寸以后续记录为准。
- **验证**：候选宫格与应用图标页使用相同的轻描边视觉资源；最终真机尺寸和红勾锚点见同日“应用图标预览框收紧与关闭改进版图标时保持分组”记录。

#### 跨品牌、跨 Android 版本启动兼容性审计（核心启动修复完成；Android 12 模拟器验证完成；多 ROM 真机回归待验证）

- **已确认高风险根因**：`ja` 的 Activity 观察器字段与注册入口、`ActivityManagerSmt` 描述符和 `ha` 观察器类仍直接引用隐藏 `IActivityObserver`；即使注册体已变为 no-op，Android 16 仍可能在类加载/校验时解析该类型。启动窗口辅助类还会直接访问 `WindowManager.LayoutParams.privateFlags`、`ServiceManager/IWindowManager`、`WindowManagerGlobal`，并在 `J.a(Context)` 直接调用普通 ROM 不存在的 `SmtPCUtils.getExtDisplayId()`。另一个仅用于锁屏下滚动提示的 `ActivityManagerNative/getRunningTasks()` 分支会在现代 ROM 被隐藏 API 或任务可见性限制命中。
- **修复与降级**：Activity 观察器启动入口改为明确记录 `SMARTISAN_API_UNAVAILABLE` 后跳过；`ha` 与 `ActivityManagerSmt` 不再使用隐藏观察器类型。窗口初始化只保留公开 `Window` API；全局动画缩放回退原始默认值 `1.0f`，外接屏回退主显示器，导航栏旧反射回退既有无导航栏布局。锁屏位置查询改为反射探测并捕获 `Throwable`，服务为空时返回安全结果；不再让隐藏 API 缺失中断 Launcher。
- **可选模块保护**：`SmartisanInstallManager.ensure()` 的 HandlerThread/Handler 建立失败会清理半初始化状态、记录 `OPTIONAL_MODULE_DISABLED` 并返回；`LauncherApps` 服务为 null 或回调注册失败时只保留 Manifest 包广播路径，不再把“已注册”永久置位。天气、动态日历、主题、在线图标、通知角标和下载动画的原有独立降级路径未被扩大或重写。
- **启动诊断**：新增 `StartupCompatibilityLogger`，在 Application、安装桥、代理和 Activity 主链记录 `LAUNCHER_APP_CREATE_BEGIN`、`INSTALL_MANAGER_INIT_BEGIN`、`APPLICATION_PROXY_CREATE_BEGIN`、`APPLICATION_PROXY_ONCREATE_BEGIN`、`LAUNCHER_ACTIVITY_CREATE_BEGIN`、`MODEL_INIT_BEGIN`、`DATABASE_INIT_BEGIN`、`MAIN_VIEW_INIT_BEGIN`、`LAUNCHER_STARTUP_COMPLETE`。可选模块失败会输出 Android 版本、厂商、型号、线程、异常类型、完整堆栈与 fallback 状态；未在 Application 外层包裹全局 `catch(Throwable)`。
- **安装前置修复**：模拟器首次覆盖安装暴露二进制 Manifest 中 `PinShortcutConfirmActivity.launchMode` 被错误写为字符串 `singleTop`，导致 `INSTALL_PARSE_FAILED_UNEXPECTED_EXCEPTION: For input string: "singleTop"`。修正 Manifest 补丁后以枚举整数 `1` 写入，最终 AXML 已显示 `launchMode=1 (Raw: "singleTop")`，覆盖安装成功；这是安装解析问题，不是 Launcher Java/native 启动崩溃。
- **验证**：`build.bat` 成功完成 Smali、Java compatibility host、Dex 合并、zipalign 和签名；`apksigner verify --verbose` 确认 v1/v2/v3 均为 true。Android 12 / API 31 Google 模拟器已成功覆盖安装、以标准 HOME Intent 冷启动，并记录到 `LAUNCHER_STARTUP_COMPLETE`、Surface ready、first frame 与 model ready；未出现 `AndroidRuntime`、`VerifyError`、`NoClassDefFoundError`、`NoSuchMethodError`、`IllegalAccessError` 或 Launcher 进程崩溃。SettingsProvider 的 `WRITE_SECURE_SETTINGS` 拒绝仅来自受限全局设置写入，进程继续完成首帧；其设置页写入兼容性仍列入多 ROM回归，不将其误判为启动失败。
- **未改与风险**：未修改数据库结构、宫格迁移、主题/冷重载、解锁业务、动画资源或原版 UI。`SecurityControlView`、Smartisan Provider 与其他非启动期隐藏接口仍保留在受功能触发路径，需按相应功能在实体机继续审计；Android 6、8、11、13、15、16 以及小米、OPPO、vivo、三星、摩托罗拉、华为、一加和原生 Android 的首次安装、拒绝权限、断网、后台回收、重启、语言/字体和无锤子组件场景均待真机验证。

#### 普通 Android Home 键兼容与原版回首页复用（核心实现完成；构建与签名验证完成；真机回归待验证）

- **根因**：原版 `Launcher.onNewIntent()` 只接受锤子私有 `android.intent.extra.FROM_HOME_KEY`；普通 Android 的 HOME 交付通常只有 `ACTION_MAIN + CATEGORY_HOME`，因此不会进入原版 `J.a(Intent)`。不能让所有新 Intent 都进入该方法，因为冷重载、快捷方式和其他内部 Intent 也会复用 `onNewIntent()`。
- **Home 判断与前后台区分**：新增 `LauncherHomeCompat`。它保留私有 extra 判断，并补充标准 `ACTION_MAIN + CATEGORY_HOME`；通过 `onResume()`、`onPause()`、`onStop()` 与 `onWindowFocusChanged()` 共同维护生命周期连续性。部分普通 Android 会在前台再次按 Home 时先调用 `onPause()`、再投递 `onNewIntent()`；此时只要 Activity 尚未 `onStop()`，仍判为前台 Home。真正离开到其他应用后已 Stop 的返回只记录 `HOME_FROM_BACKGROUND` 并保留当前普通桌面页；前台第二次 Home 才记录 `HOME_WHILE_LAUNCHER_FOREGROUND` 并调用 `J.a(Intent)`。
- **原版回首页链路**：未新增分页实现、未写死页面索引，也未触碰数据库。前台标准 HOME 仅清除平台投递的 `FLAG_ACTIVITY_RESET_TASK_IF_NEEDED` 位，以匹配原版 `J.a(Intent)` 的 Smartisan 路由判定；普通 Android 在交付前会先清空原版 `J.Oa/mHasFocus`，因此仅在已由生命周期确认的前台第二次 Home 中恢复该原版门控。`e/s.ia(context)` 的锤子 keyguard/task 私有查询对普通 Android 回退为“有效前台 context”，随后继续由原版关闭弹窗/等待页、动画检查、负一屏复位、500ms 防抖和 `createScrollToLeftEvent` 决定首个正常桌面页。锤子私有 Home 路径保持原 Intent flags。
- **日志**：新增 `HOME_INTENT_RECEIVED`、`HOME_SOURCE_SMARTISAN`、`HOME_SOURCE_STANDARD_ANDROID`、`HOME_FROM_BACKGROUND`、`HOME_WHILE_LAUNCHER_FOREGROUND`、`HOME_RETURN_TO_FIRST_PAGE`、`HOME_ALREADY_ON_FIRST_PAGE` 与 `HOME_PAGE_VIEW_NOT_READY`；PageView/MainView 未就绪仅记录并跳过。
- **未改**：`Launcher.onBackPressed()` 仍为空；不使用 finish、killProcess、冷重载、固定延迟或页面数据库写入。
- **验证**：2026-07-18 `build.bat` 成功，`apksigner verify --verbose` 确认 v1/v2/v3。当前 ADB 无连接设备，尚未执行第三页打开应用后 Home、连续第二次 Home、负一屏、文件夹、编辑模式、搜索页、快速连按以及多 ROM 真机测试。

#### 微信、支付宝小程序“添加到桌面”双协议兼容（代码实现完成；构建与签名验证完成；微信/支付宝真机回归待用户验证）

- **根因与边界**：原版现代 `CONFIRM_PIN_SHORTCUT` 入口由 `PinShortcutActivity` 转交 `d/e` 悬浮 Dialog；该 Dialog 调用 `window.setType(0x7f6)`（`TYPE_APPLICATION_OVERLAY`），且原 Activity 随后立即 `finish()`。普通 Android 非特权 Launcher 不能可靠显示该窗口，异常被旧链吞掉时不会执行 `PinItemRequest.accept()` 或原版数据库安装动作。旧 `INSTALL_SHORTCUT` / `UNINSTALL_SHORTCUT` 仍由 `LauncherReceiver -> L -> DatabaseUpdater` 处理，本轮未改动。
- **现代入口**：最终二进制 Manifest 只保留 `PinShortcutConfirmActivity` 作为 exported 的 `CONFIRM_PIN_SHORTCUT` 接收者；其 Activity Window 承载原版资源标题、文案和确定/取消按钮，不依赖悬浮窗权限或 2038。Activity 对每个 `packageName|shortcutId|userSerial` 请求串行确认，取消/返回不 accept，确定时先构造完整项目、再 exactly-once `accept()`，成功后才提交原版 `DatabaseUpdater$Action.maa`。
- **持久化与启动**：现代项目仍使用原版 `QuickLaunchItem`、数据库写入和受影响页面更新链。保存的 Intent 不保存小程序 URL 或参数，只保存 `smartisan.shortcut.package`、`smartisan.shortcut.id`、`smartisan.shortcut.user_serial`，并通过内部 `ShortcutLaunchActivity -> LauncherApps.startShortcut()` 启动。仅明确标记为主用户的无 serial 项允许回退到 `Process.myUserHandle()`；不能把未知 profile 启动到主用户。
- **【已废弃】快捷方式图标 Alpha 裁切、提前合成与 `final_icon` 数据库直通方案。**
- **兼容层限制**：Java compatibility host 的编译 classpath 不可静态引用原始 APK Dex 中的混淆类，因此仅通过已核对的反射入口调用 `d/k -> d/j.c -> QuickLaunchItem`、`e/s.a()` 与 `F.b(DatabaseUpdater$Action.maa, ...)`；没有新增第二套数据库、Model 或页面插入逻辑。
- **验证**：`build.bat` 成功；Java compatibility host 已编译并注入 `classes2.dex`；`apksigner verify --verbose` 确认 v1/v2/v3；最终 APK 二进制 Manifest 确认仅有 `PinShortcutConfirmActivity` 接收 `CONFIRM_PIN_SHORTCUT`，并保留 `LauncherReceiver` 的 `INSTALL_SHORTCUT` / `UNINSTALL_SHORTCUT` 以及内部 `ShortcutLaunchActivity`。当前无 ADB 设备，尚未取得微信、支付宝实际使用 PIN 或 legacy 协议的日志，也未执行添加、取消、重复、删除、主题/在线图标刷新、分身及多用户真机回归。

#### 解锁动画偶发播放两次修复（代码实现完成；构建与签名验证完成；解锁动画 exactly-once 真机回归待用户验证）

- **解锁去重机制重构**：【已废弃】基于握手时间和回调先后的解锁去重。
- **可信结论**：每次真实 `SCREEN_OFF` 创建唯一 `unlockGeneration`。原始 `USER_PRESENT` 与生命周期 fallback 只竞争该 generation 的一次播放权；第一个来源原子设置 `playClaimed`，后续所有来源和重复广播均拒绝。动画结束不清除 `playClaimed`，只有下一次真实 `SCREEN_OFF` 才创建新 generation。
- **修复**：
  - **解锁生成标志 (unlockGeneration)**：新增 `UnlockAnimationCoordinator` 管理解锁状态机（`IDLE`, `SCREEN_OFF_ARMED`, `PREPARED`, `PLAY_CLAIMED`, `PLAYING`, `FINISHED`）与 `unlockGeneration`。
  - **真实熄屏检测与原版准备**：`SCREEN_OFF` 和已确认设备非交互的 `onPause` 只创建一次 generation。生命周期先成功创建 generation 时，仅补发一次原版 `action_keyguard_on` 以准备原始解锁场景；后续重复 `SCREEN_OFF` 不再递增 generation 或再次准备。
  - **唯一播放派发**：普通 `USER_PRESENT` 成功领取播放权后直接进入原版接收器。仅当 ROM 没有向 HOME 进程派发该广播时，生命周期会在“设备可交互且 Keyguard 已解锁”后领取同一播放权，并补发一条带内部一次性许可的原版 `USER_PRESENT`；不再补发 `action_keyguard_on`，不使用 1.2s / 1.5s 时间窗或 120ms 延迟。
  - **首尾回调第二保护**：`b.smali` 的 `onStart` 取得当前 generation 并要求协调器确认“已有播放权且尚未开始”；无播放权、陈旧 generation 或第二次回调会记录 `UNLOCK_DUPLICATE_START_BLOCKED` 后直接返回。`onComplete` 只完成同 generation 的首次结束记录。
  - **诊断与跳过原因**：日志包括 `UNLOCK_GENERATION_CREATED`、`UNLOCK_PLAY_REQUESTED`、`UNLOCK_PLAY_CLAIMED`、`UNLOCK_ORIGINAL_PLAY_DISPATCHED`、`UNLOCK_ANIMATION_START`、`UNLOCK_ANIMATION_FINISH`、`UNLOCK_DUPLICATE_START_BLOCKED` 和 `UNLOCK_RESUME_NOT_A_REAL_UNLOCK`；后者保留 `THEME_TRANSITION`、`FOLDER_OPEN`、未实际解锁或已领取等原因。
  - **验证**：本轮 `build.bat` 成功，`apksigner verify --verbose` 确认 v1/v2/v3 签名通过。当前没有可用 ADB 设备，因此尚未把 exactly-once 标为真机完成；需覆盖普通锁屏解锁、快速重复锁屏解锁、息屏恢复、通知栏解锁、主题切换中解锁、文件夹展开时解锁及多 ROM。

#### 下滑系统面板与桌面交互手势仲裁重构（核心实现完成；构建与签名验证完成；真机竞速回归待验证）

- 【已废弃】“只有空白区域才能触发下滑系统面板”
- 【已废弃】“命中带ItemInfo的Cell后永久拒绝系统面板”
- 【已废弃】“Cell或控制节点在DOWN阶段直接取得整次手势所有权”
- 可信结论：系统面板手势允许从空白区域、应用图标和关闭状态的文件夹图标开始。最终所有权根据手势识别结果决定：向下移动先达到阈值（150px）时，系统面板接管；长按或拖动先确认时，系统面板不再接管；普通轻点仍正常启动应用。
- 修复：
  - **状态机与同步锁**：`SystemPanelCompat` 重构状态为 `IDLE` (0), `TRACKING` (1), `OTHER_GESTURE_OWNED` (2), `SYSTEM_PANEL_OWNED` (3), `FINISHED` (4)。所有状态变更及手势事件方法均使用 `synchronized` 串行同步，防止跨线程竞争导致状态混乱。
  - **其他手势占有原因追踪 (`ownerReason`)**：引入 `sOwnerReason` 标记，用于区分系统面板被拒绝的具体行为，包含 `"LONG_PRESS"`、`"DRAG"`、`"PAGE_SCROLL"`、`"UP_SWIPE"`、`"MULTI_TOUCH"`、`"FOLDER_OPEN"`、`"EDIT_MODE"`、`"DOCK"`。
  - **已实现的微小抖动容错与阻断检查**：
    - `ACTION_DOWN` 时若触控在 Dock 区域内，则直接转移至 `OTHER_GESTURE_OWNED(DOCK)` 并拒绝系统面板。
    - 仅当横向位移超出 touch slop (24px) 且 `abs(dx) > abs(dy)` 时判定为翻页，转移至 `OTHER_GESTURE_OWNED(PAGE_SCROLL)` 并拒绝。
    - 仅当向上滑动超出 150px 且 `abs(dy) > abs(dx)` 时判定为上滑搜索，转移至 `OTHER_GESTURE_OWNED(UP_SWIPE)` 并拒绝。
  - **真实占有入口修正**：`b.1.smali::j(SceneNode)` 只作为原版长按监听分发，仍可能拒绝或转入拖动，因此不再在其入口抢占系统面板。普通拖动仅在 `Ha.c()` 的原版 `i(...)` 成功分支后标记 `DRAG`；编辑态拖动仅在 `Ha.d()` 建立原版拖动状态、调用 `m(8, true)` 后标记 `DRAG`。
  - **事件完整性修正**：系统面板成功后由 `smengine/v.1.smali` 只调用一次原版 `InputManager.rh()` 投递 CANCEL，并在原始 `UP/CANCEL` 输入投递前持续消费后续事件；反射展开失败不会标记系统面板已接管、不会取消原点击。
  - **交互目标白名单与分类**：
    - `onSmEngineInteractiveTarget()` 会保存原始目标；当前只对页码、编辑控件和非 Cell/FolderIcon 的控制节点立即拒绝。普通应用与关闭状态文件夹图标保持 `TRACKING`，打开文件夹、编辑和拖动则由原版活动状态检查拒绝。
    - 关闭状态的文件夹图标与普通应用图标一致，在 `TRACKING` 期间允许继续进行下拉竞争。
  - **原子接管与容错回退**：
    - 当位移达到 150px 触发下拉时，仅在反射调用系统状态栏服务成功后，才原子地将状态设为 `SYSTEM_PANEL_OWNED`；取消事件只由 SMEngine 原始入口发送。
    - 若反射调用全部失败，则不吞掉点击、不设为 `SYSTEM_PANEL_OWNED`，且不发送 CANCEL，保持状态为 `FINISHED` 以防误吞原触摸流程。
  - **事件完整性（代码静态检查）**：系统面板反射成功后才进入 `SYSTEM_PANEL_OWNED`；反射全部失败时不调用 `InputManager.rh()`、不设置该状态，外层继续走原点击链。成功状态会维持到 `ACTION_UP/CANCEL` 的外层 consumed 检查后才重置；`SystemPanelCompat` 已移除独立反射取消，消除与 `smengine/v.1` 的双重 `rh()` 风险。
- **待真机验证**：轻微反向抖动、慢速下滑与长按/拖动竞速、反射全部失败、CANCEL 是否真正清除点击/长按状态，以及 Dock 继续禁止下滑；不扩大 Dock 适用范围。
- **构建验证**：2026-07-18 `build.bat` 成功重新编译 Smali 并注入 Java compatibility host；`apksigner verify --verbose` 确认 v1/v2/v3 有效。当前 ADB 无连接设备，未安装也未标记为真机完成。

### 2026-07-17

#### SMEngine 全局动画时间源与暂停恢复基准（核心实现完成；完整真机回归待验证）

- 审计结论：桌面解锁、文件夹开关、翻页、主题、Cell 回弹和动态图标均由 `Eb.update() -> Ra.T(engineDelta)` 的原版 SMEngine 时间线推进；未发现当前项目新增的按屏幕刷新率分支、固定 frame++ 或独立 progress/scale/alpha 帧推进。原版源码中其余 `20.0f`、`0.02f` 常量分别属于资源参数、物理参数或时间轴定义，不能机械删除；已确认粒子唯一明确入口继续使用 `engineDelta / 1000f`，没有固定 `0.02f` 推进。
- 时间基准：保留真实 `uptimeMillis` delta、`engineDelta = realDelta * 20 / 16.6667` 与 100ms 上限。`Eb.onPause()` 和 `Eb.onResume()` 均清零 `mStartTime`，因此锁屏、后台、Activity/GL 恢复后的首帧必为 0 delta，下一帧才按真实墙钟推进，避免后台间隔或快速恢复吞掉动画开头。
- 未改：所有 unlock XML、文件夹/主题动画 XML、原版 duration、缩放、透明度、插值器、解锁广播、冷重载和任何 Display refresh-rate/品牌分支。
- 静态验证：2026-07-17 apktool 已重新编译全量 Smali，`git diff --check` 无空白错误；当前已签名 APK 的 v1/v2/v3 校验有效。由于无 ADB 设备，60/90/120/144Hz 的解锁、文件夹、翻页、主题、拖动回弹和动态图标墙钟时长尚未实测，不能声称小于 5% 的回归已经完成。

#### 【已废弃】下滑系统面板所有权与 NEW 实时入库链（代码实现完成；构建、签名与二进制 Manifest 验证完成；真机回归待验证）

#### SMEngine 按真实墙钟 delta 推进，修复高刷新率动画加速（代码实现完成；构建、签名与二进制 Manifest 验证完成；真机回归待验证）

- 根因：原版 `view/Eb.update()` 虽读取 `SystemClock.uptimeMillis()`，却在写回 `mStartTime` 后丢弃 `now - previousStartTime`，每次 `GL/vsync -> Eb.update() -> Ra.T(float)` 均传入固定 `fx=20.0f`。120Hz 因而每秒调用约为 60Hz 的两倍，解锁 XML、主题和翻页等同一 SMEngine 时间线会以约两倍逻辑速度推进。
- 对照：`clean_launcher_raw` 与当前 APK 的 `Eb.update()` 均为相同固定步长；维护参考提交 `1e6ab7265dfe1b48855283d4be98b2f00e4f9546` 的 `MainView.update()` / `World.runOneFrame()` 是同一混淆映射。本轮仅按其最小差异移植到当前 `Eb -> Ra` 命名。
- 修复：每帧保留真实 delta，首次帧为 0，后续限制为最大 100ms，随后计算 `engineDelta = realDelta * fx * (1 / 16.6667)`，再调用既有 `Ra.T(engineDelta)`。100ms 上限只防止掉帧、后台恢复或调试停顿使动画跳到结尾；不读取 `Display.getRefreshRate()`，因为该 API 在部分 ROM 可返回默认模式而非实际 GL vsync。
- 粒子：已确认 `Ra.T(float)` 内的 `BU.ea(0.02f)` 是 maintained `updateAllParticleEmitter(0.02f)` 的等价唯一入口，改为 `BU.ea(engineDelta / 1000f)`；没有对无法精确映射的粒子路径猜测修改。
- 诊断：新增 `AnimationTimingDiagnostics`，仅在 SMEngine 实际推进时每秒最多记录一次 `ANIMATION_FRAME_DELTA`（异常 delta 例外），包含真实 / 引擎 delta、`fx`、uptime 和线程；既有 `UnlockAnimationXML` 的 `onStart/onComplete` 仅新增 `UNLOCK_ANIMATION_START/FINISH` 墙钟时长日志，不改变原始回调顺序或解锁业务。
- 验证：`build.bat` 成功完成 Smali、Java `classes2.dex` 注入、zipalign 与签名；独立 `apksigner verify --verbose` 确认 v1/v2/v3 为 true，`zipalign -c -P 16 -v 4` 通过，`aapt2 dump xmltree --file AndroidManifest.xml` 确认最终二进制 Manifest 仍为 `com.smartisanos.launcher` 且 `ReloadTransitionActivity` 保持 `screenOrientation=portrait`。当前 `adb devices` 无连接设备。
- 未改：`unlock9/12/16/20.xml`、原版缩放/颜色/插值、解锁广播触发、`USER_PRESENT` / 生命周期兜底、主题 / 宫格 / 冷重载链路均未修改。待同一小米设备在 60Hz 与 120Hz 各至少三次、并在 OPPO 复测解锁、翻页和主题动画；当前不能将真机结果标记为完成。

#### 桌面上滑搜索与左右下滑系统面板（代码实现完成；构建与二进制 Manifest 验证完成；真机回归待验证）

- 原下滑搜索入口：此前 `Launcher.dispatchTouchEvent(MotionEvent)` 在所有事件已交给 RootView/SMEngine 后，再调用 `MaintainedLauncherSettingsHost.handleLauncherSearchGesture()`；该旁路以向下 `dy` 判定并通过 `ThemeChooserActivity` 的 `launcher_show_search` extra 打开项目内搜索页。现已完整删除这个 Activity 级观察器、其状态字段和下滑方向判断，下滑不会再由这条链路进入搜索。
- 上滑搜索：当前 APK 原本已有 `com.smartisanos.launcher.a.a.a`（source `FlingUpGesture.java`）；`com.smartisanos.smengine.v.1` 在 ACTION_DOWN / MOVE / UP 分别调用其 `a(MotionEvent)`、`b(MotionEvent)`、`c(MotionEvent)`。保留原版单指、500ms、150px、反向移动和横向 0.83 比例限制，并在成功后改为调用现有 `MaintainedLauncherSettingsHost.openLauncherSearchFromSwipeUp()`，仍由既有 `ThemeChooserActivity` / `launcher_show_search` 打开项目内搜索页，不新建或重写搜索页面。
- 设置：原设置行保留原位置和 View ID，标题改为“上滑打开搜索页”，最终 key 为 `swipe_up_search_enabled`、默认 `true`。首次读取新 key 时，若不存在则一次性读取旧 `launcher_search_page_enabled` 并写入新 key；后续手势仅读取新 key。紧邻新增“下滑打开通知栏和控制中心”（`swipe_down_system_panels_enabled`，默认 `true`），两个开关写入现有 launcher settings 存储后立即生效，不冷重载、不杀进程。
- 下滑系统面板：当前源码没有 maintained 的同名 `DragLayer`；实际等价入口仍是原版 `smengine/v.1` 的 ACTION_MOVE。首版错误地只在该 MOVE 读取延迟回写的 `v.LE`，而 `FlingUpGesture.b()` 已先调用 SystemPanelCompat；快速图标下拉会在 Cell touch-down 结果到达前打开 SystemUI，且 `ACTION_UP` 先清除 consumed 标记，随后仍投递原图标 click。现改为真实 Cell touch-down 立即阻断，Cell long-click/拖动同样阻断；候选额外等待 120ms 让 SMEngine 命中状态稳定。单指空白区下拉超过 150px、纵向大于横向才触发；成功后 consumed 状态保留到 `smengine/v.1` 消费同一 ACTION_UP，因此不再启动应用。多指、横向、设置关闭和反射失败继续原桌面触摸链。
- 兼容调用：新增唯一 `SystemPanelCompat`，只通过 `context.getSystemService("statusbar")` 反射。左侧顺序为 `expandNotificationsPanel()` → `expand()`；右侧顺序为 `expandSettingsPanel()` → `expandNotificationsPanel()` → `expand()`。没有无障碍服务、常驻服务、厂商 Intent、Root、Shell、Shizuku 或 ROM 型号判断；所有反射失败均返回原触摸链，不抛出到 Launcher。
- Manifest：文本 Manifest 原已含 `android.permission.EXPAND_STATUS_BAR`；本次未重复修改 AXML。构建后的最终二进制 Manifest 已用 `aapt2 dump xmltree --file AndroidManifest.xml build\\launcher-signed.apk` 确认保留该权限。
- 验证：2026-07-17 已再次执行 `build.bat`，完成 maintained 资源、Smali、Java Compat、classes2.dex、zipalign 和签名；`apksigner verify --verbose` 确认 v1/v2/v3 为 true。当前 `D:\sdk\platform-tools\adb.exe devices` 未发现设备，不能声称真机通过。待在 OPPO/ColorOS、小米/HyperOS、接近 AOSP，以及 Android 11/13+/15+ 上验证左右空白区下滑、图标轻点后下拉、图标长按拖动、Dock、文件夹、编辑模式、横向翻页、多指、负一屏、12/20 宫格和连续快速操作。

#### NEW 标记不再被通知使用权或角标提醒隐藏（代码实现完成；真机回归待验证）

- 根因：原版 `view/a/g.1` 的 `SHOW_MESSAGE_FLAG` 是数字消息角标与新安装 NEW 共用的渲染位。通知使用权未授权时，maintained 设置宿主会按既定权限策略关闭“角标提醒”，并令该全局位为 `false`；这并非原版 NEW 安装判定依赖通知权限，却会把已经正确写入 `ItemInfo.isNewlyInstalled` 的 `newapp.png` 一并隐藏。
- 原版对照：`g.bb()` 继续只在 `isNewlyInstalled=true` 且 `messagesNumber<=0` 时创建原版 `newapp.png`；真实消息数大于零时仍优先显示数字消息角标。安装入库、`newlyInstalled` 数据库字段、首次点击清除 NEW、通知监听服务、通知使用权申请与角标开关持久化均未修改。
- 修复：仅在 `g.i(0x200, visible)` 与 `g.Zm()` 计算共享显示位时，为“新安装且没有数字消息”的原版条件补回可见性。关闭角标提醒、未授权或撤销通知使用权时，普通数字通知角标仍被隐藏；只有原版 NEW 保持显示，且有真实消息数时不会与数字角标叠加。
- 验证：待本次完整构建后，以未授予通知使用权的新装应用验证 NEW 出现；再验证关闭角标提醒、授予/撤销通知使用权、带真实通知数的新装应用优先显示数字角标、首次打开清除 NEW，以及普通数字角标仍受开关控制。当前无 ADB 设备，不将真机结果标记为完成。

#### 跨 ROM 新安装应用即时显示与原版 NEW 标记（代码实现完成；真机回归待验证）

- 根因：原版 `LauncherReceiver` 的 `PACKAGE_ADDED` 直接调用 `Aa.c()`，而移植层 `SmartisanInstallManager` 的动态接收器又独立调用相同入口；两条链在不同 ROM 的 PackageManager 可见性与 Launcher 模型初始化之前竞争。移植层只进行 `0/300/600ms` 三次探测，第三次失败后直接丢弃，正好会遗漏 HyperOS 等延迟暴露 Launcher Activity 的新应用。该兼容路径没有把“真实新安装”语义带入原版入库，因此依赖系统应用分类的应用可能没有原版 NEW。
- 原版对照：`Aa.c(Context, package)` 只负责收集真实 Launcher Activity 后投递 `DatabaseUpdater.Action.aaa`；`data/A.k()` 转入 `A.b(package, matches)`；`A.b()` 创建 `ItemInfo` 并在同一 `a/l.h(ItemInfo)` 入库前写入 `isNewlyInstalled`，`ItemInfo.toContentValues()` 同步写入 `newlyInstalled`。桌面 `view/a/g.1` 读取该原版字段绘制 NEW，首次点击后的原版 `clearFlagNew` 仍把同字段回写为 `0`。本轮未新增自定义 NEW、角标、Cell 刷新或数据库表。
- 修复：现有 `SmartisanInstallManager` 成为唯一协调层。Manifest 接收器在保留主题包和 `PACKAGE_DATA_CLEARED` 原版处理的前提下，将普通 `ADDED/CHANGED/REMOVED/REPLACED` 转交管理器；动态 receiver、`LauncherApps.Callback` 与 `PackageInstaller.SessionCallback.onFinished()` 同样只入同一队列。事件以包名去重并写入 `SharedPreferences`，只有 `J.MESSAGE_COMPLETE` 调用 `onLauncherModelReady()` 后才回放；首次 model-ready 记录安装基线，不扫描或重排已有桌面数据库。
- 就绪与 NEW：回放同时要求 PackageManager 可查询包和 `MAIN/CATEGORY_LAUNCHER` Activity；按 `0/100/250/500/1000/2000/4000ms` 有界重试，约 12 秒仍不可见时记录 `INSTALL_PENDING_RETAINED` 并保留落盘事件，不再永久删除。新安装由 `firstInstallTime == lastUpdateTime` 且晚于基线、并且非 replacing 判定；升级不会标 NEW，卸载会移除待处理标识，卸载后重装可重新满足新安装条件。原始 `A.b()` 仅在创建 ItemInfo 前读取该事件标识，确保 NEW 与原版同一次入库落盘；点击清除逻辑未改。
- 验证：`build.bat` 已完成 apktool 回编译、二进制 Manifest 注入、Java 兼容层编译、`classes2.dex` 合并、zipalign 和签名；`apksigner verify --verbose` 确认 v1/v2/v3 为 true；`aapt2 dump xmltree --file AndroidManifest.xml` 确认最终 APK 的 `LauncherReceiver` 仍包含 `PACKAGE_ADDED/CHANGED/REMOVED/REPLACED` 与 `package` scheme。当前 ADB 无连接设备，未声称 OPPO/HyperOS 即时显示、NEW、升级、卸载重装、冷启动恢复、分身/多用户、连续安装或 Java/native 稳定性已完成真机验证。

#### 动态天气/日历实时节点阴影主题资源解码修复（代码实现完成；最终真机回归待完成）

- 根因：实时 `WeatherView(H)` / `CalendarView(m)` 的阴影源来自 `pb.path()`，该值是相对主题 Asset 路径；原版通过 `xa.getBitmap()` 以当前 `Constants.THEME_PATH` 打开。旧兼容层错误地将该路径交给 `BitmapFactory.decodeFile()`，在通常的主题 Asset 场景中无法得到 Bitmap，导致 shadow-only PNG 和后续纹理无法生成；调整半径、颜色或节点坐标均不会改变真机视觉。
- 修复：`LauncherSettingBridge` 现在反射调用原版 `smengine.s.getBitmap(String)`（即 `xa.getBitmap()`）读取同一主题资源，再只复制该 Bitmap 用于兼容软件阴影生成；只有路径确为本地文件且原版解码不可用时才回退 `decodeFile()`。不修改原版资源、天气/日历动画、阴影参数、`sc[27]` 私有 GL 链、节点尺度或业务开关。
- 缓存与诊断：缓存目录从 `active_icon_shadow_v1` 升级到 `v2`，避免使用旧解码链生成的条目。仅在缓存创建时记录源路径是否为文件、原版解码路径、源尺寸、输出字节数；`H` / `m` 在 `setImageName()` 和 `addChild()` 后记录实际节点父级、layer、renderQueue 和 visible，供下一次真机日志确认纹理加载与节点未被裁剪。
- 验证：2026-07-17 `build.bat` 已成功生成当前 APK；ADB 当前无设备，尚未声称阴影视觉已在普通、浅色、透明主题或 12/20 宫格上确认。真机应检查 `ACTIVE_ICON_SHADOW_SOURCE_DECODED route=theme_asset`、`ACTIVE_ICON_LIVE_SHADOW_BITMAP_CREATED` 与 `ACTIVE_ICON_LIVE_SHADOW_NODE_STATE`，再按截图确认天气、日历与普通图标的外部阴影一致。

#### 【已废弃】空白区域下拉与上滑搜索手势仲裁回归修复（代码实现完成；最终真机回归待完成）

- 日志根因：`SystemPanelCompat` 将所有 `view.a.g` 节点视为有图标的 Cell。真机日志中的 `cell_empty21/22/32` 实际是空白格，但都被记录为 `PULL_DOWN_REJECT_CELL`，所以空白区域无法取得通知栏/控制中心的手势所有权；同一过宽的等待状态也会干扰随后原版上滑搜索判定。
- 修复：仅当 `g.Rj`（原版 `ItemInfo`）非空时才把 Cell 认定为交互所有者；`Rj == null` 的原版空白格保持等待原始 SMEngine dispatch 完成后进入 `EMPTY_SPACE_CANDIDATE`。图标、文件夹、控制节点、长按和拖动仍优先于系统面板；未恢复任何按时间猜测命中的旧逻辑。
- 验证：2026-07-17 已完成 `build.bat`。待真机确认左半屏空白下拉得到 `PULL_DOWN_EMPTY_CELL_IGNORED -> PULL_DOWN_EMPTY_SPACE_CONFIRMED -> STATUS_BAR_EXPAND_NOTIFICATIONS_OK`，右半屏对应 Settings/通知 fallback；图标长按拖动不得触发系统面板，上滑搜索需保持一次手势一次启动。

#### 【已废弃】动态天气/日历实时节点接入原版参数的安全软件阴影（旧解码链无效）

### 2026-07-16

#### 应用图标即时刷新收敛（核心实现完成，基本验证完成；最终回归待完成）

- 根因分离：设置页此前递归遍历 DecorView 的 `refreshIconRowsInCurrentPage()/refreshIconRowsInTree()`，只能更新已经附着的可见行；屏幕外 ListView 行在滑动重新绑定前保留旧状态。桌面侧则存在两个时序问题：全局“改进版图标”无差别对全部 Launcher 包派发 `update_icon`，在线图标在缓存写入时先启动固定 2 秒静默刷新、之后才把 `RedirectIconDB` 置为 `MODE_AUTO`，使原版更新链可能读取旧状态。
- 设置页修复：应用图标页现在以 `WeakReference<AppIconAdapter>` 维护当前页面 Adapter，不保存 Activity 或 ListView 的静态强引用。状态变化调用 `invalidateIconData() -> notifyDataSetChanged()`；每次 `getView()` 均重新读取 `RedirectIconDB` 当前记录，再解析 AUTO/ORIGINAL/RESOURCE/CUSTOM/PACK、图标包与在线内存/磁盘缓存。已删除递归 View 树刷新及其单行变体；自定义、资源、图标包、恢复原图和全局开关统一走 Adapter 刷新。
- 左右预览：列表右侧“改进版候选”与当前选择状态已分离。关闭全局改进版图标时，AUTO 项使用左侧系统原图并将 `icon_frame_selected` 对号显示在左侧；右侧已缓存/内置候选继续保留为可选预览，不退化为加号。CUSTOM/RESOURCE/PACK 的用户明确选择优先级不变。
- 桌面刷新：保留原版 `com.smartisanos.launcher.update_icon -> Aa.c -> Aa.r -> Aa.e -> DatabaseUpdater -> data/v.run -> PageView.y` 唯一链路。对比 `clean_launcher_raw` 后确认 `data/v.run()` 未改，`PageView.y()` 差异仅为既有文件夹位置适配，没有补加 Smali 回调、第二套广播、Cell 遍历或强制冷重载。`applyIconChanges()` 只向真正变更的 package 集合派发一次，不再在派发返回时假定数据库/渲染已完成或额外请求渲染帧。
- 在线与并发：`writeCachedSmartisanIcon()` 现在只写缓存和清除 miss；下载成功后先更新内存缓存、仅在改进版开关仍开启且不存在 CUSTOM/RESOURCE/PACK 覆盖时写入 AUTO，随后将实际变化包加入主线程单飞集合。删除 2 秒静默期；同一 main-loop 周期完成的包合并为一次原版更新。全局开关每次递增 generation，旧后台扫描在写库或派发前发现 generation/目标状态不一致即记录 `IMPROVED_ICON_STALE_RESULT_SKIPPED` 并退出。
- 在线别名回写：部分系统应用下载使用锤子标准图标别名，而该别名不是 Android 实际安装包名；此前下载完成后以该别名执行 `Intent.setPackage()`，查询不到 Activity，因而不会写 AUTO、刷新右侧对号或派发桌面更新。现在下载回写会遍历 Launcher Activity，以“实际包名或其 Smartisan 别名”匹配，再只将命中的真实包名加入 `update_icon`；不会刷新其他应用或重新加载 Launcher。新增 `ONLINE_ICON_AUTO_PROMOTION` 日志记录下载 key 与实际变更包。
- 单应用桌面回写：合并 `update_icon` 时一度遗漏旧单应用路径在派发后的 `O.init(context)`。设置页直接读取 `RedirectIconDB`，所以云服务、小布助手等会先显示右侧对号；已附着的桌面 Cell 却仍按旧的原版运行时配置快照绘制。`applyIconChanges()` 现仅在确有变更包并完成该包的 `Aa.c -> Aa.r -> Aa.e` 派发后恢复 `O.init(context)`；不扫描其他应用、不重载 Launcher、不新增 Cell 遍历。
- 设置页/桌面图标一致性：云服务和小布助手的截图确认，设置详情页已选中锤子图，桌面仍显示系统图。真实根因是旧桌面 `ItemInfo.componentName` 与设置页保存的当前 `ActivityInfo.name` 不一致；桌面精确组件查表失败后不进入受管图标分支。现保持精确组件记录优先；只有该包恰好只有一个 Launcher Activity 时，才回退查询其当前组件记录。多入口应用绝不使用此回退，避免跨入口串图。桌面随后以该实际组件和同一 `SettingsResourceContext` 解析选中项；联系人/拨号既有分流不变。新增 `DESKTOP_ICON_COMPONENT_FALLBACK` 日志记录命中的兼容回退。
- 诊断：新增 `ICON_UPDATE_DISPATCHED`、`ICON_ADAPTER_INVALIDATED`、`IMPROVED_ICON_STALE_RESULT_SKIPPED`，包含 generation、变更包数量和状态；不记录 Bitmap 内容。后续若真机日志确认已到 `PageView.y` 却无下一帧，才可依据原版 GL 线程投递补一次合并渲染请求，本轮没有预先添加。
- 基本验证：`build.bat` 成功，最终 APK v1/v2/v3 签名有效，PDCM00 ADB 覆盖安装并强制启动成功；启动后 logcat 未见新的 Launcher `FATAL EXCEPTION`、`VerifyError` 或 `NoSuchMethodError`。尚未在真机完成设置页屏幕外行、单次开关全量变化、在线下载完成、快速开关 generation、不同图标模式、桌面翻页/文件夹和多 ROM 回归，不能标记为全部完成。

#### 系统视频自动图标改回原版锤子视频图（核心实现完成，基本验证完成；最终回归待完成）

- 真机证据：替换图标页中的“OPPO 视频”已被系统视频类别识别，却显示 `com.android.VideoPlayer.png` 的旧跨 ROM 图；`com.smartisanos.videoplayerproject.png` 虽在在线索引和类别 variants 中存在，但仅作为手动候选，未进入自动映射。
- 修复：将系统视频类别的自动 key 从 `com.android.VideoPlayer` 调整为已有的 `com.smartisanos.videoplayerproject`，并将同一张已有 PNG 作为 maintained 设置资源的离线回退。候选页和桌面先读取该资源，不再依赖首次在线下载或已有缓存；`com.android.VideoPlayer.png` 继续保留为手动可选 variant。OPPO、ColorOS、OnePlus 等系统视频仍通过同一已验证的系统应用分类条件命中，不按手机型号写死包名。
- 验证状态：`build.bat`、v1/v2/v3 签名和 PDCM00 ADB 覆盖安装已通过。此前真机替换图标页只显示旧图，根因为在线图标未预置到 APK，且带点 key 在内置 drawable 的候选过滤中未转换为下划线资源名；现已同时修正。仍需在真机重新打开“OPPO 视频”替换图标页确认锤子视频图显示并选中，不能标记为全部完成。

#### 宫格冷重载旧 token 二次启动（核心修复完成，基本验证完成；最终回归待完成）

- 真机日志证据：连续切换中，`:reload` 正确为当前 token 启动新 Launcher 后，新主进程又先后接收过期 `f4982e48-98a6-417f-a976-bf750ecac703` 的 `grid_migration/20` Intent，再接收当前 token。例如 18:49:58 当前 token `ae2438fa...` 为 12 宫格，但同一新 PID 8159 先记录旧 token、再记录当前 token；此前 20 宫格和透明主题切换也重复同一旧 token。该双初始化可与当前 token 的首帧、任务恢复发生竞争，足以解释偶发闪退和不透明过渡页短暂失去覆盖后的系统壁纸闪回。
- 根因：Launcher 是 `singleTask`。旧主进程结束后，部分 ROM 会先用 Launcher 任务保留的旧 base Intent 重建 Activity，再把本次 `startLauncher()` 的 Intent 通过 `onNewIntent()` 送达。此前 `captureLauncherReloadIntent()` 无条件接受任意 token，因而把这次旧 base Intent 误当成新的冷重载。
- 修复：每次 `beginReload()` 在启动过渡页前同步写入唯一的 `expected_launcher_token`；新 Launcher 只接受该 token。与其不匹配的旧 base Intent 记录 `STALE_LAUNCHER_INTENT_IGNORED` 且不重置 reload 状态、不初始化 Loading window；当前 token 在 `FIRST_FRAME_READY` 后清除标记。未改 `N.d()`、`F.i()`、数据库、旧 PID 精确终止、`FIRST_FRAME_READY` 判定或 Loading 视觉链。
- 视觉回归修正：首次实现只忽略旧 token，会使当前 token 经 `onNewIntent()` 到达前，原版 `J.b()` 已创建“正在初始化”Dialog，丢失其 `show()` 前的统一窗口几何准备，导致两个 Loading 位置再次不一致。现将“业务 token 接受”与“初始化 Dialog 窗口准备”分离：旧 token 仍不会设置 `sReloadToken`，但会暂存已持久化的当前期望 token，用它在原版 Dialog 创建前应用同一几何；当前 token 到达时保留已准备状态。
- 基本验证：两次完整 `build.bat`、v1/v2/v3 签名校验与 ADB 覆盖安装均通过；代码审计确认当前 token 的 `onNewIntent()` 仍会照常捕获，旧 token 仍不会重置 reload 状态。未擅自修改真机默认桌面或宫格设置，尚未把本次连续宫格实体机回归标记为完成。
- 最终回归待完成：在 Smartisan 默认桌面连续 12→20→12 至少 10 次，并混合透明主题、图标大小、动态天气/日历切换；每轮必须只出现一个业务 `NEW_LAUNCHER_STARTED`/`FIRST_FRAME_READY` token，旧 token 仅允许出现 `STALE_LAUNCHER_INTENT_IGNORED` 和初始化窗口准备日志，不得再次进入业务初始化、壁纸闪回、失败提示或 Java/native 崩溃；逐帧确认两段 Loading 的位置不再回归。

#### 首次冷启动“正在初始化”真机耗时基线（调查完成，未改业务逻辑）

- 真机：PDCM00，受控 `am force-stop` 后冷启动 `com.smartisanos.launcher/.Launcher`；当前配置为 12 宫格、普通黑色主题、透明主题关闭、动态天气/日历关闭、图标包关闭、角标隐藏。
- 日志：`LAUNCH_ONCREATE_BEGIN=0ms`，`LAUNCH_ORIGINAL_INIT_END=82ms`，`LAUNCH_SURFACE_READY=158ms`，`LAUNCH_FIRST_FRAME=165ms`，`LAUNCH_MODEL_READY/LAUNCH_PAGE_READY=710ms`；系统 `Displayed` 为 `+329ms`。因此“正在初始化”在当前设备约覆盖首帧后 545ms 的原版模型/PageView 完整就绪窗口，不是 `ReloadTransitionActivity`、`FIRST_FRAME_READY`、网络下载或固定延迟造成的等待。
- 结论：阶段 4 的优化目标是旧进程退出、新进程首帧和窗口连续性，不能以提前关闭初始化 Dialog 代替首次桌面模型完成；否则会重新引入桌面未就绪、旧/新 Loading 交接或白/黑帧。后续若某一真实配置超过该基线，必须以同一诊断标记定位是图标包、动态天气/日历、数据库数据量或 ROM 调度，再仅把非首帧必需工作移出模型关键路径。
- 验证状态：已完成本次 ADB 冷启动与日志采样；未修改代码、资源、数据库或冷重载协议。不同宫格、动态图标开启、图标包、复杂桌面数据和其他 ROM 的首次启动耗时仍待专项采样。

#### 冷重载两段 Loading 文案与几何一致性确认（核心实现完成，基本验证完成；最终回归待完成）

- 现象：冷重载首段 `ReloadTransitionActivity` 与新 Launcher 原版初始化 Dialog 的文案归属被写反，真机先显示“正在初始化”、后显示“正在加载桌面”。
- 修复：仅将 `ReloadTransitionActivity` 的过渡文案恢复为“正在加载桌面...”；`J.smali` 中原版 `R.string.initializing` 调用未改，后段继续显示“正在初始化”。未改 `FIRST_FRAME_READY`、token、旧 PID 结束顺序、窗口策略或任一宫格/主题业务逻辑。
- 几何实现：两段分别由 `ReloadTransitionActivity` 与新 Launcher 原版 `SmartisanProgressDialog` 承载，但都通过 `OriginalLoadingContentFactory` 生成同一套原版 `loading_progress`、面板高度、圆角、padding、spinner 尺寸、文字样式和居中参数；两个窗口均在首帧前使用全屏沉浸坐标系，避免 system bar inset 改变中心位置。文案继续分别为“正在加载桌面...”和“正在初始化”。
- 基本验证：已完成源码调用点核对、`build.bat` 完整构建、v1/v2/v3 签名校验及连接真机的 ADB 覆盖安装；本次真机反馈确认两段 Loading 的大小和位置已一致。
- 最终回归待完成：仍需在连续宫格切换、图标大小、动态天气/日历及透明主题开关中逐帧确认，没有状态栏/导航栏闪现、上下位移、系统壁纸、黑白帧或“桌面重新载入失败”。

#### 普通主题被透明覆盖状态误导进入冷重载（核心修复完成，基本验证待完成；最终回归待完成）

- 日志证据：用户在普通主题操作中，`ThemeChooserActivity` 于 13:56:13 和 13:56:18 被 `ReloadTransitionActivity` 顶替，随后 `com.smartisanos.launcher:reload` 启动并结束旧主进程；这不是原版 `J.onResume()` 主题动画链。源码审计确认 `beginThemeReload()` 唯一调用点是 `applyTransparentThemeSetting()`。
- 根因：`applyTheme()` 对任何非透明主题先读取 `launcher_grid_theme`。当该透明覆盖状态仍为 `1` 时，旧分支把用户选择的普通主题错误改写为“关闭透明主题”，直接调用 `applyTransparentThemeSetting(false, true)`，因而触发黑色冷重载 Loading。
- 修复：非 `smartisan_theme_trans` 的选择现在无条件清除透明覆盖、壁纸模糊运行状态并继续原版 `ChangeThemeHandler` / `ThemeItemActivity` 等价的 100ms 返回 HOME 时序；不再因为旧覆盖状态调用 `beginThemeReload()`。透明主题的显式开启入口保持原有冷重载范围，未改宫格、图标大小、动态天气/日历、数据库或 `J` 的原版桌面动画。
- 验证状态：`build.bat` 已成功完成，最终 `build/launcher-signed.apk` 于 14:04 生成；`apksigner verify --verbose --print-certs` 确认 v1/v2/v3 签名有效。当前 ADB 无连接设备，尚未声称真机普通主题/毛玻璃主题切换、透明→普通切换的逐帧结果；需确认普通主题全程没有 `ReloadTransitionActivity`/黑色 Loading，且没有主题页闪回、壁纸闪回或新增 Java/native 崩溃。

#### 普通主题切换回归原版主题动画时序（核心实现完成，基本验证待完成；最终回归待完成）

- 原版证据：`clean_launcher/.../ThemeItemActivity` 成功执行 `X.ja()`、`RequireChangeFrom.SETTING`、`O.a()` 和 `ja.l(false)` 后，调用其 `Q` Handler 的 `sendEmptyMessageDelayed(1, 100ms)`；Handler 在约 100ms 后截取过渡画面、finish 当前主题详情 Activity 并启动 HOME。原版没有在此路径创建全屏黑色 `loading_progress` 或 `SmartisanProgressDialog`。
- 修复：maintained `ThemeChooserActivity` 的主题详情虽然不是独立 `ThemeItemActivity`，但普通/毛玻璃主题提交后现保持同一原版 100ms 时序：继续停留当前详情页，随后提交过渡截图并无动画返回 Launcher。此前新增的黑色 Decor Loading 遮罩和其生命周期转发已全部移除；透明主题、阶段 4 冷重载、宫格、图标大小、动态天气/日历、角标和主题数据库均未改。
- 桌面动画：返回 Launcher 后仍由原版 `J.onResume()` 读取已有的 `ChangeThemeHandler.RequireChangeFrom.SETTING` / `a.r.sj` 并执行 `J.a(theme, theme_changing)` 的主题切换事件；maintained 宿主不直接调用 `a.r.a(Message)` 或 `a.r.b(Message)`，也没有重新实现主题动画。
- 验证状态：`build.bat` 已成功完成 maintained 资源构建、apktool 回编译、Java 宿主编译、dex 合并、zipalign 和签名；最终 `build/launcher-signed.apk` 的 v1/v2/v3 签名均有效，版本保持 `v1.5.4 (29)`。当前无连接 ADB 设备，未声称逐帧、普通主题/毛玻璃主题来回切换、返回主题页、锁屏后切换或新主题下载完成后的真机结果；必须确认点击设定后不再出现全屏黑色 Loading、当前主题页短暂保留、随后直接进入原版桌面主题动画。

#### 角标提醒与横扫清除角标的通知使用权流程（核心实现完成，基本验证待完成；最终回归待完成）

- 语义确认：原版键 `launcher_hide_badge=true` 的真实含义是“隐藏角标”，所以“角标提醒”UI 采用 `checked = !launcher_hide_badge`；开启写入 `false`，关闭写入 `true`。横扫功能继续使用独立正向键 `launcher_badge_swipe_clean`，两个功能没有互相自动开启或关闭。
- 授权流程：两个关闭状态的开关准备开启时先调用既有 `BadgeBridge.hasNotificationAccess()`；未授权不修改 UI 或持久化设置，而是复用设置页锤子风格确认弹窗，用户确认后由既有 `BadgeBridge.openNotificationAccessSettings()` 打开 `ACTION_NOTIFICATION_LISTENER_SETTINGS`。没有新增通知权限、`POST_NOTIFICATIONS`、`requestPermissions()` 或第二套通知服务。
- 返回与撤销：pending 目标仅以 `badge_reminder` / `badge_swipe_clean` 写入 `launcher_settings`，可跨设置 Activity 重建恢复。`ThemeChooserActivity.onResume()` 回读真实通知监听授权：授权后只持久化并开启本次目标；未授权返回则保持关闭；每次进入强迫症页面或 settings resume 检测到授权被撤销时，将两个依赖键修正为关闭。开启角标提醒后复用 `BadgeBridge.replay()`，横扫开关不会清空现有角标；全程未调用阶段 4 冷重载、`N.d()`、`F.i()` 或数据库迁移。
- 文案与日志：`obsession_hide_badge` 资源 ID 保持不变，中文文案改为“角标提醒”，未使用的 Native fallback 同步该显示名。新增请求、已授权、弹窗、跳转、返回授予/拒绝、撤销、重复拦截、开关落盘及 replay 日志，不包含通知正文或标题。
- 验证状态：`build.bat` 成功；最终 APK 的 v1/v2/v3 签名均有效，`aapt2 dump xmltree` 确认 `SmartisanBadgeListenerService` 和 `android.permission.BIND_NOTIFICATION_LISTENER_SERVICE` 仍在最终二进制 Manifest。当前 ADB 无连接设备，系统设置跳转、授权后自动开启、取消/拒绝、撤销同步、角标 replay、快速重复点击和 Activity 重建均待用户真机验证，不能标记为全部完成。

#### 动态天气/日历联合开关定位授权前置（核心实现完成，基本验证待完成；最终回归待完成）

- 根因：`setting_dynamic_weather` 的联合开关此前直接写入 `launcher_dynamic_weather_calendar_enabled=true` 并立即请求 `ACTIVE_ICON_SETTINGS_CHANGE` 冷重载；虽然最终 APK 已声明 `ACCESS_COARSE_LOCATION`，该入口没有调用运行时 `requestPermissions()`，因此新 Launcher 启动后天气定位仍无授权。
- 修复：保留 WeatherBridge 已验证的粗略定位策略，不申请精确或后台定位。首次关闭→开启先由 `ThemeChooserActivity` 请求 `ACCESS_COARSE_LOCATION`；授权回调才执行主 `launcher_settings` 的同步 `commit()`、回读确认和 `LauncherColdReloadCoordinator.beginActiveIconReload()`。拒绝时开关保持关闭、不写入 `true`、不生成 token、不发送旧进程 `update_icon`；永久拒绝复用现有锤子风格确认弹窗，引导至系统应用详情设置。关闭不请求权限，直接持久化后进入同一冷重载。
- 回调与并发：设置 Activity 新增最小 `onRequestPermissionsResult()` 转发；静态 pending 标记会拦截授权弹窗未返回时的重复点击。日志覆盖 `DYNAMIC_ICON_ENABLE_REQUEST`、`DYNAMIC_ICON_PERMISSION_REQUESTED`、`DYNAMIC_ICON_PERMISSION_RESULT`、`DYNAMIC_ICON_CONFIG_COMMITTED`、`DYNAMIC_ICON_RELOAD_REQUESTED` 与永久拒绝分支，且不记录坐标。
- 验证状态：代码级检查确认权限使用点与 `WeatherBridge` 均为 `ACCESS_COARSE_LOCATION`；`build.bat` 已成功，`apksigner verify --verbose` 通过 v1/v2/v3，`aapt2 dump xmltree` 确认最终二进制 Manifest 包含粗略定位权限。当前 ADB 无连接设备，系统授权弹窗、拒绝/永久拒绝、授权后冷重载、关闭开关及连续操作仍待真机验证，不能标记为全部完成。

#### 动态天气/日历联合冷重载与过渡页竖屏统一（核心实现完成，基本验证待设备恢复；最终回归待完成）

- 当前代码与原版定位：设置页 `setting_dynamic_weather` 只绑定 `launcher_dynamic_weather_calendar_enabled`；旧路径在写入后调用 `refreshDynamicIconMode()`，向仍存活的旧 Launcher 发送原版 `com.smartisanos.launcher.update_icon`。原版 `LauncherReceiver` 确实消费该广播，但它不是当前冷重载的可靠窗口交接路径。
- 修复：写入后先从权威 prefs 回读确认值，再调用 `LauncherColdReloadCoordinator.beginActiveIconReload(oldEnabled, newEnabled)`。该方法只复用既有 `ReloadTransitionActivity`、原版 `loading_progress`、`reloadToken`、旧 PID 精确终止、新 Launcher token 启动和稳定的 `FIRST_FRAME_READY` 握手；原因固定为 `ACTIVE_ICON_SETTINGS_CHANGE`。未改首帧协议、SMEngine、数据库、`N.d()`、`F.i()`、主题队列或 ActiveIcon 业务实现。无法启动过渡页时保留已落盘设置并提示手动重试，不回退为旧进程 `update_icon`。
- 方向：`Launcher` 的最终 Manifest 已是 `screenOrientation=1`，即桌面不支持横屏。此前 `ReloadTransitionActivity` 缺少方向属性，系统可以按触发瞬间 display configuration 创建横屏 cover。现文本 Manifest 和二进制 AXML 注入脚本均声明 `screenOrientation=portrait`；`ReloadTransitionActivity.onCreate()` 在 Window/content/Loading 创建前调用 `setRequestedOrientation(SCREEN_ORIENTATION_PORTRAIT)` 作为 ROM 兜底。没有使用 `locked`、`sensor`、`behind` 或 `configChanges` 规避方向重建。
- 验证：`build.bat` 成功；`apksigner verify --verbose` 确认 v1/v2/v3 签名有效；`aapt2 dump xmltree` 确认最终 APK 的 `ReloadTransitionActivity` 为 `screenOrientation=1 (portrait)`。ADB 在覆盖安装前显示无连接设备，故本轮没有声称设备安装、动态开关、横放或逐帧验证通过。用户提供的 `build/launcher_log.txt` 已被回退删除，无法用不存在的日志判定之前“桌面重新载入失败”的具体栈；本轮刻意未恢复此前扩大有效桌面帧握手的改动。
- 最终回归待完成：真机执行天气/日历关闭↔开启、连续十次、12/20 宫格、图标大小和横放/自动旋转/横屏应用返回，确认 `ACTIVE_ICON_SETTINGS_CHANGE -> TRANSITION_FIRST_FRAME -> OLD_MAIN_PROCESS_EXIT_CONFIRMED -> NEW_LAUNCHER_STARTED -> FIRST_FRAME_READY -> TRANSITION_FINISHED`，全程竖屏且无失败提示、壁纸、黑白帧或第二套 Loading。

### 2026-07-15

#### 图标大小变更复用冷重载过渡（核心修复完成，基本验证完成；最终回归待完成）

- 原链路与根因：`MaintainedLauncherSettingsHost.showIconSizeDialog()` 的确认按钮写入 `launcher_icon_size` 后调用 `restartLauncherForIconSizeChange()`。旧实现先显示设置页内的 Loading，再通过 requestCode `1002` 安排 `AlarmManager` 350ms HOME、结束设置任务并直接 `killProcess(Process.myPid())`；旧 Launcher 消失到延迟 HOME 的新首帧之间没有不透明窗口，因此会闪回系统壁纸。
- 配置：权威读取顺序仍是 `launcher_settings` → `com.smartisanos.launcher_prefs` → 系统 Settings fallback。现在先对 `launcher_settings` 执行同步 `commit()`，失败不请求重载；成功后再镜像私有 prefs 和系统兼容值。没有修改配置 key、数据库、图标映射、在线图标缓存或用户自定义图标。
- 重载：新增 `LauncherColdReloadCoordinator.beginIconSizeReload()`，原因固定为 `ICON_SIZE_CHANGE`。它复用 `ReloadTransitionActivity`、`ReloadProtocol`、`reloadToken`、旧主 PID 精确终止、原版 `loading_progress`、首个原版 LoadingUI 抑制、`FIRST_FRAME_READY` 和失败/手动重试；没有新建 Activity、遮罩、Loading 或重启工具。`ReloadTransitionActivity` 首帧后才调用旧 PID 结束，确认 PID 已退出后才启动携带 token 的新 Launcher；过渡页只在真实 GL 首帧 token 匹配后无动画关闭。
- 新进程：`Constants.applyLauncherIconSize()` 继续按原有 `LauncherSettingBridge.readIconSizePercent()` 读取值并在 `initPoints()` 前应用尺寸；本轮只在该真实读取点增加 `ICON_SIZE_CONFIG_READ` 诊断，没有局部重建 PageView/Cell 或清除不相关缓存。
- 日志：图标大小链路现在记录 `ICON_SIZE_CHANGE_REQUESTED`、旧/新值、`ICON_SIZE_PERSISTED`、`RELOAD_TRANSITION_REQUESTED`、`TRANSITION_FIRST_FRAME`、`OLD_LAUNCHER_PID_TERMINATED`、`NEW_LAUNCHER_STARTED`、`ICON_SIZE_CONFIG_READ`、`FIRST_FRAME_READY` 和 `TRANSITION_FINISHED`。图标大小重载日志附带 token、oldPid、newPid、oldSize、newSize 和 reason；同值确认只记录 `ICON_SIZE_UNCHANGED_SKIP`，不生成 token、不结束进程。
- 基本验证：完整构建、v1/v2/v3 签名与 `emulator-5556` 覆盖安装通过。真实 UI 操作完成 100%→150% 与 150%→50%：日志确认 `TRANSITION_FIRST_FRAME -> OLD_LAUNCHER_PID_TERMINATED -> ICON_SIZE_CONFIG_READ -> FIRST_FRAME_READY -> TRANSITION_FINISHED`；同值 50%→50% 仅记录 skip，PID 保持不变。日志未见新 `FATAL EXCEPTION`、native fatal、`VerifyError` 或 `NoSuchMethodError`。
- 最终回归待完成：当前仅完成模拟器基本链路验证，不能把静态截图当作实体机逐帧验收。仍需真机录制小→中、中→大、大→小和连续十次，覆盖 12/20 宫格、文件夹、动态天气/日历、在线/自定义图标、锁屏解锁、重启保持及不同 ROM；逐帧确认无壁纸、状态栏/底栏、黑白帧、第二套 Loading、旧尺寸闪现或布局异常。

#### Dock 板块页码圆点等比缩放修复（核心修复完成，基本验证完成；最终回归待完成）

- 实现定位：Dock 页码不是 Android `Canvas`/`Drawable` 控件。`com.smartisanos.launcher.view.V` 从 `LayoutProperty.dot_width/dot_height` 构造 `com.smartisanos.launcher.view.Z`；`Z` 用这两个值创建 SMEngine 网格并缩放原版 `assets/Textures/1080p/dot_fix.png`、`dot_mask.png`、`dot_move.png`。12 宫格和 20 宫格均复用此链路。
- 根因：当前项目新增的 `LayoutPropertyAdapter.factorFor()` 先按字段名分支，导致 `dot_width` 走 `scaleX`、`dot_height` 走 `scaleY`。在已采集的 1080×2400 / 420dpi 设备上，运行日志证实 `scaleX=1.0`、`scaleY=1.25`；同一圆点的目标尺寸因此为宽×1.0、高×1.25，形成纵向椭圆。原版 `clean_launcher_raw` 不存在该兼容适配层。
- 修复：仅将 `dot_width` 和 `dot_height` 提前视为一个固定比例单元，统一返回既有 `scale=min(1, scaleX, scaleY)`。该设备上修复前布局比例为 1.0:1.25，修复后为 1.0:1.0；未改 `view.V`、`view.Z`、纹理、点数、点距、横向居中、纵向位置、Dock 高度或翻页状态。
- 资源检查：`point_normal/point_selected` 不是此指示器，未使用或修改。实际三张 SMEngine 纹理画布仍为 24×24；本轮没有重新绘制、替换或缩放其资源。
- 基本验证：`build.bat` 成功；`apksigner verify --verbose` 确认 v1/v2/v3 为 true；`emulator-5556` 覆盖安装并强制冷启动成功，日志无 Launcher `FATAL EXCEPTION`、native fatal 或 linkage 错误。
- 最终回归待完成：当前模拟器只有一个板块，原始 `screencap` 未出现可测的多页页码，不能伪造截图像素宽高。须在至少 2/5 页、12/20 宫格及另一种 density 真机原始截图中实测选中和未选中圆点宽高，并覆盖左右翻页、Launcher/设备重启与显示大小变化。

#### 宫格冷重载唯一可见 LoadingUI（核心实现完成，基本验证完成；最终回归待完成）

- 结构调整：`ReloadTransitionActivity` 不再反射构造或显示 `SmartisanProgressDialog`。它的完全不透明 content root 直接承载 `ProgressBar`，继续引用原版 `loading_progress` 资源，并逐项保留原版 `SmartisanProgressDialog.onCreate()` 的居中高度（屏宽×3/4/5）、横向 gravity、圆角、padding、spinner 尺寸、文字字号和左 margin；因此没有新增或重画加载动画，也没有新的 Dialog window/inset 坐标系。
- 重复 Loading 抑制：新 Launcher 捕获 `reloadToken` 时记录一次性 suppression token；原版 `widget.c.q()` 只在该 tokenized 冷启动的第一次调用返回而不创建 Dialog，`widget.c.show()` 同时安全处理无 Dialog。普通启动和后续原版 LoadingUI 不受影响。结果是宫格冷重载不再出现“过渡 Dialog 消失 → Launcher 初始化 Dialog 再出现”的两套可见链路。
- 系统栏：过渡 Activity 在 `onCreate()`、首个 content layout 与重新获得窗口焦点时都应用纯黑、`FULLSCREEN`、`HIDE_NAVIGATION`、布局扩展和 `IMMERSIVE_STICKY`；其根视图也是纯黑且不透明。Launcher starting window 沿用既有全屏启动主题；本轮未修改二进制 Manifest。
- 基本验证：完整构建、v1/v2/v3 签名、`emulator-5556` 覆盖安装和强制冷启动通过（`TotalTime=1850ms`），日志无 Java/native/linkage 崩溃。
- 最终回归待完成：在实体机以 60fps 逐帧确认确认弹窗后只保留 `ReloadTransitionActivity` 的同一 Loading，未显示第二个“正在初始化”、无状态栏/底部栏、无 LoadingY轴跳动、无壁纸/黑白帧，并连续 12→20→12 至少 10 次验证任务/进程修复不回归。

#### 宫格冷重载 LoadingUI 无窗口位移收口（核心修复完成，基本验证完成；最终回归待完成）

- 根因收敛：项目资源中未检出自定义 `slide`、`translate` 或 `windowAnimationStyle`。此前逐帧中的整体上下位移是多项窗口级因素共同造成：系统默认 Activity/task enter/exit 动画、过渡页在窗口获得焦点后才再次修改 system-ui 所引发的 inset/居中根布局重算，以及旧版独立 `SmartisanProgressDialog` window 与 Launcher 初始化 window 的不同坐标系。它不是 `loading_progress` 自身动画，也不应由固定延迟掩盖。
- 修复：`ReloadTransitionActivity` 和新 Launcher 的启动 Intent 均增加 `FLAG_ACTIVITY_NO_ANIMATION`；启动和结束 Activity 均立即调用 `overridePendingTransition(0, 0)`。过渡页在 `setContentView()` 前即禁用 window animation，并在同一时机完成纯黑背景、全屏、状态栏/导航栏隐藏、沉浸布局、显示缺口策略（Android 9+）和 `decorFitsSystemWindows=false`（Android 11+）。移除 `onWindowFocusChanged()` 中的二次 system-ui 写入，避免 Loading 已可见后因 inset 变化重居中。
- Loading 继续直接挂载在过渡页的 full-screen content root；冷重载场景没有 `SmartisanProgressDialog` 独立 Dialog window，只有原版 `loading_progress` spinner 自身动画。新 Launcher 的 tokenized 初始化 Loading 仍只抑制一次。Launcher starting window 继续使用既有黑色全屏启动主题，未修改二进制 Manifest、数据库结构、原版 `F.i()` 或 token/首帧协议。
- 基本验证：完整构建、v1/v2/v3 签名、`emulator-5556` 覆盖安装和强制冷启动通过（`TotalTime=2233ms`），未发现新增 Java/native/linkage 崩溃。
- 最终回归待完成：必须在反馈设备录制 60fps 以上 12→20→12，逐帧确认第一次出现后的 Loading Y 坐标不变、无 Activity/task 滑入滑出、无状态栏/导航栏、无第二套初始化 Loading、无壁纸/黑白帧；并完成连续 10 次、手势/三键导航和多 ROM 回归。当前环境不能据模拟器冷启动替代该视觉验收。

#### 宫格连续切换闪退根因：任务归属错误与旧进程记录竞争（核心修复完成，基本验证完成；最终回归待完成）

- 根因证据（`build/launcher_log.txt`）：最新三次 token 均记录 `TRANSITION_FIRST_FRAME -> OLD_MAIN_PROCESS_KILL_REQUESTED -> NEW_LAUNCHER_STARTED`，但没有 `FIRST_FRAME_TOKEN_MATCHED`。WindowManager 将 `ReloadTransitionActivity` 放入 task `3405`，其 affinity 为 `smartisanos.task.launcher`，而非 Manifest 声明的 `com.smartisanos.launcher.reload`；随后出现 `clear-task-all`、`wm_finish_activity Launcher,2nd-crash`。同一序列还出现 `ProcessRecord ... is attached to a previous process` 和 `Already have existing proc`，说明新 Launcher 启动早于旧精确终止 PID 完成 ActivityManager 脱离。
- 修复：启动 `ReloadTransitionActivity` 时无条件使用 `FLAG_ACTIVITY_NEW_TASK`，使声明的独立 `:reload` affinity 真正生效。旧主 PID 发出 kill 后不立即猜测性启动新 Launcher，而是在每个 Choreographer 帧检查 `ActivityManager`，仅在旧 PID 已不再存在时发送 HOME Launcher Intent；等待是进程状态条件，不是固定成功延迟。失败/销毁会取消未完成的启动等待。
- 原版与边界：保留 `N.d() -> F.i()`、旧主 PID 精确终止、原版 `widget.c` LoadingUI、`reloadToken` 和 `FIRST_FRAME_READY`；未改数据库、二进制 Manifest 或主题/宫格业务状态，未加入 Alarm、`recreate()` 或固定成功延迟。
- 基本验证：完整构建、v1/v2/v3 签名、`emulator-5556` 覆盖安装和冷启动通过（`TotalTime=1732ms`），无新增 Java/native/linkage 崩溃。
- 最终回归待完成：在该 Oplus 真机连续 12→20→12 至少 10 次，确认每次都有 `OLD_MAIN_PROCESS_EXIT_CONFIRMED -> NEW_LAUNCHER_STARTED -> NEW_LAUNCHER_FIRST_FRAME -> FIRST_FRAME_TOKEN_MATCHED`，且无 `clear-task-all`、`2nd-crash`、旧 ProcessRecord 竞争、壁纸/黑白帧或 LoadingUI 位移；继续覆盖复杂宫格、异常/超时和多 ROM。

#### 宫格冷重载 LoadingUI 逐帧收口（核心修复完成，基本验证完成；最终回归待完成）

- 逐帧素材：`5a5d2c36dd3696dedcee1095c9b11293.mp4`，720×1600、44.74fps、2.72 秒。帧序列确认“正在加载桌面...”和“正在初始化”使用同一原版转圈资源，却先后落在带 status/navigation inset 的过渡窗口与新 Launcher 初始化窗口；过渡页灰黑背景还透出为非纯黑。问题不是重新绘制的动画资源，也不是 `FIRST_FRAME_READY` 成功延迟。
- 修复：新增最小 `LoadingUiWindowCompat`，仅为原版 `widget.c` 展示后的 `SmartisanProgressDialog` 和 `ReloadTransitionActivity` 设置同一纯黑背景、`FULLSCREEN`、`HIDE_NAVIGATION`、布局扩展与 `IMMERSIVE_STICKY`。过渡页首帧即使用该策略，原版 LoadingUI 展示后再应用同一策略；不重绘 `loading_progress`、不手工计算加载控件坐标、不中断原版 `widget.c` 生命周期。
- 结果目标：设置确认后立即为纯黑且没有系统状态栏/底部虚拟键；“正在加载桌面...”结束后，新 Launcher 的“正在初始化”继续使用同一原版控件、同一全屏坐标系，不再上下位移或出现不同底色。
- 基本验证：完整构建、v1/v2/v3 签名、`emulator-5556` 覆盖安装和强制冷启动通过（`TotalTime=1107ms`）；日志无 `FATAL EXCEPTION`、native fatal、`VerifyError` 或 `NoSuchMethodError`。
- 最终回归待完成：在录屏实体机连续执行 12→20→12，逐帧确认首帧即无状态栏/导航栏、两个 Loading 文案位置一致、无系统壁纸/黑白闪帧；同时覆盖手势导航、三键导航与其他 ROM。

#### 宫格连续切换：过渡任务栈与底部导航栏修复（核心修复完成，基本验证完成；最终回归待完成）

- 真机 `build/launcher_log.txt` 未出现 Launcher `FATAL EXCEPTION` 或 native fatal signal；其中旧 `com.smartisanos.launcher` PID 死亡是过渡页首帧后按设计精确结束旧主进程。异常窗口序列显示：新 Launcher 启动后 `ReloadTransitionActivity` 被 `recent-task-trimmed`/`clear-task-all` 提前销毁，未能继续等待 `FIRST_FRAME_READY`，从而可能暴露系统壁纸并让连续切换表现为闪退。
- 修复：`LauncherColdReloadCoordinator` 启动单实例 Launcher 时仅保留 `FLAG_ACTIVITY_NEW_TASK`，删除会跨 ROM 裁剪仍在等待的 `:reload` 任务的 `FLAG_ACTIVITY_CLEAR_TASK`。不改数据库迁移、token 协议、旧 PID 精确终止时机或失败手动重试。
- 视觉衔接：`ReloadTransitionActivity` 调用已有 `MaintainedLauncherSettingsHost.applyLauncherNavigationBarSetting()`，LoadingUI 仍复用原版 `widget.c -> SmartisanProgressDialog`；在原版 Dialog 展示后只把 Launcher 已计算的 system-ui flags、透明状态栏/导航栏同步给 Dialog window，不新绘制加载动画。这样“隐藏桌面虚拟键”开启时，过渡页与原版 LoadingUI 不再由 ROM 补出不同颜色的底部条。
- 基本验证：完整 APK 构建通过；`apksigner verify --verbose` 确认 v1/v2/v3 有效；二进制 Manifest 仍确认 `ReloadTransitionActivity` 为私有 `:reload`、`excludeFromRecents`、独立 affinity；覆盖安装到 `emulator-5556` 后冷启动 `TotalTime=1417ms`，无新增 Launcher Java/native 崩溃。
- 最终回归待完成：在提供日志的实体机连续执行 12→20→12 至少 10 次，录屏逐帧检查 `:reload`/新 Launcher 交接期间无系统壁纸、黑帧、白帧、底部导航栏残留或 LoadingUI 位移；并覆盖复杂宫格数据、失败/超时重试和其他 ROM。

#### 任务合并和状态 + 建议 Commit 顺序（核心实现完成，基本验证完成；最终回归待完成）

- 冷重载过渡页补齐显式 `WAITING_FIRST_FRAME`、`COMPLETED`、`FAILED` 状态：首帧 token 只接受一次；等待超时只显示失败；手动重试重新挂载失败超时并再次等待新 Launcher 真实首帧，避免旧实现重试后无期限停留在过渡页。未改变旧主 PID 精确终止时机，未手工清理正常 cached 的 `:reload` 进程。
- 图标下载、图标包预热、天气和分身已有 pending/单飞状态继续复用；本阶段没有新建全局 Manager、第二套数据库或全局重试队列。
- 建议 Commit 顺序按专项计划审阅；当前工作区包含用户既有改动、跨阶段源码与构建产物，本轮未执行 git add、commit、reset 或清理，待最终回归后按阶段边界拆分。
- 基本验证：完整 APK 构建、v1/v2/v3 签名、`emulator-5556` 覆盖安装和 HOME 启动通过；无新增 Launcher Java `FATAL EXCEPTION` 或 native fatal。冷重载失败重试的实体机中断、超时恢复与连续压力仍待最终验证。

#### 固定延迟审计（核心审计完成，基本验证完成；最终回归待完成）

- 删除的竞态补偿：透明壁纸运行时原先同步 `Eb.lh()` 后又在 160ms 重复刷新；角标可见性在同步节点更新后又在 180ms 重刷；主题运行时 120/360ms 重复初始化/刷新；手动城市写入后 1800ms 再次安排天气刷新。它们均有同一调用中的原版配置、场景或天气调度入口，重复时间不能证明完成。
- 保留分类：`ReloadTransitionActivity` 的 10 秒仅进入失败提示和手动重试，绝不当作首帧成功；安装的 300ms 仅在 `PackageManager` 暂未暴露 Launcher Activity 时最多两次；主题/更新下载 800–1500ms 是 `DownloadManager` 状态轮询；在线图标 2 秒是磁盘写入的安静窗口合并；天气 TTL、Loading 120ms 帧、键盘/预览 UI 延迟均为功能性调度。旧的 Alarm 重启 helper 不在当前阶段链路中，未重新接入。
- 基本验证：完整 APK 构建完成，`apksigner verify --verbose` 确认 v1/v2/v3 有效，已覆盖安装到 `emulator-5556` 并启动 HOME；日志未发现 Launcher 新增 Java `FATAL EXCEPTION` 或 native fatal。透明壁纸、角标、普通主题和手动城市的实体机交互时序仍待最终逐帧/多 ROM 回归。

#### 启动专项阶段 10（核心实现完成，基本验证完成；最终回归待完成）：原版安装卸载事件与分身按需刷新

- 根因：普通安装完成路径会立刻、800ms、2500ms 三次调用原版新增入口；卸载路径只清理下载占位项，没有进入原版 `Aa.D()` 的数据库删除事件。分身恢复/更新保留 350/450/900/2200/2000/8000ms 的多次全量数据库刷新，并且部分图标刷新入口即使没有用户启用分身也会枚举 `LauncherApps.getProfiles()`。
- 当前修复：安装只在 `PackageManager` 已能查询 Launcher Activity 后调用一次原版 `Aa.c(context, package)`；信息暂未可用时最多重试两次，成功立即停止。卸载保留下载占位清理后调用原版 `Aa.D(package)`，并删除该包在线改进图标的内存、文件和 miss 缓存。分身 bootstrap/图标更新先检查本地已启用记录；原版 `EVENT_USER_PACKAGE_ADDED/CHANGED/REMOVED` 之后只请求一次 render，不再以延迟全量 `EVENT_REFRESH` 补偿。
- 原版复用：普通应用继续由 `Aa.c` / `Aa.D` 转换为原版 `DatabaseUpdater` 事件；分身继续使用原版 `EVENT_USER_PACKAGE_*`，没有新建桌面数据库或 profile 模型。
- 基本验证：完整 APK 构建完成，`apksigner verify --verbose` 确认 v1/v2/v3 有效，已覆盖安装到 `emulator-5556` 并启动 HOME；日志未发现 Launcher 新增 Java `FATAL EXCEPTION` 或 native fatal。尚未执行真实 APK 安装、卸载、替换、工作资料/应用分身和角标联动回归，以上保留到最终验证。

#### 启动专项阶段 9（核心实现完成，基本验证完成；最终回归待完成）：图标加载按需初始化与受影响包更新

- 根因：首帧后的统一延后任务无条件调用所选图标包预热；`shouldUseManagedIcon()` 这个应当只读模式元数据的判定也会触发预热。即使所有图标覆盖关闭，旧的一次性 `maybeRefreshLauncherIcons()` 仍可能扫描已安装图标包和解析 `appfilter`。图标包解析完成、在线 PNG 写入缓存和设置资源预热还会发出 `EVENT_REFRESH`，造成与本次图标无关的全量数据库刷新。
- 当前修复：图标包仅在持久化选择已启用时才在首帧后异步预热，普通模式不初始化图标包系统；`shouldUseManagedIcon()` 保持纯元数据快速判断。图标包完成解析后从已加载 `appfilter` 映射提取包名，合并为一次原版 `update_icon` 和一次 render。在线图标缓存写入继续保留 2 秒安静窗口合并，但只更新本批下载完成的包名；设置资源预热不再触发数据库刷新。
- 原版复用：受影响图标仍通过原版 `com.smartisanos.launcher.update_icon -> LauncherReceiver -> Aa.c/Aa.r` 更新，未新增第二套桌面模型或数据库；首帧无覆盖时继续走 `PackageManager.getApplicationIcon()` 原版快速路径。
- 基本验证：完整 APK 构建完成，`apksigner verify --verbose` 确认 v1/v2/v3 有效，已覆盖安装到 `emulator-5556` 并启动 HOME；日志未发现 Launcher 新增 Java `FATAL EXCEPTION` 或 native fatal。尚未执行真实图标包解析、在线下载、单应用覆盖与动态天气/日历混合回归，以上保留到最终验证。

#### 启动专项阶段 5（核心实现完成，基本验证完成；最终回归待完成）：透明主题复用统一冷重载

- 透明主题开启和关闭不再调用旧的 `restartLauncherForColdSceneChange()`，该旧路径会显示独立 Loading、安排 Alarm 并直接结束当前主进程，不符合统一过渡链路。
- 新入口先确认 `com.smartisanos.launcher.theme.trans` 已安装；开启时保存 `transparent_previous_theme`，再 commit `launcher_grid_theme=1`；关闭时先读取并恢复该普通主题、清除透明壁纸模糊配置，再 commit `launcher_grid_theme=0`。`smartisan_theme_trans` 不写入普通 `launcher_theme`，也不进入普通主题消息队列。
- commit 成功后仅调用 `LauncherColdReloadCoordinator.beginThemeReload()`；协调器只传递透明/普通主题语义给 `ReloadTransitionActivity`，不调用 `N.d()`、`F.i()`，不携带宫格迁移状态。新 Launcher 继续从 `LauncherSettingBridge.readTransparentMode()` 读取配置，由现有 `Constants`、`O`、`Eb` 和原版主题资源完成冷启动初始化。
- 基本验证：Java helper 已通过 Android API 36 classpath 编译；完整 APK 已构建，v1/v2/v3 签名验证通过，并已覆盖安装到 `emulator-5556`。HOME 启动回到 Launcher，日志未见新增 Java/native 崩溃。透明开启/关闭交互、资源呈现和 token 链路仍待本阶段继续验证；最终逐帧、多 ROM、压力与异常回归继续集中处理。

#### 启动专项阶段 6（核心实现完成，基本验证完成；最终回归待完成）：普通主题原版消息链收敛

- 原版对照：`a.r` 先由 `X.ja(package:id)` 写入当前主题，再将 `ChangeThemeHandler` 来源设为 `SETTING`、写入原版 `O` 配置；返回 Launcher 后消费一条原版 `MESSAGE_CHANGE_THEME` 完成场景更新。
- 当前修复：普通主题入口不再在原版持久化成功后重复 `storeThemeSelection()`，也不再使用 120 ms 固定延迟补发截图/返回桌面。现在先同步提交一次原版过渡截图并返回 Launcher；只有 `X.ja()` 明确失败时才写入一条 `a.r.sj` fallback pending message。
- 边界：未使用冷重载作为普通主题刷新，不触碰阶段 3 宫格迁移或阶段 4 冷重载协调器；未新增 Alarm、killProcess、Activity.recreate 或 PageView/EGL/SMEngine 局部重建。
- 基本验证：完整 APK 构建、v1/v2/v3 签名、`emulator-5556` 覆盖安装和 HOME 启动均通过，未出现新增 Java/native 崩溃；普通主题 A→B、透明↔普通交替及真实主题资源呈现仍待最终回归。

#### 启动专项阶段 7（核心实现完成，基本验证完成；最终回归待完成）：动态天气和日历原版场景更新

- 原版协议：`LauncherReceiver` 将 `com.smartisanos.launcher.update_icon` 转交 `Aa.c(Intent)`；该方法解析 `extra_packagename`，并进入原版 `Aa.r(String[])` 数据库/Cell 更新链。
- 根因：动态开关原先虽然调用该协议，却先扫描全部 Launcher Activity，再固定等待 600 ms 后调用冷重启，导致不必要的全量查询、进程重生和壁纸过渡。
- 当前修复：直接从原版 `activeicon.H/m.PACKAGE_NAME` 取得天气/日历包名（反射不可用时使用原版默认包名），一次发送 `update_icon`。不扫描全部应用、不调用 `reloadOriginalSettings()`、不重启、不手工操作 ActiveIcon/Cell/Eb 节点。
- 基本验证：完整 APK 构建、v1/v2/v3 签名及 `emulator-5556` 覆盖安装通过；在运行中的 Launcher 上发送包含两个原版包名的 `update_icon` 广播，接收完成且未出现 Java/native 崩溃。天气应用实际数据、日历跨日和开关 UI 回归仍待最终验证。

#### 启动专项阶段 8（核心实现完成，基本验证完成；最终回归待完成）：壁纸单次原版刷新

- 原版调查：`Eb.lh()` 的日志和实现明确为 `TransWallpaper changeWallpaper`，会释放旧透明壁纸节点并建立新的原版壁纸节点；`Eb.Vh()` 则开始 PageView 加载，不能作为壁纸热刷新入口。
- 当前修复：壁纸选择后的复制、解码、高斯图、缩略图、系统壁纸写入和 URI 落盘移入 `LauncherWallpaperSave` 后台线程；主线程只通知原版配置并调用一次 `lh()`，随后一次 render。删除 `Vh/oh/Z` 反射调用以及立即、120ms、420ms 的重复刷新。
- pending 只在 `Eb` 场景暂不可用时保留；运行时刷新成功立即清除。恢复默认壁纸同样移除额外 180ms 补帧。
- 基本验证：完整 APK 构建完成，`apksigner verify --verbose` 确认 v1/v2/v3 有效，已覆盖安装到 `emulator-5556` 并启动 HOME；日志未发现 Launcher 新增 Java `FATAL EXCEPTION` 或 native fatal。尚未在实体机选择真实大图，也未完成透明主题换壁纸、恢复默认壁纸和逐帧壁纸连续性检查，以上保留到最终回归。

#### 启动专项阶段 3 + 阶段 4（进行中）：12/20 宫格迁移与统一重载

- 原版调查：`LauncherPreview` 在原版 Settings 中使用 `content://com.smartisanos.launcher.exportprovider` 配置链；宫格相关检索未找到 `killProcess`、`restartPackage`、`forceStopPackage` 或 Launcher Alarm 重启。原版 Launcher 的 `Launcher.onDestroy()` 只记录日志，`J`/`vc` 可见 EGL 建立和局部节点释放，但未找到按 Activity → EGL → SMEngine → PageView → 静态单例完整、有序且可重入的释放重建链，因此不再尝试同进程 recreate。
- 冷重载协调：新增私有 `:reload` 进程的 `ReloadTransitionActivity`。主进程只在原版数据库迁移完成后生成唯一 token 并启动该 Activity；过渡页完成 OnPreDraw 和下一 Choreographer 帧后，核对旧主 PID，再仅对这个 PID 调用 `Process.killProcess`，随后显式启动新的 Launcher。宫格流程不再写主题 Loading、清理主题 pending 或触碰主题状态。
- 首帧握手：新 Launcher 通过 Intent 接收 token；原版 `vc.onDrawFrame()` 在 `Eb.update()` 后上报 GL 帧，再由 Decor OnPreDraw 和下一 Choreographer 帧发送包内显式 `ACTION_FIRST_FRAME_READY`。过渡页只接受同 token 的信号后结束；10 秒仅显示失败和一次手动重试，不把超时当成功。
- 过渡视觉：过渡窗口使用完全不透明背景，Loading 动画复用原版 `com.smartisanos.launcher.widget.c -> SmartisanProgressDialog -> loading_progress`，未自绘进度图。新 Launcher 使用不透明原有启动主题。
- 最新模拟器验证：12→20 和 20→12 均出现 `TRANSITION_FIRST_FRAME -> OLD_MAIN_PROCESS_KILL_REQUESTED -> NEW_LAUNCHER_FIRST_FRAME -> FIRST_FRAME_TOKEN_MATCHED -> TRANSITION_FINISHED`，token 一致，无 `FATAL EXCEPTION` 或 native fatal signal；截图确认过渡页为原版锤子 LoadingUI，最终宫格正确。`finishAndRemoveTask()` 后 `:reload` 仍可能被 Android 短暂保留为缓存进程，未主动 kill 该进程，因此阶段 4 不完成。

- 原版对照：设置 UI 使用外部 12/20 单元数；原版数据库只接受 `Constants.getPageModeFromMode()` 得到的内部页模式。迁移必须在 `DatabaseHandler.mWorker` 中依次执行 `N.d(context,newPageMode)` 和 `F.i(oldPageMode,newPageMode)`，PageView 不得由设置页手工重排。
- 持久化修复：设置确认后先同步 commit `com.smartisanos.launcher_prefs/prefs_key_launcher_mode=12|20`；commit 失败则停止迁移。成功后才尽力镜像 Settings.Global，因此主存储不再依赖系统写权限。页模式优先反射调用原版 `Constants.getPageModeFromMode()`，只在反射不可用时保留已验证的 12→12、20→9 fallback。
- 设备模式配对：首次同进程刷新捕获到 `Constants.verify(): single page mode is 16, multi page mode error [10]`。根因是 `checkPageModeWithDevice()` 会把基础页适配为设备内部模式，但 Settings.Global 仍残留另一宫格的 multi mode。当前 `O.init()` 在存在私有 12/20 主配置时，按适配后的基础页选择原版合法 multi mode；修复后该异常为 0。
- 数据和视觉验证：12→20 后原 12 个图标、板块和顺序保持不变；最终 20→12 后诊断为 `grid=12`，截图确认 3×4，图标顺序不变。当前测试板块只有 12 项，因此没有构造“超过 12 项”的拆分样本；拆分算法仍完全由原版 `F.i()` 负责。
- 同进程根因：保持当前 Surface 并触发原版 `J.onResume() -> v.run() -> J.Hv()` 时，日志证明配置变化可被识别，complex mode 会在 10/13 间切换；但现有 PageView 仍持有迁移前的 Cell 模型和 native batch 容量。只调用原版 Cell/Page 私有刷新会在 20→12 读取已拆分后的旧 Cell，并在 12→20 写越旧 native 容量，分别触发空引用、数组越界或 GL 事件重入，不能作为最小安全修复。
- 已否决并清理：`Activity.recreate()` 会撞上原版单 Activity 防护和进程级 EGL/SMEngine 全局状态，出现旧 GL 事件访问新场景、黑块或 native SIGSEGV；局部重建 Cell/Page 则实质上需要重写 PageView 模型和 native 批次生命周期。相关实验入口、trace 和 pending 状态均已删除，未把失败方案留在最终源码。
- 当前安全路径：宫格数据库迁移完成后使用独立的进程重生兜底，不再复用会清理主题消息的主题冷切换辅助函数；新旧模式相同时直接跳过。2026-07-15 最终 12→20 回归中，视觉为 4×5、模式日志为 `grid=20`，无新增 Java/native 崩溃，但 PID 从 `17724` 变为 `17942`，所以阶段 3 和阶段 4 均保持进行中。
- 验证：完整构建、v1/v2/v3 签名、ADB 覆盖安装通过；最终新进程首帧为 5530 ms，数据库和视觉迁移正确，日志无 single/multi 校验异常、无 `FATAL EXCEPTION` 或 native fatal signal。

本次未修改数据库结构或原版 `F.i()` 算法，未修改二进制 Manifest，未新增固定延迟。保留既有 grid 重载的 killProcess/Alarm 兜底，因此阶段 3、阶段 4 仍为进行中；阶段 5 及以后没有与该 PageView/EGL 生命周期共用安全修改链，本次未修改。

#### 启动专项阶段 2：天气和角标的恢复开销

- 根因：WeatherBridge 的 Launcher 恢复入口没有自身开关门禁，每次会查询全部 Launcher Activity 并加载 Label，HOME 自动定位缺权限时还会主动弹权限；已安排的小时任务不检查关闭状态。角标恢复每次 resume 都可能回放持久计数并请求监听服务绑定，旧实现还在 1500 ms 后重复 rebind；通知监听 rebuild 会广播所有包，即使计数未变化。
- 原版复用：天气数据仍进入原版 `LauncherReceiver -> DatabaseHandler/DatabaseUpdater -> Cell/PageView -> ActiveIcon/WeatherView/CalendarView`；角标继续向原版接收链广播受影响包的计数，不新增桌面数据库或场景模型。
- 天气修复：WeatherBridge 自身第一层检查动态开关，关闭时不扫描、不加载 Label、不定位、不安排周期任务、不联网；天气组件首次需要时缓存，只在包增删替换变化及 Profile/分身变化时失效。明确包名/组件名走快速判断，只有厂商天气命名空间候选才读取 Label。HOME 恢复不再申请定位权限；小时任务每轮重新检查开关，关闭后停止续约。
- 角标修复：生命周期只保留首帧后的 `applyBadgeIfDirty() -> replayIfDirty()`；角标隐藏、无通知访问权限、服务已同步或持久计数版本未变化时返回。删除 1500 ms 第二次 rebind；监听服务比较新旧计数，只广播变化包，通知消失时仍通过旧记录集合广播 0。
- 验证：完整构建、v1/v2/v3 签名和 ADB 覆盖安装成功。模拟器显式冷启动为 1253 ms；诊断确认动态天气关闭、角标隐藏。连续三次从系统设置返回前后 PID 均为 `7353`，WeatherBridge、天气缓存解析、定位权限请求和 Launcher `FATAL EXCEPTION` 日志均为 0。
- 未验证：通知访问开启且存在活动通知时的角标增量广播、动态天气开启后的组件缓存失效、实体机和多 ROM 功耗仍待真机回归。

本阶段未修改二进制 Manifest、数据库结构和原版 `F.i()`，未新增 killProcess 或 Alarm 重启；删除角标 1500 ms 重复 rebind 固定延迟，保留天气必要的 1 小时 TTL 调度且关闭后不续约。阶段 3 尚未开始。

#### 启动专项阶段 1：Launcher 启动和返回桌面

- 根因：`Launcher.onCreate()` 在原版 `J.b()` 后立即再次写系统栏并执行 `stabilizeLauncherResume()`；该方法同步回放角标、主动 requestLayout/invalidate/requestRender，并在 80/260/1200 ms 重复补帧。`onResume()` 又同步执行导航栏、壁纸、天气扫描和角标回放，`onWindowFocusChanged()` 继续无条件写窗口属性。首帧前兼容工作重复且没有真实完成信号。
- 原版复用：保留 `Launcher.onCreate() -> J.b(Activity)` 和 `Launcher.onResume() -> J.onResume()`；使用原版 `vc.onDrawFrame() -> Eb.update()` 后的真实 GL 帧作为兼容任务边界，不改变 PageView、模型或 SMEngine 初始化。
- 修复：拆分为一次性进程兼容、按状态变化应用导航栏、角标 dirty 回放和首帧后 Loading 完成。启动及每次 resume 只请求一个 GL 帧信号，GL 线程随后把壁纸 pending、角标、动态图标和所选图标包任务合并投递到主线程。动态天气关闭时不进入 WeatherBridge；角标隐藏或持久数据未变化时不 replay。
- 导航栏缓存：记录 Window token、隐藏导航栏开关、目标 system UI visibility 和导航栏颜色；ROM 没有改变实际窗口状态时直接返回，真实状态被 ROM 重置时仍会重新应用。
- 删除延迟：移除普通启动 80/260/1200 ms 三次补帧和重载 Loading 320/760/1600 ms 三次补帧；没有新增固定延迟。Loading 改为真实 GL 帧后再等待一个 Choreographer 帧关闭。
- 验证：完整构建、签名、覆盖安装成功。冷启动原版初始化 159 ms、Surface 564 ms、首个 GL 帧 937 ms、兼容任务 938–941 ms、Model/Page 964 ms；兼容任务确认晚于首帧。连续 5 次热返回为 173–219 ms，PID 前后均为 `6559`，日志无 Launcher 崩溃或定位权限请求。
- 未验证：实体机、多 ROM、通知角标开启状态、动态图标开启状态、真实重载 Loading 和逐帧录像仍待后续专项阶段或真机回归。

本阶段未修改二进制 Manifest、数据库结构和原版 `F.i()`，未新增 killProcess 或 Alarm 重启。阶段 2 后续已完成。

#### 启动专项阶段 0：启动基线和诊断

- 阶段判定：专项计划没有完成标记，代码中也不存在规定的九个诊断标记，`ORIGINAL_BEHAVIOR_REFERENCE.md` 不存在，因此阶段 0 是第一个未完成阶段。本次没有进入阶段 1。
- 原版对照：`Launcher.onCreate()` 保持调用原版 `J.b(Activity)`；`J.handleMessage()` 的 `MESSAGE_COMPLETE` 作为模型完成信号；`vc.onSurfaceChanged()` 作为有效 Surface/场景尺寸信号；`vc.onDrawFrame()` 作为真实 GL 帧信号。
- 修改：新增 `LauncherStartupDiagnostics`，记录 `elapsedRealtime`、启动相对耗时、PID、线程、Activity 实例、宫格、普通主题、透明模式、动态图标、图标包和角标状态。每个标记每次 Activity 启动只输出一次，不逐帧或逐图标记录。默认开启，可通过全局键 `launcher_startup_diagnostics_enabled=0` 关闭；状态读取异常只降级为 `state=unavailable`，不阻断 Launcher。
- 原版链路：新增 `docs/development/ORIGINAL_BEHAVIOR_REFERENCE.md`；实测结果写入 `docs/development/LAUNCHER_STARTUP_BASELINE.md`。
- 首次冷启动（覆盖安装、保留数据）：原版同步初始化 429 ms、当前兼容任务完成 824 ms、Surface 1761 ms、首个 GL 帧 1766 ms、Model/Page 4279 ms、系统 `Displayed` 2455 ms。
- 第二次冷启动：原版同步初始化 119 ms、当前兼容任务完成 135 ms、Surface 627 ms、首个 GL 帧 983 ms、Model/Page 1018/1019 ms、系统 `TotalTime` 1262 ms。
- 热返回：从系统设置页返回 Launcher 为 `LaunchState=HOT`、237 ms，PID 前后均为 `4749`；熄屏/点亮后 PID 仍保持。关闭诊断开关后冷启动标记数为 0。测试日志无 Launcher `FATAL EXCEPTION`。
- 未验证：没有清除数据测试首次安装空数据库；未单独自动化最近任务卡片返回；未做实体机、多 ROM 和逐帧录像。

验证：`build.bat` 完整通过；最终 APK 为 `v1.5.4 (29)`、`minSdkVersion=23`、`targetSdkVersion=28`；二进制 Manifest 可由 `aapt2 dump xmltree` 解析；`apksigner verify --verbose` 确认 v1/v2/v3 签名有效；`adb install -r -d` 覆盖安装到 `emulator-5554` 成功。

### 2026-07-13

#### 恢复所有设置页面的顶部/底部拉伸回弹

- 用户现象：当前设置页滚动到顶部或底部后继续拖动没有任何反馈；maintained 参考项目会随手势产生带阻力的边缘拉伸，松手后回弹。
- 根因：maintained 的 `setting_main.xml`、`app_icon_settings_layout.xml`、`launcher_anim_chooser_layout.xml` 等滚动容器原本统一声明 `android:overScrollMode="always"`，当前资源也保留了这些属性；但 `MaintainedLauncherSettingsHost.tuneScrollBars()` 在页面绑定后递归把每个 View 改成 `OVER_SCROLL_NEVER`，程序化创建的应用图标列表和单应用替换图标页也显式禁用了 overscroll，因此 XML 行为被 Java 覆盖。
- 修复：沿用 maintained 的系统实现，不新增自绘动画。公共调校只对真正可纵向滚动的 `ScrollView` 和 `AbsListView`（包含 `ListView` / `GridView`）设置 `OVER_SCROLL_ALWAYS`，并在统一 `setSettingsContentView()` 页面装载入口执行，覆盖一级、二级和三级设置页；三个程序化滚动容器同步移除 `OVER_SCROLL_NEVER`。普通 View 不参与 overscroll，弹窗内部仅在正文过长时滚动的区域继续保持原逻辑。
- 回归注意：隐藏滚动条、关闭快速滚动和关闭文本筛选等原设置页调校保持不变；不得为此引入逐页自绘弹簧动画。Android 12+ 使用系统 stretch，较旧系统可能呈现平台原生边缘反馈。

验证：`build.bat` 已完成 maintained 设置资源构建、apktool 回编译、Java 兼容宿主编译、dex 合并、zipalign 和签名；`aapt2 dump badging` 确认为 `com.smartisanos.launcher v1.5.3 (28)`，`apksigner verify` 确认 v1/v2/v3 签名有效。本次 ADB 设备列表为空，边缘拉伸幅度和所有三级页面的真机触感仍待设备连接后确认。

#### 修复首页向右拖动无反馈，恢复原版边界回弹

- 用户现象：首页向左可以正常进入第二页，但在第一页向右拖动完全没有位移，视觉上像触摸失效；maintained 参考项目会产生带阻力的越界位移，并在松手后回到第一页。
- 根因：当前 `PageView.updateScroll()` 和 `PageScrollAnimation.updateScroll()` 本身保留了原版 `SCROLL_PARA_TABLE` 阻尼曲线，但原版会在 `Constants.sLeftScreenEnabled=true` 时把首页正向位移钳制为 `0`，将手势交给锤子系统负一屏。原版锤子系统始终提供全局键 `sm_launcher_left_screen_state`，而普通 Android 没有该键；`ua.f(Context)` 却使用 `1` 作为缺省值，导致移植环境误判负一屏已开启并吃掉回弹。
- 修复：保留原版分页、阻尼和松手回弹实现，仅将缺失全局键时的默认值由开启改为关闭；读取到真实键值 `1` 时仍按原版启用负一屏。这样普通 Android 首页向右拖动会显示原版弹簧阻力，松手仍停在第一页，首页向左翻页不受影响。
- 对照：`clean_launcher` 与当前 APK 均包含负一屏钳制；maintained 已移除负一屏依赖，因此不会触发该钳制。此次修改修正的是移植环境的系统设置缺省语义，不是重写触摸或动画。

验证：`build.bat` 已完成 apktool Smali 回编译、maintained 设置资源构建、Java 兼容宿主编译、dex 合并、zipalign 和签名；`aapt2 dump badging` 确认为 `com.smartisanos.launcher v1.5.3 (28)`。本次 ADB 设备列表为空，首页右拖阻尼距离和松手回弹仍待设备连接后真机确认。

#### 动态天气/日历阴影根因修复与图标设置弹窗统一

- 动态阴影根因：当前 `ActiveIconView.a(base, active)` 已转到 `LauncherSettingBridge.composeActiveIconToBaseBounds()`；该方法为避免双层图标只把动态主体画进新的透明 Bitmap，却完全没有生成阴影。此前在 ActiveIcon 节点创建后补调 `g.rl()` 只影响私有 3D 阴影节点，不能进入最终缓存 Bitmap，而且该 `sc[27] + MutiTexMaterial` 链在现代 Android 上存在已验证崩溃风险，因此视觉上始终没有稳定阴影。
- 删除 ActiveIcon 创建尾部无效的 `rl()` 补丁，避免重复创建私有 GL 阴影节点和恢复已废弃崩溃链。
- 图标包选择不再使用系统 `AlertDialog.Builder.setItems()`；改为复用 `prepareSmartisanDialogRoot()`、统一标题/分隔线/列表按压态/底部取消按钮，并标明当前选择。选择、后台预热和桌面刷新逻辑保持不变。
- 桌面图标大小弹窗宽度统一为 `min(380dp, screenWidth - 32dp)`；移除预览区额外的渐变背景、描边和圆角框，只保留当前百分比、大小预览、滑杆与刻度，底部按钮继续复用统一组件。

验证：`build.bat` 已完成 maintained 设置资源构建、apktool 回编译、Java 兼容层编译、dex 合并、zipalign 和签名；`aapt2 dump badging` 确认为 `com.smartisanos.launcher v1.5.3 (28)`。本次 ADB 服务可启动，但设备列表为空，动态阴影视觉和三个弹窗的真机尺寸仍待设备连接后确认。

#### 桌面图标首帧恢复原版快速路径与分层缓存

- 根因：当前 `view/a/g.1.smali::vl()` 对所有普通应用无条件调用 `MaintainedLauncherSettingsHost.loadIconForDesktopItem()`；该兼容链会解析组件、查询 `RedirectIconDB`、检查图标包和在线缓存，返回后 Smali 又调用一次 `normalizeLauncherIcon()`。即使首次安装已经默认关闭改进版图标，普通应用仍承担完整兼容调度和重复归一化，因此首屏进入速度没有恢复到原版。
- 原版对照：`clean_launcher_raw` 的同一 `vl()` 在普通用户分支直接调用 `PackageManager.getApplicationIcon(packageName)`，然后转 Bitmap 并按 `icon_size_with_shadow` 缩放，不经过 Java 图标调度器。
- 修复：新增只读元数据、不解码自定义 PNG 的轻量覆盖判定。仅当全局改进版开启、图标包模式启用，或该组件存在 `AUTO/RESOURCE/PACK/CUSTOM` 覆盖时才进入现有兼容链；其余应用直接恢复原版 `getApplicationIcon()`。兼容链内部已经统一归一化，Smali 的第二次归一化已删除。
- 图标包：新增无扫描的持久模式判断和非阻塞读取。冷启动尚未解析所选图标包时，桌面先显示系统原图，只启动一个后台线程解析 `appfilter`；完成后统一触发数据库/桌面图标刷新。不得再在 Launcher 模型线程同步解析整份图标包 XML。
- 在线图标：继续保持“内存 -> `files/online_icon_cache_v3` -> 后台双镜像下载”的顺序；首帧未命中时立即回退系统原图，HTTP 只允许在专用执行器中运行，下载完成落盘后再刷新对应桌面图标。进程内 Bitmap 缓存由无上限 `HashMap` 改为按像素占用计费的 8 MiB `LruCache`，磁盘持久缓存不变。
- 回归约束：单应用改名只有展示名时不能误判为图标覆盖；自定义相册图标仍只在真正命中该组件时读取磁盘字节；图标包和在线资源未就绪时必须显示原图，不能阻塞首帧或留下空白占位。

验证：`build.bat` 已完成 apktool 重打包、Java 兼容宿主编译、dex 合并、zipalign 和签名；`aapt2 dump badging` 确认为 `com.smartisanos.launcher v1.5.3 (28)`，`apksigner verify` 确认 v1/v2/v3 均为 true。本次 ADB 设备列表为空，尚未完成真机冷启动耗时、图标包后台回填和在线图标下载后刷新验证。

#### 修复动态天气和日历双层图标

- 根因：原版 `ActiveIconView.a(base, active)` 假定 `base` 是原版包提供的底板/阴影，但当前移植链路传入的是完整静态天气或日历图标。恢复原版“先画 base、再画 active”后，两份完整图案被同时绘制，真机表现为大小不同的双边框、双层日历。
- 修复：合成缓存图时仅使用静态图标确定输出画布尺寸，不再把完整静态图标绘入画布，最终只显示一份动态天气或日历本体。
- 回归：不得再次在 ActiveIcon 合成结果下方绘制完整应用图标，也不能恢复已废弃的人工 `_shadow` 资源方案。

#### 【已废弃】恢复 v1.5.3 动态天气和日历尺寸链（比例与阴影结论已被后续真机截图推翻）

#### 应用改名弹窗接入统一锤子风格容器

- 根因：应用名称修改页仍单独使用 `smt_dialog_bg_full`、`smt_dialog_header`、`smt_dialog_footer` 与独立按钮背景，和已统一的确认、信息、检查更新、图标大小弹窗不是同一条构建链路，导致标题颜色、底部圆角、按钮高度和键盘弹出后的视觉均不一致。
- 修复：`showRenameIconDialog()` 改为复用 `prepareSmartisanDialogRoot()`、`smartisanDivider()` 和 `smartisanDialogActionButton()`；标题、面板圆角、`clipToOutline`、分隔线与双按钮的 `56dp` 高度完全沿用已验证的统一组件。改名输入框与即时写入/刷新逻辑保持不变。

#### 【已废弃】动态天气和日历的专用阴影资源选择修复（生成主题专用阴影会抹掉原版半透明边缘）

- 此方案只修复了前景路径误改问题，但将完整底框改到人工生成的 `_shadow*` 文件，并在生成时裁掉了原版 PNG 中 alpha 小于 `128` 的柔和边缘；因此透明主题下天气和日历仍明显比普通图标淡。保留本标题作为历史，不再使用该资源选择方式。

#### 【已废弃】动态天气和日历复用原版底图阴影（只恢复 PNG 不足以恢复完整合成阴影）

#### 【已废弃】动态天气和日历恢复原版 ActiveIcon 合成与实时缩放（完整静态图标被误当作底板，造成双层）

#### 通知使用权未授权时角标开关保持关闭

- 开启“显示图标上的角标”或“紧贴屏幕横扫清除角标”时，若尚未授予通知使用权，只提示并跳转系统授权页，不写入开关状态、不触发桌面角标逻辑；用户授权后需要再次手动开启。

#### 天气定位、更新与原版动态刷新链路核对

- 对照 `smartisan-launcher-maintained`：它优先读取 `LocationManager` 的最后位置，再用本地 `CityDatabaseHelper`/NMC 城市索引匹配站点，最后通过后台 `WeatherForceSyncTask` 请求中国气象数据并回写天气对象。因此“快”主要来自已有位置和本地城市匹配，不是每次打开页面都重新定位。
- 当前 `WeatherBridge` 已采用同类策略：优先使用 network/passive/GPS 的最近位置、六小时位置缓存和本地城市站点；天气数据正常一小时 TTL，只有过期、手动刷新、城市/定位模式变更时才后台联网。保持该策略，避免桌面翻页把定位和网络请求压到 UI 体验上。
- 对照原版 `clean_launcher`：天气更新由 `weather_data_changed`/`WeatherView.g(Intent)` 协议分发；CalendarView 在 Launcher 的 `onResume()` 中检查日期变化并触发原版翻页动画，WeatherView 同样在原版 ActiveIcon 恢复链路中恢复。原版没有“每次桌面翻页都重新定位或联网”的实现，因此本次不引入会破坏原版节奏和耗电的页面切换刷新。

验证：源码逐像素核对确认恢复后的天气与日历底图和 `clean_launcher_raw` 原版一致，低 alpha 边缘像素已恢复；`build.bat` 已完成重打包、签名，`aapt2 dump badging build\\launcher-signed.apk` 确认为 `com.smartisanos.launcher v1.5.3 (28)`，APK 内容已确认包含原始 `calendar/bg.png` 与 `weather/weather_bg_sunny.png`。本次 ADB `devices` 返回空列表，尚未完成覆盖安装和真机视觉回归；设备重新连接后需验证透明主题下动态天气/日历的阴影与普通图标一致性，以及天气前景动画。

### 2026-07-12

#### 单应用替换图标页的持久缓存回填与在线候选刷新

- 对照 `smartisan-launcher-maintained`：其应用图标设置主要使用本地 `IconDB`、应用原图和已安装图标包的本地资源，并不在单应用候选页临时联网下载 PNG。当前移植版新增在线图库后，必须额外保证磁盘缓存可直接渲染。
- 根因：候选列表用 `libraryIconStored()` 判断时会识别 `files/online_icon_cache_v3/` 下的 PNG；但 `libraryIconDrawableNonBlocking()` 之前只查进程内 `sSmartisanIconCache`。应用/进程重启后磁盘文件仍在、内存位图为空，候选会被加入网格却没有图片；预取又因“文件已存在”跳过下载，形成永久空白卡片。
- 修复：候选绑定未命中内存时立即解码本地持久缓存并回填内存，再渲染对应图标；在线候选页的局部网格刷新从 `0.9s/2.6s` 延伸到 `6.5s/11s`，覆盖双镜像超时和共享下载线程排队后的完成时机，且只替换网格、不重建页面或丢失滚动位置。
- 缓存语义：已下载图标不会在每次打开时重新下载；顺序为内存缓存 -> `files/online_icon_cache_v3` 持久缓存 -> 后台镜像下载。只有磁盘和内存均未命中、且未处于失败重试冷却期时才联网。

#### 设置页锤子风格弹窗容器与按钮栏统一

- 根因：宫格确认、检查更新信息、图标大小和下载进度各自创建 `Dialog` 根容器；双按钮确认框的按钮本体为 `50dp`、按钮栏却为 `56dp`，形成按钮下方留白；单按钮传入 `side=0` 时没有设置下圆角；根容器未裁剪子 View，按钮背景会覆盖面板底部圆角。
- 修复：在 `MaintainedLauncherSettingsHost` 复用 `prepareSmartisanDialogRoot()`，统一面板颜色、`8dp` 圆角和 `clipToOutline` 裁剪；统一单按钮下侧双圆角、双按钮左右下圆角，以及 `56dp` 按钮栏的实际子项高度。宫格确认、检查更新、图标大小和下载进度均已接入。
- 视觉约束：标题保持居中；说明正文保持左对齐；按钮栏紧贴正文分隔线，底部无额外留白，面板上下圆角一致。

#### 【已废弃】系统卸载取消后在 Launcher.onPause 无条件强制复位

> 此旧方案会提前清掉回收站场景并跳过取消／成功动画，已由 2026-10-02「卸载取消、成功动画与桌面下载稳定性」取代；不能恢复无条件 fd → T → hd。GL 强制清理只作为异常兜底保留。

#### 【已废弃】在 Launcher.onPause 直接调用 oa.hd（非 GL 线程崩溃）

#### 【已废弃】使用 Activity.recreate 重建卸载场景（可能触发空节点崩溃）

#### 设置弹窗统一（保留）

- 设置页的确认、信息、检查更新下载进度和桌面图标大小弹窗统一使用现有锤子风格的圆角面板、居中标题、分隔线和底部操作按钮；说明正文统一左对齐。图标大小仅保留自身滑块/预览内容，不再拥有一套不同的标题和按钮外观。

#### 12 / 20 宫格切换按原版逻辑最终修复

- 根因不是图标数据丢失，而是兼容设置层把外部的“20 宫格”直接当作原版内部页面模式使用。原版 `Constants.getPageModeFromMode(20)` 实际映射为内部 `MODE_9 (0x9)`；这个值是原版 4 x 5 宫格的运行模式标识，不是九宫格布局。此前绕过这层映射、传入 `20` 或自行保存/恢复页面，都会让旧页面坐标被错误解释，表现为每个板块只留下 9 个图标。
- 最终实现严格复用原版：设置层先通过 `Constants.getPageModeFromMode()` 获得内部模式，再在原版 `DatabaseHandler.mWorker` 线程调用 `data/F.i(oldPageMode, newPageMode)`，随后重载桌面。不得把数据库迁移放到 UI 线程，也不得按包名、安装时间或当前可见图标重新排序。
- 行为与原版保持一致：`12 -> 20` 只切换运行布局，`F.i()` 不改写板块成员、顺序或格子位置，因此同一板块原有 12 个图标会完整保留；`20 -> 12` 仅当单板块超过 12 个图标时，按原有顺序拆出后续 12 宫格板块。拆分后的板块在切回 20 宫格时不会自动合并，这是原版既定语义。
- 对照依据：`build/decompiled_theme_check/com.smartisanos.launcher-3` 中的 `Constants.smali`、`data/F.smali` 和原版模式切换调用链。已通过 ADB 安装与真机往返验证：12 -> 20 保留同板块 12 项，20 -> 12 只在溢出时拆分。

#### 首次安装默认项与应用图标候选加载优化

- 首次安装默认关闭“改进版图标”“动态天气和日历”“显示图标上的角标”“紧贴屏幕横扫清除角标”，避免桌面首帧触发额外图标替换、动态纹理和通知监听处理。
- 图标包预热对齐 maintained 的 `IconPackManager.warmUpIconPackList()`：后台扫描已安装图标包的包名、`appfilter` 与 drawable 映射，填充内存/本地缓存；它不下载在线图标，也不会因为改进版图标默认关闭而进行网络请求。
- 单应用替换页候选读取改为内存缓存、磁盘缓存和已安装图标包的本地资源。没有实际候选图标时不再留下空白默认占位格；页面绑定阶段不触发联网下载，避免首次进入出现空白后再闪烁补图。
- 已缓存的改进版图标可在用户之后开启功能或单独选择时直接复用；在线图标仍只在明确需要且本地没有缓存时才请求。

#### 【已废弃】直接重建桌面场景以消除切换闪屏

### 2026-07-11

#### 应用改名即时刷新、设置页转场与角标开关修复

- 单应用改名保存后会同步更新 redirect 展示名、桌面条目的 `title` 和当前场景的文字纹理，并在数据库提交完成后补发目标应用刷新事件；不需要退出或重开桌面。
- 设置页一级、二级、三级改为在同一容器内完成左右平移；连续进入/返回会清理上一轮转场遗留视图，避免防点击状态残留造成“点了没反应”。
- 强迫症选项中的角标开关改为正向语义“显示图标上的角标”；开启时若未授予通知使用权，直接跳转系统授权页。旧的提示链接已移除，横扫清除角标的授权行为保持不变。

#### 【已废弃】通知角标数字比例与宫格顺序迁移修复

### 2026-07-10

#### 文件夹拖动/长按释放后图标行距漂移修复

- 现象：文件夹刚打开时三层书架图标对齐正常；只要长按后松手，或拖动图标重新排列，第一行会偏上、第三行会偏下，中间行保持正常。关闭文件夹再打开又恢复正常。
- 根因：初次布局走过文件夹页的可见书架行高适配，但拖拽、回弹、换位动画会重新调用容器级 `fa.ir()`，直接取全局 `Constants.pageCellCenterPoints`。这组全局点是普通桌面网格坐标，行距比打开文件夹书架大，所以动画/释放阶段把上下两行重新拉开；旧方案只改 `M.smali` 的局部 `setTranslate()`，后续动画再次取 `ir()` 时仍会覆盖。
- 修复：在 `fa.ir()` 源头调用 `FolderCellPositionAdapter.adaptPositions(owner, positions)`。当 owner 是文件夹容器 `com.smartisanos.launcher.view.b.t` 时，返回克隆后的点数组，以中间行为锚点、按 `window_width * 358 / 1080` 计算三层书架行距；非文件夹容器直接返回原全局数组。
- 防回归点：不得直接修改 `Constants.pageCellCenterPoints`，否则普通桌面冷启动网格会被文件夹行距污染；也不要只在某个动画类里补偏移，因为拖拽链路有多处会重新读取 `fa.ir()`。
- 验证：`build.bat` 完整构建、zipalign、签名通过；最终 APK 中 `classes.dex` 的 `fa.ir()` 已包含 `FolderCellPositionAdapter.adaptPositions(...)` 调用，`classes2.dex` 已包含 `adaptPositions` 方法。用户真机复测确认问题已解决。

涉及文件：

- `launcher/smali/com/smartisanos/launcher/view/b/fa.smali`
- `launcher/tools/java/com/smartisanos/launcher/data/FolderCellPositionAdapter.java`

#### 应用图标选择页与默认图标状态修复

- 应用图标页新增单应用“替换图标”二级页，展示当前应用信息和可选图标网格；候选来源包括图标库包名、系统应用别名、`assets/icons/variants.json` 中的同应用变体、当前图标包命中图标和相册自定义入口。
- 选择图标库候选时写入 `RedirectIconDB.MODE_RESOURCE:<name>`，选择图标包候选时回到自动改进版/图标包链路，选择相册图标时沿用已有自定义图片流程；切换后刷新当前行并保持应用图标页滚动位置。
- 修复默认图标选择状态：切回默认图标会写回 `MODE_ORIGINAL`、清空自定义 icon blob、刷新桌面图标和当前行状态；右侧箭头只进入选择页，不再让默认图标选择状态停留在右侧候选图标上。
- 新增 `icons/variants.json` 与 APK 内 `launcher/assets/icons/variants.json`，用于记录同一包名的多个候选 PNG；生成图标索引后需要同步该文件，供应用图标选择页读取。

涉及文件：

- `launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java`
- `launcher/tools/java/com/smartisanos/launcher/data/redirectIcon/RedirectIconDB.java`
- `icons/variants.json`
- `launcher/assets/icons/variants.json`

### 2026-07-03

#### 主题保存成功但必须重开桌面才生效

- 客户 v1.5.3 日志显示主题四路状态已从格子正确保存为经典蓝、再保存为毛玻璃，`launcher_ready=true`，但两次均为 `original=true, queued=false`；因此不是主题包、持久化或机型识别问题，而是当前场景缺少切换消息。
- 根因是兼容层错误地把 `X.ja()` / `O.a()` 的保存成功返回值当成“原版已经发送 `MESSAGE_CHANGE_THEME`”，只在保存失败时才设置 `a.r.sj`。原版 `ThemeItemActivity` 实际是在保存后继续通过 Handler 返回桌面，由 Launcher 消费该消息。
- 修复为主题持久化后始终只设置一次待消费的 `MESSAGE_CHANGE_THEME`，再执行截图与返回桌面；新增 `THEME_DISPATCH pending_message_set/failed` 日志。切换不再依赖用户关闭并重新打开桌面。
- ADB 在 ColorOS 真机稳定复现解锁时出现 `dispatching lifecycle unlock fallback`，确认解锁兜底本身正确进入原版 `action_keyguard_on + USER_PRESENT`；异常主题动画来自 `a.r.sj` 中未及时消费的静态主题消息。
- 返回桌面 180ms 后现主动调用原版 `a.r.a(Message)` 消费并清空本次主题消息，日志记录 `pending_message_consumed`；超过主题保护期仍残留的陈旧消息会在解锁动画前清除，避免主题切换动画劫持下一次解锁。

#### 天气多数据源容错与失败状态修复

- 第二轮真机反馈确认，单纯增加 MET Norway/Open-Meteo 仍会在部分中国大陆网络同时不可达，并且系统 Geocoder 等待会让城市搜索比旧版更慢。最终方案不再把境外服务作为中国城市的首选。
- maintained 资源包原本已内置 `city_base` 与 `city_cn`，包含三千余个中国站点的名称、省市、经纬度和中国天气网站点 ID。手动城市搜索现直接查询本地数组，命中时零网络、立即返回；自动定位按经纬度选择最近国内站点，逻辑不判断手机品牌或 ROM。
- 国内站点天气优先使用中国天气网 `d1.weather.com.cn/sk_2d/{stationId}.html`，实测蚌埠站约 0.05 秒返回；连接/读取超时为 1.5/2 秒。只有国内站失败或坐标不在国内城市表覆盖范围时，才并发竞速 MET Norway/Open-Meteo。
- 根因确认：天气此前只依赖 Open-Meteo；接口 TLS/连接超时后不会写入 `weather_updated_at`，设置页只能显示“尚未更新”，动态图标则可能继续呈现旧城市温度或原版占位内容。
- 天气改为 MET Norway Locationforecast 与 Open-Meteo 并发竞速，使用首个有效结果；不再等待主源超时后才串行请求备用源，整体等待上限收口为 6.5 秒。
- 城市搜索优先使用手机系统 `Geocoder`（澎湃 OS 可走系统地理服务），无结果时才回退 Open-Meteo；在线回退连接/读取超时缩短为 1.8/2.8 秒，已搜索结果继续使用十分钟内存缓存。
- 城市或自动/手动模式改变时清除旧地点的温度、天气代码和数据源，避免把上一城市的 25℃误认为新城市结果。
- 成功刷新保存实际数据源；双源均失败时保存精确错误，动态天气设置页显示数据源或失败原因，方便客户日志分析。

#### 客户诊断日志增强与应用图标列表完整性修复

- 修复“应用图标”设置页最多只显示 120 项的问题：移除硬编码上限，已解析且符合显示条件的应用现在全部展示。
- 修复澎湃 OS 返回“非空但不完整”应用列表时无法补全的问题：当前用户始终合并 `PackageManager` 与 `LauncherApps` 的桌面 Activity 并按组件去重；分身/工作资料应用仍受相应功能开关控制。设置页枚举和全局改进版图标切换统一使用该结果，应用数量不再影响是否参与图标匹配。
- 应用图标页新增加载耗时、原始数量、显示数量、过滤数量以及被过滤组件日志，便于直接定位具体缺失应用。
- 主题切换新增切换前状态、主题包安装状态、原版调用结果、消息入队结果、切换后四路持久化值和桌面动画就绪状态。
- Android 普通应用仍只能读取本进程/系统允许范围内的 logcat；完整系统日志仍需电脑 ADB，这是系统权限边界而非记录器遗漏。
- 客户截图中的日志自报版本为 `v1.4.9`（SDK 33），不能作为 1.5.1 或当前版本已经运行的证据。

#### 文件夹、检查更新与图标系统历史记录清理

- 文件夹记录只保留当前有效实现：关闭预览由 `LayoutPropertyAdapter.centerFolderPreview()` 根据可见行列中心生成 2×2/3×3 参数；展开页使用原版固定三列并按书架实际行高适配；主题背景从 `assets/folder_theme_bg/` 读取。固定像素、整组缩放、错误页面坐标旁路等失败过程已删除。
- 检查更新记录只保留当前 `DownloadManager`、Gitee launcher Release 筛选、备用资产地址、下载状态复用和授权 URI 安装链路；自建安装 Session、`file://` 等废弃过程已删除。
- 图标记录只保留当前优先级与行为：单应用自定义 > 图标包 component/appfilter > 改进版映射 > 系统原图；首帧和刷新使用组件级识别，在线图标持久缓存并按需联网。被后续推翻的分身角标和旧待办描述已删除。
- 所有此前已经清空正文的错误实验标题统一改为 `【已废弃】日期：标题`，不再使用删除线或无标记空标题。

#### 完整功能清单与后续状态重新盘点

- 按当前代码重新核对原版交互入口，确认四指横滑切换主题和双指捏合缩放并非待移植功能：四指手势由 `view/Da -> a/a/c (FourFingerSlide)` 调用主题切换栈；双指手势由 `smengine/Ba` 根据 `pinch_scale_threshold` 分发 `onZoomOut/onZoomIn`，切换单页桌面与多页总览/编辑状态。
- 顶部“已完成”已补齐手势、多页管理、页面隐藏/锁定、文件夹、翻页动画、主题、搜索、角标、设置入口、动态图标、应用分身与多用户等现有能力；README 的核心特性同步加入四指和双指手势。
- 删除原“未完成 / 待处理”中全部 `[x]` 已完成项目。当前没有明确缺失的核心桌面功能；剩余内容改为“已完成但需要继续回归”和“已知限制”，避免把跨机型测试、通知系统边界、用户确认安装等平台限制误写成开发未完成。

#### 【部分历史结论已被取代】动态天气/日历对齐尝试、兼容阴影与 Android 16 闪退修复

- 当时真机确认天气数据、动态显示和桌面运行恢复；该样本不能证明 Weather/Calendar LIVE/STATIC world rect 已在全部比例和宫格对齐。“不会残留约 1px 跳动”的最终结论已撤销，当前必须以 `syncActiveIconToStaticArtwork()` 的 ratio/center 自动指标和逐帧矩阵验收。
- 原版阴影来自 Cell `sc[27]`、八张运行时阴影纹理和 `MutiTexMaterial`，依赖 Smartisan `Settings.Global`、已移除的 `android.graphics.BlurImageFilter` 以及旧 shader 的 `uShadowRadius`。普通 Android/Android 16 不得强制开启该链路；真机出现的 GLThread 闪退已通过 ADB 明确定位并完整撤销。
- 【已废弃】早期兼容方案曾将动态底图裁为无阴影主体并生成 `_shadow.png` / `_shadow_transparent.png`。后续真机对比确认该处理会去掉原版纹理中的低 alpha 投影，透明主题下视觉过淡；当前已恢复原版底图并由动态节点直接加载。
- 保留的原版安全路径是 `data/L.smali` 的 `extractAlpha + BlurMaskFilter` 三 Bitmap 合成；依赖 Smartisan 私有 GL/`sc[27]` 的 activeicon 运行时 shadow map 仍保持关闭，两者不能混为一条链路。

### 2026-07-02

#### 【映射/刷新结论保留，尺寸定版已撤销】动态图标、关闭动态后的标准图标映射与在线识别修复

- 实时动画使用原版 `nc(vm)` 纵向坐标；结束后的静态 Bitmap 以动画为基准，使用原版 `sq()` 几何差校正。两条路径职责不同，但最终可见外框必须重合。
- 关闭动态后不再下载天气/日历图标。构建时直接把图标库中完整的 `com.smartisanos.weather.png` 和 `com.android.calendar.png` 编入 maintained 资源 APK，运行时分别以 `static_icon_weather` / `static_icon_calendar` 读取；所有已识别厂商天气、日历均直接命中这两个本地资源，离线和非首次进入桌面也可立即取得完整静态图标。
- `Aa.smali` 关闭动态时原先只排除原版固定日历包名，厂商日历仍可能进入 activeicon 底框替换。现在统一调用 `LauncherSettingBridge.isDynamicIconPackage()`，关闭后所有已识别天气/日历都禁止注入 `weather_bg.png` / `calendar/bg.png`。
- 在线图标过去把超时、DNS/TLS 错误和 HTTP 404 全部记录成一小时“图标不存在”，造成网络偶发失败后长时间识别不到。现在只有所有镜像明确返回 404 才写 miss 缓存；网络故障不再污染不存在缓存，后续加载可自动重试。
- 用户继续真机验证确认，关闭动态后仍显示旧图并非天气/日历包识别失败，而是**已有数据库记录的异步切换竞态**：旧代码发出一次刷新后固定 800ms 杀死 Launcher，数据库 icon blob 可能尚未写回；首次进入桌面会完整建库，因此反而不容易复现。现在静态图标已经内置，并对已有记录执行两阶段刷新，最后等待写回后重建 Launcher；不再把“刷新事件已发送”当成“数据库刷新已完成”。
- 拨号/电话本的组件和标题优先分流未改动；本次标准包映射只作用于关闭动态后的天气和日历。
- 关闭动态只决定“是否走普通图标链路”，不决定普通图标来源。普通链路优先级固定为：单应用自定义/明确选择 > 图标包组件映射 > 已启用的改进版图标（天气/日历使用 APK 内置完整资源）> 应用系统原图。改进版总开关关闭时不会强制使用内置天气/日历；选中图标包时也不会被改进版别名抢占。拨号 Activity 禁止回退到联系人包级映射的保护继续保留。
- 性能日志确认此前一次图标操作会执行数百次 PNG 压缩和网络连接。优化后：动态天气/日历开关只向数据库提交已安装天气、日历包，不再两次全量刷新全部应用；图标大小重启后只重建 LayoutProperty/SceneNode，不再重新匹配、压缩或下载图标；图标更新从“反射直调 + 本应用广播”两次执行改为直调成功即结束、广播仅作失败兜底；全量包列表按包名去重。全局改进版/整包切换仍允许更新全部实际受影响应用。
- 普通 Android 的普通应用图标继续使用原版 `data/L.smali` 软件生成的 dark/light/transparent 三张 Bitmap；动态天气和日历因使用独立 activeicon 节点，直接加载原版 ActiveIcon 完整底图，依赖 Smartisan framework 的 activeicon `sc[27]` GL 阴影链路继续禁用。
- 【已废弃】曾为 256px 动态底框引入画布裁切补偿的双层生成阴影。该方案不能等价于原版纹理阴影，且会覆盖原版半透明边缘，因此不再使用。
- 在线改进版图标成功下载后持久保存到 `filesDir/online_icon_cache_v3`，跨进程重启和覆盖安装复用；读取顺序为内存缓存 → 持久文件 → 必要时联网。天气数据保存在 SharedPreferences，正常 TTL 为一小时，位置 TTL 为六小时；只有缓存过期、用户手动刷新或位置模式改变才联网。

涉及文件：

- `launcher/smali/com/smartisanos/launcher/Aa.smali`
- `launcher/smali/com/smartisanos/launcher/view/a/g.1.smali`
- `launcher/smali/com/smartisanos/launcher/view/activeicon/H.smali`
- `launcher/smali/com/smartisanos/launcher/view/activeicon/m.smali`
- `launcher/tools/java/com/smartisanos/launcher/theme/LauncherSettingBridge.java`
- `launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java`

#### 跨机型冷启动、图标数据库与 Smartisan 框架兼容收口

日志根因：

- DRA-AL00 冷启动时，原版图标数据库一次查询全部 PNG blob，38 个图标已经填满系统固定的 2MB `CursorWindow`，后续行无法装入；这会表现为相册等图标偶发未识别、缓存明明存在却仍重新生成，并增加首次进入桌面的阻塞时间。
- Android 9 及以下会进入原版 `checkDoppelganger`，遍历设备全部安装包。该逻辑只服务 Smartisan 旧分身实现，普通厂商 ROM 已由 LauncherApps/profile 兼容层覆盖。
- Launcher 引用了 Smartisan framework 提供的 `TabletWallpaperHelper` 及内部监听器；普通 Android 没有该类，部分平板/横屏分支会在 verifier 阶段报缺类。
- 冷启动还重复执行完整纹理字段反射/资产校验，并探测不存在的 Smartisan Launchpad 和支付包。这些失败可回退，但会制造主线程 I/O、异常对象和无意义日志。

修复内容：

- 新增 `IconDatabaseCompat`：只查询当前桌面 owner，按 12 条一批读取 `owner/color_info/icon_blob`，每批及时关闭 Cursor；不再依赖扩大厂商私有 CursorWindow，也不会随应用数量增长再次触发 2MB 上限。
- 原版旧分身全包扫描入口已直接停用，不再保留品牌判断；第三方 Android 统一使用现有 LauncherApps 多用户/工作资料夹链路。
- 新增 `smartisanos.app.wallpaper.TabletWallpaperHelper` 兼容类和同名嵌套监听接口，使用 `ACTION_WALLPAPER_CHANGED` 与 Launcher 私有壁纸 URI 兜底；Smartisan 原系统仍可按 framework 优先加载原生实现。
- 从文本与最终二进制 Manifest 删除 Launchpad 服务和 Smartisan 支付权限，删除对应 Service/Runnable 实现及所有调用入口；同时移除启动和布局重建阶段的调试型全资源扫描。
- 发布构建默认关闭原版大量 `Log.e` 调试输出，避免部分厂商 ROM 错误设置 `ro.debuggable=1` 后在首屏解析阶段同步刷日志；仍可通过原 `LOG.kc()` 显式启用。

验证：

- `build.bat` 完整构建和签名通过，覆盖安装 DRA-AL00 成功。
- 强停后冷启动未再出现 `CursorWindow is full`、`TabletWallpaperHelper` 缺类、`Textures/1080p/12/12`、支付包异常和逐包 `checkDoppelganger` 日志；进程保持存活，无 FATAL EXCEPTION / ANR。
- 同一设备最终冷启动首屏 `Skipped frames` 从修改前 38 帧降到 31 帧；这 31 帧来自进程首次创建原版 3D 场景的一次性集中渲染。进程保活后返回桌面复测无 `Skipped frames`，日常返回/切换不是持续性卡顿。不要为消除这一条一次性系统提示而把图标数据库或 SceneNode 更新并发写入渲染线程。

涉及文件：

- `launcher/tools/java/com/smartisanos/launcher/data/IconDatabaseCompat.java`
- `tools/remove_smartisan_runtime_components.py`
- `launcher/tools/java/smartisanos/app/wallpaper/TabletWallpaperHelper.java`
- `launcher/smali/com/smartisanos/launcher/data/a/h.smali`
- `launcher/smali/com/smartisanos/launcher/data/A.smali`
- `launcher/smali/com/smartisanos/launcher/service/LaunchpadService.smali`（已删除）
- `launcher/smali/com/smartisanos/launcher/e/f.smali`
- `launcher/smali/com/smartisanos/launcher/J.smali`
- `launcher/smali/com/smartisanos/launcher/va.1.smali`

#### 日期变更崩溃、动态图切换缓存与在线图标持久化

日志根因：

- `build/launcher_log.txt` 在手动修改系统日期后记录了连续的 Launcher 崩溃，唯一明确的 `am_crash` 为 `ClassNotFoundException: android.location.LocationListener$-CC`。日期变化会促使天气重新定位，真正崩溃点是新 SDK 编译的 `LocationListener` 默认接口桥没有随注入 dex 完成 desugar，而旧厂商系统不存在 `$-CC` 伴生类。
- 日志同时记录 `com.smartisanos.launcher.update_icon` 后台广播被系统拦截，以及天气/日历行因 APK 图标 MD5 相同而跳过写库。两者共同造成关闭动态模式后偶尔继续使用旧的空天气底框。
- `WRITE_SETTINGS` / `WRITE_SECURE_SETTINGS` 拒绝、缺少 `TabletWallpaperHelper$WallpaperChangeListener` 等日志均被原兼容代码捕获，不是本次进程崩溃堆栈；设置值已有 Launcher 私有 prefs 兜底。

修复内容：

- `WeatherBridge` 的一次定位监听显式实现当前 SDK 的全部接口方法，包括批量位置回调和 `onFlushComplete`，最终 dex 不再引用 `LocationListener$-CC`。
- 天气/日历图标数据库写入不再受“APK Bitmap MD5 未变化”短路影响；动态开关两种方向都强制重建这两个包的图标数据。
- 关闭动态天气和日历后，普通图标选择链路不再把 `app_icon_weather` / calendar 动态底框当成完整推荐图标；恢复为自定义图标、图标包或应用系统原图。
- 在线改进版图标从可被系统随时清理的 `cacheDir/online_icon_cache_v3` 迁移到 `filesDir/online_icon_cache_v3`，并自动迁移旧缓存。关闭再打开改进版图标会直接复用已下载文件，不重复下载。
- 网络下载失败不再向进程内 Map 永久写入 `null`；远端 miss 重试窗口从 7 天缩短到 1 小时。系统“相册”仍通过厂商包名/Activity/可见标签映射到 `com.android.gallery3d`，临时镜像失败后可以自动恢复识别。

验证：

- `build.bat` 完整构建、签名通过；最终 dex 搜索不到 `LocationListener$-CC`。
- `adb install -r -d` 覆盖安装到 DRA-AL00 成功，冷启动 PID `9960` 保持存活；清空日志后未发现 `FATAL EXCEPTION`、`am_crash`、`VerifyError` 或新的定位监听异常。
- 真机当前页可正常显示日历与天气完整图标。动态更新前后尺寸仍需用户用原视频场景做最终肉眼回归。

涉及文件：

- `launcher/tools/java/com/smartisanos/launcher/theme/WeatherBridge.java`
- `launcher/tools/java/com/smartisanos/launcher/theme/LauncherSettingBridge.java`
- `launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java`
- `launcher/smali/com/smartisanos/launcher/Aa.smali`
- `launcher/smali/com/smartisanos/launcher/view/activeicon/a.1.smali`

#### 天气位置即时刷新与城市搜索收口

- 自动定位开启和手动城市切换继续把 `weather_updated_at` 清零并强制刷新；新增强制刷新排队：如果切换位置时上一笔天气或定位请求仍在运行，不再丢弃新请求，而是在当前请求结束后按最新自动/手动位置立即补刷一次。
- 定位回调到达时重新检查当前模式；用户已切到手动城市则不再用迟到的自动定位坐标覆盖天气，而是按最新手动城市刷新。
- 城市搜索：
  - Open-Meteo 请求增加 `countryCode=CN`，减少国外同名地点；
  - 连接/读取超时缩短为 4s/6s，结果增加 10 分钟内存缓存；
  - 精确名称优先，优先 `PPLC/PPLA*` 行政城市，再按人口排序；
  - 精确同名城市只保留最高优先级结果，例如“三亚”不再同时显示海南、广西多个同名地点；
  - 普通结果按名称/省份/国家去重，最多显示 5 条。
- `build.bat` 构建成功，安装 DRA-AL00 成功，Launcher PID `2729`。

涉及文件：

- `launcher/tools/java/com/smartisanos/launcher/theme/WeatherBridge.java`
- `launcher/tools/java/com/smartisanos/launcher/theme/LauncherSettingBridge.java`

#### 【已废弃】动态图标视觉边界、日期高屏偏移与关闭缓存修复（尺寸方案错误）
#### 【已废弃】动态图标改为单层画布映射，消除任意尺寸双框（错误）
#### 【已废弃】动态图标两层按同一用户倍率对称缩放（错误）
#### 【已废弃】动态天气/日历绘制层完整回归原版基线（整层回退结论不完整）
#### 【已废弃】动态天气/日历中心锚点统一与错误坐标缩放回滚
#### 【已废弃】撤销动态天气/日历 120% 二次放大

### 2026-07-01

#### 【已废弃】动态天气与日历开关、原版分层恢复和多屏尺寸收口
#### 动态天气补丁导致 Launcher 启动 VerifyError

- 真机日志确认桌面启动即退出不是设置页或网络异常，而是 `Aa.a(Bitmap, String, boolean, ColorInfo)` 在 Android 运行时校验阶段被拒绝：天气包识别分支跳转到普通图标路径时，寄存器 `v2` 尚未赋值。
- 将该方法原有的 `v2 = 1` 初始化恢复到所有分支共同经过的位置，保留跨厂商天气识别，不再产生未定义寄存器。
- 重新构建并通过 ADB 覆盖安装；OPPO PDCM00 冷启动成功，`com.smartisanos.launcher/.LauncherAlias` 保持前台、进程存活，日志中不再出现 `VerifyError` 或 `FATAL EXCEPTION`。

#### 动态天气设置、自动定位与手动城市

- 桌面设置首页新增“动态天气”入口，二级页显示当前天气位置、温度、最近更新时间，并提供“立即刷新”。
- 默认使用系统粗略定位；打开自动定位但尚未授权时，从设置页发起 `ACCESS_COARSE_LOCATION` 请求。
- 新增手动城市模式：输入中文或英文城市名后，通过 Open-Meteo Geocoding API 返回候选城市，用户选中后保存城市名和经纬度并立即刷新天气。手动模式不读取定位，也不需要定位权限。
- 自动定位与手动城市使用同一套天气缓存和锤子原版动态天气广播；切回自动定位后恢复系统位置，正常刷新频率仍为一小时，手动“立即刷新”可绕过缓存。
- 设置页只改变天气数据来源，不改变天气图标所绑定的系统天气 Activity；点击桌面天气仍打开手机自带天气应用。

涉及文件：

- `launcher/tools/java/com/smartisanos/launcher/theme/WeatherBridge.java`
- `launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java`
- `launcher/tools/maintained_settings_res/res/layout/setting_main.xml`
- `launcher/tools/maintained_settings_res/res/layout/setting_dynamic_weather.xml`
- `launcher/tools/maintained_settings_res/res/values/strings.xml`
- `launcher/tools/maintained_settings_res/res/values-zh-rCN/strings.xml`

验证：`build.bat` 完整通过并重新生成、签名 `build/launcher-signed.apk`；定位授权、城市搜索和动态图标刷新仍需连接真机验收。

#### 普通 Android 动态天气恢复

- **原版能力确认**：`activeicon/H.smali`、天气纹理、温度数字、昼夜素材、日出日落切换及更新动画均完整保留；失效点是原版只识别 `com.smartisanos.weather`，并依赖普通 Android 不存在的 `content://com.android.providers.weather_app`。
- **系统天气入口**：新增厂商天气识别，覆盖 Smartisan、Android、vivo/BBK、OPPO/Oplus、MIUI、华为/荣耀和三星常见天气包。`ItemInfo.bf/Qe`、活动图标创建和静态底图生成统一使用识别结果；ItemInfo 的原包名和 Activity 不变，因此点击图标继续打开手机系统自带天气。
- **现代天气数据源**：新增 `WeatherBridge`，使用 Open-Meteo Forecast API 的经纬度接口读取 `temperature_2m`、`weather_code`、`is_day`、`sunrise` 和 `sunset`。WMO 天气代码映射到锤子原版晴、云、阴、雾、雨、冻雨、雪和雷暴代码，再转换成原版 `com.smartisanos.weather.data.update` 广播。
- **位置与权限**：最终 APK 增加 `ACCESS_COARSE_LOCATION`；仅当设备存在可识别的天气应用时请求粗略位置。优先使用 6 小时内的系统最近位置，无可用位置时请求一次网络定位；不申请精确定位。
- **刷新与缓存**：天气缓存有效期为 60 分钟；Launcher 恢复、进程内每小时定时检查以及首次授权后均会尝试刷新。缓存有效时不联网，请求失败时保留上次天气，不清空图标。位置缓存有效期为 6 小时。
- **原版协议兼容**：原 `CallExpandService.q(Context)` 改为读取桥接缓存并异步触发刷新，返回字段仍为 `weatherCode`、`temp`、`fahrenheitTemp` 和 `_1sunRiseAndSet`，因此没有重写 SMEngine 天气动画。
- **权限清单**：文本 Manifest 与最终构建注入的二进制 Manifest 均包含粗略定位权限；新增 `tools/patch_weather_location_permission.py` 用于维护保留的 AXML 清单。
- **数据服务说明**：Open-Meteo 非商业使用无需 API Key；发布时应保留来源说明，商业使用前需重新确认授权。接口文档：`https://open-meteo.com/en/docs`。

涉及文件：

- `launcher/tools/java/com/smartisanos/launcher/theme/WeatherBridge.java`
- `launcher/smali/com/smartisanos/launcher/a/a.1.smali`
- `launcher/smali/com/smartisanos/launcher/data/ItemInfo.smali`
- `launcher/smali/com/smartisanos/launcher/view/a/g.1.smali`
- `launcher/smali/com/smartisanos/launcher/Aa.smali`
- `launcher/smali/com/smartisanos/launcher/Launcher.smali`
- `launcher/AndroidManifest.xml`
- `launcher/original/AndroidManifest.xml`
- `tools/patch_weather_location_permission.py`

验证：

- `build.bat` 完整通过，输出 `build/launcher-signed.apk`。
- `aapt2 dump permissions` 确认最终 APK 同时包含 `INTERNET` 和 `ACCESS_COARSE_LOCATION`。
- 当前 ADB 未连接设备，定位授权、实际天气请求、厂商天气点击和图标动画仍需真机验收。

#### 【已废弃】动态日历尺寸与视觉中心统一
#### 文件夹打开时反复锁屏出现桌面宫格残影

日志确认每次锁屏收到 `ACTION_KEYGUARD_ON` 后，原版都会执行 `createInitUnlockAnimationEvent`，向 GL 场景准备一组桌面宫格节点；解锁阶段虽然检测到文件夹仍打开并跳过动画，但此前创建的准备节点没有被消费。多次锁屏后会积累多组节点，SurfaceView 重建时短暂覆盖在文件夹上，随后由应急解锁恢复清除。

修复：在 `ACTION_KEYGUARD_ON` 的动画准备入口同样执行文件夹/临时界面状态检查；文件夹打开时直接跳过初始化，不再创建待播放的桌面宫格节点。解锁阶段原有跳过保护继续保留。

涉及文件：

- `launcher/smali/com/smartisanos/launcher/ia.1.smali`

#### 应用分身图标跟随全局图标变化

问题：已开启的应用分身会继续显示数据库缓存的旧图标；切换改进版图标、图标包或图标大小后，只有主用户应用刷新。关闭再开启分身会删除并重建记录，所以此前只有这样才能更新。

修复：

- 全局图标刷新时枚举所有已启用的分身应用，并为对应 profile 用户发送原生 `EVENT_USER_PACKAGE_CHANGED`。
- 由原生更新链路重新读取主应用当前图标、合成分身面具并更新数据库，然后刷新桌面。
- Launcher 启动时在原有 `EVENT_USER_PACKAGE_ADDED` 后补发 `EVENT_USER_PACKAGE_CHANGED`，确保图标大小调整导致进程重启后，已有分身也会重建缓存，无需关闭再开启。
- 增加并发保护，避免启动阶段多次 bootstrap 并行刷新。
- 修复原版 `EVENT_USER_PACKAGE_CHANGED` 只接受并查询固定 `userId=10` 的限制；更新时改用事件携带的实际 profile userId，兼容 vivo 等设备动态分配的分身用户编号。此前事件在非 10 用户上会被直接丢弃，正是关闭改进版图标后分身仍保留旧图的根因。

涉及文件：

- `launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java`
- `launcher/smali/com/smartisanos/launcher/data/A.smali`

#### 【已废弃】跨厂商动态日历恢复、单层尺寸统一与分身面具微调

### 2026-06-30

#### 文件夹背景打包链路改为 assets 直读

问题与根因：

- 之前为普通主题文件夹背景补入了 `wallpaper_preview_*` / `wallpaper_light_gold` 图片文件，但当前主桌面工程是 `apktool + resources.arsc` 的半反编译结构，不是完整的 Android 源码资源工程。
- `build.bat` 构建主桌面时使用的是 `apktool b launcher`。这条链路会保留已有资源表，但不会像完整 `aapt2 link` 那样自动为后补的 drawable 生成稳定资源表项。
- 结果是：代码里主题 ID 到 `wallpaper_preview_*` 的名字映射存在，最终 APK 里也能看到这些字符串，但 `res/*wallpaper_preview_*` 实际图片并没有被打进主 APK 资源表。运行时 `Resources.getIdentifier(drawable)` 对透明主题还能命中老资源 `t_blur_background_folder`，普通主题却始终找不到，只能回退成默认黑色文件夹背景。

修复：

- 不再继续依赖主 APK 的 drawable 资源表补录文件夹背景，而是新增稳定资产目录 `launcher/assets/folder_theme_bg/`。
- 将普通主题所需的 `wallpaper_preview_*`、`wallpaper_light_gold` 文件复制到该 assets 目录中，由 APK 作为普通资产直接打包。
- 修改 `launcher/smali/com/smartisanos/launcher/e/s.smali`：
  - 新增私有方法 `th(String)`，优先从 `assets/folder_theme_bg/<imageName>.jpg/.png` 直接解码 bitmap。
  - `ug()` 保留原来的主题资源 / 本包资源 / 外部包资源查询顺序，但在本包 drawable 查询失败后，先走新的 assets 解码链路，再回落原版默认背景。
- 这样主桌面 APK 即使仍然不把新增 `wallpaper_preview_*` 注册进资源表，也不会影响普通主题文件夹背景跟随主题变化。

验证：

- `build.bat` 完整通过，新的 `build/launcher-signed.apk` 成功生成。
- 解包检查确认：最终 APK 中已包含 `assets/folder_theme_bg/wallpaper_preview_*.jpg/.png` 与 `assets/folder_theme_bg/wallpaper_light_gold.jpg`；同时 `res/*wallpaper_preview*` 仍为空，说明运行时已切换到新的 assets 读取链路，而不是继续误依赖资源表。
- 实机复测确认：文件夹背景现已随主题正常变化，不再只在透明主题正常、其他主题回退默认黑底。

防回归规则：

- 后续如果再补新的普通主题文件夹背景，不要只往 `launcher/res/drawable-*` 里塞图，然后假设 `Resources.getIdentifier()` 一定能取到。
- 这类“新增但原始资源表里没有登记”的背景图，应该优先视作运行时资产，补到 `assets/folder_theme_bg/`，并沿用 `s.ug() -> th()` 的读取链路。
- 若以后把主桌面切换成完整 `aapt2` 资源工程，再评估是否回归标准 drawable 资源表；在那之前，`assets/folder_theme_bg/` 是当前可信基线。

涉及文件：

- `launcher/smali/com/smartisanos/launcher/e/s.smali`
- `launcher/assets/folder_theme_bg/*`
- `build.bat`

#### v1.5.2 桌面显示、搜索手势与在线图标收口

> [!WARNING]
> **文件夹锁屏结论有一处历史遗漏。** 本节当时只在解锁阶段跳过动画，虽然解决了空 Context 崩溃，却没有阻止锁屏阶段反复创建待播放的桌面宫格节点。该遗漏已由 2026-07-01“文件夹打开时反复锁屏出现桌面宫格残影”修复：文件夹打开时，锁屏准备和解锁播放两端都必须跳过。

本轮在文件夹主题背景修复之外，完成以下调整并统一发布版本为 `v1.5.2 / 27`：

- **应用分身图标**：清理厂商 `getUserBadgedIcon`、旧微信专用角标和 Launcher 自绘面具可能重复叠加的路径。当前以主用户原始应用图标为底图，只绘制一层锤子风格面具，并调整面具轮廓、尺寸和位置；应用分身设置入口恢复使用原来的设置图标。
- **桌面与文件夹文字**：桌面标签略微增大，文件夹内标签保持更小的层级；两处使用一致的字体绘制基线。文件夹内标签显式清除阴影，修复文字重影和模糊。
- **搜索手势**：自绘搜索页采用完整 `DOWN / MOVE / UP` 位移、方向、时长和阈值判断，缩短有效下滑的触发距离；同时停用 SMEngine 中遗留的上滑搜索入口。当前只有明确的桌面下滑手势可以打开搜索页，上滑、点击和轻微抖动不应触发。
- **在线图标库**：取消旧锤子图标服务器依赖，按应用包名访问 `icons/drawable/<package>.png`。优先使用 Gitee 下载镜像，失败后回退 GitHub；下载在后台执行并写入应用私有缓存，包含失败缓存、文件大小与图片尺寸校验。仓库现有 2209 个图标及索引，在线资源不会增加 APK 体积。
- **跨品牌系统图标**：新增受系统应用身份约束的类别映射。不同厂商的相机、相册、浏览器、联系人、短信、邮件、计算器、文件管理、指南针、录音、音乐、视频、天气、便签、设置、安装器和 SIM 工具包可映射到统一的锤子在线图标；日历和时钟保留动态实现，第三方同名应用不参与映射。
- **系统图标识别补充**：部分厂商预装应用实际位于 data 分区，不能只依赖 `FLAG_SYSTEM`。现改为精确显示名称优先，并允许 Android、OPPO/realme、一加、小米、vivo、华为/荣耀和三星系统命名空间参与包名/Activity 识别；补齐软件商店、云服务、手机管家、钱包和语音助手。电话本/联系人优先于拨号包名判断，避免共用 `com.android.dialer` 一类包时被套成电话图标。缓存升级到 v3，清除旧的未命中结果。
- **在线图标自动刷新**：缓存写入采用 2 秒静默期合并刷新；刷新完成后不会永久锁死，后续下载批次仍可再次通知桌面，因此不再要求用户切换主题或重开“改进版图标”。刷新始终不阻塞首次桌面初始化。
- **跨 ROM 主题切换**：普通主题不再只把切换消息保存在进程静态字段后提前返回，而是先将主题 ID 写入 Launcher 两套私有配置并调用原版主题栈，再发送动画消息。这样 vivo/OriginOS 即使回收旧进程，新 Launcher 也能从持久化主题恢复。正常切换不再无条件追加第二次进程重建，避免连续播放两轮加载动画；透明主题等确实需要重启的路径仍会先安排精确 HOME PendingIntent，再结束旧进程。
- **电话本图标优先级**：厂商拨号器可能使用同一包提供拨号和电话本两个 Activity。联系人类别识别已提前到 package-wide packed icon 之前，显式自定义图标仍保持最高优先级；“电话本 / 联系人 / 通讯录”会直接使用联系人图标，不再被整包电话图标抢先覆盖。
- **电话/联系人最终渲染分流**：对照 maintained `97ff218`，图标包的三参数匹配禁止拨号 Activity 回退到联系人包级映射；桌面节点刷新同时传入 `ItemInfo.title`，按“桌面标题 > Activity > 包名”识别电话、拨号、电话本、联系人和通讯录，阻止异步刷新再次把电话本覆盖成电话。
- **原版解锁动画跨 ROM 触发**：确认动画控制器、9/12/16/20 宫格颜色资源和 `USER_PRESENT` 播放链路均属于 Launcher 主 APK。动态接收器监听标准 `SCREEN_OFF` 并映射到原版 `action_keyguard_on` 完成锁定预初始化；部分 ColorOS 可能不向默认 HOME 派发该广播，因此保留生命周期兜底。旧的“握手时间取消生命周期兜底”已废弃；当前唯一可信去重规则见 2026-07-18 的 `unlockGeneration` 记录。
- **解锁动画与临时桌面状态隔离**：修复更换主题后立即锁屏，解锁时再次执行主题切换动画的问题。主题应用原先同时通过原版主题栈和额外静态消息各派发一次 `MESSAGE_CHANGE_THEME`，第二条消息可能滞留到解锁后；现仅在原版主题栈失败时使用额外消息兜底，并在主题过渡保护期内跳过解锁场景重建。修复文件夹打开状态锁屏后解锁导致 GL 线程空上下文崩溃、Launcher 进程重启的问题；解锁前检测当前 FolderController，文件夹打开时保留现有场景，不初始化解锁动画。ADB 实测主题场景无重复 `MESSAGE_CHANGE_THEME`，文件夹场景 PID 不变且无 `FATAL EXCEPTION`，普通桌面锁屏仍正常播放解锁动画。
- **软件更新版本判断与弹窗排版**：更新检测由“版本字符串只要不相等就提示更新”改为语义版本比较，线上版本必须严格高于本地版本才显示下载提示，避免 v1.5.2 错误提示降级到 1.5.1。更新说明不再截断为 120 字；短内容弹窗按内容收紧，中等内容随正文增高，超过安全高度后正文进入可滚动区域。
- **首帧桥接闪退修正**：首次接入组件级加载时误把 `J`（ActivityProxy普通对象）直接作为 `Context` 传给Java桥，Smali可编译但ART会在运行时触发类型校验失败。现先调用 `J.getContext()` 获取真实Context后再调用 `loadIconForComponent()`。
- **改进版开关时序**：先更新所有应用的改进版选择状态并重载配置，再发送数据库与图标刷新，修复旧顺序先刷新、后写状态造成第一次开关仍显示旧图标的问题。
- **初始化阻塞与下载速度修复**：所有图标加载路径只同步读取内存和磁盘缓存，网络请求统一提交到 6 个有限并发任务的独立线程池；连接与读取超时缩短，单个镜像不可达时快速尝试备用地址。Launcher 模型线程不再等待网络超时。
- **版本维护**：新增 `tools/set_launcher_version.py`，用于同步文本 Manifest、设置页版本字符串和保留的二进制 Manifest，避免构建末尾注入旧清单导致最终 APK 版本回退。

文档核对结果：

- 旧记录中的“下滑 / 上滑搜索”是阶段性描述，已纠正为“下滑搜索”；当前上滑入口已明确禁用。
- 应用分身应以 2026-06-29 的“主用户原始图标 + 单层 Launcher 面具”为可信基线；更早关于 `getUserBadgedIcon` 或 QuickLaunchItem 主方案的记录仅代表历史尝试。
- 文件夹普通主题背景不是新增 drawable 资源表项，而是从 `assets/folder_theme_bg/` 直接读取；透明主题继续使用原版模糊背景链路。

验证要求：

- `build.bat` 完整构建后，使用 `aapt2 dump badging` 确认 `versionName='v1.5.2'`、`versionCode='27'`。
- 冷启动检查首帧图标尺寸；分别验证桌面下滑、上滑、点击和短距离抖动；检查普通主题与透明主题文件夹背景、文件夹标签清晰度及应用分身单面具显示。

### 2026-06-29

#### 应用分身落桌面与通知角标生命周期修复

问题与根因：

- 应用分身设置页能发现并开启微信分身，但原版 `EVENT_USER_PACKAGE_ADDED` 处理器读取参数中的真实 userId 后没有保存结果，后续仍把查询、`ItemInfo.userId` 和启动目标硬编码为 user 10。小米等使用 user 999/其他 profile 的分身因此不会写入桌面。
- 横扫清除只保存 suppressed 通知 key，没有把 `COUNTS` 中的持久化数字改为 0。Launcher 进程或桌面场景重建时，`BadgeBridge.replay()` 会重新广播旧数字。
- 企业微信等应用会复用同一个通知 key 更新内容。只按 key 抑制会把后续新通知永久当作旧通知，出现第一次显示、以后不再刷新的现象。
- 打开应用后，如果应用自身没有撤销通知，监听器仍会把活动通知重新统计出来；原版桌面期望从桌面点击应用时先清除该应用当前角标。

修复：

- 分身数据库事件完整保留设置页发现的真实 userId，查询对应用户、写入 `ItemInfo.userId` 并通过 `LauncherApps.startMainActivity(component, realUserHandle, ...)` 启动；反射 `startActivityAsUser` 只保留为旧 ROM 兜底。
- OPPO Android 12 复测表明，仅修正原版 `EVENT_USER_PACKAGE_ADDED` 的 userId 仍不可靠：该事件需要再次按目标用户查询 `ResolveInfo`，部分 OEM 对第三方 Launcher 返回空结果，因此开关已开启但桌面没有新增项。
- 对照 `rianlu/smartisan-launcher-maintained` 的 `ProfileAppsSettingsActivity` 后，分身开关改为直接安装/卸载 profile 快捷方式：快捷方式目标是 Launcher 内 `StartActivityForSearch`，URI 保存 `package / activity / profileSerial`，点击时再由 `LauncherApps` 启动真实 profile。该路径不依赖第二次 Launcher 数据扫描。
- 当前 v26 基线的快捷方式处理器原本只允许微信/支付宝等少量包且只把 user 10 写入 `ItemInfo`；已调整为接受设置页明确创建的 profile 快捷方式，并从 `extra_uid` 还原任意正数 userId。已启用分身在 Launcher 启动同步时也会补发快捷方式安装，升级 APK 后无需先关闭再开启开关。
- 所有 `userId > 0` 的分身图标继续统一经过 `doppelgangerIconBytes()`，叠加同一套原版面具标记，不限定微信或 user 10。
- 通知抑制标识改成 `notification key + postTime`，只屏蔽被清除的那一轮通知；同 key 的后续新发布/更新会重新计数。
- 横扫和应用点击清除时同步保存 `COUNTS=0` 并立即广播 0，Launcher 重建后不会重放旧数字。
- 桌面/搜索启动第三方应用前调用 `BadgeBridge.onPackageLaunched()` 清除该应用当前角标；通知真正移除或后续新通知到达时，监听器继续按实时状态刷新。
- `BadgeBridge.replay()` 在已有通知使用权时主动请求重新绑定监听服务，改善强行停止、覆盖安装或 ROM 后台限制解除后监听器没有及时恢复的问题。

验证与限制：

- `build.bat` 完整通过，BlackBerry 用户 0 真机覆盖安装与 Launcher 冷启动成功，无 `FATAL EXCEPTION` / `VerifyError`。
- 当前连接设备没有第二 profile，微信分身写入、面具显示和正确 profile 启动仍需在原问题手机复测。
- BlackBerry 日志显示该 ROM 在应用处于 restricted/force-stop 状态时会拒绝绑定通知监听；启动 Launcher 后通过主动 rebind 恢复。其他 ROM 仍需确保已授予通知使用权，并避免系统长期冻结 Launcher。

涉及文件：

- `launcher/smali/com/smartisanos/launcher/data/A.smali`
- `launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java`
- `launcher/tools/java/com/smartisanos/launcher/badge/BadgeBridge.java`
- `launcher/tools/java/com/smartisanos/launcher/badge/SmartisanBadgeListenerService.java`

#### 应用分身诊断日志与角标隐藏开关修复

文档校对补充（当前可信结论）：

- 本仓库当前关于“应用分身”的可信修复基线，应以 `2026-06-28：通用应用分身管理、首次加载和搜索启动` 与本节为准；更早的 `2026-06-06` 记录只可作为历史背景，不可再直接当成当前实现说明。
- 历史记录里曾出现过“分身开关改为直接安装 / 卸载 profile 快捷方式”的阶段性方案，但该方案随后已被本节上方记录明确撤销；当前正式链路仍是恢复并修正原版 `EVENT_USER_PACKAGE_ADDED / REMOVED` 应用项数据库路径，而不是长期依赖 `QuickLaunchItem` 模拟分身。
- 历史记录里还写过“分身图标会走 `PackageManager.getUserBadgedIcon` 和当前工程的面具绘制兜底”。这在当时是阶段性描述，但对 OPPO / ColorOS 等 ROM 会产生厂商角标 + 锤子面具叠加、甚至与旧微信专用 `wechat_shortcut` 叠加的双面具问题。当前可信规则是：优先读取主用户原始 Activity / Application 图标，只叠加一层锤子风格面具，不再把 `getUserBadgedIcon` 当作当前标准链路说明。
- 防回归时必须同时检查三条链路是否只保留一套面具来源：`LauncherApps/桌面应用项生成`、`ItemInfo.iconData -> doppelgangerIconBytes()`、`快捷方式/搜索图标生成`。如果其中两条以上同时叠加面具，就会再次出现双面具或厂商角标混入。

- 根据 OPPO user 999 诊断日志撤销“用 QuickLaunchItem 模拟分身”的主方案：日志显示快捷方式安装/卸载调用虽然返回成功，但点击从未进入 `PROFILE_LAUNCH`，且旧条目因 package/user/shortcutId 不同无法被新版删除。恢复原版 `EVENT_USER_PACKAGE_ADDED/REMOVED` 应用项链路，只在用户明确启用或已启用项的轻量恢复阶段触发，不恢复首次启动全量扫描。
- 原版新增分身处理器已支持从事件参数读取动态 userId；本轮继续将删除处理器从固定 user 10 改为读取事件中的 userId，因此 OPPO 999、小米/工作资料等其他 profile 均按真实用户删除。
- 启用/关闭分身前会清理历史版本创建的 `com.tencent.mm`/Launcher 包名、user -1/0/真实 profile user 下的无效快捷方式；随后创建的是 `itemType=应用`、真实 userId 的桌面项。图标走普通 user 0 的锤子主题图标链路后叠加面具，点击走 `LauncherApps.startMainActivity(component, profile)` 启动系统现有分身。
- 对照 `rianlu/smartisan-launcher-maintained`：其设置页通过 `LauncherApps.getProfiles/getActivityList` 发现分身，并以 `componentName#profileSerial`/profile serial 区分身份；当前移植保留相同的动态 profile 发现思想，但复用本版本已经存在的原版 user-package 应用项数据库链路，以匹配当前 `QuickLaunchItem`/DatabaseUpdater 数据结构。
- 修复“隐藏图标上的角标”仍显示：原版 `data.O` 仍直接读取 `Settings.System.launcher_hide_badge`，普通 APK 无系统设置写权限，重新加载时会把隐藏状态覆盖为 false。两个原版读取点均改用 `LauncherSettingBridge.readBool`，统一读取应用内持久化设置；切换后同时调用 `Eb.ii()` 更新已有 SceneNode，并在图标刷新结束后再次同步，确保现有角标立即消失而非只影响新建图标。
- OPPO 实机截图进一步确认：旧快捷方式错误地把桌面自身的中转 Activity 标记为 user 999，导致系统尝试在未安装 Launcher 的分身用户中启动中转页，点击无响应。现改为快捷方式归属 user 0，由中转页再通过 `LauncherApps.startMainActivity` 启动真实 user 999 应用，并增加 `startActivityAsUser` 反射兜底及启动结果日志。
- 分身图标不再使用 ColorOS 已经套过圆框和厂商分身角标的 `LauncherActivityInfo` 图标；优先读取 user 0 的原始 Activity/Application 图标，只叠加锤子面具角标。安装正确快捷方式前会先清理旧版无效条目。
- OPPO ADB 日志显示通知监听授权后曾发生 `binding died`，打开系统设置只是间接触发重新绑定。Launcher 每次恢复时现主动检查授权、请求 `NotificationListenerService.requestRebind` 并重放角标，无需再次点击“前往设置”。
- 分身诊断新增 profile 数量、userId、serial、LauncherActivityInfo 数量、组件名、开关状态、快捷方式 URI、直接处理/广播兜底结果及异常记录。
- 分身快捷方式安装/删除优先在桌面进程内反射调用原版 `com.smartisanos.launcher.a.L` 处理器，避免 OPPO 等系统拦截或延迟自发快捷方式广播；直接调用失败时仍保留定向广播兜底。
- “隐藏图标上的角标”不再只保存设置值：切换时直接同步 `Constants.SHOW_MESSAGE_FLAG = !hidden` 并刷新桌面，Launcher 每次恢复前也重新应用持久化值，避免进程重建后失效。
- 验证：`build.bat` 完整通过，输出 `build/launcher-signed.apk`；当前没有连接 ADB 设备，OPPO 分身和角标交互需真机验证。

### 2026-06-28

#### 普通 Android 通知角标与横扫清除

- 原版机制确认：Smartisan 系统通过 `com.smartisanos.launcher.new_message` 携带包名、组件、UID 和计数，Launcher 将其写入 `ItemInfo.messagesNumber`，再由 `g.qb(count)` 生成数字纹理；文件夹汇总和横扫动画均属于 Launcher 内部能力，并不依赖 Smartisan ROM。
- 新增 `SmartisanBadgeListenerService`，使用 Android 公共 `NotificationListenerService` API 监听通知新增、更新和移除，并在连接时通过 `getActiveNotifications()` 全量恢复。按 `packageName + uid` 隔离主用户/分身，按通知 key 去重，过滤 Launcher 自身、ongoing 通知、禁用 badge 的通知渠道和有子通知时的 group summary。
- 计数优先使用通知提供的 `Notification.number`，否则每条有效通知计 1，最高限制 999；结果转换为原版 `new_message` 广播，因此原版绘制、数据库、文件夹汇总和隐藏角标开关无需重写。
- 角标快照写入 Launcher 私有偏好，Launcher `onResume()` 会重放，解决通知监听服务已常驻但桌面动态广播接收器稍后才注册造成的计数丢失。
- 强迫症选项在“隐藏图标上的角标”下新增“紧贴屏幕横扫清除角标”开关，并增加“通知使用权”入口；首次开启横扫且尚未授权时也会跳转系统授权页。通知使用权必须由用户手动授予，应用不能静默获取。
- 横扫继续执行原版 `Yh() -> wx()` 动画和本地数据库归零，同时记录当时存在的通知 key。旧通知继续留在通知栏也不会马上把角标顶回来；只有出现新的通知 key 才重新计数。横扫不会擅自删除系统通知。
- 文本 Manifest 和最终注入 APK 的二进制 Manifest 均注册通知监听服务；新增 `tools/patch_badge_service_manifest.py` 用于向保留的 AXML 清单安全追加服务节点，避免只改文本 Manifest 导致最终 APK 丢失服务。

验证：

- `build.bat` 完整通过，Java 监听服务编译进 `classes2.dex`，APK 使用 v1/v2/v3 签名。
- `aapt2 dump xmltree build/launcher-signed.apk --file AndroidManifest.xml` 确认最终二进制清单包含 `SmartisanBadgeListenerService`、`BIND_NOTIFICATION_LISTENER_SERVICE` 和正确的 service action。
- 当前连接设备覆盖安装成功；`dumpsys package` 确认系统识别通知监听 service intent filter；真机进入“强迫症选项”确认“隐藏图标上的角标”下方显示“紧贴屏幕横扫清除角标”。
- 仍需用户在目标机手动授予通知使用权后，用微信、短信等实际通知完成数字变化、通知移除、文件夹汇总和横扫后新通知恢复四项动态验收。

#### Moto G100 Android 16 启动兼容、页面锁搜索刷新与 v1.5.1

问题与根因：

- Moto G100 升级 Android 16 后 Launcher 无法正常启动。`ja` 构造阶段会实例化继承隐藏接口 `android.app.IActivityObserver$Stub` 的观察器；该 Smartisan 私有系统接口在普通 Android 16 ROM 上不可用，应用会在初始化阶段失败。
- 搜索启动此前在无法从 favorites 数据库确认 App 所属页面时直接按“已锁定”处理。取消页面锁后页面映射可能暂时查不到，因此搜索打开仍错误弹出密码页。
- 文本 Manifest 已写 `v1.5.1 / 26`，但构建末尾注入的二进制 Manifest 和设置页版本仍停留在 `v1.4.9 / 24`，导致最终 APK 版本被覆盖。

修复：

- 在 `launcher`、`clean_launcher`、`clean_launcher_raw` 三份 `ja.1.smali` 中不再创建 `IActivityObserver` 实例，将 `nh` 初始化为 `null`，避开 Android 16 对已移除/不可访问隐藏接口的初始化失败；保留其余广播与桌面初始化流程。
- 搜索启动不再依赖 favorites 查询失败后的“默认锁定”兜底，而是从原版页面容器 `fa.Ua(packageName)` 实时取得 App 单元格，经 `g.Af()` 找到所属页面，再用原版 `M.On()` 判断页面当前是否锁定。原版状态中 `M.Nn()` 是隐藏页（`yI == 1`），`M.On()` 才是锁定页（`yI == 2`）；原版页面点击也只有 `On()` 分支会调用 `Zp()` 验证密码。只有明确处在锁定页面时进入密码页，解除页面锁后下一次搜索启动会直接读取新状态并放行。
- 版本三个写入点统一为 `v1.5.1 / 26`，并在构建后通过 `aapt2 dump badging` 核对最终 APK。
- `.gitignore` 放行根目录 `build` 和本次新增的 maintained 彩色隐私密码锁图标、黑色键盘图片，确保这些产物可以提交到 GitHub，同时避免把其余历史图片资源全部误列为新文件。

验证：

- `build.bat` 完整构建、资源编译和签名通过。
- `aapt2 dump badging build\launcher-signed.apk` 确认 `versionCode='26'`、`versionName='v1.5.1'`、`compileSdkVersion='36'`、`targetSdkVersion='28'`。
- 2026-06-28 用户安装到真机后完成最终回归：锁住板块时，从自绘搜索结果点击该板块内 App 会进入数字密码页；解除板块锁后，再从搜索点击同一 App 会直接启动，不再误弹密码。两条路径均确认正常。

防回归规则：

- 不要把 `M.Nn()` 当作页面锁状态；它表示隐藏页。页面锁必须检查 `M.On()`。
- 不要恢复“找不到 App 页面就默认要求密码”的逻辑，否则解除锁、数据库尚未同步或桌面未完全初始化时会误拦普通搜索启动。
- 不要让搜索结果缓存一个独立的 `locked` 布尔值。每次点击搜索结果时都应重新执行 `fa.Ua(packageName) -> g.Af() -> M.On()`，以当前桌面页面对象为准。
- 不要在 `ConfirmPasswordActivity` 中判断 App 是否属于锁定页面；该 Activity 只负责密码输入和验证，是否需要进入它由搜索启动入口决定。
- 修改这段链路后必须同时回归两种状态：`锁住板块 -> 搜索打开 -> 必须验证密码`，以及 `解除板块锁 -> 搜索打开 -> 必须直接启动`。

涉及文件：

- `launcher/smali/com/smartisanos/launcher/ja.1.smali`
- `clean_launcher/smali/com/smartisanos/launcher/ja.1.smali`
- `clean_launcher_raw/smali/com/smartisanos/launcher/ja.1.smali`
- `launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java`
- `launcher/AndroidManifest.xml`
- `launcher/original/AndroidManifest.xml`
- `launcher/tools/maintained_settings_res/res/values/strings.xml`
- `.gitignore`

#### 通用应用分身管理、首次加载和搜索启动

问题与根因：

- 工程原先已有零散的 `userId`、分身角标和 `LauncherApps` 兼容代码，但补录任务首次延迟 12 秒，而且没有稳定参与桌面模型第一次扫描。首轮桌面加载完成后才把分身写入数据库，因此微信分身通常要完全退出 Launcher、第二次启动才显示。
- 旧实现混用 `UserManager.getUserProfiles()`、常见用户 ID 猜测和反射构造 `UserHandle(id)`；搜索又把 `LauncherActivityInfo` 转成 `ResolveInfo` 后从 UID 反推用户。不同 ROM 的分身用户 ID 并不固定，容易只对微信或某个厂商的 user 10/999 偶然有效。
- 原版搜索 URI 只保存包名和组件名，主应用与分身组件相同时无法表达目标 profile；直接 `startActivity()` 会打开主应用。

实现：

- 统一通过 `LauncherApps.getProfiles()` 获取系统实际暴露的 profile，再对每个非当前用户调用 `LauncherApps.getActivityList(null, userHandle)`。没有写死微信、淘宝、京东、拼多多、支付宝或 QQ 包名，系统暴露的所有 Launcher Activity 都可进入同一逻辑。
- 分身记录同时保留 `ComponentName`、真实 `UserHandle`、Launcher 数据库使用的 `userId` 和 `UserManager.getSerialNumberForUser()` 返回的 profile serial。设置偏好和搜索历史键使用 `serial + component`，主应用与分身不会因包名/组件名相同而覆盖。
- 分身改为默认全部关闭。没有任何分身被用户启用时，桌面模型直接返回普通应用列表，不调用 `LauncherApps.getProfiles()`，避免为默认隐藏的功能增加冷启动等待。只有进入“应用分身”设置页时才枚举系统 profile。
- 桌面设置新增“应用分身”入口。页面异步列出所有 profile 应用并提供默认关闭的开关；打开时保存 `serial + component` 状态，发送原版用户包新增/变更事件并刷新桌面。启用过分身后，后续桌面启动才会参与 profile 枚举，并保留立即、2 秒、8 秒重试。关闭时发送 `EVENT_USER_PACKAGE_REMOVED` 并刷新数据库、桌面和搜索。没有额外 profile 或接口不可用时显示正常提示。
- 当前自绘搜索直接从 profile 枚举追加分身结果，不依赖桌面数据库是否已完成首轮补录。分身搜索项保存真实 `UserHandle` 和 serial，点击后使用 `LauncherApps.startMainActivity(componentName, userHandle, null, null)`；普通应用仍使用原来的 `Activity.startActivity()`。
- 原版 `SearchProvider` 生成分身结果 URI 时，根据 `ItemInfo.userId` 找到对应 profile 并追加第三段 serial；`StartActivityForSearch` 优先解析第三段，通过 `UserManager.getUserForSerialNumber()` 还原 `UserHandle` 后调用 `LauncherApps.startMainActivity()`。两段 URI 的普通应用保持原启动方式。
- 页面锁搜索判断继续按 `ItemInfo.userId` 区分同包主应用和分身。分身位于锁定板块时，密码验证完成后也使用保存的 profile serial 启动真正的分身，不会落回主应用。

防回归规则：

- 不得按 `packageName + componentName` 单独去重分身，唯一键必须包含 profile serial 或真实用户标识。
- 不得用固定 user 10/999/888 列表代替 `LauncherApps.getProfiles()`；固定 ID 只能作为旧 ROM 兼容兜底，不能作为主发现路径。
- 分身启动必须使用 `LauncherApps.startMainActivity()` 和发现时保存的 `UserHandle`。不要用普通 `startActivity()`，也不要只依赖反射构造 `UserHandle`。
- 不得让默认关闭状态在桌面冷启动时扫描 profile；只有至少一个 `serial + component` 被明确启用后，桌面模型才允许枚举和短延时重试。
- 设置开关、桌面数据库、当前自绘搜索和旧 SearchProvider URI 必须使用同一份启用状态；关闭分身后不能只隐藏设置行或只删除桌面图标。
- 修改页面锁链路时必须分别验证主应用和同包分身，不能因为包名相同而共用错误的页面锁状态。

验证：

- `build.bat` 完整通过，包括 maintained 设置资源、apktool smali、Java/classes2.dex、zipalign 和签名。
- 当前连接的 BlackBerry 设备覆盖安装成功；该设备只有用户 0，可确认无 profile 调用不会导致安装或 Launcher 启动崩溃。
- 初版 SearchProvider serial 补丁曾错误复用仍保存 `ResolveInfo` 的 `v10`，导致 Android Verifier 报 `VerifyError`，Launcher 在安装 ContentProvider 阶段无法启动。已改用后续会被重新赋值的 `v12` 暂存 `userId`，保留 `v10` 的引用类型；此类 smali 修改必须通过真机冷启动验证，不能只以 apktool 构建成功作为验收。
- 修正后通过 ADB 覆盖安装并执行 `am force-stop` 后冷启动 `.Launcher`：Activity 启动成功、Launcher 进程持续存活且保持前台，logcat 中无 `FATAL EXCEPTION`、`VerifyError` 或 Launcher 崩溃记录。
- Android 16 多 profile 真机仍需完成最终动态验收：微信、淘宝、京东、拼多多首次发现，设置开关即时增删，搜索命中并打开正确分身，以及主应用/分身共存。

涉及文件：

- `launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java`
- `launcher/smali/com/smartisanos/launcher/data/SearchProvider.smali`
- `launcher/smali/com/smartisanos/launcher/StartActivityForSearch.smali`
- `launcher/tools/maintained_settings_res/res/layout/setting_main.xml`
- `launcher/tools/maintained_settings_res/res/values/strings.xml`
- `launcher/tools/maintained_settings_res/res/values-zh-rCN/strings.xml`

#### 跨 ROM 安装、首次启动与下滑搜索性能收口

问题与根因：

- 小米 / HyperOS 安装返回 `-112 (INSTALL_FAILED_DUPLICATE_PERMISSION)`。二进制 Manifest 仍声明 7 个原版锤子私有权限，其中一个错误占用 `android.permission.*` 命名空间；手机上存在同名权限但签名不同时会在安装阶段直接拒绝 APK。
- 新安装没有保存过 `ro.build.date.utc`，原版逻辑把空值与当前系统构建时间不一致误判为 OTA。首次建库生成图标后，OTA 路径立即删除全部图标和阴影缓存并再次生成，造成重复 I/O、解码和数据库写入。
- 原版固定 user 10 的分身事件路径会在未启用任何分身时逐包查询第二用户，普通 ROM 上查询全部失败却仍消耗十几秒。
- 自绘搜索页此前在 `setContentView()` 前同步枚举所有 Launcher Activity 并读取全部名称、图标和 profile，导致页面本身延迟数秒；改为异步后，常用图标仍要等待完整索引完成才一起显示。

修复：

- 7 个应用内部 signature 权限统一迁移到 `com.ranhf.smartisanlauncher.permission.*`，同步文本 Manifest、保留的二进制 Manifest、Provider 权限引用、Smali 常量和预装完成广播权限。新增 `tools/patch_manifest_internal_permissions.py`，避免以后重新处理二进制清单时恢复冲突权限。
- 首次建库与 OTA 刷新设为互斥：首次安装只生成一次图标；已有数据库且系统构建时间确实变化时仍执行 OTA 缓存刷新。
- 原版分身包事件增加已启用记录与真实第二 profile 双重门禁；没有用户明确启用的分身时不枚举 profile，也不进入固定 user 10 的逐包处理。
- 搜索页先绘制搜索框并弹出键盘，完整应用索引在 `launcher-search-loader` 后台线程生成。
- 最终取消搜索框下方的常用应用图标区，避免搜索页首帧后再补图标造成明显的二次跳变；完整应用、历史和已启用分身索引仍在后台生成，用户输入搜索时继续覆盖全部应用。
- 强迫症选项里的通知使用权提示把中文“前往设置”/英文“Tap to configure”单独改为蓝色下划线链接样式，并把跳转范围严格限制在链接文字本身。
- 通知使用权提示移动到“隐藏图标上的角标”开关正下方；底部上扫说明继续跟随“紧贴屏幕横扫清除角标”开关，避免权限说明与手势说明归属混淆。
- 设置页交互按控件类型收口：所有 `SettingItemSwitch` 行（含动态创建的透明主题、壁纸模糊、应用分身和改进版图标）取消整行点击，只触摸右侧 `SwitchEx` 滑块才切换；通知权限只点击蓝色下划线“前往设置”文字才跳转；“图标包”“桌面图标大小”等带右箭头的导航标签保持整行任意位置可点击。
- 安装兼容静态审计补齐 5 个旧组件的显式 `android:exported="true"`：Launcher、PinShortcutActivity、LauncherReceiver、DataSyncReceiver、DataDumpReceiver。文本与二进制 Manifest 已同步，避免部分 HyperOS / OriginOS / Android 16 安装器把缺省 exported 判为 `MANIFEST_MALFORMED`。
- “检查更新”结果与新版本确认弹窗改为接近屏幕可用宽度的锤子式圆角卡片：标题居中，版本信息和更新说明统一左对齐，正文增加左右留白与行距，底部继续使用细分割线和分栏按钮；普通确认弹窗保持原尺寸与对齐方式。

验证：

- `build.bat` 完整通过；APK 的 v1/v2/v3 签名和 16KB zipalign 检查通过。
- BlackBerry 真机覆盖安装成功；冷启动 Activity 显示约 `1.284s`，含进程拉起总计约 `2.235s`，无分身全包扫描和 `FATAL EXCEPTION`。
- 自绘搜索 Activity 冷启动显示约 `254ms`；完整索引继续后台加载，不阻塞搜索页首帧。
- 最终 APK 确认 `minSdk=23 / targetSdk=28 / compileSdk=36`，包含 arm64-v8a、armeabi-v7a、armeabi、x86、x86_64；自定义权限已使用独有命名空间，带 intent-filter 的旧组件已显式 exported。目前静态审计未发现新的通用安装阻断项。
- 小米 17 的 `-112` 修复需在对应设备重新安装最终 APK 完成最终确认；若仍失败，应使用 `adb install` 保存 PackageManager 返回的冲突权限或冲突包名。

涉及文件：

- `launcher/AndroidManifest.xml`
- `launcher/original/AndroidManifest.xml`
- `launcher/smali/com/smartisanos/launcher/data/A.smali`
- `launcher/smali/com/smartisanos/launcher/ja.1.smali`
- `launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java`
- `tools/patch_manifest_internal_permissions.py`
- `tools/patch_manifest_exported_components.py`

### 2026-06-26

#### 隐私密码页宽度、黑色键盘和搜索解锁链路

- 隐私密码页改为复用主设置项的全宽九宫格背景尺度，“修改密码”不再额外套左右内容边距；底部“关闭密码”保持红色操作按钮，但按主设置卡片可见边缘对齐，并继续和“修改密码”同屏显示。
- 对照 maintained 版搜索页 T9 键盘确认原版按下反馈由 action-down 状态触发并重绘。内置数字键盘现在在 `ACTION_DOWN` 立即 `setPressed(true)`、输入数字、播放点击音和触感反馈，在 `ACTION_UP/CANCEL` 清除 pressed，避免之前触摸事件被消费后 selector 没有按下态。
- 浅色隐私密码验证页继续使用 maintained 设置资源里的 `btn_0_classic_normal` 到 `btn_9_classic_normal`、删除和收起按钮资源；黑色板块锁页因没有对应黑色数字键资源，改为同一套键位逻辑的黑底白字按钮，并提供更明显的按下亮态。
- 搜索结果启动锁定板块内 App 时先进入 Launcher 内置黑色数字密码页，验证成功后再启动目标 App；直接点锁定板块的 requestCode 21 也统一走同一套黑色密码页，取消后会结束本次验证状态，避免再次点击无反应。
- 追加修正：首次设置页面密码的 requestCode 20 也改为启动 `ConfirmPasswordActivity` 的全屏黑色数字键盘，不再弹旧 AlertDialog；黑色键盘资源由白色锤子 `btn_*_classic_normal.9.png` 保留九宫格边框后反色生成 `btn_*_classic_dark.9.png`；由于按下视觉态在当前兼容层里观感仍不够跟手，黑白键盘均取消视觉 pressed 变色，只保留按下即输入、点击音和触感反馈。
- 追加修正：隐私密码页的分组标题和“修改密码”文字左边距统一回 maintained 设置页 `setting_item_text_left` 的 30dp 体系；“关闭密码”按钮高度改为 72dp，左右边缘按设置项可见边缘重新对齐。设置首页“隐私密码”图标由通用齿轮改为基于页面锁动画素材制作的灰银锁图标 `privacy_password_lock_icon.png`，保持锤子设置页的拟物灰度风格。
- 追加修正：主设置页 Java 绑定层此前仍把“隐私密码”入口图标覆盖为 `launcher_settings`，现同步改为 `privacy_password_lock_icon`；“关闭密码”按钮高度从 72dp 收回 64dp，使可见高度更接近上方“修改密码”项。新增 `docs/development/CLEANUP.md`，记录可删除/需谨慎处理的构建产物、反编译目录和被 `.gitignore` 忽略的新 PNG 资源。
- 追加修正：`privacy_password_lock_icon.png` 从灰银系统感图标改为蓝绿色底座、金色锁体、红色提示点的彩色拟物锁图标，更贴近设置首页其他锤子风格彩色图标。角标链路对照：当前 original-port 仍有旧版 `com.smartisanos.launcher.P` 广播接收 `com.smartisanos.launcher.new_message` 并读取 `extra_packagename / extra_componentname / extra_uid / extra_message_count`，再调用 `Aa.a(..., count)` 更新 `ItemInfo.messagesNumber`；maintained 原版 `LauncherModel` 额外兼容 `badge_count_*`、HTC、Sony 等第三方角标字段，`ApplicationProxy` 还注册 `launcher_hide_badge / launcher_badge_swipe_clean` 观察者，通过 `LauncherPreferences` 刷新 `Constants.SHOW_MESSAGE_FLAG / ENABLE_SWEEP_MESSAGE_FLAG`，`Cell.updateFlagMessageNumber()` 根据计数创建或清除 `mFlagMessageRect`。本轮只记录差异，未改角标逻辑。
- 验证：`build.bat` 已通过 maintained 设置资源构建、apktool smali、Java 兼容层编译和签名，输出 `build\launcher-signed.apk`。

### 2026-06-25

#### 日历编辑页灰度最终回归记录

- 可工作的灰度基线是 `3b973b589338b963d5b39a82e1937922577b3f4e`。该版本进入桌面编辑页后，点击底部 Dock 左下齿轮进入“已选择 [0/12] 个应用程序”页，日历会和其他图标一样走静态图层灰度。
- 后续尝试在 `view/a/g.1.smali` 新增 `showCalendarActiveIconOnly()`、或在静态纹理绑定后按 `ItemInfo.Te()` 隐藏日历静态前景，会破坏这条灰度链路：灰度静态层被隐藏，彩色活动日历层留在最上面，导致设置页日历始终红白彩色。
- 最终方案：`view/a/g.1.smali`、`ItemInfo.smali` 的日历图层状态回到 `3b973b5` 行为；只在 `view/activeicon/m.smali` 覆盖 `d([B)` / `o(Bitmap)`，把静态图标替换为合成日历 bitmap，并同步日期矩形比例。这样普通桌面没有双层错位，编辑设置页仍能正常变灰。
- 本轮核对：文件夹对齐相关 `LayoutPropertyAdapter.centerFolderPreview()`、`folder_icon_center_offset_*`、打开文件夹只作用文件夹页的规则未被修改；图标大小相关 `normalizeLauncherIcon()`、`normalizeImprovedIcon()`、`maybeApplyLauncherIconSize()`、50%-150% 保存后完整重启 Launcher 的链路仍保留。日历回退时误带出的 `e/s.smali` 图标 override normalize 调用已补回。
- 毛玻璃主题已改为只保留 `smartisan_theme_aero` 作为透明壁纸主题，移除白雾主题入口和资源引用；毛玻璃桌面与编辑页文字已恢复为原版风格白色文字效果。
- 透明主题切换已从自定义运行时旁路改回原版方向：透明模式写入 `launcher_grid_theme` 的 0/1，普通主题 ID 只写入 `launcher_theme`；透明主题包只用于资源注册，不再把 `smartisan_theme_trans` 当普通主题写入或送入普通主题切换队列，避免关闭透明主题后无法恢复上一主题。
- 透明主题安装包使用 `build\theme-trans-signed.apk`，安装后包名为 `com.smartisanos.launcher.theme.trans`，`minSdkVersion=23`、`targetSdkVersion=28`，最终 APK 元数据已更新为 `compileSdkVersion=36`、`platformBuildVersionName=16`，用于普通 Android / Android 15 / Android 16 安装；`original_apks\com.smartisanos.launcher.theme.trans.apk` 是原始参考包，`targetSdkVersion=17`，不要作为新系统安装包。
- 透明主题开启后只能使用默认翻页动画：主设置页隐藏“桌面翻页动画”入口，翻页动画读写被钳制为 `0`，避免透明主题资源链路和非默认翻页动画混用。
- 普通不透明主题下主设置页不再显示“桌面壁纸”入口；只有毛玻璃主题 `smartisan_theme_aero` 或开启透明主题时才显示。透明主题仍隐藏“桌面主题”和“桌面翻页动画”，只保留“桌面壁纸”和“应用图标”，避免普通主题误进入只对壁纸主题生效的设置。
- 透明主题开关状态读取改为私有 prefs 优先、系统 Settings 兜底，解决普通 Android 上系统 Settings 旧值覆盖设置页开关，导致返回设置页仍显示关闭的问题。
- 修复透明主题开启后仍排队 `MESSAGE_CHANGE_THEME smartisan_theme_black` 的问题；开启透明主题只写透明覆盖状态并重启 / 刷新桌面，关闭透明主题时才恢复上一普通主题。
- 修复原版主题管理器 `X.ca()` 清空主题表后 `smartisan_theme_trans` 丢失的问题：在 `X.da()` 选择当前主题前重新注册透明主题包，避免透明状态回落到黑主题导致黑底、黑宫格或 Dock 混用。
- 透明主题开关和主题列表透明主题入口统一改为写入透明状态后重新触发桌面初始化，让 `O.V()`、`Constants.isTransparentTheme` 和 `X.va()` 重新选择资源，避免设置页开关状态正确但桌面仍停留在上一套主题资源。
- 透明主题开关确认必须完整重启 Launcher 才能稳定生效：普通 `J.a(theme, theme_changing)` 能拿到 `smartisan_theme_trans`，但不会完整重建透明桌面的壁纸 / 网格层；当前改为显示加载动画后重启桌面，避免仅退出设置页导致黑主题资源残留。
- 透明主题重启链路新增跨进程 loading pending 标记：设置页写入标记后杀进程重启，新 Launcher 进程在 `onCreate`、`J.b()` 初始化前显示加载层，等桌面渲染帧稳定后再关闭，避免切换时裸露黑屏 / 壁纸中间态。
- 透明主题壁纸取图改回原版优先系统壁纸 drawable；当 `WallpaperManagerSmt` / `WallpaperManager.getDrawable()` 在普通 Android 返回 null 时，再依次尝试 `peekDrawable()`、`getFastDrawable()`，最后才使用本地壁纸副本按屏幕比例中心裁剪，避免整图拉伸导致壁纸看起来被压缩。
- “桌面壁纸模糊效果”改回原版刷新方式：写入 `original_launcher_wallpaper_blur_on` 的 0/1，更新 `Constants.isTransWallpaperBlur` 后调用 `Eb.lh()` 重建 `t_blur_background`，不再走完整透明主题重载，修复打开模糊开关后背景变黑的问题。
- `ua.i(context)` 已加入普通 Android 兼容读取，优先从 launcher 私有 prefs 读取 `original_launcher_wallpaper_blur_on`，避免无 `WRITE_SECURE_SETTINGS` 时原版只读 `Settings.Global` 导致状态丢失。
- 对照原版确认：毛玻璃 / 透明壁纸主题下应用文字颜色由壁纸明暗决定，原版通过 `Constants.initGaussianDarkLight()` 在普通资源和 `_light` 后缀资源之间切换，不是按时间变化。
- 透明主题 / 毛玻璃主题下，状态栏文字和桌面应用文字已恢复为按壁纸明暗自动切换：
  - 根因一：`Constants.initByTheme()` 调用 `initGaussianDarkLight()` 后已经根据壁纸算出 `sGaussianResSuffix="_light"`，但后续又把 `sGaussianResSuffix` 清空为 `""`，导致浅色壁纸无法继续加载原版 `_light` 应用文字资源，应用名仍显示白字。
  - 根因二：状态栏颜色虽然已经通过原版 `status_bar_icon_color(_light)` 资源传给 `ua.setSystemUiDecoration()`，但普通 Android / Android 6+ 还需要同步 `View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR`，否则系统状态栏文字可能仍按旧颜色显示。
  - 修复方式：保留 `initGaussianDarkLight()` 算出的 `sGaussianResSuffix`，让 `Mc.o(theme)` / `Constants.initGaussianTheme()` 正常进入 `_light` 资源分支；同时在 `launcher/smali/com/smartisanos/launcher/e/g.smali` 中根据最终解析出的 `status_bar_icon_color` 设置或清除 `LIGHT_STATUS_BAR`。
  - 回归注意：只允许透明主题 `smartisan_theme_trans`、毛玻璃主题 `smartisan_theme_aero` 这类高斯 / 壁纸主题跟随壁纸明暗；普通不透明主题应继续使用主题自身文字资源和状态栏资源，不要改成跟随壁纸。
- 壁纸显示 / 模糊链路当前保持原版方向，不要再次改成手动模糊 bitmap 或把 `background.png` / `t_blur_background` 互相替换：
  - 透明主题壁纸显示正常的关键是 `s.n(context, uri)` / `decodeLauncherWallpaperSurfaceBitmap()` 按屏幕中心裁剪取壁纸，`background.png` 作为桌面背景纹理。
  - “桌面壁纸模糊效果”正常的关键是写入 `original_launcher_wallpaper_blur_on`，更新 `Constants.isTransWallpaperBlur` 后调用 `Eb.lh()`，由原版 SMEngine 重建 `t_blur_background`。
  - 不要在 Java 层自行 StackBlur 主壁纸，也不要把 `t_blur_background` 覆盖回 `background.png`；这样会造成主桌面、Dock 或局部区域显示不一致。
- 透明主题换壁纸要按原版链路做兼容，不能只依赖系统 Settings 或系统广播：
  - 原版 `ApplicationProxy` 的 `M.onReceive()` 监听 `android.intent.action.WALLPAPER_CHANGED`，仅在 `Constants.isTransparentTheme=true` 时继续。
  - 原版先通过 `e.s.ha(context)` 读取当前透明壁纸 URI，再和 `Constants.sWallpaperUri` 比较；不同则更新 `Constants.sWallpaperUri`，最后调用 `Eb.getInstance().lh()`。
  - 原版 `Eb` 重建主背景时会在高斯 / 透明主题下使用 `Constants.sWallpaperUri` 调 `e.s.n(context, uri)` 解码壁纸，并刷新 `background.png` 纹理；`lh()` 主要负责透明壁纸变化后的节点 / blur 背景刷新。
  - 实测普通 Android / 非系统签名设备上，`Settings.Global.putString(...)` 会因 `WRITE_SECURE_SETTINGS` 被拒，应用主动发送 `ACTION_WALLPAPER_CHANGED` 也会被系统拒绝；此时预览图会更新，但桌面可能继续显示系统壁纸。
  - 2026-06-16 真机日志确认：当前普通 Android 设备上桌面实际背景仍优先跟随系统壁纸；只保存 launcher 私有壁纸副本会导致壁纸页预览变化，但桌面主界面继续显示旧系统壁纸。因此选择壁纸成功后必须直接调用 `WallpaperManager.setStream(..., FLAG_SYSTEM)` 同步系统桌面壁纸，私有 URI / `Constants.sWallpaperUri` / `Eb.Vh()` 作为原版透明主题链路和预览兜底继续保留。
  - Android 7.0+（API 24+）支持 `WallpaperManager.setStream(InputStream, Rect, boolean, FLAG_SYSTEM)`，当前主 APK `minSdkVersion=23`，所以 Android 8 可以使用该接口；低版本保留 `WallpaperManager.setStream(InputStream)` 兼容回退。
  - 普通应用不应主动发送系统保护广播 `Intent.ACTION_WALLPAPER_CHANGED`；系统壁纸由 `WallpaperManager` 设置成功后，系统会自行分发真实壁纸变化事件。手动发送只会在普通 Android 上产生 `Permission Denial` 噪音，不能作为刷新依据。
  - 兼容修复必须把系统 Settings 和广播视为辅助：选择壁纸后先写 launcher 私有 prefs，再直接同步 `Constants.sWallpaperUri`，优先调用原版 `Eb.Vh()` 触发 `background.png` 主背景纹理重建，再调用 `Eb.lh()` / SMEngine 刷新透明壁纸节点和模糊背景。不能只调用 `lh()`，否则日志只会出现 `changeWallpaper TEXTURE_ID_BLUR_BACKGROUND`，主桌面仍可能不更新。
- 检查更新读取 Gitee 下载仓库 Release 列表，只识别 `launcher-` 前缀的软件发布标签，并按版本号选择最高版本；APK 资产只选择桌面主 APK，跳过搜索、主题和 `theme-trans-signed.apk` 等附加包。下载走系统 `DownloadManager`，优先使用标准 Gitee Release 下载地址，失败后尝试 Release 资产返回的备用地址；下载完成后使用 `DownloadManager.getUriForDownloadedFile(downloadId)` 得到安装 URI。
- 检查更新会复用已经下载完成的同版本安装包：保存 Release `tag`、APK 文件名和 `downloadId`；再次检查到同一线上版本时，`STATUS_SUCCESSFUL` 显示“安装”，`RUNNING/PENDING` 显示“下载中”，失败或资产变化才重新下载。
- 后续发布 GitHub / Gitee Release 时，推荐同时上传 `build\launcher-signed.apk` 和 `build\theme-trans-signed.apk`；前者是桌面主 APK，后者是透明主题 Android 15 / Android 16 兼容安装包。不要把 `original_apks\com.smartisanos.launcher.theme.trans.apk` 当用户安装资产发布。
- 桌面内“桌面设置”虚拟入口进入设置页后，已给 maintained 设置首页和壁纸页增加短暂点击保护；壁纸选择器入口也会再次检查保护状态并写入日志，避免 Activity 切换或残留输入导致刚进入设置就误打开图片选择器，进而被模拟器关闭整个 Launcher task。
- 主题详情下载按钮状态已按当前主题项隔离，避免切换到其他主题后仍残留“正在下载”状态。
- 桌面图标加载链路加入 drawable 归一化兜底，改善 MuMu 等环境 adaptive drawable 或特殊图标不显示的问题；MuMu 多用户 / 分身查询缺少 `INTERACT_ACROSS_USERS` 时，`getInstalledPackagesAsUser` 和 `queryIntentActivitiesAsUser` 会退回当前用户查询，避免初始化循环清库导致桌面空白。
- 主题详情页预览图已改为外层居中容器，手机壳和主题截图保持原版层级叠加，并会按标题栏和底部主题色栏之间的可用空间自适应缩小，避免小屏手机底部被颜色栏遮住；从主题详情返回主题列表、从关于我们返回设置首页时会保持原滚动位置，并在首帧绘制前恢复，避免上下晃动。
- 对照 maintained 的 APK 结构确认：maintained `minSdkVersion=19`、`targetSdkVersion=28`，且只保留 `assets/Textures/1080p`；当前工程第一轮先降到 `minSdkVersion=23`，保留更多运行安全余量，后续如需覆盖 Android 5.x / 4.x 再继续做 API 兼容回归。

### 2026-06-24

#### 设置页隐私密码入口与页面锁内置密码

- 对照文档中页面锁现状，原版设置隐私密码入口没有迁到当前桌面设置页，导致用户只能在编辑模式点锁时被动设置。主设置页新增“隐私密码”行，点击后无密码则输入两遍 4-16 位数字密码；已有密码则先验证旧密码，再设置新密码。保存仍只写 Launcher 私有 `launcher_page_lock/password_hash`，摘要算法继续使用带命名域的 SHA-256，页面锁 requestCode 20/21 和原版页面状态机不变。
- 页面锁弹窗的校验同步收紧为 4-16 位数字，避免设置页和锁入口对密码格式判断不一致。
- 验证：`build.bat` 已完成 maintained 设置资源构建、apktool smali、Java 兼容层编译和签名，输出 `build\launcher-signed.apk`。APK 结构检查确认包含 `assets/settings_maintained/maintained-settings-res.apk`；当前 shell 中 `adb` 不在 PATH，`apksigner verify` / `aapt dump badging` 单独调用超时，未做装机交互验证。

### 2026-06-22

#### Android 16 触摸、图标尺寸与文件夹动画修复

- Android 16 / VIVO 上压平手指后桌面不翻页：ADB 原始输入与应用事件确认触摸坐标没有中断，根因是旧 `TVelocityAndGestureTracker` 把较大的 `MotionEvent.getSize()` 当作专用 sweep 手势。Android 15+ 将旧 `sweep_threshold` 提升到 1.0，避免抢占普通翻页；下滑搜索改为先把完整 MotionEvent 交给 RootView / SMEngine，再旁路判断，避免搜索入口截断桌面触摸序列。
- 【已废弃】曾将所有来源统一到 alpha 可见边界90%，并把设置页100%运行时基准改为120%。该方案与 DEFAULT-only normalization、统一 IconVisualMetrics 和禁止来源专用倍率的合同冲突，不得恢复。
- 展开文件夹内容按书架实际可见行高自适应：图标为 48%，应用名为 9.2%，文字中心偏移为 29%；用户调整 50%~150% 图标大小时，展开图标、文字和间距同比缩放。此前误把“缩略图松手后上移”当成展开页落点问题而临时修改的 `M.smali` / `FolderCellPositionAdapter` 入口已全部撤销，不保留错误方案。
- 关闭文件夹缩略图松手后再上移：拖入动画以外框几何中心计算，而最终 2×2 / 3×3 viewport 使用 PNG 内真实搁板中心，两者相差约外框高度 3.6%~3.7%。`folder_icon_center_offset_2_2 / 3_3` 现在按当前外框尺寸动态补偿，使动画落点与最终缩略图一致，并随屏幕和图标比例自适应。
- 日期刷新链路保持不变：系统 `DATE_CHANGED`、`TIME_SET`、`TIMEZONE_CHANGED` 广播仍由原版接收器处理，日期纹理缓存键继续包含年份和年内日序；其他手机只要能被标准日历类别或厂商包名检测到，就会显示当日日期并在跨日后更新。
- 页面锁链路对照原版确认仍保留页状态 `0/2`、锁动画、待验证页面以及 requestCode 20（设置密码）/21（验证解锁）的结果处理；断点是原版依赖系统私有 `com.android.settings.ChooseLockPasswordFake`，已有 fallback 又启动依赖锤子安全中心控件的 `ConfirmPasswordActivity`。现改为 Launcher 内 AlertDialog：首次设置输入两遍4-16位数字密码，解锁输入一次；只在私有 `launcher_page_lock` 中保存带固定命名域的 SHA-256 摘要，验证成功后回调原版 `J.onActivityResult()`，页面锁定/隐藏/解锁仍由原版状态机执行。
- 本轮验证：`build.bat` 构建、Java编译、apktool smali、签名均通过；APK覆盖安装到 API31 `emulator-5554` 和华为 DRA-AL00 成功，模拟器执行 `cmd package compile -m verify -f` 成功，两台设备均无 `VerifyError`、`NoSuchMethodError` 或 Launcher 崩溃。SMEngine编辑画面不暴露Android View层级，密码弹窗和页面锁交互仍需用户在当前页面点击确认。

### 2026-06-21

#### 厂商日历识别、日期刷新、双层错位与统一图标尺寸路径

- 根因不是单一素材错误，而是原版仅把 `com.android.calendar` 当活动日历；VIVO 的 `com.bbk.calendar` 会先按主题 / 改进版静态图标绘制，随后兼容层又叠加日期，形成一大一小、底部错位或日期固定在素材中的现象。
- 新增 `CalendarAppDetector`：优先查询 Android 标准 `ACTION_MAIN + CATEGORY_APP_CALENDAR`，再用 Google、VIVO/BBK、Samsung、MIUI、ColorOS/Oplus、Huawei、OnePlus 等常见包名回退。`ItemInfo.Te()` 和活动图标创建统一使用该检测结果。
- 日期纹理缓存键加入年份和年内日序，避免跨日后继续命中旧 bitmap；活动日期节点保持可见，并继续响应系统日期 / 时间 / 时区刷新链路。VIVO Android 16 真机已确认系统日期 21 时桌面显示 21，刷新后不回退到主题素材中的 20。
- 图标百分比保存虽然正确，但旧实现只在“待处理变更”存在时缩放 `LayoutProperty`；覆盖安装、杀进程或系统回收后会从 XML 恢复 100%。`maybeApplyLauncherIconSize()` 现在每个新进程从 XML 基准只执行一次 `100 -> 保存值`，避免漏应用和重复乘算。
- 验证设备：VIVO V2435A、Android 16；ADB 覆盖安装、冷启动、日期 21、12 宫格以及图标尺寸变化均用于回归。时钟当前走普通图标尺寸链路，未增加厂商专用缩放特判。

### 2026-06-20

#### 图标大小即时生效、文件夹对齐、冷启动网格与设置首页排版

- 图标大小不立即生效的根因不是设置值没有保存，而是保存后只把已有 Launcher Activity 拉到前台。旧进程中的 `Constants.layoutPropertyMap`、网格点、普通应用 `SceneNode` 和 SMEngine 纹理仍使用修改前尺寸；因此图标大小保存后必须完整重建 Launcher。
- 删除 `Constants.applyLauncherIconSize()` 对 `MODE_9` 的跳过。当前桌面 3x3 模式同样必须应用用户比例；跳过它正是“应用图标大小改了但当前桌面不变”的直接回归点之一。
- 关闭文件夹预览不能简单沿用 XML 固定边距，也不能把整个正方形平均切成 2 / 3 行。实测 MODE_12 的 246px 文件夹纹理与 MODE_20 的 178px 纹理具有相同的归一化内部几何；2x2 可见行中心为 0.280 / 0.646，列中心为 0.356 / 0.644；3x3 可见行中心为 0.220 / 0.464 / 0.708，列中心为 0.308 / 0.500 / 0.692。`LayoutPropertyAdapter.centerFolderPreview()` 以当前 `icon_size_with_shadow` 乘这些比例，反算 top / left margin 和横纵间距，所以换屏幕、换 12 / 20 宫格、改变 50%-150% 图标尺寸后仍在每层可见区域垂直居中。
- 打开文件夹使用另一张 1080x1356 书架纹理：`FolderCellPositionAdapter.adjustY()` 只允许作用于 `com.smartisanos.launcher.view.b.a` 文件夹页，围绕中间层按可见书架行高修正 Y；X 继续用原版固定三列。普通桌面页必须原样返回坐标，否则会重现冷启动上下大缝隙。
- 文件夹防回归计算顺序：先取当前关闭外框 / 打开书架的实际绘制尺寸，再从对应 PNG 的可见内部边界求行列中心，最后计算图标边长、margin 和 space；禁止按整张含透明边缘的 PNG 均分，也禁止按某一台设备截图写死像素。资源 XML 只保留原版基准，最终坐标统一在适配器中生成。
- 图标尺寸重启使用 requestCode `1002` 的精确 HOME PendingIntent；它与透明主题曾使用的 requestCode `1001` 属于同类闪回风险。设置首页 `show()` 现在同时取消 1001 和 1002，避免用户修改尺寸后立刻重新进入设置时，残留任务再次把设置页顶回桌面。
- 桌面设置首页三枚缩略图入口同步整理：缩略图左边距改为 12dp，与下方纯文字设置行的左侧视觉基线协调；箭头右侧内边距由 30dp 改为标准 12dp，与下方箭头对齐；副标题限制最多两行并在超长时尾部省略，避免“应用图标”说明挤成三行。
- 缝隙修复：`adjustY()` 首先沿继承链确认当前 page 是打开文件夹页；普通桌面页直接返回原始 Y，只有文件夹页才按书架可见层中心修正。禁止在共用的 `M.smali` 坐标入口中使用不带页面类型保护的文件夹算法。
- 验证：`build.bat` 编译、zipalign、签名成功；APK 覆盖安装到 `emulator-5554`。在 1080x1920 / 560dpi 下，当前修复版冷启动的网格顶边直接贴合状态栏、底边直接贴合 Dock，与 `b36f1a9a` 基线一致，无需进入编辑模式；打开文件夹后三列和逐行排列保持正常。图标大小 50% / 100% 下关闭预览均按可见层中心缩放；改完尺寸后立即进入设置并停留 3 秒，`ThemeChooserActivity` 未再闪回。Logcat 未出现 `FATAL EXCEPTION`、`VerifyError` 或 `NoSuchMethodError`。

### 2026-06-19

#### 文件夹预览、展开排列和多分辨率适配

- 对照用户提供的原版 / 当前截图和 `clean_launcher_raw` 原版代码确认，原版文件夹预览由 `launcher/smali/com/smartisanos/launcher/view/a/la.smali` 按数量选择 2x2 或 3x3 参数组；展开布局由 `launcher/smali/com/smartisanos/launcher/view/b/M.smali` 直接使用 `fa.ir()[index]` 的固定网格坐标，项目按顺序逐行填充。原版不会把最后不足一行的项目移动到整行中央。
- 修复方式：
  - 删除 `M.smali` 两处 `FolderCellPositionAdapter.adjustX()` 调用，展开文件夹重新直接使用原版网格坐标；四个项目显示为第一行三项、第二行第一项，列中心与第一行一致。
  - 12 / 20 宫格竖屏资源中的 `folder_preview_*` 只作为原始 100% 输入基准；运行时统一由 `LayoutPropertyAdapter.centerFolderPreview()` 根据当前 `icon_size_with_shadow` 和可见行列中心生成最终 2x2 / 3x3 参数。4 项以内保持 2x2，5-9 项保持 3x3。
  - 删除 `LayoutProperty.smali` 文件夹专用的二次 X/Y 缩放，只保留 `LayoutPropertyAdapter` 单一适配入口。
  - `MODE_9` 的 `folder_bookcase_*`、标题和分页点参数恢复原版基准。书架素材自身带透明边缘，节点宽度等于屏宽时，可见外框约占屏幕 84%，不能再额外乘 84%。
  - 保留原版的多套 `MODE_9` 坐标基准：`values-xxhdpi` 使用 1080 基准，`values-sw411dp` 使用 1440 基准；不把两套资源强制覆盖成同一份。
  - 实测原版 `folder_open_3_3.png` 为 1080x1356，透明区域外的书架范围为 y=129..1299，三层可见中心间距为 358。`LayoutPropertyAdapter` 以 `358 / 1356` 得到真实可见行高，再按行高限制图标、字体和 `name_off_set_y`，图标与文字作为同一组合留在层内。
  - `_folder` 的书架、网格、图标偏移、文字偏移和裁剪参数统一使用屏幕宽度倍率，禁止同一文件夹混用 `scaleX` 与超长屏 `scaleY`。
  - X 坐标继续完全使用原版 `fa.ir()` 固定三列。Y 坐标只在确认 page 类型为打开文件夹页后，以中间层坐标为锚点，用 `window_width * 358 / 1080` 计算当前可见书架行距；普通桌面页无条件返回原始坐标。
  - `a.1.smali` 的文件夹页面裁剪高度改为当前 `folder_bookcase_height`，使大屏放大后的第一、三行不会被旧的 1080 网格裁剪区截断。
- 验证：
  - `build.bat` 编译、zipalign、签名成功，输出 `build\launcher-signed.apk`。
  - `adb install -r -d` 覆盖安装到 `emulator-5556` 成功并保留原文件夹数据。
  - 同一 APK 在 1080x2424 / 420dpi、720x1600 / 280dpi、1440x2560 / 560dpi 三种配置实测：桌面文件夹预览 2x2 对齐；打开后第一行三列对齐，第四项位于第二行第一列；各行图标和文字均留在对应层内，长名称不越过外框。
- 防回归：
  - 关闭预览的 `left/top/side/space` 必须由同一组归一化可见行列中心一次性反算；不能只把旧 XML 参数整组乘比例，也不能分别追加 X/Y 固定修正。
  - 放大最终行距时必须同步放大文件夹页面裁剪高度；只移动图标而不扩大裁剪区，会表现为第一行图标上半部分被截掉。

### 2026-06-17

#### 更新下载通知与透明主题重启链路回归

- 修复“检查更新”开始下载后通知栏提前显示“安装”的问题。原因是更新下载通知在未完成状态也绑定了安装 PendingIntent；现在只有 `complete=true` 且存在已下载 APK / 下载 ID 时才显示“安装”动作，开始新下载前会先清理旧更新通知。
- 更新包下载使用系统 `DownloadManager` 标准链路；完成后通过 `getUriForDownloadedFile(downloadId)` 取得授权 URI，并附加 `FLAG_GRANT_READ_URI_PERMISSION` 拉起系统安装器。
- 更新下载先 enqueue 标准 Gitee Release 地址；若 `DownloadManager` 返回失败，再自动切换 Release 资产返回的备用地址重新 enqueue。状态栏进度由系统下载管理器显示，应用内弹窗只做前台进度提示；下载完成通知和应用弹窗都使用同一个 downloadId 安装入口。
- 检查更新弹窗会复用已经下载完成的更新包：下载时保存当前 Release 的 `tag`、APK 文件名和 `downloadId`；再次检查到同一个线上版本时，如果 `DownloadManager` 状态为 `STATUS_SUCCESSFUL`，右下角按钮显示“安装”并直接调用 `installApk(downloadId)`。如果状态仍是 `RUNNING/PENDING`，按钮显示“下载中”，避免重复下载同一个安装包。
- 透明主题开启 / 关闭恢复原版方向的 Launcher 进程重启。上一轮为了避免设置页刚返回桌面时出现 SIGKILL 日志，把 `Process.killProcess()` 改成了裸 `startActivity()`，结果 `O.V()` / `Constants.isTransparentTheme` / `X.va()` 没完整重走，桌面会出现黑色主区域、Dock 和主题资源半加载。现在保留“显示加载层 -> 结束设置页 -> 重启进程”的完整初始化链路；从设置页触发时不再额外安排 `AlarmManager` HOME 重启，因为 Android 已会在 Launcher 进程结束后拉起默认桌面，残留闹钟反而会在用户立刻重新进入设置页后把页面顶回桌面。
- 修复开启 / 关闭透明主题后立即进入设置页仍会闪回桌面的问题。原因是旧的 `scheduleLauncherRestart()` 用 requestCode `1001` 排了延迟 HOME PendingIntent，进程重启后用户重新打开 `ThemeChooserActivity`，该 PendingIntent 仍可能延后触发并抢焦点。现在设置页入口会调用 `cancelScheduledLauncherRestart()` 清理残留闹钟；透明主题从 Activity 触发时直接结束设置页并杀旧进程，不再排 HOME 闹钟，非 Activity 场景才保留兜底调度。
- 回归注意：透明主题、宫格和图标大小这类依赖 Launcher 启动链路完整初始化的设置，不要仅靠运行时刷新或裸启动桌面替代进程重启；否则资源表、SMEngine 纹理、`Constants` 状态和原版主题管理器可能不同步。

### 2026-06-16

#### 透明 / 毛玻璃主题文字随壁纸明暗修复与壁纸链路说明

修复内容：

- 修复透明主题、毛玻璃主题下浅色壁纸仍显示白色应用文字的问题。
  - 问题根因：`Constants.initByTheme()` 先调用 `initGaussianDarkLight(context)` 根据当前壁纸计算明暗，并会把浅色壁纸结果写为 `sGaussianResSuffix="_light"`；但紧接着旧代码又执行 `sGaussianResSuffix=""`，把 `_light` 后缀清掉，导致 `Constants.initGaussianTheme()` 和 `Mc.o(theme)` 无法进入原版浅色资源分支。
  - 修复方式：删除这次错误清空 `sGaussianResSuffix` 的逻辑，保留 `initGaussianDarkLight()` 的计算结果；浅色壁纸继续加载 `def_apps_text_color_light`、`def_apps_shadow_color_light`、`page_title_text_color_light` 等原版资源，深色壁纸继续走默认资源。

- 修复透明主题、毛玻璃主题下系统状态栏文字不随壁纸明暗稳定切换的问题。
  - 问题根因：原版会解析 `status_bar_icon_color` / `status_bar_icon_color_light` 并传给 `ua.setSystemUiDecoration()`，但普通 Android 上状态栏深浅文字还受 `SYSTEM_UI_FLAG_LIGHT_STATUS_BAR` 控制，只写旧的装饰颜色不够。
  - 修复方式：在 `launcher/smali/com/smartisanos/launcher/e/g.smali` 中，解析出最终 `status_bar_icon_color` 后按颜色亮度设置系统 UI flag：深色图标颜色时设置 `LIGHT_STATUS_BAR`，浅色 / 白色图标颜色时清除该 flag。

- 验证结果：
  - 浅色壁纸下，状态栏文字变深；应用文字应随 `_light` 资源变深，不再白字贴浅色壁纸。
  - 深色壁纸下，状态栏和应用文字保持浅色，仍可读。
  - 本轮只修文字明暗链路，没有改壁纸模糊和背景纹理链路。

后续注意：

- 透明主题和毛玻璃主题属于“壁纸主题 / 高斯主题”，文字明暗跟随壁纸；普通不透明主题不应跟随壁纸，必须继续使用当前主题自己的文字和状态栏资源。
- 壁纸显示正常依赖原版链路：
  - 自定义壁纸保存为 launcher 私有副本，并同步 `launcher_wallpaper_uri` / `desktop_wallpaper_uri` / `lockscreen_background`。
  - 透明 / 毛玻璃主题加载壁纸时由原版路径按屏幕比例中心裁剪，不应拉伸整图。
  - 模糊开关只写 `original_launcher_wallpaper_blur_on` 并刷新 `Constants.isTransWallpaperBlur`，再调用 `Eb.lh()` 让引擎重建 `t_blur_background`。
- 不要再做以下改动：
  - 不要在 `decodeLauncherWallpaperSurfaceBitmap()` 或 Java 辅助代码里主动 StackBlur 主壁纸 bitmap。
  - 不要把 `t_blur_background` 覆盖回 `background.png`。
  - 不要为了修 Dock 或模糊，替换原版 `background.png` 与 `t_blur_background` 的职责；这会导致主桌面、Dock、动画层使用不同来源的壁纸，出现局部清晰 / 局部模糊 / 底部错图。

#### 自绘搜索页下滑误触与历史清除按钮修复

修复内容：

- 调整主设置页透明主题位置和翻页动画联动。
  - 需求原因：透明主题下桌面背景、文字和高斯壁纸链路都走特殊资源分支，继续暴露“桌面翻页动画”容易让用户选到与透明主题不匹配的动画效果。
  - 修复方式：在 `setting_main.xml` 中把“透明主题”开关移动到“强迫症选项”下面；透明主题开启时，`MaintainedLauncherSettingsHost.bindPage()` 隐藏 `item_page_flip_anims`，`applyTransparentThemeSetting()` 立即强制写回默认翻页动画。
  - 回归注意：透明主题开启期间，`readPageAnimation()` 和 `writePageAnimation()` 都会把动画值钳制为 `0`，确保其他入口也只能使用“默认动画”；关闭透明主题后主设置页会重新显示“桌面翻页动画”选项。

- 修复桌面自绘搜索页容易误触发的问题。
  - 问题根因：此前搜索手势在 `Launcher.smali`、`RootView.smali`、`SMGLSurfaceView.smali` 三层都接入了 `MaintainedLauncherSettingsHost.handleLauncherSearchGesture()`，同一次下滑会被多处重复处理；同时 Java 侧在 `ACTION_MOVE` 阶段就会打开搜索页，距离和角度阈值偏松，没有多指 / 取消手势失效和冷却限制，所以短滑、拖动或图标附近滑动容易误触。
  - 修复方式：只保留 `Launcher.smali` 顶层搜索触发入口，删除 `RootView.smali` 和 `SMGLSurfaceView.smali` 的重复搜索钩子；`handleLauncherSearchGesture()` 改为松手 `ACTION_UP` 时才确认打开，并限制单指、起始区域、下滑距离、纵向角度、手势时长和 1 秒冷却。

- 修复自绘搜索页“搜索历史”右侧清除按钮偏大、和标题不水平对齐的问题。
  - 修复方式：在 `MaintainedLauncherSettingsHost.showSearchPage()` 中让“搜索历史”标题使用垂直居中布局；右侧清除按钮从 `30dp / 18sp` 调整为 `22dp / 14sp`，圆角同步缩小，并保持 `CENTER_VERTICAL`，让按钮中心线和标题文字对齐。

验证结果：

- `.\build.bat` 编译成功，输出 `build\launcher-signed.apk`。
- `adb install -r -d build\launcher-signed.apk` 安装到 `emulator-5554` 成功。
- 在 Smartisan Launcher 桌面右侧空白区域短距离下滑，前台仍保持 `com.smartisanos.launcher/.Launcher`，未打开搜索页。
- 在同一区域明确长距离下滑，前台进入 `com.smartisanos.launcher/.theme.ThemeChooserActivity` 自绘搜索页。
- 截图 `build\search_page_after_fix.png` 确认“搜索历史”右侧 X 已缩小并与标题水平对齐。

#### 桌面设置页偶发自动返回桌面排查

现象：

- 用户反馈启动后停在设置页面时，偶尔会自动返回桌面主页。
- ADB 复现路径为：从桌面底部“桌面设置”虚拟入口进入 maintained 设置页，等待数秒后观察任务栈。

ADB 结论：

- 直接 `am start -n com.smartisanos.launcher/.theme.ThemeChooserActivity --ez from_desktop_settings true` 启动设置页，连续观察未复现自动返回。
- 从桌面虚拟入口进入设置页时，旧包日志显示先进入 `ThemeChooserActivity`，约 7 秒后同一 Launcher 进程发起 `ACTION_GET_CONTENT image/*`，系统打开 `com.android.documentsui/.picker.PickActivity`。
- 随后 MuMu 日志出现 `tabs/tab close task:3861`，系统以 `remove task` 原因 kill `com.smartisanos.launcher`，所以表现为设置页退回桌面。
- 日志中没有 `AndroidRuntime FATAL EXCEPTION`，这次不是 Java 崩溃；真正异常点是刚进入设置页后误触发了“桌面壁纸 -> 选择图片”的壁纸选择器链路。

修复方式：

- `MaintainedLauncherSettingsHost.show()` 打开 maintained 设置首页时调用 `armSettingsClickGuard()`，给 Activity 切换后的早期输入增加 800ms 保护窗口。
- `showWallpaperPage()` 切入桌面壁纸页时同样重置保护窗口。
- 首页 `click(...)` 和二级简单列表 `replaceSimpleListWithScroll(...)` 的点击监听统一包装为 `guardedSettingsClick(...)`，保护窗口内的点击会被忽略并打印 `MaintainedSettings` 日志。
- `pickWallpaper()` 在真正拉起系统图片选择器前再次检查保护状态，并记录 `pickWallpaper requested by user`，后续如果再误开图片选择器，可以直接从 logcat 确认入口。

验证：

- `build.bat` 构建成功，输出 `build\launcher-signed.apk`。
- `adb install -r build\launcher-signed.apk` 安装到 `emulator-5554` 成功，设备显示 `versionCode=25`、`versionName=v1.5.0`。
- 使用同一路径从桌面底部“桌面设置”进入设置页，连续 18 秒任务栈一直停留在 `com.smartisanos.launcher/.theme.ThemeChooserActivity`。
- 修复后完整 logcat 中没有再出现 `ACTION_GET_CONTENT`、`PickActivity`、`remove task` 或 Launcher 被 kill 的记录。

涉及文件：

- `launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java`
- `docs/development/DEVELOPMENT_LOG.md`

### 2026-06-07

#### v1.4.8 自绘搜索、主题详情与桌面恢复稳定性

修复内容：

- 版本发布：
  - 文本 `launcher/AndroidManifest.xml` 调整为 `versionCode=24` / `versionName=1.4.8`。
  - 同步修正最终构建注入的 `launcher/original/AndroidManifest.xml` 二进制 Manifest，确保最终 APK 真实版本为 `v1.4.8 (24)`。
  - 设置页“关于 / 当前版本”显示同步为 `1.4.8`。

- 搜索方案：
  - 搜索页由 launcher 内 `ThemeChooserActivity` / `MaintainedLauncherSettingsHost.showSearchPage()` 自绘，不依赖外部搜索 APK。
  - Release、构建脚本和 README 均不包含独立搜索安装包；桌面更新资产只选择主 APK。

- 检查更新与发布：
  - 软件检查更新只匹配 `launcher-` 标签，避免 `themes-v1` 主题发布被误识别成软件新版本。
  - Release 只把桌面主 APK 当作桌面更新资产；透明主题包可以随 Release 上传，但由桌面更新逻辑跳过。
  - 主题下载仍使用 Gitee Release `themes-v1`，软件更新与主题下载接口分离。

- 主题详情页：
  - 主题详情页的 PRO3 手机预览改为根据可用宽高动态缩小，尤其适配小屏手机，避免预览底部被底部主题色栏遮挡。
  - 手机外框继续使用白色主题详情框，并保持 PRO3 预览图与外框叠加。

- 桌面恢复稳定性：
  - `Launcher.onResume()` 后增加桌面 GL Surface 可见性、布局刷新和 `requestRender()` 唤醒，缓解部分手机从其他应用返回桌面时只显示黑屏和状态栏的问题。
  - MuMu 上定位到原版分身查询会访问 user 10 并触发跨用户权限异常，已为安装包列表和应用入口查询补 fallback，避免 `dataInitProtected` 多次失败后清库导致桌面空白；ADB 抓屏确认 12 宫格可正常显示。

- 构建验证：
  - `build.bat` 构建通过，输出 `build\launcher-signed.apk`。
  - `aapt dump badging build\launcher-signed.apk` 确认最终 APK 为 `versionCode='24'`、`versionName='v1.4.8'`、`sdkVersion:'23'`、`targetSdkVersion:'28'`。
  - 主 APK 中不包含 `quicksearch` / `bundled_apps` 资产。

### 2026-06-06

#### 应用分身、图标识别、毛玻璃主题、搜索和更新下载修复

修复内容：

- 版本发布：
  - 文本 `launcher/AndroidManifest.xml` 调整为 `versionCode=20` / `versionName=v1.4.6`。
  - 同步修正最终构建注入的 `launcher/original/AndroidManifest.xml` 二进制 Manifest，确保最终 APK 的真实版本也是 `v1.4.6 (20)`。
  - 设置页“检查更新”默认版本字符串同步为 `v1.4.6`。

- 应用分身：
  - 对照 maintained 的多用户查询思路，把桌面应用列表、搜索页和启动链路继续向 `LauncherApps` / 用户句柄查询靠拢。
  - 继续调整面具标记大小、位置和颜色，使其更接近原版锤子桌面左下角黑色面具效果。

- 图标识别：
  - 对照 `smartisan-launcher-maintained` 调整当前工程图标识别逻辑，同时保留当前项目已有的图标识别入口和 redirect / appfilter / 自定义图标能力。
  - 修复部分普通应用被误识别成应用商店图标的情况，例如“闲鱼”“酷安”。
  - 修复部分系统应用名称识别不稳定的情况，例如“电话”“拨号”“电话本”“电话管家”。
  - 应用图标页加载速度继续优化，避免每次打开都做不必要的重拉取和整页重建。

- 搜索页和拖动手势：
  - 搜索页改为能搜索到普通应用和分身应用。
  - 对照 maintained 收窄下滑搜索触发条件，只在明确快速下滑时打开搜索，减少长按拖动应用时误识别为打开搜索页。

- 毛玻璃主题：
  - 对比原版毛玻璃主题 `com.smartisanos.launcher.theme.aero.apk` 和 maintained 的显示效果，修复毛玻璃主题桌面文字、编辑页文字仍显示黑色或加载时先黑后白的问题。
  - 毛玻璃主题文字效果恢复为和其他深色/浅蓝主题一致的白色文字效果。
  - 删除白雾主题入口、显示顺序、字符串、公有资源项和相关 smali 判断；当前透明壁纸主题只保留毛玻璃。

- 主题下载和模拟器兼容：
  - 修复在线主题详情页从一个正在下载的主题切换到其他主题时，右上角下载按钮状态没有正确隐藏或刷新。
  - 桌面图标加载链路加入 drawable 归一化处理，改善 MuMu 模拟器等环境中 adaptive drawable 或特殊 drawable 图标不显示的问题。

- 检查更新：
  - 修复“检查更新 -> 下载”没有任何进度显示的问题。
  - 下载更新包后现在会弹出进度窗口；未知大小时显示等待 / 下载中，已知大小时显示百分比，下载完成后自动关闭并启动安装。

- 构建和清理：
  - 多次执行 `build.bat` 构建通过，输出 `build\launcher-signed.apk`。
  - `aapt2 dump badging build\launcher-signed.apk` 确认最终 APK 为 `versionCode='20'`、`versionName='v1.4.6'`、`sdkVersion:'23'`、`targetSdkVersion:'28'`。
  - `apksigner verify --verbose --print-certs build\launcher-signed.apk` 确认 v1 / v2 / v3 签名均为 true。
  - 按当前约定清理 `build` 目录，只保留 `launcher-signed.apk`、`launcher-signed.apk.idsig` 和 `tools`。

#### v1.4.7 更新下载与 Gitee 镜像测试版

修复内容：

- 版本发布：
  - 文本 `launcher/AndroidManifest.xml` 调整为 `versionCode=21` / `versionName=v1.4.7`。
  - 同步修正最终构建注入的 `launcher/original/AndroidManifest.xml` 二进制 Manifest，确保最终 APK 的真实版本也是 `v1.4.7 (21)`。
  - 设置页“检查更新”默认版本字符串同步为 `v1.4.7`。

- 下载镜像：
  - 软件更新版本列表读取 Gitee Release API，只遍历 `launcher-` 标签并选择最高版本；APK 下载优先 Gitee Release 镜像，失败后使用 Release 资产中的备用地址。
  - 主题下载基地址切换到 Gitee Release `themes-v1`，用于测试国内镜像下载链路。
  - 当前 Gitee `themes-v1` 已上传部分主题附件，已验证公开附件 URL 会跳转到 `attach_files` 下载地址；剩余主题因 Gitee 仓库附件配额提示超过 1GB，待网页端释放容量或扩容后补齐。

- 验证：
  - `build.bat` 构建通过，输出 `build\launcher-signed.apk`。
  - `aapt2 dump badging build\launcher-signed.apk` 确认最终 APK 为 `versionCode='21'`、`versionName='v1.4.7'`、`sdkVersion:'23'`、`targetSdkVersion:'28'`。
  - `apksigner verify --verbose --print-certs build\launcher-signed.apk` 确认 v1 / v2 / v3 签名均为 true。

### 2026-06-04

#### v1.4.5 设置体验、主题详情和英文文案修复

修复内容：

- 版本发布：
  - 文本 `launcher/AndroidManifest.xml` 调整为 `versionCode=19` / `versionName=v1.4.5`。
  - 同步修正最终构建注入的 `launcher/original/AndroidManifest.xml` 二进制 Manifest，避免 APK 真实版本和文本 Manifest 不一致。
  - 设置页“检查更新”默认版本字符串同步为 `v1.4.5`。
- 强迫症选项：
  - `launcher/tools/maintained_settings_res/res/values/strings.xml` 补齐 `ocd_setting=OCD Settings`，中文资源继续使用“强迫症选项”。
  - 主设置页标题改用 `launcher_setting_name`，强迫症入口改用 `ocd_setting`，强迫症二级页标题改用 `obsession_header_title`。
  - 修复英文系统下强迫症入口仍显示中文的问题；后续不要在 Java 中硬编码“强迫症选项 / 桌面设置”等标题。
- 设置返回位置：
  - 从“关于我们”、壁纸、翻页动画、应用图标、强迫症选项等子页返回主设置页时记录并恢复进入前的滚动位置。
  - 从桌面主题列表进入主题详情后返回时恢复主题列表位置。
  - 滚动恢复从 `post()` 延后滚动改为 `OnPreDrawListener` 首帧绘制前恢复，修复返回时先跳顶部再滚回当前位置造成的上下晃动。
- 主题详情页：
  - `activity_theme_item.xml` 改为外层 `phone_detail_preview` 填满标题栏和底部主题标签栏之间区域，内层保留原版手机预览图层并居中。
  - 取消依赖运行时 `translationY` 硬调预览位置，避免手机外壳和主题截图错位。
- 已纳入本轮发布记录的前序功能 / BUG：
  - 应用图标页：改进版图标开关复用首页同款控件；图标包行和图标大小行补齐箭头与点击范围；单应用默认图标、推荐图标、相册自定义图标切换后只刷新当前行并保持滚动位置。
  - 桌面图标大小：50% - 150% 连续调节，小 / 中 / 大三档快捷选择；当前仅对 12 / 20 宫格普通应用统一生效，桌面“桌面设置”保持原版独立 SettingButton，不纳入该替换或缩放链。
  - 图标包兼容：支持 appfilter / component 精确匹配，图标包优先级高于锤子自动识别，单应用自定义图标优先级最高。
  - 内置搜索页：设置页提供“启用下滑搜索”开关；搜索页去掉自绘键盘，改为系统输入法；顶部常用应用横向滑动；搜索结果行固定高度并垂直居中。
  - 双开应用：通过 `LauncherApps.getProfiles()` 补齐多用户可启动 Activity，保存 `ItemInfo.userId` 并通过 `startActivityAsUser` 启动对应用户应用。
  - 刘海屏 / 编辑态：Launcher 主窗口持续保留 fullscreen layout 和 cutout short edges，避免长按图标、进入编辑模式时露出系统状态栏并顶下桌面。
  - 解锁动画：修正动画播放状态判断，让锁屏返回桌面时能按设置开关执行解锁动画。
  - 设置体验：关于我们改为 maintained / 原版风格页面；检查更新、关闭电池优化、默认桌面、隐藏虚拟键、角标开关等入口已接入。

验证计划：

- `build.bat` 构建通过。
- `aapt dump badging build\launcher-signed.apk` 应显示 `versionCode='19'`、`versionName='v1.4.5'`、`sdkVersion:'23'`、`targetSdkVersion:'28'`。
- `apksigner verify --verbose --print-certs build\launcher-signed.apk` 应显示 v1 / v2 / v3 签名均为 true。
- 英文系统进入桌面设置时，主标题应显示 `Launcher Settings`，强迫症入口和二级页标题应显示 `OCD Settings`。
- 从主题列表滚动后进入某个主题详情再返回，应保持主题列表位置；从“关于我们”返回设置首页也应保持原位置且不再上下晃动。
- 主题详情页手机预览应在标题栏与底部主题标签之间居中，手机壳和截图不应错位。

### 2026-06-03

#### 兼容安装与第一轮包体瘦身

背景：

- 用户反馈同一个 APK 发给其他手机安装失败，同时 maintained 能在更多手机上安装、分辨率适配更好，且包体更小。
- 对比 `smartisan-launcher-maintained` 后确认，当前 original-port 主要问题有两类：
  - 安装兼容：当前 APK 原本 `minSdkVersion=29`，Android 10 以下设备会直接安装失败；maintained 为 `minSdkVersion=19`、`targetSdkVersion=28`。
  - 包体过大：当前 APK 约 105.9MB，其中 `assets` 占约 97.5MB；maintained APK 约 44.4MB，其中 `assets` 约 33.9MB。

修复内容：

- 安装兼容：
  - 文本 `launcher/AndroidManifest.xml` 的 `uses-sdk` 从 `minSdkVersion=29` / `targetSdkVersion=29` 调整为 `minSdkVersion=23` / `targetSdkVersion=28`。
  - 同步修正最终构建注入的 `launcher/original/AndroidManifest.xml` 二进制 Manifest，确保最终 APK 真实输出 `sdkVersion:'23'`、`targetSdkVersion:'28'`。
  - `launcher/apktool.yml` 同步记录 `minSdkVersion: 23`、`targetSdkVersion: 28`。
- 包体瘦身：
  - 对照 maintained，确认 maintained 只保留 `assets/Textures/1080p`，没有 `720p` 目录。
  - 将 `com.smartisanos.launcher.pb.getResolution()` 改为统一返回 `1080p`，避免低密度设备继续选择 `Textures/720p`。
  - 删除未跟踪的构建输入目录 `launcher/assets/Textures/720p`，减少约 36.9MB 纹理资源。
- 签名兼容：
  - 原构建脚本使用 `jarsigner`，`apksigner verify` 显示只有 `Verified using v1 scheme: true`，v2/v3 均为 false。
  - Android 12 及部分厂商安装器对重打包 APK 的旧 v1/JAR 签名兼容较差，容易在文件管理器安装时只显示“安装失败”。
  - `build.bat` 改为先 `zipalign -p -f 4`，再使用 `apksigner sign` 输出 v1/v2/v3 签名。

验证：

- `build.bat` 构建通过。
- `aapt dump badging build\launcher-signed.apk` 验证：
  - `versionCode='15'`
  - `versionName='v1.4.1'`
  - `sdkVersion:'23'`
  - `targetSdkVersion:'28'`
- `apksigner verify --verbose --print-certs build\launcher-signed.apk` 验证：
  - `Verified using v1 scheme: true`
  - `Verified using v2 scheme: true`
  - `Verified using v3 scheme: true`
- 新 APK 体积约 `63.92MB`，相比瘦身前约 `105.9MB` 明显降低。
- `adb install -r -d build\launcher-signed.apk` 安装到 `emulator-5554` 成功。
- 启动桌面成功，截图确认 12 宫格主界面显示正常。
- 打开桌面设置成功，截图确认设置页可进入；删除 `720p` 后没有出现启动崩溃。

后续优化方向：

- 继续瘦身的主要大头：
  - `assets/Textures/1080p` 约 27.8MB。
  - `assets/theme_preview` 约 16.2MB。
  - `assets/settings_maintained/maintained-settings-res.apk` 约 6.6MB。
  - `assets/settings_native` 约 3.5MB。
- 下一轮不建议直接删除这些目录，应先确认引用点：
  - 主题预览图可以考虑改成更小尺寸或 WebP/JPG。
  - `settings_maintained` 可以考虑把实际用到的资源合并进主 APK，取消内嵌 APK。
  - `Textures/1080p` 需要继续按实际 12 / 20 宫格、主题和文件夹引用逐项裁剪。
- Manifest 里仍存在大量原版系统级 / Smartisan 私有权限，部分普通 ROM 可能会提示风险；要真正清理需要对二进制 Manifest 做节点级删除或改造构建流程，不宜只改文本 Manifest。

#### v1.4.1 版本与内置搜索页继续修复

修复内容：

- 版本号：
  - 文本 `launcher/AndroidManifest.xml` 从 `versionCode=14` / `versionName=v1.4` 调整为 `versionCode=15` / `versionName=v1.4.1`。
  - 同步修正最终构建会注入的 `launcher/original/AndroidManifest.xml` 二进制 Manifest，确保最终 APK 的 `aapt dump badging` 能读到 `versionCode=15` / `versionName=v1.4.1`。
  - 设置页“检查更新”右侧默认版本字符串同步为 `v1.4.1`。
- 内置搜索页：
  - 去掉自绘 T9 键盘，改为点击顶部输入框后由系统输入法接管。
  - 设置首页新增“启用下滑搜索”开关，绑定 `launcher_search_page_enabled`，关闭后桌面下滑不再进入内置搜索页。
  - 搜索页顶部常用应用区从固定 5 个等分项改成横向可滑动列表，最多展示前 20 个可启动应用。
  - 修复搜索结果行文字错位：结果行固定 84dp 高度，图标和标题都垂直居中，标题使用单行省略。
  - 启动搜索页时使用 `CLEAR_TOP | SINGLE_TOP`，减少最近任务里重复出现两个“锤子桌面”窗口的概率。

验证：

- `build.bat` 构建通过，输出 `build\launcher-signed.apk`。
- `adb install -r -d build\launcher-signed.apk` 安装到 `emulator-5554` 成功。
- 直接启动搜索页，确认顶部常用应用可以横向滑动，滑动后能看到“文件 / 浏览器 / 游戏中心”等后续应用。
- 输入 `root` 后确认搜索结果行中 Root Explorer 图标和文字同一行垂直居中，不再出现标题贴到上方的问题。

涉及文件：

- `launcher/AndroidManifest.xml`
- `launcher/original/AndroidManifest.xml`
- `launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java`
- `launcher/tools/maintained_settings_res/res/layout/setting_main.xml`
- `launcher/tools/maintained_settings_res/res/values/strings.xml`
- `launcher/tools/maintained_settings_res/res/values-zh-rCN/strings.xml`
- `README.md`
- `docs/development/DEVELOPMENT_LOG.md`

#### v1.4.2 兼容签名发布

修复内容：

- 版本号：
  - 文本 `launcher/AndroidManifest.xml` 从 `versionCode=15` / `versionName=v1.4.1` 调整为 `versionCode=16` / `versionName=v1.4.2`。
  - 同步修正最终构建会注入的 `launcher/original/AndroidManifest.xml` 二进制 Manifest，确保最终 APK 的真实版本也为 `v1.4.2 (16)`。
  - 设置页“检查更新”右侧默认版本字符串同步为 `v1.4.2`。
- 兼容安装：
  - 延续本日第一轮兼容修复，最终 APK 保持 `minSdkVersion=23`、`targetSdkVersion=28`。
  - 构建脚本继续使用 `zipalign -p` 和 `apksigner` 输出 v1/v2/v3 签名，改善 Android 12 等新系统通过文件管理器安装时失败的问题。
- 包体：
  - 保持 `pb.getResolution()` 统一返回 `1080p`，并继续使用移除冗余 `720p` 纹理后的瘦身构建输入，当前 APK 约 64MB。

验证计划：

- `build.bat` 构建通过。
- `aapt dump badging build\launcher-signed.apk` 应显示 `versionCode='16'`、`versionName='v1.4.2'`、`sdkVersion:'23'`、`targetSdkVersion:'28'`。
- `apksigner verify --verbose --print-certs build\launcher-signed.apk` 应显示 v1 / v2 / v3 签名均为 true。

#### 刘海屏编辑态状态栏下移修复

背景：

- 用户反馈刘海屏手机上长按图标或进入桌面编辑模式时，会露出原本的系统状态栏，桌面内容整体向下移动，底部图标显示不全。
- 对照 maintained 的 `docs/compatibility-fixes.md`，同类问题的根因是编辑、排序、拖拽等特殊模式切换系统 fullscreen / status bar 状态，导致系统状态栏和桌面自绘状态栏坐标脱节。

修复内容：

- `launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java`
  - `applyLauncherNavigationBarSetting()` 不再只处理隐藏虚拟键。
  - 每次 `onResume()` / `onWindowFocusChanged()` 应用设置时，都强制保留 `View.SYSTEM_UI_FLAG_LAYOUT_STABLE | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN`。
  - 关闭“桌面隐藏虚拟键”时只清理 `HIDE_NAVIGATION` / `IMMERSIVE_STICKY` / `LAYOUT_HIDE_NAVIGATION`，不再清掉顶部 fullscreen layout。
  - Android 9 及以上设置 `LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES`，让 Launcher 主窗口可以延伸到刘海短边区域。
  - 同步保持透明状态栏和 `FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS`，避免系统白色状态栏重新参与布局。
- `launcher/smali/com/smartisanos/launcher/ua.1.smali`
  - 原版窗口初始化 `ua.a(Window)` 不再依赖 `Constants.IS_NAVIGATION_BAR` 才设置 fullscreen layout。
  - 无论是否存在虚拟导航栏，都保留 `0x500`（`LAYOUT_STABLE | LAYOUT_FULLSCREEN`）。
  - Android 9 及以上同步写入 `layoutInDisplayCutoutMode = SHORT_EDGES`。

验证：

- `build.bat` 构建通过。
- `adb -s emulator-5556 install -r -d build\launcher-signed.apk` 安装成功。
- `adb -s emulator-5556 shell am start -n com.smartisanos.launcher/.Launcher` 启动成功。
- 截图 `build\cutout_statusbar_fix_desktop.png` 验证普通态仍使用桌面自绘状态栏，没有出现白色系统状态栏顶下桌面。
- 该问题仍建议在实际刘海屏真机上补充回归：长按桌面图标、进入桌面编辑模式、多页预览、拖动图标到底部 Dock 附近，确认顶部不露系统状态栏、底部图标不被裁切。

### 2026-06-02

#### 【已废弃】桌面图标大小滑块旧接入方式（旧 LayoutProperty 多字段缩放）

#### 桌面设置缺口第一批补齐

修复内容：

- 桌面隐藏虚拟键：
  - restored maintained 首页 `item_id_hide_navigation_bar` 开关，绑定 key `launcher_hide_navigation_bar`。
  - Launcher 主 Activity 在 `onCreate()`、`onResume()`、`onWindowFocusChanged()` 中读取该 key，只在桌面主界面应用 `HIDE_NAVIGATION`、`IMMERSIVE_STICKY`、`LAYOUT_HIDE_NAVIGATION`、`LAYOUT_STABLE`。
  - 设置页、主题页、图标页不直接应用隐藏虚拟键，避免影响非桌面界面。
- 角标相关强迫症选项：
  - maintained 风格设置首页新增“隐藏图标上的角标”和“紧贴屏幕横扫清除角标”两个开关。
  - 分别绑定 `launcher_hide_badge` 和 `launcher_badge_swipe_clean`，沿用旧桌面读取 / 刷新链路。
- 更多区域：
  - “检查更新”读取 Gitee Release 列表，筛选 `launcher-` 标签最高版本，下载使用 `DownloadManager`，Gitee 优先并保留 Release 资产备用地址。
  - “关闭电池优化”优先使用 `ACTION_REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` + 当前包名 `com.smartisanos.launcher`，目标是直接弹出当前锤子桌面的电池优化确认；系统或权限不允许时回退当前应用详情页，不再默认进入所有应用的电池优化列表。
  - “关于我们”从简短信弹窗改为完整页面：顶部锤子风格标题栏、Smartisan OS 标识卡片、“更多 Smartisan 的应用软件”列表和“关注我们”分组。
  - 隐藏“分享此应用给朋友”“问题反馈”“用户体验改进计划 / Smartisan 服务条款”，并修正更多区域卡片背景。
- 下滑搜索：
  - 这一阶段发现原桌面手势代码实际只认上滑，曾临时改为上下滑方向都可进入搜索；该过渡方案已在 2026-06-30 收口，上滑入口现已停用，仅保留下滑搜索。
  - 移除旧逻辑中前三次只弹 `fling_down_tips` 提示、不真正打开搜索的分支，第一次触发就直接进入搜索页。
  - `CallStubUtils.Q()` 不再调用缺失的 `com.smartisanos.quicksearch.provider.extra`，改为直接启动本项目内置搜索页。
  - 将旧 `ua.fc()` 搜索目标从缺失的 `com.smartisanos.quicksearch / com.android.quicksearchbox.SearchActivity` 改为已注册的 `ThemeChooserActivity`，并通过 `launcher_show_search=true` extra 进入搜索模式。
  - `MaintainedLauncherSettingsHost.show(...)` 根据 extra 切换为内置搜索页，支持应用名 / 包名过滤和点击启动。
  - 搜索手势只保留 Launcher 顶层入口；RootView 和 SMGLSurfaceView 不再重复处理同一次触摸，避免下滑被多层触发。

验证：

- `build.bat` 构建通过，输出 `build\launcher-signed.apk`。
- `adb install -r -d build\launcher-signed.apk` 安装到 `emulator-5554` 成功。
- 设置首页截图确认“桌面隐藏虚拟键”“隐藏图标上的角标”“紧贴屏幕横扫清除角标”均显示为同款锤子开关。
- 直接启动 `ThemeChooserActivity --ez launcher_show_search true` 可打开内置搜索页；输入 `root` 后列表过滤到 Root Explorer。
- ADB 与桌面操作验证：短距离下滑保持桌面，明确长距离单指下滑进入 launcher 内自绘搜索页；搜索入口不依赖外部 provider。
- 通过系统设置值和桌面启动路径确认 Launcher 可读取 `launcher_hide_navigation_bar` 并应用隐藏虚拟键 flags；当前模拟器本身底部虚拟键不可见，仍建议在有三键导航的设备上补充截图回归。

涉及文件：

- `launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java`
- `launcher/tools/maintained_settings_res/res/layout/setting_main.xml`
- `launcher/smali/com/smartisanos/launcher/Launcher.smali`
- `README.md`
- `docs/development/DEVELOPMENT_LOG.md`

### 2026-06-01

#### 应用图标页交互、样式和刷新稳定性修复

背景：

- 用户反馈应用图标页的“改进版图标”开关虽然接近首页开关，但不是同一个 Smartisan/maintained 样式。
- 选择单应用图标后页面会整体刷新并跳回顶部，尤其从相册选择图片返回后会闪一下回到顶部。
- 点击右侧图标行的文字区域也会弹出选择框，实际预期是只有图标块或图标包右侧状态文字可以点击。
- 图标包行宽度和背景没有和上方开关组成同一组卡片。

修复内容：

- `改进版图标` 开关：
  - 从手写 `LinearLayout + SwitchEx` 改为复用首页同款 `SettingItemSwitch`。
  - 使用 maintained 的 `setting_item_switch_layout`、`SettingSubItemSingleStyle` 背景和同一个 `SwitchEx` 绘制链路。
  - 点击整行和点击开关本身都能切换，但视觉样式不再单独手写。
- `图标包` 行：
  - 背景改为 maintained 的 `selector_setting_sub_item_bg_bottom`，和上面的 `改进版图标` 行组合成一个整体。
  - 默认显示 `不使用图标包`。
  - 弹窗入口收窄为右侧状态文字，点击左侧 `图标包` 标题不再弹出选择框。
- 单应用图标选择：
  - 左侧系统原图、右侧推荐/加号图标块保留点击。
  - 取消整行点击，右侧应用名和说明文字不再误触发弹窗。
  - 选择左侧默认图标、右侧推荐图标后只刷新当前行，不再调用 `showIconPage(activity)` 整页重建。
- 相册自定义图标：
  - 保存选择图片前的当前滚动位置。
  - 图片返回后优先在当前页面查找对应应用行并刷新该行。
  - 如果当前行找不到，才兜底重建应用图标页，并恢复原来的 `ScrollView` 位置。
- 全局改进版图标开关：
  - 开启/关闭后更新当前页面所有已渲染图标行的红色对号和说明文字。
  - 不再通过整页重建制造滚动跳动。

涉及文件：

- `launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java`
- `README.md`
- `docs/development/DEVELOPMENT_LOG.md`

验证：

- `build.bat` 构建通过，输出 `build/launcher-signed.apk`。
- `adb install -r -d build\launcher-signed.apk` 安装到 `emulator-5554` 成功。
- 已在 MuMu 虚拟机中确认：
  - 开关样式与桌面设置首页同款开关一致。
  - 选择推荐图标、默认图标时当前页即时更新。
  - 从相册选择图片作为图标后保持当前位置。
  - 右侧应用文字区域不弹窗。
  - 图标包只有右侧状态文字区域弹窗，左侧标题区域不弹窗。

后续注意：

- 应用图标页当前仍由 `ThemeChooserActivity` 承载 maintained 风格兼容页，还不是完整迁移的原生 Smartisan Settings Activity。
- 图标自动识别资源和 Smartisan 网络图标链路仍建议继续做更多应用回归，尤其是系统应用、Google 应用和第三方应用混合安装场景。


<a id="历史专项计划"></a>

---

> 历史归档，截止 2026-10-26 整理前。以下“当前／下一项”均为当时的历史快照，不能作为当前施工指令。当前入口见[专项计划](../LAUNCHER_FIX_AND_OPTIMIZATION_PLAN.md)。

# LAUNCHER_FIX_AND_OPTIMIZATION_PLAN.md

## 2026-10-26 当前执行项：默认圆框跨机型一致性

全节点扩容的内存代价已收口为只扩三类批量节点。4df00ecaff7d4da75d2848053e5fee05434fcae0226cb7f590d2b7f905f4c604已在X21A/Android9保数据安装，三动画与五次启动有限回归通过，恢复默认动画0。内存五样本仅为固定原生分配场景，不冒充整机提速；具体证据与未验项见开发日志2026-10-26首节。

按用户新增截图，下一项先审计同一应用DEFAULT来源在不同手机得到Bitmap／adaptive包装时的背景判断、缓存身份以及白边来源；只修改确认有差异的既有来源／圆框实现，保留匹配图标与主体。搜索上滑本轮未验收、Android16最终候选断开未核对、故障iQOO及32位实装／长稳／冷启动仍开放，不重复已通过的旧模糊样本。


## 2026-10-25 百叶窗故障插队修复后的当前入口

用户本轮的百叶窗缺图／标题镜像及测试期闪退优先于下方旧“下一项”。已修复MAIN越权读取GL坐标，以及随包arm64批量光照第17格起越界；保留12／20宫格、原动画与页数。最终d2bf6af8e583b10f304d5dcab9fce1375323bad7edb37a66fb881493d7f1886e已安装并核对；162项原生写入／初始化／创建释放、控制器及V2458A三种动画有限路线通过，动画恢复4，默认桌面按新授权恢复锤子。详细原因、负控、撤回实验、内存成本与未验机型只以开发日志同日首节为准。

当前不再重复同批翻页样本；下一项是扩充native存储后的内存／冷启动代价与长稳，补故障iQOO11和Android9覆盖。不能把本机不复现当成全部反馈关闭。旧快捷桌面窗口耗时热点等暂停项保留，不宣称已解决。


## 2026-10-25 当前唯一执行入口：合并验收与剩余边界

本节取代下方各历史批次的“下一项”。已验收且实现未变的项目冻结；只有新故障、相关代码变化或新增目标设备才重开对应回归。不得把同一热点换标题重复采样，或把审计/拒绝候选写成优化完成。不以文件数或局部样本计算项目完成百分比。

**10/25截图后分段与精确商表优化收口：** V2458A原/新各五有效样本确认MAIN排队/绑定不是主要热点；只在原Capture.blur本次调用内复用7396项整数商，除法2046720→7396，额外约28.89KiB临时数组，不跨截图保存。77项像素/预算检查、旧源码预算负控、33项世代/300项手势通过；纵横索引预计算候选无时间收益已撤回。模糊整体中位6.645→3.079ms，截图返回→背景就绪回调18.735→16.441ms；首次总链31.320→35.855ms未改善，不能称首次打开卡顿或冷启动解决，更不是SF可见帧计时。候选首组与原生测试重叠已排除，仅candidate-valid计性能。正式v1.6.0/34 af03262473ffd2fb2129e9664c31ec1bea249bed4b91a63eb042823f77d7ad99已安装/拉回核对；生产仅Capture，原参数/原窗口关闭与触摸合同不变，正式完整功能路线＋额外四轮快捷桌面通过。**下一项限定onBackgroundReady约11–12ms窗口链内部（资格检查、Popup创建/showAtLocation、动画启动）；无可删除调用就冻结，不重复本批模糊或池化实验。** 细节及未验证Android9/其他ROM/长期内存边界见开发日志，证据build/quickdesktop-stages-20261025。整体冷启动、Folder尖峰等仍开放。

**10/25单缓冲复用评估完成，不采用：** V2458A正常打开旧实现/候选各五次，DirectByteBuffer分配5→1，但额外保留14112000字节（13.46MiB）；分配调用累计仅0.303→0.072ms，请求发布→背景就绪回调中位49.111→46.211ms，不是SF可见时延，未证明值得常驻成本。GC增量37/37受meminfo采样扰动，不能泛化；原组采样错误及起始PSS差异使严格峰值/空闲A/B不验收，不宣传内存下降。候选30项原生/分配边界检查、33项世代、300项手势通过后仍按收益不足撤回，生产及原测试七文件逐字节恢复，新试验工具撤下，仅build显式留证。正式重新构建内容与任务前非META-INF全部等值，最终沿用e94a73…正式包；真机拉回同哈希及恢复后基础回归通过。该池化候选冻结，不再作为“下一项待实现”循环；S1b长期内存整体仍开放。**下一项改为截图完成后的worker模糊计算与MAIN排队/绑定分段，只有确认可删除工作再最小修复。** 证据build/quickdesktop-buffer-20261025；具体失败/恢复与测量边界见同日开发日志。

**10/25快捷桌面取消分配批更新：** 已修复请求取走后、Eb.update期间失效仍进入整屏读回的问题；沿现有Capture世代Owner在update后/vc.b前检查。33项ART世代检查、300项手势门禁、旧Renderer静态负控及四项顺序合同通过；正式包V2458A五轮开关/反向短拖/HOME、搜索、设置、Folder和翻页回归通过，PID保持，截图人工核对。v1.6.0/34 SHA256=e94a73f04823769bcb20c293bb50dba263addf9979511a96585b39ba4cb733d6已保数据安装/拉回核对；生产仅Capture与Renderer门禁，不改通用vc.b或图像参数。该检查仅避免检查时已失效的请求；检查后取消仍由原结果丢弃链处理。约26.9MiB是本屏尺寸一次缓冲+Bitmap的理论分配量，不是测得的峰值改善。S1b正常有效截图的DirectByteBuffer复用/生命周期与长期内存仍未验收，不能将本批当作S1b全部完成。下一步只处理该缓冲Owner与生命周期对照，不重开图标微任务。证据build/quickdesktop-preread-20261025，细节见同日开发日志。

**10/25图标资源入口批更新（优先于下段旧判断）：** 真机保存的是RESOURCE/IMPROVED:com.android.BBKClock，仓库512px原图为白盘；诊断与正式包五次保数据重启、毛玻璃→透明ON/OFF→格子实际均匹配该选择。因此上批把白盘直接称“主题缓存残留”、把重启恢复黑盘当正确目标，证据不足，撤销该判断；历史黑盘回退没有被证明是同一个已修根因，后续有现场再按来源核对，不强制黑/白样式。本批实际修复iconOverrideDrawable在sSettingsResources未预热时用Launcher资源表解析设置图标的确定性缺陷，直接复用settingsResources既有Owner；33项资源表边界检查/旧源码负控及49项壁纸Owner检查通过。首次需要可同步加载资源表，未验首装性能或Android9，本批不是冷启动提速。正式v1.6.0/34 SHA256=71d77a968b0a0e943ecfeb570110527bf318860ffd2a7009cfe807c62e361c60已安装并拉回核对，生产本批仅Host入口。被否决Smali候选及临时诊断均已撤回，证据build/theme-icon-refresh-160-20261025。

**10/25真机重连批更新：** 用户“真机连接了，全部帮我解决”重新授权整体推进，Folder性能恢复审查，不再按旧暂停状态阻断。当前设备仅V2458A/API36。实际修复A08新写入/导出/恢复的32位文件名碰撞，旧源码原生负控准确串图，修后29项及导入命名接线1项通过；不自动迁移/删除旧图片，已被旧算法覆盖的图像无法凭现存数据还原。正式v1.6.0/34 c9fd1a158c41fdd1d3b583104ac287aac2516a1619b40bd55254c2f2a345f49a已保数据安装并拉回核对，非META-INF仅classes2.dex变化。20轮有效压力为修前正式包，五轮功能及五次Folder trace为修后包，不混成性能A/B。经典黑→毛玻璃→透明ON/OFF→格子实屏补验，原格子/12宫格/透明OFF已恢复；深浅自选壁纸、全部转场帧与其他ROM仍缺。主题往返后时钟表盘在同进程残留另一外观，进程重启后恢复，另记为未定位刷新问题，不能称整个主题矩阵收口。证据build/finish-real16-20261025；详细测试失败/恢复边界见同日开发日志。

| 范围 | 当前结论 | 剩余动作与停止条件 |
|---|---|---|
| 搜索、图标既有局部修复、快捷桌面触摸终止、加载窗顶栏、四窗口高刷申请 | 保留既有修复和已记录回归，不重复施工 | 仅对新设备或实际复发补对应路径；V2458A窗口120Hz申请不代表魅族验收或稳定120FPS。 |
| A07本地备份→实际恢复→撤销 | 本批API36临时只读模拟器真实SAF导出、界面恢复、界面撤销通过；22应用身份/位置全量一致，2页，0文件夹/自定义图标 | 本地基础恢复闭环关闭。大/旧备份、多用户/分身、云盘/外置卡、复制中撤权、进程退出和硬断电仍未验；同名拒绝为当前安全合同，不把可选覆盖功能混作BUG。 |
| A11/A19整体冷启动 | **未解决**；上一正式真机五次PAGE_READY中位1830ms。逐图已排除同路径重复解码；本批decodeStream五对照无CPU收益，候选拒绝，生产未改 | 不再重复来源/hash/类型/逐图计数及本次流式解码候选。后续优化需新的可删除工作或可复用表示证据与所有权证明；没有收益不提交。 |
| Folder打开卡顿 | **未解决，10/25按新授权恢复审查**；保留既有修复 | 本次一次进程内五打开最大GL回调37.812/12.796/13.303/12.181/11.496ms，首个仍尖峰；非五次冷开或修前后收益。只围绕未解释的首帧工作/缓冲等待继续，不恢复已关闭的PM/hash微任务。 |
| A05 OPPO系统HOME闪回 | **未解决/缺对应设备**；当前ADB无真机 | OPPO重接先将旧临时采样包恢复正式包，再沿同一路径采集；普通APK不拥有系统Recents/Quickstep交接，不重启已废弃截图/固定延时方案。 |
| A04严格16KiB | x86_64 ELF p_align=4096缺口仍开放 | 需原生库构建来源与严格16KiB环境；ZIP-P16通过不等于ELF兼容。 |
| A06实体光影、A18/A24/A25长稳与压力、S1b截图分配/GC | 生命周期局部合同已验；实体可见链、长期内存/GPU/慢网压力及截图性能仍未完成 | 按真实sensor→GL→SurfaceFlinger输出和足够持续运行窗口验收，不用夹具或短时计数替代。 |
| A08自定义图标文件名碰撞 | **新写入/备份导出/恢复已修；旧目录与旧备份兼容读取通过** | 原生已知碰撞负例成立；同一Owner统一v2_SHA256名称，旧路径只读不移动，reset不误删其他身份的共享旧图。已被覆盖的旧图无法自动恢复；旧残留不主动迁移/清理，不承诺向旧APK降级后能读新名称。 |
| 设备/主题/显示完整矩阵 | **未全验** | 魅族60Hz、三星S25U Share、OPPO现场，透明/毛玻璃深浅壁纸与状态栏顺序，12/20宫格/尺寸/刷新率/跨ROM/首装冷缓存仍有缺口。原主APK归档缺失不能称已重新对照解包。 |

本批仅修复restore_worker夹具缺少现有LauncherHomeCompat依赖导致的编译失败；HOME路由在此仍是边界替身，不冒充生产路由测试。导出636+错误UI8+撤销保护85+worker122+预览52共903项通过。真实恢复/撤销后的翻页、底部上滑搜索Maps、设置和HOME通过，crash缓冲为空。PNG解码像素/元信息一致但五组CPU均无收益，拒绝候选。未改生产代码/版本，正式APK仍v1.6.0/code34 bc68b1d9850275746678e482b4f3f1299bd6920e19854e66963daaf60d12db71；不重复构建未变化APK。

证据：build/consolidated-finish-160-20261024/acceptance-result.json、四阶段DB、真实界面XML/截图、read-device.log。设备中断后的旧read-only实例状态已丢弃，本批重启同AVD只读不保存快照重新验收；不使用上一轮尚未完成的SAF弹窗当作已授权。模拟器退出不保存本批授权/测试目录/布局，真机数据未操作。MEMORY.md未改；开发日志已更新。

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

阶段状态：同次几何快照复用已修复并在Android9真机验收，本微项收口。整体启动仍开放，下一项转剩余最长等待，先用已有trace；不把本次Java重载变更拆成更多几何任务，也不把局部18ms当整项性能验收。


## 2026-10-23 第十六批：定位静态节点构建耗时，排除把整段归因GL上传

**10/23第十六批当前：耗时定位完成，生产逻辑净改动为零，冷启动未解决。** 当前无真机连接；复用第十五批真机五份trace，解码区间去重中位169.250ms/运行164.903ms，不能解释1065.776ms整帧。另在已有API36只读模拟器/host RTX3060做5次分段诊断，PAGE_READY3479/2468/2185/2496/2392ms，中位2468；静态节点构建中位1153.187ms，而GL位图上传23.637ms、文字23.358ms。单次细分确认静态合成507.151ms、来源307.359ms、准备143.175ms、键135.944ms；圆框127.220ms含在准备阶段，Alpha扫描62.282ms含在合成阶段，均不可重复累加。该单次不是五样本性能收益，更不能与真机1286ms混比。没有证据支持删除原版绘制/上传，本轮不交付臆测修复。9份临时源码逐字节恢复，重建包全部非META-INF成员与本轮原包相同；正式SHA256=4806115c3ea2b32336497c1b3b5857fcd79ed8089a159c7e2abc6d9ad85ca18f，签名/P16/覆盖安装拉回哈希、13静态区域及5轮搜索/设置/返回通过。第5轮ADB中断后同PID重跑，前4轮与中断证据保留。134项原暂存patch保持，MEMORY.md未改。下一项只核对composeTexture中NormalIconRasterSpec和IconVisualMetrics的同次重复几何解析，量化后考虑复用同一快照；不重开来源三查/旧阴影提取/最终磁盘缓存/无条件页延后实验。证据build/startup-cell-content-20261023。

阶段状态：资源解码/纹理上传归因完成，整体冷启动仍开放；当前正式绘制逻辑保持，未交付新的速度修复。下一步仅限同次合成几何解析的可复用性及成本验证；已有失败候选、Folder暂停和跨设备验收边界继续有效。


**10/22第十五批当前：静态合成的来源/类型/身份改为复用同次快照。** 生产仅IconRasterDiagnostics.java与MaintainedLauncherSettingsHost.java，复用已有ManagedIconSource和来源解析Owner；未引入跨调用缓存、Bitmap持有、线程或数据协议，纹理键与合成仍各解析一次。实际方法+Android原生Bitmap的480键场景/480合成场景共2631检查通过；自定义图完整key+compose链的文件解码/重编码5→2（不代表全部内存PNG解码），改进图来源请求3→2，缺失图仍保留晚到复查；旧源码负控准确失败。Android16真机V2458A同条件各5启动PAGE_READY中位1321→1286ms，GL构建帧wall1093.780→1065.776ms/运行CPU1002.108→976.637ms；未隔离缓存/顺序/调度，不能将35ms全归因或宣称冷启动解决。首屏13静态区域像素一致，首次8页往返无>50ms GL帧；正式包五轮图标/底部上滑搜索/准确settings查询/设置与返回及文件夹开关通过。最终SHA256=c4b70eb3d537921cabb4982559c82f3931e4f9ebc3217fd0061e8f17b10cd9c0，签名/P16/安装拉回哈希通过，仅classes2.dex变化，临时Trace逐字节恢复，129项暂存patch保持，MEMORY.md未更新。下一项定位首屏GL剩余约1秒中CELL_CONTENT_CREATE的资源解码/纹理创建实际调用，先细分归因，不再重复本批来源快照、磁盘缓存或无条件延后页实验。Folder性能仍暂停；Android9/三星Share/全ROM/首装/长稳/真实16KiB缺口保留。证据build/startup-compose-source-20261022。


**10/22第十四批当前：最终纹理磁盘候选已否决，过期纹理键门禁已最小修复。** 在Android16真机V2458A完成原/候选/空缓存/反向原/门禁修复各5样本。磁盘候选稳定命中67张时PAGE_READY中位1183ms，但受控空缓存1423ms，初始原1339ms、反向原1351ms；首次无缓存更慢，因此撤回全部缓存生产改动并清理测试文件，不再将这条路线作为当前首启优化推进。另确认e.s入口仍硬编码v18，当前Java已v30，导致完整纹理键被重复生成；改为调用Java唯一版本判断，普通/过期键仍构建，保留调用方已解析的当前键。实际入口Smali前缀18检查与旧分支负控通过，有完整日志样本键生成138→70；修后5启动1341/1288/1308/1265/1313ms，中位1308，较相邻修前1351约少3%，不能将整个差值视为已完全隔离的代码收益。最终正式包五轮图标/底部上滑搜索/准确settings查询/设置/返回及文件夹开关通过，首次8页往返无>50ms GL帧；修前反向原/修后13个静态区域像素一致。最终SHA256=59031d278cf0c08f345731399d84376bfd362f7862df5766a14e41c4df1393d4，签名/P16/安装拉回哈希通过；永久生产仅e/s.smali与IconRasterDiagnostics.java，本批无新缓存/线程池/数据协议，临时诊断与持久化Owner逐字节恢复，129项暂存patch保持，MEMORY.md未更新。整体冷启动仍开放；下一项核对跨纹理键生成与正式合成的重复来源解析，区别于本批入口门禁、先计数再最小修复，不重复磁盘缓存实验。Folder性能仍暂停；Android9/三星Share/全ROM/首装/长稳/真实16KiB未验。证据build/startup-final-cache-20261022。

**10/22第十三批当前：缓存持久化准入核对完成，未上线缓存改动。** 提取现有来源解析/纹理键方法，在API36只读模拟器两个独立ART进程各跑480组/1684检查，圆框、透明主题、逻辑/物理尺寸、surface、geometryRevision、宫格、分类、阴影、光影、用户及既有来源替换规则通过；相同安装元数据跨进程键一致。删除圆框区分的负控按预期失败。实际Android Bitmap构造出不同像素但相同32位摘要的反例，非Bitmap颜色改变也未进入类名/尺寸/身份摘要，故禁止直接将当前进程纹理键当作持久化完整性协议。旧三列为带阴影成品，data1～3还参与快捷方式备份/恢复，不因当前为空就占用。未改生产源码/APK/DB协议，没有新五启动或安装/功能回归，也不声称提速；冷启动仍未解决。下一项只做既有Owner内版本化最终PNG磁盘候选：先证明来源强身份、表示/版本、负载SHA256、原子发布、容量与恢复失效，再决定接入；不得先把旧PNG当RAW。证据build/startup-cache-validity-20261022，正式APK仍aa336816…，129项暂存patch未变，MEMORY.md未更新。真机/Share/全ROM/长稳/16KiB缺口保留。

**10/22第十二批当前：** 已修图标数据库保存结果误报：data/a/e只在SQLite更新命中/插入非-1时成功，e.s.a失败告警但保留内存字节，异步日志改CACHE_READY避免冒称落盘；没有新缓存/表结构/重试或页面时序改变。实际e/V/U与完整caller方法+Android SQLite的16检查、第二进程3读回、旧writer/旧caller两个负例及补写队列通过；修正了第十批接口变化后过期的队列夹具，PM/源生成/入口仍为夹具，不是完整存储故障UI。实际应用22条缓存跨原/最终各5启动内容哈希一致，旧三列成品与private iconData有读取链，尚无带版本/来源/尺寸身份的RAW跨进程恢复协议，不是已确认写库丢失。最终API36只读模拟器5启动中位2259ms、正式包五轮图标/底部上滑搜索/设置回归通过，未称提速；拼音恢复。当前SHA256=aa336816dd9bb78b0af196bb13a20cc46fd83fad4bccaa5f06340453c4a1ec72，构建签名P16及安装哈希通过，129项暂存保持，MEMORY.md未更改。冷启动仍开放；下一项为现有Owner下版本化RAW/纹理持久化协议及失效/容量/恢复证明，不能直接塞旧成品或重复延后翻页。真机/Top5/Share/全ROM/长稳/16KiB未验；详见开发日志第十二批、build/startup-source-roundtrip-20261022。

**10/22第十一批当前：后续页延后候选已否决并完整撤回。** 纠正“只有前两普通页图标初始化”的旧归因：旧统计只覆盖两页，真机实际9个普通页构造时均提前g.create；约640ms主要在余下工厂循环，阴影预载<1ms，Dock约33ms。原/候选/反向原同诊断各5启动中位1325/847/1335ms，但候选首次向前8次翻页出现7个50～173ms长帧，原/反向原同一路径约11～13ms且无>50ms帧，故未交付。候选仅复用ka既有Hn/oo初始化，没有新增缓存，但确实把工作移到首滑；所有实验/临时诊断源码均逐字节恢复。恢复build.bat/签名/P16/安装拉回哈希及正式包五轮图标/常用应用/底部上滑搜索/设置回归通过；恢复APK与原3b827…非签名ZIP全相同，重建容器SHA256=23a889a4cf370d57ef8f2dbf99edb99c3bc1591002eb737f68ed1fe4856ddb20。129项暂存patch保持，MEMORY.md未更新，系统日志保持开启。冷启动仍开放；下一项核实既有异步源补写是否实际持久化并在下次加载恢复iconRawData，先跨两进程读写对照，不重复无条件延后/旧成品直接套用。完整15样本、9页往返、日志漏采与诊断边界见开发日志第十一批、build/startup-bind-tail-20261022。其他ROM/三星Share/首装/长稳/16KiB等缺口保持，Folder暂停。

**10/22第十批当前：** 已否决将旧 dark/light DB 字节直接复用为当前最终纹理（含旧阴影/几何且缺少现有失效身份）；在既有静态合成调用内借用合格 ARGB_8888 BitmapDrawable，保持 DEFAULT 圆框和所有权边界，无新缓存。cached274/uncached311原生检查、两负例、13静态区域像素一致、构建签名安装哈希及真机五轮图标/常用应用/底部上滑搜索/设置回归通过。Android16 V2458A原/最终五次PAGE_READY中位1351/1361ms，GL wall1139.359/1134.758ms、CPU1038.927/1038.559ms；SOURCE_RASTER计数17→1，但未证明整体提速，冷启动仍开放。无日志与cached-only原型保留，不混入有效组；系统日志按用户授权保持开启，5个诊断标签I，其他设置保持。当前APK=3b8276618a2f220b0fb35f91cc4f855aef2d8563c54518cb913a988ed8b2b9be，129项暂存patch保持，MEMORY.md未更改。下一项 Eb.Vh 内两页初始化后至绑定结束约640ms的真实调用；Folder暂停，其他ROM/三星Share/首装/长稳/16KiB仍待验。完整细节和失败边界见开发日志第十批及build/startup-persisted-icon-audit-20261021。

## 2026-10-20 连续执行与验收总入口（历史快照，以顶部当前入口为准）

**10/21第九批当前：前移候选已实测否决并撤回。** 同一已有2-worker池、一次性最终Bitmap移交，81原生所有权检查/负控/主机167通过，21纹理每次全部接收，11静态区域像素相同；但原/候选/反向原五启动中位1751/2206/1800ms。GL帧虽1129→571ms，DB结束到场景却11→1021ms，候选仍完整重算并等待，不能交付为提速。实验源码和工具只在build/startup-raster-handoff-20261021归档，生产净改动为零；已恢复原0afe93ba…APK及源码/产物，不保留约4.85MiB额外暂存。有效五样本及所有失败原型保留；详见开发日志第九批。下一项核对现有dark_icon/light_icon/ItemInfo.Oe成品缓存的来源、表示与尺寸有效性，再决定是否有可复用结果，不能再重复“单纯前移+join”。冷启动仍未解决，Folder暂停及其他缺口保持；实验前后129项暂存patch保持（初始100项变化发生于捕获实验基线前，未回退外部变化）。

**10/21第八批调查当前：** 已按用户要求对照maintained首次进入链与历史记录，复用第七批五份trace。首屏GL帧中位1507ms/CPU919ms/调度等待479ms，两页初始化1205ms，来源450/阴影429/内容238/纹理创建阶段70ms；非GPU全部耗时，各区间/中位不混加。maintained把阴影图生成/编码放在模型准备链，缺失项3线程，GL优先解码已准备iconData；当前高分辨率RAW/圆框兼容合成仍在GL。两边都已有缓存/前两正常页初始化，未把旧“加载全部页”猜测恢复。未做maintained同机同数据首次安装A/B，不能认定全部速度差或承诺收益。生产/APK未变、无新功能回归，当前仍0afe93ba…；下一项在既有Owner/Composer内验证软件准备前移的来源失效与Bitmap移交合同，不新增并行raw Bitmap缓存、不改GL线程归属。冷启动仍未解决，Folder暂停，详情同日开发日志第八批。

**10/21第七批当前：** 已将Catalog发布后的页面接受/ready、在线与包查询、MAIN分页、保存/恢复和索引ready身份缺口一批修复。生产限IconLibrarySearchPage/IconPackManager，复用现有request/session/generation/epoch，普通IO无自动重试。旧页面负例10组失败，修后15组25检查；实际ART目录164/构建失效31、页面16、主机预览167及正式安装/五轮基础功能通过。实际目录chrome 48项、滚动/离开到系统设置再BACK保留状态；未在真实UI注入失效时序或跨60项边界。五启动中位2185ms，首轮取消仍保留，不宣称整体提速。当前SHA256=0afe93ba559f3b5b4b16a2610071d65e5338acbd5d4ae9158b86bd2de64a51d4。目录一致性已确认链路收口，下一优先项利用现有五份trace定位首屏GL构建剩余CPU热点，不再重复目录微任务；冷启动仍未解决，Folder暂停及原真机/长稳等缺口保留。详情开发日志第七批。

**10/21第六批当前：** 已修IconLibraryCatalog构建中失效被旧instance赋值覆盖的竞态，短发布锁+失效代数，过期构建明确取消；IO仍仅后台单构建者。旧源码负例失败，ART实际Catalog加快照闩锁31项/原目录159项/页面14项/主机队列167项、构建签名安装哈希和五轮基础回归通过。五启动2860/2194/2124/2080/2382ms，中位2194；首轮真实发生失效取消，其他4轮正常ready，没有删除样本；不宣称提速或冷启动解决。当前SHA256=09f59081322a9bc68105c56ffd4fd49dd90bb968a023bb6b7cbfec92d3a00155。下一项已发布目录到MAIN回调/搜索快照的失效校验，区别于本项“构建中”竞态；Folder暂停，真机/Share/长稳等缺口保留。详细边界见开发日志第六批。

**10/21第五批当前：** 目录预热从decodePool移到既有有界indexPool，保留pauseP2；受控目录+单decoder阻塞不再阻止可见loader。主机/ART各167项、两负控、构建签名/安装哈希/五轮功能通过。实际五次ready均转为icon-directory，仍5199项/每进程一次，目录工作约1.1秒。旧/新启动中位2146/2030ms，GL构建帧wall几乎相同，不证明整体启动提速；冷启动仍未解决。当前SHA256=935efbeecd8bd4ed047651f3b44e0f9b144e55295bcd8e0ddec1815279c5c149。下一项目录失效/构建并发发布，先中途失效负例，不重复已收口worker占位采样；Folder暂停，详细边界见最新开发日志。

**10/21第四批记录：** 原L.a相同Alpha遮罩同次复用，仍保留两颜色及不同半径绘制，Alpha4→3/Bitmap生产操作6→5，外层自有padding在成功路径回收。363原生像素组/6267检查、实际引用所有权/完整计数、两负控及58/24/44既有合同、构建签名/安装哈希/五轮基础回归通过。旧/新启动中位2208/2172ms，差异小且调度/缓存未隔离，整体冷启动仍未解决。当前SHA256=be4cb7f019cfef1ac66ba9aa527b606999edab8634cf5fa02fc7385a5560199d。下一项首屏资源装载与后台预热同包重复读取，先建立Owner/包组件/时间线；不重复已收口的颜色/扫描/Alpha局部任务。Folder暂停，详细边界见最新开发日志。

**10/21第三批记录：** 同次未变Bitmap的诊断边界扫描复用，普通3→2；identity/generation保护保证角标或变更仍重扫，无缓存/绘制变更。1007场景8056检查+两负例、LocalCompose246/Uncached289、构建签名/安装哈希/五轮基础回归通过。旧/新启动中位2368/2138ms而GL CPU972.511/1019.287ms，仍不证明整体提速，冷启动未解决。当前正式SHA256=ca7c3c809767cfc0eba9c17d96b116d547472cad7e52254760c3b6c5a17ad266。下一项原版阴影多层alpha提取/遮罩/临时分配，不重复本项采样；Folder暂停。详细边界见最新开发日志。

**10/21第二批记录：** f.d颜色分类的≤64×64采样改为单次getPixels，保留原顺序/分类/大图路径，临时数组≤16KiB。303 Android/实际Smali等值及完整非采样4096→1计数、旧源码负控通过；构建/签名/最终安装哈希/五轮图标搜索设置通过。旧/新/反向旧五样本PAGE_READY中位2450/1761/1734ms，故不归因初始差值、不宣布整体提速，冷启动仍未解决。当前正式SHA256=a4b23942db8647478a6e1bf87161ee8c03f6dd5515a372772532ae8057203711；只改f.d，无新缓存。下一项首屏原图绘制/可见边界扫描/原版阴影中重复工作，色彩JNI局部已收口、Folder继续暂停。详细验证与失败采集边界见最新开发日志；下方首批及10/20 APK哈希是历史记录。

**10/21更新：** 按用户要求用API36硬件GPU只读模拟器核对剩余启动路径。5次PAGE_READY中位2465ms，构建帧GL中位1821ms/CPU1142ms；同buffer锁存距回调约-39至+8ms，无回调后数秒显示等待。就绪后主线程可选任务1–5ms，目录/ICU后台CPU约1秒且关联自动别名，未直接删除；冷启动仍未解决，生产APK未变。已修shell手势工具API36反射兼容，81合同+4兼容场景及5轮基础功能通过，失败采集边界见同日开发日志。此更新不是启动优化完成或真机/物理首帧验收，Folder仍暂停。

用户要求不再逐个小项等待“继续”。后续按关联链路连续审计、最小修复和回归，只有新增设备授权、缺失设备/源码或真实风险需要人工决定时才单列。下方“历史批次”中的“下一项”是当时记录，不是当前并行待办；不重复已关闭的PM/hash/ID微优化，不重测用户确认恢复的A22。

**本轮完成：** A07已从夹具推进到V2458A/API36本地DocumentsProvider真实SAF授权、约3.05MB导出、COMPLETE记录、74个ZIP成员CRC检查、恢复预览回读（9页/2文件夹/70应用）、预览返回取消、同名拒绝及原归档哈希保持。仅暂停备份线程，在真实partial已创建后的复制入口调用现有取消方法，CANCELLED且partial被删除、旧归档不变；这是受控入口取消，不是大文件流中途/云盘断流。真实撤销专用测试目录权限后验证失效弹窗→原目录重选→取消，无自动授权。没有执行“开始恢复”。原撤销快照哈希不变，测试目录/文件/授权已清；备份元信息恢复；用户确认/backups是临时手动选择后，也撤销该新增授权并恢复原“尚未选择”，最终持久授权列表为空。诊断仅临时debuggable标记，正式包已恢复，正式SHA256仍343fd257b9b13abb989ff9d09bcb67ab61cb7d242152260e6755abb7ec937bea。统一证据build/consolidated-acceptance-20261020/，详细失败样本和恢复步骤见同日开发日志。

| 范围 | 当前验收状态 | 尚缺条件或后续工作 |
|---|---|---|
| A07备份本地SAF闭环 | 本机导出/校验/回读预览/取消/同名保护/授权失效入口已验；不是全部恢复完成 | 真实恢复需隔离数据环境，不能覆盖用户桌面；大档/旧档/分身/多用户、外置卡/云盘、传输中撤权/进程退出/硬断电仍未验。安全覆盖尚未实现，现保持要求换名。 |
| A11/A19冷启动与读图 | 已证明的局部重复工作已修；整体冷启动仍未解决 | 需要新的物理首帧/首交互和就绪后负载证据，再决定最小修改；不继续重复同一来源/纹理采样当成新任务。 |
| Folder打开卡顿 | 保留既有修复；按用户要求暂停 | 不默认恢复循环测试，不宣称已解决。 |
| A18内存/长稳、A24/A25压力 | 本轮关联合同回归通过 | 长期PSS/Graphics/纹理增长、真实慢网/GPU争用仍需长稳窗口；A22已由用户清后台恢复，不再单列当前故障。 |
| A04严格16KiB | x86_64 ELF对齐缺口仍开放 | 缺对应原生库构建来源及严格16KiB验证环境；ZIP-P16不能代替ELF适配。 |
| A05系统HOME交接 | 普通APK边界保留 | 系统Recents/Quickstep或独立HOME模块及对应ROM现场；不重启已废弃截图/固定延时方案。 |
| A06实体光影 | 本轮Android隔离生命周期/线程交接/恢复绑定通过 | 手持sensor→GL→SF→可见输出尚需实体视觉对齐，不用隔离计数代替。 |
| A08旧图标文件名碰撞 | 现有32位hash存储合同风险保留 | 需兼容读取/写入/旧档迁移的独立方案；不能只改备份文件名。 |
| 设备/主题/显示总矩阵 | 当前Android16正式包基础回归及V2458A四窗口120Hz修前/后各五轮完成；稳定呈现FPS未验，既有Android9记录保留 | 三星S25U Share现场、其他ROM、完整主题/尺寸/刷新率及长期运行仍未验；原版APK归档缺失。 |

本轮没有新增已确认根因需要修改的生产代码；不为凑“优化”改动画、布局或图标所有权。21组既有主机/Android隔离套件纳入统一回归，正式安装及功能五轮记录见formal-five-rounds.json。MEMORY.md未更新，暂存区保持。

## 2026-10-20 历史批次：SAF权限分类/重选入口已修，下一项专用目录端到端验收

SAF SecurityException及cause归权限失效，rename拒绝不再继续fallback；本地SecurityException/普通IO负控保持原分类。两错误展示入口共享原picker的用户触发重选，不自动grant/重开失败预览。636导出+8UI夹具+85撤销+122worker共851项、构建签名/P16及V2458A/API36基础入口回归通过；实际picker打开/BACK取消，位置未选，无新权限或备份写入。下一批：专用SAF目录导出/回读/取消完整验收，先列目录、测试文件与恢复步骤并取得新增授权。真实provider/撤权/断流/断电/安全同名替换仍未完成，Folder性能继续暂停。

## 2026-10-20 历史批次：上次备份元信息交接已修，下一项目录授权失效分类

两保存路径先确认COMPLETE、后发布元信息；提交尝试后保持文件/日志权威，未完成清候选、已完成补写记录。可选completedFileName支持恢复，重试完成时间不变，pending阻止新journal覆盖。491导出+85撤销+122worker共698项、构建签名/P16和V2458A/API36基础入口回归通过，无真机磁盘/偏好/SAF故障注入。下一批：导出中权限失效SecurityException分类及目录重选入口，先夹具负例再修；不擅改设备权限。真实provider/进程退出/断电/安全同名替换仍未完成，Folder性能暂停。

## 2026-10-20 历史批次：备份日志写后确认已修，下一项上次备份元信息交接

日志FD.sync、finish后逐字节回读确认与Entry延后发布、候选大小预检已改；356导出+85撤销+122worker共563项、构建签名/P16及V2458A/API36保数据安装基础入口回归通过，未在真机注入磁盘/SAF故障。下一批：上次备份时间/名称/URI先于COMPLETE提交，日志失败删新文件后可能留下错误引用，先注入元信息保持负例再修。非事务URI/多provider/断电/安全同名替换仍未完成，Folder性能继续暂停。

## 2026-10-20 历史批次：备份日志失败关闭已修，下一项静默写入失败确认

已区分缺失与坏/不可读日志，write/reset预读保护证据；新操作阻断并释放锁/明确提示，保存错误记账不会吞回调，checkpoint成功才发布预览。314导出+85撤销+122worker共521项、最终构建签名/P16通过；V2458A/API36安装拉回哈希一致，正常启动/图标/设置与只读备份页/底部上滑搜索基础回归完成，无真机故障注入或备份恢复。下一批：AtomicFile.finishWrite静默错误仍返回true，建立负例并复用Restore日志sync/写后回读确认。实际provider/URI非事务/断电/安全同名替换仍未完成；损坏内容保留分析，Folder性能继续暂停。

## 2026-10-20 历史批次：fallback临时文件交接已修，下一项损坏备份日志失败关闭

partial删除拒绝/查询异常时不再丢弃追踪或报告成功，复用既有清理确认函数；247导出+85撤销+122worker共454项、构建签名/P16通过。V2458A/API36保数据安装、APK拉回哈希一致、基础图标/文件夹开关/底部上滑搜索与settings启动/桌面设置返回完成；无真实SAF故障或完整备份恢复验收。下一项：BackupOperationJournal.read损坏/读取失败返回IDLE，建立故障负例并复用恢复日志的失败关闭模式修复。静默持久化/非事务URI/多provider矩阵/安全同名替换仍未完成。Folder性能按用户要求暂停。

## 2026-10-20 历史批次：启动清理失败保留journal，下一项fallback临时文件交接

已修记录在journal内的未完成文件被拒绝删除后仍reset：保留未清理URI/路径和非终态、检查IDLE提交，新备份先执行一次旧操作清理，失败不覆盖记录并释放锁。184导出+85撤销+122worker回归、构建签名/P16通过，无设备未安装。下一批：复现fallback复制成功但partial删除失败仍丢弃追踪，再修成功路径清理确认/日志交接。损坏journal/非事务URI/真实SAF权限与多ROM矩阵、安全同名替换仍未完成；Folder性能暂停。旧“下一项启动清理”以此局部验收为准。

## 2026-10-20 历史批次：封闭破坏性覆盖入口，下一项清理失败保留journal

同名保存现在明确要求换名，Controller即使收到overwrite=true也拒绝，旧文件不删除；UI保留预览并提示改名。完整安全替换协议尚未实现，不能标为已完成。后台目录查询异常/null停止写入。160导出+85撤销+122worker回归、构建签名/P16通过，ADB无设备未安装。下一批：复现provider拒绝删除后journal却reset，最小修复保留待清理URI/状态，再跑隔离回归。真实SAF/并发目录改动/URI非事务间隙/损坏journal仍待验；Folder性能按用户要求暂停。更早条目的“下一批同名替换”以此范围限制为准。

## 2026-10-20 历史批次：SAF新文件失败清理已局部修复，下一项同名覆盖保护

Owner清理partial/第二目标、跟踪真实URI、取消归CANCELLED及关键checkpoint失败拦截已改；133新provider夹具/真实JVM IO检查+85撤销+122worker通过，构建签名通过。ADB无设备，未安装或访问真实备份。下方旧“下一项SAF导出”本批仅完成上述边界；同名覆盖提前删除existing为下一批P1，provider拒绝删除/非事务URI间隙/日志损坏/真实SAF重启与多ROM仍未验，不称全部取消安全。Folder性能暂停，旧撤销和圆框修复保留。

## 2026-10-19 最新：旧撤销快照取消保护与操作锁修复完成局部验收

preparing_TOKEN候选隔离，成功后FD同步/SHA校验/Os.rename发布，Guard和首帧cleanup共享恢复；内容等值token可释放正确owner，旧token不释新owner。85新JVM+144 checkpoint+122 worker及Android9隔离112检查通过，构建签名通过，未安装或恢复用户桌面。下方旧“下一批处理替换旧撤销包”已由本批收口；完整真实归档/SAF/硬断电/空间极限/多ROM仍未验。下一项备份导出到SAF的写入中断/取消及未完成文件清理。Folder性能继续暂停，圆框修复保留。

## 2026-10-19 当前：未匹配圆框已按用户最新期望修复；继续恢复取消边界

实际effectiveType=DEFAULT回退原图遵循圆框开关，命中managed不加框；334/59/289隔离及Android9正式安装一次功能回归通过。checkpoint144/worker122通过，备份生产无新增修改，但createRollbackAndTransition先删旧rollback_latest再创建新快照的取消/失败边界尚未解决，下一批优先故障注入并最小修复。下方旧“下一项清理审计”由本条细化；Folder性能仍暂停，真实恢复/多ROM长稳未验。

## 2026-10-19 用户调整顺序：Folder暂停，当前A07备份恢复

按用户要求停止Folder性能循环采样，保留已验证修复，打开前CPU等待未解决。下方旧“当前/下一项几何复用”是调整前计划，暂不执行，不重新采样该链。

A07本批已修缺主题包回退commit失败仍报成功，31新检查/5场景及144/122/25既有回归通过，构建签名通过；未安装或恢复真机数据。本批继续修复纯文件夹页预览漏计，52预览/25偏好及真实Android隔离SQLite120项通过；只修Reader、不改布局导入，未安装或恢复用户数据。结构校验批已补预览Topology入口及源/DB查环，143真实Android隔离SQLite+144 checkpoint通过；孤儿引用原写前保护仍保留。下一项取消/失败后临时文件、撤销快照和操作锁生命周期；真实归档/SAF/中断/多ROM整体验收仍未完成。详见同日开发日志。

## 2026-10-17 总体进度与剩余任务入口

结构盘点、重点执行链审计和五份主报告已完成；全项目功能/性能矩阵仍未收口。按A01–A25主登记编号去重：15项已完成局部修复或维护及对应回归（A01/03/09/10/12/13/14/15/16/17/20/21/23/24/25），2项部分完成（A11/19），6项未闭环（A04/05/06/07/08/18），1项历史现象并入内存压力观察（A22，用户确认清理后台后恢复，不再单列复测/修复），1项不可达生产候选撤回（A02）。A12旧legacy标识同号备忘不另计。编号含父子关系，局部通过不等于跨ROM验收，不能换算成可靠的整项目百分比。

| 顺序/范围 | 剩余工作与完成门 |
|---|---|
| 来源/首轮纹理阶段：排查收束，冷启动未解决 | 有/无缓存来源局部复用已完成；补写与首轮纹理无新增可安全删减候选。硬件/SwiftShader同包各5次对照确认纹理分配等待显著受后端影响，不能当正式APK重复创建。当时基线b09ead0c…；A25修复后当前正式为88bab291…/v1.5.8/33。本阶段停止循环采样，整体启动/真实可见帧保留未验收。 |
| 启动及内存/真实返回 | 整体冷启动稳定收益、物理首帧/首交互、PAGE_READY后后台负载；用户已确认清理后台后返回正常，A22不再单列当前故障或要求解锁复测；A18压力/ABE阈值及长期PSS/Graphics/纹理增长作为后续长稳边界。 |
| 图标队列：A24局部修复已回归 | P1预取共享给P0后误裁剪、全局淘汰中途加入旧批次已修；JVM/Android9/16各161项及API36最终5轮滚动通过，真实全GPU压力/长期争用仍未验。 |
| 图标库边界：A25局部修复已回归 | 新下载结构/CRC/Deflate坏图和超限镜像中断已修；37/44/44项及分类/网格各5轮暂停恢复通过。显式同名替换/跨进程文件与404标记通过；真实线路慢网、历史缓存/完整语义及三星Share现场仍未验。 |
| 来源失效审计已完成；搜索失败归因由10/19下行修正 | 10/19最终5297d96f仅改IconPackManager/reset候选和Host所选包事件覆盖全局跟随者；18边界、64/12既有检查、构建签名/安装hash/53暂存保护通过。API28 X21A修前db14/修后各5次同Folder、5对静态像素相同，5轮图标/设置BACK同PID通过。搜索开关开启但Dock上滑未打开，查询未执行，下一项优先同基线定位入口；不得记完整回归通过。外部文件与异步来源缺完整失效屏障，保留来源校验、不新加键/Bitmap缓存。本次核对收束，不重复PM/hash/ID微优化；入口定位后回到Folder输入至首个运动buffer的CPU阻塞。长帧仍在，Folder/冷启动未关闭；真实图标包更新/选择矩阵、本轮API36/多ROM/长稳未验。 |
| 10/19用户优先插入：DEFAULT圆框方块白底已局部修复 | Renderer v8延展近方形实心PNG的原边缘颜色，保持原完整图案矩阵，不裁主体/文字；透明/不规则保守回退，自适应/managed路径保留。59项Android Canvas、11实际源对照和API28五轮Folder/设置BACK通过，5d2ac17e安装；原53暂存/配置保留。复杂纹理/多ROM未验，不称语义分割或全矩阵完成。之后回到上行Android9搜索入口失败，再继续Folder初始阻塞。 |
| Android9搜索测试输入已修正，五轮通过 | stock adb swipe逐事件更换downTime，触发原异常流保护；诊断/AOSP确认，仅修shell回归工具，生产代码未改。正式5d2ac17e/API28五轮Folder、底部上滑、实际查询/结果启动、BACK及桌面设置同PID16664通过；CANCEL/短滑/坏流及下次正常流通过。81隔离检查、安装hash/诊断撤除/53暂存保护通过。历史未打开不再归为已确认搜索业务故障；下一项定位输入到首个运动buffer CPU阻塞，不重复已关闭微优化；Folder卡顿和冷启动整体仍开放。 |
| Folder同次几何计算重复已局部修复，绑定细查由下行收束 | 两现有Java Owner在已验证布局后复用本次几何计算，无公式/动画/跨帧缓存变化。839几何bit对照、mode查询2700→1548，正式4b1/API28两次预热后修前后各五样本，最重帧CPU中位85.196→76.594ms，仍有94ms长帧；五对静态像素相同，五轮Folder/实际搜索查询启动/桌面设置BACK同PID21272通过。签名/安装hash/诊断撤除/本轮97暂存保护通过。下一项沿cell-create→folder-content-create→g.Ba同步绑定细分剩余开销；不称Folder/冷启动已解决，不重复已关闭微优化。 |
| Folder绑定细查收束，后续时间线见下行 | 4b1/API28五组诊断确认9格实际创建一次；另9次create入口原iH早退共约0.05ms，2项应用各一次纹理/键解析，无新重复绑定证据。动态同步/阴影合计不足1ms、文字构造约2–4ms；生产0修改，正式包恢复hash一致、五轮Folder/查询启动/设置BACK同PID27301、100暂存保护通过。下一项串联触摸UP→同步准备→GL/EGL提交→首个运动buffer；不重复坐标/hash/ID微优化或为无新根因删原流程，Folder/冷启动整体仍开放。 |
| 当前：创建当帧首步漏门已修，下一项几何复用核对 | API28五次证明输入回调内创建Folder使原预输入门漏判，首步63.6–108；Ra.T/Eb最小补门后五次均约20，346/64检查及旧源码负对照通过。正式1bb4五对静态像素一致、签名/安装hash/100暂存保护通过，功能结果见同日开发日志补充。正式五次仍72–84ms GL长帧，不称Folder或冷启动解决；下一项核对固定几何结果的既有Owner、重复适配成本及尺寸/方向/布局/主题/图标文字尺寸失效，先证明再窄改，不循环PM/hash/ID微优化，不新增无所有权证明的Point/Bitmap/完整场景缓存。API36高刷/动态图/九实际应用/多ROM长稳仍未验。 |
| 系统HOME和实体光影 | A05系统手势/Quickstep闪壁纸，A06手持Sensor→GL→显示及主题/动态交接；普通APK边界和独立模块验收分别记录。 |
| 恢复/分身/存储 | A07真实大备份/旧档/SAF/中断恢复/分身/多用户；A08哈希文件命名碰撞为独立兼容风险，不无证据迁移用户档案。 |
| 设备与显示矩阵 | Android8–16及17前瞻、多ROM；720p/1080p/2K、12/20宫格、50/100/150%图标、60/90/120/144Hz、普通/透明/毛玻璃及不同数据量，按风险分层覆盖；A04严格16KiB原生库不能由zipalign或兼容模式替代。 |
| 累积性能与长稳收口 | 同会话五样本、帧分布/长帧、CPU/GC/PSS/Graphics/IO/后台唤醒/耗电与长时间运行；以失败样本和未验项保留边界，不把一次烟测写成全功能通过。 |

既有S1/S2/S3局部收益、F01–F15修复及图标库实现不重做；P1–P4/S6最终状态仍由上述剩余验收决定。详细证据保留在性能、功能和问题清单中。2026-10-17用户再次纠正：清理后台后返回已恢复，不继续A22独立复测；硬件GPU对照结束后转图标可见任务队列压力/取消与旧回调边界。

## 2026-10-17 单次键生成来源复用完成局部验收

现有ManagedIconSource携带本次Drawable/type/identity，CUSTOM同图解码及PNG编码隔离计数4→1，IMPROVED来源请求2→1；480组/1093项在Android9/16通过。受管未命中仍重查类型/身份，覆盖图标包在回退时变可用；不跨准备/合成缓存Bitmap。最终包0d9794b8…仅classes2.dex变化，原53项暂存不变。API36紧邻基线/最终各5次PAGE_READY中位5495→4710ms，但初始基线4390ms、长样本9104ms揭示明显波动，不认定整体稳定提速；两页像素零差异，5轮搜索/设置/图标查询返回同PID7279。

**下一项：量化prepareStaticSource→composeTexture的剩余重复来源请求及生命周期。** 先确认是否同条目、同版本RAW来源，区分DEFAULT圆框已准备Bitmap与受管RAW，明确持有/回收及来源切换失效，再决定是否最小复用；不能把本次短期结果变成常驻图像缓存。冷启动整体、A22首次返回重建、真实压力及全ROM/长稳继续开放。

## 2026-10-17 来源哈希/有效性/绘制核对完成（只读）

重复来源请求成立；IMPROVED后续请求可命中既有Bitmap缓存，不能计作每次磁盘解码。CUSTOM的类型/身份及正式来源读取调用完整redirect接口，每次文件解码/PNG重编码，存在明确冗余。最终纹理命中前仍计算来源内容hash、加载及扫描像素；旧trace已证明该链实际出现磁盘解码和getPixels，但无参数/同条目精确次数。详见性能报告本日顶部。生产源码/APK未变，未新增性能收益结论。

**下一项：在现有Host/ManagedIconSource内验证单次来源解析结果供同一次纹理键hash/type/identity复用。** 先提取生产链负对照、同组件/用户/sourceId计数，覆盖CUSTOM、受管缺失/损坏、来源替换及DEFAULT旁路；再最小修改，五样本及键/像素/图标/搜索/设置/返回回归。不创建新Resolver或常驻Bitmap缓存；准备/合成之间更长跨度复用须另证生命周期。原整体冷启动及A22首次重建风险仍未关闭。

## 2026-10-16 用户恢复后继续A19：来源标识复用已完成局部验收

按用户最新指令继续修后采样，定位identity内部重复type解析/正式来源检查，现有Host包内重载复用紧邻effectiveType，Raster两处改调用；不改纹理/颜色算法、几何、原阴影或HOME。720组/3690项负对照、Android来源481及相关回归通过；正式e3d84deb…包真机同条件5样本PAGE_READY3048→2827ms、scene2271→2030ms，两页像素零差异。初始功能首轮Activity重建后自行SIG9单列保留，随后补5轮逐轮同PID3629；API36同包5次兼容回归中位5099ms，不能宣称整体冷启动/全部返回问题关闭。

**接下来：核对resolvedSourceHash、正式来源有效性检查与实际绘制是否重复读取同一图。** 先在现有Owner量出具体重复解码/调用数，不能新建并行缓存或凭热点排名修改分类/阴影；确认后最小修复，再同条件5样本、像素、图标来源/搜索/设置/真实返回回归。首轮重建原因、整机压力/ABE触发条件、全ROM/长稳仍独立保留。下方旧“暂停”仅代表用户本次明确恢复任务前状态。

## 2026-10-16 当前阻塞：Android9外部应用返回冷启动

**最新状态修正：用户清理后台后报告返回正常。** 只读快照当前可用约3.40GiB、Launcher PSS约204.7MiB，其中图形约111.4MiB。现象已由用户恢复，根因仍未关闭；缺清理前/强停瞬间压力数据，不确认泄漏或ABE内存阈值。下一项优先审计现有Bitmap/纹理/缓存内存所有者和可复现持续增长，保留原动画与交接链；不重复设备策略试验、不将当前单次快照当长期内存正常证明。

**最新对照：** 获授权临时自启动开启5次、恢复关闭5次均换PID，已确认恢复关闭。用户提出交接动画实验回退疑问后，安装更早的10/11实验前50a8befb…APK，5次仍换PID；J.onPause/onResume和Eb.onResume与现行去行号后相同，未见主动冷重载变化；现行HomeCompat与10/14实验前备份字节一致，API34/36实验不适用API28。最新5e1b3d1b…包已恢复，不能称为已修复。下一项改为只读查清ABE强停的具体触发条件及用户此前正常状态的变化点；不要重复把已失败的自启动开关当作修复方案，后续设备策略实验须按附件授权。

用户反馈返回桌面出现加载动画后，暂停下方冷启动热点优化顺序。vivo真实点击系统设置→HOME，新5e1b3d1b…及优化前旧4944e939…各5次均换PID；用户授权临时开启日志后，当前5次am_kill均明确stop by com.vivo.abe。系统自启动开关关闭仅是观察值，尚未证明因果，未授权不调整后台策略。

**下一项：查明ABE强制停止触发条件并恢复正常返回。完成门：** 可恢复单变量对照明确因果，5次真实应用返回同进程且无冷加载，图标/搜索/设置回归通过，临时日志及测试设置恢复。未满足前不继续MainView.oh等性能改动，不通过隐藏Loading或生产保活规避。详见DEVELOPMENT_LOG的ANDROID9_EXTERNAL_RETURN_BLOCKER；当前仍未修复，旧包也复现不等于用户之前的正常状态已解释。

## 2026-10-16 真机采样后第二个最小修复

两次真机自采样未支持沿用SwiftShader的GL创建瓶颈假设，确认GL内旧PNG/三套图标缓存重建耗时。复用现有prepareUncachedStaticSource和页面就绪后的有界补写，移除其DEFAULT专属判断，仅让有正式来源、无旧字节的静态受管图标走已存在路径；不扩大DB阶段延后、不改原GL/阴影/MD5/数据格式。新负例与相关回归通过，正式包5e1b3d1b…真机同机5样本PAGE_READY中位6315→4553ms，29项补写全完成，五轮搜索/设置/图标及补写未完成时即时搜索通过；API36同包5次兼容回归中位5028ms，不作跨会话提速声明。

**下一项：修后约4.5s关键路径重新采样。** 重点核实MainView.oh阴影纹理预载/图像解码、颜色分类的重复或无效工作；不沿用修前热点排名直接改。**完成条件：** 具体调用/次数或可复现负例，同机同数据五样本、来源/视觉/搜索/设置回归；就绪后的后台负载和首交互帧仍需测，冷启动整体尚未关闭。该项之后再推进文件夹首开长帧。

## 2026-10-16 A19 首个最小修复与下一项

已定位并消除DEFAULT圆框Bitmap在合成阶段被弃用Drawable的重复加载，API36前两页21个静态图标每轮加载42→21，局部加载中位283→142ms，桌面区域像素一致。481项Android resolver及图标合同/阴影/补写回归通过；正式包4979fc9b…在API36、vivo均完成同条件5次启动。API36整体PAGE_READY基线续组中位5378、候选5881ms，未证明整体提速或不退化；vivo当前图标未命中DEFAULT圆框条件，复用0次，同诊断基线6392/最终候选6283ms不归为该分支收益。详细全样本、安装失败留证与回归以性能报告/开发日志为准。

**下一项：真实GPU上的首次纹理/Shader创建定位。** 原完成事件绑定后0–2ms已入队；API36一次ART采样约1.92s停留RenderManager.r/SceneNode.render，重点glGenTextures和Shader创建/链接。软件GPU与采样开销限制仍在，先在真机确认调用/重复次数后才窄改。**完成条件：** 可复现的重复或无效工作证明、同机同数据5次对照及来源/像素/搜索/设置回归；不能提前释放Loading或绕过原GL完成门。之后再进入文件夹首开长帧。

## 2026-10-16 Android 16 补测与后续入口

同一2b8d3fad…包在API36/4KiB、12宫格黑主题、SwiftShader只读临时副本完成5次冷启动及5次同进程系统设置返回。PAGE_READY中位5221ms，DB256ms、scene task到bind2413ms、bind到page ready1950ms。前置SystemUI弹窗/窗口标题脚本失败保留，正式组未按速度筛样；不同设备/布局不与vivo作收益比较。下一项A19除来源/阴影子调用外，同时定位绑定后完成区段真实工作；拿到耗时/次数或复现证据再最小修复，同机同数据5次与图标/搜索/设置回归是完成门。详见性能报告，冷启动优化尚未关闭。

## 2026-10-16 本批完成与下一项

本批：2b8d3fad…包在vivo X21A完成持续日志的5次进程冷启动、5次桌面点击系统设置返回及5次同进程桌面设置返回。PAGE_READY中位5509ms，DB区段177ms，GL scene task到bind中位4747ms；前两页来源解析1992ms、阴影993ms。外部应用5次均被系统am_kill/stop by com.vivo.abe转成冷启动，未记热恢复PASS；内部设置5/5同PID。未改生产代码/用户后台策略，详见性能报告及开发日志。

**下一项任务：静态图标来源解析与阴影准备的子调用定位。** 从现有e.s.a→IconRasterDiagnostics及原阴影Owner进入，先细分图像解码/资源读取/重复来源判断。**完成条件：** 可重复负例或具体耗时/次数证明；仅消除真实重复工作；同机同数据5样本对比、图标合同及真机来源/搜索/设置回归通过。之后再转入文件夹首开长帧；vivo后台策略作为独立兼容边界，不靠新增Service/保活/延时遮盖规避。

## 2026-10-16 元数据读取优化及真机连续回归

继续A11重复图像处理项：四个纯名称/模式消费者改用现有元数据接口，42项Android隔离和29组主机回归通过；受控512PNG、24个名称读取的5轮wall中位2314.076→0.773ms、图片IO24→0，只证明局部重复工作消除。2b8d3fad…正式包已在vivo保留数据安装、拉取hash一致；5轮Dock搜索、结果启动系统设置、HOME、图标列表包名查询及往返通过，同PID12016。按用户要求测试以真机为主；短暂16KiB/API37只读副本已停止，严格16KiB原生库、三星现场及P4完整矩阵不随局部通过而关闭。详细见开发日志、性能报告、回归报告本日新增节。

## 2026-10-16 图标库页面补修

接续P1图标库正确性，已复现并修复防抖/后台查询被暂停后恢复只绑定旧结果、目录失败时重试文字隐藏。生产页面方法负例及修后6项通过，目录10项、预览61项通过；vivo X21A保留数据安装并拉取校验ca263178…正式包，`weixin`真机8个搜索结果和图标可见。暂停窗口与故障目录的真机注入未做，不标P1/P4整体验收完成。此前搜索页、图标补载与Dock修复保留；没有改变SMEngine或增加性能收益宣称。详细见DEVELOPMENT_LOG和FULL_FUNCTION_REGRESSION_REPORT本日新增节。

## 2026-10-16 审计后续与当前验收边界

继续10月15日审计及此前P2/P4计划，修复已复现搜索LRU失载、旧PNG缺失、暂存启动补写被P2丢弃和Dock起点排除；没有为无测量依据的性能候选改变SMEngine、动画时机或系统HOME路线。28组离线、8组真实Android隔离检查及vivo X21A正式包搜索/常用图标/设置/应用往返通过，最终APK f9e30adc…；临时权限和常用应用开关已恢复。详细证据见DEVELOPMENT_LOG与FULL_FUNCTION_REGRESSION_REPORT本日追加节。三星S25U、整库恢复/分身、全主题/宫格组合、手持光影/解锁与长稳仍待验，P4/S6不标整体验收完成，首次启动性能阶段不以此关闭。MEMORY.md未更新。

## 2026-10-14 首次加载当前进展

已完成启动分段、普通DEFAULT缓存延后、首次刘海缓存校准和启动应用放置批量落盘；圆框外观保持等价。最终API37五轮空目录页面就绪中位9325ms、最坏12144ms，**首次加载尚未完全解决**。下一步边界是数据准备、页面/纹理构建、场景绑定到原GL完成事件的1.56–2.57s；保留Loading/原SMEngine/动画，不直接提前释放交互。最新APK、修改范围及可重跑证据见DEVELOPMENT_LOG的STARTUP_PLACEMENT_BATCH_AND_TIMELINE及ANDROID17_STARTUP_AND_ICON_AUDIT_20261014.md顶部。MEMORY.md未更新。


# Smartisan Launcher Original Port
## 原版代码复用、BUG 修复与性能优化专项计划

## 2026-10-08 审计后修复顺序与防回归门（计划，尚未实施）

本节以当前工作树（包括已暂存及未暂存内容）和 10 月 7 日开发日志为起点。旧 `docs/build/LAUNCHER_FIX_AND_OPTIMIZATION_PLAN.md` 是历史副本，不能覆盖本文件的当前状态。以下“待修”不表示已经修改或真机通过；每阶段只处理一个现有 Owner，阶段间重新记录源码／APK hash 和验证结果，不覆盖用户已有暂存内容。

| 顺序 | 当前证据与改动边界 | 完成门（缺一不可） |
|---|---|---|
| P0 固定现状 | 分开记录 HEAD、暂存、未暂存及设备 APK；对照 `DEVELOPMENT_LOG.md` 最新状态、原 APK／`clean_launcher`／maintained，确认用户最近改动是否已覆盖旧审计问题。锁屏、Folder、快捷桌面、图标库各固定一条可重放路径。 | 有同一构建的源码与 APK hash、设备／ROM／宫格／主题／数据状态、复现步骤和第一异常；旧记录与新证据冲突时标明被取代。无需清除用户数据。 |
| P1 图标库正确性 | 先在 `IconLibrarySearchPage` 复现暂停时待执行查询丢失、恢复后旧结果与当前输入不一致，以及目录失败时重试文字不可见。只在现有查询世代和 Loading View 内修复。随后在 `tools/icon_library.py` 验证截断／损坏 PNG 不可入库、同名图片换内容后的目录修订与缓存失效；在现有 `IconPackManager` 隔离单个坏包，保留其余包可用。 | 每个问题有修前失败、修后通过的行为断言；取消／恢复、快速改词、分类返回、坏包＋好包、图片替换与重新进程均通过。源审计失败应阻止生成，不能静默丢资源。 |
| P2 预览队列及回归门 | `IconPreviewRepository` 的 96 项阈值目前仅淘汰 P1/P2，P0 连续进入仍可增长；先测真实可见 Cell 最大并发、队列峰值、取消与回调时序，再决定保留／合并 P0 的现有调度策略。把 P1 的生产行为负例接入现有 `tools/tests` 与构建前门；构建后核对实际二进制 Manifest、签名、版本和 APK hash。 | 同一 session 压力下队列／内存有可解释上限，当前可见图标不丢失、不闪旧图、取消后不回写；负例在修前确实失败。每次触及图标库、主题、解锁、快捷桌面或恢复 Owner，运行该 Owner 的既有回归及共享冒烟矩阵。 |
| P3 流畅度证据与窄优化 | 延续 S0–S6，不重做已完成的 S1a／S2／S3／F01–F15。优先核验锁屏 Perfetto 是否实际包含 Launcher／窗口／首个可见帧，再对齐关屏、Resume、准备、PLAY 和解锁前静止段；普通／兼容起播时机、120ms 预滚和动画时长冻结。Folder 首开长帧、快捷桌面 readPixels／S1b、图标候选峰值分别采样，确认首个重活 Owner 后才单项优化。 | 相同设备、APK、数据、12／20 宫格、主题及刷新率下各至少 5 次，记录中位数与最坏值、帧／CPU／内存／GC 和录像；保持原版视觉、手势、动态效果与数据新鲜度。无有效样本则保持现状，不以构建成功或局部 CPU 数值宣称整体流畅。 |
| P4 累积验收与文档收口 | 按现有 S6／全项目回归矩阵检查冷启动、HOME、锁屏／解锁、12↔20、普通／透明／毛玻璃、四指主题、Folder、搜索／T9、图标替换、快捷桌面首次打开／取消、备份恢复与分身；区分可自动测和需真机测。 | 每项记录 PASS／FAIL／NOT TESTED 及 APK hash；失败仅回退所属小补丁并重测。最终状态更新本文件与 `DEVELOPMENT_LOG.md` 顶部及当日详情，长期稳定规则才进入项目 `MEMORY.md`，不创建新的流水文档。 |

施工时遵守 `ICON_RENDERING_CONTRACT.md` 的四层 Owner、`QUICK_SEARCH_FINAL_STATUS.md` 的冻结边界和 `MODERN_ANDROID_LAUNCHER_MODEL_REFACTOR.md` 的唯一 Package/Profile/Model 状态源。10 月 7 日已撤回的光影 atlas／mesh／直接绘制试验、历史标记【已废弃】的解锁或图标方案均不得当作候选修复。快捷桌面冷重载后首次打开已有有限真机证据；真实备份恢复与跨 ROM 仍是待验项，不能因 P3 再次改变其原手势或背景交接。

## 2026-10-05 当前暂停点与验收边界

用户要求“先这样，更新文档”，代码处理停在当前版本；本次只更新文档，不继续构建、安装、操作手机或调整参数。最新事实以DEVELOPMENT_LOG的“图标搜索界面与锁屏／解锁：停止时的当前状态”为准。

| 范围 | 当前状态 | 尚未验收／后续约束 |
|---|---|---|
| 图标搜索与候选（S4相关） | 已实现元数据索引、可回收网格、网络／预览线程隔离、有界缓存；本机分类真分页、原设置样式、结果数量及返回已检查 | 中文／分类未全量完善，真实跨应用持久化与恢复、20个真实安装包、长稳／跨ROM未全覆盖；不能再把S4整体写成尚未实施，也不能写整体验收完成 |
| 微信返回误播 | 已取到后台USER_PRESENT晚消费证据并加入现有Owner资格保护；一个诊断包获用户确认，正常兼容解锁也有记录 | 后续准备流程多次调整，最终包完整误播回归待补；不能用系统设置未复现证明微信正常 |
| 锁屏卡顿／解锁前静止 | **未解决、未完成性能验收**；用户最新反馈优先 | 普通与兼容起播时机冻结，不改变原120ms预滚、焦点门或动画时长；播放方法相同不等于首次可见画面时序相同 |
| 新Perfetto样本 | trace已保留本地，首次查询未返回Launcher进程／切片 | 必须先验证采样有效性，再对齐窗口与真实动画帧；不能据此宣称提速／根因已确认 |

先前S1／S2／S3的实测收益仍只对其原样本有效，不能延伸为本轮锁屏／解锁通过。准备链恢复与再次调整未获得稳定最终验收，后续必须先读当前代码与包hash，不继续按中间试验结论施工。MEMORY.md未更新；既有暂存／未暂存内容保留，本次不暂存、提交或推送。

## 2026-10-04 流畅度专项方案：功能与原版表现优先

状态：**已开始实施，首批正式包已安装；完整矩阵未全部验收**。本节对应用户要求“制定完整方案，看下怎么优化流畅度，但是不要影响正常功能操作”。它补充本文件旧阶段计划，不重新编号或重做已完成的阶段，也不将 F01–F15 稳定性修复撤回。最新实现、正式性能样本及未验范围见 DEVELOPMENT_LOG 的“2026-10-04 流畅度优化首批实施”。

| 当前项 | 实施状态与所测结果 | 后续边界 |
|---|---|---|
| S0 | 基线 APK／源码保存；相同普通主题12宫格动作复测，剔除采错页面的样本 | 冷启动、多主题与跨ROM基线仍需补足 |
| S1a | DOWN 不截图；原版确认分支授予资格，背景完成后揭露，GPU读回携带 generation。2026-10-05纠正多页13／10被一律拒绝的回归：单／多页首页沿原版门进入，截图前CANCEL，终止不重复派发，未呈现宿主／窗口失败清理。97项触发／模式／归属及9项世代检查通过；单／多页各10次图标起手、取消／反向／第二指、非首页返回及Folder／设置响应已测，详见10月5日日志 | 历史冻结未全部捕获同等现场；实际20宫格、多主题、四指及完整系统打断／生命周期矩阵未全覆盖，不标全阶段验收 |
| S3（比例校正热点） | S1复测仍有长帧后，定位重复反射并缓存元数据；71项几何检查通过。正式5轮10组切换，最大 GL CPU 28.011／15.161／13.751／13.963／14.897 ms；基线52.999 ms，所测 >33.33ms CPU 长帧由4降至0 | 实际20宫格／透明／毛玻璃／倍率／编辑拖动回归待补；未缓存场景结果、未改引擎 |
| S2a/S2b | 已实施资源数据复用、主题共享状态及后台刷新、同 Activity 已离场 MAIN 复用；434项 Android 资源、23项主题状态、67项页面生命周期检查通过。正式包10轮设置往返，BACK处理最大7.783–12.063ms，基线29.171ms；完整结果见最新日志 | 初次主题状态扫描仍在MAIN以保持首屏准确；全设置／下载安装／配置变更／overlay完整真机矩阵未全部验收 |
| S5（搜索资源准备） | 原搜索资源提取复用已有队列，在真实首帧后预热；不更改Loading、恢复守卫或首帧交接 | 仅此非关键准备项已实现，不代表启动／HOME／Loading阶段验收 |
| S1b、S5其余项 | 尚未实施；S4后续实现与验收边界见本文件2026-10-05节 | 继续按实际Owner逐阶段定位，不能用设置返回收益替代截图缓冲、候选预览及Loading验收 |
| S6 | 本批标准构建、签名／对齐、保留数据安装与hash、正式包双向路径和日志检查通过 | 全范围回归仍待完成 |

首批性能正式 APK 为 v1.5.8/code33，SHA256 `3BF81D29ECD21E033874232949C1E512FE2EC90D2BAE75DA3316AB83FA1CA827`；后续触摸归属修复包 SHA256 为 `84F06AADC57E99F3D6DD23E71759E1EB63B222706BDE6ED843F047AFDA57FF7A`，vivo V2458A/Android16 已保留数据安装并拉取校验一致。最新现场及验证见 DEVELOPMENT_LOG“快捷桌面与单页／多页触摸归属修复”。临时 Trace 包装已移除。普通帧 p95/p99 未证明改善，当前收益是减少已定位的切换尖峰与误截图，不代表整个项目的显示帧率。S3先处理同一多页复测中确认的热点，S2资源／转场没有混入该补丁。

2026-10-05的现行触摸修复包为v1.5.8/code33，SHA256 `083CD9C8E1E149EB92C5F87D51C11A8F1620D9936ED7C2CD2B61F8E151031393`，保留数据安装与拉取hash一致。原版核对证明多页首页可进入；上一条历史包的模式13／10排除规则不再适用。最终包单／多页各3次、反向取消、Folder／设置返回的18项窗口复验及9次请求的取消先于截图日志通过；更完整首轮矩阵与剩余边界详见DEVELOPMENT_LOG的10月5日记录。

S2后续正式包为v1.5.8/code33，SHA256 `DB2C5CF79F051C5CDEDC3DDC88F7E88A4FC5C43DC76001977D3C0CA7C009BE99`；已在同一vivo保留数据安装并拉取校验。原动画时长／曲线、光影及主题参数保持。10轮结果限定主题、应用图标、翻页动画页重复打开与返回，不代表所有子页或整个项目已优化完成。

2026-10-04后续建议已作可行性复核，详见DEVELOPMENT_LOG“后续流畅度建议可行性复核”：初始化迁移已有持久完成门，调度去重仅属有限后台整理，尚无滑动收益证明；候选已有优先级／缓存／尺寸采样，应先量完整批次的队列占用，保持完整列表单次发布与下载副作用；S1b缓冲复用不能减少readPixels且可能增加闲时内存，需实测再保留。正式主题详情70张源图仅626×1356／556×1204，不采纳笼统普遍降采样。搜索资源预热锁等待、首次主题状态及共享队列竞争需补证，Loading与恢复安全门不动。本次为审计，未实施上述后续改动。

### A. 目标、基线与施工约束

目标是减少点击后停顿、动画中的长帧、重复打开的加载和不必要的内存分配。手势、页面结构、数据新鲜度、图标来源／尺寸／Alpha／光影、原版动画和稳定性保护优先于性能收益。不能预先承诺所有 ROM 零风险；以明确回归矩阵和逐项验收证明所测范围功能保持。

2026-10-04 已测 APK SHA256 为 `0598DD95FDD8DF48EE52AF497AE47A38E597E176E7F0DA688DED0AB2022CBF2E`，vivo V2458A / Android16，本地正式产物 hash 本次重查仍一致。工作区含既有 staged／unstaged 修改；实施前必须重新记录相关源文件 hash 与安装 APK hash，不以 HEAD 单独代表当前功能基线。

| 已有证据 | 可据此决定的事 | 不能据此决定的事 |
|---|---|---|
| 普通点击／Folder／多指会申请快捷桌面截图，普通点击产生1260×2800锐利层；缓冲＋位图约26.9 MiB | 优先消除无效截图，审计读回与分配 | 不能未经验证延后真实揭露所需截图、降低背景清晰度 |
| 两轮单页↔四页切换出现47.6–52.8 ms GL长帧 | 必须单独定位模式切换与截图链 | 当前缺方法栈，不认定唯一长帧Owner，不直接改原版FBO／mipmap |
| 设置Activity往返84个surface frame中9个App Deadline Missed；MAIN doFrame最高32.65 ms，inflate最高28.55 ms | 减少重复页面准备和首帧布局 | 不是所有子页／overlay的卡顿率，不能混入Buffer Stuffing／Display HAL |
| 1919²解码45.54 ms发生在worker，GC48.07 ms发生在HeapTaskDaemon | 核对源图内存及任务并发 | 不能写成主线程被解码或GC暂停48 ms |

固定施工规则：

1. 一次只处理一个Owner或一个可独立验证的改动；先验证误截图触发，再验证缓冲复用，二者不绑成不可拆的补丁。
2. 复用现有QuickDesktopController／Capture、SettingsHost、Bridge、IconPreviewRepository、资源Owner、ReloadCoordinator；不新增重复Manager／Service，不替换原版引擎。
3. 不改动画时长／曲线／手势阈值来制造“更快”；不关闭感应光影、动态图标、模糊或其他现有功能换取帧率。
4. F01–F15身份、事务、UNKNOWN保留、writer锁、generation／session、GU三分量原子交接均为保护条件。磁盘commit／fsync只按调用线程和数据依赖逐个判断，禁止整体改成apply或删锁。
5. 所有复用都有明确失效条件和生命周期上限；不静态持有Activity／View，不缓存一次结果后永不刷新，不任意增大线程池或长期缓存容量。
6. 保留原版资源、12／20可选宫格、透明主题动画限制和图标冻结合同。九／十六宫格仅参考，不作为新增可选项。

### B. 实施顺序与每阶段范围

| 顺序 | 范围 | 预期收益 | 风险控制 |
|---|---|---|---|
| S0 | 固定基线、补足动作／帧／任务时间线 | 后续能证明改善而非换场景 | 不做功能改动，临时诊断可移除 |
| S1a | 快捷桌面截图触发及多指取消 | 消除普通操作中的无效GPU读回／大分配 | 原版手势归属和揭露前背景逐帧对比 |
| S1b | 截图缓冲生命周期 | 降低真实打开时分配／GC压力 | 不覆盖worker／ImageView仍消费的位图 |
| S2a | 共用资源复用、主题状态快照 | 降低页面准备和重复Binder查询 | 配置／安装／下载变化正确失效 |
| S2b | 设置共用转场、有限页面复用 | 降低返回和首次布局长帧 | Activity与overlay分别验，数据／返回／滚动状态一致 |
| S3 | Cell热路径与多页切换剩余Owner | 减少重复反射／临时对象／模式准备 | 保留像素对齐、圆形比例、Folder／Dock遮挡 |
| S4 | 图标候选／预览及搜索绑定 | 减少队列等待、大图及集中回调 | 稳定候选排序、来源契约、IME／T9／取消门 |
| S5 | 启动／HOME／Loading非关键工作 | 减少首帧前和动画期间竞争 | 数据库前安全门及真实首帧交接不动 |
| S6 | 全路径回归与同条件性能复测 | 确认累积改动的收益和功能保持 | 每项失败回退对应补丁，保留既有稳定性修复 |

S1完成后重新采样多页和Folder；若长帧已消失，不以旧样本为由继续修改原版渲染。S2、S3、S4也采用相同“复测后再决定”的原则。

#### S0：可比较的功能和性能基线

- 复用现有Perfetto、LauncherStartupDiagnostics、SettingsNavigation、SmartisanPerf、QuickDesktop日志与审计脚本。以事件标记记录点击／手势开始、原版Owner确认、资源就绪、首个可见画面、动画结束、任务取消；避免逐图标逐帧日志。
- 先跑正式包功能烟测再启用诊断。需要补采样时只增加受控短时Trace区段：模式准备、Cell绑定、页RenderTarget、截图分配／readPixels／worker、设置inflate／bind／layout；不增加第二套性能Service。
- 当前正式包不允许shell方法采样；只有必要时才做可移除的诊断包，先验证启动／Folder／日历／设置基本功能，诊断开销明显的样本不与正式包直接比较。结束恢复正式包，确认诊断类和标记不残留。
- 真实打开方式由截图／窗口／页面标记确认：长按单图标不算多页编辑，失败搜索入口不算搜索性能，冷进程不算首次干净安装。普通HOME、进程冷启动、升级后第一次打开、同进程重复打开分别记录。
- Perfetto缓冲必须覆盖动作完整区间；检查丢失事件。GL统计区分CPU运行、buffer／VSync等待和实际显示；FrameTimeline缺少GL应用帧时不输出虚假的显示FPS／全项目卡顿率。

#### S1a：消除快捷桌面误截图，不改变手势

当前问题是ACTION_DOWN只按桌面区域即准备截图。已有RootView调用顺序是Controller.onTouch在原识别器之前，RootView.a中的onProgress也位于`J.Ta()`／单指／原版MagicFlow允许门之前。因此**不能简单把DOWN里的schedule搬到现有onProgress，然后宣称触发条件正确**。

实施边界：

- DOWN仅记录手势起点和候选状态；普通点击不刷新内容、不清空背景、不申请整屏截图。
- 必须复用原版确认为可揭露快捷桌面的单指右滑状态，包括`J.Ta()`、sLeftScreenEnabled、桌面区域、RootView当前状态和现有取消规则。Folder／编辑／多指／竖滑／反向翻页／Dock／系统区域不提前领取快捷桌面截图。
- 优先在现有原版确认分支与Capture之间做最小接线。原识别器继续拥有手势，兼容层不能提前消费事件或改变RootView的Ad／拖拽／多指派发。
- 确认意图后，核对GL framebuffer是否仍是揭露前完整桌面，并让所需锐利层在首次可见揭露时可用。先用逐帧证据选择安全读回位置，不用固定毫秒延迟，不在揭露途中替换已显示背景。
- 新世代、第二指、ACTION_CANCEL、关闭／HOME／stop／detach使旧请求失效；已开始的GPU读回不声称可以强行取消，但其结果不得覆盖新窗口或新手势。

验收：每种非快捷桌面操作连续20次，capture请求／读回次数应为0；一次有效打开最多一次有效读回，不能漏背景。慢拖／快甩／往返反向取消、揭露后加第二指、快速开关、Dock／Folder、多页模式、设置／搜索返回及最新桌面背景均通过；没有闪白、旧画面、背景突然更换或错误吃手势。若不能同时做到触发准确和揭露连续，S1a不验收，不使用视觉退化fallback。

#### S1b：只优化已有截图Owner的内存生命周期

- S1a先降低频率，再决定是否值得复用DirectByteBuffer；仅在GL线程按真实Surface宽高／像素格式复用一个受限缓冲，尺寸或Surface变化时失效，退出／内存压力时释放引用。
- `vc.b`还服务原版截图路径；新增可选缓冲使用方式必须留在既有Owner内，只影响快捷桌面调用，其他原版截图仍走原合同。
- 初期不复用仍交给worker／ImageView的Bitmap，不主动recycle显示中的锐利层。确需位图池时必须先证明交接完成与独占写入，并限制容量；不能为了减少分配制造撕裂、recycled bitmap或UAF式竞态。
- 保留当前锐利分辨率、垂直翻转、240px模糊层和既定模糊参数，不换截图API或原版背景材质。

验收：重复开关、取消、Surface重建、分辨率／配置变化、后台／内存压力下图像正确；比较峰值内存、分配次数、GC与首次揭露延迟，不能用额外长期常驻全屏位图抵消收益。

#### S2a：资源与状态数据复用

1. `OriginalQuickSearchResources`复用AssetManager／Resources，按自身APK更新时间、完整Configuration／density建立有效资源项；每次创建绑定当前Context的轻包装，Theme按现有应用样式创建或校验，禁止复用绑定旧Activity的Wrapper／Theme。复制失败不发布有效缓存；升级提取先在已有后台链预热，临时文件完成后发布，不取消fsync语义。
2. maintained设置资源已有`settingsResources`缓存和`scheduleSettingsResourcesWarm`，保留并核对锁等待，不另建预热线程系统。预热安排在真实首帧之后，受可见任务优先级约束；不能把所有页面提前inflate来拖慢启动。
3. 主题页面两个adapter共用一次安装／下载状态快照；worker查询，MAIN绑定。沿用现有页面身份、下载任务和广播；安装、卸载、下载状态变化更新相关条目，下载时仍显示真实进度，已完成时不能继续显示过期“下载中”。
4. 保留已有SwitchEx位图缓存、ThemePreviewAdapter资源ID缓存、后台主题预览和图标分组；它们已实现，不重复施工。

验收：首次／重复打开，覆盖升级、语言／密度／系统配置变化、主题安装卸载、下载失败／恢复／完成、页面离开后迟到回调；开关／搜索栏／主题预览无资源串用，当前主题与图标来源即时正确。

#### S2b：设置共用转场及受限页面复用

- 先修首帧集中工作：减少重复构造／绑定／requestLayout，仅变化条目更新；可见列表优先，未显示内容不抢首帧；禁止将Android View inflate／操作整体移到任意worker。
- 第一批页面复用只考虑主设置页和测得重复构建较重的页面，限定当前Activity／会话与少量最近页面；能释放监听器和重绑数据才保留View。应用图标、分身、权限、备份／密码等状态敏感页不直接缓存完整View。主页面复用成功后再按证据扩大，而非一次缓存所有子页。
- 复用和重建共用原back／scroll／owner逻辑；进入／返回重新读取变更数据并创建正确请求session，旧图标／主题回调不得更新新页面。
- 评估新旧整页硬件层的建立／上传／销毁成本。保持当前动画180ms、主设置进退场260／220ms和现有曲线；只在同条件证实层策略降低长帧后调整层使用。动画取消、快速导航、HOME和销毁都释放层、清理旧root并恢复触摸状态。
- Activity与Launcher overlay分别走回归，不用其中一条通过代替另一条。首次页面必须正确布局后可见；不靠延迟触摸或空白占位掩盖准备耗时。

验收：所有设置子页逐项前进／返回、快速重复点击、标题返回／系统返回／HOME／边缘手势、滚动位置恢复、开关修改后重进、权限页往返；不存在错页、空白、点击穿透、丢滚动位置、过期标题／开关、重复监听或Activity泄漏。

#### S3：绘制热路径和剩余多页长帧

- `LauncherSettingBridge.alignStaticIconPixelGrid`保留所有原判断与1:1像素对齐，仅补全按真实类／方法签名的Method与Field缓存，以及GL线程scratch复用。首批不缓存最终位置或父链动画结果，因为场景仍可能变化。
- `preserveOverviewIconAspect`只在模式绑定链优化相同模式几何／反射信息；保留节点自身scale被ActiveIcon重绑后重新计算的行为，不能累计缩放或永久缓存旧模式比例。
- 缓存不持有Scene／Activity，scratch不能在MAIN／GL共享写入。主题、图标倍率、12↔20、Surface、节点／ActiveIcon重建仍能正确生效。
- S1／上述优化后若多页仍有长帧，用短时区段或方法栈定位到模式准备、Cell绑定、FBO／纹理上传或mipmap真实Owner再做单项改动。优先复用未变化的原版RenderTarget／dirty机制；没有失效证据不改引擎、不新增预渲染系统。
- Folder与Dock分别验证：保留当前Folder打开时全部桌面／Dock及投影隐藏和关闭恢复、Dock投影遮挡修复；不为减少draw把日历／天气／时钟或投影停住。

验收：12／20各验证单页↔多页、页间拖动、编辑／垃圾桶升降、松手取消、图标加入／移出Folder与Dock；50／100／150%图标倍率，普通／透明／毛玻璃主题、静态及活动日历／天气／时钟。正文与影子几何按合同比较，静止像素对齐和多页圆形比例保持，手持投影方向一致。

#### S4：图标候选、预览与搜索

- 现有IconPreviewRepository已具备两线程优先级队列、最多96个会话任务、容量限制、取消门及多类缓存；不增加第二仓库。补测task enqueue→start→decode→publish，区分排队、解码、MAIN绑定与布局。
- 候选页保持“当前选中优先＋稳定来源顺序”的完整列表语义；优先复用元数据，将长批次拆成有取消边界的小任务，让真正可见预览可以执行。不要把顺序更新为按下载完成顺序，不漏候选或因后台慢任务阻止返回。
- 只对有尺寸采样入口的栅格来源采用目标尺寸解码；不能泛化为Drawable强转、改变AdaptiveIcon裁切或给正式桌面增加二次resample。系统Drawable无法在现有入口低成本降采样时，先做缓存和去重，不重写系统资源解码。
- 图片源／应用／图标包更新、主题与配置变化及时失效；缓存权重按真实字节计。页面不可见时取消预览，卸载、恢复、搜索与桌面仍消费正确来源。
- 搜索先复用S2a资源成果；索引／历史／联系人已有后台与快照链保持。只有采到集中bind／layout开销才合并MAIN刷新，首个可见结果不为批量合并等待固定延迟。原T9、系统IME、首开键盘时机和进退场行为不动。

验收：应用图标查询、清空、返回重进、改进版／原图／图标包／自定义切换、当前选中候选、快速换应用／退出、图标包升级卸载、分身身份；搜索实际进入、首开与重复打开、IME／T9切换、输入清空／结果点击／返回、索引更新／联系人权限及头像回调。

#### S5：启动、HOME和Loading

- 分别测普通HOME、冷进程、升级后资源首次提取和真实重载；分离launcher model、必要图标、恢复守卫、资源提取和首帧之后任务的时间。
- 仅将无首帧／事务依赖的资源预热、预览、索引和维护工作放入现有后台链，首帧后按优先级执行；不在首帧完成瞬间同时启动所有后台任务，也不凭经验新增固定延迟。
- RestoreRecoveryGuard仍在DB初始化之前完成durable状态判定和writer互斥。恢复中的rollback／写日志不能异步越过数据库；只对已确认安全的非事务清理评估后台处理，已有清理后台实现不重复改。
- OriginalLoadingContentFactory／ReloadTransitionActivity保留原加载素材、正常无文字、失败反馈、token匹配、真实首帧交接、10秒失败提示及手动重试。Loading不卡依靠MAIN及时调度；不改为提前关闭遮罩／timeout成功／自动杀进程。
- 角标、天气、安装／卸载／替换和分身沿用已有事件Owner与单飞／合并机制；只有记录到重复任务竞争才在已有队列合并，不能丢通知、延迟正确新增或把UNKNOWN当卸载。

验收：冷启动／HOME／重载／锁屏解锁、加载中切后台／返回／失败重试，正常Loading无黑屏／壁纸闪回／残留遮罩；独立故障注入检查锁／日志／token／generation保持，真实备份恢复另以保留数据的可恢复验证包验收，不拿真实布局做破坏性实验。

### C. 功能保护与集中回归矩阵

| 模块 | 必须保持的操作 | 必须保持的状态／视觉 |
|---|---|---|
| 桌面／多页／Dock | 单页／多页、12／20、编辑、拖拽、垃圾桶及取消 | 图标不压扁／跳位，Dock与桌面同显隐，动画完整 |
| Folder | 打开关闭、快速连开、翻页、应用启动、增删／移出 | 无Dock幽灵投影、无错位、关闭后正确恢复 |
| 设置全部子页 | 标题／系统／边缘返回、HOME、快速导航、值修改重进、权限往返 | 页面和滚动位置正确，状态即时，点击不穿透 |
| 主题／壁纸／动画 | 普通主题、四指切换、透明覆盖、毛玻璃、下载／安装、壁纸变更 | 状态栏／虚拟键／背景交接正确，透明主题动画限制保持 |
| 图标／感应 | 五类来源、倍率、静态／动态日历天气时钟、手持倾斜 | 原Alpha／正文清晰度／比例／位置／投影合同保持，不改深浅 |
| 快捷桌面 | 开关、慢拖、快甩、反向取消、多指、卡片启动／返回、搜索／设置入口 | 背景是最新桌面且揭露连续，媒体／天气正确，手势归属保持 |
| 搜索 | 下滑／快捷桌面入口、T9／系统IME、查询／清空／启动／返回 | 索引新鲜、权限正确、键盘与进退场正确，无旧结果回调 |
| 事件与持久化 | 安装／更新／卸载、角标、OEM分身／工作资料、备份／恢复 | 身份／槽／数据不丢，事务门不退化，UNKNOWN继续保留 |
| 生命周期与内存 | HOME、stop/resume、锁屏解锁、进程／Surface重建、低内存／配置变更 | 无Activity／位图／监听器泄漏，无黑屏／残留层／崩溃 |

每阶段先测受影响路径双向20次、快速操作至少10组；资源／缓冲修改增加50次连续往返内存采样。集中阶段热路径至少10个完整同条件样本，冷进程至少5次；数量是发现回归的起点，不等于全机型可靠性证明。V2458A优先；原版锤子Android9可作行为参考，Android8兼容检查及其他ROM／旧设备在可用时追加，未提供设备的范围明确标为未验。

### D. 性能目标与“不影响功能”的验收门

- 每条路径记录点击／手势→首个正确可见画面、动画区间、p50／p95／p99帧间隔或真实present耗时、超预算帧数、MAIN与GL CPU、任务排队、位图分配／峰值内存、GC。按当前实际刷新间隔T计算预算，60Hz时T约16.67ms；不提前承诺120Hz或统一用60Hz判断所有设备。
- 同一设备／APK来源／宫格／主题／图标倍率／光影开关／缓存冷热／动作／刷新率下，先明确热状态再取多次样本；同时记录后台负载和温度异常，不能用少图标／关闭功能／等待更久伪造收益。
- S1a硬指标：非快捷桌面操作capture读回为0；有效打开次数不多于有效手势数，取消结果不晚到覆盖。
- 有测量根因的目标路径，以跨样本p95／p99改善至少20%或超过2T的长帧次数减少至少50%为优化目标；重复约3T长帧优先消除。它们是待验目标，不是当前结果；改善小于测量波动时不保留增加复杂度的补丁。
- 无关路径p95或首个可见画面延迟若稳定变差超过10%，必须调查；数据、手势、视觉、崩溃／ANR、遮罩、位图安全出现任一回归，直接判该项失败，无论平均FPS是否提高。
- 一项通过需要代码／平台隔离检查＋标准build.bat＋签名／对齐检查＋保留数据安装＋所涉真实前进／返回路径＋AndroidRuntime／ANR／native日志＋视觉／状态对比＋同条件性能复测。编译和安装仅是中间验证。

### E. 回退、产物与阶段报告

实施前在本地build下保存当前已安装／正式APK及本项相关文件内容／hash；既有源码和build产物保留，不执行reset／clean或覆盖用户无关改动。保存基线无需提交或推送。阶段变更保持可独立撤销；发现回归只撤销本项，并按需保留数据恢复本轮已确认可用APK，重新验证启动、Folder、日历、设置和数据状态。不得因为性能补丁失败撤销F01–F15稳定性保护。

每项结果记录进DEVELOPMENT_LOG：实际改动、真实根因、文件、构建／安装／功能／性能证据、未验范围、是否保留、回退结果。成功标准是用户正常操作与原版视觉保持，并且目标路径有可重复收益；未验收项不标完成。阶段完成后去掉临时诊断、验证正式包，并恢复采样临时改变的用户偏好。

本方案仅使用现有Owner和项目构建流程；新增代码须在实施时说明为何现有方法不能直接复用。当前建议先完成S0→S1a，以最少风险消除已证明的无效截图，再按复测结果进入后续阶段。

## 1. 文档用途

本计划用于分阶段处理：

- Launcher 启动和返回桌面速度
- 重载时闪回系统壁纸
- 12/20 宫格
- 透明主题和普通主题
- 动态天气/日历
- 壁纸处理
- 图标加载
- 应用安装、更新、卸载
- 角标
- 应用分身和多用户

每次任务只执行用户指定阶段或第一个未完成阶段，不要一次修改所有模块。

开始每个阶段前：

1. 阅读 `AGENTS.md`
2. 阅读 `MEMORY.md`
3. 阅读 `DEVELOPMENT_LOG.md` 最新状态
4. 阅读本计划对应章节
5. 检查工作区未提交修改
6. 先调查原版链路，再修改当前代码

---

# 2. 总体目标

最终结构必须是：

```text
当前设置页 UI
→ 原版 Smartisan Settings 行为语义
→ 原版 Launcher 配置/事件
→ 原版数据库
→ 原版 PageView / ActiveIcon / Theme / SMEngine
→ 最小普通 Android 兼容
```

需要逐步淘汰：

```text
设置页 Java helper
→ 反射调用多个用途不明的方法
→ 多次固定延迟刷新
→ 杀进程
→ Alarm 重启 Launcher
```

---

# 3. 代码参考顺序

## 3.1 原版 Smartisan Settings

```text
build/decompiled_theme_check/com.android.settings-100/
```

用于确认原版设置操作：

- 点击回调
- 写入键值
- Provider
- 广播
- Intent
- Loading
- 返回 Launcher 顺序

重点入口：

```text
smali_classes2/com/android/settings/widget/LauncherPreview.smali
smali_classes2/com/android/settings/widget/LauncherPreview$Callback.smali
smali/com/android/settings/AppIconsSettingsFragment.smali
smali/com/android/settings/AppIconsSettingsFragment$4.smali
```

以下是当前补写兼容控件，不是原版行为依据：

```text
launcher/tools/java/com/android/settings/widget/LauncherPreview.java
```

## 3.2 原版 Launcher

```text
clean_launcher_raw/
```

用于确认原版生命周期、配置读取、数据库迁移、PageView、主题、ActiveIcon、安装事件和 SMEngine。

## 3.3 已有兼容

```text
clean_launcher/
```

用于确认已经完成的普通 Android 兼容。

## 3.4 当前修改目标

```text
launcher/
```

最终修复必须落在这里。

## 3.5 maintained

```text
E:\FANG\smartisan\smartisan-launcher-maintained
```

只参考 UI 和公开 API 兼容，不替换原版核心。

---

# 4. 修改前必须建立原版链路记录

创建：

```text
docs/development/ORIGINAL_BEHAVIOR_REFERENCE.md
```

每个核心功能按以下格式记录：

```markdown
## 功能名称

### 原版 Settings
- 文件：
- 方法：
- 点击值：
- 写入键：
- Provider/广播/Intent：
- Loading/返回流程：

### 原版 Launcher 接收
- 文件：
- 方法：
- 线程：

### 原版数据库
- 文件：
- 方法：
- 完成条件：

### 原版场景
- 文件：
- 方法：
- 渲染线程：
- 更新节点：

### 当前差异
- 新增代码：
- 被替换的原版行为：
- 固定延迟：
- 是否杀进程：
- 是否重复刷新：

### 最小修复
- 复用方法：
- 必需兼容：
- 修改文件：
```

没有完成对应链路调查，不直接重写核心功能。

---

# 5. 阶段 0：启动基线和诊断

状态：已完成（2026-07-15）。诊断实现和实测基线见
`docs/development/LAUNCHER_STARTUP_BASELINE.md`，原版链路见
`docs/development/ORIGINAL_BEHAVIOR_REFERENCE.md`。

## 目标

先测量，再优化。本阶段不改变功能。

## 参考

```text
clean_launcher_raw/smali/com/smartisanos/launcher/Launcher.smali
clean_launcher_raw/smali/com/smartisanos/launcher/J.smali

clean_launcher/smali/com/smartisanos/launcher/Launcher.smali
clean_launcher/smali/com/smartisanos/launcher/J.smali

launcher/smali/com/smartisanos/launcher/Launcher.smali
launcher/smali/com/smartisanos/launcher/J.smali
```

## 修改

增加可关闭的轻量日志：

```text
LAUNCH_ONCREATE_BEGIN
LAUNCH_ORIGINAL_INIT_BEGIN
LAUNCH_ORIGINAL_INIT_END
LAUNCH_MODEL_READY
LAUNCH_PAGE_READY
LAUNCH_SURFACE_READY
LAUNCH_FIRST_FRAME
LAUNCH_DEFERRED_TASKS_BEGIN
LAUNCH_DEFERRED_TASKS_END
```

记录：

- `elapsedRealtime`
- PID
- 线程
- Activity 实例
- 宫格
- 普通主题
- 透明模式
- 动态图标
- 图标包
- 角标

不得逐帧或逐图标写日志。

## 测试

- 首次安装启动
- 第二次冷启动
- HOME 返回
- 最近任务返回
- 锁屏解锁
- 熄屏点亮
- 进程回收后启动

输出基线：

- `onCreate → first frame`
- 原版初始化耗时
- 模型耗时
- 首屏绑定耗时
- SMEngine 首帧
- `onResume` 兼容任务耗时

---

# 6. 阶段 1：Launcher 启动和返回桌面

状态：已完成（2026-07-15）。首帧后兼容任务、窗口状态缓存和实测结果见
`docs/development/LAUNCHER_STARTUP_BASELINE.md`；阶段 2 已完成，阶段 3 为下一个未完成阶段。

## 目标

首帧只执行原版必要初始化，其他任务首帧后按需执行。

## 当前目标

```text
launcher/smali/com/smartisanos/launcher/Launcher.smali
launcher/smali/com/smartisanos/launcher/J.smali
launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java
```

搜索：

```powershell
rg -n "stabilizeLauncherResume|showPendingLauncherReloadLoading|applyLauncherNavigationBarSetting|maybeRefreshLauncherWallpaper|BadgeBridge\.replay|WeatherBridge\.onLauncherResume" launcher
```

## 修改步骤

恢复顺序：

```text
super.onCreate
→ 廉价且必要的窗口设置
→ 原版 J.b(Activity)
→ Page/Surface ready
→ 第一帧
→ 延后兼容任务
```

拆分 `stabilizeLauncherResume()`：

```text
applyProcessCompatOnce()
applyNavigationBarIfChanged()
applyBadgeIfDirty()
completePendingReloadAfterFirstFrame()
```

删除普通启动中的多次补帧。

缓存导航栏状态：

```text
lastWindowToken
lastHideNavigationBar
lastSystemUiVisibility
lastNavigationBarColor
```

首帧后再安排：

- 天气
- 角标
- 图标包
- 在线图标
- Profile
- 设置资源
- 检查更新

每项先判断开关、dirty、缓存和重复任务。

## 验收

- 原版 `J.b()` 和场景初始化不被跳过
- 首帧前无网络、定位、全应用扫描和大图处理
- 重复 `requestLayout/invalidate/requestRender` 明显减少
- 不以关闭原版动画换取速度

---

# 7. 阶段 2：天气和角标的恢复开销

状态：已完成（2026-07-15）。天气关闭态、组件缓存、定位权限边界和角标增量同步已实现；
构建、签名、覆盖安装及关闭态冷启动/三次恢复验证通过。通知访问开启后的实体机角标回归仍保留为风险项。

## 天气参考

```text
build/decompiled_theme_check/com.android.settings-100/
smali/com/android/settings/AppIconsSettingsFragment.smali

build/decompiled_theme_check/com.android.settings-100/
smali/com/android/settings/AppIconsSettingsFragment$4.smali

launcher/tools/java/com/smartisanos/launcher/theme/WeatherBridge.java
launcher/tools/java/com/smartisanos/launcher/theme/LauncherSettingBridge.java
```

## 天气修改

`WeatherBridge.onLauncherResume()` 第一层判断：

```java
if (!LauncherSettingBridge.dynamicWeatherCalendarEnabled(activity)) {
    return;
}
```

关闭时不得：

- 扫描天气应用
- 加载应用 Label
- 请求定位
- 安排周期任务
- 联网

缓存天气组件，以下事件才失效：

```text
PACKAGE_ADDED
PACKAGE_REMOVED
PACKAGE_REPLACED
PACKAGE_CHANGED
Profile 变化
分身变化
```

定位权限只在用户进入天气设置、开启自动定位或主动刷新时申请。

周期任务每次执行前重新检查开关，关闭后停止续约。

## 角标参考

```text
clean_launcher_raw/smali/com/smartisanos/launcher/
launcher/tools/java/com/smartisanos/launcher/badge/
```

搜索：

```powershell
rg -n "badge|Badge|SHOW_MESSAGE_FLAG|EFFECT_REMOVE_BADGE" clean_launcher_raw\smali\com\smartisanos\launcher
```

## 角标修改

只保留一个 `BadgeBridge.replay()` 生命周期入口。

以下情况直接返回：

- 角标关闭
- 无通知访问权限
- 服务已同步
- 通知版本未变化

只更新受影响节点，不重复全量数据库和场景刷新。

## 验收

- 关闭动态图标后恢复桌面不扫描天气应用
- 普通 Launcher 启动不弹定位权限
- 每次 resume 角标只同步一次
- 无多次延迟全量刷新

---

# 8. 阶段 3：12/20 宫格配置和原版迁移

状态：核心实现完成，完整回归待最终验证（2026-07-15）。已确认私有配置优先、原版模式映射和
`N.d + F.i` 数据库链；12→20 已成功，模式相同时直接跳过，未修改数据库结构或原版迁移算法。
阶段 3 的最终回归集中保留：20→12 且板块超过 12 个图标、文件夹、隐藏板块、加密板块、连续切换和设备重启保持。

## 原版 Settings

```text
build/decompiled_theme_check/com.android.settings-100/
smali_classes2/com/android/settings/widget/LauncherPreview.smali

build/decompiled_theme_check/com.android.settings-100/
smali_classes2/com/android/settings/widget/LauncherPreview$Callback.smali
```

查找真实 Callback：

```powershell
rg -n "onLauncherTypeChanged|onLauncherModeChanged|LauncherPreview\$Callback|launcher_mode|launcher_multi_block_mode" `
  build\decompiled_theme_check\com.android.settings-100
```

确认点击值、写入键、确认框、Provider 和重载流程。

## 原版 Launcher

```text
clean_launcher_raw/smali/com/smartisanos/launcher/ua.1.smali
clean_launcher_raw/smali/com/smartisanos/launcher/data/N.smali
clean_launcher_raw/smali/com/smartisanos/launcher/data/F.smali
clean_launcher_raw/smali/com/smartisanos/launcher/data/A.smali
clean_launcher_raw/smali/com/smartisanos/launcher/data/O.smali
```

对照相同路径：

```text
clean_launcher/
launcher/
```

## 当前目标

```text
launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java
```

方法：

```text
confirmLauncherMode()
saveLauncherMode()
writeLauncherModePref()
pageModeForLauncherCellCount()
migrateLauncherModeAndRestart()
restartLauncherAfterGridMigration()
```

## 修改步骤

```text
读取当前模式
→ 将 12/20 写入私有 SharedPreferences
→ commit 成功
→ 有权限时镜像 Settings.Global
→ DatabaseHandler worker 执行 N.d + F.i
→ 等待数据库完成
→ Launcher 重新读取配置和页面
→ 等待真实第一帧
→ 关闭设置页
```

私有配置：

```text
prefs: com.smartisanos.launcher_prefs
key: prefs_key_launcher_mode
value: 12 / 20
```

必须保留：

```text
N.d(context, newPageMode)
F.i(oldPageMode, newPageMode)
```

不得重写 12→20、20→12、隐藏/加密板块、图标顺序和文件夹数据。

## PageView 验证

```powershell
rg -n '\.source "PageView.java"|\.source "Cell.java"|switchPageMode|handleSettingsChange|initPageLocation' `
  clean_launcher_raw\smali\com\smartisanos\launcher
```

验证重新建立：

- 行列数
- 单板块容量
- Cell
- Dock
- 文件夹
- 隐藏/加密板块
- 当前页

## 验收

- 12→20 保留原板块和顺序
- 20→12 只由原版 `F.i()` 拆分
- 重启后模式不丢失
- 主存储不依赖系统写权限
- 宫格迁移完成后交给阶段 4 冷重载协调器；宫格业务本身不得直接杀进程

---

# 9. 阶段 4：统一重载与闪回系统壁纸

状态：核心实现完成，完整回归待最终验证（2026-07-15）。独立 `:reload` 不透明过渡页、原版 Smartisan
LoadingUI、旧主进程 PID 精确终止、新 Launcher 真实首帧 token 握手均已验证；没有 Alarm 延迟重启或新增固定成功延迟，未发现新的 Java/native 崩溃。
`:reload` Activity 结束后暂时作为 cached 进程存在属正常系统行为，不得手工杀掉。最终回归集中保留：实体机逐帧无系统壁纸、黑帧/白帧、多 ROM、连续切换压力、异常中断和超时恢复。

## 目标

消除“杀进程后等待 Launcher 新首帧”造成的窗口空档。

## 当前目标

```text
launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java
```

搜索：

```powershell
rg -n "killProcess|System\.exit|scheduleLauncherRestart|restartLauncherForColdSceneChange|restartLauncher\(|recreateLauncherInPlace|finishSettingsTask|startLauncherFromForeground|showRestartLoading" `
  launcher\tools\java\com\smartisanos\launcher\theme
```

## 原版参考

```text
clean_launcher_raw/smali/com/smartisanos/launcher/Launcher.smali
clean_launcher_raw/smali/com/smartisanos/launcher/J.smali
clean_launcher_raw/smali/com/smartisanos/launcher/ua.1.smali
```

原版设置 Loading：

```powershell
rg -n "SmartisanProgressDialog|LoadingUI|ProgressDialog|finish\(|CATEGORY_HOME|startActivity" `
  build\decompiled_theme_check\com.android.settings-100
```

## 修改步骤

正常路径：

```text
原版数据库/主题业务准备完成
→ 主进程生成唯一 reloadToken 和旧主 PID
→ 启动 :reload 中不透明 ReloadTransitionActivity
→ OnPreDraw + 一个 Choreographer 帧确认过渡窗口已显示
→ 精确结束旧主 PID
→ 显式启动新 Launcher
→ GL 帧 + Decor OnPreDraw + 一个 Choreographer 帧
→ 包内 Broadcast 校验同一 reloadToken
→ 关闭并移除过渡任务
```

禁止：

```text
Activity.recreate() 处理宫格
手工重建 PageView、Cell、EGL 或 SMEngine
按包名 force-stop / killBackgroundProcesses
透明过渡 Activity
固定延迟判定启动成功
```

进程重启只能作为以下异常的最终兜底：

- 找不到 Launcher Activity
- Activity 正在 finishing
- `recreate()` 抛异常
- 场景无法恢复

必须记录兜底原因。

## 真实首帧判断

不得固定等待 260/650/1200/1600ms。

组合使用现有真实状态：

- Launcher Activity 有效
- MainView 有效
- PageView 有效
- 当前页存在
- Surface 有效
- Cell 已绑定
- 原版 ready 状态
- `OnPreDrawListener`
- `Choreographer.FrameCallback`
- SMEngine 渲染状态

## 验收

- 旧主 PID 仅在过渡窗口真实绘制后按精确 PID 结束
- `:reload` 在新 Launcher 首帧前仍存在
- reloadToken 严格匹配，不串线
- 过渡窗口和 Launcher starting window 均不透明
- 逐帧无系统壁纸、黑帧和白帧

该阶段解决项目代码主动进程重生导致的闪屏，不包含系统强杀、Launcher 崩溃和厂商 WindowManager BUG。

---

# 10. 阶段 5：透明主题

状态：进行中（2026-07-15）。本阶段复用阶段 4 的 `ReloadTransitionActivity`、`LauncherColdReloadCoordinator`、`ReloadProtocol`、reloadToken、旧主 PID 精确终止、`FIRST_FRAME_READY` 与失败手动重试；不携带任何宫格迁移状态。

## 原版 Settings

```text
build/decompiled_theme_check/com.android.settings-100/
smali_classes2/com/android/settings/widget/LauncherPreview.smali
```

搜索：

```powershell
rg -n "onLauncherThemeChanged|launcher_grid_theme|TransparentTheme|transparent" `
  build\decompiled_theme_check\com.android.settings-100
```

## 原版 Launcher

```text
clean_launcher_raw/smali/com/smartisanos/launcher/ua.1.smali
clean_launcher_raw/smali/com/smartisanos/launcher/data/O.smali
clean_launcher_raw/smali/com/smartisanos/launcher/data/Constants.smali
clean_launcher_raw/smali/com/smartisanos/launcher/theme/X.smali
clean_launcher_raw/smali/com/smartisanos/launcher/theme/t.smali
clean_launcher_raw/smali/com/smartisanos/launcher/theme/ThemeChooserActivity.smali
clean_launcher_raw/smali/com/smartisanos/launcher/view/Eb.smali
```

搜索：

```powershell
rg -n "launcher_grid_theme|isTransparentTheme|smartisan_theme_trans|initByTheme|ChangeThemeHandler|updateGLView" `
  clean_launcher_raw\smali\com\smartisanos\launcher
```

资源：

```text
build/decompiled_theme_check/com.smartisanos.launcher.theme.trans/
```

## 当前目标

```text
launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java
launcher/tools/java/com/smartisanos/launcher/theme/LauncherSettingBridge.java
```

## 修改步骤

保留：

```text
launcher_grid_theme
transparent_previous_theme
原版透明主题资源
Constants.isTransparentTheme
原版 O/X 初始化
```

开启：

```text
保存当前普通主题
→ 私有配置写 launcher_grid_theme=1
→ commit 成功
→ 注册原版透明资源
→ 准备原版透明壁纸、模糊和翻页动画限制
→ 调用冷重载协调器
→ 新 Launcher 冷启动读取透明配置
→ 原版 Constants/O/X/Eb/SMEngine 按透明模式初始化
→ 等待真实首帧
→ 关闭过渡页
```

关闭：

```text
写 launcher_grid_theme=0
→ 恢复 transparent_previous_theme
→ 清除透明模式专用覆盖和模糊状态
→ commit 成功
→ 调用冷重载协调器
→ 新 Launcher 按普通主题初始化
→ 等待首帧
→ 关闭过渡页
```

禁止：

- 永久写 `launcher_theme=smartisan_theme_trans`
- 透明主题进入普通主题队列
- 正常路径杀进程
- Alarm 拉起 HOME
- 调用 `N.d()`、`F.i()` 或宫格 pending 消息
- 固定延迟判断成功
- Activity.recreate()、局部重建 PageView/Cell、手工重置 EGL/SMEngine

第一阶段稳定后，才研究原版 SMEngine 热切换；不得新建第二套主题引擎。

---

# 11. 阶段 6：普通主题

状态：进行中（2026-07-15）。普通主题只使用原版 ThemeManager、`ChangeThemeHandler.RequireChangeFrom.SETTING`、过渡截图和 Launcher 返回后的单条原版消息；仅当原版持久化明确失败时，才写一条兼容 pending 消息。

## 原版参考

```text
clean_launcher_raw/smali/com/smartisanos/launcher/theme/X.smali
clean_launcher_raw/smali/com/smartisanos/launcher/theme/t.smali
clean_launcher_raw/smali/com/smartisanos/launcher/theme/ThemeChooserActivity.smali
```

搜索：

```powershell
rg -n "MESSAGE_CHANGE_THEME|0x12|RequireChangeFrom|launcher_theme|ChangeThemeEvent|ChangeThemeHandler" `
  clean_launcher_raw\smali\com\smartisanos\launcher
```

## 当前目标

```text
launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java
```

方法：

```text
applyTheme()
applyThemeViaOriginalStack()
queueThemeChangeForLauncher()
submitThemeSnapshot()
refreshThemeRuntime()
refreshLauncherThemeSurface()
```

## 修改步骤

权威流程：

```text
设置页选主题
→ 原版 ThemeManager 持久化
→ ChangeThemeHandler 来源为 SETTING
→ 原版过渡截图
→ 返回 Launcher
→ 消费一条原版主题消息
→ 原版场景更新
```

原版栈明确持久化失败才使用一条 fallback pending message；fallback 不再叠加原版写入、手工 Handler 消息或固定延迟。

同一次切换不能同时执行：

- 原版 `O.a`
- 多份手工配置
- 手工 pending message
- 手工 Handler message
- 所有 `Eb` 方法
- 多次延迟刷新

必须从原版确认 `Eb.lh/Vh/oh/Z` 等混淆方法用途。

## 验收

- 一次操作只有一条主题链
- 主题重启后保持
- 无重复动画
- 不用冷启动方法作为通用刷新
- 正常路径不杀进程

---

# 12. 阶段 7：动态天气和日历场景更新

状态：进行中（2026-07-15）。动态开关已收敛为原版 `com.smartisanos.launcher.update_icon` → `Aa.c()` → 原版数据库更新；只发送原版 WeatherView/CalendarView 的包名，不扫描全部 Launcher 应用、不重启 Launcher。

## 原版协议

```text
build/decompiled_theme_check/com.android.settings-100/
smali/com/android/settings/AppIconsSettingsFragment.smali
smali/com/android/settings/AppIconsSettingsFragment$4.smali
```

```text
action: com.smartisanos.launcher.update_icon
extra: extra_packagename
```

## 原版 Launcher

```text
clean_launcher_raw/smali/com/smartisanos/launcher/receiver/LauncherReceiver.smali
clean_launcher_raw/smali/com/smartisanos/launcher/data/
```

搜索：

```powershell
rg -n "update_icon|extra_packagename|EVENT_REFRESH|EVENT_PACKAGE_CHANGED|updateCell|updateCells" `
  clean_launcher_raw\smali\com\smartisanos\launcher
```

查找场景类：

```powershell
rg -n '\.source "ActiveIcon.java"|\.source "WeatherView.java"|\.source "CalendarView.java"|ActiveIcon|WeatherView|CalendarView' `
  clean_launcher_raw\smali\com\smartisanos\launcher
```

## 当前目标

```text
launcher/tools/java/com/smartisanos/launcher/theme/LauncherSettingBridge.java
launcher/tools/java/com/smartisanos/launcher/theme/WeatherBridge.java
launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java
launcher/smali/com/smartisanos/launcher/receiver/LauncherReceiver.smali
```

## 修改步骤

```text
写开关
→ 原版 update_icon 或数据库事件
→ DatabaseHandler 更新
→ 数据库完成
→ 只更新天气/日历 Cell
→ 创建原版 ActiveIcon 或普通图标
→ 一次渲染
```

兼容层只负责定位、天气数据、包映射、配置 fallback 和安全阴影 fallback。

禁止：

- 重启 Launcher
- recreate Activity
- 杀进程
- 设置页直接强转 ActiveIcon
- 设置页直接操作用途不明的节点槽位
- 多次延迟刷新

## 验收

- 开关无需重启 Launcher
- 天气/日历使用原版节点
- 数据库类型与场景节点一致
- 关闭后无天气后台任务

---

# 13. 阶段 8：壁纸处理和刷新

状态：核心实现完成，基本验证完成（2026-07-15）；最终回归待完成。已确认 `Eb.lh()` 是原版透明壁纸 `changeWallpaper` 入口；壁纸选择在后台完成复制/解码/缩略图/高斯图，主线程只写最终状态并调用一次 `lh()`，场景不可用才保留 pending。已完成完整构建、v1/v2/v3 签名、`emulator-5556` 覆盖安装和 HOME 启动无新增 Java/native fatal；图片选择、透明主题壁纸、默认壁纸恢复及逐帧视觉回归留待最终集中验证。

## 原版 Settings

```powershell
rg -n "WallpaperCache|launcher_wallpaper_uri|WallpaperManager|CHANGE_LOCKSCREEN_WALLPAPER" `
  build\decompiled_theme_check\com.android.settings-100
```

其他参考：

```text
build/decompiled_theme_check/com.smartisanos.wallpaperprovider-100/
build/decompiled_theme_check/com.smartisanos.desktop-3/
```

## 原版 Launcher

```text
clean_launcher_raw/smali/com/smartisanos/launcher/ua.1.smali
clean_launcher_raw/smali/com/smartisanos/launcher/data/O.smali
clean_launcher_raw/smali/com/smartisanos/launcher/view/Eb.smali
```

## 当前目标

```text
launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java
```

搜索：

```powershell
rg -n "onWallpaperPicked|saveGaussianWallpaperCopy|refreshLauncherWallpaperNow|refreshLauncherAfterWallpaperUriChanged|maybeRefreshLauncherWallpaper|markWallpaperRefreshPending" `
  launcher\tools\java
```

## 修改步骤

后台线程：

- 文件复制
- 大图解码
- 裁剪
- 缩略图
- 高斯图
- 压缩和保存

主线程：

```text
写最终 URI
→ 通知原版配置
→ 调用一个确认用途的原版壁纸刷新入口
→ 一次渲染
```

删除“立即 + 120ms + 420ms + onResume pending”的重复刷新。

运行时刷新成功后清除 pending；只有 Launcher/场景不可用时设置 pending。

未确认 `Eb.Vh()` 用途前，不把它作为壁纸热刷新方法。

## 验收

- 图片处理不阻塞设置页
- 壁纸只更新一次
- 成功后不重复 pending 刷新
- 透明主题壁纸状态正确

---

# 14. 阶段 9：图标加载

状态：加载性能核心实现完成；图标 geometry/raster 架构于 2026-08-21 重新审计并冻结为 [`ICON_RENDERING_CONTRACT.md`](../ICON_RENDERING_CONTRACT.md)。当前实现仍需按合同消除数据库预合成与最终 Composer 的双 Owner，并打通 ActiveIcon attach 后的 STATIC geometry sync，最终跨分辨率矩阵尚未完成。普通模式不再启动图标包扫描或 appfilter 解析；所选图标包解析、在线图标落盘均只合并更新受影响包名，不再以设置资源预热或图标缓存写入触发全量数据库刷新。

冻结规则只在 [`ICON_RENDERING_CONTRACT.md`](../ICON_RENDERING_CONTRACT.md) 维护，本计划不再复制另一套算法。核心边界：来源只解析 RAW；`IconVisualMetrics` 唯一决定 geometry/physical raster；普通 Application 每次生成只调用一次最终 Composer；DEFAULT-only optical normalization；ActiveIcon 内部原版动画冻结并在每个 geometry generation 追随 STATIC artwork world rect。完整矩阵通过前不得标记 `ICON_SYSTEM_VALIDATION_FROZEN=true`、`FINAL` 或 `PASS`。

## 原版参考

```powershell
rg -n '\.source "IconCache.java"|\.source "IconBitmapCache.java"|loadIcon|ResolveInfo|ItemInfo' `
  clean_launcher_raw\smali\com\smartisanos\launcher
```

## 当前目标

```text
launcher/tools/java/com/smartisanos/home/settings/icons/IconManager.java
launcher/tools/java/com/smartisanos/home/settings/icons/IconPackManager.java
launcher/tools/java/com/smartisanos/home/settings/icons/AppIconAdapter.java
launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java
```

搜索：

```powershell
rg -n "shouldUseManagedIcon|selectedIconDrawable|preloadSelectedIconPackAsync|warmUpIconPackList|online_icon|RedirectIconDB" `
  launcher\tools\java
```

## 修改步骤

以下全部关闭时，直接走原版图标：

- 改进图标
- 图标包
- 单应用覆盖
- 在线/本地覆盖

快速判断不得解码图片、扫描图标包、解析 appfilter、联网、读大 JSON 或枚举全部应用。

首帧显示原图；下载或解析完成后只更新受影响包名。

删除仅因设置资源预热而触发的数据库刷新。

## 验收

- 普通模式不初始化管理图标系统
- 在线图标失败不阻塞模型
- 图标更新合并执行
- 动态图标不被静态图片覆盖

---

# 15. 阶段 10：安装、卸载、角标和分身

状态：核心实现完成，基本验证完成（2026-07-15）；最终回归待完成。普通安装广播在 Launcher Activity 可查询后只进入一次原版 `Aa.c(context, package)`；仅当 PackageManager 尚未暴露目标 Activity 时最多重试两次。卸载进入原版 `Aa.D(package)` 删除链，并清除该包可选图标缓存。分身只在存在已启用记录时查询 profile，删除 350/450/900/2200/2000/8000ms 的多次全量补偿刷新；已完成完整构建、v1/v2/v3 签名、`emulator-5556` 覆盖安装与 HOME 启动无新增 Java/native fatal。真实安装/卸载、替换、工作资料/分身和角标联动留待最终回归。

## 应用事件参考

```text
clean_launcher_raw/smali/com/smartisanos/launcher/receiver/LauncherReceiver.smali
clean_launcher_raw/smali/com/smartisanos/launcher/data/
```

搜索：

```powershell
rg -n "PACKAGE_ADDED|PACKAGE_REMOVED|PACKAGE_REPLACED|PACKAGE_CHANGED|EVENT_PACKAGE_ADDED|EVENT_PACKAGE_REMOVED|EVENT_PACKAGE_CHANGED" `
  clean_launcher_raw\smali\com\smartisanos\launcher
```

当前目标：

```text
launcher/tools/java/com/smartisanos/launcher/install/SmartisanInstallManager.java
launcher/smali/com/smartisanos/launcher/receiver/LauncherReceiver.smali
```

## 修改步骤

普通 Android 的广播、`LauncherApps.Callback` 和 `PackageInstaller` 最终转换为原版 DatabaseUpdater 事件。

安装：

```text
LauncherActivityInfo 可查询
→ 原版 PACKAGE_ADDED
→ 数据库完成
→ 受影响页面
→ 一次渲染
```

PackageManager 信息暂未可用时最多有限重试 2–3 次，成功立即停止。

卸载：

```text
原版 PACKAGE_REMOVED
→ 删除数据库
→ 移除 Cell
→ 清理图标缓存
→ 一次渲染
```

## 分身参考

```powershell
rg -n "EVENT_USER_PACKAGE_ADDED|EVENT_USER_PACKAGE_REMOVED|EVENT_USER_PACKAGE_CHANGED|getInstalledPackagesAsUser|startActivityAsUser" `
  clean_launcher_raw\smali\com\smartisanos\launcher
```

没有启用分身记录时不调用 `LauncherApps.getProfiles()`，不枚举次用户应用。

有变化时：

```text
原版 USER_PACKAGE 事件
→ 数据库完成
→ 一次刷新
→ 一次渲染
```

删除 350/900/2200ms 等多次全量补偿刷新。

## 验收

- 安装后无需重启即显示
- 卸载后无需重启即移除
- 默认不扫描 Profile
- 角标和分身不重复全量刷新

---

# 16. 固定延迟审计

状态：核心审计完成，基本验证完成（2026-07-15）；最终回归待完成。已删除透明壁纸 160ms、角标 180ms、主题运行时 120/360ms、手动城市 1800ms 的竞态补偿刷新。保留项已分类：`:reload` 10 秒仅为失败提示；安装 300ms 仅在 PackageManager 尚不可查询时最多两次；主题/更新下载 800–1500ms 为网络轮询；在线图标 2 秒为写入安静窗口合并；天气 TTL、UI Loading 帧和键盘/预览动画属于功能性调度。未重新接入旧 Alarm 重启路径。

搜索：

```powershell
rg -n "postDelayed|setExact|setExactAndAllowWhileIdle|sleep\(" launcher
```

把每个延迟分类：

- UI 动画必要
- 系统节流必要
- 网络轮询必要
- 有上限的安装轮询
- 竞态掩盖
- 重复补帧

后两类必须替换为真实完成信号。

保留的延迟必须在代码或文档说明原因。

---

# 17. 任务合并和状态

状态：核心实现完成，基本验证完成（2026-07-15）；最终回归待完成。既有图标、天气、分身和冷重载任务均保持单飞/合并状态；`ReloadTransitionActivity` 已明确 `WAITING_FIRST_FRAME → COMPLETED/FAILED`，失败手动重试会重新挂载失败超时，token 首帧只完成一次。超时仅显示失败，不自动杀进程。

优先在现有类中使用轻量状态：

```text
IDLE
DATABASE_UPDATING
SCENE_UPDATING
WAITING_FIRST_FRAME
COMPLETED
FAILED
```

规则：

- 同类任务同时只运行一个
- 重复请求合并
- 新请求可覆盖旧参数
- 数据库未完成不更新场景
- 场景不可用时只记一个 pending
- 一次完成只提交一次渲染
- 超时记录错误并恢复状态
- 超时不自动杀进程

---

# 18. 建议 Commit 顺序

状态：已审阅（2026-07-15）。本轮未暂存、未提交：工作区包含用户既有改动与跨阶段的构建产物，必须待最终回归后按上述功能边界人工拆分提交。

1. `perf: add launcher startup and first-frame diagnostics`
2. `perf: defer non-critical launcher resume work`
3. `perf: skip weather work when dynamic icons are disabled`
4. `fix: persist launcher grid mode before original migration`
5. `fix: reload launcher in process after grid migration`
6. `fix: apply transparent mode without process rebirth`
7. `fix: refresh dynamic icons through original update pipeline`
8. `perf: remove redundant wallpaper and theme refreshes`
9. `perf: preserve original icon fast path`
10. `perf: coalesce badge and profile refresh events`

每阶段独立构建和验证后再进入下一阶段。

---

# 19. 构建和安装

```powershell
.\build.bat
```

产物：

```text
build\launcher-signed.apk
```

检查：

```powershell
aapt2 dump badging build\launcher-signed.apk
aapt2 dump xmltree build\launcher-signed.apk AndroidManifest.xml
apksigner verify --verbose build\launcher-signed.apk
```

安装：

```powershell
adb install -r build\launcher-signed.apk
```

回归测试不要清除数据。

---

# 20. 重载和闪屏验证

操作前后：

```powershell
adb shell pidof com.smartisanos.home
```

日志：

```powershell
adb logcat -c
adb logcat -v threadtime > launcher_reload_test.txt
```

录屏：

```powershell
adb shell screenrecord /sdcard/launcher_test.mp4
adb pull /sdcard/launcher_test.mp4
```

检查：

- `am_proc_died`
- `Process.killProcess`
- scheduled process rebirth
- FATAL EXCEPTION
- HOME 切换
- 系统壁纸帧
- 黑帧/白帧
- 旧场景闪回
- 设置页或 Loading 提前消失

---

# 21. 测试矩阵

## 启动

- 首次安装
- 覆盖安装
- 冷启动
- 热启动
- HOME 返回
- 最近任务返回
- 锁屏解锁
- 熄屏点亮
- 进程回收后启动

## 宫格

- 12→20
- 20→12
- 连续切换 10 次
- 超过 12 个图标的板块
- 少于 12 个图标的板块
- 隐藏板块
- 加密板块
- 文件夹
- 重启保持

## 主题

- 普通 A→B
- 普通→透明
- 透明→普通
- 连续开关透明 10 次
- 透明模式换壁纸
- 透明模式锁屏解锁
- 透明模式 HOME/Recents

## 动态图标

- 开启/关闭
- 有/无天气应用
- 定位允许/拒绝
- 手动城市
- 自动定位
- 跨日
- 天气更新

## 应用和分身

- 安装
- 更新
- 卸载
- 禁用/恢复
- 分身开启/关闭
- 次用户应用

---

# 22. 每阶段完成报告

必须说明：

## 修改内容

具体行为变化。

## 根因

旧实现为什么失败或慢。

## 原版复用

具体原版 Settings 和 Launcher 文件/方法。

## 普通 Android 兼容

缺失的 Smartisan 能力、使用的替代方式，以及为何不改变原版语义。

## 修改文件

完整路径。

## 验证

- 构建
- 签名
- 安装
- PID
- 日志
- 录屏
- 功能测试

## 风险

- 未测试 ROM
- 反射
- fallback
- 仍保留的延迟
- 未验证行为

还必须明确：

- 是否仍有 `killProcess`
- 是否仍有 Alarm 重启
- 增删了哪些固定延迟
- 是否修改二进制 Manifest
- 是否修改数据库结构
- 是否修改原版 `F.i()`
- 是否更新 `MEMORY.md`
- 是否更新 `DEVELOPMENT_LOG.md`

---

# 23. 闪回系统壁纸的预期结论

旧项目内闪屏链路：

```text
设置页结束
→ Launcher 进程死亡
→ Surface 消失
→ 延迟启动 HOME
→ 新首帧未准备好
→ 系统壁纸暴露
```

当前受控冷重载结构：

```text
原版宫格数据库迁移完成
→ :reload 过渡 Activity 不透明首帧
→ 精确结束旧 Launcher 主 PID
→ 新 Launcher 不透明 starting window
→ GL 帧、Decor OnPreDraw、Choreographer 帧
→ token 匹配后关闭过渡任务
```

该方案允许 Launcher 主 PID 变化，但要求用户始终被过渡窗口或 Launcher starting window 覆盖。不得使用 timeout 当成功；10 秒只用于显示失败和一次手动重试。

不包含：

- Launcher 自身崩溃
- 系统低内存强杀
- 厂商手势合成 BUG
- WindowManager/SurfaceFlinger 异常
- 用户切换默认桌面

只有在可用 ROM 上多次逐帧验证通过后，才能把项目内部重载闪屏标记为已修复。
