#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"a": @1,
    @"b": @2.5,
    @"c": @3,
};
(void)my_data;
my_data = @{
    @"a": @1,
    @"b": @2.5,
    @"c": @3,
};
    (void)my_data;
}
    return 0;
}
