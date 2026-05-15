#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"project": @"alpha",
    @"lead_task": @{@"id": @100, @"description": @"first task", @"is_done": @NO, @"blocks": @[@102, @103]},
};
(void)my_data;
my_data = @{
    @"project": @"alpha",
    @"lead_task": @{@"id": @100, @"description": @"first task", @"is_done": @NO, @"blocks": @[@102, @103]},
};
    (void)my_data;
}
    return 0;
}
