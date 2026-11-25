#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    @{@"id": @100, @"label": @"first entry", @"enabled": @NO, @"related_ids": @[@102, @103]},
    @{@"id": @101, @"label": @"second entry", @"enabled": @YES, @"related_ids": @[@100]},
];
    (void)my_data;
}
    return 0;
}
