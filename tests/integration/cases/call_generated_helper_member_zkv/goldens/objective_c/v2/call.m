#import <Foundation/Foundation.h>
static void kObj_ZKV_stub_(id _a0) { (void)_a0; }
struct kObjType_ { void (*ZKV)(id); };
static const struct kObjType_ kObj = { .ZKV = kObj_ZKV_stub_ };
int main(void) {
@autoreleasepool {
kObj.ZKV(@1);
}
    return 0;
}
