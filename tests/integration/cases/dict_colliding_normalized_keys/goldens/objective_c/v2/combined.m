#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"user_name": @1,
    @"user.name": @2,
    @"user-name": @3,
    @"field_name_that_is_really_quite_long_one": @4,
    @"field_name_that_is_really_quite_long_two": @5,
};
(void)my_data;
my_data = @{
    @"user_name": @1,
    @"user.name": @2,
    @"user-name": @3,
    @"field_name_that_is_really_quite_long_one": @4,
    @"field_name_that_is_really_quite_long_two": @5,
};
    (void)my_data;
}
    return 0;
}
