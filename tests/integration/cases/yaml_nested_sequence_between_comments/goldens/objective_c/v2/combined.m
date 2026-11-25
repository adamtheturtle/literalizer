#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    @[
        @{@"item": @"existing"},
        @"kept",
        // This comment trails the first pair.
    ],
    @[@{@"item": @"next"}, @"also kept"],
    // This comment describes the last pair.
    @[@{@"item": @"last"}, @"kept too"],
];
(void)my_data;
my_data = @[
    @[
        @{@"item": @"existing"},
        @"kept",
        // This comment trails the first pair.
    ],
    @[@{@"item": @"next"}, @"also kept"],
    // This comment describes the last pair.
    @[@{@"item": @"last"}, @"kept too"],
];
    (void)my_data;
}
    return 0;
}
