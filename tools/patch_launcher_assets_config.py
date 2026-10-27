"""Handle wallpaper palette asset updates without relaunching the original HOME.

Add only CONFIG_ASSETS_PATHS to the effective preserved binary Activity mask.
Mirror that effective mask in the text Manifest, whose old mask differed.
"""
from pathlib import Path
import re,struct,sys
sys.dont_write_bytecode = True
from patch_badge_service_manifest import read_pool,u16,u32,NO_INDEX

ROOT=Path(__file__).resolve().parents[1]
ASSETS_PATHS=0x80000000

def main():
    binary=ROOT/'launcher/original/AndroidManifest.xml'
    text=ROOT/'launcher/AndroidManifest.xml'
    data=bytearray(binary.read_bytes())
    _,_,strings,_=read_pool(data)
    offsets=[];pos=8
    while pos<len(data):
        kind,size=u16(data,pos),u32(data,pos+4)
        if size<8: raise ValueError('Invalid AXML chunk')
        if kind==0x0102 and strings[u32(data,pos+20)]=='activity':
            attrs=[pos+16+u16(data,pos+24)+i*u16(data,pos+26) for i in range(u16(data,pos+28))]
            name=next((strings[u32(data,a+16)] for a in attrs if strings[u32(data,a+4)]=='name'),None)
            if name=='com.smartisanos.launcher.Launcher':
                offsets.extend(a for a in attrs if strings[u32(data,a+4)]=='configChanges')
        pos+=size
    if len(offsets)!=1: raise ValueError('Expected one HOME configChanges attribute')
    attr=offsets[0]
    if u32(data,attr+8)!=NO_INDEX: raise ValueError('Unexpected raw configChanges string')
    old=u32(data,attr+16);updated=old|ASSETS_PATHS
    struct.pack_into('<I',data,attr+16,updated)
    original=text.read_text(encoding='utf-8')
    pattern=r'(<activity\b[^>]*android:name="com\.smartisanos\.launcher\.Launcher"[^>]*android:configChanges=")[^"]+("[^>]*>)'
    mirrored,count=re.subn(pattern,lambda m:m[1]+f'0x{updated:08X}'+m[2],original)
    if count!=1: raise ValueError('Expected one text HOME configChanges attribute')
    binary.write_bytes(data)
    text.write_text(mirrored,encoding='utf-8')
    print(f'HOME effective configChanges {old:#010x} -> {updated:#010x}; text mirror aligned')

if __name__=='__main__':main()
