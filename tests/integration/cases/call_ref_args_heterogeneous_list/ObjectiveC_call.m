#import <Foundation/Foundation.h>
static void process(id _a0, id _a1) { (void)_a0; (void)_a1; }
int main(void) {
@autoreleasepool {
id my_ints = @[
    @1,
    @2,
    @3,
];
id my_strings = @[
    @"a",
    @"b",
];
id my_empty = @[];
process(my_ints, @42);
process(my_strings, @7);
process(my_empty, @99);
}
    return 0;
}
