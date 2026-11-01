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
