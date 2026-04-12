#import <Foundation/Foundation.h>
static void check_(void) {
id my_data = @{
    @"key": @"\"bang!\"",  // real
};
    (void)my_data;
}
