#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    [NSSet setWithArray:@[@"a", @"b"]],
];
(void)my_data;
my_data = @[
    [NSSet setWithArray:@[@"a", @"b"]],
];
    (void)my_data;
}
    return 0;
}
