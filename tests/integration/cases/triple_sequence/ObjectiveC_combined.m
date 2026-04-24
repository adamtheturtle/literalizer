#import <Foundation/Foundation.h>
void check_(void) {
id my_data = @[
    @(1),
    @"hello",
    @YES,
];
(void)my_data;
my_data = @[
    @(1),
    @"hello",
    @YES,
];
    (void)my_data;
}
