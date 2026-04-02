#import <Foundation/Foundation.h>
void _check(void) {
id my_data = @[
    @"prefix ${HOME} suffix",
    @"${interpolated}",
];
my_data = @[
    @"prefix ${HOME} suffix",
    @"${interpolated}",
];
    (void)my_data;
}
