#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"double": @"a b",
    @"single": @"c d",
    @"both": @"e f g",
    @"continued": @"hi",
    @"escaped backslash": @"j\\ k",
};
    (void)my_data;
}
    return 0;
}
