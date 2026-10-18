#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"below": @(-2147483649),
    @"minimum": @(-2147483648),
    @"above": @(-2147483647),
    @"nested": @[@0],
};
    (void)my_data;
}
    return 0;
}
