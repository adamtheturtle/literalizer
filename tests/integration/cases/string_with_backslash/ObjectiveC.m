#import <Foundation/Foundation.h>
static void check_(void) {
id my_data = @[
    @"C:\\path\\to\\file",
    @"back\\\\slash",
    @"hello \\\"world\\\"",
    @"path\\to \"# file",
    @"trailing\\",
    @"both \"quotes''' here",
    @"line1\\nline2\nwith newline",
];
    (void)my_data;
}
