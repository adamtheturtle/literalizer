#import <Foundation/Foundation.h>
int main(void) {
id my_data = @[
    @[@[@1, @2], @[@"a", @"b"]],
];
(void)my_data;
my_data = @[
    @[@[@1, @2], @[@"a", @"b"]],
];
    (void)my_data;
    return 0;
}
