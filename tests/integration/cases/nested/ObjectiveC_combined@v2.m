#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"users": @[@{@"name": @"Bob", @"tags": @[@"admin", @"user"]}, @{@"name": @"Carol", @"tags": @[@"guest"]}],
};
(void)my_data;
my_data = @{
    @"users": @[@{@"name": @"Bob", @"tags": @[@"admin", @"user"]}, @{@"name": @"Carol", @"tags": @[@"guest"]}],
};
    (void)my_data;
}
    return 0;
}
