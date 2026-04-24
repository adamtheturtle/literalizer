#import <Foundation/Foundation.h>
void check_(void) {
id my_data = [NSSet setWithArray:@[
    @YES,
    @(42),
    @"apple",
]];
(void)my_data;
my_data = [NSSet setWithArray:@[
    @YES,
    @(42),
    @"apple",
]];
    (void)my_data;
}
