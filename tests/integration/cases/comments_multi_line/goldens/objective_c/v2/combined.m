#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    // line 1
    // line 2
    @"a",
];
(void)my_data;
my_data = @[
    // line 1
    // line 2
    @"a",
];
    (void)my_data;
}
    return 0;
}
