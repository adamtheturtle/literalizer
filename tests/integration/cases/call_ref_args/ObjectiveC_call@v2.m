#import <Foundation/Foundation.h>
static void process(id _a0, id _a1) { (void)_a0; (void)_a1; }
int main(void) {
@autoreleasepool {
id my_var = @[
    @1,
    @2,
    @3,
];
id my_other = @[
    @4,
    @5,
    @6,
];
process(my_var, @42);
process(my_other, @7);
}
    return 0;
}
