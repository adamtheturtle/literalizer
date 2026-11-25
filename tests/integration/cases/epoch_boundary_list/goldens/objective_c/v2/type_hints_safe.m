#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    [NSDate dateWithTimeIntervalSince1970:-2147483649],
    [NSDate dateWithTimeIntervalSince1970:-2147483648],
    [NSDate dateWithTimeIntervalSince1970:2147483647],
    [NSDate dateWithTimeIntervalSince1970:2147483648],
];
    (void)my_data;
}
    return 0;
}
