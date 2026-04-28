#import <Foundation/Foundation.h>
int main(void) {
id my_data = @9223372036854775808ULL;
(void)my_data;
my_data = @9223372036854775808ULL;
    (void)my_data;
    return 0;
}
