#import <Foundation/Foundation.h>
void _check(void) {
id my_data = @[
    @"line1\r\nline2",
    @"line1\rline2",
    @"",
];
    (void)my_data;
}
