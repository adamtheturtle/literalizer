#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
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
}
    return 0;
}
