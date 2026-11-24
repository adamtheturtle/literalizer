#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"ancient_date": @"1500-03-01",
    @"modern_date": @"2024-01-15",
    @"before_date": @"1582-10-04",
    @"gap_date": @"1582-10-10",
    @"transition_date": @"1582-10-15",
    @"after_date": @"1582-10-16",
    @"before_naive": [NSDate dateWithTimeIntervalSince1970:-12220198199.999999],
    @"gap_naive": [NSDate dateWithTimeIntervalSince1970:-12219679799.5],
    @"transition_positive": [NSDate dateWithTimeIntervalSince1970:-12219355800],
    @"transition_negative": [NSDate dateWithTimeIntervalSince1970:-12219143400],
    @"after_positive": [NSDate dateWithTimeIntervalSince1970:-12219269400],
};
    (void)my_data;
}
    return 0;
}
