#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    @[@{@"name": @"Alice"}, @{@"name": @"Bob"}],
    @[@{@"name": @"Charlie"}, @{@"name": @"Dave"}],
];
(void)my_data;
my_data = @[
    @[@{@"name": @"Alice"}, @{@"name": @"Bob"}],
    @[@{@"name": @"Charlie"}, @{@"name": @"Dave"}],
];
    (void)my_data;
}
    return 0;
}
