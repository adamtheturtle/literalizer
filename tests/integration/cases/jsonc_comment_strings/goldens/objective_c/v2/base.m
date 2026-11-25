#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    // strings stay data
    @"https://example.org/a/*b*/",  // URL annotation
    @"escaped quote: \" // still data",
    @"backslash: \\",  // outside the string
    @"/* not a comment */",
];
    (void)my_data;
}
    return 0;
}
