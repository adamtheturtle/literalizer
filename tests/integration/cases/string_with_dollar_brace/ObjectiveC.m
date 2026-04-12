#import <Foundation/Foundation.h>
static void check_(void) {
id my_data = @[
    @"prefix ${HOME} suffix",
    @"${interpolated}",
];
    (void)my_data;
}
