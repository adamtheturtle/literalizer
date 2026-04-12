#import <Foundation/Foundation.h>
static void check_(void) {
id my_data = [NSSet setWithArray:@[
    @"apple",  // inline comment
    // before banana
    @"banana",
    // trailing
]];
    (void)my_data;
}
