#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    @{@"replacement": [NSNull null], @"present": @1},
    @{@"replacement": @2, @"present": @3},
];
(void)my_data;
my_data = @[
    @{@"replacement": [NSNull null], @"present": @1},
    @{@"replacement": @2, @"present": @3},
];
    (void)my_data;
}
    return 0;
}
