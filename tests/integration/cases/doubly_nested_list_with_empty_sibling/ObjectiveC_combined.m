#import <Foundation/Foundation.h>
void check_(void) {
id my_data = @[
    @[@[@1, @2]],
    @[],
    @[@[@3, @4]],
];
(void)my_data;
my_data = @[
    @[@[@1, @2]],
    @[],
    @[@[@3, @4]],
];
    (void)my_data;
}
