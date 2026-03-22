#import <Foundation/Foundation.h>
void _check(void) {
    id _v = @[
    @(42),
    @(3.14),
    @YES,
    @NO,
    @"hello \"world\"",
];
    (void)_v;
}
