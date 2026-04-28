#import <Foundation/Foundation.h>
int main(void) {
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
    return 0;
}
