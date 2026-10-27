"""Exercise the production allocation bridge's old-API and 32-bit lazy-loading boundary."""
import argparse
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]


def main():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('--jdk', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    sources = {
        'android/os/Build.java': 'package android.os; public class Build {public static class VERSION {public static int SDK_INT;}}',
        'android/os/Process.java': 'package android.os; public class Process {public static boolean bit64;public static int calls;public static boolean is64Bit(){calls++;return bit64;}}',
        'AllocationApiProbe.java': '''import android.os.Build;
import com.smartisanos.launcher.compat.NativeBatchAllocation;
public class AllocationApiProbe {
 public static void main(String[] args){int checks=0;
  int api=Integer.parseInt(args[0]);
   Build.VERSION.SDK_INT=api;android.os.Process.bit64=false;android.os.Process.calls=0;
   for(boolean batch:new boolean[]{false,true}){
    if(NativeBatchAllocation.create(batch)!=0)throw new AssertionError("32-bit native allocation changed");checks++;
   }
   if(android.os.Process.calls!=(api<23?0:1))throw new AssertionError("process bitness must be resolved once on supported APIs");checks++;
  System.out.println("PASS ALLOCATION_API_BOUNDARY="+checks);
 }
}''',
    }
    files = []
    for name, text in sources.items():
        path = args.output / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        files.append(path)
    files.append(ROOT / 'launcher/tools/java/com/smartisanos/launcher/compat/NativeBatchAllocation.java')
    subprocess.run([str(args.jdk / 'bin/javac.exe'), '-encoding', 'UTF-8', '-d', str(args.output),
                    *map(str, files)], check=True)
    for api in [19, 22, 23, 28, 36]:
        subprocess.run([str(args.jdk / 'bin/java.exe'), '-cp', str(args.output), 'AllocationApiProbe', str(api)], check=True)


if __name__ == '__main__':
    main()
