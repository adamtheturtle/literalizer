#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"0a": @"first",
    @"1b": @"second",
};
(void)my_data;
my_data = @{
    @"0a": @"first",
    @"1b": @"second",
};
    (void)my_data;
}
    return 0;
}
