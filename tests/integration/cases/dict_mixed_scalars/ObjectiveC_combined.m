#import <Foundation/Foundation.h>
void check_(void) {
id my_data = @{
    @"a": @1,
    @"b": @"x",
};
(void)my_data;
my_data = @{
    @"a": @1,
    @"b": @"x",
};
    (void)my_data;
}
