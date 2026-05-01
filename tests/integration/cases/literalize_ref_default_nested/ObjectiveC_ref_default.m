#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_var = @{
    @"_": @"_",
};
id item_var = @{
    @"_": @"_",
};
id my_data = @{
    @"key": my_var,
    @"items": @[item_var, @{@"fallback": @"value"}],
};
    (void)my_data;
}
    return 0;
}
