#import <Foundation/Foundation.h>
void _check(void) {
id my_data = @{
    @"name": @"Alice",
    @"tags": [NSSet setWithArray:@[@YES, @(42), @"apple"]],
};
    (void)my_data;
}
