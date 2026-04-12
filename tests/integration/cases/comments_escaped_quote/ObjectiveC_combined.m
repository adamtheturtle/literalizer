#import <Foundation/Foundation.h>
static void check_(void) {
id my_data = @{
    @"key": @"value \" # not a comment",  // real
};
my_data = @{
    @"key": @"value \" # not a comment",  // real
};
    (void)my_data;
}
