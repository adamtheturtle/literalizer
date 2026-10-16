#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    @"// data",
    @"/* data */",
    @"escaped quote: \" // data",
    @"backslash: \\",
];
    (void)my_data;
}
    return 0;
}
