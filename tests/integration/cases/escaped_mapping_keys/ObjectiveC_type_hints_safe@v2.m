#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"quote\"backslash\\": @1,
    @"line\nbreak": @2,
    @"$(literal)${text}": @3,
    @"RStr prefix": @4,
};
    (void)my_data;
}
    return 0;
}
