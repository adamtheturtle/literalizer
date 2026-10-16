#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id item = @[
    @1,
    @2,
];
id my_data = @[
    @1,
    @2,
];
(void)my_data;
my_data = item;
(void)my_data;
}
    return 0;
}
