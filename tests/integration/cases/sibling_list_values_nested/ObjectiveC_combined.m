#import <Foundation/Foundation.h>
void check_(void) {
id my_data = @{
    @"lint": @[@(2), @[]],
    @"test": @[@(5), @[@"compile"]],
};
(void)my_data;
my_data = @{
    @"lint": @[@(2), @[]],
    @"test": @[@(5), @[@"compile"]],
};
    (void)my_data;
}
