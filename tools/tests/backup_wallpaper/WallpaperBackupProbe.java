package com.smartisanos.launcher.backup;
import android.content.*;import android.graphics.*;import android.net.Uri;import org.json.*;import java.io.*;import java.lang.reflect.*;import java.util.*;
import com.smartisanos.launcher.theme.MaintainedLauncherSettingsHost;
import com.smartisanos.launcher.data.redirectIcon.*;
public class WallpaperBackupProbe {
 static int checks;static void check(boolean b,String name){checks++;if(!b)throw new AssertionError(name);}
 interface Action{void run()throws Exception;}
 static void rejects(Action a,String name)throws Exception{try{a.run();}catch(Exception e){check(true,name);return;}throw new AssertionError(name);}
 static class C extends ContextWrapper {
  final File files;final Map<String,Map<String,Object>> maps=new HashMap<>();
  C(Context base,File f){super(base);files=f;f.mkdirs();}
  @Override public File getFilesDir(){return files;}
  @Override public SharedPreferences getSharedPreferences(final String file,int mode){
   Map<String,Object> values=maps.get(file);if(values==null){values=new HashMap<>();maps.put(file,values);}final Map<String,Object> m=values;final Object[] edit=new Object[1];
   edit[0]=Proxy.newProxyInstance(getClass().getClassLoader(),new Class[]{SharedPreferences.Editor.class},(p,k,a)->{String n=k.getName();if(n.equals("commit"))return true;if(n.equals("apply"))return null;if(n.equals("clear"))m.clear();else if(n.equals("remove"))m.remove(a[0]);else if(n.startsWith("put"))m.put((String)a[0],a[1]);return edit[0];});
   return (SharedPreferences)Proxy.newProxyInstance(getClass().getClassLoader(),new Class[]{SharedPreferences.class},(p,k,a)->{String n=k.getName();if(n.equals("edit"))return edit[0];if(n.equals("getAll"))return new HashMap<>(m);if(n.equals("contains"))return m.containsKey(a[0]);if(n.startsWith("get"))return m.containsKey(a[0])?m.get(a[0]):a[1];return null;});
  }
 }
 static JSONObject emptyLayout()throws Exception{return new JSONObject().put("items",new JSONArray()).put("pages",new JSONArray());}
 static void source(C c,File f){c.getSharedPreferences("launcher_settings",0).edit().putString("launcher_wallpaper_uri",Uri.fromFile(f).toString()).commit();}
 static File image(File f)throws Exception{Bitmap b=Bitmap.createBitmap(240,320,Bitmap.Config.ARGB_8888);b.eraseColor(Color.rgb(40,100,150));FileOutputStream o=new FileOutputStream(f);try{check(b.compress(Bitmap.CompressFormat.PNG,100,o),"fixture image created");}finally{o.close();b.recycle();}return f;}
 static void validateImages()throws Exception {
  for(int[] size:new int[][]{{48,48},{1024,1024},{2048,32}}) {
   Bitmap bitmap=Bitmap.createBitmap(size[0],size[1],Bitmap.Config.ARGB_8888);
   bitmap.eraseColor(0x804080c0);ByteArrayOutputStream output=new ByteArrayOutputStream();
   try{check(bitmap.compress(Bitmap.CompressFormat.PNG,100,output),"validation fixture PNG");}finally{bitmap.recycle();}
   byte[] data=output.toByteArray(),original=data.clone();
   check(IconBackupCodec.isValidImage(data,1,Integer.MAX_VALUE),"custom raster remains valid");
   check(IconBackupCodec.isValidImage(data,48,1024)==(size[0]<=1024&&size[1]>=48),"portable dimensions checked");
   check(java.util.Arrays.equals(data,original),"image validation preserves original bytes/alpha");
  }
  check(!IconBackupCodec.isValidImage(new byte[]{1,2,3},1,Integer.MAX_VALUE),"invalid bitmap rejected");
 }
 public static void main(String[] args)throws Exception {
  validateImages();
  File root=new File(args[0]).getCanonicalFile();if(!root.getPath().startsWith("/data/local/tmp/wallpaper-backup-"))throw new IllegalArgumentException("outside fixture");android.os.Looper.prepareMainLooper();Class<?> t=Class.forName("android.app.ActivityThread");Object thread=t.getMethod("systemMain").invoke(null);Context system=(Context)t.getMethod("getSystemContext").invoke(thread);
  C a=new C(system,new File(root,"source")),b=new C(system,new File(root,"target"));File picture=image(new File(root,"photo.png"));source(a,picture);a.getSharedPreferences("launcher_settings",0).edit().putString("previous","smartisan_theme_blue").commit();
  File staging=new File(root,"staging");staging.mkdirs();JSONObject theme=ThemeBackupCodec.encode(a,staging,new DesktopBackupController.CancellationToken());check(theme.getJSONObject("wallpaper").getString("source").equals("selected"),"selected metadata");check(!theme.toString().contains("file:"),"archive contains no source device URI");File copied=new File(staging,"wallpaper/selected-image");check(BackupFileUtils.sha256(copied).equals(BackupFileUtils.sha256(picture)),"one lossless original");
  ThemeBackupCodec.restoreWallpaper(b,theme,staging);String restored=MaintainedLauncherSettingsHost.selected(b);check(restored.startsWith(Uri.fromFile(b.files).toString()+"/"),"URI rebased to target");File actual=new File(Uri.parse(restored).getPath());check(BackupFileUtils.sha256(actual).equals(BackupFileUtils.sha256(picture)),"restored bytes match");check(b.getSharedPreferences("launcher_settings",0).getString("previous","").equals("smartisan_theme_blue"),"underlying transparent theme preserved");
  JSONObject legacy=new JSONObject();ThemeBackupCodec.restoreWallpaper(b,legacy,staging);check(restored.equals(MaintainedLauncherSettingsHost.selected(b)),"legacy archive omission preserves existing wallpaper");
  JSONObject defaults=new JSONObject().put("wallpaper",new JSONObject().put("version",1).put("source","default"));ThemeBackupCodec.restoreWallpaper(b,defaults,staging);check(MaintainedLauncherSettingsHost.selected(b).length()==0,"explicit default clears selected source");
  ThemeBackupCodec.restoreWallpaper(b,theme,staging);File rollback=new File(root,"rollback");rollback.mkdirs();JSONObject snapshot=ThemeBackupCodec.encode(b,rollback,null);ThemeBackupCodec.restoreWallpaper(b,defaults,staging);ThemeBackupCodec.restoreWallpaper(b,snapshot,rollback);check(BackupFileUtils.sha256(new File(Uri.parse(MaintainedLauncherSettingsHost.selected(b)).getPath())).equals(BackupFileUtils.sha256(picture)),"rollback restores original image");
  for(String reference:new String[]{"../photo.png","/sdcard/photo.png","content://foreign/picture"}){
   final JSONObject bad=new JSONObject().put("wallpaper",new JSONObject().put("version",1).put("source","selected").put("file",reference));rejects(()->ThemeBackupCodec.validateWallpaper(bad,staging),"unsafe image reference rejected");
  }
  final JSONObject newer=new JSONObject().put("wallpaper",new JSONObject().put("version",2).put("source","default"));rejects(()->ThemeBackupCodec.validateWallpaper(newer,staging),"unknown version rejected");
  final JSONObject badDefault=new JSONObject().put("wallpaper",new JSONObject().put("version",1).put("source","default").put("file","wallpaper/selected-image"));rejects(()->ThemeBackupCodec.validateWallpaper(badDefault,staging),"default cannot reference foreign image");
  final JSONObject badPrevious=new JSONObject().put("wallpaper",new JSONObject().put("version",1).put("source","default").put("previousTheme","smartisan_theme_trans"));rejects(()->ThemeBackupCodec.validateWallpaper(badPrevious,staging),"alpha overlay cannot be underlying theme");
  DesktopBackupController.CancellationToken cancelled=new DesktopBackupController.CancellationToken();cancelled.cancelled=true;rejects(()->ThemeBackupCodec.encode(a,new File(root,"cancelled"),cancelled),"copy honours cancellation");
  File large=new File(root,"oversize");RandomAccessFile sparse=new RandomAccessFile(large,"rw");sparse.setLength(20L*1024L*1024L+1);sparse.close();source(a,large);rejects(()->ThemeBackupCodec.encode(a,new File(root,"large"),null),"oversize image not silently omitted");source(a,picture);
  JSONObject layout=emptyLayout();layout.getJSONArray("items").put(new JSONObject().put("packageName","org.example.current"));JSONObject icons=new JSONObject().put("records",new JSONArray().put(new JSONObject().put("packageName","org.example.saved").put("drawableName","resource:org.example.chosen")));
  HashSet<String> names=RestoreIconSourceReconciler.requiredSourceFiles(layout,icons);for(String id:new String[]{"org.example.current","org.example.saved","org.example.chosen"}){check(names.contains(id+".png"),"package/sourceId filename retained");check(names.contains(Integer.toHexString(id.hashCode())+".png"),"historical hash filename retained");}check(!names.contains("org.example.browsed.png"),"unused browse cache excluded");
  File cache=new File(a.files,"online_icon_cache_v4");cache.mkdirs();BackupFileUtils.writeBytes(new File(cache,"org.example.current.png"),BackupFileUtils.readBytes(picture,100000));BackupFileUtils.writeBytes(new File(cache,"org.example.saved.png"),BackupFileUtils.readBytes(picture,100000));BackupFileUtils.writeBytes(new File(cache,"org.example.chosen.png"),BackupFileUtils.readBytes(picture,100000));BackupFileUtils.writeBytes(new File(cache,"org.example.browsed.png"),BackupFileUtils.readBytes(picture,100000));
  BackupFileUtils.writeBytes(new File(cache,"org.example.systemalias.png"),BackupFileUtils.readBytes(picture,100000));BackupFileUtils.writeBytes(new File(cache,"deadbeef.png"),BackupFileUtils.readBytes(picture,100000));
  JSONObject portable=RestoreIconSourceReconciler.encodePortableSources(a,new File(staging,"icons/sources"),layout,icons);check(portable.getJSONArray("records").length()==5,"active/saved/OEM alias and historical hash sources preserved");check(new File(cache,"org.example.browsed.png").isFile(),"cache itself never deleted");
  File targetCache=new File(b.files,"online_icon_cache_v4");targetCache.mkdirs();BackupFileUtils.writeBytes(new File(targetCache,"org.example.existing.png"),BackupFileUtils.readBytes(picture,100000));
  RestoreIconSourceReconciler.restorePortableSources(b,portable,staging);
  for(int i=0;i<portable.getJSONArray("records").length();i++){JSONObject row=portable.getJSONArray("records").getJSONObject(i);check(BackupFileUtils.sha256(new File(targetCache,row.getString("portableFile"))).equals(row.getString("sha256")),"improved raw source restored byte-for-byte");}
  check(new File(targetCache,"org.example.existing.png").isFile(),"restore preserves newer existing icon source");
  final JSONObject tampered=new JSONObject(portable.toString());tampered.getJSONArray("records").getJSONObject(0).put("sha256","invalid");rejects(()->RestoreIconSourceReconciler.restorePortableSources(b,tampered,staging),"bad improved source checksum rejected");check(new File(targetCache,"org.example.existing.png").isFile(),"failed source restore does not swap active cache");
  byte[] custom=BackupFileUtils.readBytes(picture,100000);RedirectIconInfo ci=new RedirectIconInfo();ci.packageName="org.example.custom";ci.componentName="CustomActivity";ci.drawableName="custom";ci.iconData=custom;RedirectIconDB.infos.add(ci);RedirectIconInfo pack=new RedirectIconInfo();pack.packageName="org.example.packed";pack.componentName="PackActivity";pack.drawableName="pack:org.example.iconpack:draw";RedirectIconDB.infos.add(pack);
  File customDir=new File(staging,"icons/custom");JSONObject customIndex=IconBackupCodec.encode(a,customDir);IconBackupCodec.restore(b,customIndex,staging);File customRestored=new File(new File(b.files,"redirect_icons"),Integer.toHexString((ci.packageName+";"+ci.componentName).hashCode())+".png");check(Arrays.equals(custom,BackupFileUtils.readBytes(customRestored,100000)),"custom uploaded icon bytes restored");check(b.getSharedPreferences("redirect_icon_db",0).getString("r."+pack.packageName+";"+pack.componentName+".drawable","").equals(pack.drawableName),"per-app iconpack selection restored");
  BackupManifest manifest=new BackupManifest();manifest.createdAt=System.currentTimeMillis();manifest.gridMode=12;manifest.screenWidth=1080;manifest.screenHeight=2400;JSONObject emptyIcons=new JSONObject().put("records",new JSONArray());File archive=BackupArchiveWriter.write(staging,manifest,emptyLayout(),new JSONObject(),theme,customIndex,emptyIcons,portable,nullToken());BackupArchiveReader.ValidatedBackup read=BackupArchiveReader.read(archive,new File(root,"extracted"));check(read.theme.has("wallpaper"),"new archive read validates image metadata and checksums");check(new File(read.extractedRoot,"wallpaper/selected-image").isFile(),"wallpaper payload round trip");
  BackupArchiveReader.ValidatedBackup old=BackupArchiveReader.read(new File(root,"old.slauncherbackup"),new File(root,"old-read"));check(!old.theme.has("wallpaper"),"2.86MB historical archive accepted");BackupArchiveReader.ValidatedBackup newerBackup=BackupArchiveReader.read(new File(root,"new.slauncherbackup"),new File(root,"new-read"));check(newerBackup.portableSources.getJSONArray("records").length()==508,"28.84MB historical sources still accepted");
  C saved=new C(system,new File(root,"saved-context"));File raw=new File(saved.files,"online_icon_cache_v4");raw.mkdirs();File[] inputs=new File(newerBackup.extractedRoot,"icons/sources").listFiles();for(File f:inputs)BackupFileUtils.writeBytes(new File(raw,f.getName()),BackupFileUtils.readBytes(f,512*1024));
  File filtered=new File(root,"filtered");filtered.mkdirs();JSONObject selectedSources=RestoreIconSourceReconciler.encodePortableSources(saved,new File(filtered,"icons/sources"),newerBackup.layout,newerBackup.icons);check(selectedSources.getJSONArray("records").length()==63,"user archive retains 37 direct references plus all legacy hash sources");
  File compact=BackupArchiveWriter.write(filtered,newerBackup.manifest,newerBackup.layout,newerBackup.settings,newerBackup.theme,newerBackup.icons,newerBackup.shortcutIcons,selectedSources,nullToken());BackupFileUtils.writeBytes(new File(root,"filtered.slauncherbackup"),BackupFileUtils.readBytes(compact,100L*1024L*1024L));check(compact.length()<3L*1024L*1024L,"source filtering reduces measured user archive without image reencoding");
  System.out.println("PASS WALLPAPER_BACKUP_CHECKS="+checks+" FILTERED_BYTES="+compact.length()+" LEGACY_AND_REFERENCED_SOURCES=63; controlled prefs/layout boundary, not complete UI restore acceptance");
 }
 static DesktopBackupController.CancellationToken nullToken(){return new DesktopBackupController.CancellationToken();}
}
