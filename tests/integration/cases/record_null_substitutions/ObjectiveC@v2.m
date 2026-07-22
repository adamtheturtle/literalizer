#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    @{@"missing": @(-1), @"present": @1},
    @{@"missing": @2, @"present": @3},
];
    (void)my_data;
}
    return 0;
}
