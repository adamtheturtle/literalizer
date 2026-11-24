#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    @(-9223372036854775807LL - 1),
    @(-0x1),
    @0x7fffffffffffffff,
];
    (void)my_data;
}
    return 0;
}
