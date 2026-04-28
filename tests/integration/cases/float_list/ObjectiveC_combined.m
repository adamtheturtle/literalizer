#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @[
    @1.1,
    @(-2.2),
    @3.3,
];
(void)my_data;
my_data = @[
    @1.1,
    @(-2.2),
    @3.3,
];
    (void)my_data;
}
    return 0;
}
