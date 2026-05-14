#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"my-key": @"value1",
    @"another-key": @"value2",
    @"normal_key": @"value3",
};
(void)my_data;
my_data = @{
    @"my-key": @"value1",
    @"another-key": @"value2",
    @"normal_key": @"value3",
};
    (void)my_data;
}
    return 0;
}
