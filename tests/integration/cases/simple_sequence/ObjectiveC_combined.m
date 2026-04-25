#import <Foundation/Foundation.h>
void check_(void) {
id my_data = @[
    @1,
    @"hello",
    @YES,
    [NSNull null],
];
(void)my_data;
my_data = @[
    @1,
    @"hello",
    @YES,
    [NSNull null],
];
    (void)my_data;
}
