#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"value": @{@"$ref": @"foo"},
};
(void)my_data;
my_data = @{
    @"value": @{@"$ref": @"foo"},
};
    (void)my_data;
}
    return 0;
}
