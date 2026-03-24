#import <Foundation/Foundation.h>
void _check(void) {
    id _v = @{
    @"key": @"\"bang!\"",  // real
};
    (void)_v;
}
