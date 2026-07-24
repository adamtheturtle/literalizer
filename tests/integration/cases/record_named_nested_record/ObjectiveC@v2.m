#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"project": @"alpha",
    @"lead_item": @{@"id": @100, @"label": @"first item", @"enabled": @NO, @"related_ids": @[@102, @103]},
};
    (void)my_data;
}
    return 0;
}
