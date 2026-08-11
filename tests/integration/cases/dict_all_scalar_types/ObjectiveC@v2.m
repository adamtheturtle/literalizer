#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"s": @"string",
    @"i": @1,
    @"f": @1.5,
    @"b": @YES,
    @"n": [NSNull null],
    @"d": [NSDate dateWithTimeIntervalSince1970:1705276800],
    @"dt": [NSDate dateWithTimeIntervalSince1970:1705320000],
    @"by": @"48656c6c6f",
};
    (void)my_data;
}
    return 0;
}
