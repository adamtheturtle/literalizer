#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"minimum": @(-2147483648),
    @"neighbor": @(-2147483647),
    @"maximum": @2147483647,
    @"nested": @[@(-2147483648)],
};
    (void)my_data;
}
    return 0;
}
