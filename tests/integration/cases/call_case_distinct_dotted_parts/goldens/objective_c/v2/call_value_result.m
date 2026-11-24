#import <Foundation/Foundation.h>
static id kA_foo_Foo_bar_stub_(id _a0) { (void)_a0; return nil; }
struct FooType_ { id (*bar)(id); };
struct fooType_ { struct FooType_ Foo; };
struct kAType_ { struct fooType_ foo; };
static const struct kAType_ kA = { .foo = { .Foo = { .bar = kA_foo_Foo_bar_stub_ } } };
int main(void) {
@autoreleasepool {
id my_data = kA.foo.Foo.bar(@[@1]);
    (void)my_data;
}
    return 0;
}
