#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = [NSSet setWithArray:@[
    @1,
    @1099511627776,
]];
(void)my_data;
my_data = [NSSet setWithArray:@[
    @1,
    @1099511627776,
]];
    (void)my_data;
}
    return 0;
}
