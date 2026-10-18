#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"i32_below": @(-0x80000001),
    @"i32_minimum": @(-0x80000000),
    @"i32_above": @(-0x7fffffff),
    @"i32_maximum": @0x7fffffff,
    @"i32_over": @0x80000000,
    @"i64_minimum": @(-9223372036854775807LL - 1),
    @"i64_maximum": @0x7fffffffffffffff,
};
    (void)my_data;
}
    return 0;
}
