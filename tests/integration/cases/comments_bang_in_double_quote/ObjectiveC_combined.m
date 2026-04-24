#import <Foundation/Foundation.h>
void check_(void) {
id my_data = @{
    @"key": @"\"bang!\"",  // real
};
(void)my_data;
my_data = @{
    @"key": @"\"bang!\"",  // real
};
    (void)my_data;
}
