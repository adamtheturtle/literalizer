#import <Foundation/Foundation.h>
void _check(void) {
id my_data = @[
    @{@"x": @(1), @"y": @(2.5)},
    @{@"x": @(3), @"y": @(4.0)},
];
my_data = @[
    @{@"x": @(1), @"y": @(2.5)},
    @{@"x": @(3), @"y": @(4.0)},
];
    (void)my_data;
}
