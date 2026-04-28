#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"a": @1,
    @"b": @3000000000,
    @"c": @"x",
};
(void)my_data;
my_data = @{
    @"a": @1,
    @"b": @3000000000,
    @"c": @"x",
};
    (void)my_data;
}
    return 0;
}
