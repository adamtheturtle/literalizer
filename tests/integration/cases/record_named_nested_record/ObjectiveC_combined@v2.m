#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"collection": @"alpha",
    @"featured_entry": @{@"id": @100, @"label": @"first entry", @"enabled": @NO, @"related_ids": @[@102, @103]},
};
(void)my_data;
my_data = @{
    @"collection": @"alpha",
    @"featured_entry": @{@"id": @100, @"label": @"first entry", @"enabled": @NO, @"related_ids": @[@102, @103]},
};
    (void)my_data;
}
    return 0;
}
