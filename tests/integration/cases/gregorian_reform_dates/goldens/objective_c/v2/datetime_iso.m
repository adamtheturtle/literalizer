#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"ancient_date": [NSDate dateWithTimeIntervalSince1970:-14826672000],
    @"modern_date": [NSDate dateWithTimeIntervalSince1970:1705276800],
    @"before_date": [NSDate dateWithTimeIntervalSince1970:-12220243200],
    @"gap_date": [NSDate dateWithTimeIntervalSince1970:-12219724800],
    @"transition_date": [NSDate dateWithTimeIntervalSince1970:-12219292800],
    @"after_date": [NSDate dateWithTimeIntervalSince1970:-12219206400],
    @"before_naive": @"1582-10-04T12:30:00.000001",
    @"gap_naive": @"1582-10-10T12:30:00.500000",
    @"transition_positive": @"1582-10-15T00:30:00+18:00",
    @"transition_negative": @"1582-10-15T23:30:00-18:00",
    @"after_positive": @"1582-10-16T00:30:00+18:00",
};
    (void)my_data;
}
    return 0;
}
