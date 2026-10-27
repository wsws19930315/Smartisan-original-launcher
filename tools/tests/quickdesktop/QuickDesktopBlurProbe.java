package com.smartisanos.launcher.quickdesktop;

import android.graphics.Bitmap;
import android.os.Looper;
import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.Random;

/** Native pixel equivalence against the pre-change kernel, including clamped boundaries. */
public final class QuickDesktopBlurProbe {
    private static int checks;
    private static Method current, reference;
    private static void check(boolean ok, String why) {
        if (!ok) throw new AssertionError(why);
        checks++;
    }
    private static Bitmap source(int w, int h) {
        int[] pixels = new int[w*h];
        Random random = new Random(7291L + w * 17L + h);
        for (int i=0; i<pixels.length; i++) pixels[i] = random.nextInt();
        Bitmap b = Bitmap.createBitmap(w,h,Bitmap.Config.ARGB_8888);
        b.setPixels(pixels,0,w,0,0,w,h);
        return b;
    }
    private static void compare(int w, int h, int radius, int passes) throws Exception {
        Bitmap input=source(w,h), old=input.copy(Bitmap.Config.ARGB_8888,true);
        reference.invoke(null,old,radius,passes); current.invoke(null,input,radius,passes);
        int[] expected=new int[w*h],actual=new int[w*h];
        old.getPixels(expected,0,w,0,0,w,h);input.getPixels(actual,0,w,0,0,w,h);
        check(Arrays.equals(expected,actual), "pixels differ " + w+"x"+h+" radius="+radius+" passes="+passes);
        old.recycle(); input.recycle();
    }
    public static void main(String[] args) {
        try {
            if (Looper.myLooper()==null) Looper.prepareMainLooper();
            current=QuickDesktopBackgroundCapture.class.getDeclaredMethod("blur",Bitmap.class,int.class,int.class);
            reference=ReferenceBlur.class.getDeclaredMethod("blur",Bitmap.class,int.class,int.class);
            current.setAccessible(true);reference.setAccessible(true);
            for (int[] size:new int[][]{{1,1},{1,37},{41,1},{3,7},{13,17},{240,533}})
                for (int radius:new int[]{0,1,14,31})
                    for (int passes:new int[]{0,1,2}) compare(size[0],size[1],radius,passes);
            for (int color:new int[]{0,0xffffffff,0xff000000,0x80ff00ff}) {
                Bitmap input=Bitmap.createBitmap(7,9,Bitmap.Config.ARGB_8888);input.eraseColor(color);
                Bitmap old=input.copy(Bitmap.Config.ARGB_8888,true);
                reference.invoke(null,old,14,2);current.invoke(null,input,14,2);
                int[] a=new int[63],b=new int[63];
                old.getPixels(a,0,7,0,0,7,9);input.getPixels(b,0,7,0,0,7,9);
                check(Arrays.equals(a,b),"constant/alpha channel boundary differs");
                input.recycle();old.recycle();
            }
            Bitmap work=source(240,533);
            ReferenceBlurWork.divisionCalls=0;ReferenceBlurWork.blur(work,14,2);
            CurrentBlurWork.divisionCalls=0;CurrentBlurWork.blur(work,14,2);
            check(CurrentBlurWork.divisionCalls<ReferenceBlurWork.divisionCalls,
                    "repeated channel division was not reduced");
            System.out.println("DIVISION_CALLS old="+ReferenceBlurWork.divisionCalls+" new="+CurrentBlurWork.divisionCalls);
            work.recycle();
            for(int i=0;i<5;i++) {
                Bitmap a=source(240,533),b=a.copy(Bitmap.Config.ARGB_8888,true);
                long oldNs,newNs,start;
                if(i%2==0) {
                    start=System.nanoTime();reference.invoke(null,a,14,2);oldNs=System.nanoTime()-start;
                    start=System.nanoTime();current.invoke(null,b,14,2);newNs=System.nanoTime()-start;
                } else {
                    start=System.nanoTime();current.invoke(null,b,14,2);newNs=System.nanoTime()-start;
                    start=System.nanoTime();reference.invoke(null,a,14,2);oldNs=System.nanoTime()-start;
                }
                System.out.println("KERNEL_PAIR n="+i+" oldMs="+oldNs/1e6+" newMs="+newNs/1e6);
                a.recycle();b.recycle();
            }
            System.out.println("PASS BLUR_KERNEL checks="+checks);System.exit(0);
        } catch(Throwable error) {error.printStackTrace();System.exit(1);}
    }
}
