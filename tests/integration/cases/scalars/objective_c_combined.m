#import <Foundation/Foundation.h>
void _check(void) {
id my_data = @[
    @(42),
    @(3.14),
    @YES,
    @NO,
    @"hello \"world\"",
];
my_data = @[
    @(42),
    @(3.14),
    @YES,
    @NO,
    @"hello \"world\"",
];
    (void)my_data;
}
