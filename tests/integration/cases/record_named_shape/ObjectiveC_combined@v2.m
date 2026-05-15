#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    @{@"id": @100, @"description": @"first task", @"is_done": @NO, @"blocks": @[@102, @103]},
    @{@"id": @101, @"description": @"second task", @"is_done": @YES, @"blocks": @[]},
];
(void)my_data;
my_data = @[
    @{@"id": @100, @"description": @"first task", @"is_done": @NO, @"blocks": @[@102, @103]},
    @{@"id": @101, @"description": @"second task", @"is_done": @YES, @"blocks": @[]},
];
    (void)my_data;
}
    return 0;
}
