#import <Foundation/Foundation.h>
static void kFoo_Foo_bar_stub_(id _a0) { (void)_a0; }
struct FooType_ { void (*bar)(id); };
struct kFooType_ { struct FooType_ Foo; };
static const struct kFooType_ kFoo = { .Foo = { .bar = kFoo_Foo_bar_stub_ } };
int main(void) {
@autoreleasepool {
kFoo.Foo.bar(@[@1]);
}
    return 0;
}
