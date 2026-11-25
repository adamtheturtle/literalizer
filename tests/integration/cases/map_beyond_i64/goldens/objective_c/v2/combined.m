#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"a": @9223372036854775807,
    @"b": @9223372036854775808ULL,
};
(void)my_data;
my_data = @{
    @"a": @9223372036854775807,
    @"b": @9223372036854775808ULL,
};
    (void)my_data;
}
    return 0;
}
