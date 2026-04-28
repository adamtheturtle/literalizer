#import <Foundation/Foundation.h>
int main(void) {
id my_data = [NSSet setWithArray:@[
    @YES,
    @42,
    @"apple",
]];
(void)my_data;
my_data = [NSSet setWithArray:@[
    @YES,
    @42,
    @"apple",
]];
    (void)my_data;
    return 0;
}
