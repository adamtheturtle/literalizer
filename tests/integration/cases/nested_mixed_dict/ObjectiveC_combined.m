#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"outer": @{@"a": @1, @"b": @"x", @"c": [NSNull null]},
};
(void)my_data;
my_data = @{
    @"outer": @{@"a": @1, @"b": @"x", @"c": [NSNull null]},
};
    (void)my_data;
}
    return 0;
}
