#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"a": @1,
    @"b": @"x",
    @"e": @[@1, @2],
    @"f": @{@"g": @"h"},
};
    (void)my_data;
}
    return 0;
}
