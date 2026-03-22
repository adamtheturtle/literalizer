#import <Foundation/Foundation.h>
void _check(void) {
    id _v = [NSSet setWithArray:@[
    @"apple",  // inline comment
    // before banana
    @"banana",
    // trailing
]];
    (void)_v;
}
