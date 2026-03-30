#import <Foundation/Foundation.h>
void _check(void) {
id my_data = @[
    @"C:\\path\\to\\file",
    @"back\\\\slash",
    @"hello \\\"world\\\"",
    @"path\\to \"# file",
    @"trailing\\",
    @"both \"quotes''' here",
];
    (void)my_data;
}
