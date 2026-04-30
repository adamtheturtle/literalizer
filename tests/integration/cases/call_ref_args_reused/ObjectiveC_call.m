#import <Foundation/Foundation.h>
static void process(id _a0, id _a1) { (void)_a0; (void)_a1; }
int main(void) {
@autoreleasepool {
id repeated_var = @1;
id single_var = @[
    @4,
    @5,
    @6,
];
process(repeated_var, @1);
process(single_var, @0);
process(repeated_var, @8);
}
    return 0;
}
