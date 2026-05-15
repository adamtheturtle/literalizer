#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"items": @[@{@"id": @1}, @{@"id": @2, @"count": @10}, @{@"id": @3, @"count": @20}],
};
(void)my_data;
my_data = @{
    @"items": @[@{@"id": @1}, @{@"id": @2, @"count": @10}, @{@"id": @3, @"count": @20}],
};
    (void)my_data;
}
    return 0;
}
