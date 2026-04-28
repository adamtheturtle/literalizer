#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"key\nwith\nnewlines": @"value1",
    @"key\twith\ttabs": @"value2",
    @"": @"value3",
};
(void)my_data;
my_data = @{
    @"key\nwith\nnewlines": @"value1",
    @"key\twith\ttabs": @"value2",
    @"": @"value3",
};
    (void)my_data;
}
    return 0;
}
