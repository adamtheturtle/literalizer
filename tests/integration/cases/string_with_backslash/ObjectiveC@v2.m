#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
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
    return 0;
}
