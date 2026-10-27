# 壁纸备份恢复与图标源体积审计

日期：2026-10-14。施工路径：E:\FANG\smartisan\home-main，main分支。真机vivo V2458A / API36仅做backups目录只读检查，没有安装、恢复或改动真机备份。证据保存在build/backup-wallpaper-20261014，临时用户备份不进入Git。

## 已确认体积原因

| 真机备份 | 文件字节（文件管理器十进制MB） | 图标原图数 | 图标文件压缩字节 |
|---|---:|---:|---:|
| 2026-10-03 22-22 | 2,855,663（2.86MB） | 61 | 2,831,649 |
| 2026-10-09 16-20 | 28,840,143（28.84MB） | 508 | 28,694,867 |
| 2026-10-10 21-58不带阴影 | 29,840,614（29.84MB） | 518 | 29,692,538 |

体积几乎全部来自icons/sources。三份都没有壁纸文件，没有第三方图标包APK；布局JSON、设置JSON没有对应数量级增长。之前版本修复了包名PNG未被归档的问题，随后整目录遍历也将图标库浏览/预取的未引用原图纳入备份。10/9样本中63个旧哈希文件加445个其他源文件；不能把文件管理器文件名中的“带阴影”当成压缩包内打包了阴影纹理的证据，也不能把增长归因于本轮系统壁纸同步。

## 最小改动与保留条件

- RestoreIconSourceReconciler仍是图标原图归档/恢复拥有者。导出现在读取稳定布局和保存的redirect记录，保存应用包名原图、resource选择原图及其旧哈希文件名；不要求选择必须当前可见，已保存但不在桌面的选择同样保留。
- 自动候选、组件候选和OEM系统别名通过现有IconPreviewRepository/系统别名拥有者查询，只获取源ID，不解码预览、不下载、不新增匹配规则。无法可靠反查身份的历史十六进制文件暂时保留，避免跨设备别名或缺失应用被过度裁剪。此兼容保留意味着不能承诺所有备份固定为某个大小。
- 未引用的包名/组件/库源PNG不进入新归档，但手机缓存本身不删除。自定义上传图标仍由IconBackupCodec打包icons/custom，PNG原字节和Alpha不更改；图标包仍保存全局/单应用选择信息，不包含第三方APK。恢复设备需要安装相应图标包，缺包时沿用既有回退和选择保留规则。
- 原图校验后立即回收临时Bitmap。没有改图标渲染比例、光影、材质、纹理生成或恢复后的已有重整链路。

对28.84MB原档用实际筛选/写ZIP代码隔离重打包，保留63张源文件后为2,882,631字节（2.88MB）。最初1.9MB是只按37个直接引用文件的估算，最终加入历史哈希保护；实际新备份还可能包含当前解析到的组件/OEM候选和自选壁纸，因此不将隔离2.88MB等同真机新备份最终大小。旧28MB备份仍按旧格式完整读取，不修改、替换或删除用户旧档。

## 壁纸归档与恢复

复用ThemeBackupCodec和MaintainedLauncherSettingsHost的壁纸URI拥有者，向theme.json增加可选wallpaper对象version=1。普通主题/默认背景只保存default和透明底层主题选择，不打包主题背景资产或整份主题APK；由恢复后的原主题资源与当前尺寸重建。自选图片只打包一份原始文件wallpaper/selected-image；不包含系统壁纸副本、gaussian_wallpaper.png、默认源缓存或缩略图，不保存旧设备file/content URI。

恢复前BackupValidator完成全部ZIP检查、SHA256检查及图片头尺寸/路径验证。恢复时后台复制到新设备的Launcher私有目录，用现有偏好/Constants URI链路激活；透明底层主题单独恢复，维持普通/毛玻璃/透明的区别。待现有恢复协调器初始化目标主题并冷重载后，复用之前的系统壁纸同步入口，避免恢复中向系统写入旧的活动主题。图片复制与默认清理不在主线程执行。

普通备份和恢复前回滚归档均加入壁纸，失败回滚会恢复原壁纸来源。历史备份未记录wallpaper时保留当前壁纸，不假定缺字段代表用户选择默认；历史备份从未保存的图片不能从旧档凭空恢复。新备份显式default会清除自选源并使用恢复主题默认背景。主题包和图标包本体沿用原来的外部安装条件。

保持格式version2，新增的是可选主题元数据和受现有完整性保护的文件；旧档1/2读取兼容。图片沿用ZIP单项20MiB上限，尺寸最多1亿像素；原图缺失、超限或无效时备份失败，不生成“成功但丢壁纸”的档案。新特性的跨旧APK降级恢复不保证旧APK识别wallpaper元数据。

## 验证与边界

- Android16虚拟机隔离测试43项：实际Bitmap/URI/File/JSON/ZIP/SHA代码，提取的生产壁纸复制/恢复方法；自选原图字节、目标私有URI重定位、默认、透明底层选择、旧档缺失字段保留、壁纸回滚、路径/版本/取消/超限拒绝、自动别名保护、历史哈希保护、改进版原图逐文件恢复、自定义上传图片逐字节恢复、单应用图标包选择、损坏源拒绝与缓存原子切换。Launcher PID28444保持；测试没有读取/修改已安装Launcher数据。
- 读取实际2.86MB和28.84MB用户归档，原始校验通过；大档仍接受全部508条原图记录。布局/快捷方式数据库拥有者在隔离测试中是受控边界，不将此称为真实数据库合并或完整SAF UI恢复验收。
- 生产PreferenceBackupCodec 25项检查，包括全局改进版/图标包选择往返。既有主题/系统壁纸同步47项检查通过。
- build.bat、APK签名、16KiB zipalign通过；Android16虚拟机安装启动，HOME可见。没有在真机覆盖安装或执行真实布局恢复。完整图标包素材呈现、分身/多用户、真实SAF选择文件→恢复→首帧、所有主题壁纸仍待现场验收；不能把元数据/字节测试称为全图标视觉通过。

交付APK：build/backup-wallpaper-20261014/launcher-backup-wallpaper.apk，SHA256 43A8F180580944B7DF447ADC166941304C737CEA3707940A030729C9206F0F2E，v1.5.8/33。临时filtered.slauncherbackup仅为隔离验算，不作为替换用户备份的交付文件。

修改文件：backup/RestoreIconSourceReconciler.java、ThemeBackupCodec.java、BackupValidator.java、DesktopBackupController.java、DesktopRestoreController.java，theme/MaintainedLauncherSettingsHost.java；测试tools/tests/backup_wallpaper与backup_preferences。未改原版SMEngine、备份SAF入口、布局结构或用户备份格式基础。更新DEVELOPMENT_LOG与INDEX，未更新MEMORY.md。
