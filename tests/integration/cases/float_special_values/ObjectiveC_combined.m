#import <Foundation/Foundation.h>
void check_(void) {
id my_data = @[
    @(INFINITY),
    @(-INFINITY),
    @(NAN),
];
(void)my_data;
my_data = @[
    @(INFINITY),
    @(-INFINITY),
    @(NAN),
];
    (void)my_data;
}
