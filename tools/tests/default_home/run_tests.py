"""Exercise production HOME detection and launch/return rules with controlled platform failures."""
import argparse
from pathlib import Path
import subprocess
import tempfile
import re
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / 'launcher/tools/java/com/smartisanos/launcher/theme/MaintainedLauncherSettingsHost.java'


def method(source, name):
    pos = source.index(name)
    start = source.rfind('\n    ', 0, pos) + 1
    brace = source.index('{', start)
    depth, end = 1, brace + 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}')
        end += 1
    return source[start:end]


def public_method(source, declaration):
    start = source.index(declaration)
    brace = source.index('{', start)
    depth, end = 1, brace + 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}')
        end += 1
    return source[start:end]


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--jdk', required=True)
    args = parser.parse_args()
    page = SOURCE.with_name('DefaultHomeSettingsPage.java').read_text(encoding='utf-8')
    assert not re.search(r'[\u4e00-\u9fff]', page), 'UI copy must live in resources'
    source = page + SOURCE.read_text(encoding='utf-8')
    names = ['int defaultHomeState(', 'String defaultHomeStatusMessage(',
             'String defaultHomeHelpMessage(', 'void checkDefaultHomeReturn(',
             'boolean isDefaultHomePage(', 'void showDefaultHomeCheck(', 'void updateDefaultHomePage(',
             'void openDefaultHomeSettings(Activity activity)',
             'void openDefaultHomeSettings(Activity activity, boolean allowRoleRequest)',
             'boolean requestHomeRole(', 'String text(']
    production = '\n'.join(method(source, name) for name in names)
    production += '\n' + public_method(source,
        '    public static boolean keepSettingsPageOnDesktopReturn(')
    # Exercise only the dedicated production result branch; unrelated image/backup
    # handlers are intentionally outside this fixture.
    result_start = source.index('    public static boolean onActivityResult(')
    result_end = source.index('        if (requestCode == REQUEST_BACKUP_TREE', result_start)
    production += '\n' + source[result_start:result_end] + '\n        return false;\n    }\n'
    resume_start = source.index('    public static void onSettingsHostResumed(')
    resume_end = source.index('        if (ownsSettingsSession(activity))', resume_start)
    production += '\n' + source[resume_start:resume_end] + '\n    }\n'
    fixture = r'''
 static final int REQUEST_DEFAULT_HOME=54041;
 static final String PREF_DEFAULT_HOME_PENDING="default_home_pending_v1", LOG_TAG="test";
 static final String PREF_DEFAULT_HOME_RETURN_PAGE="default_home_return_page_v2";
 static final String EXTRA_SHOW_QUICK_DESKTOP_SETTINGS="quick";
 static int checks, returnChecks, help;
 static void check(boolean c) { checks++; if(!c)throw new AssertionError("check "+checks); }
 static class Build { static String MANUFACTURER="Google",BRAND="google"; static class VERSION { static int SDK_INT=28; } }
 static class Log { static void w(String t,String m,Throwable e){} static void i(String t,String m){if(m.startsWith("DEFAULT_HOME_CHECK state="))returnChecks++;} }
 static class Animator {void cancel(){}}
 static class View {
   static final int LAYER_TYPE_NONE=0,VISIBLE=0,GONE=8;
   int visibility,background;
   String page="MAIN",text=""; Map<String,View> children=new HashMap<String,View>();
   Object getTag(){return page;} Animator animate(){return new Animator();}
   void setTranslationX(float value){} void setLayerType(int type,Object paint){}
   void setVisibility(int value){visibility=value;}void setBackgroundResource(int value){background=value;}
 }
 static class ViewGroup extends View {
   List<View> views=new ArrayList<View>();int getChildCount(){return views.size();}
   View getChildAt(int i){return views.get(i);}void removeViewAt(int i){views.remove(i);}
 }
 static class ScrollView {int getScrollY(){return 0;}}
 static ScrollView firstScrollView(View view){return null;}
 static class Resources {
   static boolean english;
   static Map<String,String> zh=new HashMap<String,String>(),en=new HashMap<String,String>();
   Map<Integer,String> keys=new HashMap<Integer,String>();
   int getIdentifier(String key,String type,String pkg){int id=key.hashCode();keys.put(id,key);return id;}
   String getString(int id){return (english?en:zh).get(keys.get(id));}
 }
 static Resources getMaintainedResources(Activity a){return new Resources();}
 static int drawable(Resources r,String name){return 1;}
 static boolean canShowDialog(Activity a){return a!=null;}
 static String settingsPageId(View v){return v==null?null:v.page;}
 static View find(Resources r,View root,String key){if(!root.children.containsKey(key))root.children.put(key,new View());return root.children.get(key);}
 static void setText(View view,String text){view.text=text;}
 static class Intent {
   static final String ACTION_MAIN="main", CATEGORY_HOME="home",CATEGORY_LAUNCHER="launcher";
   String action;boolean search,quick;Set<String> categories=new HashSet<String>();
   Intent(String a){action=a;} Intent addCategory(String c){categories.add(c);return this;}
   String getAction(){return action;} boolean hasCategory(String category){return categories.contains(category);}
   boolean getBooleanExtra(String key,boolean fallback){return key.equals("launcher_show_search")?search:key.equals("quick")?quick:fallback;}
 }
 static class ActivityNotFoundException extends RuntimeException {}
 static class Settings { static final String ACTION_SETTINGS="settings"; }
 static class ActivityInfo { String packageName,name; ActivityInfo(String p,String n){packageName=p;name=n;} }
 static class ResolveInfo { ActivityInfo activityInfo; ResolveInfo(String p,String n){activityInfo=new ActivityInfo(p,n);} }
 static class PackageManager {
   static final int MATCH_DEFAULT_ONLY=65536;
   ResolveInfo selected; List<ResolveInfo> candidates=new ArrayList<ResolveInfo>(); boolean fail;
   ResolveInfo resolveActivity(Intent i,int f){if(fail)throw new SecurityException();return selected;}
   List<ResolveInfo> queryIntentActivities(Intent i,int f){return candidates;}
 }
 static class SharedPreferences {
   boolean pending,save=true; String returnPage=""; Editor edit(){return new Editor();}
   boolean getBoolean(String k,boolean d){return pending;}
   class Editor {
     boolean value;
     Editor putBoolean(String k,boolean v){value=v;return this;}
     Editor putString(String k,String v){returnPage=v;return this;}
     Editor remove(String k){if(k.equals(PREF_DEFAULT_HOME_PENDING))value=false;else if(k.equals(PREF_DEFAULT_HOME_RETURN_PAGE))returnPage="";return this;}
     void apply(){pending=value;} boolean commit(){if(save)apply();return save;}
   }
 }
 static class Context {
   static final int MODE_PRIVATE=0;
   PackageManager pm=new PackageManager(); Object role; SharedPreferences prefs=new SharedPreferences();
   Object getSystemService(String s){return role;}
   String getPackageName(){return "ours";} PackageManager getPackageManager(){return pm;}
   SharedPreferences getSharedPreferences(String n,int m){return prefs;}
 }
 static class Activity extends Context {
   View root=new View(); <T extends View>T findViewById(int id){return (T)root;}
   int attempts,code; String last; int allowAt=0;
   void startActivityForResult(Intent i,int c){
     attempts++; code=c;last=i.action;
     if(attempts<=allowAt)throw new ActivityNotFoundException();
   }
 }
 static void logOperation(Activity a,String k,String s){}
 static void showInfoDialog(Activity a,String t,String m){help++;}
 public static void main(String[] args) {
   check(defaultHomeState(null)==-1);
   Context c=new Context(); check(defaultHomeState(c)==-1);
   c.pm.selected=new ResolveInfo("android","ResolverActivity");
   c.pm.candidates.add(new ResolveInfo("ours","Launcher")); check(defaultHomeState(c)==-1);
   c.pm.selected=new ResolveInfo("ours","Launcher"); check(defaultHomeState(c)==1);
   c.pm.selected=new ResolveInfo("other","Home"); check(defaultHomeState(c)==-1);
   c.pm.candidates.add(c.pm.selected); check(defaultHomeState(c)==0);
   c.pm.fail=true; check(defaultHomeState(c)==-1); c.pm.fail=false;
   Build.VERSION.SDK_INT=29;
   android.app.role.RoleManager r=new android.app.role.RoleManager(); c.role=r;
   r.held=true; check(defaultHomeState(c)==1);
   r.held=false; check(defaultHomeState(c)==0);
   c.pm.selected=new ResolveInfo("ours","Launcher"); check(defaultHomeState(c)==0);
   r.fail=true; check(defaultHomeState(c)==-1);
   r.fail=false;r.available=false;check(defaultHomeState(c)==1);
   c.role=null;check(defaultHomeState(c)==1);
   check(defaultHomeStatusMessage(0).contains("系统尚未确认默认桌面设置生效"));
   check(defaultHomeStatusMessage(-1).contains("无法可靠确认"));
   check(!defaultHomeStatusMessage(-1).contains("已确认锤子桌面"));
   check(defaultHomeHelpMessage("vivo","vivo").contains("如果系统提供"));
   check(defaultHomeHelpMessage("OPPO","OPPO").contains("若系统提供"));
   check(!defaultHomeHelpMessage("Google","google").contains("CTS"));
   check(defaultHomeHelpMessage("vivo","vivo").length()<150);
   Activity a=new Activity();a.prefs.pending=true;checkDefaultHomeReturn(a);
   check(returnChecks==1&&!a.prefs.pending);checkDefaultHomeReturn(a);check(returnChecks==1);
   // API 28: fallbacks retain pending only after a system screen really opened.
   Build.VERSION.SDK_INT=28;
   a=new Activity();openDefaultHomeSettings(a);check(a.attempts==1&&a.prefs.pending&&a.code==REQUEST_DEFAULT_HOME);
   a=new Activity();a.allowAt=2;openDefaultHomeSettings(a);check(a.attempts==3&&a.prefs.pending);
   a=new Activity();a.allowAt=99;int before=help;openDefaultHomeSettings(a);
   check(a.attempts==4&&!a.prefs.pending&&help==before);
   check(a.root.children.get("default_home_instructions").text.contains("无法打开系统设置"));
   a=new Activity();a.prefs.save=false;openDefaultHomeSettings(a);check(a.attempts==0&&!a.prefs.pending);
   // Opening a chooser must never call the status-success path.
   check(returnChecks==1);
   Build.VERSION.SDK_INT=29;
   a=new Activity();r=new android.app.role.RoleManager();r.request=new Intent("role-request");a.role=r;
   openDefaultHomeSettings(a);check(a.attempts==1&&"role-request".equals(a.last)&&a.prefs.pending);
   check(a.code==REQUEST_DEFAULT_HOME&&returnChecks==1);
   a=new Activity();a.role=r;openDefaultHomeSettings(a,false);
   check(a.attempts==1&&"android.settings.HOME_SETTINGS".equals(a.last));
   a=new Activity();r.held=true;a.role=r;openDefaultHomeSettings(a);
   check(a.attempts==1&&"android.settings.HOME_SETTINGS".equals(a.last));
   // Immediate cancellation need not be followed by onResume. A later Resume
   // must not consume the same result twice; RESULT_OK follows the same rule.
   a=new Activity();a.prefs.pending=true;int previous=returnChecks;
   check(onActivityResult(a,REQUEST_DEFAULT_HOME,0,null));check(returnChecks==previous+1);
   checkDefaultHomeReturn(a);check(returnChecks==previous+1);
   a.prefs.pending=true;check(onActivityResult(a,REQUEST_DEFAULT_HOME,-1,null));
   check(returnChecks==previous+2&&!a.prefs.pending);
   a.prefs.pending=true;check(!onActivityResult(a,123,0,null)&&a.prefs.pending);
   a=new Activity();a.root.page="DEFAULT_HOME";Build.VERSION.SDK_INT=28;
   a.pm.selected=new ResolveInfo("ours","Launcher");a.pm.candidates.add(a.pm.selected);
   showDefaultHomeCheck(a);
   check(a.root.children.get("default_home_status").text.equals("锤子桌面"));
   check(a.root.children.get("default_home_recheck").visibility==View.GONE);
   check(a.root.children.get("default_home_instructions").visibility==View.GONE);
   a.pm.selected=new ResolveInfo("other","Home");a.pm.candidates.add(a.pm.selected);showDefaultHomeCheck(a);
   check(a.root.children.get("default_home_status").text.equals("尚未设置"));
   check(a.root.children.get("default_home_instructions").text.contains("选择"));
   a.pm.fail=true;showDefaultHomeCheck(a);check(a.root.children.get("default_home_status").text.contains("无法确认"));
   check(a.root.children.get("default_home_recheck").visibility==View.VISIBLE);
   a.root=new View();a.prefs.pending=true;checkDefaultHomeReturn(a);
   check(a.root.children.isEmpty()&&!a.prefs.pending);
   a=new Activity();a.root.page="DEFAULT_HOME";openDefaultHomeSettings(a,false);
   check(a.prefs.returnPage.equals("DEFAULT_HOME"));checkDefaultHomeReturn(a);
   check(!a.prefs.pending&&a.prefs.returnPage.equals("DEFAULT_HOME"));
   a.root.page="MAIN";onSettingsHostResumed(a);check(a.prefs.returnPage.equals("DEFAULT_HOME"));
   a.root.page="DEFAULT_HOME";onSettingsHostResumed(a);check(a.prefs.returnPage.isEmpty());
   check(isDefaultHomePage("DEFAULT_HOME")&&!isDefaultHomePage("DEFAULT_HOME_HELP")&&!isDefaultHomePage("MAIN"));
   a=new Activity();ViewGroup group=new ViewGroup();View page=new View();page.page="DEFAULT_HOME";
   group.views.add(page);a.root=group;
   check(keepSettingsPageOnDesktopReturn(a,new Intent(null)));
   check(!keepSettingsPageOnDesktopReturn(a,new Intent("install-update")));
   Intent search=new Intent(Intent.ACTION_MAIN);search.search=true;
   check(!keepSettingsPageOnDesktopReturn(a,search));
   Intent quick=new Intent(Intent.ACTION_MAIN);quick.quick=true;
   check(!keepSettingsPageOnDesktopReturn(a,quick));
   page.page="MAIN";check(!keepSettingsPageOnDesktopReturn(a,new Intent(null)));
   check(keepSettingsPageOnDesktopReturn(a,new Intent(Intent.ACTION_MAIN).addCategory(Intent.CATEGORY_LAUNCHER)));
   page.page="DEFAULT_HOME";group.views.add(0,new View());
   check(keepSettingsPageOnDesktopReturn(a,new Intent(null))&&group.getChildCount()==1&&group.getChildAt(0)==page);
   System.out.println("PASS production HOME checks="+checks);
 }
'''
    fixture = re.sub(r'defaultHomeStatusMessage\((?!Resources resources)([^)]*)\)',
                     r'defaultHomeStatusMessage(new Resources(), \1)', fixture)
    fixture = fixture.replace('defaultHomeHelpMessage(', 'defaultHomeHelpMessage(new Resources(), ')
    res = ROOT / 'launcher/tools/maintained_settings_res/res'
    translations = {locale: {node.attrib['name']: node.text for node in
                    ET.parse(res / folder / 'default_home_guidance.xml').getroot()}
                    for locale, folder in [('en', 'values-en'), ('zh', 'values-zh-rCN')]}
    assert translations['en'].keys() == translations['zh'].keys()
    assert translations['en'] == {node.attrib['name']: node.text for node in
                                ET.parse(res / 'values/default_home_guidance.xml').getroot()}
    init = 'static {\n' + '\n'.join(
        'Resources.' + locale + '.put(' + json.dumps(key, ensure_ascii=False) + ','
        + json.dumps(value, ensure_ascii=False) + ');'
        for locale, entries in translations.items() for key, value in entries.items()) + '\n}\n'
    fixture += init
    fixture = fixture.replace('   System.out.println("PASS production HOME checks="+checks);', '''
   Resources.english=true;
   check(defaultHomeStatusMessage(new Resources(),0).contains("not confirmed"));
   check(defaultHomeStatusMessage(new Resources(),-1).contains("cannot reliably confirm"));
   check(defaultHomeHelpMessage(new Resources(),"vivo","vivo").contains("If your system offers"));
   check(defaultHomeHelpMessage(new Resources(),"OPPO","OPPO").contains("only if"));
   check(defaultHomeHelpMessage(new Resources(),"Google","google").contains("Home app"));
   a=new Activity();a.root.page="DEFAULT_HOME";Build.VERSION.SDK_INT=28;
   a.pm.selected=new ResolveInfo("ours","Launcher");a.pm.candidates.add(a.pm.selected);
   showDefaultHomeCheck(a);check(a.root.children.get("default_home_status").text.equals("Smartisan Launcher"));
   Resources.english=false;
   System.out.println("PASS production HOME checks="+checks);''')
    role = '''package android.app.role;
public class RoleManager {
 public static final String ROLE_HOME="home";
 public boolean available=true,held,fail;
 public Object request;
 public Object createRequestRoleIntent(String role){return request;}
 public boolean isRoleAvailable(String role){if(fail)throw new SecurityException();return available;}
 public boolean isRoleHeld(String role){return held;}
}'''
    with tempfile.TemporaryDirectory(prefix='default-home-') as temporary:
        base = Path(temporary)
        (base/'HomeTest.java').write_text('import java.util.*;\npublic class HomeTest {\n'+production+fixture+'\n}', encoding='utf-8')
        (base/'RoleManager.java').write_text(role, encoding='utf-8')
        (base/'R.java').write_text('package android; public class R {public static class id {public static int content=1;}}', encoding='utf-8')
        subprocess.run([str(Path(args.jdk)/'bin/javac.exe'), '-encoding', 'UTF-8', '-d', str(base),
                        str(base/'HomeTest.java'), str(base/'RoleManager.java'), str(base/'R.java')], check=True)
        subprocess.run([str(Path(args.jdk)/'bin/java.exe'), '-cp', str(base), 'HomeTest'], check=True)


if __name__ == '__main__':
    main()
