#import <Foundation/Foundation.h>
void check_(void) {
id my_data = @{
    @"key": @"it's here",  // a comment
};
(void)my_data;
my_data = @{
    @"key": @"it's here",  // a comment
};
    (void)my_data;
}
