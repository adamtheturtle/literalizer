#import <Foundation/Foundation.h>
void check_(void) {
id my_data = @(42);
(void)my_data;
my_data = @(42);
    (void)my_data;
}
