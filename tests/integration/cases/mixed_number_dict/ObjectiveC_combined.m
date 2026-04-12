#import <Foundation/Foundation.h>
static void check_(void) {
id my_data = @{
    @"a": @(1),
    @"b": @(2.5),
    @"c": @(3),
};
my_data = @{
    @"a": @(1),
    @"b": @(2.5),
    @"c": @(3),
};
    (void)my_data;
}
