#import <Foundation/Foundation.h>
static void check_(void) {
id my_data = @{
    @"a": @{@"x": @(1)},
    @"b": @(2),
};
my_data = @{
    @"a": @{@"x": @(1)},
    @"b": @(2),
};
    (void)my_data;
}
