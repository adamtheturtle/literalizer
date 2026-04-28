#import <Foundation/Foundation.h>
int main(void) {
id my_data = @[
    @42,
    @3.14,
    @YES,
    @NO,
    @"hello \"world\"",
];
(void)my_data;
my_data = @[
    @42,
    @3.14,
    @YES,
    @NO,
    @"hello \"world\"",
];
    (void)my_data;
    return 0;
}
