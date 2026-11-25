#import <Foundation/Foundation.h>
static void kObj_ZVal_stub_(id _a0) { (void)_a0; }
struct kObjType_ { void (*ZVal)(id); };
static const struct kObjType_ kObj = { .ZVal = kObj_ZVal_stub_ };
int main(void) {
@autoreleasepool {
kObj.ZVal(@1);
}
    return 0;
}
