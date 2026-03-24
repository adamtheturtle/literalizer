#import <Foundation/Foundation.h>
void _check(void) {
id my_data = [NSSet setWithArray:@[
    @"apple",  // inline comment
    // before banana
    @"banana",
    // trailing
]];
    (void)my_data;
}
