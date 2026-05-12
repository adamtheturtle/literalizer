#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"sibling_lists": @{
        @"numbers": @[
            @1,
            @2,
        ],
        @"strings": @[
            @"x",
            @"y",
        ],
    },
    @"ref_marker_present": @[
        @"$keep",
        @"z",
    ],
};
    (void)my_data;
}
    return 0;
}
