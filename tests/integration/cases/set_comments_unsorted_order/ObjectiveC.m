#import <Foundation/Foundation.h>
void _check(void) {
id my_data = [NSSet setWithArray:@[
    // before apple
    @"apple",
    @"banana",  // banana inline
    // trailing
]];
    (void)my_data;
}
