#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    @{@"id": @1, @"label": @"first", @"tags": @[]},
    @{@"id": @2, @"label": @"second", @"tags": @[]},
    @{@"id": @3, @"label": @"third", @"tags": @[]},
];
(void)my_data;
my_data = @[
    @{@"id": @1, @"label": @"first", @"tags": @[]},
    @{@"id": @2, @"label": @"second", @"tags": @[]},
    @{@"id": @3, @"label": @"third", @"tags": @[]},
];
    (void)my_data;
}
    return 0;
}
