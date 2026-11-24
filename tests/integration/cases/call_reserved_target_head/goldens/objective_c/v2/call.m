#import <Foundation/Foundation.h>
static void kClass_member_stub_(id _a0) { (void)_a0; }
struct kClassType_ { void (*member)(id); };
static const struct kClassType_ kClass = { .member = kClass_member_stub_ };
int main(void) {
@autoreleasepool {
kClass.member(@42);
}
    return 0;
}
