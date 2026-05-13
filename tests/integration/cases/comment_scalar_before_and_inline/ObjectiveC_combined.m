#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
// before
// inline
id my_data = @"plain";
(void)my_data;
// before
// inline
my_data = @"plain";
    (void)my_data;
}
    return 0;
}
