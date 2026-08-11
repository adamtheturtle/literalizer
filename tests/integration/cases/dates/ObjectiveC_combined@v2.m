#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"date": [NSDate dateWithTimeIntervalSince1970:1705276800],
    @"datetime": [NSDate dateWithTimeIntervalSince1970:1705321800],
};
(void)my_data;
my_data = @{
    @"date": [NSDate dateWithTimeIntervalSince1970:1705276800],
    @"datetime": [NSDate dateWithTimeIntervalSince1970:1705321800],
};
    (void)my_data;
}
    return 0;
}
