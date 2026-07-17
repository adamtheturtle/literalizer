#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    @9223372036854775807,
    @9223372036854775808ULL,
];
(void)my_data;
my_data = @[
    @9223372036854775807,
    @9223372036854775808ULL,
];
    (void)my_data;
}
    return 0;
}
