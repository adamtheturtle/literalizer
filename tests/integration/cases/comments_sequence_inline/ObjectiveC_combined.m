#import <Foundation/Foundation.h>
int main(void) {
id my_data = @[
    @"a",  // note a
    @"b",  // note b
];
(void)my_data;
my_data = @[
    @"a",  // note a
    @"b",  // note b
];
    (void)my_data;
    return 0;
}
