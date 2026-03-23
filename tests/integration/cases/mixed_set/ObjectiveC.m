#import <Foundation/Foundation.h>
void _check(void) {
    id _v = [NSSet setWithArray:@[
    @YES,
    @(42),
    @"apple",
]];
    (void)_v;
}
