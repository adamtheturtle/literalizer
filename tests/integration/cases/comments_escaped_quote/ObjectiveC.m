#import <Foundation/Foundation.h>
void _check(void) {
    id _v = @{
    @"key": @"value \" # not a comment",  // real
};
    (void)_v;
}
