#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"date": @"0099-05-27",
    @"naive": [NSDate dateWithTimeIntervalSince1970:-62135551800],
    @"recent": [NSDate dateWithTimeIntervalSince1970:1716804000],
};
    (void)my_data;
}
    return 0;
}
