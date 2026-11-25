#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"minimum": @(-0x80000000),
    @"neighbor": @(-0x7fffffff),
    @"maximum": @0x7fffffff,
    @"nested": @[@(-0x80000000)],
};
    (void)my_data;
}
    return 0;
}
