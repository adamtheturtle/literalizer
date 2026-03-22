#import <Foundation/Foundation.h>
void _check(void) {
    id _v = @"hello \"world\" -- not a comment";
    (void)_v;
}
