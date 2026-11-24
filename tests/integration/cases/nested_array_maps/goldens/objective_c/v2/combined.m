#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"groups": @[@[@{@"id": @1}], @[@{@"id": @2}]],
};
(void)my_data;
my_data = @{
    @"groups": @[@[@{@"id": @1}], @[@{@"id": @2}]],
};
    (void)my_data;
}
    return 0;
}
