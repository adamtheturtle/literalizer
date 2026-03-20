#import <Foundation/Foundation.h>
void _check(void) {
    id _v = @[
    @YES,
    @"hi",
    @[@(1), @(2)],
    [NSNull null],
];
    (void)_v;
}
