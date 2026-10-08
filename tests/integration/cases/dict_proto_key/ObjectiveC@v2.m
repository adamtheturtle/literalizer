#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"__proto__": @{@"x": @1},
    @"n": @{@"__proto__": @3},
    @"y": @2,
};
    (void)my_data;
}
    return 0;
}
