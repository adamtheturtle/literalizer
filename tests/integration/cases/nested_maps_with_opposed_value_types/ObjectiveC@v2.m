#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    @{@"input": @{@"name": @"alice", @"city": @"paris"}, @"expected": @{@"count": @1, @"total": @2}},
    @{@"input": @{@"name": @10, @"city": @20}, @"expected": @{@"count": @"done", @"total": @"pending"}},
];
    (void)my_data;
}
    return 0;
}
