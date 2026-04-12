#import <Foundation/Foundation.h>
static void check_(void) {
id my_data = @"hello \"world\" -- not a comment";
my_data = @"hello \"world\" -- not a comment";
    (void)my_data;
}
