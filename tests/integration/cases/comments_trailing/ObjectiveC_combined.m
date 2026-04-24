#import <Foundation/Foundation.h>
void check_(void) {
id my_data = @[
    @"a",
    // trailing
];
(void)my_data;
my_data = @[
    @"a",
    // trailing
];
    (void)my_data;
}
