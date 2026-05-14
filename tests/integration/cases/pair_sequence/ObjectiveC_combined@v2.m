#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    @1,
    @"hello",
];
(void)my_data;
my_data = @[
    @1,
    @"hello",
];
    (void)my_data;
}
    return 0;
}
