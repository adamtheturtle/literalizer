#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    @{@"item": @"existing"},
    // This comment describes the next item.
    @{@"item": @"next"},
];
(void)my_data;
my_data = @[
    @{@"item": @"existing"},
    // This comment describes the next item.
    @{@"item": @"next"},
];
    (void)my_data;
}
    return 0;
}
