#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"a": @[@{@"item": @[@1]}],
    @"b": @[@{@"item": @[@2, @3]}],
};
    (void)my_data;
}
    return 0;
}
