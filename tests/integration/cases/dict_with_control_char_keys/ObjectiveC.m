#import <Foundation/Foundation.h>
void _check(void) {
    id _v = @{
    @"key\nwith\nnewlines": @"value1",
    @"key\twith\ttabs": @"value2",
    @"": @"value3",
};
    (void)_v;
}
