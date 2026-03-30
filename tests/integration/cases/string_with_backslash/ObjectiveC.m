#import <Foundation/Foundation.h>
void _check(void) {
id my_data = @[
    @"C:\\path\\to\\file",
    @"back\\\\slash",
    @"hello \\\"world\\\"",
    @"path\\to \"# file",
];
    (void)my_data;
}
