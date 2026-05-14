#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
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
    return 0;
}
