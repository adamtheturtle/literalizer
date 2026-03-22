#import <Foundation/Foundation.h>
void _check(void) {
    id _v = @{
    @"users": @[@{@"name": @"Bob", @"tags": @[@"admin", @"user"]}, @{@"name": @"Carol", @"tags": @[@"guest"]}],
};
    (void)_v;
}
