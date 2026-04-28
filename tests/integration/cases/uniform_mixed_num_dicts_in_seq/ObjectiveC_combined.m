#import <Foundation/Foundation.h>
int main(void) {
id my_data = @[
    @{@"x": @1, @"y": @2.5},
    @{@"x": @3, @"y": @4.0},
];
(void)my_data;
my_data = @[
    @{@"x": @1, @"y": @2.5},
    @{@"x": @3, @"y": @4.0},
];
    (void)my_data;
    return 0;
}
