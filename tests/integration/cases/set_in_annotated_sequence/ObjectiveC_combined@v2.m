#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    [NSSet set],
    [NSSet setWithArray:@[@1, @2]],
    @[],
];
(void)my_data;
my_data = @[
    [NSSet set],
    [NSSet setWithArray:@[@1, @2]],
    @[],
];
    (void)my_data;
}
    return 0;
}
