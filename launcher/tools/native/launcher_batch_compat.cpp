#include <jni.h>
#include <dlfcn.h>
#include <cstdint>
#include <cstring>
#include <new>

namespace {
constexpr size_t kOriginalSize = 0x818;
constexpr size_t kBatchSize = 0x2040;
using Constructor = void (*)(void*);

Constructor originalConstructor() {
    // The engine remains loaded for the process lifetime, just like System.loadLibrary.
    static const Constructor constructor = [] {
        void* library = dlopen("liblauncher_opt.so", RTLD_NOW | RTLD_NOLOAD);
        return library ? reinterpret_cast<Constructor>(
                dlsym(library, "_ZN24SceneNodeTransformNativeC1Ev")) : nullptr;
    }();
    return constructor;
}
}

// Shared by JNI and the real-library bounds/ownership probe. The original engine
// finalizer calls its original destructor and operator delete on this same pointer.
extern "C" __attribute__((visibility("default")))
void* SmartisanAllocateSceneNode(bool batchOwner) {
    Constructor constructor = originalConstructor();
    if (!constructor) return nullptr;
    void* node = ::operator new(batchOwner ? kBatchSize : kOriginalSize, std::nothrow);
    if (!node) return nullptr;
    if (batchOwner) {
        std::memset(static_cast<unsigned char*>(node) + kOriginalSize, 0,
                    kBatchSize - kOriginalSize);
    }
    constructor(node);
    return node;
}

extern "C" JNIEXPORT jlong JNICALL
Java_com_smartisanos_launcher_compat_NativeBatchAllocation_00024Arm64_allocate(
        JNIEnv* env, jclass, jboolean batchOwner) {
    if (!originalConstructor()) {
        env->ThrowNew(env->FindClass("java/lang/UnsatisfiedLinkError"),
                      "Original Smartisan node constructor unavailable");
        return 0;
    }
    void* node = SmartisanAllocateSceneNode(batchOwner);
    if (!node) {
        env->ThrowNew(env->FindClass("java/lang/OutOfMemoryError"),
                      "Smartisan native node allocation failed");
    }
    return reinterpret_cast<jlong>(node);
}
