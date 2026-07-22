#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    @{@"missing": [NSNull null], @"present": @1},
    @{@"missing": @2, @"present": @3},
];
(void)my_data;
my_data = @[
    @{@"missing": [NSNull null], @"present": @1},
    @{@"missing": @2, @"present": @3},
];
    (void)my_data;
}
    return 0;
}
