#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id shared = @[
    @1,
    @2,
];
id my_data = @[
    shared,
    shared,
];
    (void)my_data;
}
    return 0;
}
