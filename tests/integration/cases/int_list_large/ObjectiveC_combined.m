#import <Foundation/Foundation.h>
int main(void) {
id my_data = @[
    @1000000,
    @(-1234),
    @255,
    @(-10),
];
(void)my_data;
my_data = @[
    @1000000,
    @(-1234),
    @255,
    @(-10),
];
    (void)my_data;
    return 0;
}
