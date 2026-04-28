#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
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
    return 0;
}
