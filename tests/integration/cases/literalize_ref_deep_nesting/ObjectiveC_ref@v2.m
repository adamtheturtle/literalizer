#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id deep = @[
    @[
        @1,
        @2,
    ],
    @[
        @3,
        @4,
    ],
];
id my_data = @{
    @"a": @{
        @"b": @{
            @"c": deep,
        },
    },
};
    (void)my_data;
}
    return 0;
}
