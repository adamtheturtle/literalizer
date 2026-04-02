#import <Foundation/Foundation.h>
void _check(void) {
id my_data = @{
    @"my-key": @"value1",
    @"another-key": @"value2",
    @"normal_key": @"value3",
};
my_data = @{
    @"my-key": @"value1",
    @"another-key": @"value2",
    @"normal_key": @"value3",
};
    (void)my_data;
}
