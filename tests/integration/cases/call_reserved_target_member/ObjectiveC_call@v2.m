#import <Foundation/Foundation.h>
static void kObj_class_stub_(id _a0) { (void)_a0; }
struct kObjType_ { void (*class)(id); };
static const struct kObjType_ kObj = { .class = kObj_class_stub_ };
int main(void) {
@autoreleasepool {
kObj.class(@42);
}
    return 0;
}
