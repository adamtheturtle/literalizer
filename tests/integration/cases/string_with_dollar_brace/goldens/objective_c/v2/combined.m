#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    @"prefix ${HOME} suffix",
    @"${interpolated}",
];
(void)my_data;
my_data = @[
    @"prefix ${HOME} suffix",
    @"${interpolated}",
];
    (void)my_data;
}
    return 0;
}
