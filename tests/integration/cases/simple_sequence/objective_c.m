#import <Foundation/Foundation.h>
void _check(void) {
    id _v = @[
    @(1),
    @"hello",
    @YES,
    [NSNull null],
];
    (void)_v;
}
