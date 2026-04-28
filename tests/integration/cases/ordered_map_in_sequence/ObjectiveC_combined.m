#import <Foundation/Foundation.h>
int main(void) {
id my_data = @[
    @{@"a": @1},
    @"hello",
];
(void)my_data;
my_data = @[
    @{@"a": @1},
    @"hello",
];
    (void)my_data;
    return 0;
}
