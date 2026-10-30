#import <Foundation/Foundation.h>
static void kA_foo_Foo_bar_stub_(id _a0) { (void)_a0; }
struct FooType_ { void (*bar)(id); };
struct fooType_ { struct FooType_ Foo; };
struct kAType_ { struct fooType_ foo; };
static const struct kAType_ kA = { .foo = { .Foo = { .bar = kA_foo_Foo_bar_stub_ } } };
int main(void) {
@autoreleasepool {
kA.foo.Foo.bar(@[@1]);
}
    return 0;
}
