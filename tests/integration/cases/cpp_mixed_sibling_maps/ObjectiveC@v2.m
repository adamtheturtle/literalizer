#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    @[@{@"a": @1}, @{@"a": [NSNull null]}, @42],
    @[@{@"a": @1}, @{@"a": @"s"}, @42],
    @[@{@"a": @1}, @{@"a": [NSNull null]}],
    @[@{@"a": @1}, @{@"a": @"s"}],
];
    (void)my_data;
}
    return 0;
}
