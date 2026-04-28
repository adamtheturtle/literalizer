#import <Foundation/Foundation.h>
int main(void) {
id my_data = @[
    @(INFINITY),
    @(-INFINITY),
    @(NAN),
];
(void)my_data;
my_data = @[
    @(INFINITY),
    @(-INFINITY),
    @(NAN),
];
    (void)my_data;
    return 0;
}
