#import <Foundation/Foundation.h>
void check_(void) {
id my_data = @[
    @"prefix ${HOME} suffix",
    @"${interpolated}",
];
    (void)my_data;
}
