#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"a": @{
        // inner note
        @"b": @1,  // inline b
    },
    @"list": @[
        @1,  // first
        @2,  // second
    ],
};
(void)my_data;
my_data = @{
    @"a": @{
        // inner note
        @"b": @1,  // inline b
    },
    @"list": @[
        @1,  // first
        @2,  // second
    ],
};
    (void)my_data;
}
    return 0;
}
