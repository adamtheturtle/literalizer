#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @{
    @"host": @"it's here",  // a comment
    @"port": @80,  // another
};
(void)my_data;
my_data = @{
    @"host": @"it's here",  // a comment
    @"port": @80,  // another
};
    (void)my_data;
}
    return 0;
}
