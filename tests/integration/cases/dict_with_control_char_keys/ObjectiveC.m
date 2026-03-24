#import <Foundation/Foundation.h>
void _check(void) {
id my_data = @{
    @"key\nwith\nnewlines": @"value1",
    @"key\twith\ttabs": @"value2",
    @"": @"value3",
};
    (void)my_data;
}
