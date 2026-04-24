#import <Foundation/Foundation.h>
void check_(void) {
id my_data = [NSSet setWithArray:@[
    // before apple
    @"apple",
    @"banana",  // banana inline
    // trailing
]];
(void)my_data;
my_data = [NSSet setWithArray:@[
    // before apple
    @"apple",
    @"banana",  // banana inline
    // trailing
]];
    (void)my_data;
}
