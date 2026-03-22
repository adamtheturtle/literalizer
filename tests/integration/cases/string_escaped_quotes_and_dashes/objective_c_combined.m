#import <Foundation/Foundation.h>
void _check(void) {
id my_data = @"hello \"world\" -- not a comment";
my_data = @"hello \"world\" -- not a comment";
    (void)my_data;
}
