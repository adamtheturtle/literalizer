#import <Foundation/Foundation.h>
int main(void) {
@autoreleasepool {
id my_data = @"hello \"world\" -- not a comment";
(void)my_data;
my_data = @"hello \"world\" -- not a comment";
    (void)my_data;
}
    return 0;
}
