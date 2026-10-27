"""Compare actual folder geometry owners across inputs and layout replacement.

--baseline-source points to the two pre-change Java files. No device settings change.
"""
from pathlib import Path
import argparse, subprocess, shutil, json

FIXTURES = {
'com/smartisanos/launcher/data/Constants.java': '''package com.smartisanos.launcher.data;
public class Constants {
 public static int calls; public static Object folder;
 public static Point[] pageCellCenterPoints;
 public static int getPAGE_1_3X3_MODE_FOLDER(){return 8;}
 public static Object mode(int mode){calls++;return folder;}
 public static class Point {public float x,y;public Point(float a,float b){x=a;y=b;}public Point(Point p){x=p.x;y=p.y;}}
 public static class Layout {public float folder_bookcase_width,page_view_margin_left,page_view_margin_right,icon_size_with_shadow,text_font_size;}
}''',
'com/smartisanos/launcher/view/b/t.java': '''package com.smartisanos.launcher.view.b;
public class t {public int mode=8;public int getSinglePageMode(){return mode;}}''',
'com/smartisanos/launcher/view/b/a.java': '''package com.smartisanos.launcher.view.b;
public class a {public t dl;public a(t owner){dl=owner;}}''',
'GeometryProbe.java': '''import com.smartisanos.launcher.data.*;
import com.smartisanos.launcher.data.Constants.*;
public class GeometryProbe {
 static int checks;
 static void check(boolean b){checks++;if(!b)throw new AssertionError("check "+checks);}
 static void emit(float f){System.out.print(Integer.toHexString(Float.floatToIntBits(f))+",");}
 public static void main(String[] args){
  com.smartisanos.launcher.view.b.t owner=new com.smartisanos.launcher.view.b.t();
  com.smartisanos.launcher.view.b.a page=new com.smartisanos.launcher.view.b.a(owner);
  int count=0;
  for(float scale:new float[]{.6666667f,1f,1.3333334f,2f}) {
   for(float text:new float[]{0f,30f,42f}) {
    Layout layout=new Layout();layout.folder_bookcase_width=1080*scale;
    layout.page_view_margin_left=30*scale;layout.page_view_margin_right=35*scale;
    layout.icon_size_with_shadow=182*scale;layout.text_font_size=text*scale;Constants.folder=layout;
    for(int length:new int[]{0,3,6,9,12}) {
     Point[] source=new Point[length];for(int i=0;i<length;i++)source[i]=new Point(i*7,(i/3-1)*-358*scale);
     if(length==9)source[4]=null;
     Constants.pageCellCenterPoints=source;Constants.calls=0;
     Point[] copy=(Point[])FolderCellPositionAdapter.adaptPositions(owner,source);
     check(copy!=source);check(copy.length==source.length);
     for(int i=0;i<length;i++) {
      check(copy[i]==null?source[i]==null:copy[i]!=source[i]);
      if(copy[i]!=null){emit(copy[i].x);emit(copy[i].y);}
      if(source[i]!=null)check(source[i].x==i*7);
     }
     for(int i=0;i<9;i++)emit(FolderCellPositionAdapter.adjustY(page,i/3,i%3,123f));
     count+=Constants.calls;System.out.println();
    }
   }
  }
  owner.mode=20;Point[] raw=new Point[]{new Point(1,2)};
  check(FolderCellPositionAdapter.adaptPositions(owner,raw)==raw);
  check(FolderCellPositionAdapter.adjustY(page,0,0,123f)==123f);
  check(FolderCellPositionAdapter.adaptPositions(new Object(),raw)==raw);
  check(FolderCellPositionAdapter.adjustY(null,0,0,123f)==123f);
  check(FolderCellPositionAdapter.adjustYByIndex(page,-1,123f)==123f);
  owner.mode=8;Constants.folder=null;
  check(FolderCellPositionAdapter.adaptPositions(owner,null)==null);
  check(FolderCellPositionAdapter.adjustY(page,0,0,123f)==123f);
  check(FolderVisualGeometry.rowGap(new Object())==358f);
  check(FolderVisualGeometry.contentGroupCenterCorrectionY(new Object())==0f);
  owner.mode=8;Constants.folder=new Layout();Object[] broken=new Object[]{new Object()};
  check(FolderCellPositionAdapter.adaptPositions(owner,broken)==broken);
  Object nonArray=new Object();check(FolderCellPositionAdapter.adaptPositions(owner,nonArray)==nonArray);
  System.err.println("CHECKS="+checks+" MODE_LOOKUPS="+count);
 }
}'''
}

def run_variant(source,out,jdk):
 out.mkdir(parents=True,exist_ok=True)
 for rel,code in FIXTURES.items():
  target=out/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(code,encoding='utf8')
 for name in ['FolderVisualGeometry.java','FolderCellPositionAdapter.java']:
  shutil.copy2(source/name,out/'com/smartisanos/launcher/data'/name)
 files=list(out.rglob('*.java'))
 subprocess.run([str(jdk/'bin/javac.exe'),'-encoding','UTF-8','-d',str(out),*map(str,files)],check=True,capture_output=True)
 result=subprocess.run([str(jdk/'bin/java.exe'),'-cp',str(out),'GeometryProbe'],check=True,capture_output=True,text=True)
 (out/'values.txt').write_text(result.stdout);(out/'counts.txt').write_text(result.stderr)
 return result

def main():
 ap=argparse.ArgumentParser(__doc__);ap.add_argument('--baseline-source',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--jdk',type=Path,required=True);args=ap.parse_args()
 source=Path(__file__).resolve().parents[3]/'launcher/tools/java/com/smartisanos/launcher/data'
 before=run_variant(args.baseline_source,args.output/'before',args.jdk)
 after=run_variant(source,args.output/'after',args.jdk)
 assert before.stdout==after.stdout,'Geometry changed; inspect values.txt'
 import re
 counts=[int(re.search(r'MODE_LOOKUPS=(\d+)',r.stderr)[1]) for r in [before,after]]
 assert counts[1]<counts[0],counts
 report=dict(geometryBitwiseEqual=True,modeLookupsBefore=counts[0],modeLookupsAfter=counts[1],checks=after.stderr.strip())
 (args.output/'summary.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))

if __name__=='__main__':main()
