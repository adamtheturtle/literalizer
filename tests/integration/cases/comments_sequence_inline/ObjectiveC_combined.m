#import <Foundation/Foundation.h>
void check_(void) {
id my_data = @[
    @"a",  // note a
    @"b",  // note b
];
my_data = @[
    @"a",  // note a
    @"b",  // note b
];
    (void)my_data;
}
