#import <Foundation/Foundation.h>
void check_(void) {
id my_data = @{
    @"name": @"Alice",
    @"scores": @{@"1": @"first", @"2": @"second"},
};
(void)my_data;
my_data = @{
    @"name": @"Alice",
    @"scores": @{@"1": @"first", @"2": @"second"},
};
    (void)my_data;
}
