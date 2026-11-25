#import <Foundation/Foundation.h>
static void kObj_BEGIN_stub_(id _a0) { (void)_a0; }
struct kObjType_ { void (*BEGIN)(id); };
static const struct kObjType_ kObj = { .BEGIN = kObj_BEGIN_stub_ };
int main(void) {
@autoreleasepool {
kObj.BEGIN(@42);
}
    return 0;
}
