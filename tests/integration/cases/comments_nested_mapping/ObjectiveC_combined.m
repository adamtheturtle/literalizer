#import <Foundation/Foundation.h>
int main(void) {
id my_data = @{
    @"a": @{@"x": @1},
    @"b": @2,
};
(void)my_data;
my_data = @{
    @"a": @{@"x": @1},
    @"b": @2,
};
    (void)my_data;
    return 0;
}
