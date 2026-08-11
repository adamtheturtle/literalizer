#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"schema": @{@"$ref": @"#/defs/Foo"},
};
(void)my_data;
my_data = @{
    @"schema": @{@"$ref": @"#/defs/Foo"},
};
    (void)my_data;
}
    return 0;
}
