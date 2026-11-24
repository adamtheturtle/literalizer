#import <Foundation/Foundation.h>
static void kFoo_class_stub_(id _a0) { (void)_a0; }
struct kFooType_ { void (*class)(id); };
static const struct kFooType_ kFoo = { .class = kFoo_class_stub_ };
int main(void) {
@autoreleasepool {
kFoo.class(@1);
}
    return 0;
}
