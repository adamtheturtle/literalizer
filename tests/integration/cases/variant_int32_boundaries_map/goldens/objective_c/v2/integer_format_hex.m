#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"below": @(-0x80000001),
    @"minimum": @(-0x80000000),
    @"above": @(-0x7fffffff),
    @"nested": @[@0x0],
};
    (void)my_data;
}
    return 0;
}
