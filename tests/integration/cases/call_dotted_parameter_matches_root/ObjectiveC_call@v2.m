#import <Foundation/Foundation.h>
static void kOuter_inner_stub_(id _a0, id _a1) { (void)_a0, (void)_a1; }
struct kOuterType_ { void (*inner)(id, id); };
static const struct kOuterType_ kOuter = { .inner = kOuter_inner_stub_ };
int main(void) {
@autoreleasepool {
kOuter.inner(@1, @2);
}
    return 0;
}
