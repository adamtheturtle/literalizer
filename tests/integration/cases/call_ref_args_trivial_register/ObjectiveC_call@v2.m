#import <Foundation/Foundation.h>
static void process(id _a0, id _a1) { (void)_a0; (void)_a1; }
int main(void) {
@autoreleasepool {
id my_int = @1;
id my_bool = @YES;
id my_float = @3.14;
id my_list = @[
    @1,
    @2,
    @3,
];
process(my_int, @42);
process(my_bool, @7);
process(my_float, @9);
process(my_list, @1);
}
    return 0;
}
