#include <dlfcn.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <initializer_list>
#include <malloc.h>
int main(int argc,char**argv){
 if(argc<3)return 1;
 size_t size=argc>2?strtoul(argv[2],nullptr,0):0x818;
 void* lib=dlopen(argv[1],RTLD_NOW);if(!lib){puts(dlerror());return 2;}
 auto make=(int64_t(*)(void*,void*))dlsym(lib,"_Z19native_CreateNativeP7_JNIEnvP7_jclass");
 auto release=(void(*)(void*,void*,int64_t))dlsym(lib,"_Z20native_ReleaseNativeP7_JNIEnvP7_jclassx");
 auto light=(void(*)(void*,void*,int64_t,int64_t,int,float,float,float))dlsym(lib,"_Z43native_CalculateModelSpaceLightDirArrayDataP7_JNIEnvP7_jclassxxifff");
 if(!make||!release||!light)return 3;
 void* (*allocator)(bool)=nullptr;
 if(argc>3){void* bridge=dlopen(argv[3],RTLD_NOW);if(!bridge){puts(dlerror());return 6;}
  allocator=(void*(*)(bool))dlsym(bridge,"SmartisanAllocateSceneNode");if(!allocator)return 7;}
 auto create=[&](){return allocator?(int64_t)allocator(true):make(nullptr,nullptr);};
 auto original=create();auto source=create();if(!original||!source)return 8;
 if(allocator){auto normal=(int64_t)allocator(false);auto reference=make(nullptr,nullptr);
  if(!normal||!reference||malloc_usable_size((void*)normal)!=malloc_usable_size((void*)reference))return 9;
  release(nullptr,nullptr,reference);release(nullptr,nullptr,normal);puts("PASS ORDINARY_NODE_ORIGINAL_SIZE");}
 auto cameraCreate=(int64_t(*)(void*,void*,int,int))dlsym(lib,"Java_com_smartisanos_smengine_Camera_nCreate");
 auto cameraRelease=(void(*)(void*,void*,int64_t))dlsym(lib,"Java_com_smartisanos_smengine_Camera_nRelease");
 auto matrix=(void(*)(void*,void*,const float*,int,int))dlsym(lib,"_ZN24SceneNodeTransformNative23calculateMVPMatrixArrayEP6CameraRK8Matrix4fii");
 if(!cameraCreate||!cameraRelease||!matrix)return 3;
 if(size==0x2040){
  auto* bytes=(unsigned char*)original;
  for(size_t n=0x818;n<0x818+81*12;n++)if(bytes[n])return 4;
  for(size_t n=0xc00;n<0xc00+81*64;n++)if(bytes[n])return 5;
  puts("PASS ARRAY_ZERO_INITIALIZATION");
 }
 auto camera=cameraCreate(nullptr,nullptr,1260,2800);
 float identity[16]={1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1};
 for(int index=0;index<=80;index++){
  auto* guarded=(unsigned char*)malloc(0x4000);memset(guarded,0xa5,0x4000);memcpy(guarded,(void*)original,size);
  light(nullptr,nullptr,(int64_t)guarded,source,index,0.2f,0.4f,1.0f);
  int outside=0;size_t first=0;
  for(size_t n=size;n<0x4000;n++)if(guarded[n]!=0xa5){if(!outside)first=n;outside++;}
  printf("index=%d outside_object_changed_bytes=%d first_offset=0x%zx\n",index,outside,first);free(guarded);
  guarded=(unsigned char*)malloc(0x4000);memset(guarded,0xa5,0x4000);
  matrix(guarded,(void*)camera,identity,index,-1);
  int prefix=0,matrixOutside=0;
  for(size_t n=0;n<0x818;n++)if(guarded[n]!=0xa5)prefix++;
  for(size_t n=size;n<0x4000;n++)if(guarded[n]!=0xa5)matrixOutside++;
  printf("matrix_index=%d legacy_fields_changed=%d outside=%d\n",index,prefix,matrixOutside);free(guarded);
 }
 for(int i=0;i<10000;i++){auto node=create();release(nullptr,nullptr,node);
  if(allocator){node=(int64_t)allocator(false);release(nullptr,nullptr,node);}}
 puts("PASS CREATE_RELEASE_CYCLES=10000");
 cameraRelease(nullptr,nullptr,camera);release(nullptr,nullptr,source);release(nullptr,nullptr,original);return 0;
}
