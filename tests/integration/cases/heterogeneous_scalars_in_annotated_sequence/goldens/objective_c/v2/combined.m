#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    @YES,
    @1.5,
    [NSNull null],
    [NSDate dateWithTimeIntervalSince1970:1577836800],
    [NSDate dateWithTimeIntervalSince1970:1577836800],
    @[],
];
(void)my_data;
my_data = @[
    @YES,
    @1.5,
    [NSNull null],
    [NSDate dateWithTimeIntervalSince1970:1577836800],
    [NSDate dateWithTimeIntervalSince1970:1577836800],
    @[],
];
    (void)my_data;
}
    return 0;
}
