#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id item_var = @{
    @"_": @"_",
};
id my_data = @{
    @"items": @[item_var, @{@"fallback": @"value"}],
};
    (void)my_data;
}
    return 0;
}
