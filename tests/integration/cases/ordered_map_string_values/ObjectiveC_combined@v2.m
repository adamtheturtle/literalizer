#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"first": @"one",
    @"second": @"two",
    @"third": @"three",
};
(void)my_data;
my_data = @{
    @"first": @"one",
    @"second": @"two",
    @"third": @"three",
};
    (void)my_data;
}
    return 0;
}
