#import <Foundation/Foundation.h>
void check_(void) {
// note
id my_data = @42;
(void)my_data;
// note
my_data = @42;
    (void)my_data;
}
