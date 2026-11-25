#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"omap_value": @{@"first": @1},
    @"sibling_lists": @{@"numbers": @[@1, @2], @"strings": @[@"x", @"y"]},
    @"ref_marker_present": @[@"$keep", @"z"],
};
(void)my_data;
my_data = @{
    @"omap_value": @{@"first": @1},
    @"sibling_lists": @{@"numbers": @[@1, @2], @"strings": @[@"x", @"y"]},
    @"ref_marker_present": @[@"$keep", @"z"],
};
    (void)my_data;
}
    return 0;
}
