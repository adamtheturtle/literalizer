#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    @"foo",
    @"bar",
    @"baz",
];
(void)my_data;
my_data = @[
    @"foo",
    @"bar",
    @"baz",
];
    (void)my_data;
}
    return 0;
}
