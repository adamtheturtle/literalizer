#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    @{@"$ref": @"ref_x"},
    @1,
    @2,
];
(void)my_data;
my_data = @[
    @{@"$ref": @"ref_x"},
    @1,
    @2,
];
    (void)my_data;
}
    return 0;
}
