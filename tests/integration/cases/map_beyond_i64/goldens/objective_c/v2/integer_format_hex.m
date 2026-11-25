#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"a": @0x7fffffffffffffff,
    @"b": @9223372036854775808ULL,
};
    (void)my_data;
}
    return 0;
}
