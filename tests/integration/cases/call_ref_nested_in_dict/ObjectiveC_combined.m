#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    @[@{@"key": @{@"$ref": @"my_var"}, @"count": @42}],
];
(void)my_data;
my_data = @[
    @[@{@"key": @{@"$ref": @"my_var"}, @"count": @42}],
];
    (void)my_data;
}
    return 0;
}
