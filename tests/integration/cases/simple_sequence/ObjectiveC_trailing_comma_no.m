#import <Foundation/Foundation.h>
void _check(void) {
id my_data = @[
    @(1),
    @"hello",
    @YES,
    [NSNull null]
];
    (void)my_data;
}
