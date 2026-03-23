#import <Foundation/Foundation.h>
void _check(void) {
id my_data = [NSSet setWithArray:@[
    @YES,
    @(42),
    @"apple",
]];
my_data = [NSSet setWithArray:@[
    @YES,
    @(42),
    @"apple",
]];
    (void)my_data;
}
