"""Execute the actual Ra.T Smali branches with controlled input/event callbacks.
Animation math is covered separately by run_tests.py; this verifies stage and identity gates.
"""
from pathlib import Path
import argparse,re,struct,math,json
class Obj:
 def __init__(self,role,**fields):self.role=role;self.fields=fields

def method(path,signature):
 s=path.read_text(encoding='utf8');a=s.index('.method '+signature);return s[a:s.index('.end method',a)]

def execute(body,receiver,value,env):
 lines=[x.split('#',1)[0].strip() for x in body.splitlines()]
 labels={x:i for i,x in enumerate(lines) if x.startswith(':')}
 regs={'p0':receiver,'p1':value};regs.update(env.get('registers',{}));result=None;pc=0
 while pc<len(lines):
  x=lines[pc];pc+=1
  if not x or x[0] in '.:':continue
  if x.startswith('return-void'):return None
  if x.startswith('return '):return regs[x.split()[1]]
  if x.startswith('move-result'):
   regs[x.split()[1]]=result;continue
  m=re.fullmatch(r'move(?:-object)? (\w+), (\w+)',x)
  if m:regs[m[1]]=regs[m[2]];continue
  m=re.fullmatch(r'iget(?:-object|-boolean)? (\w+), (\w+), .*;->(\w+):.*',x)
  if m:regs[m[1]]=regs[m[2]].fields[m[3]];continue
  m=re.fullmatch(r'sget-object (\w+), (L[^;]+;)->(\w+):.*',x)
  if m:regs[m[1]]=env['static_fields'][(m[2],m[3])];continue
  m=re.fullmatch(r'if-(eqz|nez) (\w+), (:\w+)',x)
  if m:
   if (not bool(regs[m[2]]))==(m[1]=='eqz'):pc=labels[m[3]]
   continue
  m=re.fullmatch(r'if-(eq|ne) (\w+), (\w+), (:\w+)',x)
  if m:
   if (regs[m[2]]==regs[m[3]])==(m[1]=='eq'):pc=labels[m[4]]
   continue
  if x.startswith('goto '):pc=labels[x.split()[1]];continue
  m=re.fullmatch(r'const/high16 (\w+), (0x[0-9a-f]+)',x)
  if m:regs[m[1]]=struct.unpack('!f',int(m[2],16).to_bytes(4,'big'))[0];continue
  m=re.fullmatch(r'div-float (\w+), (\w+), (\w+)',x)
  if m:regs[m[1]]=regs[m[2]]/regs[m[3]];continue
  m=re.fullmatch(r'invoke-(static|virtual|interface) \{([^}]*)\}, (L[^;]+;)->(\w+)\(.*',x)
  if m:
   args=[regs[z.strip()] for z in m[2].split(',') if z.strip()];owner,name=m[3],m[4]
   if name=='getInstance':result=env['controller']
   elif name=='Ch':result=args[0].fields['folder']
   elif name=='Zr':result=args[0].fields['opening']
   elif name=='folderCreationAnimationDelta':result=execute(env['accessor'],args[0],args[1],env)
   elif name=='folderAnimationFrameDelta':
    env['normalized']+=1;result=env['normalizer'](*args)
   elif owner=='Lcom/smartisanos/launcher/data/FolderCellPositionAdapter;' and name=='adjustY':
    result=env['adjust_y'](*args)
   else:
    obj,*vals=args;env['log'].append((obj.role,name,vals));result=None
    if obj.role==env.get('phase') and name in ('update','d'):
     env['change'](env)
   continue
  raise AssertionError('Unsupported actual Smali instruction: '+x)
 raise AssertionError('No return')

def main():
 ap=argparse.ArgumentParser(__doc__);ap.add_argument('--source',type=Path,default=Path('launcher/smali/com/smartisanos/smengine/Ra.smali'));ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
 body=method(args.source,'public T(F)V');accessor=method(Path('launcher/smali/com/smartisanos/launcher/view/Eb.smali'),'public folderCreationAnimationDelta(F)F')
 checks=0;cases=[]
 for phase in ['input','event','listener']:
  for initial in [None,Obj('old',opening=False)]:
   for delta,normal in [(108.,20.),(72.,20.),(20.,20.),(10.,10.),(0.,0.),(100.,100.)]:
    controller=Obj('controller',folder=initial,fx=20.);folder=Obj('folder',opening=True)
    env=dict(controller=controller,accessor=accessor,normalized=0,log=[],phase=phase,normalizer=lambda elapsed,original,n=normal:n,change=lambda e,c=controller,f=folder:c.fields.update(folder=f))
    engine=Obj('engine',DU=True,EU=True,CU=Obj('listener'),yU=Obj('input'),zU=Obj('event'),uU=Obj('animation'),BU=Obj('physics'),vU=Obj('scene'),tU=Obj('timer'))
    execute(body,engine,delta,env)
    for role,name,values in env['log']:
     if role=='animation':assert values==[normal],(phase,delta,normal,values)
     if role in ['input','event','timer'] or (role=='listener' and name=='b'):assert values==[delta]
     if role=='physics':assert values==[delta/1000]
     checks+=1
    assert env['normalized']==1;checks+=1
    cases.append(dict(phase=phase,delta=delta,animationDelta=normal))
 # Identity/no-folder/closing/no-host transitions must retain the caller's delta.
 for action in ['unchanged','close','absent','replace-closing','host-removed','no-host','not-ready','no-post-update']:
  controller=Obj('controller',folder=Obj('folder',opening=True),fx=20.)
  def change(e):
   if action=='close':controller.fields['folder'].fields['opening']=False
   elif action=='absent':controller.fields['folder']=None
   elif action=='replace-closing':controller.fields['folder']=Obj('new',opening=False)
   elif action=='host-removed':e['controller']=None
  env=dict(controller=None if action=='no-host' else controller,accessor=accessor,normalized=0,log=[],phase='input',normalizer=lambda a,b:20.,change=change)
  engine=Obj('engine',DU=action!='not-ready',EU=action!='no-post-update',CU=None,yU=Obj('input'),zU=Obj('event'),uU=Obj('animation'),BU=Obj('physics'),vU=Obj('scene'),tU=Obj('timer'))
  execute(body,engine,108.,env);assert env['normalized']==0
  assert all(vals==[108.] for role,name,vals in env['log'] if role=='animation');checks+=2
  if action=='not-ready':assert not env['log'];checks+=1
  if action=='no-post-update':assert not any(role=='physics' for role,_,_ in env['log']);checks+=1
 for fx in [10.,30.]:
  controller=Obj('controller',folder=None,fx=fx)
  env=dict(controller=controller,accessor=accessor,normalized=0,log=[],phase='input',normalizer=lambda elapsed,original:original/2,change=lambda e:controller.fields.update(folder=Obj('new',opening=True)))
  engine=Obj('engine',DU=True,EU=False,CU=None,yU=Obj('input'),zU=Obj('event'),uU=Obj('animation'))
  execute(body,engine,108.,env)
  assert next(v for r,n,v in env['log'] if r=='animation')==[fx/2]
  assert env['normalized']==1;checks+=2
 args.output.mkdir(parents=True,exist_ok=True);(args.output/'summary.json').write_text(json.dumps(dict(checks=checks,creationCases=len(cases),identityBoundaries=8),indent=2));print('PASS FOLDER_CREATION_GATE checks='+str(checks))
if __name__=='__main__':main()
