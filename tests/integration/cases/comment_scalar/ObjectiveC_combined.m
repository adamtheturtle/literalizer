#import <Foundation/Foundation.h>
int main(void) {
// note
id my_data = @42;
(void)my_data;
// note
my_data = @42;
    (void)my_data;
    return 0;
}
