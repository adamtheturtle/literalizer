#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"key": @"value \" # not a comment",  // real
};
(void)my_data;
my_data = @{
    @"key": @"value \" # not a comment",  // real
};
    (void)my_data;
}
    return 0;
}
