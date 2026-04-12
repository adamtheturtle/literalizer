#import <Foundation/Foundation.h>
static void check_(void) {
id my_data = @[
    @YES,
    @"hi",
    @[@(1), @(2)],
    [NSNull null],
];
my_data = @[
    @YES,
    @"hi",
    @[@(1), @(2)],
    [NSNull null],
];
    (void)my_data;
}
