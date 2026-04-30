#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    @[@{@"$ref": @"repeated_var"}, @1],
    @[@{@"$ref": @"single_var"}, @0],
    @[@{@"$ref": @"repeated_var"}, @8],
];
(void)my_data;
my_data = @[
    @[@{@"$ref": @"repeated_var"}, @1],
    @[@{@"$ref": @"single_var"}, @0],
    @[@{@"$ref": @"repeated_var"}, @8],
];
    (void)my_data;
}
    return 0;
}
