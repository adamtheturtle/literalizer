#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"quantity": @1000000,
    @"big": @18446744073709551615ULL,
    @"ratio": @2.5,
    @"label": @"tag",
    @"ok": @YES,
};
(void)my_data;
my_data = @{
    @"quantity": @1000000,
    @"big": @18446744073709551615ULL,
    @"ratio": @2.5,
    @"label": @"tag",
    @"ok": @YES,
};
    (void)my_data;
}
    return 0;
}
