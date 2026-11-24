#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"v": [[@((const char[]){'\141', '\342', '\200', '\252', '\000'}) stringByAppendingString:@"\000"] stringByAppendingString:@"é😀b"],
};
    (void)my_data;
}
    return 0;
}
