#import <Foundation/Foundation.h>
void check_(void) {
id my_data = @[
    @[@(1), @"a"],
    @[@(2), @"b"],
];
(void)my_data;
my_data = @[
    @[@(1), @"a"],
    @[@(2), @"b"],
];
    (void)my_data;
}
