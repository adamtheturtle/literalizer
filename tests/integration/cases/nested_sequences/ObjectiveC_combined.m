#import <Foundation/Foundation.h>
static void check_(void) {
id my_data = @[
    @[@[@(1), @(2)], @[@(3), @(4)]],
    @[@[@(5)]],
];
my_data = @[
    @[@[@(1), @(2)], @[@(3), @(4)]],
    @[@[@(5)]],
];
    (void)my_data;
}
