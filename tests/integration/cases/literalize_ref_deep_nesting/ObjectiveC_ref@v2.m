#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id deep = @[
    @[
        @"one",
        @"two",
    ],
    @[
        @"three",
        @"four",
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
