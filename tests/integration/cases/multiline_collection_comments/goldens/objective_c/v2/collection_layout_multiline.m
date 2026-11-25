#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"a": @[
        @1,
        @2,
        @3,
    ],  // inline a
    @"b": @2,  // inline b
};
    (void)my_data;
}
    return 0;
}
