#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"key": @"\"bang!\"",  // real
};
(void)my_data;
my_data = @{
    @"key": @"\"bang!\"",  // real
};
    (void)my_data;
}
    return 0;
}
