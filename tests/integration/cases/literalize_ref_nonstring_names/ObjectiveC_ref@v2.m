#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id actual = @{
    @"_": @"_",
};
id my_data = @[
    @{@"$ref": @1},
    @{@"$ref": [NSNull null]},
    actual,
];
    (void)my_data;
}
    return 0;
}
