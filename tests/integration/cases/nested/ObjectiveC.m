#import <Foundation/Foundation.h>
void _check(void) {
    id my_data = @{
    @"users": @[@{@"name": @"Bob", @"tags": @[@"admin", @"user"]}, @{@"name": @"Carol", @"tags": @[@"guest"]}],
};
    (void)my_data;
}
