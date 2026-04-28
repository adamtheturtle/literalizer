#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"a": @1,
    @"b": @"x",
};
(void)my_data;
my_data = @{
    @"a": @1,
    @"b": @"x",
};
    (void)my_data;
}
    return 0;
}
