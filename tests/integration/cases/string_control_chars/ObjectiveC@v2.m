#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    @"line1\r\nline2",
    @"line1\rline2",
    @"\001",
];
    (void)my_data;
}
    return 0;
}
