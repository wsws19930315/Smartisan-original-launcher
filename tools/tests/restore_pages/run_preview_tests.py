"""Exercise production backup preview counts, including legacy optional omissions.

No archive import or installed Launcher data is used. JSON boundaries reuse the
existing preference suite's doubles; the actual BackupArchiveReader is compiled.
"""
import argparse
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
B = 'com/smartisanos/launcher/backup/'
spec = importlib.util.spec_from_file_location('preference_fixtures', Path(__file__).parent.parent / 'backup_preferences/run_tests.py')
fixtures = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixtures)
SOURCES = {k: fixtures.SOURCES[k] for k in ('org/json/JSONObject.java', 'org/json/JSONArray.java')}
SOURCES['org/json/JSONObject.java'] = SOURCES['org/json/JSONObject.java'][:-1] + '''
public int optInt(String k,int d){Object v=opt(k);return v instanceof Number?((Number)v).intValue():d;}}'''
SOURCES['org/json/JSONArray.java'] = SOURCES['org/json/JSONArray.java'][:-1] + '''
public JSONObject optJSONObject(int i){return i>=0&&i<a.size()&&a.get(i) instanceof JSONObject?(JSONObject)a.get(i):null;}}'''
SOURCES[B + 'BackupManifest.java'] = 'package com.smartisanos.launcher.backup;public class BackupManifest{}'
SOURCES[B + 'BackupValidator.java'] = '''package com.smartisanos.launcher.backup;import java.io.*;
public class BackupValidator{public static BackupArchiveReader.ValidatedBackup validateAndExtract(File a,File b){throw new AssertionError("Archive IO must not occur in preview count tests");}}'''
SOURCES[B + 'PreviewTest.java'] = '''package com.smartisanos.launcher.backup;
import org.json.*;public class PreviewTest{
 static int checks;
 static JSONObject item(int type,int folder,int page,int cell){return new JSONObject().put("itemType",type).put("folderIndex",folder).put("pageIndex",page).put("cellIndex",cell);}
 static BackupArchiveReader.ValidatedBackup backup(JSONArray items){return new BackupArchiveReader.ValidatedBackup(null,null,new BackupManifest(),new JSONObject().put("items",items),new JSONObject(),new JSONObject(),new JSONObject(),new JSONObject(),new JSONObject());}
 static void expect(int pages,JSONArray items){checks++;int actual=backup(items).pageCount();if(actual!=pages)throw new AssertionError("pages expected="+pages+" actual="+actual+" case="+checks);}
 public static void main(String[] args){
  expect(1,new JSONArray().put(item(2,0,3,0))); // A page containing only an empty root folder.
  expect(0,new JSONArray());
  expect(1,new JSONArray().put(item(0,-1,3,0)));
  expect(1,new JSONArray().put(item(2,0,3,0)).put(item(0,10,0,0)).put(item(0,10,8,12)));
  expect(2,new JSONArray().put(item(2,0,3,0)).put(item(2,0,7,1)));
  expect(1,new JSONArray().put(item(2,0,3,0)).put(item(0,-1,3,1)));
  expect(0,new JSONArray().put(item(0,10,3,0))); // Child's internal page is not a desktop page.
  expect(0,new JSONArray().put(item(2,0,-1,0)).put(item(0,-1,-2,0)));
  expect(0,new JSONArray().put(item(2,0,3,-1)));
  expect(1,new JSONArray().put(item(2,-1,3,0))); // Historical root representation.
  JSONObject legacy=item(0,-1,2,0);legacy.remove("folderIndex");legacy.remove("itemType");
  expect(1,new JSONArray().put(legacy));
  JSONObject missingPage=item(0,-1,2,0);missingPage.remove("pageIndex");expect(0,new JSONArray().put(missingPage));
  expect(0,new JSONArray().put("not-an-item"));
  expect(1,new JSONArray().put(item(1,-1,2,0))); // Root shortcut.
  checks++;if(backup(new JSONArray().put(legacy)).itemCount()!=1)throw new AssertionError("item count changed");
  BackupArchiveReader.ValidatedBackup noItems=new BackupArchiveReader.ValidatedBackup(null,null,new BackupManifest(),new JSONObject(),new JSONObject(),new JSONObject(),new JSONObject(),new JSONObject(),new JSONObject());
  checks++;if(noItems.pageCount()!=0||noItems.itemCount()!=0||noItems.customIconCount()!=0)throw new AssertionError("optional arrays");
  for(int page:new int[]{0,1,999})for(int cell:new int[]{0,1,11,19}){
   expect(1,new JSONArray().put(item(2,0,page,cell)));
   expect(1,new JSONArray().put(item(0,-1,page,cell)));
   expect(0,new JSONArray().put(item(0,42,page,cell)));
  }
  System.out.println("PASS production backup preview checks="+checks);
 }
}'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jdk', type=Path, required=True)
    parser.add_argument('--reader', type=Path, help='Saved pre-fix reader for negative control')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='restore-preview-') as temporary:
        base = Path(temporary)
        files = []
        for name, source in SOURCES.items():
            path = base / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(source, encoding='utf-8')
            files.append(str(path))
        reader = ROOT / 'launcher/tools/java' / B / 'BackupArchiveReader.java'
        if args.reader:
            reader = base / B / 'BackupArchiveReader.java'
            reader.write_bytes(args.reader.read_bytes())
        files.append(str(reader))
        subprocess.run([str(args.jdk / 'bin/javac.exe'), '-encoding', 'UTF-8', '-d', str(base), *files], check=True)
        subprocess.run([str(args.jdk / 'bin/java.exe'), '-cp', str(base), B.replace('/', '.')+'PreviewTest'], check=True)


if __name__ == '__main__':
    main()
