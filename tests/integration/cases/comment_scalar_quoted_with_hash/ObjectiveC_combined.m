#import <Foundation/Foundation.h>
void check_(void) {
// note
id my_data = @"hello # world";
(void)my_data;
// note
my_data = @"hello # world";
    (void)my_data;
}
