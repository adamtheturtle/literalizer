#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"positive": @[@{@"item": @[@2147483648]}],
    @"negative": @[@{@"item": @[@(-2147483649)]}],
    @"mixed": @[@{@"item": @[@0, @2147483648]}],
};
    (void)my_data;
}
    return 0;
}
