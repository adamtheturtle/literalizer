#import <Foundation/Foundation.h>
void _check(void) {
id my_data = @{
    @"key": @"\"bang!\"",  // real
};
    (void)my_data;
}
