#import <Foundation/Foundation.h>
void _check(void) {
    id _v = [NSSet setWithArray:@[
    // before apple
    @"apple",
    @"banana",  // banana inline
    // trailing
]];
    (void)_v;
}
