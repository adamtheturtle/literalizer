#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    @[@[@{@"$ref": @"my_var"}, @42, @"static"]],
    @[@[@{@"$ref": @"my_other"}, @7, @"label"]],
];
    (void)my_data;
}
    return 0;
}
