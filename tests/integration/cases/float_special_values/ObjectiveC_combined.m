#import <Foundation/Foundation.h>
void _check(void) {
id my_data = @[
    @(INFINITY),
    @(-INFINITY),
    @(NAN),
];
my_data = @[
    @(INFINITY),
    @(-INFINITY),
    @(NAN),
];
    (void)my_data;
}
